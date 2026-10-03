"""Code-first moves (`--policy code`, Chief Sat 22:00, for Aleks's review): code decides accept / hold / step and
the day; one model call writes only the words, within TEXT_TIMEOUT_S, else code's plain text.

Why: Duels II's model decisions took 9.2 s on average (p90 12.4 s, max 20 s, 29% over 10 s; docs/duels, 270
decisions): the strategist alone 6.9 s, the negotiator 2.4 s, and 14% of decisions sent a second negotiator call after
a vetoed draft. At 15 s ticks the runner's whole-decision budget is 10 s, so about a third of model moves would turn
into fallbacks. Here a decision is one text call, capped, and never a retry: the words are checked by the same guards
(no claims, no stray or past-limit numbers, no agreement words unless accepting) and replaced by code's plain text
when they fail, so a decision takes at most about TEXT_TIMEOUT_S plus code time.

The moves follow the Duel Lab's simulated policy (intel/duel-lab.md, tools/duel_sim.py), with the duelist's code
rules unchanged around them (the runner's deadline / small-gap accepts, the silent walk, the late day switch):
- opener: OPENER_SHARE of our limit away from it, in worth (Duels I openers: median 0.42, the simulator's U);
- each move after: concede CODE_STEP_SHARE of the gap between the standing offers, in worth, cut to MAX_STEP_SHARE
  and held when below `min_step`, as `agent.held` does for the models. Simulated (tools/duel_sim.py, Sunday's 12
  ticks at 10% decay, 6,000 duels a world, paired against today's model steps capped at 25%): 12% wins in all four
  rival worlds (+0.008 to +0.010 a duel, every CI above 0); 15% +0.005 to +0.013; 20% and 25% lose in one or two;
  in the last CLOSING_TICKS: END_STEP_SHARE of the gap, never held or cut;
- accept their standing offer when it is worth at least our own, or within ACCEPT_NEAR_P of where our step lands;
- the day: the day rules' call (`agent.day_read`): take their day, give it (worth up by its cost: the premium), or
  hold ours (a menu holds ours too; the words may name the other package);
- never past our limit: the step stops at our limit on the day offered, and `agent.final` checks the move again.
What it gives up: the strategist's reading of the rival's words (bluffs, deadlines, menus). It plays the numbers only.
"""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

from engine import LLMError

from . import agent as A
from .guards import claims, mentions_past_limit, past_limit, price_at, reads_as_agreement, worth
from .model import Observation
from .prices import money

if TYPE_CHECKING:
    from .agent import DuelAgent, Move

OPENER_SHARE = 0.42      # our opener's distance from our limit, as a share of the limit (Duels I median, Duel Lab U)
CODE_STEP_SHARE = 0.12   # a mid-duel concession: this share of the gap (simulated vs today's 25% cap, below)
END_STEP_SHARE = 0.5     # in the last CLOSING_TICKS ticks: this share (the simulator's end_alpha)
ACCEPT_NEAR_P = 2.0      # their offer within this of where our step lands: take it instead of another round
TEXT_TIMEOUT_S = 3.5     # the text model's budget; after it, code's plain words


class Words(BaseModel):
    message: str = Field(max_length=A.MAX_MESSAGE, description="exactly what the other side reads")


def plain(move: "Move", currency: str = "P") -> str:
    if move.action == "accept":
        return "Agreed."
    return f"I can do {money(move.price, currency)}" + (f", delivery on day {move.days}." if move.days is not None
                                                         else ".")


def code_day(agent: "DuelAgent", obs: Observation) -> tuple[int | None, str | None, float]:
    """(the day our offer names, the day rules' call, the premium in worth): their day when the call takes or gives
    it, else ours."""
    r = A.day_read(obs)
    if r is None:
        return agent._days(None, obs), None, 0.0
    if r.call == "take":
        return r.their_day, r.call, 0.0
    if r.call == "give":
        return r.their_day, r.call, r.cost
    return r.our_day, r.call, 0.0


def code_move(agent: "DuelAgent", obs: Observation) -> "Move":
    """This turn's move, by code: an opener, an accept, a hold (our standing offer again: the runner sends nothing)
    or a step. No text yet (`write`)."""
    v, s = agent.view, agent.s
    ours, theirs = A.our_offers(obs), A.standing_offer(obs)
    day, call, premium = code_day(agent, obs)
    meta: dict[str, Any] = {"policy": "code", "day_call": call}
    if not ours:
        price = A.toward_us(s, price_at(v, OPENER_SHARE * v.limit + premium, day))
        return A.Move("offer", "", price=price, days=day, meta={**meta, "rule": "code opener"})
    last = ours[-1]
    hold = lambda why: A.Move("offer", "", price=last.price, days=last.days,  # noqa: E731
                              meta={**meta, "rule": why})
    if theirs is None:
        return hold("code: nothing of theirs to answer")
    now, their_w = worth(v, last.price, last.days), worth(v, theirs.price, theirs.days)
    if their_w >= now and not past_limit(v, theirs.price, theirs.days):
        return A.Move("accept", "", price=theirs.price, meta={**meta, "rule": "code: theirs is as good as ours"})
    gap = now - their_w
    left = obs.ticks_left
    closing = left is not None and left <= A.CLOSING_TICKS
    step = (END_STEP_SHARE if closing else CODE_STEP_SHARE) * gap
    if not closing:
        step = min(step, A.MAX_STEP_SHARE * gap)
        if step < A.min_step(v, last, theirs) and call != "give":
            return hold("code: small step")
    target = max(now - step, 0.0)
    if their_w >= 0 and target - their_w <= ACCEPT_NEAR_P and not past_limit(v, theirs.price, theirs.days):
        return A.Move("accept", "", price=theirs.price, meta={**meta, "rule": "code: theirs is within reach"})
    price = A.toward_us(s, price_at(v, target + premium, day))
    if past_limit(v, price, day):
        price = A.toward_us(s, price_at(v, 0.0, day))
    if (price, day) == (last.price, last.days):
        return hold("code: same offer")
    return A.Move("offer", "", price=price, days=day, meta={**meta, "rule": "code step", "step": round(step, 2),
                                                             "closing": closing})


def problems(agent: "DuelAgent", move: "Move", text: str, obs: Observation) -> list[str]:
    """The guards on the words alone: the move is code's and already checked."""
    v = agent.view
    out = []
    if not text.strip():
        out.append("empty")
    if bad := mentions_past_limit(v, text):
        out.append(f"names {bad}")
    if move.action != "accept" and reads_as_agreement(text):
        out.append("reads as agreement")
    out += claims(v, text, *agent._named(move.action, move.price, move.days, obs))
    return out


async def write(agent: "DuelAgent", move: "Move", obs: Observation) -> "Move":
    """One text call for a fixed move, within TEXT_TIMEOUT_S; code's plain words on a timeout, a model error or a
    text the guards reject (no second call: that retry is what cost Duels II its 14%)."""
    v = agent.view
    what = ("accept their standing offer" if move.action == "accept" else
            f"offer {money(move.price, v.currency)}" + (f", delivery on day {move.days}" if move.days is not None
                                                         else ""))
    note = (f"{A.OWN_NOTE} Your side's move this turn is fixed: {what}. Write only the message that goes with it: "
            "one or two short sentences, in the language of the conversation."
            + (" You may name their day as the other choice, at a price no better for them than this one."
               if move.meta.get("day_call") == "menu" else ""))
    try:
        r = await asyncio.wait_for(agent.negotiator.parse(Words, agent.text_system, A.with_note(A.transcript(obs),
                                                                                              note)), TEXT_TIMEOUT_S)
        agent._record("text", r)
        text = r.parsed.message  # type: ignore[attr-defined]
    except (TimeoutError, asyncio.TimeoutError):
        move.meta["text"] = f"timeout after {TEXT_TIMEOUT_S:g} s: plain words"
        text = ""
    except LLMError as e:
        move.meta["text"] = f"model error ({e}): plain words"
        text = ""
    if text and (found := problems(agent, move, text, obs)):
        move.meta |= {"text": "rejected: plain words", "text_problems": found, "drafted_text": text}
        text = ""
    move.text = text or plain(move, v.currency)
    return move
