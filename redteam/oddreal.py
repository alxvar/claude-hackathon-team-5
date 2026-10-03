"""Experiment 1c: the odd rivals the stand-in flagged, with the real models (one wave of 6, paid ~$1-2):
a rival that flips its day every tick (the stand-in followed it: 11-14 rounds), and one that sends no day at all.

    python -m redteam.oddreal
"""
from __future__ import annotations

import asyncio
import json
import random

from . import SCRATCH
from .arena import play, result, scenario
from .llm import live_models, spent

CASES = [("clock", "flip", "words", "seller"), ("clock", "flip", "words", "buyer"),
         ("follower", "flip", "words", "seller"), ("follower", "flip", "words", "buyer"),
         ("clock", "none", "words", "seller"), ("acceptonly", "none", "words", "buyer")]


def main() -> None:
    scen = [scenario(i + 1, random.Random(7 + i), *c) for i, c in enumerate(CASES)]
    s, n = live_models(cassette="odd")
    server, r = asyncio.run(play(scen, s, n, name="odd"))
    rows = [result(x, r) for x in scen]
    for x, row in zip(scen, rows):
        print(json.dumps({k: row.get(k) for k in ("kind", "days", "role", "deal", "price", "day", "rounds", "points",
                                                   "our_msgs", "bad", "refusals")}))
        print("   " + " | ".join(f"{m['tick'] - 1000}{'U' if m['from'] == 'you' else 'R'} {m['price']}/{m['days']}"
                                for m in x.messages))
    (SCRATCH / "oddreal.json").write_text(json.dumps(rows, default=str))
    print(f"spend so far ${spent():.2f}")


if __name__ == "__main__":
    main()
