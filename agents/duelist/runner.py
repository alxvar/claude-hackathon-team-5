"""The duel loop: poll the game, let the agent decide for each live duel that needs a move, send the move.

A duel needs a move when the rival has moved, in its last DECIDE_LEFT ticks whatever the rival does, when both
sides have sat still for HOLD_TICKS ticks, when a rival that has said nothing is due our next step
(`silent_rival`: code, no model), and when code should accept its standing offer (`closer`): the
deadline can't wait, or the gap is smaller than what one more round risks. When our acceptance must wait for the
team's one acceptance per tick, we offer the rival its own price instead, if that costs no round (`their_price`).
With days, the code rules weigh whole packages (`guards.worth`); a days duel whose weight we can't read stays with
the models (`by_code`).

Rules it keeps (RULES.md): one message per duel per tick, one acceptance per team per tick, 5 requests a second
per key. A poll is two reads (`clock`, `duels`) every `poll_s` seconds while a duel is live, every IDLE_POLL_S (at
most a third of a tick) while none is, since the key's 5 requests a second are the team's; each duel then costs one
write per tick at most. The SDK is synchronous, so every call runs in a thread and the model calls of several duels overlap.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from bazaar_sdk import Bazaar, BazaarError
from engine import Model

from .adapter import Snapshot, parse_duel
from .agent import DuelAgent, Move, our_offers, silent, standing_offer, still_ticks, swing, their_offers
from .guards import past_limit, worth
from .model import DuelView, Observation, Offer, Turn
from .prices import money
from .records import Records, duel_key, ended, sessions_in

DECIDE_LEFT = 3     # ticks left at or below which we decide every tick, whether or not the rival has moved
ACCEPT_BY = 2       # every standing offer inside our limit is accepted by this many ticks left (1, the last, is spare)
HOLD_TICKS = 3      # both sides still this long, once the rival has offered: decide again (duels 103/104)
IDLE_POLL_S = 10.0  # no duel live: poll this often, or every third of a tick if that is shorter


class Log:
    """Everything to one JSONL file: raw payloads (when they change), decisions, sends, errors."""

    def __init__(self, folder: Path):
        folder.mkdir(parents=True, exist_ok=True)
        self.path = folder / f"duels-{datetime.now():%Y%m%d-%H%M%S}.jsonl"
        self._seen: dict[str, str] = {}

    def write(self, event: str, **data: Any) -> None:
        with self.path.open("a") as f:
            f.write(json.dumps({"ts": round(time.time(), 2), "event": event, **data}, default=str) + "\n")

    def changed(self, key: str, payload: Any) -> bool:
        h = hashlib.sha1(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
        if self._seen.get(key) == h:
            return False
        self._seen[key] = h
        return True


def say(msg: str) -> None:
    print(f"{datetime.now():%H:%M:%S} {msg}", flush=True)


@dataclass
class Memory:
    """What we remember about one duel between polls."""
    agent: DuelAgent
    snap: Snapshot
    sent: list[Turn] = field(default_factory=list)       # our messages, with the decision behind each
    seen: list[Turn] = field(default_factory=list)       # their offers as we saw them change (no message list)
    decided_on: Any = None                               # the rival's state our last move answered
    sent_tick: int | None = None
    decided_tick: int | None = None                      # the tick of our last decision: one per tick
    task: asyncio.Task | None = None
    pending: tuple[Move, Any, int | None] | None = None  # a move held back on its tick, for the next one
    force: bool = False                                  # decide again even if the rival hasn't moved


def by_code(v: DuelView) -> bool:
    """Code may play this duel's rules (accepts, their price, the silent walk): price only, or days with a weight
    we can read, so every package has a worth."""
    return not v.has_days or v.day_values is not None


def signature(snap: Snapshot) -> Any:
    """The rival's state that a new move from us answers: its offers as they changed. A message that repeats its
    standing offer (same price and day), or carries no price, is not a move (duel 278: Rival Oro sent 111 every
    tick, we answered every tick, 10 rounds: 2.7 instead of 4.7)."""
    offers: list[tuple[int, int | None]] = []
    for o in [*(t.offer for t in (snap.messages or []) if not t.mine), snap.rival_offer]:
        if o is not None and (not offers or offers[-1] != (o.price, o.days)):
            offers.append((o.price, o.days))
    return json.dumps(offers)


def answered(msgs: list[Turn]) -> bool:
    """Our side has sent something since the rival's current offer first appeared (its repeats don't count)."""
    start, last = -1, None
    for i, t in enumerate(msgs):
        if not t.mine and t.offer is not None and (t.offer.price, t.offer.days) != last:
            start, last = i, (t.offer.price, t.offer.days)
    return any(t.mine for t in msgs[start + 1:])


class DuelRunner:
    def __init__(self, b: Bazaar, strategist: Model, negotiator: Model, *, dry_run: bool, log: Log,
                 decay: float | None, duel_ticks: int | None, poll_s: float, records: Records | None = None):
        self.b = b
        self.strategist, self.negotiator = strategist, negotiator
        self.dry_run = dry_run
        self.log = log
        self.overrides = {k: v for k, v in (("decay", decay), ("duel_ticks", duel_ticks)) if v is not None}
        self.upcoming: dict[str, Any] = {}      # the next duel session on the schedule, for the console
        self.sessions: dict[Any, dict[str, Any]] = records.sessions() if records else {}   # by number, from the feed
        self.sessions_read = 0.0                # when we last read the feed for them
        self.poll_s = poll_s
        self.team: set[str] = set()
        self.duels: dict[Any, Memory] = {}
        self.tick: int | None = None
        self.tick_seconds = 60.0
        self.accepted_tick: int | None = None   # one acceptance per team per tick
        self.spent_usd = 0.0
        self.swings: dict[Any, dict[Any, float]] = {}   # session -> duel -> our day weight's size, for its rank
        self.records = records

    def record(self, key: Any, **fields: Any) -> None:
        """Into the duel's record; a failure here must never stop a duel."""
        if self.records is None:
            return
        try:
            self.records.save(key, **fields)
        except Exception as e:
            self.log.write("error", where="record", duel=key, error=repr(e))

    async def call(self, fn, *args, **kw):
        return await asyncio.to_thread(fn, *args, **kw)

    def wait_s(self, live: list[dict[str, Any]]) -> float:
        """Seconds to the next poll: `poll_s` while any duel is live or still ours to finish; otherwise up to
        IDLE_POLL_S, never more than a third of a tick, so a new duel is seen early in its first tick."""
        if live or self.duels:
            return self.poll_s
        return max(self.poll_s, min(IDLE_POLL_S, self.tick_seconds / 3))

    # The session's params

    async def refresh_session(self, now_hours: float | None = None) -> None:
        """The next duel session on the schedule, for the console. Never a live duel's params: the schedule lists
        only sessions still to come, so once one starts it shows the one after (Friday's practice records say
        "Duels I" for that reason)."""
        try:
            sched = await self.call(self.b.schedule)
        except BazaarError as e:
            self.log.write("error", where="schedule", error=str(e))
            return
        nxt = next((u for u in sched.get("upcoming", []) if u.get("action") == "duels"), None)
        if nxt and nxt != self.upcoming:
            self.upcoming = nxt
            p = nxt.get("params") or {}
            self.log.write("upcoming_session", at_hours=nxt.get("at_hours"), params=p)
            say(f"next duel session: {p.get('name')} at hour {nxt.get('at_hours')}, {p.get('duel_ticks')} ticks, "
                f"decay {p.get('decay')}, {p.get('max_concurrent')} at once, issues {p.get('issues', ['price'])}")

    def learn_sessions(self, events: list[dict[str, Any]]) -> None:
        for num, params in sessions_in(events).items():
            if num not in self.sessions:
                self.sessions[num] = params
                self.log.write("session", params=params)
                say(f"duel session {num}: {params.get('name')}, {params.get('duel_ticks')} ticks, "
                    f"decay {params.get('decay')}")

    async def read_sessions(self) -> None:
        """A live duel's session we don't know yet: its `duels.scheduled` event is on the feed (the feed keeps
        only the last few hundred events, so this runs as soon as the duel shows up)."""
        self.sessions_read = time.monotonic()
        try:
            self.learn_sessions((await self.call(self.b.feed, 500)).get("events", []))
        except Exception as e:
            self.log.write("error", where="sessions", error=repr(e))

    def defaults(self, raw: dict[str, Any]) -> dict[str, Any]:
        """The duel's session params (the duel's own `decay_per_round` wins), then --decay / --duel-ticks."""
        s = self.sessions.get(raw.get("session")) or {}
        return {"decay": s.get("decay"), "duel_ticks": s.get("duel_ticks"), **self.overrides}

    # Observations

    def observe(self, mem: Memory) -> Observation:
        snap = mem.snap
        if snap.messages is not None:
            turns = [t.model_copy() for t in snap.messages]
            ours = iter(mem.sent)
            for t in turns:                       # our decisions, in order, for the negotiator's transcript
                if t.mine and (sent := next(ours, None)) is not None:
                    t.decision = sent.decision
        else:
            turns = sorted([*mem.sent, *mem.seen], key=lambda t: (t.tick if t.tick is not None else -1, not t.mine))
        assert snap.view is not None
        return Observation(view=snap.view, turns=turns, rival_offer=snap.rival_offer, tick=self.tick,
                           ticks_left=snap.ticks_left, rounds=snap.rounds,
                           day_swings=list(self.swings.get(snap.raw.get("session"), {}).values()))

    def update(self, raw: dict[str, Any]) -> Memory | None:
        snap = parse_duel(raw, team=self.team, tick=self.tick, defaults=self.defaults(raw))
        key = snap.id
        if self.log.changed(f"duel:{key}", raw):
            self.log.write("duel", tick=self.tick, raw=raw, problems=snap.problems)
            self.record(key, payloads=[{"tick": self.tick, "raw": raw}], problems=snap.problems or None)
        mem = self.duels.get(key)
        if mem is None:
            if snap.view is None:
                if self.log.changed(f"unreadable:{key}", snap.problems):
                    say(f"duel {key}: can't read it ({'; '.join(snap.problems)}); see {self.log.path}")
                return None
            agent = DuelAgent(snap.view, self.strategist, self.negotiator)
            mem = self.duels[key] = Memory(agent=agent, snap=snap)
            if (dv := snap.view.day_values) is not None:
                self.swings.setdefault(raw.get("session"), {})[key] = swing(dv)
            self.resume(mem)
            v = snap.view
            days = (v.day_values.how if v.day_values else f"CAN'T READ the day weight {v.days_weight!r}, models "
                    f"only") if v.has_days else None
            say(f"duel {key} vs {v.rival or '?'}: {v.role.value}, limit {money(v.limit)}, issues {v.issues}, "
                f"{snap.ticks_left} ticks left" + (f", days: {days}" if days else "")
                + (f" [{'; '.join(snap.problems)}]" if snap.problems else ""))
            self.log.write("new_duel", duel=key, view=v.model_dump(), days=days,
                           strategist_system=agent.strategist_system, negotiator_system=agent.negotiator_system)
            self.record(key, session=self.sessions.get(raw.get("session")) or {"session": raw.get("session")},
                        first_tick=self.tick, view=v.model_dump(), days_reading=days,
                        models={"strategist": self.strategist.label, "negotiator": self.negotiator.label},
                        strategist_system=agent.strategist_system, negotiator_system=agent.negotiator_system)
        mem.snap = snap
        self.check_ours(mem)
        if snap.messages is None and snap.rival_offer is not None:
            last = next((t.offer for t in reversed(mem.seen)), None)
            if last != snap.rival_offer:
                text = str(raw.get("rival_text") or raw.get("rival_message") or "")
                mem.seen.append(Turn(mine=False, text=text, offer=snap.rival_offer, tick=self.tick))
        return mem

    def resume(self, mem: Memory) -> None:
        """A duel already under way when this process first sees it (after a restart): our messages so far count
        as sent, and when ours is the last word we wait as before. Friday's restarts re-sent our standing offer in
        duel 181 (50 on tick 134, 54 on 137) because a fresh process saw nothing sent."""
        msgs = mem.snap.messages or []
        mem.sent = [t.model_copy() for t in msgs if t.mine]
        if mem.sent:
            mem.sent_tick = mem.decided_tick = mem.sent[-1].tick
            if answered(msgs):
                mem.decided_on = signature(mem.snap)

    def check_ours(self, mem: Memory) -> None:
        """More priced messages from our side in the game than this process sent: another duelist is running on
        the team key (the one guard across machines). Says so loudly, once per duel."""
        if mem.task is not None or mem.snap.messages is None or self.dry_run:
            return
        in_game = sum(1 for t in mem.snap.messages if t.mine and t.offer is not None)
        if in_game > sum(1 for t in mem.sent if t.offer is not None) and \
                self.log.changed(f"foreign:{mem.snap.id}", in_game):
            self.log.write("foreign_message", duel=mem.snap.id, tick=self.tick)
            say(f"WARNING duel {mem.snap.id}: a message from our side that this process didn't send. Is another "
                f"duelist running on the team key? Stop one of them.")

    # Deciding and sending

    def due(self, mem: Memory) -> bool:
        """Decide now? At most once per tick (a decision whose send was refused waits for the next one)."""
        if mem.task is not None or mem.sent_tick == self.tick or not mem.snap.live:
            return False
        if mem.pending is not None:
            return mem.pending[2] != self.tick
        if mem.force:
            return True
        if mem.decided_tick == self.tick or self.accepted(mem):
            return False
        if not mem.sent or signature(mem.snap) != mem.decided_on:
            return True                           # the rival has moved
        if self.silent_rival(mem):
            return mem.agent.silent_move(self.observe(mem)) is not None   # its schedule, nothing else
        left = mem.snap.ticks_left
        return ((left is not None and left <= DECIDE_LEFT)        # the clock alone is a reason (duel 181)
                or self.closing(mem) is not None
                or self.standoff(mem) >= HOLD_TICKS)               # both sides still (duels 103/104)

    def accepted(self, mem: Memory) -> bool:
        """Our acceptance of their standing offer is out and they haven't changed it: it settles at the next tick."""
        return bool(mem.sent) and mem.sent[-1].accept and signature(mem.snap) == mem.decided_on

    def standoff(self, mem: Memory) -> int:
        """Ticks since anything moved, once the rival has made an offer: their offer changed, we sent something, or
        we decided (a hold included, so a held standoff is asked again HOLD_TICKS later, not every tick). A rival
        that repeats its offer every tick doesn't reset it (278). Read from the duel's messages, so a restart
        doesn't reset it either."""
        if mem.snap.view is None:
            return 0
        still = still_ticks(self.observe(mem))
        if still and mem.decided_tick is not None and self.tick is not None:
            return min(still, self.tick - mem.decided_tick)
        return still

    def silent_rival(self, mem: Memory) -> bool:
        """After our opener, a duel whose rival hasn't sent anything is code's (`agent.silent_move`); with days,
        only when we can read the day weight (our day stays, the price walks)."""
        return (mem.snap.view is not None and bool(mem.sent) and by_code(mem.agent.view)
                and silent(self.observe(mem)))

    def closer(self) -> tuple[Memory, str] | None:
        """The duel whose standing offer code accepts this tick, and why; None when none should.

        "deadline": the team accepts one offer per tick and the duels of a wave end together, so an offer inside
        our limit can't wait for the last tick. The one in the i-th place (earliest deadline first, then the
        bigger surplus) gets the i-th tick from now, and once that would land later than ACCEPT_BY ticks left,
        the first in line accepts now.
        "small gap": otherwise, the first in line whose gap to our standing offer is no more than one more round
        risks (`small_gap`).
        With days, the surplus is the package's worth to us, day included; a days duel whose weight we can't
        read is left to the models (`by_code`)."""
        if any(m.pending is not None and m.pending[0].action == "accept" for m in self.duels.values()):
            return None                           # an acceptance held from an earlier tick goes first
        line = []
        for mem in self.duels.values():
            v, left = mem.agent.view, mem.snap.ticks_left
            if not mem.snap.live or not by_code(v) or left is None or mem.snap.view is None or self.accepted(mem):
                continue
            their = standing_offer(self.observe(mem))
            surplus = None if their is None else worth(v, their.price, their.days)
            if surplus is not None and surplus > 0:
                line.append((left, -surplus, mem, their))
        line.sort(key=lambda x: x[:2])
        ready = [(mem, their, -neg) for _, neg, mem, their in line if mem.sent_tick != self.tick]
        if any(left - i <= ACCEPT_BY for i, (left, *_) in enumerate(line)):
            return (ready[0][0], "deadline") if ready else None
        return next(((mem, "small gap") for mem, their, surplus in ready if self.small_gap(mem, their, surplus)),
                    None)

    def closing(self, mem: Memory) -> str | None:
        """Why code accepts this duel's standing offer this tick, if it does."""
        c = self.closer()
        return c[1] if c is not None and c[0] is mem else None

    def small_gap(self, mem: Memory, their: Offer, surplus: float) -> bool:
        """Their offer is within max(2 P, 2d/(1-d) x our surplus at it) of our standing offer (plan §4D): one
        more round costs about d of the whole deal, and pressing for the gap usually takes two (our counter and
        their reply), so the gap isn't worth it. Only when their offer answers ours: when our offer is the latest
        word, they get the tick to take it (time is free). With days, the gap is in worth to us, days included."""
        if mem.sent and signature(mem.snap) == mem.decided_on:
            return False
        ours = mem.snap.our_offer or next(reversed(our_offers(self.observe(mem))), None)
        if ours is None:
            return False
        v = mem.agent.view
        d = v.decay or 0.0
        return worth(v, ours.price, ours.days) - surplus <= max(2.0, 2 * d / (1 - d) * surplus)

    def their_price(self, mem: Memory, accept: Move) -> Move | None:
        """Our acceptance must wait (the team's one acceptance this tick is spent): offer the rival its own standing
        price instead, so it accepts and spends its acceptance. Only when that adds no round (we have sent at least
        as many messages as they have, priced or not, so rounds = min(ours, theirs) doesn't move), or on the last
        tick, where there is no next one to wait for. With days, their whole package: their price on their day."""
        v = mem.agent.view
        obs = self.observe(mem)
        their = standing_offer(obs)
        if not by_code(v) or their is None or their.price != accept.price or (v.has_days and their.days is None) \
                or past_limit(v, their.price, their.days):
            return None
        last = mem.snap.ticks_left is not None and mem.snap.ticks_left <= 1
        if len(obs.ours) < len(obs.theirs) and not last:
            return None
        day = f", delivery on day {their.days}" if v.has_days else ""
        move = Move("offer", f"I can do {money(their.price, v.currency)}{day}: accept it and we're done.",
                    price=their.price, days=their.days if v.has_days else None, meta={"rule": "their price"})
        return mem.agent.final(move, obs)

    async def decide(self, mem: Memory) -> None:
        sig = signature(mem.snap)
        if mem.pending is not None:
            move, pending_sig, _ = mem.pending
            mem.pending = None
            if pending_sig == sig and (move.action == "accept" or self.closing(mem) is None):
                await self.send(mem, move, sig)   # nothing changed: send what we decided last tick
                return
        mem.force = False
        mem.decided_tick = self.tick
        obs = self.observe(mem)
        start = time.perf_counter()
        timeout = max(8.0, self.tick_seconds - 5.0)
        if why := self.closing(mem):
            move = mem.agent.final(mem.agent.close(obs, why), obs)
        elif self.silent_rival(mem):
            if (step := mem.agent.silent_move(obs)) is None:
                return                            # nothing to send this tick
            move = mem.agent.final(step, obs)
        else:
            try:
                move = await asyncio.wait_for(mem.agent.respond(obs), timeout)
            except TimeoutError:
                move = mem.agent.final(mem.agent.safe_move(obs, f"timeout after {timeout:.0f} s"), obs)
            except Exception as e:                # never let one duel's bug stop the loop
                self.log.write("error", where="respond", duel=mem.snap.id, error=repr(e))
                move = mem.agent.final(mem.agent.safe_move(obs, f"error: {e!r}"), obs)
            if move.action != "accept" and (why := self.closing(mem)):   # things moved while the models thought
                move = mem.agent.final(mem.agent.close(obs, why), obs)
        took = time.perf_counter() - start
        cost = sum(c["cost_usd"] for c in move.meta.get("calls", []))
        self.spent_usd += cost
        hold = self.is_hold(mem, move, obs)
        self.log.write("decision", duel=mem.snap.id, tick=self.tick, took_s=round(took, 2), cost_usd=cost,
                       obs=obs.model_dump(), move=move.__dict__, hold=hold)
        self.record(mem.snap.id, decisions=[{"tick": self.tick, "took_s": round(took, 2), "cost_usd": cost,
                                             "obs": obs.model_dump(), "move": move.__dict__, "hold": hold}])
        if signature(mem.snap) != sig and move.action == "accept":
            say(f"duel {mem.snap.id}: their offer changed while deciding; deciding again")
            mem.force = True
            return
        if hold:                                  # nothing sent: every message is a round (277, 278)
            mem.decided_on = sig
            say(f"[tick {self.tick}] duel {mem.snap.id}: hold, nothing sent ({move.action} "
                f"{money(move.price) if move.price is not None else 'without a price'}) {took:.1f}s")
            return
        await self.send(mem, move, sig, took)

    def is_hold(self, mem: Memory, move: Move, obs: Observation) -> bool:
        """A move that only holds our standing offer: a message without a price, or an offer at its price and day.
        Every message is a round once they have sent as many (277: three no-price messages, three rounds), so a
        hold sends nothing. Before our first offer a message is never a hold (`agent.check` asks for an offer)."""
        ours = mem.snap.our_offer or next(reversed(our_offers(obs)), None)
        if ours is None or move.action == "accept":
            return False
        return move.action == "message" or (move.price == ours.price and move.days == ours.days)

    async def send(self, mem: Memory, move: Move, sig: Any, took: float | None = None) -> None:
        did, v = mem.snap.id, mem.agent.view
        band = move.meta.get("band") or {}
        what = (f"offer {money(move.price)}" + (f" day {move.days}" if move.days is not None else "")
                if move.action == "offer" else
                f"accept {money(move.price) if move.price is not None else '?'}" if move.action == "accept" else
                "message")
        note = (f" band {band.get('worst')}..{band.get('best')}" if band else "") + \
               (f" FALLBACK({move.meta['fallback']})" if move.meta.get("fallback") else "") + \
               (" repaired" if move.meta.get("repaired") else "") + \
               (f" [{move.meta['rule']}]" if move.meta.get("rule") else "") + (f" {took:.1f}s" if took else "")
        accepting = move.action == "accept"
        if accepting and self.accepted_tick == self.tick:
            if (alt := self.their_price(mem, move)) is not None:
                say(f"duel {did}: our acceptance is spent this tick; offering their own price so they accept")
                return await self.send(mem, alt, sig, took)
            mem.pending = (move, sig, self.tick)  # one acceptance per team per tick: try next tick
            say(f"duel {did}: {what} waits for the next tick (another acceptance this tick)")
            return
        if accepting:
            self.accepted_tick = self.tick        # taken before the call, so two duels can't both send one
        say(f"{'DRY ' if self.dry_run else ''}[tick {self.tick}] duel {did} ({v.role.value}, limit {v.limit}): "
            f"{what}{note} :: {move.text[:140]}")
        result: Any = "dry-run"
        if not self.dry_run:
            try:
                if move.action == "accept":
                    result = await self.call(self.b.duel_accept, did)
                else:
                    result = await self.call(self.b.duel_say, did, move.text, move.price, move.days)
            except BazaarError as e:
                self.log.write("send_error", duel=did, tick=self.tick, code=e.code, message=e.message,
                               extra=e.extra, move=move.__dict__)
                self.record(did, errors=[{"tick": self.tick, "code": e.code, "message": e.message,
                                          "move": move.__dict__}])
                if e.code == "wait_for_tick":
                    if accepting and (alt := self.their_price(mem, move)) is not None:
                        return await self.send(mem, alt, sig, took)
                    mem.pending = (move, sig, self.tick)
                    return
                if accepting and e.code != "network":       # refused, so not spent (a network error may have landed)
                    self.accepted_tick = None
                if e.code == "missing_days" and "days" not in v.issues:
                    v.issues.append("days")
                    mem.agent = DuelAgent(v, self.strategist, self.negotiator)
                    mem.force = True
                say(f"duel {did}: refused: {e.code}: {e.message}")
                return
        self.log.write("sent", duel=did, tick=self.tick, move=move.__dict__, result=result)
        self.record(did, sent=[{"tick": self.tick, "dry_run": self.dry_run, "move": move.__dict__, "result": result}])
        mem.sent.append(Turn(mine=True, text=move.text, accept=move.action == "accept", tick=self.tick,
                             offer=Offer(price=move.price, days=move.days) if move.action == "offer" else None,
                             decision=move.meta.get("decision")))
        mem.sent_tick = self.tick
        mem.decided_on = sig

    async def finish(self, gone: list[Any]) -> None:
        """Duels that left the live list: log how they ended."""
        try:
            done = {d.get("id", d.get("duel_id", d.get("duel"))): d for d in (await self.call(self.b.duels, True)).get("duels", [])}
        except BazaarError:
            done = {}
        for key in gone:
            mem = self.duels.pop(key)
            if mem.task is not None:
                mem.task.cancel()
            raw = done.get(key)
            self.log.write("finished", duel=key, raw=raw)
            self.record(key, last_seen_tick=self.tick, done=raw)   # if not in the done list yet, the sweep adds it
            say(f"duel {key} finished: " + (json.dumps({k: raw[k] for k in raw if k not in ('messages',)})[:300]
                                             if raw else "(not in the done list yet)"))

    async def sweep(self) -> None:
        """Every minute: finished duels we haven't recorded (also ones a restart missed), the feed's duel events,
        our duel points. Three reads; any failure is logged and skipped."""
        if self.records is None:
            return
        try:
            for raw in (await self.call(self.b.duels, True)).get("duels", []):
                key = duel_key(raw)
                if key is not None and key not in self.duels and ended(raw) and not self.records.finished(key):
                    self.record(key, done=raw)
                    self.log.write("recorded", duel=key)
            events = (await self.call(self.b.feed, 200)).get("events", [])
            self.records.add_feed(events)
            self.learn_sessions(events)
            self.records.add_score(self.tick, (await self.call(self.b.me)).get("score") or {})
        except Exception as e:
            self.log.write("error", where="sweep", error=repr(e))

    # The loop

    async def run(self) -> None:
        me = await self.call(self.b.me)
        self.team = {str(me.get("id")), str(me.get("name"))}
        say(f"{me.get('name')} ({me.get('id')}): {'DRY RUN, ' if self.dry_run else ''}strategist "
            f"{self.strategist.label}, negotiator {self.negotiator.label}; log {self.log.path}")
        await self.refresh_session()
        await self.sweep()
        last_schedule = time.monotonic()
        while True:
            try:
                clock = await self.call(self.b.clock)
                if clock.get("tick") != self.tick:
                    self.tick = clock.get("tick")
                    self.tick_seconds = float(clock.get("tick_seconds") or self.tick_seconds)
                if time.monotonic() - last_schedule > 60:
                    await self.refresh_session(clock.get("t_hours"))
                    await self.sweep()
                    last_schedule = time.monotonic()
                if clock.get("doors") not in (None, "open") or clock.get("paused"):
                    await asyncio.sleep(max(self.poll_s, 10))
                    continue
                live = (await self.call(self.b.duels)).get("duels", [])
                unknown = {raw.get("session") for raw in live} - set(self.sessions) - {None}
                if unknown and time.monotonic() - self.sessions_read > 10:
                    await self.read_sessions()
            except Exception as e:                # never let a bad read stop the loop
                self.log.write("error", where="poll", error=repr(e))
                say(f"poll failed: {e!r}")
                await asyncio.sleep(self.poll_s * 2)
                continue
            keys, polled = set(), []
            for raw in live:
                try:
                    mem = self.update(raw)
                except Exception as e:            # one unreadable duel must not stop the others
                    self.log.write("error", where="update", raw=raw, error=repr(e))
                    say(f"duel payload failed: {e!r}")
                    if (k := duel_key(raw)) in self.duels:
                        keys.add(k)               # keep it; don't finish it on a parse error
                    continue
                if mem is None:
                    continue
                keys.add(mem.snap.id)
                polled.append(mem)
            for mem in polled:                    # after every duel is read: `closer` weighs them all
                if self.due(mem):
                    mem.task = asyncio.create_task(self._decide(mem))
            if gone := [k for k in self.duels if k not in keys and self.duels[k].task is None]:
                try:
                    await self.finish(gone)
                except Exception as e:
                    self.log.write("error", where="finish", error=repr(e))
            await asyncio.sleep(self.wait_s(live))

    async def _decide(self, mem: Memory) -> None:
        try:
            await self.decide(mem)
        except Exception as e:
            self.log.write("error", where="decide", duel=mem.snap.id, error=repr(e))
            say(f"duel {mem.snap.id}: error {e!r}")
        finally:
            mem.task = None
