#!/usr/bin/env python3
"""Rebuild race-data.js (the race chart's data) from data/leaderboard.jsonl. Read-only: no game request.
Run from anywhere: python3 judges/pitch/a5/race_data.py"""
import json, pathlib

here = pathlib.Path(__file__).resolve().parent
src = here.parents[2] / "data" / "leaderboard.jsonl"
snaps, seen = [], set()
for line in src.read_text().splitlines():
    if not line.strip():
        continue
    r = json.loads(line)
    if r["tick"] in seen:
        continue
    seen.add(r["tick"])
    snaps.append(r)
snaps.sort(key=lambda r: r["tick"])
teams = sorted({t["team"] for r in snaps for t in r["teams"]})
out = {
    "source": "data/leaderboard.jsonl",
    "ticks": [r["tick"] for r in snaps],
    "score": {tm: [next((t["score"] for t in r["teams"] if t["team"] == tm), None) for r in snaps] for tm in teams},
    "us": {
        "rank": [sorted(r["teams"], key=lambda t: -t["score"]).index(next(t for t in r["teams"] if t["team"] == "t05")) + 1 for r in snaps],
        "negotiating": [next(t["negotiating"] for t in r["teams"] if t["team"] == "t05") for r in snaps],
        "market": [next(t["market"] for t in r["teams"] if t["team"] == "t05") for r in snaps],
    },
}
(here / "race-data.js").write_text("window.RACE = " + json.dumps(out, separators=(",", ":")) + ";\n")
print(f"race-data.js: {len(snaps)} snapshots, ticks {snaps[0]['tick']}-{snaps[-1]['tick']}, {len(teams)} teams")
