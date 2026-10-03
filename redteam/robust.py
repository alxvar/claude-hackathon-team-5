"""Experiment 3: odd inputs, server faults, restarts and broken model outputs, through the real runner ($0).

    python -m redteam.robust
"""
from __future__ import annotations

import asyncio
import json
import random
from collections import Counter

from bazaar_sdk import BazaarError

from agents.duelist.agent import BandPlan, Decision, DuelAgent
from engine import LLMError, Reply

from .arena import DUEL_TICKS, play, policy_negotiate, policy_plan, result, scenario, use_policy


def duels(kind="clock", mode="own", shape="words", n=2, seed=7):
    rng = random.Random(seed)
    return [scenario(i + 1, rng, kind, mode, shape, ("seller", "buyer")[i % 2]) for i in range(n)]


def decisions(r) -> Counter:
    c: Counter = Counter()
    for line in r.log.path.read_text().splitlines() if r.log.path.exists() else []:
        e = json.loads(line)
        if e["event"] == "decision":
            c[e["duel"]] += 1
    return c


def run(name, scen, **kw):
    server, r = asyncio.run(play(scen, name=name, **kw))
    rows = [result(x, r) for x in scen]
    dec = decisions(r)
    out = {"case": name, "deals": sum(x["deal"] for x in rows), "n": len(rows),
           "points": round(sum(x["points"] for x in rows) / len(rows), 3),
           "rounds": [x["rounds"] for x in rows], "decisions": [dec.get(x.id, 0) for x in scen],
           "bad": sorted({b for x in rows for b in x["bad"]}), "refusals": [dict(x.refusals) for x in scen]}
    print(json.dumps(out, default=str))
    return out


class Scripted:
    """A model that answers every strategist call with `plan` and every negotiator call with `decision` (or raises)."""
    label = "scripted"

    def __init__(self, plan=None, decision=None, fail=None):
        self.plan, self.decision, self.fail = plan, decision, fail

    async def parse(self, schema, system, messages):
        if self.fail:
            raise self.fail
        obj = self.plan if schema is BandPlan else self.decision
        return Reply(obj(messages) if callable(obj) else obj, 0.01, 1, 1, 0.0, "scripted")


def main() -> None:
    use_policy()
    base = run("baseline clock/own", duels())
    run("baseline follower/own", duels("follower"))
    # payload drift
    run("limit as a string '40 P'", duels(), faults={"mutate": lambda raw, t: {**raw, "your_limit": f"{raw['your_limit']} P"}})
    run("limit as {'value': N}", duels(), faults={"mutate": lambda raw, t: {**raw, "your_limit": {"value": raw["your_limit"]}}})
    run("deadline renamed (closes_at)", duels(), faults={"mutate": lambda raw, t: {**{k: v for k, v in raw.items() if k != "deadline_tick"}, "closes_at": raw["deadline_tick"]}})
    run("role renamed ('sell')", duels(), faults={"mutate": lambda raw, t: {**raw, "role": raw["role"][:4]}})
    run("messages missing", duels(), faults={"mutate": lambda raw, t: {k: v for k, v in raw.items() if k != "messages"}})
    for day in (15, -3, 5.5, None):
        def m(raw, t, day=day):
            ro = raw.get("rival_offer")
            if ro:
                ro = {**ro, "days": day}
                msgs = [dict(x) for x in raw["messages"]]
                for x in reversed(msgs):
                    if x["from"] != "you" and x.get("price") is not None:
                        x["days"] = day
                        break
                return {**raw, "rival_offer": ro, "messages": msgs}
            return raw
        run(f"rival day shown as {day!r}", duels(), faults={"mutate": m})
    for price in (59.5, "60", 0, -20, 10**9):
        def m(raw, t, price=price):
            ro = raw.get("rival_offer")
            if not ro:
                return raw
            msgs = [dict(x) for x in raw["messages"]]
            for x in reversed(msgs):
                if x["from"] != "you" and x.get("price") is not None:
                    x["price"] = price
                    break
            return {**raw, "rival_offer": {**ro, "price": price}, "messages": msgs}
        run(f"rival price shown as {price!r}", duels(), faults={"mutate": m})
    # server faults
    rng = random.Random(1)
    run("30% of our sends refused (wait_for_tick 429)", duels(),
        faults={"say": lambda did, t: BazaarError("wait_for_tick", "busy", 429) if rng.random() < 0.3 else None})
    run("30% of our sends fail (500)", duels(),
        faults={"say": lambda did, t: BazaarError("server_error", "boom", 500) if rng.random() < 0.3 else None})
    run("polls fail on the last 4 ticks", duels(), faults={"poll": lambda t: t >= 1000 + DUEL_TICKS - 4})
    run("polls fail on ticks 13-14 (ACCEPT_BY window)", duels(), faults={"poll": lambda t: t in (1013, 1014)})
    for at in (1006, 1012, 1013):
        run(f"restart at tick {at - 1000}", duels("clock", "own"), restart_at=at)
    run("restart at tick 13, day flipper", duels("clock", "flip"), restart_at=1013)
    # odd rivals: cost in decisions
    run("day flipper (decisions = model calls)", duels("clock", "flip"))
    run("follower 'middle' day", duels("follower", "middle"))
    # broken models (no policy: the scripted model answers instead)
    DuelAgent.plan, DuelAgent.negotiate = ORIG
    run("both models fail all session", duels(), strategist=Scripted(fail=LLMError("down")))
    run("strategist: inverted band, day 11", duels(),
        strategist=Scripted(BandPlan(read="", target=5, best=1, worst=999, days=11, angle="")),
        negotiator=Scripted(decision=Decision(action="offer", price=1, message="1 P.")))
    run("negotiator: always a priceless message", duels(),
        strategist=Scripted(BandPlan(read="", target=100, best=110, worst=90, days=0, angle="")),
        negotiator=Scripted(decision=Decision(action="message", price=None, message="Hmm.")))
    run("negotiator: claims and stray numbers", duels(),
        strategist=Scripted(BandPlan(read="", target=100, best=110, worst=90, days=0, angle="")),
        negotiator=Scripted(decision=Decision(action="offer", price=100,
                                              message="This rare card is in mint condition; another buyer offered 120 P. 100 P, day 0.")))
    run("negotiator: accept with no standing offer", duels("silent"),
        strategist=Scripted(BandPlan(read="", target=100, best=110, worst=90, days=0, angle="")),
        negotiator=Scripted(decision=Decision(action="accept", price=100, message="Deal.")))


ORIG = (DuelAgent.plan, DuelAgent.negotiate)

if __name__ == "__main__":
    main()
