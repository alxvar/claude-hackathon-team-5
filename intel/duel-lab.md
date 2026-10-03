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

## Overnight program, checkpoint 1 (Sat 22:20): Duels III and the Final

_For Aleks's Sunday morning. Duels III and the Final: 12 ticks, 10% decay, 4 at once, price + day
(`/api/schedule` at 22:08: Duels III `rounds` 2 = 68 duels; the Final `rounds` 1 = 34). Code and raw outputs are in the
scratchpad `night/`: `sim2.py`, `fit2.out`, `clusters.out`, `calib2.out`, `validate2.out`, `search_n1.out`,
`final2.out`, `final3.out`, `tuner.py`, `tuner_dryrun.out`. Code-only: no LLM spend, no game writes, no duelist process.
Labels: [V] measured on records or code, [L] modelled, [?] unknown._

### Recommendation: three constants, about +1.5 duel points over Duels III [L]

| Constant (live → proposed) | Where | Δ per duel at 12 ticks / 10% |
|---|---|---|
| `MIN_STEP_P` 3 → **5** | `agent.py:50` | +0.010 alone |
| `MAX_STEP_SHARE` 0.25 → **0.18** (back to the 16:30 value; a40ced6 raised it to "close faster") | `agent.py:52` | +0.003 alone |
| `LATE_SWITCH_LEFT` 4 → **2** | `agent.py:54` | +0.008 for "off"; at 2 ticks the switch stays as a last-moment deal-saver, at the same score |
| **All three together (Q4)** | | **+0.022 per duel** (5 worlds: worst +0.015, best +0.027; CI ±0.0015). Under the other scoring reading (H2): +0.022. On the Duels II setting: +0.022. **≈ +1.5 points over 68 Duels III duels, +0.75 in the Final** (baseline ≈ 0.37 per duel: +6%) |

- **Stronger variant:** `MIN_STEP_P` 6 (Q5): +0.027, worst +0.018. The gain grows from 4 to 6 P (4: +0.018; 5:
  +0.023; 6: +0.027).
- **Not recommended, though the model likes them:**
  - **A fixed code opener at 0.55 × limit (+0.063 in the model).** The raw data disagrees: our 9 Duels II openers above
    1.0 × limit all closed, with the best mean result (27.1 P vs 22.9 for 0.4-0.7). The model draws our opener
    independently of the pie; reality likely isn't independent. [?]
  - **`OPEN_WAIT` 2 → 0 (+0.006).** The model charges the waiting ticks but undervalues seeing their day first; the
    earlier days model said the opposite. Conflicting models, so keep. [?]
  - **Accept at the last tick, `ACCEPT_BY` 1 (+0.006):** a missed settle on 15 s ticks costs the whole deal.
- **Confirmed no-change [L]:**
  - the opener scale (×0.8 and ×1.2 both lose);
  - the accept rules (`acc_f` thresholds ≈ 0; earlier exact replays lose);
  - give the day only when C ≤ 15 (C ≤ 30/60/always lose −0.018 to −0.057: many rivals ignore the day when they price);
  - `SILENT_KEEP` 0.15 (0 and 0.3 both lose a little);
  - `DECIDE_LEFT` / end-game step (both directions lose).

### 1. Rival fits on the Duels II transcripts (35 closed duels) [V counts, L types]

- **Price behaviour:**
  - reply-only: 66% (answers each of our messages, else silent);
  - clock: 17% (posts every tick);
  - one-shot / accept-only: 14%;
  - silent: 3%.
- **Day behaviour:**
  - locked at its own best day: 34%;
  - moves (copies ours or erratic): 31%;
  - locked at the far end (day-blind?): 17%;
  - locked at day 5: 14%.
- **Reaction to our step [V, n = 67 exchanges]:** their concession after our message doesn't depend on our step size
  (slope −0.06, corr −0.06). They give ≈ 12-14% of the gap per reply whether we concede 0 P or 15 P. So our step size
  only decides how much share we hand over; the number of messages decides the decay.
- **Pies are bigger than in Duels I:** inferred median 0.44 × our limit vs 0.26 (8 duels with a score jump). Our shares
  were lower (median 0.52).
- **The worth formula reproduces the game's `result` in all 33 closed deals [V].**

### 2. Simulator validation (`validate2.out`) [L]

- **Calibrated on Duels II after the day fix:** deal rate, rounds, worth per deal, result per duel and share fitted
  within ±10% (rounds −10%).
- **Per duel:** each real duel was simulated 1,000 times with its own role, limit and day weight.
  - The actual result falls inside the simulated 10-90% band in 29-31 of 32 duels.
  - Predicted total result vs actual: −0% / −9% / −3% across the three calibrated worlds.
  - Mean per-duel error is ≈ 10 P, so a per-deal ±10% match isn't achievable with unknown rival limits. The aggregate
    is.
- **Five worlds bracket the uncertainty:** three calibrated, one with the exact Duels II rival mix, one where 80% of
  rivals price the day.

### 3. Latency: code-first moves (design for the Builder) [L]

- **Live today:** Duels II decisions averaged 9.4 s on Opus medium, 29% over 10 s [V]. Sunday's decision budget is
  10 s.
- **Design:**
  - The LLM makes **one** decision per duel: the opener, during the 2-tick `OPEN_WAIT`, so it has time.
  - **Every later move is code:**
    - step = 12-15% of the gap in worth, clamped to [`MIN_STEP_P`, `MAX_STEP_SHARE` × gap];
    - accept = the existing closer;
    - day = the existing `day_read` rules;
    - holds = the existing rules.
  - **Text:** the template "I can do N P, delivery on day D." (the claims guard already falls back to it), or an
    optional Sonnet-low text with a hard 3 s cap that never delays the send.
- **Effect:** every non-opener move goes out within about a second of the tick.
- **In the model:** code steps score as well as the LLM's steps (12% steps on top of the other changes: +0.027 vs
  +0.024 with LLM steps). So moving steps into code costs nothing and removes the latency risk.
- **Test:** fake server at 15 s ticks, 4 concurrent duels; every send lands within 5 s of its tick.

### 4. Between-waves tuner (`night/tuner.py`; advisory: Aleks approves, the Builder wires the hot-reload)

- **What it does:** reads the session's closed records and proposes at most three constants in fixed bounds, one notch
  per wave:
  - `MIN_STEP_P` 3-8;
  - `MAX_STEP_SHARE` 0.12-0.25;
  - `HOLD_TICKS` 2-5.
- **Guardrails:** nothing changes before 6 closed duels; a change is reverted if the next wave scores under 0.7× the
  session mean. Output is a JSON file (`version`, `params`, `reason`, `evidence`, history) written atomically, which the
  duelist can reload by mtime.
- **Dry run on Duels II:** no rule fired (deal rate 0.889 among rivals that spoke, 3.6 rounds per deal;
  `tuner_dryrun.out`).
- **Its rules are untested in the model:** a wave is about 4 duels, so it's a safety valve, not an optimiser.

_Next checkpoints: 01:00 (re-run on the complete Duels II set) and 04:00 / 07:30 (final, verified)._

## Update Sat 22:30: for Sunday (Duels III ≈ 11:00, 12 ticks, 10% decay, 4 at once; the Final the same)

_Data: the closed Duels II records in `docs/duels/` (30 for the 21:50 replays, 32-33 by 22:20) and Duels I. Outputs in
the scratchpad `lab2/`: `fast_v2.out`, `rules_v2.out`, `rules10.out` (the same replays re-scored at Sunday's 10% decay),
`d2_v3.out`, `latency.out`, `lateswitch.out`._

_Method: each replay takes an offer the rival actually made, at the moment it appeared, with the rounds counted up to
that moment. Messages are kept in the game's own order. A first draft re-sorted them (the rival first within each tick);
the verifier caught it, and everything below is re-run. Worth is days-aware (buyer: limit − price − w·day; seller:
price − limit + w·day), and it reproduces the game's `result` in **all 33 closed deals** [V]. Units are P of
`result`: pies are known for only 6 Duels II duels [L: P overweights big pies]. Two verifier passes are applied._

**Bottom line for Sunday: fix latency; keep the accept rules. Two small optional tweaks.**

| # | Change | Evidence | Test |
|---|---|---|---|
| 1 | **Fit the 15 s tick.** Strategist on Opus `--effort low`, not medium. Fix the failover budget (`engine/failover.py` `timeout_s` = 20 s): it is longer than the runner's whole-decision timeout (`runner.py`: max(8, tick − 5) = 10 s at 15 s ticks), so a slow primary never reaches the backup. The backup still runs on a fast error or during the 120 s cooldown | **Duels II, Opus medium, 6 at once [V]:** model decisions mean 9.4 s, p95 13.6 s, max 20 s; 29% over 10 s (35% in the later waves). If Sunday looked the same, about a third of model moves would become code fallbacks [L: projection]. **Duels I, Opus low, 3 at once [V]:** mean 6.3 s, p90 7.2 s, 7% over 8 s, 1% over 10 s; at least two decisions over 12 s, max 25 s. Effort and load are confounded. **Aleks's red team [L]:** Opus low max 8.0 s; points per duel 0.386 (Opus low), 0.424 (Opus medium), 0.273 (Sonnet medium, 70% closed). `saturday-plan.md` plans a Sonnet strategist for Sunday; on those numbers Opus low is the better trade | Smoke with 4 concurrent days duels at 15 s ticks: p95 under 9 s and no `timeout` fallbacks |
| 2 | **Accept rules: keep the closer.** Optional: break-even **only in the last 4 ticks** (accept a standing in-limit offer when their last step < d/(1−d) × its worth and ≤ 4 ticks are left) | **[V replays]** The broad rules all lose. After the day fix, at 8% decay: break-even at any time −65.7 P, accept-first −47% per duel, B (≥ 50% of our opener) −10%, `ACCEPT_BY` 3 −1.5 P. **Re-scored at 10%:** break-even −9%, accept-first −49%. **Only two endgame variants are flat or slightly positive:** break-even from 4 ticks left +2.7 P (8%) / +3.1 P (10%) over 24-32 duels (5662, 6094), and "their jump ≥ 15% of the gap within 4 ticks" +0.4 / +0.8. Duels I in share: break-even −0.67, accept-first −2.94 of 9.06 | Offline runner: in-limit offer at 4 ticks left with their last step under d/(1−d) × its worth → accept; a bigger step → no accept |
| 3 | **Late switch: optional narrowing.** Skip it when an in-limit rival offer is standing **and** the rival posts without waiting for us (a clock bot) | [V `lateswitch.out`] 9 firings by 21:55: 6 with an in-limit offer standing, 2 without (5801 then closed at 3.6; 5813 no deal), 1 live. **Clock rival (6094: it posted every tick, 1273-1287):** the replay is exact, and the switch's extra round cost 24.1 → 28.5 at 8%. **Reply-only rivals (5662, 5663):** their better offer came right after our switch, so the switch may have drawn it [L]. n = 1 exact case | Offline runner: a clock rival with an in-limit offer at 4 ticks left → no switch; a reply-only rival → the switch goes out |

**The Chief's three duels, plus the real leaks [V transcripts, game order]:**
- **5653 and 5797 aren't losses.** Their earlier "in-limit" offers were in limit on price only: 93 on day 10 was worth
  −2.3 to us, 60 on day 10 was worth −12.3. **Any such check must use worth including the day.**
- **The real leaks share one pattern: late in the duel, we countered an improved in-limit rival offer instead of
  taking it** (verifier's figures):
  - 5808 −1.4: their 159 on day 0 (worth 36) arrived at round 4; we sent one more offer and took 158 at round 5.
  - 5662 −2.4: their 100 came at round 6; we countered 110 and took the same 100 at round 7.
  - 6094 −2.1: we echoed their 65 instead of accepting it.
  - 5663 −0.4.
  - Total ≈ 6 P over the first ~30 duels: about 1% of the result.
- **The endgame break-even (#2) targets exactly this pattern,** and it is the only accept rule that doesn't lose on
  replay.
- **The "33% lost to decay in wave 3"** is the Chief's figure. These replays show it as the price of haggling that paid:
  cutting rounds by accepting earlier lost more than it saved.

**Also check for Duels III (12 ticks) [?, not modelled]:** the fixed tick constants were set for 16-tick duels:
`OPEN_WAIT` 2, `LATE_SWITCH_LEFT` 4, `ACCEPT_BY` 2, `DECIDE_LEFT` 3, `HOLD_TICKS` 3. With 12 ticks they cover a larger
share of each duel. The overnight search will test them.

## Update Sat 18:30: second pass before the 19:30 freeze (Chief's three questions)

**Answer: one change, as insurance. Everything Aleks picked from the Lab's list is live** (69ef465 + 89a6dd6, running
since 17:15). The fixed 15% step and `HOLD_TICKS` 3 → 5 were declined at 16:24 and stay out.

**1. Pairings: not visible [V].**
- `/api/duels` lists 0 live duels (tick 972).
- `/api/schedule` gives only the parameters: Duels II at hour 11.65 ≈ 20:33, `rounds` 2 (each team plays us 4 times),
  16 ticks, 8% decay, 6 at once, price + days.
- **The meeting order can't predict the rival either [V].** The order differs between sessions: by Friday id, R3, R15,
  R7, R8, R1, R13, R4, R5 (`docs/duel-rivals.md`), against R1, R3, R4, R5, R7, R8, R13, R15 in Duels I.
- **So rivals can only be identified live**, from the first line's wording (fingerprints in `docs/duel-rivals.md`). The
  live day and step rules don't depend on the cluster, so no per-cluster parameters are needed.

**2. Duels I losses, re-checked with days in play.**
- **The 4 no-deals can't be recovered by a rule [V transcripts]:**
  - 2367: R5 never came inside our limit (its lowest was 83 against our 72).
  - 2414/2415: R6 was silent (Team 11 [L]).
  - 2523: R13 was silent in that role. The only lever is the silent walk, and it already goes further:
    `SILENT_KEEP` 0.15 walks to 183 of our 196, not 170.
- **Days may silence more scripted bots** (a priced message without `days` is refused). The walk and the accept-only
  path cover that, and both are live, but the walk runs only when we can read our day weight (`runner.py`: an unreadable
  days duel stays with the models).
- **The rounds loss.** The 18% step cap is live.
- **Aleks's "stay silent against clock bots", re-scored in share** [L: the pies are inferred] (`silence_share.out`, 10
  of his 12 duels: 2460 and 2507 have no pie): **−0.19** share-points as a rule for every clock-bot rival (R15 −1.00),
  **+0.80** for R4, R9 and R13 only. It works only as a rule keyed to the rival's
  wording, and that needs a matcher built before the freeze, with no evidence the wording survives the days update.
  **Not worth it tonight.**
- **The biggest swing left is our day reading [L, Aleks's red team, `docs/duelist-redteam.md`].**

  | Our reading of the day weight | Points per duel |
  |---|---|
  | read right | 0.47 |
  | direction unknown | 0.23 |
  | can't read | 0.15 |
  | direction backwards | −0.18, with 30% of deals worth less than nothing |

  - **The danger:** backwards against right is ≈ 0.65 per duel in the red team's simulated share score [L], about 4
    points per wave of 6.
  - **The gap today [V code]:** there is no switch to flip or distrust the reading. `read_days` has no flag, no
    environment variable and no override file.
  - **The cost of fixing it live [L, my guess at the timing]:** a wrong reading at 20:33 would need a code edit, the
    suite and a restart mid-session. At about 8 minutes per wave, that's probably 2-4 waves, or 8-16 points.

**3. Changes for Aleks.**
1. **Day-reading override, default off** [L, insurance].
   - **What:** `supervise.sh … --days-read auto|flip|unsure`, passed through to `read_days`.
     - `flip`: reverse the reading's direction (for a linear weight, day d gets day 10 − d's value; our best end
       becomes the other end), and `sure` stays.
     - `unsure`: set `sure = False`, the safe "direction unknown" mode (0.23/duel, no negative deals in the red team).
     - `auto` (the default) behaves exactly as now.
   - **Tests:**
     - the red-team "backwards" fixture with `flip` scores as "read right";
     - `auto` passes the current suite unchanged.
   - **Runbook, 20:33:** read the console's day line against the game's `days_meaning`.
     - Clearly reversed: restart with `flip`. A restart doesn't re-send (records).
     - Ambiguous: restart with `unsure`.
   - **Worth [L]:** 0 if the reading is right. If it's backwards, about 1 wave lost instead of 2-4, which saves ≈ 4-12
     points (red-team share score, my timing guess).
   - **The freeze rule (PLAN #23)** asks for a clear sim gain. This change has none by default: `auto` is today's code.
     Its gain exists only if the reading is wrong, so whether it qualifies is Aleks's call.
2. **No other change.** The step cap, the day tweaks, `SILENT_KEEP`, per-duel accepts and the 2-tick day wait are all
   live, and the red team found no tweak clearly better (best +1.7%).

_Everything below is the 16:15 report, unchanged._

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
