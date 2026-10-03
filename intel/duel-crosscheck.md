# Duel cross-check: an independent model against the Duel Lab (Sun 04 Oct, before Duels III and the Final)

_Independent quant pass, analysis only: no game calls, no keys, no edits outside this file and
`docs/duels/opponent_profiles.json`._
- _**Built from:** `docs/duels/*.json` (136 duels), `scores.jsonl` and `RULES.md`, before reading `intel/duel-lab.md`
  (§4 uses its Sun 02:00 version)._
- _**Labels:** **[V]** counted on the records, **[L]** modelled, **[?]** unknown._
- _**Checked:** an independent verifier pass audited this file against its outputs (1 blocker, 8 major, 8 minor
  flags), and every flag is fixed below._
- _**Code and raw outputs** are in the session scratchpad (`model.py`, `sim.py`, `labpol.py`, `labsim_*.py`,
  `out/*.out`), which is temporary._

## Verdict

- **We agree on the Lab's recommendation.**
  - **Set C, code-first, with the 02:00 openers (seller 0.42 in price, buyer 0.37)** is my best robust choice too.
  - It beats the FINAL params file (`MIN_STEP_P` 5, `MAX_STEP_SHARE` 0.18, `LATE_SWITCH_LEFT` 2,
    `MONO_END_SHARE` 0.5) in both models: **+0.03 share per duel in mine, +0.06 in theirs (R1)**.
  - Both models also rank C > A > today (code against code), find code-first ≥ LLM moves, find `MONO_END_SHARE` 0.5 no
    better than 0.25, and find per-opponent adaptation not worth building.
- **We disagree on one design question: the closing.**
  - **My model's optimum ("XC"):** no mid-duel messages at all, **one** final offer at 3 ticks left that concedes 55%
    of the gap, then accept their offer on the last tick.
  - **With the same openers (0.42 / 0.37) XC beats C by +0.040 ± 0.010 share per duel in my model** (better against 15
    of 17 teams) [L].
  - **In the Lab's simulator it loses in 14 of 15 cells, by 0.001 to 0.030,** and wins one by 0.007 [L].
  - **The data on the crux are mixed (§4).** Two teams (C, G) keep conceding while we're silent; two (H, L) barely move
    either way; the Lab's Duels I re-score of "stay silent against clock bots" is negative.
  - **Edge of XC over C: −0.03 to +0.04 per duel. Not worth a code change on Sunday.**
- **Per-opponent profiles: −0.012 ± 0.012 share per duel out of sample** (cross-fit). The in-model upper bound is
  +0.035 ± 0.009. Not worth building [L]. Use the JSON for monitoring and to recognise rivals.

## 1. Data facts the model stands on [V]

- **Score field.** The `result` of a deal = our surplus × (1 − decay)^rounds: exact on 105 of 105 deals.
  - Seller surplus = price − cost + w·day; buyer surplus = value − price − w·day.
  - rounds = min(our priced messages, theirs). Accepting adds no round, and a rival that never speaks keeps rounds at
    0 (2446: it accepted our opener without a word, 0 rounds).
- **The game scores share of pie, not P.**
  - Duels II added 21.46 `duel_points` over 68 duels (0.316 per duel), while its results summed 1,210 P.
  - Duels I: 13.93 points (0.41 per duel) for 479 P.
  - The ratio differs by session, so the points aren't P. I report **share × 0.9^rounds** first and P second.
  - My simulator takes the pie as the rival's reservation (§2): a ranking proxy, the absolute shares are approximate.
- **Aliases are random per duel.** "Rival Oro" appears 7–8 times per session, and the two duels of a pair usually
  carry different aliases.
  - Each opponent plays us in a **pair**: ids n and n+1, the same item, one duel per role.
  - Teams are fingerprinted by message templates: **17 teams (A–Q)**. In Duels II each has exactly 2 pairs.
  - **Links back to Duels I and the practice round:**
    - high confidence for most teams;
    - medium for K, O and Q;
    - low for J and P. P and Q are split by behaviour only: P never accepts, Q accepts late;
    - F and N are unlinked before Duels II.
  - Regexes for each team are in the JSON (`identify.signature_regex`).
  - **When they speak:** 10 teams by tick 1, M by t2, A by t3. In Duels II, H opened at t7–11, E at about t6, O at
    t5, Q at t11 or never, and P never spoke.
- **Latency (Duels II LLM decisions):** median 9.1 s, p90 12.4 s. 7% take over 13 s and 1.2% over 15 s. Duels handled
  by code alone averaged 0.6–0.8 s per decision (README `avg_s`).

## 2. Opponent model and out-of-sample validation

**The model, per team and pooled over roles.** u = our surplus as a share of our limit.
- **Tempo:** P(message | we spoke the tick before) and P(message | we were silent), plus the tick of its first offer.
- **Opening:** u0.
- **Concession per message:** 1.2 × (a + b·gap + c·our last concession + t·k/T). The 1.2 is a global calibration:
  without it the replays reach about 85% of the rivals' real concessions.
- **Reservation:** R = u0 + D, with D log-normal. Offers are capped at R.
- **Acceptance:** they take our offer if it is within their current offer + α·(R − current). In the last
  (window + 1) ticks they take anything up to R.
- **Days:** day-aware κ, and their preferred day by role. Hand-coded from the day table.

The fit uses an offer-path plus acceptance likelihood, shrunk toward the pooled model, on the 116 team-attributed duels.
In the table:
- **Tempo** is the raw count over all sessions [V].
- **Step** is the rival's mean move per message, day-adjusted, from the JSON [V]. The price-only steps in
  `out/facts.out` differ slightly.
- **The other columns** are fitted [L].

| Team | Template | Msgs after our msg / after our silence [V] | 1st offer | Opening u0 (zone share claimed) | Step per msg | Room D | α · deadline window | Day (κ; pref as buyer / seller) | Our P per duel, deal rate (n) |
|---|---|---|---|---|---|---|---|---|---|
| A | Propongo | 7/26 / 15/47 (periodic) | t3 | −0.23 (1.82) | 0.086 | 0.50 | 0 · 1 | 0; d0/d0 | 7.5, 0.67 (6) |
| B | HiThere | 1/18 / 11/33 (periodic) | t1 | +0.01 (0.99) | 0.097 | 0.80 | 0 · 0 | 0.5; d5/d5 | 18.6, 0.83 (6) |
| C | TeOfrezco | 33/33 / 25/25 (clocked) | t0 | −0.12 (1.21) | 0.033 | 0.70 | 0.25 · 5 | 0; d0/d10 | 22.7, 1.0 (8) |
| D | PropuestaJusta | 39/45 / 4/36 (reactive) | t0 | −0.12 (1.41) | 0.042 | 0.40 | 0 · 2 | 0.5; d5/d5 | 11.6, 0.88 (8) |
| E | HolaPerfect | 1–2 msgs per duel (sparse) | t6 | −0.13 (1.36) | 0.33 (n = 2) | 0.50 | 0.5 · 0 | 0.5; d0/d0 | 10.1, 1.0 (6) |
| F | RapidoJusto (trades days) | 26/32 / 0/39 (reactive) | t1 | −0.03 (1.07) | 0.094 | 0.50 | 0 · 0 | 1; d3/d8 | 18.7, 1.0 (8) |
| G | HelloICanDo | 29/29 / 29/29 (clocked) | t0 | +0.06 (0.92) | 0.039 | 0.70 | 0 · 0 | 1; d0/d10 | 18.5, 1.0 (6) |
| H | Barrio small-talk | 40/40 / 26/26 (clocked) | t0 (I), t7–11 (II) | −0.14 (1.41) | 0.016 | 0.50 | 0.25 · 0 | 0; d5/d5 | 10.4, 0.88 (8) |
| I | ThankYouMeeting | 15/19 / 3/32 (reactive) | t0 | +0.09 (0.85) | 0.074 | 0.50 | 0 · 1 | 0; d0/d10 | 28.5, 1.0 (8) |
| J | Effusive LLM | 35/36 / 4/18 (reactive) | t0 | −0.45 (2.28) | 0.101 | 0.80 | 0.5 · 1 | 0; d10/d10 | 16.6, 0.83 (6) |
| K | HappyPrimas LLM | 26/33 / 4/26 (reactive) | t0 | −0.03 (1.05) | 0.057 | 0.60 | 0.25 · 1 | 0.5; d0/d10 | 21.6, 1.0 (6) |
| L | DayCost (+1 steps) | 26/29 / 24/32 (clocked) | t0 | +0.08 (0.88) | 0.010 | 0.60 | 0.25 · 1 | 1; d0/d10 | 15.7, 0.88 (8) |
| M | ThankForTalk | 10/13 / 6/16 (periodic) | t2 | +0.14 (0.68) | 0.043 | 0.30 | 0.25 · 0 | 0; d0/d0 | 39.6, 1.0 (6) |
| N | VoyConPrisa | 10/20 / 2/40 (reactive) | t0 | +0.04 (0.93) | 0.096 | 0.50 | 0 · 1 | 0.5; d0/d10 | 18.0, 1.0 (6) |
| O | OneShot (Duels II) | 1 msg per duel in Duels II | t5 | +0.06 (0.81) | 0.076 (n = 5, Duels I) | 0.25 | 0 · 0 | 0; d0/d0 | 16.0, 0.62 (8) |
| P | Silent | never speaks, never accepts | — | — | — | — | — | — | 0.0, 0.0 (6) |
| Q | Late one-shot / silent accepter | 1 msg or none | t11 | −0.06 (1.25) | — | 0.30 | 0 · 0 | 0; d0/d0 | 7.5, 0.67 (6) |

**Out of sample [L].** Fitted on the practice round, Duels I and Duels II round 1; tested on Duels II round 2 (34
duels, one pair per team):

| Metric | Team model | Pooled model | Team − pooled, paired |
|---|---|---|---|
| Opening, MAE (u) | 0.220 | 0.276 | **−0.055 ± 0.019** |
| Concession step, MAE (u) | 0.052 | 0.062 | −0.010 ± 0.005 |
| Message timing, Brier | 0.157 | 0.214 | **−0.057 ± 0.019** |
| Deal / no deal, Brier (replay of our actual offers) | 0.148 | 0.218 | **−0.071 ± 0.029** |
| Points, MAE (replay) | 10.4 P | 11.4 P | −1.0 ± 1.3 (n.s.) |
| Points, bias (replay) | −3.9 P (in sample: −1.2 P) | −4.9 P | — |

- **The profiles predict behaviour** out of sample: openings, tempo, deal or not.
- **They don't predict points or who accepts better.** The error is dominated by the hidden ZOPA, and the acceptance
  parameters overfit.
- **In P the model is pessimistic** by ≈ 4 P per duel out of sample.
- **In share it reproduces the real score.** An LLM-proxy of the policy we played, at Duels II settings, gives **0.30**
  share per duel against the **actual 0.316** (`out/ablation_share.out`).

## 3. Simulator and policy search (Sunday: 12 ticks, 10% decay, 15 s ticks)

**Setup.**
- Every policy plays all 17 team models with common scenario draws: our limit and w drawn by role from Duels II, the
  rival's w from the other role.
- A missed tick delays our move one tick; a delayed accept of a replaced offer fails.
- Random search and coordinate refinement (console output, not saved), then a base run plus 8 model variants:
  - missed ticks at 10% and 25%;
  - pooled rivals;
  - harsh deadline;
  - no deadline acceptance;
  - fitted on the earlier data only;
  - every rival day-aware;
  - rivals that compress their clock to 12 ticks.

**XC at the Lab's openers (0.42 / 0.37)** (`out/ablation_share.out`, 2,000 draws per team; paired SE of a difference
≈ 0.01) [L]:

| Change to XC | Share per duel (base: 0.35) |
|---|---|
| 3 small mid-duel steps (12% of the gap, in reply) | 0.31 |
| Final concedes 70% / 55% / 40% of the gap | 0.32 / 0.35 / 0.36 |
| Accept from ticks_left 2 instead of only on the last tick | 0.31 (it pre-empts their acceptance of our final) |
| Seller asks day 0 instead of 10 | 0.28; 0.27 vs 0.29 even if every rival is day-aware |
| No silent-rival walk | 0.35 overall: Q 0.36 → 0.28, H 0.30 → 0.33 (H opens late, after the walk has started) |
| Mid-duel accept ratio 0.7 / 0.9 / 1.0 | 0.34 / 0.35 / 0.35 |

**Mean rounds per duel:** XC 1.5, C 2.0, today's LLM proxy 2.8.

**Head to head, share per duel** (`out/open_share.out`, 2,000 draws per team) [L]:

| Policy | Base | 10% missed | 25% missed | Pooled rivals | No deadline accepts | Earlier-data fit | All day-aware |
|---|---|---|---|---|---|---|---|
| XC, openers 0.9 / 0.6 (this model's optimum) | **0.38** | 0.37 | 0.36 | 0.28 | 0.26 | 0.38 | 0.32 |
| XC, openers 0.42 / 0.37 | 0.35 | 0.35 | 0.35 | 0.27 | 0.24 | 0.35 | 0.29 |
| **Set C, openers 0.42 / 0.37 (recommended)** | 0.31 | 0.31 | 0.32 | 0.23 | 0.20 | 0.29 | 0.26 |
| Set C, openers 0.73 / 0.37 (a99f641) | 0.31 | 0.31 | 0.31 | 0.23 | 0.21 | 0.29 | 0.27 |
| FINAL params file (LLM proxy) | 0.28 | 0.28 | 0.29 | 0.23 | 0.22 | 0.27 | 0.24 |
| Today (LLM proxy) | 0.28 | 0.28 | 0.28 | 0.23 | 0.21 | 0.27 | 0.24 |

- **Set C is flat in the opener** in my model (0.31 to 0.32 from 0.42 to 0.9). The Lab's simulator prefers 0.42
  clearly, so the 02:00 ruling costs nothing here.
- **Missed ticks barely matter for code-decided policies.** XC's two fragile ticks are the final at ticks_left 3 and
  the last-tick accept. With an LLM in the loop, move the final to ticks_left 4.

## 4. Cross-check with the Duel Lab

**The Lab's sets in my simulator** (its code policy re-implemented from `origin/duelist-loop`: `policy.py` plus the
runner's closing rules; P per duel, `out/robust_pts.out`, 1,000 draws per team) [L]:
- **Set against set:** C 17.1 > A 16.7 > today (code) 16.3.
- **LLM proxies:** FINAL file 15.8, today 15.6.
- **`MONO_END_SHARE` 0.5 on C:** 16.0, against C's 17.2 in the same run (`out/facts.out`). 0.5 and 0.6 are identical:
  `END_STEP_SHARE` 0.5 binds.
- **Agrees with the Lab's ordering of C, A and today.** The FINAL file sits below today-code here. The Lab compared it
  with today's LLM, where FINAL is ahead in both models (15.8 vs 15.6 here).

**My XC inside the Lab's simulator** (`tools/duel_sim_v2.py`, imported read-only; RW worlds; H1 share; both policies
open at a **price** share as `policy.py` reads it; `out/labsim_open_H1.out`, 6,000 duels per cell). XC − C:

| Rival mix | 0.42 / 0.37 (R1..R5) | 0.73 / 0.37 (R1..R5) |
|---|---|---|
| Lab's (66% reply / 17% clock / 14% accept-only / 3% silent) | −0.020, −0.013, −0.022, −0.030, −0.011 | −0.013, −0.003, −0.017, −0.024, −0.009 |
| Measured, periodic teams as "clock" (35 / 41 / 18 / 6) | −0.001, +0.007, −0.005, −0.011, (R5 = R1) | +0.007, +0.017, +0.002, −0.006 |
| Measured, periodic teams as "reply" (53 / 24 / 18 / 6) | −0.011, −0.005, −0.015, −0.022, (R5 = R1) | −0.005, +0.004, −0.010, −0.018 |

- **The best cell in the Lab's simulator is C at 0.42 / 0.37:** 0.468 in R1 with the Lab's mix.
- **XC only beats C at high openers, where C itself is weak.**

**Where the models disagree, and what the data say:**
1. **Do rivals keep conceding while we're silent? (the crux)**
   - **Tempo [V]:** C, G and H message on every tick after our silence (25/25, 29/29, 26/26), L on 24/32, and A, B and
     M on 32–38%.
   - **Concession on those ticks [V]:**
     - C 0.054 u per message (n = 25) and G 0.024 (n = 29): they keep moving.
     - H 0.003 (n = 26) and L 0.008 (n = 23) barely move, but they barely move when we concede either (0.024 and
       −0.008).
     - A 0.052 (n = 5) and M 0.026 (n = 3) are too few to read.
   - **Anecdotes [V, confounded: n = 1 each, and 5652 includes a day-10 term]:**
     - 5652 (C): 2 offers from us, the rival walked from 0.87× to 1.56× our cost on its own. 52.9 P, best of Duels II.
     - 6094 (G): silent from t0 to t12.
   - **Across Duels II deals [V, confounded by the ZOPA]:** ≤ 2 of our offers averaged 34.5 P (n = 8); ≥ 5 averaged
     12.3 P (n = 23).
   - **Against:** the Lab's Duels I re-score of "stay silent against clock bots" gives −0.19 share-points per clock-bot
     rival (n = 10, inferred pies).
   - **Verdict: mixed. Neither model is clearly better supported on this point.**
2. **Rival mix.** Neither of my two readings flips the Lab's simulator decisively.
   - My strict count: 4 clocked teams of 17 (24%), 3 periodic, 6 reactive, 3 sparse, 1 silent.
   - Counting periodic teams as reply, XC still loses to C by 0.005–0.022.
3. **Deadline acceptance.**
   - **[V]:** 27 of the 55 rival acceptances came with ≤ 3 ticks left. Both models include it.
   - Switched off entirely in my model, XC still beats C (0.24 vs 0.20).
4. **Calibration.**
   - **Mine:** 0.30 share vs the actual 0.316 in Duels II. In P it's pessimistic (−3.9 P out of sample).
   - **The Lab's:** its out-of-sample P check was +18% overall, inside the actual's CI, and +3% on duels where the
     rival spoke. That was the LLM policy at 16 ticks / 8%.
   - **Its 12-tick C (0.43–0.47)** is above our Duels II share (0.316) and near Duels I's (0.41, a price-only session).
   - **Neither model has seen a 12-tick, 10% session.**

**Net.**
- **Agreement:** set C (code, 02:00 openers) over the FINAL file, by +0.03 in mine and +0.06 in theirs (R1).
- **Disagreement:** XC vs C, +0.040 in mine against −0.030 to +0.007 in theirs.
- **Recommendation: ship C as the Lab proposes.** Don't swap the closing logic on Sunday on one model's word.

**Gates** (the Lab's: switch C → A if the deal rate is below 0.60 over ≥ 12 duels with a rival that spoke). Two notes
from my model:
- **The modelled deal rate for C counts silent P as a no-deal:** 0.84 over all duels, ≈ 0.89 over rivals that speak.
- **A rule at 8 duels misfires often.** P(≤ 5 deals of 8 | true rate 0.84) ≈ 12%, so the Lab's 12-duel rule is the
  right one.

## 5. Value of per-opponent adaptation (the bot knows the profile at duel start) [L]

The method:
- **Candidates:** 176 policies (random draws, XC variants, the 6 Lab sets).
- **Robust choice:** the best mean over the teams.
- **Per-team choice:** the best for each team.
- **Gain:** the per-team choice minus the robust choice, scored on the team it was chosen for (`out/facts.out`).

| Estimate | Share per duel | P per duel |
|---|---|---|
| In-model (choose on one draw set, score on another of the same fit): upper bound, no estimation error | +0.035 ± 0.009 (SE over teams) | +2.9 ± 0.6 |
| **Cross-fit** (3 random splits of each team's pairs: choose on half A's fit, score on half B's, both ways) | **−0.012 ± 0.012** (teams) / ± 0.003 (folds) | −0.4 ± 1.0 |

- **Profiles fitted on 6–8 duels per team overfit.**
- **Agrees with the Lab:** +0.0014, 95% CI +0.0001 to +0.0027.
- **The JSON's per-team best responses are in-model only:** reference, not parameters.
- **Silent-rival handling is the one adaptation that pays** (Q: +0.08 share in my model). C already has it as the
  silent walk.

## 6. Caveats

- **Day handling is hand-coded** from the day table, since there are only 4 days-duels per team. Day-aware rivals' w
  is taken as our own role means (buyer 4.0, seller 2.3).
- **The share pie is a proxy:** the rival's reservation R, margin 0.
- **Bots may change for Sunday.** Rivals that change strategy with 12 ticks aren't in the data [?].
- **Team links before Duels II are uncertain** for F, J, K, N, O, P and Q. The profiles lean on Duels II, which has 4
  duels per team.
