"""Experiment 1: days duels against Duels I's rival types x how they handle the day x how the game states our day
weight, with the code stand-in for the models ($0). Variants patch the duelist's constants in this process only.

    PYTHONHASHSEED=0 python -m redteam.days [--seeds 5] [--variant NAME ...]   (the hash seed fixes the duels)
"""
from __future__ import annotations

import argparse
import json
import random
import statistics as st
from collections import defaultdict
from contextlib import contextmanager
from typing import Any

from agents.duelist import agent as A, runner as R

from . import SCRATCH
from .arena import DAY_MODES, KINDS, SHAPES, run_waves, scenario, use_policy

VARIANTS: dict[str, dict[tuple[Any, str], Any]] = {
    "live": {},
    "open_wait_0": {(R, "OPEN_WAIT"): 0},
    "late_switch_6": {(A, "LATE_SWITCH_LEFT"): 6},
    "late_switch_2": {(A, "LATE_SWITCH_LEFT"): 2},
    "no_late_switch": {(A, "LATE_SWITCH_LEFT"): -1},
    "accept_by_3": {(R, "ACCEPT_BY"): 3},
    "give_cost_30": {(A, "GIVE_COST_P"): 30},
    "same_side_5": {(A, "DAY_SAME_SIDE_P"): 5},
    # the late switch only when their standing offer is past our limit (inside it, the deadline accept takes it anyway)
    "late_switch_if_out": {(A.DuelAgent, "late_switch"): (lambda f: lambda self, obs: None if (
        (t := A.standing_offer(obs)) is not None and not A.past_limit(self.view, t.price, t.days)) else f(self, obs))(
        A.DuelAgent.late_switch)},
    # a rival that has sent no PRICED offer (only text, e.g. 'Hola.') counts as silent: the code walk applies
    "silent_no_offer": {(A, "silent"): (_s := lambda obs: not A.their_offers(obs)), (R, "silent"): _s},
}


@contextmanager
def patched(changes: dict[tuple[Any, str], Any]):
    old = {k: getattr(*k) for k in changes}
    try:
        for (mod, name), v in changes.items():
            setattr(mod, name, v)
        yield
    finally:
        for (mod, name), v in old.items():
            setattr(mod, name, v)


def grid(seeds: int, kinds=KINDS, modes=DAY_MODES, shapes=SHAPES) -> list:
    out, i = [], 1
    for seed in range(seeds):
        for kind in kinds:
            for mode in modes:
                for shape in shapes:
                    for role in ("seller", "buyer"):
                        rng = random.Random(hash((seed, kind, mode, shape, role)) & 0xFFFFFFFF)
                        out.append(scenario(i, rng, kind, mode, shape, role))
                        i += 1
    return out


def table(rows: list[dict], key: str) -> str:
    g: dict[Any, list[dict]] = defaultdict(list)
    for r in rows:
        g[r[key]].append(r)
    lines = [f"| {key} | n | deals | points/duel | rounds/deal | day lost (P of pie) | bad |", "|---|---|---|---|---|---|---|"]
    for k, rs in sorted(g.items(), key=lambda kv: str(kv[0])):
        deals = [r for r in rs if r["deal"]]
        lines.append(f"| {k} | {len(rs)} | {len(deals) / len(rs):.0%} | {st.mean(r['points'] for r in rs):.3f} | "
                     f"{st.mean(r['rounds'] for r in deals) if deals else 0:.1f} | "
                     f"{st.mean(r['day_gap'] for r in deals) if deals else 0:.1f} | "
                     f"{sum(bool(r['bad']) for r in rs)} |")
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--seeds", type=int, default=3)
    p.add_argument("--variant", nargs="*", default=["live"])
    a = p.parse_args()
    use_policy()
    results: dict[str, list[dict]] = {}
    for name in a.variant:
        with patched(VARIANTS[name]):
            rows = run_waves(grid(a.seeds))
        results[name] = rows
        n = len(rows)
        print(f"\n## {name}: {n} duels, deals {sum(r['deal'] for r in rows) / n:.1%}, points/duel "
              f"{st.mean(r['points'] for r in rows):.4f}, bad {sum(bool(r['bad']) for r in rows)}")
        if name == a.variant[0]:
            for key in ("kind", "days", "shape", "role"):
                print("\n" + table(rows, key))
            bad = defaultdict(int)
            for r in rows:
                for b in r["bad"]:
                    bad[(b, r["shape"])] += 1
            print("\nbad by (what, shape):", dict(bad))
    if len(results) > 1:
        base = results[a.variant[0]]
        print("\n| variant | points/duel | Δ vs first | paired wins/losses | deals | bad |\n|---|---|---|---|---|---|")
        for name, rows in results.items():
            d = [x["points"] - y["points"] for x, y in zip(rows, base)]
            print(f"| {name} | {st.mean(r['points'] for r in rows):.4f} | {st.mean(d):+.4f} | "
                  f"{sum(v > 1e-9 for v in d)}/{sum(v < -1e-9 for v in d)} | "
                  f"{sum(r['deal'] for r in rows) / len(rows):.1%} | {sum(bool(r['bad']) for r in rows)} |")
    (SCRATCH / "days.json").write_text(json.dumps(results, default=str))


if __name__ == "__main__":
    main()
