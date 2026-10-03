"""Experiment 4: Sunday's 15 s ticks with 6 duels at once.

    python -m redteam.latency burst [--bursts 5]     # paid: 6 decisions at once per burst, per model setup
    python -m redteam.latency live [--tick 15]       # $0: the real runner loop in real time, fake models that take
                                                     # as long as the measured calls (6 duels, one wave)
"""
from __future__ import annotations

import argparse
import asyncio
import json
import random
import statistics as st
import time
from pathlib import Path

from agents.duelist.agent import BandPlan, Decision, DuelAgent
from agents.duelist.model import Offer
from engine import Reply

from . import SCRATCH
from .arena import DUEL_TICKS, FakeServer, new_runner, policy_negotiate, policy_plan, result, scenario
from .baits import VIEW, obs

SETUPS = {
    "opus-medium/sonnet-low (tonight)": ("claude-opus-5-5", "medium", "claude-sonnet-5-5", "low"),
    "opus-low/sonnet-low (Duels I)": ("claude-opus-5-5", "low", "claude-sonnet-5-5", "low"),
    "sonnet-medium/sonnet-low": ("claude-sonnet-5-5", "medium", "claude-sonnet-5-5", "low"),
    "sonnet-low/haiku": ("claude-sonnet-5-5", "low", "claude-haiku-4-5", "low"),
}
OUT = SCRATCH / "latency"


# Part B: bursts of 6 real decisions

def variants() -> list:
    out = []
    for i, (p, d, t) in enumerate([(85, 10, "I can do 85 P. Delivery on day 10."), (90, 10, "90."),
                                   (95, 0, "95 P, day 0."), (80, 5, "80 P on day 5, final."),
                                   (100, 10, "I can do 100 P. Delivery on day 10."), (70, 0, "70?")]):
        o = obs(t)
        o.turns[-1].offer = Offer(price=p, days=d)
        o.rival_offer = Offer(price=p, days=d)
        out.append(o)
    return out


async def burst(setup: str, n: int) -> list[dict]:
    from .llm import live_models
    s, ng = live_models(*SETUPS[setup])
    rows = []
    for b in range(n):
        async def one(o):
            a = DuelAgent(VIEW, s, ng)
            t = time.perf_counter()
            m = await a.respond(o)
            return {"setup": setup, "burst": b, "took": time.perf_counter() - t, "fallback": m.meta.get("fallback"),
                    "calls": [(c["stage"], c["model"], c["latency_s"]) for c in m.meta.get("calls", [])]}
        rows += await asyncio.gather(*(one(o) for o in variants()))
    return rows


def q(xs, p):
    xs = sorted(xs)
    return xs[min(int(p * len(xs)), len(xs) - 1)] if xs else float("nan")


def burst_main(n: int) -> None:
    from .llm import spent
    OUT.mkdir(exist_ok=True)
    allrows = []
    for setup in SETUPS:
        rows = asyncio.run(burst(setup, n))
        allrows += rows
        took = [r["took"] for r in rows]
        print(f"{setup}: n {len(took)}, p50 {q(took, .5):.1f} s, p90 {q(took, .9):.1f}, max {max(took):.1f}; "
              f"> 10 s: {sum(t > 10 for t in took)}; fallbacks {sum(bool(r['fallback']) for r in rows)}; "
              f"spend so far ${spent():.2f}", flush=True)
    (OUT / "bursts.json").write_text(json.dumps(allrows))


# Part A: the real runner loop, in real time

class Realtime(FakeServer):
    """The tick moves with the wall clock; at each new tick the rivals move first."""

    def __init__(self, duels, start: int, tick_seconds: float):
        super().__init__(duels, start, tick_seconds)
        self.t0, self.start = time.monotonic(), start
        self.sent_at: list[tuple[int, int, float]] = []          # (duel, tick, seconds into the tick)
        self.bots_act()

    def _advance(self) -> None:
        now = self.start + int((time.monotonic() - self.t0) // self.tick_seconds)
        while self.tick < now:
            self.tick += 1
            self.expire()
            self.bots_act()

    def clock(self):
        self._advance()
        return {**super().clock(), "next_tick_in": self.tick_seconds - (time.monotonic() - self.t0) % self.tick_seconds}

    def duels(self, done=False):
        self._advance()
        return super().duels(done)

    def duel_say(self, did, text="", price=None, days=None):
        self._advance()
        self.sent_at.append((did, self.tick, (time.monotonic() - self.t0) % self.tick_seconds))
        return super().duel_say(did, text, price, days)

    def duel_accept(self, did):
        self._advance()
        self.sent_at.append((did, self.tick, (time.monotonic() - self.t0) % self.tick_seconds))
        return super().duel_accept(did)


class Slow:
    """The code stand-in's answer, after a delay drawn from measured call latencies."""

    def __init__(self, stage: str, samples: list[float], rng: random.Random, label: str):
        self.stage, self.samples, self.rng, self.label = stage, samples, rng, label

    async def parse(self, schema, system, messages):
        await asyncio.sleep(self.rng.choice(self.samples))
        return Reply(None, 0.0, 0, 0, 0.0, "slow")


def patch_slow_policy(strategist: Slow, negotiator: Slow) -> None:
    async def plan(self, obs):
        await strategist.parse(BandPlan, "", [])
        return await policy_plan(self, obs)

    async def negotiate(self, obs, band, plan_, days, feedback):
        await negotiator.parse(Decision, "", [])
        return await policy_negotiate(self, obs, band, plan_, days, feedback)
    DuelAgent.plan, DuelAgent.negotiate = plan, negotiate


def samples(setup: str) -> tuple[list[float], list[float]]:
    """Per-call latencies by stage: from the bursts if run, else the calibration cassettes (tonight's setup)."""
    strat, neg = [], []
    f = OUT / "bursts.json"
    if f.exists():
        for r in json.loads(f.read_text()):
            if r["setup"] == setup:
                for stage, _, lat in r["calls"]:
                    (strat if stage == "strategist" else neg).append(lat)
    if not strat:
        for name, into in (("calib-strategist", strat), ("calib-negotiator", neg)):
            p = SCRATCH / "cassettes" / f"{name}.jsonl"
            for line in p.read_text().splitlines() if p.exists() else []:
                into.append(json.loads(line)[1]["latency_s"])
    return strat, neg


async def live_wave(setup: str, tick: float, seed: int = 3, failover_budget: float | None = None) -> dict:
    strat, neg = samples(setup)
    rng = random.Random(seed)
    patch_slow_policy(Slow("strategist", strat, rng, setup), Slow("negotiator", neg, rng, setup))
    scen = [scenario(i + 1, random.Random(seed * 10 + i), k, "own", "words", ("seller", "buyer")[i % 2])
            for i, k in enumerate(["clock", "follower", "clock", "holder", "follower", "clock"])]
    start = 2000
    for x in scen:
        x.start = start
    server = Realtime(scen, start, tick)
    r = new_runner(server, Slow("s", [0], rng, "x"), Slow("n", [0], rng, "x"), tick, name=f"live-{tick}")
    r.poll_s = 2.0
    task = asyncio.create_task(r.run())
    while server.tick < start + DUEL_TICKS:
        await asyncio.sleep(1)
        server._advance()
    task.cancel()
    rows = [result(x, r) for x in scen]
    fallbacks = timeouts = decisions = late = 0
    for line in r.log.path.read_text().splitlines():
        e = json.loads(line)
        if e["event"] == "decision":
            decisions += 1
            fb = (e["move"]["meta"] or {}).get("fallback") or ""
            fallbacks += bool(fb)
            timeouts += "timeout" in fb
            if e["took_s"] > tick:
                late += 1
    return {"setup": setup, "tick": tick, "decisions": decisions, "fallbacks": fallbacks, "timeouts": timeouts,
            "slower_than_a_tick": late, "deals": sum(x["deal"] for x in rows), "n": len(rows),
            "points": round(st.mean(x["points"] for x in rows), 3),
            "send_s_into_tick_p90": round(q([s for _, _, s in server.sent_at], .9), 1),
            "strat_p50": round(q(strat, .5), 1), "strat_p95": round(q(strat, .95), 1), "neg_p50": round(q(neg, .5), 1)}


def live_main(tick: float, setups: list[str]) -> None:
    for setup in setups:
        print(json.dumps(asyncio.run(live_wave(setup, tick))), flush=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("part", choices=["burst", "live"])
    p.add_argument("--bursts", type=int, default=5)
    p.add_argument("--tick", type=float, default=15.0)
    p.add_argument("--setup", nargs="*", default=list(SETUPS))
    a = p.parse_args()
    burst_main(a.bursts) if a.part == "burst" else live_main(a.tick, a.setup)


if __name__ == "__main__":
    main()
