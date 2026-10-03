# Duel Lab: Duels II recommendations (Sat 16:15, for Aleks's decision; analysis only)

_Lucas's Duel Lab session. It never writes to the game or to `agents/duelist/`._
- _**Inputs:** our 68 records in `docs/duels/` (Duels I = session 2, the practice round = session 1),
  `docs/duels/scores.jsonl`, `docs/duels-1-review.md`, `intel/score-model.md` §1d-1e, the organisers' Duels deck, and
  the merged duelist (4699673)._
- _**Sources:** code and raw outputs are in the session scratchpad (`lab/`: `sim.py`, `validate.out`, `final.out`,
  `search3.out`, `extra.out`, `replay.out`, `fit.out`, `build.out`, `days_sim.py`, `days.md`, `r1m_out.txt`). Every
  number below is copied from them._
- _**Checked:** an independent verifier pass audited this file against those sources. Its 2 high and 14 low flags are
  fixed below._
- _**Labels:** [V] measured on our records or code, [L] modelled or inferred, [?] unknown._

## Bottom line

- **Step size is the lever. Cap each mid-duel concession at about 18% of the gap, or better, make it about 15%.**
  - Every step-size variant gains in all four calibrated versions of the rival model ("worlds"):
    - a cap alone: +0.9 to +4.0 duel points over Duels II's 68 duels;
    - a fixed 15% step: +1.8 to +3.9.
  - The merged plan's baseline is about 20-25 points.
  - The four worlds are parameter sets of **one** simulator, so they share its structure.
- **Days:** keep the merged rule and add three tweaks:
  - never pre-pay to keep our day;
  - switch to their day late rather than let a day standoff kill the deal;
  - when they open on a middle day, propose our own corner.
  - Modelled gain: about +1.2 points, up to +3.1 if rivals open mid.
- **Leave alone:**
  - **Accept rules:** an exact replay on the real transcripts confirms Aleks's call [V].
  - **Opener:** keep it. The model leans slightly to lowering it (+0.7 to −0.2, 3 of 4 worlds positive), but its known
    bias favours closing fast, and the replay says lowering it costs about 5%.
- **Score in share, not primas [V].** Duel points are not proportional to P. Every replay so far summed P, and that
  overweights the big-pie duels.

## 1. Two facts the rest stands on

**Duel points are not proportional to P [V]; they fit share × (1 − d)^rounds per deal [L].**
- Our `duel_points` (`scores.jsonl`) jump each time a deal closes.
- Over 6 single-deal intervals the jump per primas earned ranges 8× (0.012-0.100):
  - 2585 made 60.2 P and moved us +0.72;
  - 2319 made 3.4 P and moved us +0.34.
- Each jump fits that deal's share of the gap between the two limits (as Aleks inferred). The pie itself is solved from
  the jumps, so that reading is [L].
- **Consequence:** a 10 P pie counts as much as an 80 P one. The P-weighted replays in `docs/duels-1-review.md` and
  score-model §1d weigh duels by size.
- Re-scored in share (`extra.out`, `replay.out`). **No verdict flips**; the sizes change:
  - **Anchor closer** (opener at 75% of the distance, rounds held fixed), on the 20 deals with a known pie:
    −0.47 share-points (−5.2%). In P on the same deals: −30 P. Aleks's −43 P is over all deals.
  - **Accept the rival's first in-limit offer:** 9.06 → 6.12 share-points (−32%). Aleks's P replay gave −28%, the
    Analyst's −55%. Haggling paid.

**The rival's limit can be estimated for 20 of our 30 Duels I deals [L].**
- Our 26 score samples make 25 intervals; 20 of them hold exactly one closed deal of ours. For each, pie = result ÷ jump.
- All 20 implied shares are ≤ 1 when the jump is matched to the feed's `duel.closed` tick. Matching one tick later
  gives a share of 1.05 and a pie of 302, so that reading is wrong.
- Pies run 10-84 P, median 0.26 × our limit. Our opener sits at 1.5 pies on median: it asks for more than the whole pie,
  as theirs do.

## 2. The rival-response model (fitted on Duels I)

| What | Duels I evidence | In the simulator |
|---|---|---|
| Opener | Rivals ask on median 1.4× the (inferred) pie, beyond our limit; 4 of 18 open inside it ("We can do N P. Thank you for the talk.") [L] | Rival demand drawn from the 18 observed openers |
| Concession | [V transcripts, L types]. **Fast, then hold:** 2296/97, 2430/31. **Slow every tick:** 2318/19, 2356/57, 2460/61, 2522, 2534, 2540/41. **Bursts:** 2506/07. **Repeaters:** 2366/67, 2535 | A mix of fast (35-65% of the distance per move) and slow (2-8%) rivals, plus a "two moves then hold" type |
| Reaction to us | Weak. Their step ≈ 0.24 × ours + 0.06 × gap + 1.4 (Aleks, R² 0.11) [V]. Our opener barely changes their total concession: corr 0.13, n 23 (`extra.out`) [V] | + 0.24 × our last step |
| Acceptance | Took our offer at a rival share of 0.06-0.42 [V]. Refused 0.0-0.35, except the 2430 holder, which refused about 0.46 and 0.61. 2534 refused 0.12, 0.18 and 0.23, then took 0.27. Laxer near the deadline: 2494 took 0.06 near the end, 2495 took 0.19 at the deadline | Threshold τ drawn per rival, lower in the last 3 ticks |
| Talk | Silent, no deal: 3 of 34 (Team 11 + 2523). At most one message, then accept-only: about 6 of 34 (2314/15, 2472/73, 2446, 2495). The rest message most ticks [V] | The same mix |
| Teams | Rivals come in pairs with the same template; each team plays us 4 times in Duels II. Rival book in the appendix [L] | — |

**Validation.** No single parameter set fits every statistic, so I bracket with four worlds (`validate.out`):

| | Duels I actual | W1 base | W2 fast/slow mix | W3 tough accept | W4 lumpy steps + tough accept |
|---|---|---|---|---|---|
| Deal rate | 0.88 | 0.90 | 0.90 | 0.90 | 0.90 |
| Rounds per deal | 4.4 | 4.28 | 4.20 | 4.45 | 4.08 |
| Deals in ≤ 1 round / ≥ 7 rounds | 0.30 / 0.27 | 0.29 / 0.24 | 0.25 / 0.23 | 0.21 / 0.25 | 0.22 / 0.18 |
| Points per duel (share × decay) | 0.41 | 0.394 | 0.374 | 0.319 | 0.310 |
| Deals closed on our accept | ≈ 0.4 | 0.13 | 0.22 | 0.31 | 0.19 |
| Out-of-sample: "accept first in-limit" ÷ actual | 0.68 | 0.87 | 0.79 | 0.75 | 0.79 |
| Deals closing ≥ 75% of our opener's distance | 0.17 | 0.17 | 0.11 | 0.05 | 0.04 |
| Our mid-duel step ÷ gap: median / q75 / share ≥ ¼ | 0.16 / 0.27 / 0.27 | 0.11 / 0.18 / 0.14 | 0.14 / 0.24 / 0.23 | 0.15 / 0.27 / 0.28 | 0.17 / 0.32 / 0.34 |

How well each world fits:
- **W1** fits the outcomes (deal rate, rounds, points per duel), but its steps are smoother than ours.
- **W3** best matches our real step spread. W4 is lumpier than the data.
- **W2-W4** trade outcome fit for the out-of-sample target and score too low (0.31-0.37 vs 0.41).
- **Every world misses out of sample** (0.75-0.87 vs 0.68): the model's rivals make too few thin early in-limit offers,
  so it undervalues haggling.

What I trust it for:
- **Yes:** comparing step sizes and hold timing. Those change share, mostly upward.
- **No:** changes that only trade share for rounds, like the opener.
- **Its simplifications:**
  - price-only (no days);
  - in the last 3 ticks it concedes 50% of the gap mechanically;
  - `HOLD_TICKS` forces a step there, where the code asks the model again.

## 3. Policy search at d = 8% (16 ticks)

- **Baseline:** the merged plan, as `default_policy` with the 3 P floor and `MIN_STEP_SHARE` 0.05. No offer budget,
  `HOLD_TICKS` 3, silent walk to 30%, accept by 2 ticks left, small-gap closer.
- **Our step size:** the Duels I fit, 3.1 + 0.21 × their step + 0.025 × gap, with noise.
- **Method:** 20,000 duels per cell, paired (same duels, same rivals). 95% CIs are ±0.05 to ±0.15 points.
- **Units:** Δ is in duel points over 68 duels. Baseline level per world: 25.3 / 24.2 / 20.8 / 20.3 (`final.out`).

| Change (where) | W1 | W2 | W3 | W4 | Average |
|---|---|---|---|---|---|
| **1d. Every mid-duel concession = 15% of the gap** (code sets the size: small steps raised, big ones cut; 3 P floor still holds) | **+1.82** | **+2.40** | **+2.66** | **+3.93** | **+2.70** |
| 1c. Clamp to 12-18% of the gap | +1.67 | +2.20 | +2.37 | +3.67 | +2.48 |
| **1a. Cap at 18%:** a bigger concession is cut back to 18% of the gap, then the existing floor check runs (held if under max(3 P, 5% of the gap), so under a ~17 P gap a capped step is held) | **+0.93** | **+1.92** | **+2.36** | **+3.95** | **+2.29** |
| 1b. 1a + `MIN_STEP_SHARE` 0.05 → 0.10 | +0.95 | +2.19 | +2.78 | +4.41 | +2.58 |
| 2. `HOLD_TICKS` 3 → 5 (`runner.py`) | +0.02 (n.s.) | +0.36 | +0.53 | +0.84 | +0.44 |
| 3. `SILENT_KEEP` 0.3 → 0.15 (silent walk goes further) | +0.20 | +0.16 | +0.17 | +0.08 | +0.15 |
| 4. Opener ×0.9 | +0.74 | +0.38 | +0.16 | −0.19 | +0.27 |
| 1c + 2 + 3 | +1.54 | +2.32 | +2.68 | +4.02 | |
| 1a + 2 + 3 | +0.94 | +2.11 | +2.72 | +4.22 | |

**Why step size wins [L, with data support].**
- **Our LLM's steps are lumpy [V].** Mid-duel (more than 3 ticks left) it conceded a median 16% of the gap; 27% of its
  steps were a quarter of the gap or more, up to 67%.
- **Big steps gave value away [V].** In Aleks's buckets, steps of a quarter of the gap or more drew 4.8 P back for
  7.5 P given.
- **What the model shows.** Capping or fixing the step raises our share of the pie in every world (+0.02 to +0.09).
  Rounds fall in W1-W3 and rise slightly in W4 (3.69 → 3.86).
- **It survives a stronger rival reaction.** With rivals answering at 2.5× the fitted reaction (ρ 0.6, `extra.out`):
  - cap: +0.91 / +1.80 / +2.20 / +3.78;
  - fixed 15%: +1.72 / +2.28 / +2.50 / +3.79.
- **1d vs 1a.** 1d beats 1a in W1-W3. 1d also raises small steps, and Aleks's buckets say small steps at large gaps
  drew 5.5 P back for 3.8. So 1a is the cautious version: it leaves small steps alone.

**Leave these alone.**
- **Accept rules: no early-accept rule [V, exact replay].** Replayed on the real transcripts of the 20 deals with a
  known pie, in share units. The rule only stops earlier, so no rival model is needed. Against our actual 9.06:
  - accept-first: 6.12;
  - break-even (rival step < S·d/(1−d)): 8.38;
  - "rival held once in-limit": 8.38;
  - "held twice": 8.88;
  - "their offer ≥ 0.7 × ours": 9.13 (+0.07, noise).
- **Deadline accepts.** In the earlier 3-world search (`search3.out`), accepting at 1 tick left instead of 2 adds only
  +0.4-0.5. It isn't worth risking a missed settle.

## 4. Delivery days (modelled only: no days duel has been played) [L/?]

Sub-model (`days_sim.py`, `days.md`, `r1m_out.txt`):
- **Money split:** Duels I shares and rounds.
- **Day weights:** linear, |w| 0.5-5 P/day, sign random, so about half the duels conflict.
- **Rival day types:** follower, price-for-day, integrative, soft-stubborn, hard-stubborn.
- **Scoring, both readings:** H1 = our gain ÷ best pie over the days; H2 = our gain ÷ pie at the agreed day. Which one
  the server uses is unknown [?].
- **Baseline:** R1m = the merged `day_read` (4699673).

**Recommendation: the merged rule with three changes.**
1. **Hold our day without pre-paying** (drop "pay up to C/2 to keep it" from the strategist guide). An aware rival's
   price already charges for its lost day. Worth +0.015/duel against R1m; 0 if anchors don't stick (κ = 0).
2. **Late switch.** If the day is still open with about 4 ticks left, offer their day at +C (worth-neutral) so a day
   standoff never costs the deal. Worth +0.002 in the main mix, +0.007/+0.010 (H1/H2) against rivals that never move
   their day.
3. **A middle-day opener (1-9) says nothing about their side.** Answer with our own corner (call = hold) instead of the
   merged `give_day = 10 − dv.best` (the far corner). That corner is both sides' worst day half the time. Worth +0.021
   (H1) / +0.001 (H2) when rivals open at day 5; it is the largest gain that survives κ = 0, where the late switch is
   also +0.009.

**Total against R1m:**
- main mix: +0.017 ± 0.001/duel (H1) / +0.018 (H2), about **+1.2 duel points over 68**;
- rivals opening at day 5: +0.045 (H1) / +0.027 (H2), up to +3.1 points.

**Also robust in the sub-model:**
- never settle a middle day (worst rule nearly everywhere);
- wait ≤ 2 ticks to see their day first (+0.013/duel, but the model doesn't charge the ticks);
- keep the give threshold;
- asking C + C or just C is a wash;
- the merged ranking thresholds already beat the review's R1 (0.310 vs 0.298 per duel).

## 5. Top changes for Aleks (ranked)

| # | Change | Expected Δ, 68 duels | Evidence | Risk |
|---|---|---|---|---|
| 1 | **Step size in `agent.held`.** Preferred: every mid-duel concession = **15% of the gap** in worth (1d). Cautious, two constants: new `MAX_STEP_SHARE = 0.18` cuts a bigger step back to 18% (1a), and the existing floor check then runs unchanged. Closing ticks and worth-neutral day swaps exempt. **A resized move must carry a code-written text** ("I can do N P.", as the silent walk does): the negotiator's draft names its own number | 1d: +1.8 to +3.9 · 1a: +0.9 to +4.0 (CIs ±0.1-0.15) | [L] 4 worlds + ρ 0.6 check; [V] our lumpy steps, Aleks's ≥ ¼ bucket | Model structure: all worlds share it. 1d enlarges the small steps that Aleks's data says paid |
| 2 | **Days, on top of the merged rule:** no pre-pay; late switch at ~4 ticks left; middle-day opener → our corner | ≈ +1.2 (up to +3.1 if rivals open mid) | [L] modelled only; H1/H2 [?] | Rival day behaviour invented. Gate: first-wave `pred` = `points` |
| 3 | **`HOLD_TICKS` 3 → 5** | 0 to +0.8 | [L] | More standoffs: the model's deal rate is unchanged (0.900 vs 0.899), but 103/104 were standoffs |
| 4 | **`SILENT_KEEP` 0.3 → 0.15** | +0.1 to +0.2 | [L] positive in all 4 worlds | Small either way |
| 5 | **Desk question: are duel accepts limited per duel or per team per tick?** | Making every code accept 1 tick earlier cost 0.5-0.8 (`search3.out`, 3 worlds) | [?] `/api/clock` lists only the trading limit (1 per team per tick); the deck says duel limits are separate | If they're per duel, `runner.closer`'s line-up (one accept per tick across 6 duels) forces needless early accepts |

**Not changing:** the opener, the accept rules, no offer budget, the 3 P floor.

**Optional (Aleks's §3.5 stretch):** give the strategist the appendix's rival book as facts when a first message
matches a template. This is untested in the model.

**How to read Δ.** Duels I gave us 13.93 duel points over 34 duels. The Analyst's §1b mapping (duel part ≤ 12 Saturday
points = 8 board) suggests about 0.4 board per duel point, if Duels II feeds the same part [?].

## 6. Risks and first-wave checks

- **Model risk [L].**
  - Rivals are fitted on 34 duels; their bots may change.
  - Within this simulator, the step-size gain is positive in every world and under ρ 0.6.
  - Still unknown: a structure the simulator lacks (e.g. rivals that read big steps as weakness and stop conceding),
    and the out-of-sample miss above.
- **Days scoring [?].** At the first deals of wave 1, check `pred` = `points` with the day value in. If it misses, read
  the jump: our gain ÷ best pie (H1) or ÷ pie at the agreed day (H2).
- **Day reading [V for code, ? for payload].** `days.py` has never seen the real `your_days_weight`. If it prints
  `CAN'T READ`, every day rule falls back to the models.
- **Live checks per wave** (`agents.duelist review`):
  - no concession over 18% of the gap outside the closing ticks (1a), or every one about 15% (1d);
  - our share per deal against Duels I's inferred ~0.58.
  - Rounds per deal can't tell the change apart: the baseline is already 3.7-4.0 in the model.

## Appendix: rival book (Duels I templates; each team plays us 4× in Duels II) [V transcripts, L types]

| Duels | Template (first message) | Type | What happened |
|---|---|---|---|
| 2296/2297 | "Thank you for meeting me. I can do N P." | Fast, then holds near the middle | We took theirs at shares .52/.54 after 4-6 rounds. In 2296 they offered 101 (share .73) at round 3, then slid back to 97 |
| 2318/2319 | "I can do N. That is a fair deal for both of us." | Slow every tick, accelerating +3..+15 | Took our offer at rival share .21/.40 after 9 rounds. Our messages only added rounds |
| 2356/2357 | "Propuesta justa para cerrar pronto…" (rotating Spanish lines) | Slow shrinking steps every tick | Took our 117 (rival .42); we took their 78 |
| 2366/2367 | "67?" / "101?" | Repeater, never moves | 2366 took our 110; 2367 no deal (never inside our limit) |
| 2430/2431 | "N for [item]. Every round costs us both…" | Two ~11 P steps, then a silent hold | Refused our offers even at a rival share ≈ 0.46-0.61; we took their number at the deadline (.20/.24) |
| 2460/2461 | "Happy to close quickly at N…" / "A real step from me" | Slow, 2-9 P every tick | 10-12 rounds; they took ours |
| 2472/2473 | "N P y cerramos ahora." | One message, then accept-only | Took our walk late, 1 round |
| 2506/2507 | "Propongo este precio, creo que es justo para los dos." | 9-12 P bursts every ~3 ticks | 6-7 rounds |
| 2540/2541 | "Hello! I can do N. Thank you for your time." | Shrinking steps every tick | Met our number (our share .87 in 2541) |
| 2584/2585 | "We can do N P. Thank you for the talk." | Generous opener inside our limit | Took our opener (2584) |
| singles | 2522 "Let's close it quickly" (1-2 P/tick) · 2534 "Puedo llegar a N primas" (took ours at .27) · 2535 "Es una pieza que merece su precio" (repeater, took ours at .24) · 2530 "Hi there. N P from my side." (we took 97: our share **.16** of a 63 P pie, the biggest leak) · 2446/2495 silent accept-only · 2414/2415/2523 silent, no deal | | |
