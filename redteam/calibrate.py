"""Experiment 1b: the same days scenarios played by the code stand-in and by the real models (live setup), to see
whether the stand-in's verdicts hold. Paid: ~$0.1 a duel; the meter stops everything at REDTEAM_CAP_USD.

    PYTHONHASHSEED=0 python -m redteam.calibrate   (the hash seed fixes the duels)
"""
from __future__ import annotations

import json
import random
import statistics as st
import time

from agents.duelist.agent import DuelAgent

from . import SCRATCH
from .arena import play, policy_negotiate, policy_plan, result, scenario
from .llm import live_models, spent

import asyncio

SUBSET = ([(k, d, "words", r) for k in ("follower", "clock", "holder", "holder7", "acceptonly")
           for d in ("own", "middle") for r in ("seller", "buyer")]
          + [(k, "own", s, r) for k in ("follower", "clock") for s in ("unsure", "unreadable") for r in ("seller", "buyer")])


def build() -> list:
    out = []
    for i, (kind, mode, shape, role) in enumerate(SUBSET, 1):
        rng = random.Random(hash((0, kind, mode, shape, role)) & 0xFFFFFFFF)
        out.append(scenario(i, rng, kind, mode, shape, role))
    return out


async def waves(scen, strategist, negotiator, name):
    rows = []
    for i in range(0, len(scen), 6):
        wave = scen[i:i + 6]
        t = time.time()
        server, r = await play(wave, strategist, negotiator, name=name)
        rows += [result(x, r) for x in wave]
        print(f"{name}: wave {i // 6 + 1} done in {time.time() - t:.0f} s, spend so far ${spent():.2f}", flush=True)
    return rows


def summary(rows):
    n = len(rows)
    return {"n": n, "deals": sum(r["deal"] for r in rows) / n, "points": st.mean(r["points"] for r in rows),
            "rounds": st.mean([r["rounds"] for r in rows if r["deal"]] or [0]), "bad": sum(bool(r["bad"]) for r in rows)}


def main() -> None:
    orig = DuelAgent.plan, DuelAgent.negotiate
    DuelAgent.plan, DuelAgent.negotiate = policy_plan, policy_negotiate
    stand_in = asyncio.run(waves(build(), None, None, "standin"))
    DuelAgent.plan, DuelAgent.negotiate = orig
    s, n = live_models(cassette="calib")
    real = asyncio.run(waves(build(), s, n, "real"))
    out = {"standin": stand_in, "real": real}
    (SCRATCH / "calibrate.json").write_text(json.dumps(out, default=str))
    print("\n| | n | deals | points/duel | rounds/deal | bad |\n|---|---|---|---|---|---|")
    for k, rows in out.items():
        m = summary(rows)
        print(f"| {k} | {m['n']} | {m['deals']:.0%} | {m['points']:.3f} | {m['rounds']:.1f} | {m['bad']} |")
    print("\n| kind | days | shape | role | stand-in pts | real pts | real rounds | real day | real bad |")
    print("|---|---|---|---|---|---|---|---|---|")
    for a, b in zip(stand_in, real):
        print(f"| {a['kind']} | {a['days']} | {a['shape']} | {a['role']} | {a['points']:.2f} | {b['points']:.2f} | "
              f"{b['rounds']} | {b.get('day')} | {';'.join(b['bad'])} |")
    print(f"\nspend so far ${spent():.2f}")


if __name__ == "__main__":
    main()
