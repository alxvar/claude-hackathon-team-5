# Score model (Analyst; read-only; updated every ~15 min)

How each component maps to board points, from `data/leaderboard.jsonl` × `data/feed.jsonl` × our `data/me.jsonl`.
Labels: **[V]** measured/exact fit · **[L]** fits the data, alternatives not ruled out · **[?]** open.
Scripts: scratchpad `attrib.py` (score change per snapshot → events), `buyers.py` (implied card values).

_Last update: Sat 16:54 (tick 784), snapshot 780: **us #1 at 30.02** (t14 29.83, t12 29.12, t01 29.04, t10 28.98, t18 28.61).070 ladder. Duels I post-mortem §1d; Duels II day rule §1e. Rival detail: intel/rivals.md (Analyst-owned)._

## 1. Board = Friday × Saturday blend [V]

- **board = (0.5·Fri + w·Sat) / (0.5 + w)**, w = min(1, (tick − 160)/161), for Negotiating and Market separately.
  Fit on the stall teams' market (11 snapshots, ticks 220-320): the implied w gives (tick − 160)/w = 161.0 ± 0.2 every time.
  Saturday has counted in full since **tick 321**: today the board is **(0.5·Fri + Sat)/1.5**.
- Fri = each team's board at tick 160 (frozen; Fri market = 0 for everyone). **1 Saturday point = 0.667 board.**
- Gap to t13 from Friday alone: (29.94 − 19.99)/3 = **3.32 board, fixed**. Saturday-only Negotiating before Duels I (tick 440):
  t13 21.6 · t02 21.3 · t01 19.3 · t18 19.2 · t14 16.8 · t16 15.3 · t09 13.3 · **t05 12.75** · t04 12.6 · t17 8.8 · t15 8.2 · t03 8.1 · t10 8.1 · t12 8.0.

## 0. Where we stand (snapshot 570, Sat 12:56) — board points [L where split]

| | Friday (/3) | Sat trades+ladder at 460 (×0.6, /1.5) | since 460: duels + new deals | Market bench | Market VC | Total |
|---|---|---|---|---|---|---|
| **us (#3)** | 6.66 | 5.10 | 10.31 (ladder ≈ +4.4, duels ≈ +5.9) | 7.5 | 0 | 29.57 |
| t14 (#1) | 6.02 | 6.71 | 8.44 (incl. Pilar LAT-08 ≈ +2) | 7.5 | 3.10 | 31.76 |
| t18 (#2) | 6.39 | 7.67 | 8.43 (incl. MAL-10 sale ≈ +2) | 7.5 | 0 | 29.98 |

- Gap to t14 (−2.19) = its one v14 trade (VC 3.10) + its pre-duel base (−1.61); we lead on duels + ladder (+1.87) and Friday (+0.64).
- Ladder board rate measured in the 550→560 window (MAL-06 → Pilar, +0.040, +1.67 board vs ≈ +0.2 in duel-only windows):
  **≈ 35 board per 1.0 ladder, still uncapped at 0.181** [L].
- **Value-created grading is relative** [V]: at 570 every VC team fell (t14 11.86 → 10.60, t12 → 10.52, t10 → 12.06,
  t17 → 9.46) when t06's v01 got its 2nd trade (t12 → t08 SAL-10 at 76, tick 556; t06 9.83 → 11.64). No trade on v14 since 418.
- **Clock map after the 13:26-15:30 pause [V]:** game hour = wall − 8.92 h. Benches 15:55, 17:55, 19:55, 21:55 · Salamanca
  fever (Pilar +25% over book on SAL) 18:04-20:04 · **Duels II ≈ 20:34** · close 23:00 (game 14.083); the hard Market Test
  (game 14.65) falls after today's close.

### Update snapshot 600 (13:10): us #5 at 28.96 · t14 30.42 · t12 29.88 · t10 29.51 · t18 29.21
- **t12 market → 12.50 cap** [V]: t14 sold RET-05/02/03/01/04 at 9 as maker on t12's v02 (ticks 591-598) to t09 ×3, t04, t15.
- **Ladder erosion** [L]: snapshot 580, our board −1.07 with duel_points flat; the window's only events were rival Pilar sells
  (t04 SAL-06 24, t09 LAV-06 19). Ladder-heavy t13 slid 5.4 → 4.0 (duel-part column) over four snapshots. Revised marginal
  value of a full-share L2/L3 slot ≈ +0.6-0.9 board.
- t04 sold 7 commons to Abuela at her opening bid 5 (ticks 594-600): cash raise, no ladder [V feed].

## 1b. Duels are 40% of Saturday Negotiating [V, snapshot 470]

- When the first Duels I deals scored, five teams with no duel yet had their Saturday part scaled by exactly **0.600-0.602**
  (t03 8.09→4.86, t10 8.13→4.89, t14 16.76→10.06, t15 8.25→4.96, t16 15.27→9.17).
  **Saturday Negotiating = 0.6 × (team trades + ladder) + duel part**, duel part ≤ 12 Saturday points (= 8.0 board);
  t12 sits at exactly 12.01 → graded against the field's best (max or top-3 mean) [L].
- **Rates after the re-weighting:** 1 neg_point ≈ **0.094 board**; +0.01 ladder ≈ **+0.33 board**; a +50 page close ≈ **+4.7 board**;
  the full duel part = **8.0 board**. The §2 table below is pre-duel (multiply its Saturday points by 0.6).

## 1d. Duels I post-mortem (34 duels, decay 0.06; Analyst 13:30) [V on our records `docs/duels/`, field from feed + board]

**Headline: haggling paid; decay is the cost to cut, not the haggling.**
- Our 34: **30 deals (88%)** vs the field 226/299 = 76% (t11 is silent: 34 no-deals; field without t11 ≈ 85%).
  Sum of results **478.9 P**; raw surplus of our deals 591.0 → **decay cost 112.1 P (19%)**.
- Counterfactual "accept the rival's FIRST in-limit offer": **217.6 P (−261)**. "Accept the rival's best offer as soon as
  seen": 320.5 P (−158). Rivals' first in-limit offers are thin (median surplus 7 P, n = 21); 9 deals closed with the rival
  accepting OUR price and no in-limit rival offer before. The big early offers are the exception: 2531 (S45, taken at r1:
  optimal), 2584 (S31 at r0 → we got S53 at r1: +18.8), 2585 (S64 at r0 → took it at r1: −3.8).
- **Break-even test** (another round pays only if the rival's improvement > S × d/(1−d) = 6.4%): 54 rival moves after an
  in-limit offer, **9 failed (17%)**: 2296 ×3, 2319 ×2, 2318, 2535, 2540, 2585. Small in P.
- **Decay by length** (deals): 0-1 rounds n=9, mean result 25.4, lost 11.7 · 2-3 rounds n=5, 13.2, lost 9.8 · 4-6 rounds
  n=8, 14.6, lost 39.3 · **7-12 rounds n=8, mean result 8.5 of 14.9 raw, lost 51.3**. Rounds track the opening gap: our opener
  was 18 P from the final in 0-1-round deals vs **38 P in 7-12-round deals**.
- Ceiling: the same final prices with ≤ 3 rounds would be 523.0 P (+44, +9%). That's an upper bound: a hard "max 3 rounds"
  cap would have forced thin offers (median S7) or no-deals in the long duels (2460: first in-limit S1 at r6, final S26 at
  r10 → 14.0). **No round cap; and the break-even accept also loses on replay (see levers).**
- No-deals: 2367 (rival stuck at 101 vs our limit 72: correct); 2414, 2415, 2523 (silent rivals, rounds 0: unavoidable).
- Field position [L]: our duel-part column (14.0 at 620) includes ~+5-6 Saturday points of ladder gains since 460, so our
  pure duel part ≈ 8-9.5 Saturday points vs clean teams t01 10.8, t15 ~11. Upper-mid, not top. duel_points 13.93
  (≈ 0.41 per duel, 0.46 per deal).

**Field ranking at the end of Duels I** (snapshot 630; Saturday points gained since 460 net of the 0.6 re-weighting =
duel part + every other deal since 460; full duel part = 12). Only t01 had no other deals, so this ranks Saturday momentum,
not duels alone [V numbers, L reading]:
t05 13.3 (ladder +0.126 inside) · t03 13.1 (MAL-10 sale) · t14 12.5 (Pilar, LAT page, RET sales) · t15 10.9 · t18 10.9
(MAL-10 sale) · t08 10.8 · t07 10.7 · **t01 10.4 (clean)** · t10 10.0 · t16 9.9 · t17 8.1 · t06 8.0 · t02 7.2 · t12 6.9 ·
t09 6.1 · t04 5.8 · **t13 2.1** · t11 0. t13 fell from #2 (snapshot 480) to #7: weak duels plus a ladder-heavy score
eroded as the field copied the dealer-sell play.

**Levers for Duels II (decay 0.08 → break-even 8.7%; price + days)**, expected board points [L]:
1. ~~Anchor closer~~ **REFUTED by Aleks's replay on actual rival offers** (`docs/duels-1-review.md` §2): opener at 60%/75%
   of today's distance → −82.5 P / −42.9 P; the best deals came from rivals that met our ambitious opener. My +0.3-0.5
   board estimate assumed the same final prices with fewer rounds, which the replay shows doesn't hold.
2. ~~Break-even accept rule in code~~ **REFUTED by the same replay**: 447 P vs 479 (−31); rivals' steps are lumpy (a small
   step is often followed by a big one: 2535 −25.8). The 17% "failed" rounds were not losses in practice.
3. **Days (integrative)**: concede days where `your_days_weight` is low, ask price in return; the pie grows only when both
   trade on what each cares about. Largest unknown upside: a 20-30% bigger pie at our share ≈ **+1-1.5 board**.

<details><summary>Per-duel table (34)</summary>

| Duel | Role | Item | Limit | Rival's first in-limit offer (round, price, surplus → value) | Final (price, rounds → result) | Δ vs first |
|---|---|---|---|---|---|---|
| 2296 | seller | El Mesón de la Cava | 87 | r2 @93 S6 → 5.3 | deal 97, r6 → 6.9 | +1.6 |
| 2297 | buyer | El Mesón de la Cava | 175 | r2 @167 S8 → 7.1 | deal 161, r4 → 10.9 | +3.8 |
| 2314 | buyer | El Mesón de la Cava | 75 | none (we closed on the rival accepting ours, or no deal) | deal 68, r1 → 6.6 | +6.6 |
| 2315 | seller | El Mesón de la Cava | 64 | none (we closed on the rival accepting ours, or no deal) | deal 72, r1 → 7.5 | +7.5 |
| 2318 | seller | Palacio de Cristal | 74 | r6 @76 S2 → 1.4 | deal 85, r9 → 6.3 | +4.9 |
| 2319 | buyer | Palacio de Cristal | 97 | r6 @96 S1 → 0.7 | deal 91, r9 → 3.4 | +2.7 |
| 2356 | seller | Café en Goya | 101 | r4 @102 S1 → 0.8 | deal 117, r10 → 8.6 | +7.8 |
| 2357 | buyer | Café en Goya | 92 | r2 @87 S5 → 4.4 | deal 78, r6 → 9.7 | +5.3 |
| 2366 | seller | Palacio de Cristal | 101 | none (we closed on the rival accepting ours, or no deal) | deal 110, r5 → 6.6 | +6.6 |
| 2367 | buyer | Palacio de Cristal | 72 | none (we closed on the rival accepting ours, or no deal) | no_deal -, r5 → 0.0 | +0.0 |
| 2414 | seller | El Mesón de la Cava | 60 | none (we closed on the rival accepting ours, or no deal) | no_deal -, r0 → 0.0 | +0.0 |
| 2415 | buyer | El Mesón de la Cava | 95 | none (we closed on the rival accepting ours, or no deal) | no_deal -, r0 → 0.0 | +0.0 |
| 2430 | buyer | La Heroína del Dos de Mayo | 192 | r2 @184 S8 → 7.1 | deal 184, r3 → 6.6 | -0.5 |
| 2431 | seller | La Heroína del Dos de Mayo | 125 | r2 @134 S9 → 8.0 | deal 134, r3 → 7.5 | -0.5 |
| 2446 | buyer | Mercado de la Paz | 73 | none (we closed on the rival accepting ours, or no deal) | deal 45, r0 → 28.0 | +28.0 |
| 2447 | seller | Mercado de la Paz | 86 | r1 @98 S12 → 11.3 | deal 118, r2 → 28.3 | +17.0 |
| 2460 | seller | La Heroína del Dos de Mayo | 172 | r6 @173 S1 → 0.7 | deal 198, r10 → 14.0 | +13.3 |
| 2461 | buyer | La Heroína del Dos de Mayo | 170 | r6 @170 S0 → 0.0 | deal 150, r12 → 9.5 | +9.5 |
| 2472 | seller | El Mesón de la Cava | 80 | none (we closed on the rival accepting ours, or no deal) | deal 92, r1 → 11.3 | +11.3 |
| 2473 | buyer | El Mesón de la Cava | 94 | none (we closed on the rival accepting ours, or no deal) | deal 88, r1 → 5.6 | +5.6 |
| 2494 | seller | La Heroína del Dos de Mayo | 57 | r1 @64 S7 → 6.6 | deal 74, r2 → 15.0 | +8.4 |
| 2495 | buyer | La Heroína del Dos de Mayo | 124 | none (we closed on the rival accepting ours, or no deal) | deal 107, r0 → 17.0 | +17.0 |
| 2506 | buyer | Palacio de Cristal | 103 | r6 @96 S7 → 4.8 | deal 96, r6 → 4.8 | -0.0 |
| 2507 | seller | Palacio de Cristal | 100 | none (we closed on the rival accepting ours, or no deal) | deal 106, r7 → 3.9 | +3.9 |
| 2522 | seller | Café en Goya | 44 | r0 @52 S8 → 8.0 | deal 59, r7 → 9.7 | +1.7 |
| 2523 | buyer | Café en Goya | 196 | none (we closed on the rival accepting ours, or no deal) | no_deal -, r0 → 0.0 | +0.0 |
| 2530 | seller | Mercado de la Paz | 87 | r2 @97 S10 → 8.8 | deal 97, r2 → 8.8 | -0.0 |
| 2531 | buyer | Mercado de la Paz | 146 | r1 @101 S45 → 42.3 | deal 101, r1 → 42.3 | +0.0 |
| 2534 | seller | Café en Goya | 129 | none (we closed on the rival accepting ours, or no deal) | deal 167, r4 → 29.7 | +29.7 |
| 2535 | buyer | Café en Goya | 219 | r2 @219 S0 → 0.0 | deal 176, r4 → 33.6 | +33.6 |
| 2540 | seller | El Mesón de la Cava | 71 | r1 @73 S2 → 1.9 | deal 90, r7 → 12.3 | +10.4 |
| 2541 | buyer | El Mesón de la Cava | 108 | r2 @104 S4 → 3.5 | deal 87, r6 → 14.5 | +11.0 |
| 2584 | seller | Mercado de la Paz | 122 | r0 @153 S31 → 31.0 | deal 175, r1 → 49.8 | +18.8 |
| 2585 | buyer | Mercado de la Paz | 160 | r0 @96 S64 → 64.0 | deal 96, r1 → 60.2 | -3.8 |

</details>

## 1e. Duels II: the delivery-day rule (code-ready; Analyst 13:40) [L: from the organisers' deck p.7 + RULES; untested]

**Why it pays.** Each side scores its price margin plus its own day value. With linear weights the pie is linear in the
day, so **the efficient day is an extreme (0 or 10): the one the side that cares more prefers**. Deck example: seller +1/day
later, buyer −4/day → pie 50 at day 0, 20 at day 10. Two agents that each hold their own day and meet at day 5 make a pie of
35; the efficient day makes 50 (+43%). Our share of a bigger pie is the lever (≈ +1-1.5 board at our Duels I share).

**Inputs.** `dv = read_days(your_days_weight, days_meaning)` (days.py; values per day, 0 at our best). `b_us = dv.best`.
`w_us = (max(dv.values) − min(dv.values)) / 10` (P per day; linear case). `r0` = the `days` of the rival's FIRST priced
message. Duels II decay d = 0.08 → break-even 8.7%.

**Rule.**
1. **Learn the rival's day before showing ours.** If the rival hasn't sent a price, wait up to 2 ticks: silence costs 0
   rounds (rounds = min(ours, theirs)). A rival opens at its own best day; take `r0` as its preferred side.
2. **No conflict** (`r0` on the same side as `b_us`, or `r0 == b_us`): settle the day there; negotiate price only, as in Duels I.
3. **Conflict.** `Δ = |b_us − r0|`, our cost of taking their day `C = dv(b_us) − dv(r0)` (≥ 0).
   Prior for the rival's weight: `w_r ≈ 2.5 P/day` (deck example 1 and 4; unknown).
   - **We care less** (`w_us ≤ 1.5`, or `C ≤ 0.15 × S_exp`, where S_exp = half the gap between our limit and the rival's
     first price): **give the day at once.** Send `days = r0` with price moved against the rival by a premium
     `π = C + 0.5 × max(0, w_r·Δ − C)` (deck case: C = 10, w_r·Δ = 40 → π = 25; with the prior: π = 17.5).
   - **We care more** (`w_us ≥ 3`): **hold `b_us`** and pay for it: concede price by up to `0.5 × C` over the next rounds,
     never more than C.
   - **In between:** hold `b_us` for the first priced round, then offer `r0` with premium π once. If the rival takes it or
     moves price toward π, its weight is high: keep `r0`. If it moves its day toward ours instead, its weight is low:
     take `b_us` and give price ≤ 0.5 × C.
4. **Never a middle day** with linear weights (it shrinks the pie on both sides). A middle day is right only when a
   weight is a best-day V-shape (`{"best_day": k}`); then the efficient day lies between the two best days.
5. **Read the rival's weight from its replies**: rival keeps its day and concedes ≥ half our premium in price → high
   weight (hold the premium; accept by the break-even rule). Rival moves its day and holds price → low weight (take
   our day).
6. **Guards (unchanged):** `guards.worth(package) = price margin − C(day) ≥ 0`; accept a rival package when its worth now ≥
   our expected next-round worth × (1 − d) (8.7% rule). Answer every duel.
7. **Check at the first wave:** `review`'s `pred` must equal the game's `points` on the first days deals; if not, the
   day reading (or its sign) is off: fix `read_days` before the next wave.

**Expected:** with half the duels in conflict and the rival's weight above ours half the time, giving the day with a premium
lifts those deals' worth by ≈ `0.5 × (w_r − w_us) × Δ` each (deck case +15 P). ≈ +20-30% on Duels II results ≈ +1-1.5 board [L].

## 1c. Duels I (live; session 2 from tick 459, 306 duels, decay 0.06, ends ≈ 13:35)

Duel part = Saturday Negotiating − 0.6 × the team's Saturday part at snapshot 460 (exact for teams with no non-duel events;
t13 and t04 have dealer deals in the window). Full = 12 Saturday points = 8.0 board.

| Snapshot | t12 | t15 | t14 | t09 | t13 | t03 | **t05** | t08 | t17 | t02 | t04 | t07 | t01 | t18 | t16 | t06 | t10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 470 | 12.0 | 0 | 0 | 10.5 | 7.4 | 0 | **6.5** | 10.2 | 5.9 | 6.3 | 6.5 | 0 | 7.9 | 7.9 | 0 | 0.4 | 0 |
| 480 | 12.0 | 10.3 | 9.9 | 8.8 | 8.3 | 8.3 | **8.2** | 7.8 | 7.5 | 7.3 | 6.8 | 6.6 | 6.5 | 5.0 | 4.2 | 3.1 | 2.0 |
| 510 | 11.5 | 11.2 | 6.4 | 7.8 | 5.4* | 10.6 | **11.7*** | 10.9* | 11.3* | 7.0* | 4.9* | 8.0* | 11.9 | 8.9* | 7.9* | 7.0* | 5.0* |

- `*` = the team also had dealer/team deals since 460, so its number includes 0.6 × those (ours: +0.067 ladder from the LAT-08
  Chato and MAL-07 Pilar sells; t17: MAL-10 page close bought from t18 at 70 + 5, pages 1 → 2; t18: that sale).
  Clean teams at 510: t01 11.9, t12 11.5, t15 11.2, t03 10.6, t09 7.8. Nobody sits at exactly 12 now, so the scale is not
  "leader = 12" [L]; it may be absolute (pie share) or graded vs a moving reference [?].
- Deal rate at 510 [V feed]: field 98/111 = 88%; **ours 11/12** (one correct no-deal: 2367, buyer limit 72 vs the rival's
  last 101). Field by item: Mesón 93% · Café en Goya 90% · Mercado de la Paz 88% · Palacio de Cristal 85% · Heroína 82%.
- Our decay bill: 5.75 rounds per duel on average → 0.94^5.75 ≈ 0.70, i.e. **~30% of our surplus lost to decay**.
  Worst: 2318 (9 rounds, 11 → 6.3), 2319 (9 rounds, 6 → 3.4), 2356 (10 rounds, 16 → 8.6). Best: 2541 (6 rounds, 21 → 14.5),
  2315 and 2314 (1 round each).
- The part is relative [V]: t09 10.5 → 8.8 and t08 10.2 → 7.8 while the field closed more deals. Our `duel_points` 0.78 → 2.0
  mapped to 6.5 → 8.2 (not linear) → graded against the leader / top 3 [L].
- Deal rate [V feed]: field 36/39 = 92%; ours 4/4. By item: Mercado de la Paz 11/13, Café en Goya 6/7, the rest 100%.
- Ours (result = surplus × 0.94^rounds): 2296 sell 97 vs cost 87, 6 rounds → 6.9 (31% lost to decay) · 2297 buy 161 vs 175,
  4 rounds → 10.9 (22%) · 2314 buy 68 vs 75, 1 round → 6.6 (6%; the rival had offered 100) · 2540 sell 90 vs 71, 7 rounds →
  12.3 (35%).

## 2. Negotiating (Saturday part) = team trades + ladder (+ duels once Duels I scores)

| Part | Our raw | → Saturday pts | → board | Label |
|---|---|---|---|---|
| Team trades (`neg_points`) | 35.2 | 0.235 per point → 8.3 | 0.157 per point → 5.5 | [L] rate ≈ 0.20-0.235: MAL-03 +2.0 → +0.47 Sat (tick 404); idle teams drifted +0.04-0.06 board in that window |
| Ladder | 0.055 | **≈ 4.5** (≈ 82 Sat per 1.0 ladder point) | ≈ 3.0 | [L] remainder: 12.75 − 8.3 |
| Duels | 0 | — | — | [?] weight unknown; starts with Duels I |

- **Negative `neg_points` are floored at 0** [V]: RET-01 took us −21.5 → +28.5 (+50) but the board showed only +28.5 worth
  (+7.94 Sat at 0.279 then). Independent check: 250→260, our neg_points −19 → −21.5 (tick 253), ladder unchanged, our Saturday part 7.013 → 7.012 [V]. Same signature on t13 before 340 [L].
- **Both parts are relative to the field** [L]: the trade rate fell 0.279 → 0.245 → 0.235 Sat/point (ticks 280 → 360 → 410)
  as others' trade totals rose; at 350 everyone idle rose together when t02 (then a top trader) lost ~15 points on Chato
  buys above list → consistent with a top-3-mean normaliser, capped at 1. Not proven.
- **The ladder normaliser jumped ~70% at snapshots 380-390** [L]: our `ladder_points` stayed 0.055, yet our ladder part fell
  ≈ 7.7 → 4.5 Saturday points (−2.1 board) while the trade rate moved only −4%. Teams fell together (t13 −4.1 Sat,
  t18 −5.3, t14 −5.0, us −3.2). **Not separated from the alternative** (trade normaliser up ~39%, ladder unchanged): it fits
  us and t13 about as well; only the single post-drop trade rate at 404 argues against it, and that is ±20% [verifier].
  t01/t09 are not valid controls (t01 likely trade-capped; t09 made 4 team buys at 380-383); t08 (dealer sells only) stayed
  flat at 1.17. **Cause: [?]** (no Pilar settlement in the public feed for 361-392; settlement ids 447-471 are missing
  from the feed, probably grants/gifts, a dealer deal not excluded).
- **Marginal value of the ladder now** [L]: 4.5 Sat for 0.055 → **+0.01 ladder ≈ +0.8 Sat ≈ +0.54 board ≈ 3.5 neg_points**.
  Our Abuela commons at 9 gave +0.014-0.018 each (≈ +0.8-1.0 board at today's rate) **if they still beat our best three
  at that level** (only the best 3 per level count; RULES).

### Our measured ladder deals today (`data/me.jsonl` + feed thread paths) [V]
| Tick | Deal | Dealer path → close | ladder_points |
|---|---|---|---|
| 185-269 | 5 Abuela buys ≤ list (3 commons at 9, RET-08 22, RET-07 23) | her 12 → 9-10; 29 → 22-23 | 0 → 0.055 (+0.014/+0.018/+0.016, then +0.003/+0.004 as 4th/5th = replacements) |
| 481 | SELL LAT-08 → Chato at 14 | his bids 13, 13, 13, 14, 14 | 0.055 → 0.072 (**+0.017**, first L2 slot) |
| 508 | SELL MAL-07 → Pilar at 19 | her bids 16, 16, 17, 17, 18; she accepted our 19 | 0.072 → 0.122 (**+0.050**, first L3 slot) |
| 522 | SELL SAL-08 → Pilar at 23 | her 22, 22, 22, FINAL 23 after our 34 → 31 → 28 → **23** (one −5 step) | 0.122 → 0.141 (**+0.019**, 2nd L3 slot) |
| 515 | MAL-06 → Pilar: walked | she said FINAL 17 (worth 17.5 to us) | — |
| 551 | SELL MAL-06 → Pilar at 19 | — | 0.141 → 0.181 (+0.040, 3rd L3 slot) |
| 632 / 639 | BUY SAL-06 ← Abuela at 23, then SELL → Pilar at 25 | Pilar SAL opening 22 | neg_points 35.2 → 32.5 (−2.7); ladder 0.181 → 0.188 (+0.007, replaces SAL-08's slot). **Net ≈ −0.2 board**: Pilar's SAL range is wide, 25 is a small share |
| 704 | SELL LAT-08 → Chato at 14 (2nd L2 slot; LAT-08 regained via a swap) | his opening 13 | 0.188 → 0.200 (**+0.012**); our Saturday part +0.28 vs field −0.08 → ≈ +0.24 board → **≈ 20 board per 1.0 ladder, down from ≈ 35 at tick 550** (erosion as the field fills its slots) [L] |
| 709 | Workshop: 3 commons → MAL-06 (uncommon; our first copy again, 17.5 to us) | — | no score (luck) |
| 775 | **BUY SAL-09 ← Los Pícaros at 54** (L4; below list 63; worth 63 to us) | their asks 73, 65 (words "El Marqués", structure SAL-06: the trick), 60 "final", 56; they took our 54 | 0.200 → **0.270 (+0.070, first L4 slot)**; neg 0; cash 180 → 126 Board at 780: our negotiating +0.49 vs field median −0.24 → **≈ +0.73 board** (≈ 10 board per 1.0 ladder) [V/L] |

- **Same card, other teams [V feed]:** SAL-08 → Pilar: t04 25 (opened 40, 6 messages), t10 24, **us 23**; her opening 22.
  Uncommons (non-SAL): t14 LAT-08 20, **us MAL-07 19**, t08 MAL-08 18, t16/t08/t13 17; her opening 16. So a full share at L3
  ≈ +0.06 ladder, and our SAL-08 captured ~1/3 of it: **the big final step (28 → 23) handed her the final** (dealers
  mirror step size; GAME.md Chato note).
- **Erosion [L]:** at snapshot 520 our board fell −0.80 while our duel_points rose 5.02 → 5.35. Five rival Pilar sells in
  509-517 (t16, t08, t14, t10, t08) fit a ladder normaliser rising under us.
- Fits ladder ≈ Σ_level w × mean(best-3 shares) / Σ w, share = (price − opening)/(limit − opening), weights rising with level [L].
- Board value [L]: ≈ 49 Saturday points per 1.0 ladder after the duel re-weighting (≈ +1.6 board for +0.050) **only below the
  field cap**, which pre-duel sat near our ladder ≈ 0.15 ± 0.03 [?]. Not measurable while Duels I runs; measure the first
  isolated ladder deal after ~13:35.

### t13's lead over us (24.39 vs 15.16 = 9.23 board)
| Source | board | Evidence |
|---|---|---|
| Friday (frozen) | **+3.3** | Fri 29.94 vs 19.99 [V] |
| Saturday team trades | **≈ +1.2-3.3** (pre-duel rates; ×0.6 since Duels I) | t13 Saturday part flat at 12.5 from 220 to 330 through every normaliser move that hit traders → t13 trades ≤ 0 (floored) until MAL-10 (tick 331, from t09 at 65 + 5 fee, +10.76 Sat ≈ +43-56 pts at the 0.19-0.25 rates of that time; the window also holds a Chato MAL-08 sell at 14). Est. t13 trades ≈ 43-56 vs our 35.2 [L] |
| Saturday ladder | **≈ +3.6-4.2** (pre-duel; ×0.6 since Duels I) | t13 = 12.5 Sat **from the ladder alone** at 330 (vs our 7.5 then); after the 380-390 cut ≈ 10 vs our 4.5 [L]. t13 never pays a dealer above list; it is the only level-3 team (Pilar since tick 262) |
| Market | t13 3.33 (bench below stall), ours 7.5 | t13 has no value-created and a bad broker [V] |

**Read:** of t13's Saturday edge, roughly 2/3 is the ladder and 1/3 one page-closing trade. The Friday 3.3 can't be recovered;
the ladder can.

### Ladder rule test ("at or below the dealer's MENU list counts, above doesn't") [L, holds on every case checked]
- MENU (`/api/dealers`, keyless): Abuela sells common 10, uncommon 25, pack 26 (opening 30); Chato uncommon 26, rare 77, silver 150; Pilar gold 420. Buy-side lists are not published.
- Ours: 5 Abuela buys ≤ list all moved `ladder_points`; 5 Chato buys > list (87, 86, 30, Fri 93/31) and 1 Chato sale at his opening bid (Fri LAT-08 at 13) never did [V on us].
- t13's Pilar unlock ("3 deals with chato", tick 262) does NOT fit cleanly [?]: before 262 t13 had 4 Chato deals, 2 buys at
  exactly list (LAV-06/07 at 26, Chato accepted t13's number) and 2 sells at Chato's final above his opening (LAT-09 46 vs 39,
  MAL-06 15 vs 13). "≤ list buys + above-opening sells" predicts 4, "below list only" 2; the server says 3. Our 3 Chato buys
  above list unlocked nothing [V]. Friday Chato unlock counts (t98) are ambiguous on whether packs / the welcome price count.
- Dealer SELLS: at the dealer's opening bid they never moved our ladder [V: Fri LAT-08 to Chato at 13, LAV-05 to Abuela at 5,
  ladder stayed 0.064]. Above the opening bid: counts toward unlocks [L: t13's Friday "6 deals with abuela" = 5 buys + its LAT-04
  sell at 6 vs her 5], **and for the ladder [L, n=1, clean window]: t12 420→430, its only event the Chato LAV-06 sell at 14 (his opening 13), t12
  Saturday part +0.885 with the whole field flat** (t12's trade part looks floored at 0, so it was ladder). Pre-duel that was
  ≈ +0.59 board; today ×0.6 ≈ +0.35 board per such sell while it improves the team's best three at that level. Counter-case:
  t13's Pilar sell at 326 (LAV-08 at 19 vs her 16) didn't move t13 (its ladder may have been capped). Opening bids seen: Abuela 5 common / 12 uncommon; Chato 13 uncommon / 39 rare. t13's +2.1 Sat at 350 (two Abuela sells at 6)
  coincided with a field-wide +1.5 drift, so it proves nothing.

## 3. Market = bench + value created on our venue

- **Bench** [V]: the free auto stall scores exactly 7.5 board whatever its efficiency (ours 0.899 → 0.933 in session 2, still
  7.5). Board venues are graded against it: at snapshot 460 (session 2 averaged in) t03 7.5 → 3.61 (replaced its stall by board
  venue v20 "La Celestina"), t13 3.33 → 5.49, t06 8.90 → 9.83. Closing/replacing a venue mid-round is risky.
- **Value created (VC) per trade = buyer's value − seller's value at private values, copy number included** [L+].
  `/api/me` (12:35): `venue.value_created` 9.0 for v10's two trades; `score.mm_points` −5.2.
- **mm_points = value_created − 14.2** [L+: fits both our readings; implies MAL-07 (tick 311) +19.19 and SAL-07 (tick 398)
  −10.19, matching independent estimates +19.4 (t10's duplicate ≈ 3.1 → t01's first copy 22.5) and −10.0 (SAL 0.9 → 0.5)].
  Whether the 14.2 hurdle is fixed or field-relative: **[?]**. Other venues' gaps move without their own trades (t10/t12 → 5.0
  at snapshot 400 when our VC fell), so field-relative is likely [L].
- **Board gap = clamp(mm_points, 0, +5)** [L: +4.99 → market 12.47; −5.2 → exactly 7.5]. Several teams sat at exactly 12.50
  (cap) [V]; negative floors at 0 [V].
- **What v10 needs:** value_created ≥ 14.2 to score at all, ≈ 19.2 for the full +5. Now 9.0 → **+10.2 more**: one
  duplicate → first-copy trade (+15-20) or one uncommon from a 0.5-0.7 holder into a 1.3-1.6 first-copy buyer (+15-27).
  +5 board ≈ 32 neg_points of team trades. A trade where the buyer values the card less than the seller subtracts in full.
- Field gaps' sources [V feed for trades]: t14 +4.36 = v14 tick 418, t15 → t12 LAT-07 at 19; t17 +2.76 = v17 tick 433, t15 → t12
  LAT-01 at 7 (t15 selling duplicates into t12's first copies: [L], holdings are not public); t10 = v07: t05 → t03 SAL-01 (351, we sold), t04 → t05 MAL-03 (404, no visible change: t10 already at 12.5);
  t12 = v02: t13 → t15 MAL-03 (203), RET-02 (234).
- To pin the hurdle: log `score.mm_points`, `bench_points`, `venue.value_created` in `data/me.jsonl` on every change.
- **Our first swap [V]:** tick 669 on t07's v11, our spare RET-04 (2nd copy, ≈ 2.75 to us) for t08's SAL-04 (our first copy,
  9): `neg_points` 32.5 → 38.7 (**+6.2**), board negotiating 20.42 → 20.84 (**+0.42**) at snapshot 670 with the field flat.
  Today's trade rate ≈ **0.068 board per neg_point** (was 0.094 after the duel re-weighting): the trade normaliser keeps rising
  as the field trades.

## 3c. New levels announced at tick 630 (during the pause) [V /api/levels, /api/dealers; reading L]
- **Los Pícaros: ACTIVE since tick 761 (16:35), level 4; WE HAVE THE HEAD START** [V feed `level.unlocked` "3 deals with
  pilar"; rule per `/api/dealers`: early = 2 deals with Pilar]. Open to all at game 8.667 ≈ 17:35 wall. Also early: t02, t03,
  t04, t08, t09, t10, t16. Menu: sells rares (list 63) and epics (list 162); buys commons and uncommons; 6 deals/team/hour;
  traits patience 0.4, shrewdness 0.7, memory 0.3, chattiness 0.8. "Bargains and bad faith: read every offer before you
  accept, and flag a trick (POST /api/flags)."
  - EV per deal [L]: full-share L4 deal ≈ +0.08 ladder ≈ +1.6 board (at ≈ 20 board per ladder point). Best plays: buy a SAL
    rare we lack at ≤ 63 (worth 63 to us → 0 neg) and resell to Pilar in the fever (≈ 87); sell the Workshop's MAL-06 and
    spare commons above their opening at ≥ our value. No epics (cash).
  - **Flags SCORE +10.0 neg_points each [V, n=2]:** a correct flag on a Pícaros lie ("they stopped printing this one
    yesterday"): `neg_points` 43.2 → 53.2 (tick 766), then a repeated lie in a separate message 53.2 → 63.2 (769). Board at
    snapshot 770: our negotiating +0.95 with the field ≈ −0.2 → **≈ +0.57 board per flag** (≈ +0.058 per neg_point). We moved
    to **#2 at 29.53, 0.53 behind t14**. Pícaros lies are public in the feed (t02 763, t08 765, t01 768 got the same lines);
    t02's +0.54 net with no scoring event at 770 fits one flag [L]. Abuela/Chato/Pilar: 3,253 messages, no checkable false
    facts (only "last word" posture and the golden-chulapa egg lore): don't flag them.
    **A wrong flag costs −10.0 [V]:** flag #3 +10 (tick 773), then 73.2 → 63.2 (774). Safe classes: words ≠ structure (msg 7160:
    words sell "El Marqués" = SAL-09 at 65, structure gives `card:SAL-06`) and checkable false facts ("stopped printing").
    Not lies: "final" / "last offer" price posture, deadline theatre.
- **The Workshop: ACTIVE since tick 706 (16:00)** [V]: `POST /api/taller {"assets": [a, b, c]}`: three spare copies of one
  rarity (keep ≥ 1 of each card) → one card of the next rarity; "the pull is luck, shown and never scored". Value only comes
  from using the pulled card (team sale ≈ +5-12 neg_points, swap, or a dealer slot). Swaps of the same spares score directly
  (+4-6 each), so the Workshop is the fallback for spares nobody swaps.

## 3b. Card-for-card swaps (a mechanic we haven't used) [V feed; scoring L]
- t15 ↔ t07 swapped 3 times on El Rastro at price 0 (607 LAV-08 ↔ LAV-06, 613 LAV-03 ↔ MAL-08, 616 MAL-01 ↔ SAL-02).
- A swap is a team trade for both sides: each scores its value gained at private values; no cash; maker fee 0, taker
  1 P per card on El Rastro, 0 on a 0% venue.
- On a team venue, value created = buyer gain + seller gain, so an accepted swap of spares for lacks is positive for the
  venue owner by construction (+5 to +25 raw each). Whether an auto stall crosses swaps by itself: [?].
- Our spares: LAV-02/03/04 (2nd copies, 3.2 each), SAL-02 (2.2), LAT-04 (1.2). Partners: LAV collectors outside the top 5
  (t09, t03, t04, t06).

## 4. Buyer model (multiplier per team × set) for v10 steering

Method: implied ΔV of each team-trade side from its Saturday-part jump ÷ 0.235 (clean windows only) + price/book of bids and
buys (a floor). Every team has the same six multipliers {1.6, 1.3, 1.1, 0.9, 0.7, 0.5} shuffled over CHA/LAV/RET/SAL/MAL/LAT.
No independent validation yet (our MAL-03 buy reads 0.70, but the rate was calibrated on that trade: circular). The −10.19 / +19.19
per-trade values from the mm_points fit (§3) agree with t15 SAL 0.5, t10 SAL ≈ 0.9, t10 MAL 0.5, t01 MAL 0.9.

| Set | High (buy from us / on v10) | Low (sellers, avoid as buyers) |
|---|---|---|
| **LAV** | t06 1.3-1.6 (bid 1.19, paid 1.17, LAV-10+SAL-10 jump) · t09 ≥1.3 (LAV-09 at 89, LAV-04 jump) · t12 ≥1.3 (LAV-06 at 31) · t03 ≥1.1 (bid 1.01) · t04 ~1.2 (paid 1.23) · t14 high (top-4) | **t16 ≈ 0.5-0.7** (sold LAV-10 at 82 in the 370→380 window, which also holds the ladder cut: loss ≈ 36-48) [L] · t02 ≤0.5 |
| **MAL** | t13 1.6 (MAL-10 jump, top-4) · **t17 ≥1.3** (bid MAL-09 85 = 1.21, paid 1.24) · t09 ~1.1 (MAL-07 jump) · t01 ~0.9 (MAL-06 jump) | **t10 ~0.5** (sold MAL-07 at 14, lost 9.9) · t02 ≤0.6 · t15 0.7 · us 0.7 |
| **LAT** | **t15 1.3-1.6** (buys LAT×6; its LAT dups read as 25%/10% copies of 1.3-1.6) · t16 1.1-1.3 (LAT-10 at 91, LAT-09 jump) · t14 1.1-1.3 (LAT-03 jump 1.22; top-4) · t03 ~0.9-1.1 (bid 0.93) | t02 0.5 (bids 0.52) · **t12 0.7-0.9** (LAT-05 9.0, LAT-07 18.7, LAT-01 7.0: it *buys* LAT, but as a ~0.7-0.9 set) · us 0.5 |
| **SAL** | t03 ~0.9-1.3 [?: SAL-01 jump reads 1.37 but t10's v07 gap (4.34, not capped) implies far less; bid 1.06] · t06 1.3-1.6 · t16 ~1.3 (bid 1.11, paid 1.29) · t01 ≥1.1 (bought SAL-10, -07, -08) | **t15 ~0.5** (SAL-07 on v10: 13.8 = 0.55) · t10 ~0.9-1.1 · t12 dumps · us 0.9 |
| **RET** | t18 high (RET-02 at 49, page) · t15 ~1.3 (RET-07 at 24) · t02 ~1.2 | t13 (sells RET at 10-20) |

**Safest high-value pairs for v10** (buyer outside the top 4; seller holds a dup or a low-multiplier copy):
- LAT: **t15's LAT dups → t16 (1.1-1.3) or t03 (~1.0)**. t15 collects LAT, so its 2nd/3rd copies are worth 25%/10% to it;
  that pattern is exactly what fed v14 (+4.36) and v17 (+2.76) through t12.
- MAL: **t10's or our MAL → t17 (≥1.3)**, then t09.
- SAL: **t15's SAL → t06 or t16** (t03 [?], see table).
- LAV: **t16's LAV → t06, t09, t03 or t04**.
- Never as buyers: t15 for SAL, t10/t02 for MAL, t16 for LAV, t02 for LAT; t12 only for LAT dups, never a first copy from a ≥0.9 holder (value created goes negative, see v10 tick 398).

Caveats: a team at the trade cap or floor shows no jump (t01 since ~380 [L], t09/t10 early); windows with ladder moves
(380-390) inflate or deflate the implied values. The CHA multiplier is unknown for every team until Sunday.

## 5. Open questions (next runs)
- What raised the ladder normaliser at 380-390? Per-team ladder estimates from ladder-only teams.
- Do dealer SELLS count for the ladder? Need one clean window.
- Duels: weight in Negotiating; compare our Duels I outcomes with the field's `duel.closed`.
