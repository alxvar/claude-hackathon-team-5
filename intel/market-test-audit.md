# Market Test and real trades: independent audit (Sun 00:40, read-only)

Sources: `bazaar-kit/RULES.md`, `bazaar-kit/starter_broker.py`, `~/Downloads/The Bazaar - Payday.pdf` (slide 5, read as an
image), `data/leaderboard.jsonl` (snapshots 90-1440), `data/bench/results.jsonl` + `bench-h*.jsonl`, `data/me.jsonl`,
`data/feed.jsonl` (`bench.started`, `venue.*`), `broker/` (replay + sim, run offline). No keyed calls.
Labels: **[V]** read or fitted exactly · **[L]** fits the data, alternatives not fully excluded · **[?]** open.
Scripts (scratchpad, not in the repo): `rt.py` (market decomposition), `ev2.py` (broker EV in the sim).

## 0. The headline: the 21:10 directive has the deck backwards [V]

Payday deck, slide 5 ("THE SCOREBOARD"), read as an image: the blue box says **22.5 · ① Market Test**, the orange box
says **7.5 · ② Real trades**. `intel/directives.md` 21:10 wrote "Market Test 7.5 + REAL TRADES 22.5", and that error
spread to `strategy.md:15-18`, `judge.md:11`, `market-sunday.md` §1/§4, `sunday-plan.md:10`, `market-log.md` 21:15 and
`team/lucas.md` 21:15. (The text extraction of that slide jumbles the numbers, which is probably how it happened.)

The data say the same as the slide, independently:
- Stall teams sit at 7.5 board. With Friday's market = 0 at weight ½, board = Saturday × 2/3, so the stall is
  **11.25 Saturday points = half of 22.5**. The server's own `bench_points` reads **0.5** after every session.
- The real-trades gap tops out at **+5.0 board = 7.5 Saturday points = the full 7.5**.

So: **the stall is at half the Market Test, not at its maximum**, and **+5.0 is already the full real-trades
score**. There is no hidden 22.5 to unlock on v10.

## 1. How the Market Test is scored

**Per session k** [V rules text + server fields; L for the shape below the stall]:
- efficiency e = gains realised between the traders' true limits / possible gains (`bench_efficiency`; our stall
  0.899 · 0.933 · 0.878 · 0.891 · 0.886 · 0.854).
- bench points: matching the stall = **0.5**; below the stall, continuous (t08 0.494, t06 0.381, t13 0.222 at session 1;
  consistent with 0.5 × e/e_stall, unproven) [L]; above the stall, the rules say "the full points go to the mean of the top three" (never observed, §1c).

**Per round** [L, strong]: a **weighted** mean of the session points, × 22.5. Equal weights are ruled out: t03 scored
0.5 (stall) then its new board venue v20 scored 0 (no working broker, open since tick 269), and t03 showed 3.61 board,
not the 3.75 an equal average gives. Fitting t13 and t03 (no real trades ever, so their market is all bench) gives
session weights **1.00 : 1.07 : 0.86 : 1.04 : 0.93 : 0.81** (anchored on t13 = 0.5 after session 1). The independent
check is t03: with those weights it lands on 0.500 · 0.498 · 0.505 · 0.494 in sessions 3-6, and t06/t08 land on 0.500 ±
0.001 in sessions 2-3. Every team's residual market after the decomposition (§2) is 0.00 ± 0.01 at every snapshot. The weights track session size,
probably each session's possible gains [L]. So **a 12-trader hard session likely weighs more than a 10-trader one** [L].

**To board and final points** [V blend, fitted 11 snapshots by score-model §1]: board = (0.5·Fri + Sat)/1.5 for Market;
final = (0.5·Fri + Sat + Sun)/2.5 → **1 Sunday round point = 0.4 final points.**
- Market Test full value per round: 22.5. Stall: 11.25. **Unclaimed by every team: 11.25 per round.**
- Sunday, if all its sessions beat the stall: +11.25 Sunday points = **+4.5 final**; ≈ **+1.5 final per Sunday session** if
  there are 3 (17.0, 19.0, 21.0 [L]). A dead broker in one session: **−1.5 final** (0 instead of 0.5).

### 1a. Did anyone ever beat the stall? No [V where separable, L for uncapped trading venues]

Per-session bench points (fitted; "≤0.5" = consistent with 0.5, can't exceed it without breaking the cap):

| Team (venue) | s1 3.0 | s2 5.0 | s3 7.0 | s4 9.0 | s5 11.0 | s6 13.0 |
|---|---|---|---|---|---|---|
| t13 (v03→v24, board, own broker) | **0.222** | 0.5 (anchor) | 0.5 (anchor) | 0.5 (anchor) | 0.5 (anchor) | 0.5 (anchor) |
| t06 (v01, board) | **0.381** | 0.50 | 0.50 | 0.50 | ≤0.5 | ≤0.5 |
| t08 (v06, "matched on estimated limits") | **0.494** | 0.50 | 0.50 | ≤0.5 | ≤0.5 | ≤0.5 |
| t03 (stall → v20 board) | 0.5 | **0.0** | 0.50 | 0.50 | 0.50 | 0.49 |
| t12 (v02, board) | ≤0.5 | ≤0.5 | ≤0.5 | 0.5 | 0.5 | **0.38** |
| t10 (v07, board) | 0.5 | ≤0.5 | 0.5 | ≤0.5 | ≤0.5 | ≤0.5 |
| t04 (v05), t01 (v19), t02 (v26) board | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 |

- 51 board-venue sessions, **0 above the stall, 5 clearly below**. Every deviation we can measure was downward (t13,
  t06, t08 at session 1, t03 at 2, t12 at 6). t10 sat at 12.50 with its real-trades part at the cap after sessions 2, 4,
  5 and 6 (a bench above 0.5 would have pushed it past 12.50), and its market didn't move at sessions 1 and 3. The
  highest market anyone ever showed is 12.50.
- Board venues that never deviated (t04, t01, t02) score exactly the stall's 0.5. A board venue = stall + downtime risk.
- **One venue per team** [L]: every `bench.started` lists exactly 18 venues (one per team), and t13 closed each venue
  before opening the next. So a "safe clone + experimental" two-venue hedge is likely impossible.

### 1b. Could a better broker score more on the hard test or later? Only through the untested top-three rule

Offline sim (`broker/replay`, true limits, 1,000 seeds, our strategies vs `auto_clone` = the stall). Two readings of the
rule: **nonlinear** (the best venue above the stall gets the full 1.0, which is what "full points at the mean of the top
three" gives when you're the only one above) vs **linear** (0.5 × e/e_stall on both sides). Δ = change in expected bench
points per session (×9 = final points over a Sunday round):

| Trader model | strategy | wins | losses | Δ nonlinear | Δ linear |
|---|---|---|---|---|---|
| hard-12 (our "firmer, impatient" guess) | v1 | 0.0% | 0.0% | +0.000 | 0.000 |
| hard-12 | v1_literal | 1.7% | 1.8% | +0.008 | −0.000 |
| staggered-20 (calibrated on bench 3.0; stall eff 0.885 ≈ real 0.85-0.93) | v1 | 6.8% | 16.0% | +0.027 | −0.005 |
| staggered-20 | v1_literal | 15.4% | 52.4% | +0.045 | −0.026 |
| staggered-20-firm (stall 0.827) | v1 | 6.9% | 9.3% | +0.030 | −0.002 |
| staggered-20-firm | v1_literal | 15.5% | 43.4% | +0.049 | −0.021 |

- Best case (nonlinear, v1_literal): +0.045 bp per session ≈ **+0.4 final** over Sunday. Linear: ≈ **−0.2 final**.
- Costs not in the table: downtime (t03 lost a whole session; at 5% per session ≈ −0.2 final), and **270 P** (250 P bond
  locked until close + cooldown, 20 P fee). That's the MAL close (+0.6-1.2 final, score-model §3g) or part of CHA.
- The real stall books we recorded are post-engine leftovers: every replay is degenerate (proxy 0 or 1). **We have zero
  real-data evidence for any broker edge**, and every rival deviation from the stall we can measure was a loss (§1a).

### 1c. The hard Market Test (14.65) [L]
- If the clock **resumes** at 13.367, 14.65 and 15.0 are sessions 7-8 of **Saturday's** round. Each is ≈ 1/8 of it, the hard
  one maybe a bit more (12 traders): winning it (nonlinear) ≈ +1.7 Sat points ≈ **+0.7 final**; a dead broker ≈ −0.7 final.
  Replacing v10 in the Saturday tail also risks v10's Saturday real-trades credit (mm +2.2 at the close) [?].
- If the clock **jumps** to 16.65, they may not run; Sunday's sessions start at 17.0.
- The hard-12 sim shows our brokers almost never differ from the stall there (≤ 1.8% of sessions).

## 2. How "real trades" is scored

**Fit [L, strong]:** RT_round = **7.5 × min(1, max(0, VC_i) / M)**, M = mean VC of the **top three venues** in the round;
board = 5.0 × the same after the Friday blend. VC_i = the net value created on venue i between two other teams
(buyer's value − seller's value, summed; the scored number is `mm_points`, not `venue.value_created`: ours read 9.0 vs mm
−5.2 and scored exactly 0).

Decomposition (`rt.py`: market − fitted bench part, every snapshot 220-1440):
- **The top venue is always at the cap exactly**, including the ramp: t12 alone at 3.21 → 4.88 (ticks 220-310) = 5.0 ×
  the blend factor. Relative scoring, the leader always full.
- **Two venues at the cap at once** in 6 windows (t05+t12 320-350, t10+t12 400, t12+t06 600-690, t12+t10 720, t06+t10
  910-1080); **never three**. Fits "top-3 mean" (at most 2 of 3 can sit at or above their own mean).
- Non-trading teams: residual 0.00 ± 0.01 at every snapshot; negatives floor at 0 (us, t12 at 910, t07 at 1210).

**Alternatives tested:**

| Alternative | Verdict | Why |
|---|---|---|
| Real trades out of 22.5 | **Rejected** [V] | Would allow +15 board; max ever +5.00 over 1,200 ticks. The deck says 7.5 anyway |
| Relative to the top venue only | Rejected [L] | Two venues at the cap in 6 separate windows would need exact VC ties |
| Per-day / share-of-day weighting | Rejected [V] | The cap grows only with the blend (3.2 at tick 220 → 5.0 at 321), then stays flat to 1440 |
| Friday blend | **Confirmed** [V] | 5.0 board = 7.5 × 2/3; stall 7.5 = 11.25 × 2/3; same w = (tick − 160)/161 |
| Top-2 mean / top-4+ mean | Top-2 rejected (ties again); top-4 not excluded, never 3 at the cap [L] | — |

Display quirk [L, n=1]: before a round's first bench, market = 30 × the real-trades share (t12 showed 11.49 at tick 210
= 30 Saturday points with only one trade). Early-Sunday snapshots will overstate trading venues until the 17.0 bench.

**Why +5.0 is the ceiling:** +5.0 board IS the full 7.5. Nobody can show more on real trades.

## 3. Recommendations for Sunday

**3a. Keep the free stall v10 for the hard test and all Sunday benches. Don't open a board venue** [L].
The stall gives 0.5 every session, the same as every rival so far. A board venue only pays if (1) the top-three rule
gives full points for any edge, (2) we have ≥ 270 P idle after CHA, and (3) we have a broker with ≥ 15% wins and no
average loss in the staggered sims. Today only (1) is plausible, and it's untested. Expected value is about +0.4 to
−0.4 final before the 270 P, and negative after it.
- One cheap move: ask the desk, "If a single venue beats the stall's efficiency by a hair and nobody else does, does it
  get the full Market Test points for that session?" If yes **and** cash is idle after CHA, revisit with `v1`
  (lowest-risk: −0.002 to −0.005 per session linear, +0.03 nonlinear) for the 19.0/21.0 sessions, opened between sessions.
- Replace market-sunday §4's desk question: the 22.5 is answered by the slide. Keep its second question
  (mm −5.2 vs `value_created` 9.0, and the +2.2 flip at the close).

**3b. Real-trades VC target: net VC ≥ the average of the two best rival venues' VC, at the close** [L].
- Full 7.5 Sunday points (**= 3.0 final**) come at VC_us ≥ M; with us in the top three that's VC_us ≥ (R1 + R2)/2.
  Points = 22.5·VC/(VC + R1 + R2) below it. Anything above it earns nothing.
- Saturday's scale was small. Top three at the end ≈ t10 1.39 M, t06 0.94 M, t09 0.68 M with M ≤ ~15 (score-model §3h,
  verifier-checked). So (R1 + R2)/2 ≤ ~17 VC units; at 320-350 one MAL-07 trade capped us.
- **Sunday target: ≈ 40-50 net VC by the close** (Saturday × 2-3 for 15 s ticks, +150 P and a field that now
  knows markets count), front-loaded, **zero negative trades** (a negative subtracts at the same rate; the net floors at 0).
  `market-sunday.md`'s "170 at the close" assumes a rival top-three mean of 59-213 (its §1 table), which the ≤ 15
  Saturday bound contradicts. It overstates the target 3-4× [L].
- Value per unit: at R1 + R2 ≈ 80, the first 20 VC ≈ +4.5 Sunday pts (+1.8 final), 40 caps it. One good page finisher
  (RET-09 t07 → t09, matchmaker low estimate +68) could cap v10 on its own if the estimate is in the same units [?].
- Trades on rival venues raise their VC and M: keep routing club and swap deals to v10.

**3c. Re-weight the Sunday plan.** v10 is worth up to **3.0 final**, not "the biggest lever" sized off 22.5. It's
still free (0 P), so keep it, but it doesn't outrank CHA (+3.2-5.6 final for ≈ 330 P). Duels III + Final (up to 4.8)
and the Market Test bench (par at the stall) are unchanged.

## 4. Open questions [?]
- Above-stall payoff (§1b): the only unknown that could make a board venue worth it.
- What `mm_points` subtracts (9.0 − 14.2 = −5.2 all day, then +2.2 at the close with no new trade), and whether
  real-trades VC resets per round (neg/ladder did at tick 160).
- Session weights = possible gains? (fits, unproven); number of Sunday benches (17.0 listed; 19.0/21.0 assumed).
