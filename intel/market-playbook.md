# Market-making playbook (owner: the Market session; Aleks reviews after Duels I)

Market-making is **30 points, as much as all of Negotiating**, and every team scored 0 on Friday: no Market Test has run.
Whoever learns the bench fastest takes this third of the game. Sunday's two benches weigh ~4× a Saturday bench each.

## 1. How it scores (RULES.md:66-84, 119, 122) [V]
- **Market Test (bench)**: every 2 game hours, every venue gets the same synthetic book: 10 traders over 16 ticks
  (the **hard** one at hour 16.0: 12 traders, "firmer and more impatient"). Score = share of the possible gains (between
  the traders' TRUE hidden limits) that our venue's matching realises.
- Each session counts our **best venue open during it**; no venue → 0. The round averages its sessions, so closing a
  venue after a good session keeps nothing.
- **Matching as well as the free auto stall = half the bench points; full points = the mean of the top three.** The exact
  curve between and below is unpublished (desk Q5). A small efficiency edge over the stall can be most of the other half.
- **Value created between OTHER teams on our venue** also scores (fees never count). We can't trade on our own venue.
- Teams without a venue get a free starter stall (`auto`). A broker can act only on a **`board`** venue; on `auto` the
  engine crosses every pair first.

## 2. Mechanics we must get right [V SDK/RULES]
- Open: `b.open_venue(name, fee_bps=0, rules={"mechanism": "board"})` (needs level 2; bond 250 refundable after a
  cooldown + 20 sunk). **It returns the broker key ONCE: write it to `.env` as `BROKER_KEY` immediately.**
- Broker: `GET /api/broker/book` (header `X-Broker-Key`) → `bench_offers` (ids like `b12-7`; seller ask = `want.cash`,
  buyer bid = `give.cash`); `POST /api/broker/matches {"sell": id, "buy": id, "price": p}` with ask ≤ p and p + fee ≤ bid,
  both from the same run. We choose WHICH crossing pairs and WHEN; we can't cross quotes that don't overlap.
- Open or close **only between sessions**. A board venue whose broker is down during a session scores 0 (worse than the
  stall's half): run the broker under `tools/daemons.sh` with a heartbeat, on a machine that doesn't sleep.

## 3. Our tools (built Fri night; see `broker/README.md`)
- `broker/record_bench.py`: records every bench book state to `data/bench/<session>.jsonl` + our bench fields + every
  team's `market` after the session.
- `broker/broker.py`: `auto_clone` (does exactly what the stall does) and `v1` (auto_clone + match the most impatient
  traders first + cross everything in the last 2 ticks).
- `broker/replay.py`: replays recorded or simulated sessions through any strategy → realised share; `--compare`.
- `broker/sim.py`: offline simulator (calibrate it on recorded sessions).

## 4. The learning loop (every bench, ~2 h apart)
1. **Before**: recorder running; if our venue is open, broker running with the chosen strategy; heartbeat green.
2. **During** (8 min Sat, 4 min Sun): watch the heartbeat only.
3. **Right after**: read our `bench_efficiency` / `bench_points` and every team's `market` on the leaderboard. Who beat
   the stall, by how much? (Rival board venues: Team 6, 12, 13.)
4. **Within 30 min**: replay the recorded session through `auto_clone`, `v1` and any new variant; calibrate `sim.py` to
   the real traders (shade size, how fast quotes relax, patience, share of firm traders).
5. **Deploy** the best variant only if it beats `auto_clone` on the real replays AND never falls > 1 pp below it.
6. Log the session's numbers and the decision in `intel/market-log.md` (newest first) and report one line to the Chief.

## 5. The venue decision (Lucas: option A or B, plan §4E)
- **A**: open a `board` venue at fee 0 early, running `auto_clone` (floor = the stall) and switching to `v1` when replays
  justify it. Risk: broker downtime → 0 for that session. Cost: 270 P (250 back later).
- **B**: stay on the free stall (half points) until replays prove an edge, then open between sessions.
- Either way: if Sunday's two benches (each half of round 3's bench score) can be won, the venue must be open, tested
  and supervised before Sunday 10:00.

## 6. Hypotheses to test (cheapest first)
| # | Hypothesis | Test | Decides |
|---|---|---|---|
| M1 | The stall's efficiency is ~0.90-0.95 | First bench: our `bench_efficiency` on the stall | How much room exists above it |
| M2 | Rival board brokers beat the stall | Leaderboard `market` of Teams 6/12/13 vs stall teams | Whether the top-3 mean sits above the stall |
| M3 | Impatient traders leave unmatched under greedy matching | Replays: who leaves unmatched under auto_clone | Whether v1's rule helps |
| M4 | We can record the bench on the stall | Recorder output at the first bench | Whether replays need a venue of our own |
| M5 | The hard bench (16.0) punishes greedy matching more | Replay the hard session | Strategy for 16.0 and Sunday |
| M6 | A 0-fee venue attracts other teams' trades | Dani steers page-completion trades between two other teams to our venue | "Value created on our venue" |

## 7. Escalate to the Chief (never wait for Lucas)
Broker down during a session · a session scored below the stall · a variant beats the stall by ≥ 2 pp on replays (to
open the venue) · anything that needs cash.
