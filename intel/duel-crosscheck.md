# Duel cross-check: an independent model against the Duel Lab (Sun 04 Oct, before Duels III and the Final)

_Independent quant pass, analysis only: no game calls, no keys, no edits outside this file and
`docs/duels/opponent_profiles.json`. Built from `docs/duels/*.json` (136 duels), `scores.jsonl` and `RULES.md` before
reading `intel/duel-lab.md`. Labels: **[V]** measured on the records, **[L]** modelled, **[?]** unknown.
Code and raw outputs are in the session scratchpad (`model.py`, `sim.py`, `labpol.py`, `labsim_xc.py`, `out/*.out`),
which is temporary._

## Verdict

- **Partly agree.** Both models say: hold mid-duel instead of stepping, let code decide the moves (not the LLM), Lab set
  **C > A > today ≥ the FINAL params file**, `MONO_END_SHARE` 0.5 is no better than 0.25, and **per-opponent
  adaptation isn't worth building**.
- **Where we disagree: how far to push the hold.** My model says drop mid-duel concessions entirely and close with
  **one** final offer at 3 ticks left. That beats set C by **+0.056 ± 0.010 share per duel** (better against 16 of 17
  teams; +3.3 P per duel) [L]. In the Lab's own simulator the same policy **ties** C: −0.014 to +0.009, depending on
  how many rivals keep conceding while we're silent [L]. The data favour my rival mix (§4), so the expected edge is
  between 0 and +0.056.
- **Best robust params ("XC"), code-decided:**
  - open at once with the Lab's openers;
  - no mid-duel moves;
  - accept at ≥ 0.9 × ours;
  - walk the price down against a silent rival;
  - one final offer at 3 ticks left that concedes 55% of the gap;
  - accept their offer on the last tick;
  - day 10 as seller, day 0 as buyer.

  Details in §3. If the closing logic can't change today, run **set C**: it's the best of the Lab's sets in my model too.
- **Per-opponent profiles:** out of sample, **−0.012 ± 0.012 share per duel** (cross-fit). The in-model upper bound is
  +0.035 ± 0.009. Not worth building [L].

## 1. Data facts the model stands on [V]

- **Score field.** The `result` of a deal = our surplus × (1 − decay)^rounds: exact on 105 of 105 deals.
  - Seller surplus = price − cost + w·day; buyer surplus = value − price − w·day.
  - rounds = min(our priced messages, theirs). Accepting adds no round, so taking their opening offer before we say
    anything scores at full value (2446: 0 rounds).
- **The game scores share of pie, not P.** Duels II added 21.46 `duel_points` over 68 duels (0.316 per duel), while
  its results summed 1,210 P (Duels I: 13.93 points for 479 P). The ratio differs by session, so the points aren't P.
  I report **share × 0.9^rounds** first and P second. Share needs the pie, so in my simulator the pie is the rival's
  reservation (the most it will concede; §2).
- **Aliases are random per duel.** "Rival Oro" appears 7–11 times in one session, and the two duels of the same pair
  carry different aliases.
  - Each opponent plays us in a **pair**: ids n and n+1, the same item, one duel per role.
  - Teams are fingerprinted by message templates: **17 teams (A–Q)**. In Duels II each has exactly 2 pairs.
  - The links back to Duels I and the practice round are high-confidence for most teams; low for J, P and K; F and N
    are unlinked before Duels II.
  - Regexes for each team are in the JSON (`identify.signature_regex`). 13 teams speak by tick 1; E speaks at about
    t6, O at t5, Q at t11 or never, P never.
- **Latency (Duels II LLM decisions):** median 9.1 s, p90 12.4 s. 7% take over 13 s and 1.2% over 15 s. Code-only
  moves take under 1 s.

## 2. Opponent model and out-of-sample validation

**The model, per team and pooled over roles.** u = our surplus as a share of our limit.
- **Tempo:** P(message | we spoke the tick before) and P(message | we were silent), plus the tick of its first offer.
- **Opening:** u0.
- **Concession per message:** 1.2 × (a + b·gap + c·our last concession + t·k/T). The 1.2 is a global calibration:
  without it the replays undershoot the rivals' real concessions.
- **Reservation:** R = u0 + D, with D log-normal. Offers are capped at R.
- **Acceptance:** they take our offer if it is within their current offer + α·(R − current). In the last
  (window + 1) ticks they take anything up to R.
- **Days:** day-aware κ, and their preferred day by role. Hand-coded from the day table.

The fit uses an offer-path plus acceptance likelihood, shrunk toward the pooled model.

| Team | Template | Tempo (P msg after ours / when we're silent) | 1st offer | Opening u0 (zone share claimed) | Step per msg (obs.) | Room D | α · deadline window | Day (κ; pref as buyer / seller) | Our P per duel, deal rate (n) |
|---|---|---|---|---|---|---|---|---|---|
| A | Propongo | periodic (0.39 / 0.17) | t3 | −0.23 (1.82) | 0.086 | 0.50 | 0 · 1 | 0; d0/d0 | 7.5, 0.67 (6) |
| B | HiThere | periodic (0.08 / 0.39) | t1 | +0.01 (0.99) | 0.097 | 0.80 | 0 · 0 | 0.5; d5/d5 | 18.6, 0.83 (6) |
| C | TeOfrezco | **clocked** (1.00 / 0.99) | t0 | −0.12 (1.21) | 0.033 | 0.70 | 0.25 · 5 | 0; d0/d10 | 22.7, 1.0 (8) |
| D | PropuestaJusta | reactive (0.85 / 0.13) | t0 | −0.12 (1.41) | 0.042 | 0.40 | 0 · 2 | 0.5; d5/d5 | 11.6, 0.88 (8) |
| E | HolaPerfect | sparse (≤ 2 msgs) | t6 | −0.13 (1.36) | 0.33 | 0.50 | 0.5 · 0 | 0.5; d0/d0 | 10.1, 1.0 (6) |
| F | RapidoJusto (trades days) | reactive (0.79 / 0.00) | t1 | −0.03 (1.07) | 0.094 | 0.50 | 0 · 0 | 1; d3/d8 | 18.7, 1.0 (8) |
| G | HelloICanDo | **clocked** (1.00 / 0.99) | t0 | +0.06 (0.92) | 0.039 | 0.70 | 0 · 0 | 1; d0/d10 | 18.5, 1.0 (6) |
| H | Barrio small-talk | **clocked** (1.00 / 0.96) | t8 | −0.14 (1.41) | 0.016 | 0.50 | 0.25 · 0 | 0; d5/d5 | 10.4, 0.88 (8) |
| I | ThankYouMeeting | reactive (0.78 / 0.10) | t0 | +0.09 (0.85) | 0.074 | 0.50 | 0 · 1 | 0; d0/d10 | 28.5, 1.0 (8) |
| J | Effusive LLM | reactive (0.95 / 0.12) | t0 | −0.45 (2.28) | 0.101 | 0.80 | 0.5 · 1 | 0; d10/d10 | 16.6, 0.83 (6) |
| K | HappyPrimas LLM | reactive (0.61 / 0.15) | t0 | −0.03 (1.05) | 0.057 | 0.60 | 0.25 · 1 | 0.5; d0/d10 | 21.6, 1.0 (6) |
| L | DayCost (+1 steps) | **clocked** (0.93 / 0.85) | t0 | +0.08 (0.88) | 0.010 | 0.60 | 0.25 · 1 | 1; d0/d10 | 15.7, 0.88 (8) |
| M | ThankForTalk | periodic (0.75 / 0.37) | t2 | +0.14 (0.68) | 0.043 | 0.30 | 0.25 · 0 | 0; d0/d0 | 39.6, 1.0 (6) |
| N | VoyConPrisa | reactive (0.62 / 0.03) | t0 | +0.04 (0.93) | 0.096 | 0.50 | 0 · 1 | 0.5; d0/d10 | 18.0, 1.0 (6) |
| O | OneShot | sparse (1 msg) | t5 | +0.06 (0.81) | — | 0.25 | 0 · 0 | 0; d0/d0 | 16.0, 0.62 (8) |
| P | Silent | **never speaks, never accepts** | — | — | — | — | — | — | 0.0, 0.0 (6) |
| Q | Late one-shot / silent accepter | sparse (1 msg or none) | t11 | −0.06 (1.25) | — | 0.30 | 0 · 0 | 0; d0/d0 | 7.5, 0.67 (6) |

**Out of sample [L].** Fitted on the practice round, Duels I and Duels II round 1; tested on Duels II round 2 (34 duels,
one pair per team). The differences are team model − pooled model, paired:

| Metric | Team model | Pooled model | Paired difference |
|---|---|---|---|
| Opening, MAE (u) | 0.220 | 0.276 | **−0.055 ± 0.019** |
| Concession step, MAE (u) | 0.052 | 0.062 | −0.010 ± 0.005 |
| Message timing, Brier | 0.157 | 0.214 | **−0.057 ± 0.019** |
| Deal / no deal, Brier (replay of our actual offers) | 0.148 | 0.218 | **−0.071 ± 0.029** |
| Points, MAE (replay) | 10.4 P | 11.4 P | −1.0 ± 1.3 (n.s.) |
| Points, bias (replay) | −3.9 P | −4.9 P | in sample −1.2 P |

- **The profiles predict behaviour** (openings, tempo, deal or not) out of sample. **They don't predict points better**:
  the error is dominated by the hidden ZOPA.
- **Who accepts isn't better predicted either:** the team model's acceptance parameters overfit.
- **Calibration on the real score:** an LLM-proxy of the policy we actually played, simulated at Duels II settings,
  gives 0.30 share per duel against the **actual 0.316** [L vs V].

## 3. Simulator and the policy search (Sunday: 12 ticks, 10% decay, 15 s ticks)

**Setup.**
- Every policy plays all 17 team models with the same scenario draws: our limit and w drawn by role from Duels II,
  the rival's w from the other role.
- A missed tick delays our move one tick; a delayed accept of a replaced offer fails.
- A 3,000-policy random search plus coordinate refinement, then a robustness grid over 9 model variants:
  - missed ticks at 10% and 25%;
  - pooled rivals;
  - harsh deadline (window 0, α 0, D × 0.7);
  - no deadline acceptance at all;
  - fitted on the earlier data only;
  - every rival day-aware;
  - rivals that compress their clock to 12 ticks.

**What wins, every time [L]:**

| Component | Effect (share per duel, base model) |
|---|---|
| **No mid-duel concessions** (silence is free; clocked and periodic rivals keep moving) | 3 small steps cost ≈ −0.04 |
| **One final offer at ticks_left 3**, conceding ≈ 55% of the gap (final = theirs + 0.45 × (ours − theirs)) | 30% / 55% / 40% conceded: 0.37 / 0.38 / 0.37 |
| **Accept their offer on the last tick only** (ticks_left 1) | accepting from ticks_left 2 pre-empts their acceptance of our final: −0.03 to −0.05 |
| **Seller asks day 10, buyer day 0** | seller day 0: −0.04. A tie even if every rival is day-aware (0.33 vs 0.33) |
| **Silent rival: walk the price down from half-time** (rounds stay 0) | +0.01, from P and Q |
| Accept mid-duel at ≥ 0.9 × our standing offer | flat from 0.7 to 1.0 |

**Expected share per duel [L]** (my model; 3,000 draws per team; paired SE of a difference ≈ 0.01):

| Policy | Base | 10% missed | 25% missed | Pooled rivals | No deadline accepts | Earlier-data fit | All day-aware | Deal rate |
|---|---|---|---|---|---|---|---|---|
| **XC, Lab openers 0.73 / 0.37 (recommended)** | **0.36** | 0.36 | 0.35 | 0.27 | 0.24 | 0.36 | 0.30 | 0.82 |
| XC, higher anchors 0.9 / 0.6 | 0.38 | 0.37 | 0.36 | 0.29 | 0.26 | 0.38 | 0.33 | 0.80 |
| Lab set C (code) | 0.30–0.31 | 0.31 | 0.31 | 0.24 | 0.21 | 0.30 | 0.27 | 0.83 |
| Lab FINAL file (LLM proxy) | 0.28 | 0.28 | 0.29 | 0.23 | 0.22 | 0.27 | 0.24 | 0.84 |

- **In P per duel (base):** XC 0.73 / 0.37 = 20.5, XC 0.9 / 0.6 = 22.6, C = 17.3, FINAL file = 15.9.
- **Missed ticks are a small cost for XC:** it sends 2–3 messages a duel and keeps a spare tick before its final.
- **Two ticks are fragile:** the final at ticks_left 3 and the accept at ticks_left 1. Keep both in code. With an LLM
  in the loop, move the final to ticks_left 4: it costs ≈ 0.

**Run-ready spec** (it maps onto `policy.py`, but the closing differs from `CLOSING_TICKS` / `MONO_END_SHARE`):

```json
{"OPENER_SHARE_SELLER": 0.73, "OPENER_SHARE_BUYER": 0.37, "OPEN_WAIT": 0, "MID_DUEL_STEPS": "none",
 "ACCEPT_RATIO": 0.9, "SILENT_WALK": {"from_share_of_ticks_left": 0.5, "floor_share_of_limit": 0.08, "by_ticks_left": 2},
 "FINAL_AT_TICKS_LEFT": 3, "FINAL_CONCEDES_SHARE_OF_GAP": 0.55, "FINAL_MIN_MARGIN_SHARE": 0.03,
 "ACCEPT_BY": 1, "SMALL_GAP_ACCEPT": false, "LATE_SWITCH_LEFT": 0, "DAY": {"seller": 10, "buyer": 0}}
```

## 4. Cross-check with the Duel Lab (read after the model above was done)

**The Lab's sets in my simulator.** Its code policy, re-implemented from `origin/duelist-loop` (`policy.py` + the
runner's closing rules):
- **The ranking matches the Lab's:** C 17.2 P > A 16.7 > today 16.3 > FINAL file (LLM proxy) 15.8 > today LLM 15.6.
- **`MONO_END_SHARE` 0.5 on C:** 16.0 P, below 0.25. Same direction as the Lab.

**My policy inside the Lab's simulator.** `tools/duel_sim_v2.py`, imported read-only, its RW worlds, share scoring H1:

| | Lab C | Lab FINAL file (LLM) | XC 0.73 / 0.37 | XC 0.9 / 0.6 |
|---|---|---|---|---|
| R1, Lab's rival mix (66% reply / 17% clock) | **0.434** | 0.405 | 0.420 | 0.415 |
| R1, my measured mix (35% reactive / 41% message while we're silent / 18% sparse / 6% silent) | 0.426 | 0.399 | **0.435** | 0.427 |
| R4 day-aware, Lab mix | **0.355** | 0.339 | 0.330 | 0.322 |
| R4 day-aware, my measured mix | **0.347** | 0.332 | 0.342 | 0.331 |
| Mean of the 5 RW worlds, Lab mix | **0.417** | 0.392 | 0.403 | 0.385 |

- **By rival kind (R1):** XC beats C against "clock" rivals (0.479 vs 0.431) and loses against "reply" rivals (0.394
  vs 0.432).
- **In P, the Lab's simulator also prefers XC:** 23.7 vs 22.8 in R1.

**Where the models disagree, and what the data support:**

1. **How many rivals keep conceding while we're silent: the crux.**
   - **Measured per team [V]:** C, G, H and L send a message on 85–99% of ticks after we stayed silent. A, B and M
     send periodically (17–39%).
   - **Their concessions continue on those ticks [V].** Mean step per message after a silent tick: C 0.054, A 0.052,
     M 0.026, G 0.024 u.
   - **Natural experiments [V]:**
     - 5652 (C): we sent 2 offers and the rival walked from 0.87× to 1.56× our cost on its own. 52.9 P, our best duel.
     - 6094 (G): silent from t0 to t12 while G went from 0.21 to 0.91 u.
     - 5827 (L): one message, 25.2 P.
   - **Across Duels II deals [V, confounded]:** ≤ 2 of our offers averaged 34.5 P (n = 8); ≥ 5 offers averaged
     12.3 P (n = 23).
   - **The Lab's 17% "clock" understates this.** My tempo model is fitted per team on 136 duels and validated out of
     sample (message Brier 0.157 vs 0.214 pooled). **Better supported: mine.**
2. **Anchor height.**
   - My model likes higher anchors: seller 0.9–1.1 and buyer 0.9 add +0.02 to +0.04.
   - The Lab's simulator penalises them: −0.02 to −0.06.
   - Our real openers sit around seller 0.5–0.9 and buyer 0.3–0.6. Above that both models extrapolate.
   - **Adopt the Lab's openers (0.73 / 0.37):** inside the data, and robust in both simulators.
3. **Deadline acceptance.** Both models have it (Lab: tau_end; mine: a per-team window).
   - **[V]:** 27 of the 55 rival acceptances came with ≤ 3 ticks left.
   - XC still beats C in my model with deadline acceptance switched off entirely (0.24 vs 0.21), so the
     recommendation doesn't hinge on it.
4. **Calibration.**
   - **Mine:** 0.30 share per duel vs the actual 0.316 for the policy we played in Duels II.
   - **The Lab's:** its own out-of-sample check over-predicted P by 18% (19.1 vs 16.1). Its 12-tick C (0.42–0.43)
     sits well above anything we have scored.
   - **Neither model has seen a 12-tick, 10% session.**

**Net:**
- **Both models agree:**
  - XC ≥ the FINAL file in every world tested;
  - C ≥ A ≥ today;
  - code ≥ LLM.
- **XC vs C:** +0.05 in my model, −0.01 to +0.01 in theirs. The tie-breaker is the rival-tempo evidence above, which
  favours XC.
- **Low-risk path:** the first wave on XC with the gates below; fall back to C if they trip.

**Gates for the first two waves (8 duels with a rival that spoke):**
- deal rate ≥ 0.70: XC models 0.82 and C 0.83, so a drop to 0.70 or below signals rivals that don't take finals;
- rounds per deal ≈ 1.5–2.0;
- no mid-duel message sent;
- the final goes out at ticks_left 3 in every duel.

## 5. Value of per-opponent adaptation (the bot knows the profile at duel start) [L]

The method:
- **Candidates:** 176 policies (random draws, XC variants, the 6 Lab sets).
- **Robust choice:** the best mean over the teams.
- **Per-team choice:** the best for each team.
- **Gain:** the per-team choice minus the robust choice, scored on the team it was chosen for.

| Estimate | Share per duel | P per duel |
|---|---|---|
| In-model (choose on one draw set, score on another of the same fit): upper bound, no estimation error | +0.035 ± 0.009 (SE over teams) | +2.9 ± 0.6 |
| **Cross-fit** (3 random splits of each team's pairs: choose on half A's fit, score on half B's, both ways) | **−0.012 ± 0.012** (teams) / ± 0.003 (folds) | −0.4 ± 1.0 |

- **Profiles fitted on 6–8 duels per team overfit,** and the robust policy is stable across folds:
  - no mid-duel moves;
  - final at ticks_left 3;
  - last-tick accept;
  - seller day 10;
  - silent walk.
- **Agrees with the Lab** (+0.0014, 95% CI +0.0001 to +0.0027).
- **What adaptation is worth keeping is already in the robust policy:** the silent-rival walk (P, Q).
- **Profiles in the JSON:** use them for monitoring and for spotting a new rival type, not for per-team parameters.

## 6. Caveats

- **Day handling is hand-coded** from the day table, since there are only 4 days-duels per team. Day-aware rivals' w
  is taken as our own role means (buyer 4.0, seller 2.3).
- **Pie for share in my simulator = the rival's reservation R** (margin 0). It's a ranking proxy; the absolute shares
  are approximate.
- **Bots may change for Sunday.** Silence at 12 ticks is still free under the rules. A rival that counts our silence
  against us isn't in the data [?].
- **Team links before Duels II are uncertain** for F, J, N, O, P and Q. The profiles lean on Duels II, which has 4
  duels per team.
