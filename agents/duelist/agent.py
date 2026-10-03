"""Clock-Standing for the duels: a strategist sets the band, a negotiator writes the message inside it, code holds
the move to the band and the hard limits (regateo agents/ranged/v4, config clock-standing: `hold`, `standing`
and `clock` on, the negotiator never told our limit).

Code states facts only: offers so far, how far each side has moved, ticks left, rounds and what one more costs, the
gap. Prices and
when to accept stay with the models, with two exceptions. The fallback when both models fail (`safe_move`)
concedes on a schedule and accepts once their offer meets it, so a duel still closes. And code accepts a standing
offer inside our limit when the runner says the acceptance can't wait (`close`).

Decay is per round, not per tick (Friday's 30 practice duels): result = our surplus x (1 - decay)^rounds, with
rounds = min(our priced offers, theirs). Silence costs nothing but the deadline.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from string import Template
from typing import Any, Literal

from pydantic import BaseModel, Field

from engine import LLMError, Model, Reply

from .guards import mentions_past_limit, past_limit, reads_as_agreement, standing_problems
from .model import DuelView, Observation, Offer, Role, sign
from .prices import money

PROMPTS = Path(__file__).parent / "prompts"
OPENING = "(The duel begins. You make the first move.)"
OWN_NOTE = "[Note from your own system, not from the other side]"
AGREEMENT_FEEDBACK = ("the message could be read as accepting, but you are not accepting. Don't use words like "
                      "'deal', 'agree', 'accept', 'sounds good' or 'works for me' unless you accept.")
MAX_MESSAGE = 1000                      # characters; the game keeps 1,200


class BandPlan(BaseModel):
    """The strategist's output: its read of the conversation, then the band for this turn."""
    read: str = Field(description="one or two sentences: what their latest message offers, claims or asks, "
                                  "and how far to trust it")
    target: int = Field(description="the price your side's next offer should be")
    best: int = Field(description="the best price for your side the negotiator may still offer this turn")
    worst: int = Field(description="the furthest the negotiator may concede this turn; a standing offer from "
                                   "them at least this good may be accepted")
    days: int | None = Field(description="the delivery day (0-10) your side proposes this turn; null when the "
                                         "duel is on price only")
    angle: str = Field(description="one sentence for the negotiator: what to stress or ask this turn")


class Decision(BaseModel):
    action: Literal["offer", "accept", "message"]
    price: int | None = Field(description="price offered or accepted; null for a message")
    message: str = Field(max_length=MAX_MESSAGE, description="what the other side reads")


@dataclass
class Move:
    """What the runner sends: an offer (price, and days when the duel has them), an acceptance of their standing
    offer, or a message without a price."""
    action: Literal["offer", "accept", "message"]
    text: str
    price: int | None = None
    days: int | None = None
    meta: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Band:
    """The prices the negotiator may offer this turn: from `worst` (the most we concede, never past our limit)
    to `best`."""
    worst: int
    target: int
    best: int

    def allows(self, s: int, price: float) -> bool:
        return s * self.worst <= s * price <= s * self.best

    def clamp(self, s: int, price: float) -> int:
        return s * int(min(max(s * price, s * self.worst), s * self.best))


def toward_us(s: int, price: float) -> int:
    """A whole price, rounded in our favour, so rounding never crosses the limit."""
    return s * math.ceil(s * price - 1e-9)


def make_band(view: DuelView, plan: BandPlan) -> Band:
    s = sign(view.role)
    lo, hi = sorted((s * plan.worst, s * plan.best))
    t = s * plan.target
    lo, hi = min(lo, t), max(hi, t)
    lo = max(lo, s * view.limit)
    hi = max(hi, lo)
    t = min(max(t, lo), hi)
    return Band(worst=toward_us(s, s * lo), target=toward_us(s, s * t), best=toward_us(s, s * hi))


# The facts

def fmt_offer(view: DuelView, o: Offer) -> str:
    return money(o.price, view.currency) + (f" (day {o.days})" if o.days is not None else "")


def our_offers(obs: Observation) -> list[Offer]:
    return [t.offer for t in obs.ours if t.offer is not None]


def their_offers(obs: Observation) -> list[Offer]:
    out = [t.offer for t in obs.theirs if t.offer is not None]
    if obs.rival_offer is not None and (not out or out[-1] != obs.rival_offer):
        out.append(obs.rival_offer)                # the game's standing offer is the latest fact
    return out


def standing_price(obs: Observation) -> int | None:
    """Their standing offer's price: the game's field when it gives one, else their last structured offer."""
    if obs.rival_offer is not None:
        return obs.rival_offer.price
    theirs = their_offers(obs)
    return theirs[-1].price if theirs else None


def last_tick(obs: Observation) -> bool:
    return obs.ticks_left is not None and obs.ticks_left <= 1


def quiet_ticks(obs: Observation) -> int:
    """Ticks since either side last sent anything; 0 when no message has a tick."""
    ticks = [t.tick for t in obs.turns if t.tick is not None]
    return max(obs.tick - max(ticks), 0) if ticks and obs.tick is not None else 0


def ledger(obs: Observation) -> str:
    """Facts for the strategist, computed from the duel. No advice."""
    v = obs.view
    f = lambda p: money(p, v.currency)  # noqa: E731
    s = sign(v.role)
    ours, theirs = our_offers(obs), their_offers(obs)
    lines = ["Facts from your own system (computed, not from the other side):"]
    lines.append("- Your offers so far: " + (", ".join(fmt_offer(v, o) for o in ours) if ours else "none"))
    lines.append("- Their offers so far: " + (", ".join(fmt_offer(v, o) for o in theirs) if theirs else "none"))
    if len(ours) >= 2:
        lines.append(f"- You have moved {f(abs(ours[-1].price - ours[0].price))} from your first offer.")
    if len(theirs) >= 2:
        moved = s * (theirs[-1].price - theirs[0].price)     # positive: they have moved toward us
        lines.append(f"- They have moved {f(abs(moved))} from their first offer"
                     + ("" if moved > 0 else " (not toward you)" if moved < 0 else "") + ".")
    lines.append(f"- Messages sent so far: {len(obs.ours)} by your side, {len(obs.theirs)} by theirs.")
    if theirs and (quiet := quiet_ticks(obs)) >= 2:
        lines.append(f"- Neither side has sent anything for {quiet} ticks.")
    if obs.ticks_left is None:
        lines.append("- The number of ticks left is unknown: the duel can end, with no deal, after any tick.")
    elif last_tick(obs):
        lines.append("- This is the last tick of the duel: an offer in your next message may never be answered.")
    else:
        total = f" of {v.duel_ticks}" if v.duel_ticks else ""
        lines.append(f"- Ticks left in the duel, including this one: {obs.ticks_left}{total}.")
    rounds = obs.rounds if obs.rounds is not None else min(len(ours), len(theirs))
    if v.decay:
        lines.append(f"- Rounds so far: {rounds} (the smaller of your {len(ours)} priced offers and their "
                     f"{len(theirs)}). Each round costs any deal about {v.decay:.0%} of its value; time alone "
                     "costs nothing.")
        lines.append("- Your next priced offer adds a round at once (they have made more priced offers than you)."
                     if len(ours) < len(theirs) else
                     "- Your next priced offer adds no round by itself; a priced reply from them would.")
    their = standing_price(obs)
    if their is not None:
        lines.append(f"- Their standing offer: {fmt_offer(v, theirs[-1]) if theirs else f(their)}"
                     + (" (within your limit)." if not past_limit(v, their) else " (past your limit)."))
        if v.decay and not past_limit(v, their):
            worth = s * (their - v.limit) * (1 - v.decay) ** rounds
            lines.append(f"- Accepting it now is worth about {f(round(worth))} to you; each further round would "
                         f"take about {f(round(worth * v.decay))} off any deal near it.")
    if their is not None and ours:
        gap = s * (ours[-1].price - their)                  # positive: our last offer is better for us
        lines.append(f"- Gap between your last offer ({f(ours[-1].price)}) and their standing offer ({f(their)}): "
                     f"{f(abs(gap))}." if gap >= 0 else
                     f"- Their standing offer ({f(their)}) is already better for you than your last offer "
                     f"({f(ours[-1].price)}), by {f(-gap)}.")
    return "\n".join(lines)


# The prompts

def render(name: str, **values: object) -> str:
    return Template((PROMPTS / f"{name}.md").read_text()).substitute({k: str(x) for k, x in values.items()}).strip()


def brief(view: DuelView, *, strategist: bool) -> dict[str, str]:
    """The placeholders the system prompts fill. Only the strategist's include the limit and the raw extras."""
    rules = ["- Prices are whole primas (P). Each side may send one message per tick; an offer is binding once "
             "the other side accepts it, and settles at the next tick.",
             f"- The duel lasts {view.duel_ticks} ticks." if view.duel_ticks else
             "- The duel has a deadline; the facts each turn say how many ticks are left."]
    if view.decay:
        rules.append(f"- Every round of offers shrinks the value of any deal by about {view.decay:.0%}. The rounds "
                     "are the smaller of the two sides' numbers of priced offers, so time alone costs nothing and "
                     "silence adds no round.")
    if view.has_days:
        rules.append("- The duel settles two issues: the price and a delivery day from 0 to 10. Every offer names both.")
    item = view.item or "an item"
    out = {
        "role": view.role.value,
        "item_line": f"The deal is over {item}." + (f" {view.context}" if view.context else ""),
        "market": f"- {view.market}" if view.market else "- Nothing beyond the scenario: no market price is given.",
        "rules": "\n".join(rules),
    }
    if strategist:
        out |= {
            "limit": money(view.limit, view.currency),
            "limit_rule": ("It is your cost: never sell below it." if view.role is Role.SELLER else
                           "It is what the item is worth to you: never pay more than it."),
            "extra": ("Other fields of the duel, as the game gives them:\n" + json.dumps(view.extra)[:1500] + "\n"
                      if view.extra else ""),
            "days_private": (f"- Your weight on the delivery day, as the game gives it: "
                             f"{json.dumps(view.days_weight)}. It is private: the other side has its own.\n"
                             if view.has_days else ""),
            "days_guide": ("\nThe delivery day: set \"days\" (0 to 10) every turn. Each side cares about the day "
                           "differently, and the deal can be worth more to both when the side that cares more about "
                           "the day gets it. Read their offers for which days they push, give ground on the day where "
                           "it costs you little, and ask for price in return; hold the day where it matters to you.\n"
                           if view.has_days else ""),
        }
    else:
        out["days_negotiator"] = ("- The duel also settles a delivery day (0 to 10). Your brief names the day your "
                                  "side proposes; when you offer, mention it in your message.\n"
                                  if view.has_days else "")
    return out


def quoted(text: str) -> str:
    return "\n".join(f"> {line}" for line in (text or "(no message)").splitlines() or [""])


def transcript_text(obs: Observation) -> str:
    """The conversation as one text for the strategist. Every line of a message is quoted with "> ", so text
    inside a message can't pass for a header."""
    v = obs.view
    if not obs.turns:
        return "(No messages yet. Your side makes the first move.)"
    blocks = []
    for i, t in enumerate(obs.turns, 1):
        who = "your side" if t.mine else "the other side"
        move = (" (accepts)" if t.accept else f" (offers {fmt_offer(v, t.offer)})" if t.offer else "")
        when = f", tick {t.tick}" if t.tick is not None else ""
        blocks.append(f"[message {i}, {who}{move}{when}]\n{quoted(t.text)}")
    return "\n\n".join(blocks)


def transcript(obs: Observation) -> list[dict[str, str]]:
    """The conversation as chat turns for the negotiator: theirs as user turns with their structured offer,
    ours as the decisions we made. Consecutive turns of one side are merged, since chat turns alternate."""
    v = obs.view
    out: list[dict[str, str]] = []

    def add(role: str, content: str) -> None:
        if out and out[-1]["role"] == role:
            out[-1]["content"] += "\n\n" + content
        else:
            out.append({"role": role, "content": content})

    if not obs.turns or obs.turns[0].mine:
        add("user", OPENING)
    for t in obs.turns:
        if t.mine:
            d = t.decision or {"action": "accept" if t.accept else "offer" if t.offer else "message",
                               "price": t.offer.price if t.offer else None, "message": t.text}
            add("assistant", json.dumps(d))
        else:
            move = "[accepts]" if t.accept else f"[offer {fmt_offer(v, t.offer)}]" if t.offer else "[message]"
            add("user", f"{move}\n{t.text or '(no message)'}")
    return out


def with_note(messages: list[dict[str, str]], note: str) -> list[dict[str, str]]:
    """`messages` with `note` added to the last user turn (or as a new one): the API needs a user turn last."""
    if messages and messages[-1]["role"] == "user":
        return [*messages[:-1], {"role": "user", "content": f"{messages[-1]['content']}\n\n{note}"}]
    return [*messages, {"role": "user", "content": note}]


# The agent

class DuelAgent:
    def __init__(self, view: DuelView, strategist: Model, negotiator: Model | None = None):
        self.view = view
        self.s = sign(view.role)
        self.strategist = strategist
        self.negotiator = negotiator or strategist
        self.strategist_system = render("strategist", **brief(view, strategist=True))
        self.negotiator_system = render("negotiator", **brief(view, strategist=False))
        self.calls: list[dict[str, Any]] = []         # per turn: stage, latency, tokens, cost

    def _record(self, stage: str, r: Reply) -> None:
        self.calls.append({"stage": stage, "latency_s": round(r.latency_s, 2), "in": r.input_tokens,
                           "out": r.output_tokens, "cost_usd": round(r.cost_usd, 5), "model": r.model})

    # The strategist

    def _plan_problems(self, plan: BandPlan) -> list[str]:
        f = lambda p: money(p, self.view.currency)  # noqa: E731
        bad = [f"{name} {f(price)}" for name, price in (("target", plan.target), ("worst", plan.worst))
               if past_limit(self.view, price)]
        out = [f"{' and '.join(bad)} are past your limit. Set the band within it."] if bad else []
        if self.view.has_days and (plan.days is None or not 0 <= plan.days <= 10):
            out.append("set \"days\" to a delivery day from 0 to 10.")
        return out

    async def plan(self, obs: Observation) -> BandPlan:
        prompt = (f"The conversation so far:\n\n{transcript_text(obs)}\n\n{ledger(obs)}\n\n"
                  "Set the band for your side's next message.")

        async def ask(text: str) -> BandPlan:
            r = await self.strategist.parse(BandPlan, self.strategist_system, [{"role": "user", "content": text}])
            self._record("strategist", r)
            assert isinstance(r.parsed, BandPlan)
            return r.parsed

        plan = await ask(prompt)
        if found := self._plan_problems(plan):     # one retry; make_band keeps whatever comes back in the limit
            plan = await ask(f"{prompt}\n\n{OWN_NOTE} Your previous band was rejected: {' '.join(found)}")
        return plan

    # The negotiator

    def _brief(self, band: Band, plan: BandPlan, days: int | None, obs: Observation) -> str:
        f = lambda p: money(p, self.view.currency)  # noqa: E731
        lines = [f"{OWN_NOTE} Your strategist's brief for this turn:", f"- Their latest message: {plan.read}"]
        if last_tick(obs):
            lines.append("- This is the last tick: an offer in your message may never be answered.")
        if band.best == band.worst:
            lines.append(f"- Offer exactly {f(band.target)}.")
        else:
            lines.append(f"- Offer between {f(band.worst)} and {f(band.best)}; aim for about {f(band.target)}.")
        if days is not None:
            lines.append(f"- Your side proposes delivery on day {days}.")
        lines.append(f"- Accept their standing offer only if it is {f(band.worst)} or better for you.")
        lines.append(f"- Angle: {plan.angle}")
        return "\n".join(lines)

    def check(self, d: Decision, obs: Observation, band: Band) -> list[str]:
        """What keeps a decision from being sent. Worded so a negotiator that doesn't know the limit learns
        nothing about it beyond the band it was given."""
        f = lambda p: money(p, self.view.currency)  # noqa: E731
        out: list[str] = []
        their = standing_price(obs)
        if d.action == "offer":
            if d.price is None:
                out.append("an offer needs a price.")
            else:
                if not band.allows(self.s, d.price):
                    out.append(f"{f(d.price)} is outside the band for this turn ({f(band.worst)} to {f(band.best)}).")
                out += standing_problems(self.view, d.price, their)
        elif d.action == "accept":
            if their is None:
                out.append("there is no standing offer from the other side to accept.")
            elif self.s * their < self.s * band.worst:
                out.append(f"you may only accept an offer of {f(band.worst)} or better for you.")
        if bad := mentions_past_limit(self.view, d.message):
            out.append(f"the message mentions {', '.join(map(f, bad))}. Don't write those amounts, not even to "
                       "reject them.")
        if d.action != "accept" and reads_as_agreement(d.message):
            out.append(AGREEMENT_FEEDBACK)
        return out

    async def negotiate(self, obs: Observation, band: Band, plan: BandPlan, days: int | None,
                        feedback: str | None) -> Decision:
        messages = with_note(transcript(obs), self._brief(band, plan, days, obs))
        if feedback:
            messages = with_note(messages, feedback)
        r = await self.negotiator.parse(Decision, self.negotiator_system, messages)
        self._record("negotiator", r)
        assert isinstance(r.parsed, Decision)
        return r.parsed

    def _days(self, plan: BandPlan | None, obs: Observation) -> int | None:
        """The day a priced message carries: the strategist's, else our last one, else the middle."""
        if not self.view.has_days:
            return None
        if plan is not None and plan.days is not None:
            return min(max(int(plan.days), 0), 10)
        ours = [o.days for o in our_offers(obs) if o.days is not None]
        return ours[-1] if ours else 5

    def to_move(self, d: Decision, obs: Observation, days: int | None, **meta: Any) -> Move:
        meta = {"decision": d.model_dump(), **meta}
        if d.action == "offer" and d.price is not None:
            return Move("offer", d.message, price=int(d.price), days=days, meta=meta)
        if d.action == "accept":
            return Move("accept", d.message, price=standing_price(obs), meta=meta)
        return Move("message", d.message, meta=meta)

    def safe_move(self, obs: Observation, reason: str, **meta: Any) -> Move:
        """Code's move when the models fail, so a duel still closes without them: open far from our limit; then
        concede a share of the gap to the better of our limit and their standing offer, a larger share as the
        clock runs out; accept their standing offer once it is inside our limit and at least as good as that
        concession (or within 2 P of it)."""
        ours = our_offers(obs)
        days = self._days(None, obs)
        meta = {"fallback": reason, **meta}
        if not ours:
            price = toward_us(self.s, self.view.limit * (1.6 if self.s > 0 else 0.6))
        else:
            last = ours[-1].price
            their = standing_price(obs)
            floor = self.view.limit
            if their is not None and not past_limit(self.view, their) and self.s * their > self.s * floor:
                floor = their
            left = obs.ticks_left if obs.ticks_left is not None else 4
            share = 1.0 if left <= 1 else min(0.5, 1 / max(left - 1, 2))
            price = toward_us(self.s, last - (last - floor) * share)
            if self.s * price < self.s * floor:
                price = floor
            if their is not None and not past_limit(self.view, their) and self.s * (price - their) <= 2:
                return Move("accept", "Agreed.", price=their, meta=meta)
        text = f"I can do {money(price, self.view.currency)}" + (f", delivery on day {days}." if
                                                                  days is not None else ".")
        return Move("offer", text, price=price, days=days, meta=meta)

    def close(self, obs: Observation, why: str) -> Move:
        """Code's acceptance of their standing offer, no model asked: the runner calls it when the offer is inside
        our limit and either the acceptance can't wait for the deadline (duel 181: their 73 sat inside our 85 for
        the last three ticks and the duel ended with no deal) or the gap is smaller than what one more round
        risks. `final` still checks the limit."""
        self.calls = []
        return Move("accept", "Agreed.", price=standing_price(obs), meta={"rule": why})

    def repair(self, d: Decision, obs: Observation, band: Band, days: int | None, /, **meta: Any) -> Move:
        """A decision that failed its checks twice: an offer clamped into the band with a plain message."""
        price = band.clamp(self.s, d.price) if d.action == "offer" and d.price is not None else band.target
        their = standing_price(obs)
        if their is not None and self.s * price < self.s * their:
            price = band.clamp(self.s, their)       # never below their standing offer
        text = f"I can do {money(price, self.view.currency)}" + (f", delivery on day {days}." if days is not None
                                                                 else ".")
        return Move("offer", text, price=price, days=days, meta={"repaired": True, **meta})

    async def respond(self, obs: Observation) -> Move:
        self.calls = []
        try:
            plan = await self.plan(obs)
        except LLMError as e:
            return self.final(self.safe_move(obs, f"strategist: {e}"), obs)
        band = make_band(self.view, plan)
        days = self._days(plan, obs)
        meta: dict[str, Any] = {"band": {"worst": band.worst, "target": band.target, "best": band.best},
                                "plan": plan.model_dump()}
        vetoes: list[str] = []
        feedback = None
        d: Decision | None = None
        for _ in range(2):
            try:
                d = await self.negotiate(obs, band, plan, days, feedback)
            except LLMError as e:
                return self.final(self.safe_move(obs, f"negotiator: {e}", vetoes=vetoes, **meta), obs)
            if not (found := self.check(d, obs, band)):
                return self.final(self.to_move(d, obs, days, **({"vetoes": vetoes} if vetoes else {}), **meta), obs)
            vetoes += found
            feedback = f"{OWN_NOTE} Your previous draft was rejected: {' '.join(found)} Decide again."
        assert d is not None
        return self.final(self.repair(d, obs, band, days, vetoes=vetoes, rejected=d.model_dump(), **meta), obs)

    def final(self, move: Move, obs: Observation) -> Move:
        """Last line of defence: whatever happened before, never offer or accept past our limit, and never write
        an amount past it."""
        move.meta["calls"] = self.calls
        bad = ((move.action == "offer" and (move.price is None or past_limit(self.view, move.price)))
               or (move.action == "accept" and (standing_price(obs) is None
                                                or past_limit(self.view, standing_price(obs))))
               or mentions_past_limit(self.view, move.text))
        if not bad:
            return move
        if move.meta.get("fallback"):                 # the fallback itself failed: say nothing binding
            return Move("message", "Let me think about that.", meta={"blocked": move.meta})
        return self.final(self.safe_move(obs, "past the limit despite the band", blocked=move.meta), obs)
