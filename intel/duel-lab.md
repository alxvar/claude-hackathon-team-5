# Duel Lab: Duels II recommendations (Sat 16:00, for Aleks's decision; analysis only)

_Lucas's Duel Lab session. It never writes to the game or to `agents/duelist/`. Inputs: our 68 records in `docs/duels/`
(Duels I = session 2, the practice round = session 1), `docs/duels/scores.jsonl`, `docs/duels-1-review.md`,
`intel/score-model.md` §1d-1e, the organisers' Duels deck, and the merged duelist (4699673). Code and raw outputs are in
the session scratchpad (`lab/`: `sim.py`, `validate.out`, `final.out`, `search3.out`, `replay.out`, `fit.out`,
`days_sim.py`, `days.md`, `r1m_out.txt`); the numbers below are copied
from them. Labels: [V] measured on our records or code, [L] modelled or inferred, [?] unknown._

## Bottom line

- **One change wins in every model: cap each mid-duel concession at about 18% of the gap.**
  - **Where:** `agent.held`, the same place as `MIN_STEP_SHARE`.
  - **Gain:** +0.9 to +4.0 duel points over Duels II's 68 duels, depending on which calibrated model of the rivals is
    right. Our merged plan's baseline is about 20-25 points.
- **Days:** keep Aleks's rule, with three tweaks:
  - never pre-pay to keep our day;
  - switch to their day late rather than let a day standoff kill the deal;
  - when they open on a middle day, propose our own corner.
- **Leave alone:** the opener and the accept rules. Exact replays and the model both confirm Aleks's calls there.
- **Our yardstick was wrong [V].** Duel points measure **share of the pie**, not primas. Every replay so far summed P,
  and that overweights the big-pie duels.

## 1. Two facts the rest stands on

**Duel points = share × (1 − d)^rounds per duel, not P [V].**
- Our `duel_points` (`scores.jsonl`) jump each time a deal closes, and each jump matches that deal's share of the pie.
- 2585 made 60.2 P and moved us +0.72; 2319 made 3.4 P and moved us +0.34.
- So a 10 P pie counts as much as an 80 P one. Every "−43 P / −83 P / +261 P" replay in `docs/duels-1-review.md` and
  score-model §1d weighs duels by size.
- Re-scored in share:
  - **Anchor closer** (opener at 75% of the distance, rounds held fixed): −0.47 share-points over the 20 deals with a
    known pie, about 5%. It was "−30 P", and is smaller in share. No P-based verdict flips.
  - **Accept the rival's first in-limit offer:** −2.94 share-points (9.06 → 6.12, −32%). Haggling paid even more than
    the P replay said.

**The rival's limit can be read for 20 of our 30 Duels I deals [V].**
- Our 26 score samples make 25 intervals; 20 of them hold exactly one closed deal of ours. For each, pie = result ÷
  jump.
- All 20 shares come out ≤ 1 when the jump is matched to the feed's `duel.closed` tick. Matching one tick later gives a
  share of 1.05 and a pie of 302, so that reading is wrong.
- Pies run 10-84 P, median 0.26 × our limit. Our opener sits at 1.5 pies on median: it asks for more than the whole pie,
  as theirs do.

## 2. The rival-response model (fitted on Duels I)

| What | Duels I evidence | In the simulator |
|---|---|---|
| Opener | Rivals ask on median 1.4× the pie (beyond our limit); 4 of 18 open inside our limit ("We can do N P. Thank you for the talk.") [V] | Rival demand drawn from the 18 observed openers |
| Concession | Two kinds [V transcripts, L classification]. **Fast, then hold** near a "fair" point: 2296/97, 2430/31, 2357, 2506. **Clockwork**: 1-15 P every tick, whatever we do: 2318/19, 2460/61, 2522, 2534/35, 2540/41, 2356 | A mix of fast (35-65% of the distance per move) and slow (2-8%) rivals, plus a "two moves then hold" type |
| Reaction to us | Weak. Their step ≈ 0.24 × ours + 0.06 × gap + 1.4 (Aleks, R² 0.11) [V]. Our opener barely changes their total concession: corr 0.13, n 23 [V] | + 0.24 × our last step |
| Acceptance | They take our offer when it leaves them about 0.2-0.45 of the pie [L, from these points]. Accepted at a rival share of 0.06-0.42; refused at 0.0-0.35 (2534 refused 0.12, 0.18, 0.23, then took 0.27). Laxer near the deadline: 2494 took 0.06 with 3 ticks left, 2495 took 0.19 at the deadline | Threshold τ drawn mid-duel, a lower τ in the last 3 ticks |
| Talk | Silent, no deal: 3 of 34 (Team 11 + 2523). At most one message, then accept-only: about 6 of 34 (2314/15, 2472/73, 2446, 2495). The rest message most ticks [V] | The same mix |
| Teams | Rivals come in pairs with the same template; each team plays us 4 times in Duels II. Rival book in the appendix [L] | — |

**Validation [V data / L sim].** No single parameter set fits every statistic, so I bracket with four calibrated worlds:

| | Duels I actual | W1 base | W2 fast/slow mix | W3 tough accept | W4 lumpy steps |
|---|---|---|---|---|---|
| Deal rate | 0.88 | 0.90 | 0.90 | 0.90 | 0.90 |
| Rounds per deal | 4.4 | 4.28 | 4.20 | 4.45 | 4.08 |
| Deals in ≤ 1 round / ≥ 7 rounds | 0.30 / 0.27 | 0.29 / 0.24 | 0.25 / 0.23 | 0.21 / 0.25 | 0.22 / 0.18 |
| Points per duel (share × decay) | 0.41 | 0.394 | 0.374 | 0.319 | 0.310 |
| Deals closed on our accept | ≈ 0.4 | 0.13 | 0.22 | 0.31 | 0.19 |
| Out-of-sample: "accept first in-limit" ÷ actual | 0.65 | 0.87 | 0.79 | 0.75 | 0.79 |
| Deals closing ≥ 75% of our opener's distance | 0.17 | 0.17 | 0.11 | 0.05 | 0.04 |

- **Where it fits:** deal rate, rounds and points per duel are fitted, not predictions.
- **Known bias:** the model's rivals make too few thin early in-limit offers. So it **undervalues haggling**: every world
  puts "accept first" above the real 0.65.
- **Consequence:** I trust it on step size and hold timing, which gain both share and rounds. I don't trust it where a
  change only trades share for rounds, like the opener.

## 3. Policy search at d = 8% (16 ticks)

- **Baseline:** the merged plan: 3 P floor, `MIN_STEP_SHARE` 0.05, no offer budget, `HOLD_TICKS` 3, silent walk to 30%,
  accept by 2 ticks left, small-gap closer. Our step size is the Duels I fit: 3.1 + 0.21 × their step + 0.025 × gap,
  with noise.
- **Method:** 20,000 duels per cell, paired (same duels, same rivals), 95% CI.
- **Units:** Δ is in duel points over 68 duels. Baseline level per world: 25.3 / 24.2 / 20.8 / 20.3.

| Change (where) | W1 | W2 | W3 | W4 | Verdict |
|---|---|---|---|---|---|
| **1a. Cap a mid-duel concession at 18% of the gap** (`held`: cut a bigger step back to 18%; closing ticks exempt) | **+0.93** [0.85, 1.01] | **+1.92** | **+2.36** | **+3.95** | **Ship** [L] |
| 1b. 1a + `MIN_STEP_SHARE` 0.05 → 0.10 | +0.95 | +2.19 | +2.78 | +4.41 | Optional: it holds the small steps that drew 5.5 P back in Duels I |
| 1d. Every mid-duel concession = 15% of the gap (code sets the step) | +1.82 | +2.40 | +2.66 | +3.93 | Best on average; a bigger change |
| 2. `HOLD_TICKS` 3 → 5 (`runner.py`) | +0.02 (n.s.) | +0.36 | +0.53 | +0.84 | Cheap; standoff risk [L] |
| 3. `SILENT_KEEP` 0.3 → 0.15 (silent walk goes further) | +0.20 | +0.16 | +0.17 | +0.08 | Small but never negative |
| 4. Opener ×0.9 | +0.74 | +0.38 | +0.16 | **−0.19** | **Don't** (Aleks's call stands) |
| 1c + 2 + 3 (1c = 1a with small steps raised to 12%) | +1.54 | +2.32 | +2.68 | +4.02 | |
| 1a + 2 + 3 | +0.94 | +2.11 | +2.72 | +4.22 | |

All CIs are ±0.1-0.15 points. Cells without one are significant unless marked n.s. (`final.out`).

### Why the cap wins [L, with data support]
- **The steps really are lumpy [V].** Mid-duel (more than 3 ticks left), our LLM conceded a median 16% of the gap;
  27% of its steps were a quarter of the gap or more, up to 67%.
- **Big steps gave value away [V].** In Aleks's own buckets, steps of a quarter of the gap or more drew 4.8 P back for
  7.5 P given.
- **What the cap does:** it gives up less per round. The model finds both share (+2 to +9 points) and rounds go the
  right way: share +0.02 to +0.09. The gain is biggest where steps are lumpiest (W4), and that's the world whose steps
  match the data's spread.
- **It leaves the haggling alone:** small steps and the number of offers don't change.

### Confirmed: leave these alone
- **Accept rules: no early-accept rule [V, exact replay].** Replayed on the real transcripts of the 20 deals with a
  known pie, in share units. The rule only stops earlier, so no rival model is needed. Against our actual 9.06:
  - accept-first: 6.12;
  - break-even (rival step < S·d/(1−d)): 8.38;
  - "rival held once in-limit": 8.38;
  - "held twice": 8.88;
  - "their offer ≥ 0.7 × ours": 9.13 (+0.07, noise).
- **Opener [L/?].** Not robust in the model (+0.74 to −0.19). The replay says −5% with rounds held fixed. Keep it.
- **Deadline accepts.** Accepting at 1 tick left instead of 2 would add +0.4-0.5. It isn't worth the risk of a missed
  settle.

## 4. Delivery days (modelled only: no days duel has been played) [L/?]

Sub-model in `days_sim.py` / `days.md`:
- **Money split:** Duels I shares and rounds.
- **Day weights:** linear, |w| 0.5-5 P/day, sign random, so about half the duels conflict.
- **Rival day types:** follower, price-for-day, integrative, soft-stubborn, hard-stubborn.
- **Scoring, both readings:** H1 = our gain ÷ best pie over the days; H2 = our gain ÷ pie at the agreed day. Which one
  the server uses is unknown [?].

**Recommendation: the merged rule with three changes.**
1. **Hold our day without pre-paying** (drop "pay up to C/2 to keep it"). An aware rival's price already charges for its
   lost day. Never negative in the model: +0.018/duel if anchors stick, 0 if not.
2. **Late switch.** If the day is still open with about 4 ticks left, offer their day at +C, a worth-neutral price, so a
   day standoff never costs the deal. Worth +0.013 to +0.025/duel against rivals that never move days; 0 against
   followers.
3. **A middle-day opener (1-9) says nothing about their side.** Answer with our own corner (call = hold). Don't give the
   far corner (the merged `day_read` sets `give_day = 10 − dv.best`), and never take the middle day.

- **Against the merged code (R1m = `day_read` as merged in 4699673): R1m + the three changes = +0.017 ± 0.001/duel (H1)
  / +0.018 (H2), about +1.2 duel points over 68.** If rivals open at day 5: +0.045 (H1) / +0.027 (H2), up to +3.1.
- **Where the gain comes from (H1):**
  - main mix: no pre-pay +0.015, late switch +0.002, middle-day fix 0 (no middle openers in that mix);
  - rivals opening at day 5: no pre-pay +0.017, late switch +0.007, middle-day fix +0.021.
- **The middle-day fix is the one gain that survives** if anchors don't stick (κ = 0). The far-corner gift is the weak
  branch: half the time that corner is both sides' worst day.
- **The merged thresholds already beat the review's R1** in the model (0.310 vs 0.298 per duel).
- **R9 vs holding our own day (the old default):** +0.032/duel, about +2.2 points.
- **Also robust:**
  - never settle a middle day (worst rule nearly everywhere);
  - wait ≤ 2 ticks to see their day first: +0.013/duel, but the model doesn't charge the ticks;
  - keep the give threshold (|w| ≤ 1.5 or C ≤ 15);
  - asking C + C or just C is a wash.

## 5. Top changes for Aleks (ranked)

| # | Change | Expected Δ, 68 duels | Evidence | Risk |
|---|---|---|---|---|
| 1 | **`MAX_STEP_SHARE = 0.18`** in `agent.held`: a mid-duel concession above 18% of the gap (in worth) is cut back to 18% of the gap, not held; closing ticks and day swaps exempt. **The capped move must carry a code-written text** ("I can do N P.", as the silent walk does): the negotiator's draft names its own, bigger number | **+0.9 to +4.0** (CI ±0.1 each) | [L] 4 worlds; [V] our lumpy steps, Aleks's ≥ 25% bucket | Rivals that answer big steps with big steps. In an earlier model version, fixed 15% steps at 2.5× the fitted reaction still gained +1.65 |
| 2 | **Days, on top of the merged rule:** no pre-pay; late switch at ~4 ticks left; middle-day opener → our corner | **≈ +1.2** (up to +3.1 if rivals open mid) | [L] modelled only; H1/H2 [?] | Rival day behaviour invented. Gate: first-wave `pred` = `points` |
| 3 | **`HOLD_TICKS` 3 → 5** | 0 to +0.8 | [L] | More standoffs: the model's deal rate is unchanged (0.900 vs 0.899), but standoffs are exactly what 103/104 were |
| 4 | **`SILENT_KEEP` 0.3 → 0.15** | +0.1 to +0.2 | [L] | ~0: share near our limit is small |
| 5 | **Desk question: are duel accepts limited per duel or per team per tick?** | Accepting all code accepts 1 tick earlier costs 0.5-0.8 | [?] `/api/clock` lists only the trading limit (1 per team per tick); the deck says duel limits are separate | If per duel, `runner.closer`'s line-up (one accept per tick across 6 duels) forces needless early accepts |

**Not changing:** the opener, the accept rules, no offer budget, the 3 P floor.

**Optional (Aleks's §3.5 stretch):** give the strategist the appendix's rival book as facts when a first message
matches a template. This is untested in the model.

**How to read Δ.** Duels I gave us 13.93 duel points over 34 duels. The Analyst's §1b mapping (duel part ≤ 12 Saturday
points = 8 board) suggests about 0.4 board per duel point, if Duels II feeds the same part [?].

## 6. Risks and first-wave checks

- **Model risk [L].**
  - Rivals are fitted on 34 duels; their bots may change.
  - The cap's gain rests on the step-reaction fit (R² 0.11).
  - In all four worlds the cap is positive with tight CIs. Its size is uncertain, its sign much less so.
- **Days scoring [?].** At the first deals of wave 1, check `pred` = `points` with the day value in. If it misses, read
  the jump: our gain ÷ best pie (H1) or ÷ pie at the agreed day (H2).
- **Day reading [V for code, ? for payload].** `days.py` has never seen the real `your_days_weight`. If it prints
  `CAN'T READ`, every day rule falls back to the models.
- **Live stats to watch per wave** (`agents.duelist review`):
  - rounds per deal: model 3.5-3.9 with the cap, vs 4.4 in Duels I;
  - share of deals ≥ 7 rounds;
  - concessions over 18% of the gap: there should be none outside the closing ticks.

## Appendix: rival book (Duels I templates; each team plays us 4× in Duels II) [V transcripts, L types]

| Duels | Template (first message) | Type | What happened |
|---|---|---|---|
| 2296/2297 | "Thank you for meeting me. I can do N P." | Fast, then holds near the middle | We took theirs at shares .52/.54 after 4-6 rounds. In 2296 they offered 101 (share .73) at round 3, then slid back to 97 |
| 2318/2319 | "I can do N. That is a fair deal for both of us." | Clockwork, accelerating +3..+15/tick | Accepted our offer at rival share .21/.40 after 9 rounds. Our messages only added rounds |
| 2356/2357 | "Propuesta justa para cerrar pronto…" (rotating Spanish lines) | Slow shrinking steps every tick | Took our 117 (rival .42); we took their 78 |
| 2366/2367 | "67?" / "101?" | Never moves | 2366 took our 110; 2367 no deal (never inside our limit) |
| 2430/2431 | "N for [item]. Every round costs us both…" | Two ~11 P steps, then a silent hold | Refused our offers even at a rival share ≈ 0.6; we took their number at the deadline (.20/.24) |
| 2460/2461 | "Happy to close quickly at N…" / "A real step from me" | Steady 2-9 P every tick | 10-12 rounds; they took ours |
| 2472/2473 | "N P y cerramos ahora." | One message, then accept-only | Took our walk late, 1 round |
| 2506/2507 | "Propongo este precio, creo que es justo para los dos." | 9-12 P bursts every ~3 ticks | 6-7 rounds |
| 2540/2541 | "Hello! I can do N. Thank you for your time." | Shrinking steps every tick | Met our number (our share .87 in 2541) |
| 2584/2585 | "We can do N P. Thank you for the talk." | Generous opener inside our limit | Took our opener (2584) |
| singles | 2522 "Let's close it quickly" (1-2 P/tick) · 2534 "Puedo llegar a N primas" (took ours at .27) · 2535 "Es una pieza que merece su precio" (repeater, took ours at .24) · 2530 "Hi there. N P from my side." (we took 97: our share **.16** of a 63 P pie, the biggest leak) · 2446/2495 silent accept-only · 2414/2415/2523 silent, no deal | | |
