"""The arena: a fake game server with the duel rules, rival bots (Duels I's five types x how they handle the day),
and a stepped driver that plays sessions through the real `DuelRunner` / `DuelAgent` code.

Economics: each side has a limit at its own best day and a linear weight on the day (0 at its best day). The pie of
a duel is the best total surplus over the days; our points proxy is our true surplus x (1 - decay)^rounds / pie
(the Duel Lab's share-based score). Rival bots think in "worth" (their surplus at their own best day): a day-aware
bot prices its day in, a day-blind one ignores it.
"""
from __future__ import annotations

import asyncio
import math
import random
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from bazaar_sdk import BazaarError

from agents.duelist import agent as A
from agents.duelist.agent import BandPlan, Decision, DuelAgent, day_read, our_offers, standing_offer
from agents.duelist.guards import claims, price_at, worth
from agents.duelist import runner as R
from agents.duelist.runner import DuelRunner, Log
from engine import LLMError

from . import SCRATCH

R.say = lambda msg: None                    # the runner's console lines: off in the arena

DUEL_TICKS = 16
DECAY = 0.08
SESSION = 3
TEAM = "Team 5"
SESSION_PARAMS = {"session": SESSION, "name": "Duels II", "rounds": 2, "duel_ticks": DUEL_TICKS, "decay": DECAY,
                  "max_concurrent": 6, "issues": ["price", "days"]}
KINDS = ["follower", "clock", "holder", "holder7", "acceptonly", "silent"]
DAY_MODES = ["own", "zero", "middle", "copy", "trade", "none", "flip"]
SHAPES = ["words", "signed", "list", "dict", "unsure", "unreadable", "wrong_unit"]


@dataclass
class Side:
    role: str            # seller | buyer
    limit: int           # seller: cost; buyer: value; at its own best day
    w: float             # cost per day away from its best day
    prefer: str          # early | late

    @property
    def s(self) -> int:
        return 1 if self.role == "seller" else -1

    @property
    def best(self) -> int:
        return 0 if self.prefer == "early" else 10

    def day(self, d: int | None) -> float:
        if d is None:
            d = 10 - self.best                       # a missing day counts as the worst
        d = min(max(int(d), 0), 10)
        return -self.w * (d if self.prefer == "early" else 10 - d)

    def worth(self, price: float, d: int | None, blind: bool = False) -> float:
        return self.s * (price - self.limit) + (0.0 if blind else self.day(d))

    def price(self, w: float, d: int | None, blind: bool = False) -> float:
        return self.limit + self.s * (w - (0.0 if blind else self.day(d)))


def present(side: Side, shape: str) -> tuple[Any, str | None]:
    """How the game might state our day weight (the real shape was never seen before Duels II)."""
    w, early = side.w, side.prefer == "early"
    later = "later" if early else "earlier"
    if shape == "words":
        return w, f"each day {later} costs you {w:g} P"
    if shape == "signed":
        return (-w if early else w), None
    if shape == "list":
        return [side.day(d) for d in range(11)], None
    if shape == "dict":
        return {"per_day": w, "prefers": "early" if early else "late"}, None
    if shape == "unsure":
        return w, "your weight per day of delivery"
    if shape == "unreadable":
        return {"k": w, "curve": "linear", "side": "early" if early else "late"}, None
    if shape == "flipped":                          # we read the wrong direction
        return w, f"each day {'earlier' if early else 'later'} costs you {w:g} P"
    if shape == "wrong_unit":                       # the game means 3x what the number says
        return round(w / 3, 2), f"each day {later} costs you {w / 3:g} P"
    raise ValueError(shape)


@dataclass
class Bot:
    """A rival. kind: Duels I's types (docs/duel-rivals.md); days: how it handles the delivery day."""
    kind: str
    days: str
    side: Side
    pie: float
    has_days: bool
    rng: random.Random

    def __post_init__(self) -> None:
        r = self.rng
        self.open = self.pie * r.uniform(1.0, 1.8)          # rivals ask ~1.4x the pie on median (Duel Lab)
        self.floor = self.pie * r.uniform(0.05, 0.4)
        self.shape = r.choice(["linear", "accel", "slow", "burst"])
        self.tau = r.uniform(0.06, 0.42)
        self.sent = 0
        self.last_w: float | None = None

    @property
    def blind(self) -> bool:
        return not self.has_days or self.days in ("zero", "middle", "flip", "none", "copy")

    def their_day(self, ours_day: int | None, k: int) -> int | None:
        if not self.has_days or self.days == "none":
            return None
        b = self.side.best
        return {"own": b, "zero": 0, "middle": 5, "copy": b if ours_day is None else ours_day,
                "trade": b if ours_day is None else ours_day, "flip": 0 if k % 2 == 0 else 10}[self.days]

    def offer(self, w: float, ours: tuple | None, k: int) -> tuple:
        day = self.their_day(ours[1] if ours else None, k)
        price = round(self.side.price(w, day, blind=self.blind))
        self.last_w, self.sent = w, self.sent + 1
        return ("say", f"I can do {price} P." + (f" Delivery on day {day}." if day is not None else ""), price, day)

    def act(self, d: "DuelState", tick: int) -> tuple | None:
        k, left = tick - d.start, d.deadline - tick
        ours = d.standing(mine=True)
        w_ours = self.side.worth(ours[0], ours[1], blind=self.blind) if ours else None
        if self.kind == "silent":
            return None
        if self.kind == "acceptonly":
            if self.sent == 0 and self.rng.random() < 0.5:
                self.sent += 1
                return ("say", "Hola.", None, None)
            if ours and left <= 3 and w_ours >= self.tau * self.pie * (0.5 if left <= 1 else 1):
                return ("accept",)
            return None
        if self.kind == "holder":                            # R5: one number, takes ours once inside its limit
            if ours and w_ours >= self.floor:
                return ("accept",)
            return self.offer(self.floor + 0.3 * self.pie, ours, k) if self.sent == 0 else None
        if self.kind == "holder7":                           # R7: 3 moves, then silent, never accepts
            return self.offer(self.open - 0.15 * self.pie * self.sent, ours, k) if self.sent < 4 else None
        if self.kind == "clock":                             # its own schedule, whatever we do
            x = min(k / (DUEL_TICKS - 3), 1.0)
            f = {"linear": x, "accel": x * x, "slow": math.sqrt(x),
                 "burst": min(math.floor(k / 3) * 3 / (DUEL_TICKS - 3), 1.0)}[self.shape]
            w = self.open + (self.floor - self.open) * f
            if ours and w_ours >= max(w, self.floor):
                return ("accept",)
            return self.offer(w, ours, k)
        if self.kind == "follower":                          # comes to our number
            if self.last_w is None:
                return self.offer(self.open, ours, k)
            if ours is None:
                return None
            if w_ours >= self.last_w:
                return ("accept",)
            if w_ours >= self.floor and self.last_w - w_ours <= max(1.0, 0.08 * self.pie):
                return self.offer(w_ours, ours, k)           # ends on our exact number (R16)
            w = max(self.floor, w_ours + 0.5 * (self.last_w - w_ours))
            return None if w >= self.last_w - 0.5 else self.offer(w, ours, k)
        raise ValueError(self.kind)


@dataclass
class DuelState:
    id: int
    start: int
    us: Side
    rival: Side
    bot: Bot
    has_days: bool
    shape: str
    weight: Any
    meaning: str | None
    alias: str = "Rival Sol"
    item: str = "a Malasaña rare card"
    messages: list[dict[str, Any]] = field(default_factory=list)
    status: str = "live"
    deal: dict[str, Any] | None = None
    said: dict[str, int] = field(default_factory=dict)      # side -> tick of its last message
    refusals: Counter = field(default_factory=Counter)
    tags: dict[str, Any] = field(default_factory=dict)

    @property
    def deadline(self) -> int:
        return self.start + DUEL_TICKS

    def standing(self, mine: bool) -> tuple[int, int | None] | None:
        for m in reversed(self.messages):
            if (m["from"] == "you") == mine and m.get("price") is not None:
                return m["price"], m.get("days")
        return None

    def rounds(self) -> int:
        ours = sum(m["from"] == "you" for m in self.messages)
        return min(ours, len(self.messages) - ours)

    def pie_at(self, d: int | None) -> float:
        buyer, seller = (self.us, self.rival) if self.us.role == "buyer" else (self.rival, self.us)
        return buyer.limit - seller.limit + self.us.day(d) + self.rival.day(d)

    @property
    def pie(self) -> float:
        return max(self.pie_at(d) for d in range(11)) if self.has_days else self.pie_at(None)

    def payload(self) -> dict[str, Any]:
        def off(o: tuple | None) -> dict | None:
            return None if o is None else {"price": o[0], "days": o[1] if self.has_days else 0}
        return {"duel": self.id, "session": SESSION, "status": self.status, "role": self.us.role, "item": self.item,
                "issues": ["price", "days"] if self.has_days else ["price"],
                "your_days_weight": self.weight if self.has_days else None,
                "days_meaning": self.meaning if self.has_days else None, "your_limit": self.us.limit,
                "limit_meaning": "never sell below your cost" if self.us.role == "seller" else
                "never pay more than your value", "rival": self.alias, "deadline_tick": self.deadline,
                "decay_per_round": DECAY, "rounds": self.rounds(), "your_offer": off(self.standing(True)),
                "rival_offer": off(self.standing(False)), "messages": [dict(m) for m in self.messages]}

    def say(self, who: str, tick: int, text: str, price: int | None, days: int | None) -> None:
        if self.status != "live" or tick >= self.deadline:
            raise BazaarError("duel_closed", "the duel is over", 409)
        if self.said.get(who) == tick:
            raise BazaarError("wait_for_tick", "one message per tick", 429)
        if price is not None and self.has_days and days is None:
            raise BazaarError("missing_days", "a priced message needs days", 400)
        if days is not None and (not isinstance(days, int) or not 0 <= days <= 10):
            raise BazaarError("bad_days", "days must be 0-10", 400)
        if len(text) > 1200:
            raise BazaarError("too_long", "text too long", 400)
        self.said[who] = tick
        self.messages.append({"tick": tick, "from": "you" if who == "us" else self.alias, "text": text,
                              "price": price, "days": days if self.has_days else None})

    def accept(self, who: str, tick: int) -> None:
        if self.status != "live" or tick >= self.deadline:
            raise BazaarError("duel_closed", "the duel is over", 409)
        o = self.standing(mine=(who != "us"))
        if o is None:
            raise BazaarError("no_offer", "nothing to accept", 409)
        self.status = "deal"
        self.deal = {"price": o[0], "days": o[1], "tick": tick, "rounds": self.rounds(), "by": who}


class FakeServer:
    """The SDK calls the runner makes, on the duel rules. `faults` injects trouble: {"say": f(did, tick) ->
    BazaarError | None, "poll": f(tick) -> bool (True: the read fails)}."""

    def __init__(self, duels: list[DuelState], tick: int, tick_seconds: float = 30.0,
                 faults: dict[str, Any] | None = None):
        self.d = {x.id: x for x in duels}
        self.tick, self.tick_seconds = tick, tick_seconds
        self.faults = faults or {}
        self.calls: Counter = Counter()

    def clock(self) -> dict:
        self.calls["clock"] += 1
        return {"tick": self.tick, "tick_seconds": self.tick_seconds, "t_hours": 11.7, "doors": "open", "paused": False}

    def me(self) -> dict:
        return {"id": "t05", "name": TEAM, "score": {}}

    def schedule(self) -> dict:
        return {"upcoming": []}

    def feed(self, limit: int = 150) -> dict:
        return {"events": [{"type": "duels.scheduled", "tick": 0, "payload": SESSION_PARAMS}]}

    def duels(self, done: bool = False) -> dict:
        self.calls["duels"] += 1
        if (f := self.faults.get("poll")) and f(self.tick):
            raise BazaarError("server_error", "poll failed", 500)
        out = [x.payload() for x in self.d.values() if (x.status != "live") == done]
        if (m := self.faults.get("mutate")):
            out = [m(raw, self.tick) for raw in out]
        return {"duels": out}

    def duel_say(self, did: int, text: str = "", price: int | None = None, days: int | None = None) -> dict:
        self.calls["say"] += 1
        if (f := self.faults.get("say")) and (e := f(did, self.tick)):
            raise e
        try:
            self.d[did].say("us", self.tick, text, price, days)
        except BazaarError as e:
            self.d[did].refusals[e.code] += 1
            raise
        return {"ok": True}

    def duel_accept(self, did: int) -> dict:
        self.calls["accept"] += 1
        if (f := self.faults.get("say")) and (e := f(did, self.tick)):
            raise e
        try:
            self.d[did].accept("us", self.tick)
        except BazaarError as e:
            self.d[did].refusals[e.code] += 1
            raise
        return {"ok": True}

    def bots_act(self) -> None:
        for x in self.d.values():
            if x.status != "live" or self.tick >= x.deadline:
                continue
            act = x.bot.act(x, self.tick)
            try:
                if act and act[0] == "say":
                    x.say("rival", self.tick, act[1], act[2], act[3])
                elif act and act[0] == "accept":
                    x.accept("rival", self.tick)
            except BazaarError as e:
                x.refusals["rival:" + e.code] += 1

    def expire(self) -> None:
        for x in self.d.values():
            if x.status == "live" and self.tick >= x.deadline:
                x.status = "no_deal"


# Scenarios

def scenario(i: int, rng: random.Random, kind: str, days: str, shape: str, role: str,
             has_days: bool = True) -> DuelState:
    L = rng.randint(40, 150)
    w_u, w_r = (rng.choice([0.5, 1, 2, 3, 4]) for _ in range(2)) if has_days else (0.0, 0.0)
    pu, pr = rng.choice(["early", "late"]), rng.choice(["early", "late"])
    pie = round(L * rng.uniform(0.12, 0.6))
    if pu != pr:
        pie = max(pie, math.ceil(10 * min(w_u, w_r)) + 6)
    us = Side(role, L, w_u, pu)
    rival = Side("buyer" if role == "seller" else "seller", L + pie if role == "seller" else L - pie, w_r, pr)
    weight, meaning = present(us, shape) if has_days else (None, None)
    bot = Bot(kind, days, rival, pie, has_days, random.Random(rng.random()))
    return DuelState(i, 0, us, rival, bot, has_days, shape, weight, meaning,
                     tags={"kind": kind, "days": days, "shape": shape, "role": role})


# The models: a code stand-in for the LLMs (experiment 1's bulk runs), and one that always fails

OPEN_SHARE = {"seller": 0.5, "buyer": 0.35}        # our openers: seller ~1.5x limit, buyer ~0.65x


async def policy_plan(self: DuelAgent, obs) -> BandPlan:
    """The strategist as its prompt asks: open far, then 15% of the gap (40% in the last 3 ticks), the day by the
    ledger's day call (take / give with a premium of C / hold / menu = hold)."""
    v, ours, their = self.view, our_offers(obs), standing_offer(obs)
    dv, day, r = v.day_values, None, None
    if v.has_days:
        r = day_read(obs)
        last = ours[-1].days if ours and ours[-1].days is not None else (dv.best if dv else 5)
        day = last if r is None else {"take": r.their_day, "give": r.their_day, "menu": r.our_day,
                                       "hold": r.best_day if r.middle else r.our_day}[r.call]
    if not ours:
        tw = OPEN_SHARE[v.role.value] * v.limit
    else:
        now = tw = worth(v, ours[-1].price, ours[-1].days)
        share = 0.15 if (obs.ticks_left or 9) > 3 else 0.4
        if their is not None and (gap := now - worth(v, their.price, their.days)) > 0:
            tw = now - share * gap
        elif their is None:
            tw = now * (1 - share)          # no offer from them: walk toward our limit, as the models did in Duels I
    if r is not None and r.call == "give" and (not ours or ours[-1].days != day):
        tw += r.cost
    target = A.toward_us(self.s, price_at(v, max(tw, 0.0), day))
    return BandPlan(read="policy", target=target, best=target, worst=target, days=day, angle="plain")


async def policy_negotiate(self: DuelAgent, obs, band, plan, days, feedback) -> Decision:
    their = standing_offer(obs)
    if their is not None and worth(self.view, their.price, their.days) >= worth(self.view, band.target, days):
        return Decision(action="accept", price=their.price, message="Agreed.")
    return Decision(action="offer", price=band.target,
                    message=f"I can do {band.target} P" + (f", delivery on day {days}." if days is not None else "."))


def use_policy() -> None:
    DuelAgent.plan = policy_plan            # type: ignore[method-assign]
    DuelAgent.negotiate = policy_negotiate  # type: ignore[method-assign]


class NoModel:
    label = "none"

    async def parse(self, schema, system, messages):
        raise LLMError("no model in this run")


# The driver

def new_runner(server: FakeServer, strategist, negotiator, tick_seconds: float, name: str = "arena") -> DuelRunner:
    r = DuelRunner(server, strategist, negotiator, dry_run=False, log=Log(SCRATCH / "logs" / name), decay=None,
                   duel_ticks=None, poll_s=0, records=None)
    r.team, r.sessions, r.tick_seconds = {"t05", TEAM}, {SESSION: dict(SESSION_PARAMS)}, tick_seconds
    return r


async def play(duels: list[DuelState], strategist=None, negotiator=None, *, start: int = 1000,
               tick_seconds: float = 30.0, faults: dict | None = None, restart_at: int | None = None,
               name: str = "arena") -> tuple[FakeServer, DuelRunner]:
    """One wave, tick by tick: the rivals move, then the runner polls and decides (all due duels at once)."""
    for x in duels:
        x.start = start
    server = FakeServer(duels, start, tick_seconds, faults)
    strategist, negotiator = strategist or NoModel(), negotiator or strategist or NoModel()
    r = new_runner(server, strategist, negotiator, tick_seconds, name)
    for tick in range(start, start + DUEL_TICKS + 1):
        server.tick = r.tick = tick
        server.expire()
        server.bots_act()
        if restart_at == tick:
            old, r = r, new_runner(server, strategist, negotiator, tick_seconds, name)
            r.spent_usd = old.spent_usd
        try:
            live = server.duels()["duels"]
        except BazaarError:
            continue
        mems = [m for raw in live if (m := r.update(raw)) is not None]
        await asyncio.gather(*(r._decide(m) for m in mems if r.due(m)))
    server.tick = start + DUEL_TICKS
    server.expire()
    return server, r


def result(x: DuelState, r: DuelRunner) -> dict[str, Any]:
    """One duel's outcome against the truth, and the invariants."""
    mem = r.duels.get(x.id)
    view = mem.agent.view if mem else None
    ours = [m for m in x.messages if m["from"] == "you"]
    row: dict[str, Any] = {**x.tags, "id": x.id, "deal": x.status == "deal", "rounds": x.rounds(),
                           "pie": round(x.pie, 1), "our_msgs": len(ours), "refusals": dict(x.refusals),
                           "read": view.day_values.how if view and view.day_values else None}
    row["points"] = 0.0
    if x.deal:
        p, d = x.deal["price"], x.deal["days"]
        true = x.us.worth(p, d)
        row.update(price=p, day=d, by=x.deal["by"], true=round(true, 2), rounds=x.deal["rounds"],
                   points=true * (1 - DECAY) ** x.deal["rounds"] / x.pie,
                   day_gap=round(x.pie - x.pie_at(d), 1) if x.has_days else 0.0,
                   read_worth=round(worth(view, p, d), 2) if view else None)
    bad = []
    if x.deal and row["true"] < -1e-9:
        bad.append("negative deal (true weight)")
    if x.deal and row.get("read_worth") is not None and row["read_worth"] < -1e-9:
        bad.append("negative deal (our own reading)")
    for m in ours:
        if m["price"] is not None and x.us.worth(m["price"], m["days"]) < -1e-9:
            bad.append("offer past the true limit")
            break
    for m in ours:
        if view and (found := claims(view, m["text"], m["price"], m["days"])):
            bad.append("claim words/stray numbers sent")
            row["claim_text"] = (m["text"], m["price"], m["days"], found)
            break
    if x.refusals.get("missing_days") or x.refusals.get("bad_days"):
        bad.append("refused: " + ",".join(k for k in ("missing_days", "bad_days") if x.refusals.get(k)))
    row["bad"] = bad
    return row


def run_waves(scen: list[DuelState], **kw) -> list[dict[str, Any]]:
    """Waves of up to 6 duels, as in Duels II."""
    rows: list[dict[str, Any]] = []
    for i in range(0, len(scen), 6):
        wave = scen[i:i + 6]
        server, r = asyncio.run(play(wave, **kw))
        rows += [result(x, r) for x in wave]
    return rows
