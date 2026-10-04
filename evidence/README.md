# evidence/ · the game data behind every number (frozen at the 15:00 close)

A copy of the collector's output (`data/`, which is git-ignored because it keeps growing), taken after the game closed. Every score, rank and time in the README, the pitch and `intel/` can be checked here.

| File | What | Key rows |
|---|---|---|
| `leaderboard.jsonl` | Every public leaderboard snapshot, all 18 teams, Fri → Sun | tick 160 (Friday frozen: us #6, 19.99) · tick 1440 (Saturday close: us #3, 30.49 vs Team 10 37.58) · tick 2802 (final: **us #1, 37.73** vs Team 10 35.76) |
| `me.jsonl` | Our own score components, one row per change (`/api/me`) | last row: negotiating 24.64, market 13.08, neg_points 104.8, duel_points 35.84, 74 deals |
| `v10_listings.jsonl` | Every listing seen on our venue v10 | |
| `bench/` | Every Market Test session recorded by `broker/record_bench.py`, plus `results.jsonl` | |

Not included: the raw public feed (`data/feed.jsonl`, ~19 MB); the hub (`hub/`, Neon) keeps the shared copy of the game's events. Per-duel records are in `docs/duels/`.
