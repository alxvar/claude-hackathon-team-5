"""Experiment 4b: Sunday's candidate model setups on the calibration duels (paid). Quality next to tonight's setup.

    PYTHONHASHSEED=0 python -m redteam.setups "opus-low/sonnet-low (Duels I)"   (the seed keeps the duels the same
                                                                                across runs)
"""
from __future__ import annotations

import asyncio
import json
import sys

from . import SCRATCH
from .calibrate import build, summary, waves, SUBSET
from .latency import SETUPS
from .llm import live_models, spent


def main() -> None:
    name = sys.argv[1]
    s, n = live_models(*SETUPS[name], cassette="setup-" + name.split(" ")[0].replace("/", "_"))
    scen = [x for x, c in zip(build(), SUBSET) if c[2] == "words"]      # the 20 duels with a readable weight
    rows = asyncio.run(waves(scen, s, n, name))
    (SCRATCH / f"setup-{name.split(' ')[0].replace('/', '_')}.json").write_text(json.dumps(rows, default=str))
    m = summary(rows)
    print(f"| {name} | {m['n']} | {m['deals']:.0%} | {m['points']:.3f} | {m['rounds']:.1f} | {m['bad']} |")
    print(f"spend so far ${spent():.2f}")


if __name__ == "__main__":
    main()
