# broker/: Market Test tooling (Team 5)

Market-making is 30 % of the score. Most of it is the **Market Test** ("bench"): every venue gets the same synthetic book
of buyers and sellers (10 traders × 16 ticks; 12 at the hard bench, game hour 16.0). The score is the share of the
possible gains, between the traders' hidden limits, that the venue's matching realises. The free `auto` stall earns
half the points; full points go to the mean of the top three. Rules: `bazaar-kit/RULES.md` (Your own market), plan
`intel/saturday-plan.md` §4E, playbook `intel/market-playbook.md`.

| File | What |
|---|---|
| `record_bench.py` | Read-only recorder: bench book states → `data/bench/bench-h05.0.jsonl`; our bench fields + every team's `market` after each session → the same file and `data/bench/results.jsonl` |
| `broker.py` | Deterministic broker for a `board` venue: `auto_clone` (= the stall), `v1` (auto_clone + impatience rule, can only add pairs), `v1_literal` (experimental) |
| `replay.py` | Replays recorded or simulated sessions through any strategy → realised share of possible gains, `--compare`, quote-oracle ceiling |
| `sim.py` | Offline trader model (all guesses are `Model` parameters): calibrate it on recorded sessions |
| `common.py` | Keyless reads, tick clock, broker-key lookup, key scrubbing |
| `../tests/test_broker.py` | 23 offline tests: `uv run pytest tests/test_broker.py -s` |

Run everything from the repo root after `source .env`. Keys never get printed or written: every file line goes through
`scrub()`, which drops any field whose name contains "key".

## Run

### Recorder (read-only, GET only)
```bash
python3 -m broker.record_bench --once     # clock, scheduled benches, broker key found or not, our bench fields, top market
python3 -m broker.record_bench --loop     # all day; book 2/s while a bench is live or due, every 5 s otherwise
python3 -m broker.record_bench --loop --no-book   # results only, when broker.py --record already reads that key's book
```
- Broker key: `BROKER_KEY` from the env (our own venue) wins; otherwise the stall's key from `/api/me`
  (`starter_broker_key` per the SDK; any `*broker_key` field is accepted). **Friday 23:00: `/api/me` has no such
  field yet** (the stall exists from game hour 3.0). Without a key the loop still saves the results after every
  scheduled bench, and looks for a key once a minute.
- Session = the schedule's bench entry (`bench-h05.0`); a bench seen in the book but not in the schedule is named after
  its run ids. A session ends when the book has had no bench offers for 2 ticks; results are saved at +5 s, +3 min,
  +7 min (the leaderboard snapshot refreshes every few minutes).
- File lines: `meta` (schedule entry, venue fees, runs), `book` (tick, t_hours, the whole book; at least one per tick,
  plus every change), `match` (from `broker.py --record`), `end`, `result` (me: `bench_efficiency`, `bench_points`,
  `mm_points`, `bench_venue`, `market`; every team's `market`; every venue's mechanism).

### Broker (only on a `board` venue; on `auto` the engine crosses first)
```bash
BROKER_KEY=bk_... python3 -m broker.broker --strategy auto_clone --dry-run   # print what it would post
BROKER_KEY=bk_... python3 -m broker.broker --strategy auto_clone --record    # live + record the sessions
BROKER_KEY=bk_... python3 -m broker.broker --strategy v1 --record
```
- One heartbeat line per tick: `tick N · strategy · bench offers/runs · public · planned · posted · refused · errors`.
- Exits 1 after `--max-errors` (20) consecutive failures of one kind (book/clock reads, planning, 5xx/network match
  errors), 2 if the key is missing or rejected, so the supervisor restarts it. Nothing else stops the loop (odd book
  shapes and recorder errors are logged and skipped).
- Also crosses our venue's real offers card by card (as the starter broker does): value created on our venue scores.
- Never re-posts a pair (posted ids are excluded until they leave the book); plans once per book state. A run absent
  for 2 ticks is forgotten (quote history, start tick), so a later session reusing the same ids starts clean.
- Bench matches ignore the venue fee, as `starter_broker.bench_plan` does (`--bench-fee` to change). Open the venue at fee 0.
- Supervision: `tools/daemons.sh` is Lucas's file; the lines to add to `cmd_for` (run from any cwd):
  ```
  recorder) echo "python3 -u $R/broker/record_bench.py --loop" ;;           # stall phase
  broker)   echo "python3 -u $R/broker/broker.py --strategy auto_clone --record" ;;   # once our venue is open
  ```
  With `broker --record` running, stop the recorder or run it `--no-book` (both reading one key's book = double the
  reads). The broker's recording also saves the results; a `--no-book` recorder skips sessions already on disk.

### Replay
```bash
python3 -m broker.replay data/bench/bench-h05.0.jsonl                         # every strategy, one session
python3 -m broker.replay data/bench/bench-h*.jsonl --compare auto_clone v1    # paired, all recorded sessions
python3 -m broker.replay data/bench/bench-h05.0.jsonl --strategy v1 -v        # its matches, tick by tick
python3 -m broker.replay --sim all --seeds 200 --compare auto_clone v1        # 9 trader models
python3 -m broker.replay --sim hard-12 --seeds 3 --write data/bench/sim       # sim sessions as recorder files
```
- Sim sessions carry true limits. Recorded ones don't: a trader's limit is proxied by its most relaxed quote, so a
  recorded score is a **proxy** (comparable between strategies on one file; biased toward the stall, because a trader
  matched early never shows how far it would have relaxed). Check it against the server's `bench_efficiency`, printed
  under the table when the file has a `result` line.
- `quote-oracle` = the hindsight ceiling of any broker that only crosses quotes (max-weight matching over pairs that
  crossed at some tick while both were in the book). `oracle − auto_clone` is the room a better broker could take.
- `--censor leave` (default): a recorded trader is matchable only while it was in the book. `hold`: a trader the
  recording shows as matched stays at its last quote until the run ends (optimistic for variants).

## Offline results (Fri night, `broker/sim.py` traders, true limits)

Seeds 0-199 (the test set). Efficiencies are shares of the possible gains; differences are in percentage points.

| Model | auto_clone | v1 | v1 − auto_clone | quote-oracle (− auto_clone) |
|---|---|---|---|---|
| default (10 traders) | 0.9461 ± 0.126 | 0.9461 ± 0.126 | +0.00 pp (200 equal) | 0.983 (+3.7 pp) |
| hard-12 (12, impatient 0.7, firm 0.4: our guess) | 0.9283 ± 0.128 | 0.9285 ± 0.128 | +0.03 ± 0.40 pp (1 better, 0 worse) | 0.980 (+5.2 pp) |

Held out (seeds 1000-2999, 2,000 sessions per model, all 9 models): v1 − auto_clone is −0.006 to +0.013 pp, and v1
differs in at most 6 of 2,000 sessions per model (worse in at most 2). What we learned:
- **v1 is safe but nearly inert on these traders.** Each tick it matches every trader the stall would, plus maybe some
  (an augmenting path re-pairs the stall's traders to bring in a fast-relaxing one). Per session it can still differ
  either way, since the extra pair changes who is left later. After the stall's greedy pass the leftover book never
  crosses, and new crossings appear one at a time, so there is rarely anything to add. The last-2-ticks rule never
  changed a session's outcome.
- **The rule as first written (`v1_literal`: urgent first, may displace a stall trader) is a coin flip**: −0.10 to
  +0.03 pp held out, losing about as often as it wins (seeds 0-199: worst session −17.6 pp). Relax speed mixes shade
  size and patience, and quotes alone can't separate the two in this model.
- **Crossing as many pairs as possible loses**: sim.py's `most_pairs` is −3 pp on default; even keeping every stall pair
  and adding every possible one each tick is −0.02 to −8.3 pp in 7 of 9 models. Matching more pairs early uses up
  traders who had better partners later.
- **The headroom is real: +3.4 pp (default), +4.8 pp (hard-12)** between the stall and the quote-oracle (seeds
  1000-1999; +3.7 / +5.2 pp on the test seeds above), present in 36-48 % of sessions. It sits mostly in tick-0 pairing (which bid gets the cheap ask: e.g. leave a cheap
  impatient seller to a patient buyer who will cross it next tick, and give the high bid the firm seller only it can
  reach). Capturing it needs a signal about limits or departures that the sim's quotes don't carry. **Look for one in
  the real book.**

## The learning loop (every bench, ~2 h apart)
1. **Before**: recorder running (or broker `--record`); `record_bench --once` shows the key and the next bench.
2. **During** (16 ticks: 8 min Sat, 4 min Sun): watch the heartbeat only.
3. **Right after**: `results.jsonl`: our `bench_efficiency`/`bench_points`; every team's `market`; which venues are
   `board`. Did anyone beat the stall's half points?
4. **Score**: `replay FILE --compare auto_clone v1` + the quote-oracle line: how much room did this session have?
5. **Calibrate** `sim.Model` on the recorded traders (shade, relax curve, departures, firm share, limit range), re-run
   `replay --sim` on the calibrated model, try variants (a new strategy is a function in `broker.py` + a name in
   `STRATEGIES`; the tests check it for crossing violations and the live-loop/replay equality for free).
6. **Deploy** a variant only if it beats `auto_clone` on the real replays and the calibrated sim and never falls more
   than 1 pp below it; restart the broker **between** sessions.

## Failure modes
- **A `board` venue whose broker is down during a session scores 0** for that session (the stall would have scored
  half). Run it under `daemons.sh` on a machine that doesn't sleep (`caffeinate`), and check the heartbeat before each
  bench.
- **Open or close a venue only between sessions.** Each session counts our best venue open during it; closing after a
  good session keeps nothing.
- Broker restarted mid-run: v1 loses its quote history (needs 2 ticks to see relaxing) and the run's start tick (the
  last-2-ticks rule may fire late); auto_clone is unaffected.
- The stall's book is read **after** the engine's own crossing [Uncertain]: a stall recording shows the leftovers and
  the stall's settlements, so it calibrates the model but can't prove replay equality. Equality needs a recording of
  our own `board` venue (`broker --record`).
- Broker + recorder book polling on one key ≈ 5 req/s, the per-key limit: use `--no-book` on the recorder.
- A refused match costs nothing; the broker logs `refused (code: why)` and moves on. Repeated 5xx/network errors exit 1.

## Check after the first real bench
1. Did `data/bench/bench-h0X.0.jsonl` get `book` lines? Does the stall's book show bench offers at all, or only what
   its engine left (M4)?
2. **The bench offer's fields**: anything beyond `id`/`give`/`want` (expiry tick, patience, a side flag, maker
   pseudonym, a limit hint)? An expiry field is the "who is about to leave" signal v1 lacks: switch v1's urgency to it.
3. Runs per session, traders per run, ticks per run; does everyone arrive at tick 0?
4. Quote paths: linear or stepped relaxation, firm share, departure ticks, limit range → `sim.Model`.
5. Settlements: their field name and price rule (midpoint?), so `load()` can tag matched offers precisely.
6. Server `bench_efficiency` for the stall vs our proxy and the sim's 0.93-0.95; `bench_points` for "as good as the
   stall" (half points?).
7. Leaderboard `market` of the board venues (Teams 6, 12, 13) vs stall teams: does anyone beat the stall (M2)?
8. If our broker ran: zero `refused` lines, one heartbeat per tick, `replay FILE --strategy auto_clone` reproduces the
   recorded `match` lines.

## [Uncertain]
- `starter_broker_key` is the field name (SDK docstring only; absent tonight). Broker keys' rate limit is separate from
  the team key's (rules say "per key").
- The bench charges no venue fee (inferred from `starter_broker.bench_plan`). Irrelevant at fee 0.
- Whether the book carries the tick or the session's end; we label states with `/api/clock`'s tick, read around each
  tick boundary (a state read right at a boundary could carry the old tick).
- The hard-12 model's firm/impatient shares are our guess at "firmer and more impatient".
- Every v1 number above comes from our guessed trader model, not from real benches.
