# Score model (Analyst; read-only; updated every ~15 min)

How each component maps to board points, from `data/leaderboard.jsonl` × `data/feed.jsonl` × our `data/me.jsonl`.
Labels: **[V]** measured/exact fit · **[L]** fits the data, alternatives not ruled out · **[?]** open.
Scripts: scratchpad `attrib.py` (score change per snapshot → events), `buyers.py` (implied card values).

_Last update: Sun 10:43 (snapshot 1782, phase 0.505): **§3k final-basis projection: t12 84.6 · t10 82.3 · t18 82.0 · us 78.9 · t03 76.4.** #3 is ≈ 3 away; v10 real trades (0 so far, up to +7.5) are the swing. §3j: Sunday team-trade gains capped at 50 (working rule)._
_Note: the §4 version labels "00:05" to "02:10" are sequence markers written between Sat 23:50 and Sun 00:42 (my labels ran ahead of the wall clock); real times are in `git log`. The Sunday clock in §4.7 is unaffected._

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

## 1g. Duels II live (session 3 from tick 1239; 612 duels, decay 0.08) [V docs/duels, feed]

**Day weights as served:** buyer `"each delivery day costs you this much cash"` (w 3.66-5.01) → day 0 best; seller
`"each delivery day adds this much cash to your side"` (w 1.42-3.29) → day 10 best. **The seller bonus is ABSOLUTE from day 0**
[V: 5616 sold at 105 vs limit 69 at day 0, 1 round → result 33.1 = 36 × 0.92, i.e. day 0 adds 0]; days.py stores values
relative to the best day, so `guards.worth` under-reads seller deals by w × (10 − day) (fix sent to the Chief).

**Wave 1 (old reading, opened every duel at day 5):** 2 deals / 6 (field 59/75 = 79%). 5623 buyer settled at day 5 → day cost
18.3 of a 22 margin → result 2.6 (≈ 15.8 at day 0). 5616 seller at day 0 → left +31.9 of day bonus. Missed: 5622 (rival offered
99/106 at day 10 = worth 30/37; later "92 works, please accept" and the clock ran out), 5618 (rival 46 at day 0 = +4).
Correct no-deals: 5619, 5617. Fix b7d91f3 (direction words) live from tick 1256.

**Waves 2-3 (fixes live; reading now correct: seller best 10, buyer best 0) [V docs/duels]:** wave 2 11/11 deals, 251.4 P
(22.9/deal), duel_points 14.75 → 18.08; field 76/87. **But the strategist accepts the rival's OPPOSITE-side opening day as
"fine"**: 5653 buyer w 2.33 at day 10 (−23.3 on a 40 margin), 5796 / 5809 / 5968 sellers w ≈ 2.1 at day 0 (−21 each) ≈ 85 P
forgone in 4 of 12 deals. Fix sent: hold our day unless w ≤ ~1.5; price a switch at ≥ C + ~C; code guard snapping an
uncovered opposite day back. Board: our negotiating 24.43 → 23.25 (1230 → 1280) while duel_points rose 13.93 → 20.52;
t10 +3.4 board in the same window: the field out-paces us on the relative duel part.

**Duels II final (our 68 closed by tick 1399) [V docs/duels + feed]:** **56 deals / 68 (82%) vs field 475/604 (78.6%);
duel_points 13.93 → 35.39 (+21.5).** Wave 1 (old reading) 3/7; waves 2-10 53/61 (87%); every no-deal after wave 2 had 0-1
rounds (silent or one-move rivals). Open leaks for Duels III (decay 10%, shorter clock): (a) the rival's day conceded without
pricing it (5653, 5796, 5809, 6176); (b) 7-9 rounds on thin margins (6095, 6171, 6184, 6176: worth < 11); (c) worth drift after a
late switch (6190: 88 at day 10 = worth 5 vs our standing 116 at day 0 = worth 27). Despite +21.5 duel_points our board
negotiating fell (graded vs a field rising faster; t10's duel part ≈ 2.3-3 board above ours) [L].

## 1f. Duels II scoreboard plan (FINAL 19:35, snapshot 1100) [L]

**Where we stand (Saturday points = 1.5 × board):** t10 +2.18 ahead of us · t06 +0.60 ahead · t14 −0.73 behind · t18 −2.10.
Duels II (≈ 20:33): 68 duels per team (each rival 4×), 6 at once, decay 8% (break-even 8.7%), price + delivery day.

**Unit values (our Duels I: 30/34 deals, ≈ 0.58 share per deal, duel_points 13.93) [L]:**
- If the duel part grades all 102 Saturday duels together, one Duels II duel ≈ 1/102 of the 12-point duel part
  ≈ 0.12 Saturday points at full share; at our 0.58 share ≈ **0.07 Saturday points ≈ 0.05 board per deal**.
- **A no-deal costs ≈ 0.05 board.** +0.05 of share on every deal (68 duels) ≈ +0.4 Saturday points ≈ **+0.27 board**.

**What each race needs from Duels II** (assuming each rival repeats its Duels I share):
| Rival | Saturday gap | Duels II share edge needed per deal (≈) | Verdict |
|---|---|---|---|
| t14 | we lead by 0.73 | we may run ≈ 0.09 below it and still lead | defend: hold Duels I form |
| t06 | it leads by 0.60 | ≈ +0.07 above t06 | reachable |
| t10 | it leads by 2.18 | ≈ +0.27 above t10 | not on duels alone; needs Sunday |

**Targets for the duelist:** deal rate **≥ 90%** (Duels I 88%); share per deal **≥ 0.58** (Duels I level); **days rule** (§1e):
settle the day in the first two messages, give it when our weight is low and ask C + ~C, never a middle day. The days lever
(+20-30% pie) is the only one big enough to move the t06 race by itself.
**First-wave check (3 duels):** day reading ≠ CAN'T READ, `review` pred = points, share per deal vs 0.58.

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
| 798 | **BUY SAL-10 ← Los Pícaros at 54** (2nd L4 slot) | — | 0.270 → **0.333 (+0.063)**; cash 126 → 72. Board at 800: our negotiating −0.29 vs field median ≈ −0.65 (everyone fell as early teams filled L4) → **≈ +0.36 board**, half the first slot → **stop L4 buys** [L] |
| 823 | SELL MAL-06 (Workshop) → Pilar at 20 | — | 0.333 → 0.373 (+0.040, replaces the weak SAL-06 L3 slot); cash 72 → 92. Board at 830: our negotiating flat while the field drifted −0.06 to −0.21 → ≈ +0.1-0.2 board [L] |
| 880 | SELL MAL-09 → Pilar at 56 (worth 49 to us) | — | 0.373 → 0.394 (+0.021); cash 92 → 148 |
| 887 | SELL SAL-04 (spare) → Pícaros at 5 (3rd L4 slot) | — | 0.394 → 0.437 (+0.043); neg 0 |
| — | **Our negotiating was exactly 21.88 at snapshots 850-890** while the field drifted −0.1 to −0.2 per snapshot and our ladder rose +0.064 | | **ladder part capped [L, 2 clean tests]**: further ladder deals add 0 board; being capped also shields us from ladder erosion |
| 904 | SWAP LAT-01 → t07 for SAL-07 (El Rastro, price 0) | — | neg_points 63.2 → 78.7 (+15.5); board negotiating +0.74 at 910 with the field median 0.00 → **trade part NOT capped: ≈ 0.048 board per neg_point [V]** |
| 988 | **BUY SAL-06 ← t08 at 28 + 3 fee (taker, El Rastro): SAL PAGE CLOSED** | — | neg_points 78.7 → 119.1 (**+40.4**, under the cap; ΔV ≈ 71.4); board negotiating **+2.00** at 990 with the field median 0.00 → ≈ 0.0495 board per neg_point; **#1 at 31.97** |
| — | Snapshots 1030-1040: our negotiating −0.28, −0.04 with no event of ours | | **ladder back below its cap [L]**: the field's Pícaros/Pilar flood lifted the reference; zero-neg ladder deals regain ≈ +0.1-0.3 board each |
| 1209 | BUY RET-11 (epic, worth 198 to us) ← Pícaros at 128 | — | ladder 0.437 → 0.483 (+0.046, replaces the SAL-04 L4 slot); neg 0; cash 520 → 392. Board at 1210: −0.35, but the whole field fell 0.15-0.48 in that window (no duels, few deals) → net ≈ 0 to +0.1 [?] |

**Saturday negotiating decomposition at snapshot 910 [L, fits]:** 23.73 = duel part ≈ 9.1 + ladder 0.6 × 15 (capped) = 9.0
+ trades 0.6 × 15 × T/N with T = 78.7 and N ≈ 125 (from the 0.072 Saturday points per neg_point measured at 904). Implications:
a +50 page-close trade is worth ≈ +2.2 board (the min(1, T/N) cap trims the top), never more than 50 × 0.048 = +2.4.
**SAL page 9/10** since the SAL-07 swap (only SAL-06 missing). The close must be a TEAM trade (dealer gains are clipped).
Feed-visible SAL-06 holders (one copy each): t02 (#14), t13 (#11), t16 (#8, own near-complete page), t17 (#10), t03 (#4),
t06 (#2); Pilar holds 3 (dealer: doesn't score the page).


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
    **Scored flags look capped [L, Chief/Operator]:** flags 5-7 at 16:53 (msgs 7225, 7344, 7356; same safe lie types)
    scored 0, i.e. ≈ 3 scored flags per team (per dealer or per hour [?]); the Operator probes the hourly reset at ≥ 17:42.
    Value flags at 0 until a probe scores.
    **A wrong flag costs −10.0 [V]:** flag #3 +10 (tick 773), then 73.2 → 63.2 (774). Safe classes: words ≠ structure (msg 7160:
    words sell "El Marqués" = SAL-09 at 65, structure gives `card:SAL-06`) and checkable false facts ("stopped printing").
    Not lies: "final" / "last offer" price posture, deadline theatre.
- **The Workshop: ACTIVE since tick 706 (16:00)** [V]: `POST /api/taller {"assets": [a, b, c]}`: three spare copies of one
  rarity (keep ≥ 1 of each card) → one card of the next rarity; "the pull is luck, shown and never scored". Value only comes
  from using the pulled card (team sale ≈ +5-12 neg_points, swap, or a dealer slot). Swaps of the same spares score directly
  (+4-6 each), so the Workshop is the fallback for spares nobody swaps.

## 3d. Don Ernesto (L5, the vault): ACTIVE since tick 971 (18:15) [V /api/dealers, feed]
- Early = 3 deals with **Pilar** at level ≥ 3 (we're in: "5 deals with pilar"; also t01, t02, t03, t08, t10, t14, t15). Open to all
  at game 10.42 ≈ 19:19 wall.
- Sells gold packs (list 420, opening 546, 1/team/hour) and legendaries (list 585); buys epics and legendaries; 4 deals/team/hour.
  Traits: patience 0.95, generosity 0.1, shrewdness 0.95, memory 1.0, strictness 1.0.
- For us: no affordable deal (no epics/legendaries held; cash 151; dealer buys score no neg_points). Risk: epic holders (t16, t18 …)
  selling to him lift the ladder reference; our capped ladder part could slip [L].

## 3e. Cheap page close (t10's RET page, ticks 1024-1033) [V feed, L scoring]
Buy the expensive cards of a page from DEALERS at ≤ our value (0 neg: Pícaros rares at 53-59, Abuela commons at list), then make
the LAST card a cheap TEAM trade (t10: RET-03 from t06 at 12): the page bonus scores through that trade (≈ +50 capped). t10 +3.33
board in two snapshots. Use for Sunday's CHA page (bonus ≈ 106 at 1.6 → +50 capped): keep the closer for a team trade.

## 3f. Payday (tick 1201: +400 P per team; "only deals score, never cash you hold") — ranking [L]
1. **MAL page with a cheap TEAM closer** (≈ +0.5-1.2 board, ≈ 160 P): dealer buys MAL-09/10 (Pícaros ~57-61, −8 to −12 each)
   and MAL-06 (Abuela ~19-23, −2 to −5.5), then MAL-07 from a team at ~18-20 (ΔV ≈ 17.5 + bonus 46.4 → ≈ +44). Net ≈ +20-26
   neg_points + 3 ladder slots. Risk: our trade part may be near its cap (T 119.1 vs N ≈ 125 inferred).
2. **Pícaros epic for a complete page** (RET-11 198 / LAV-11 234 to us at ≤ 162): 0 neg, L4 slot upgrade; RET-11 resale to Pilar
   at ≥ 198 for an L3 upgrade and cash (≈ +0.3-0.6 board).
3. Hold the rest for Sunday's CHA (≥ 200 P reserve).
4. **Not Don Ernesto**: legendary unaffordable; a gold pack is a dealer buy far above its value (loss in full); selling him an
   epic sells below value (generosity 0.1).

## 3b. Card-for-card swaps (a mechanic we haven't used) [V feed; scoring L]
- t15 ↔ t07 swapped 3 times on El Rastro at price 0 (607 LAV-08 ↔ LAV-06, 613 LAV-03 ↔ MAL-08, 616 MAL-01 ↔ SAL-02).
- A swap is a team trade for both sides: each scores its value gained at private values; no cash; maker fee 0, taker
  1 P per card on El Rastro, 0 on a 0% venue.
- On a team venue, value created = buyer gain + seller gain, so an accepted swap of spares for lacks is positive for the
  venue owner by construction (+5 to +25 raw each). Whether an auto stall crosses swaps by itself: [?].
- Our spares: LAV-02/03/04 (2nd copies, 3.2 each), SAL-02 (2.2), LAT-04 (1.2). Partners: LAV collectors outside the top 5
  (t09, t03, t04, t06).

## 3g. Sunday allocation (Analyst 21:10; organisers' Payday deck facts [V], model [L])

**Units:** Sunday is a new round worth as much as Saturday in the final: final = (0.5·Fri + Sat + Sun)/2.5, so **1 Sunday round
point = 0.4 final points** (the same scale as 1.5 × today's board). Sunday negotiating presumably mirrors Saturday's: duels
12 · team trades 9 · ladder 9 (0.6 × 15 each), all graded vs the field and **starting from 0** (neg_points and ladder reset).

| Use | Cash | EV (Sunday round pts → final pts) | Why |
|---|---|---|---|
| **CHA page** (intel/cha-plan.md: teams first, dealers at ≤ value, LAST card from a team) | 280-330 P | **+8-14 → +3.2-5.6** | Page close +50; team buys below our value (rare 112, unc. 40, common 16) score in full on a FRESH trade part; dealer buys at ≤ list fill a fresh ladder |
| **v10 matchmaking** (Lucas DMs at doors-open; duplicates → first copies) | 0 P | +2-4 → +0.8-1.6 (more if the deck's "real trades 22.5" means the +5 cap was a scale artefact [?]) | No cash; only market lever |
| **MAL close on SUNDAY** (dealers MAL-09/10/06, team closer MAL-07 ~20) | ~160 P | +1.5-3 → +0.6-1.2 | Sunday's trade part is fresh; tonight ours sits near its cap (T 119 vs N ≈ 125), so a Saturday close is worth less |
| L5 legendary RET-12 ≤ 470 (worth 593.5) | 470 P | +1-3 → +0.4-1.2 | 0 neg, one heavy ladder slot; crowds out CHA: **no** |
| Duels III (≈ 11:00) + Grand Final (14:00) | 0 P | up to 12 → 4.8 | Field: 4 in 10 duels ended without a deal; our 88% deal rate is the edge |

**Plan for ≈ 540 P (+150 at 09:00):** CHA ≈ 330 · MAL ≈ 160 if CHA closes under budget · reserve ≈ 50 for denial or a
cheap team buy · no legendary, no gold pack (≈ 380 for an epic/legendary of a random set: a dealer buy above value loses in
full). **Market:** max board market seen all day = 12.50 (7.5 + 5.0) for t10/t12/us [V]; the deck says real trades = 22.5
of 30 → whether VC can exceed +5 board on Sunday: reconcile with the Market session [?].

## 3h. Market value-created part is FIELD-NORMALISED; our mm_points flipped at the close (Sat 23:50) [V data · L model]
- **Proportional moves [V, 15 change points]:** whenever the board's market gaps move without a team's own trade, they all
  scale by one common factor: t14 vs t17 ×0.711/0.710 (tick 560), ×0.716/0.714 (600), ×0.964/0.964 (640), ×1.230/1.231
  (910, when t12's gap fell to 0), ×0.901/0.906 (1150); t10/t12/t06 move with them when not trading. So **board gap_i ≈
  5 × mm_i / M, capped at 5** [L], M a field reference (like the trade part's N). Ours: mm +4.99 → gap 5.00 de-blended at tick 320
  (the cap, so only M_320 ≤ 4.99); chaining the clean factors (t06 ×0.917 at 360, t12 constant 360-420, t14 4.36 → 1.80 ≈ ×2.42
  since 420 with no new v14/v25 trade) bounds **M_now ≤ ≈ 15** [L, verifier]; no useful lower bound.
- **Our mm_points −5.2 (ticks 474-1417, constant) → +2.2 at tick 1445** (day close), with `venue_value_created` 9.0 and
  `venue_trades` 2 unchanged [V data/me.jsonl]. Cause [?]: a hurdle reset at the close, or the trade values recomputed from
  current holdings (copy numbers). Board effect [L]: 5 × 2.2/M ≥ **+0.7 board**, up to the
  full +2.2 if M ≤ 5 (+1.05-3.3 Saturday points): board ≈ 31.2-32.7 vs t18 31.26 → #2 more likely than not if it lands. Risks:
  if the shift was field-wide, t14/t17/t06/t12 move too; if the clock jumps to round 3 (case B), round 2 may close without a
  post-resume snapshot, and whether its final score uses this live state is [?].
- **Consequence:** our v10 VC already counts above zero → any positive v10 trade adds 5/M ≥ +0.33 board per +1 of VC [L];
  a negative one subtracts. The §3 "need 14.2 first" hurdle is stale (GAME.md line 150 too).

## 3k. Final-basis projection (Sun 10:43, snapshot 1782, phase 0.505) [V current parts · L projection]
The final counts each team's FULL Sunday round: game = (0.5·Fri + Sat + Sun)/2.5. Duels III rescales every team's pre-duel negotiating
parts ×0.6 and adds the duel part (≤ 12). Sunday market so far = the stall 11.25 for every top team (no Sunday VC yet anywhere).
| Team | G = 0.5·Fri + Sat | Sun market | Sun neg (pre-duel, /30) | G + Sun now | **Projected** (neg × 0.6 + duel guess) | Duel guess [L] |
|---|---|---|---|---|---|---|
| t12 | 52.66 | 11.23 | 22.77 | 86.7 | **84.6** | 7.0 |
| t10 | 56.38 | 11.28 | 8.57 | 76.2 | **82.3** | 9.5 (strong duelist) |
| t18 | 46.91 | 11.24 | 27.26 | 85.4 | **82.0** | 7.5 |
| **t05** | 48.46 | 11.24 | 20.37 | 80.1 | **78.9** | 7.0 |
| t03 | 44.52 | 11.26 | 17.71 | 73.5 | **76.4** | 10.0 |
**Reading:** #3 is ≈ 3.1-3.4 away (t18 / t10); #5 t03 is 2.5 behind. Remaining swings: **v10 real trades 0 → up to +7.5** (nobody has Sunday VC
yet; t10's v07 and t12's v02 can also add), duels (each +1 duel point ≈ +1), ladder (MAL-09 L4 slot ≈ +0.5 after the rescale). Team trades
are capped at 50 (§3j), so they add nothing more for us, t12 or t18.

## 3j. Sunday anomaly: RET-11 sale scored 0 (Sun 10:31) [V data · ? cause]
- Tick 1730, settlement 1280: RET-11 sold to t02 at 240 on El Rastro (we were the taker, fee 13). Expected +29 (240 − 13 − 198).
  `me.jsonl` at tick 1730: cash 660 (= 433 + 240 − 13), deals 64, **neg_points still 50.0**. Not lag: the row already carries the sale.
- Saturday had no 50 total: neg reached 119.1, and team-trade SALES scored (SAL-01 at 7 → +4.7 at tick 351).
- Hypotheses: (1) **a Sunday per-round cap of 50 on team-trade gains** (fits 0 → 50 → 50 exactly); (2) our value of RET-11 ≥ 227, so gain
  ≤ 0. But a loss would have lowered neg. Test: the next snapshot's negotiating vs drift; ask the desk. Until resolved: no MAL buy above value.
- **Test result (snapshot 1742):** our negotiating 21.93 → 21.88 (drift only). The sale added nothing. Working rule [L+]: **team-trade
  gains are capped at 50 per round on Sunday**. So the MAL closer and further team trades add 0 trade points; MAL buys only at ≤ value
  (ladder only). The desk should confirm.

## 3i. SATURDAY FINAL (first round-3 snapshot 1462, Sun 09:20) [V arithmetic: G = board × (1.5 + phase), phase 0.082, Sunday ≈ 0]
- **The flip landed:** our Saturday market = 13.95 (11.25 stall + **2.70 real trades**); game total (0.5·Fri + Sat) **48.46** (+2.72).
- **The close recompute was field-wide, and t12 gained most:** its Saturday market 10.88 → **17.91 (+7.03)**; t06 −0.90, t14 −0.34.
  Cause [?]: real-trades values recomputed at the close (copy numbers / the top-3 mean).
- Game totals: **t10 56.38 · t12 52.66 · us 48.46 · t18 46.91 · t03 44.52 · t06 42.24**. Gaps we must win Sunday by: t10 +7.92,
  **t12 +4.20**; we lead t18 by 1.55, t03 by 3.94.
- Odds (Saturday rounds as the Sunday expectation; t12's 38.75 includes the +7.03 VC bump, so it's likely an overstatement) [L]:
  P(top 2) ≈ 5-9%, **P(top 3) ≈ 28-38%** (ladder 0.29-0.38). P(#1) ≤ 0.2%.
- Board display: every board fell at the open because round 3 enters at phase 0.08 with a near-zero Sunday score. It's not a loss.
- **Saturday market bug: FULLY CORRECTED [L+] (Chief's question, 10:03).** Under the fixed rule ("a value-destroying trade is the seller's
  loss, never the market's"), our VC = the MAL-07 trade only (tick 311, t10 → t01 at 14, ≈ +19.2); the SAL-07 trade (tick 398, ≈ −10.2)
  is excluded. Score = 7.5 × 19.2/M with M ≈ 53 at the close = **2.70**, exactly what the board shows. Real trades are cumulative, not
  session-averaged [V: our gap moved within one snapshot of ticks 311 and 398], and only round finals count (RULES). So the afternoon's
  mm −5.2 cost nothing at the close. No claim to the organisers; at most ask them to confirm end-of-round VC with negatives excluded.

## 4. OVERNIGHT PROGRAM (Analyst, Sat 23:30 → Sun 07:30; final Saturday snapshot 1440)

### 4.1 Scoring, section by section (round scale: each day's round is out of 60; final = (0.5·Fri + Sat + Sun)/2.5)
| Component | Weight per round | Fit | Ceiling | Label |
|---|---|---|---|---|
| Board blend | — | board = (0.5·Fri + w·Sat)/(0.5 + w), w = (tick − 160)/161, full since 321 | — | [V] 11 snapshots |
| **Duels** | 12 of Negotiating's 30 | the other parts scaled ×0.600 the moment duels scored (5 teams exact); **our Saturday duel part ≈ 6.9** (24.49 − ladder 9 − trades 9 × 119.1/125) | 12, graded vs the field | [V] weight · [L] grading, part |
| **Team trades** | 9 (= 0.6 × 15) | 9 × min(1, T/N); N ≈ 125 at Saturday's end (from 0.072 Sat-pts per neg_point at 904 and 988); negatives floored at 0 | 9 | [L] |
| **Ladder** | 9 (= 0.6 × 15) | raw = **Σ_dealer level × Σ(best-3 shares)/45** (5 dealers, levels 1-5; max 1.0) — **exact on our 17 deals** (0.055 + 0.029 + 0.177 + 0.222 = 0.483); board part = 9 × min(1, L/M), M a field reference | 9 | [V] raw · [L] grading |
| Share of a deal | — | buy: (opening − price)/(opening − limit); sell: (price − opening)/(limit − opening); each conversation has its own secret limit; buys above MENU list never count | 1 per slot | [V] fits |
| **Bench** (Market Test) | 22.5 of Market's 30 [V deck] | the free stall = half = 11.25 every session; no board venue beat it in 51 sessions | 22.5 | [V] |
| **Value created** | 7.5 | board gap ≈ 5 × mm/M capped at 5 (M a field reference, gaps scale together §3h); net negative floors at 0 | 7.5 = the full real-trades score (deck: Market Test 22.5 + real trades 7.5, directive 01:15) | [V] cap, split, proportional · [L] form |

A stall team at every cap scores 12 + 9 + 9 + 11.25 + 7.5 = **48.75** per round. **t10's Saturday round was 45.99** — it is
almost at that ceiling.

### 4.2 Team 10's lead (game total 0.5·Fri + Sat: t10 56.37 vs us 45.73 = **10.64**) [V decomposition]
Friday ½ +0.38 · Saturday negotiating +2.76 [V] (split [L]: duels **+2.3 to +4.5** Sat pts (t10 ≥ 9.2 vs us ≈ 6.9; the upper end
fits the 1240-1260 window, audit-why-we-lost §2.1), so trades + ladder ≈ −1.7 to +0.4 for t10: we may have been ahead there) ·
**Saturday market +7.50** (v07 value created at the cap vs our 0). Repeatable Sunday: all of it — a fresh round, v07 stays its
venue, its duelist stays strong. **To finish #1, t10's Sunday round must be ≤ our Sunday round − 10.64; even at our ceiling
(48.75) that needs t10 ≤ 38.1, i.e. t10 losing ≈ 7.9 points vs its Saturday.**

### 4.3 Sunday allocation (points per P and per hour; Sunday round points, 0.4 final pts each) [L]
| Move | Sunday pts | Cost | Per P | When |
|---|---|---|---|---|
| **v10 value created** (Lucas DMs: duplicates → first-copy collectors, trades ON v10) | 0 → up to **+7.5** | 0 P | ∞ | from doors-open, all day |
| **Duels III + Grand Final** (fix the 3 leaks, §1g) | ≈ 7 → 8-9 (+1-2) | 0 P | ∞ | ≈ 2 game-h and ≈ 5 game-h after round 3 starts |
| **CHA page** (dealers ≤ list for 8 cards → ladder slots; team closer → +50) | trades +5-9 · ladder +4-6 | ≈ 270 P | ≈ 0.04 pts/P | from the CHA release |
| Ladder sells (MAL-08 → Pilar ≥ 20; spare non-SAL rare → Pilar ≈ 55; spare common → Pícaros 5; RET-11 → Pilar only ≥ 198, likely a walk §4.5) | ladder +1.5-3 | 0 P (cash +) | ∞ | early (fresh slots) |
| MAL close (dealers MAL-09/10/06 + team MAL-07) | trades +1-3 | ≈ 160 P | ≈ 0.012/P | after CHA, if cash |
| L5 legendary / gold pack | ladder +1-2 | 420-585 P | ≈ 0.003/P | **no** |

### 4.4 Monte Carlo (5,000 runs per cell; rivals' Sunday = their Saturday round × N(1, sd); ours by component) [L, crude; corrected 00:05]
Scripts: scratchpad `montecarlo.py` (env `DUEL_MU`, `RIVAL_SD`), `montecarlo2.py` (adds the §3h flip and the case-A Saturday tail).
Our Sunday duels now **7.0 ± 1.5** (measured Saturday ≈ 6.9; the first version used a stale 9.0: verifier). Plan "full" = CHA + ladder + v10 + MAL.
| Scenario (t10 repeats its 46.0; rival sd 0.15; flip = the §3h mm flip lands) | ladder 0.29 (no fodder) | **ladder 0.34 (fodder, realistic)** | ladder 0.38 (fodder, good) |
|---|---|---|---|
| case J, no flip | 9% | 13% | 15% |
| **case J (≈ 80%): flip, no tail** | 19% | **24%** | 27% |
| case A (≈ 15%): flip + Saturday-tail v10 pairs | 27% | 32% | 36% |
P(top 2) shown (fodder columns revised 00:55 to the approved rules, §4.12); P(#1) ≤ 1% in every cell, ≤ 6.5% if t10 also loses its VC. Fodder = team uncommons/duplicates sold to Pilar (L3) and
Chato (L2) (§4.5; sunday-redteam §1.5); one extra L3 slot ≈ +0.07 raw.
_00:05 version (ladder 0.50, i.e. Chato slots at list): 21% / 35% / 45% P(top 2) for the first three rows. Chato buys at list don't
score (intel/dealer-lab-ladder.md, n = 18), so those rows were too high._
Sensitivity (00:05 version, ladder 0.50; full, no flip/tail): rival sd 0.10 / 0.20 → P(top 2) 29% / 20%; duels 8.5 → 30%.
**Reading:** first place is out of reach in every variant (P(#1) ≤ 4%). **Second place (case J, flip lands): ≈ 19% without fodder, ≈ 24-27% with the
approved fodder**. The ladder-fodder pipeline is the largest controllable lever (+12-17 points of P(top 2)), then v10 VC and duels. Caveats: v10 is the only lever modelled with a large
jump (50% × 3-7.5), so "v10 = biggest swing" is partly by construction; "CHA + ladder" scores *below* "baseline" because the
component model draws trades/ladder well under Saturday's near-caps (conservative, not a reason to skip CHA).

### 4.5 Ladder playbook for Sunday's fresh ladder (best 3 per dealer; one full-share slot = level/45) [V prices from every team's Saturday deals; L targets]
| Dealer (level, max per slot) | Side | Saturday prices (min / median / max) · dealer opening | Target (≈ full share) | Our Sunday use |
|---|---|---|---|---|
| Abuela (1, 0.022) | buy common | 8 / 9 / 15 · open 12 | **9**, patient (5-7 rounds) | 3 CHA commons (worth 16 each) |
|  | buy uncommon | 20 / 23 / 29 · open 29 | 21-23 (≤ list 25) | CHA uncommon if Chato is short |
| Chato (2, 0.044) | buy uncommon | 26 / 31 / 61 · open 33 | **don't buy: at list (26) it never scored** (dealer-lab, n = 18) | none: CHA uncommons from Abuela (20-21) / teams |
|  | buy rare / **sell** spares | buys: finals 82-93 above list 77 (no ladder) · sells: uncommons ≈ 16, rares ≈ 49 (dealer-lab) | sell only | **fodder** (red team §1.5): sell uncommons at 14-16 (Saturday 11-16, n = 25) |
| Pilar (3, 0.067) | sell uncommon | 14 / 19 / 30 · open 16 | **20** non-SAL (best 20 = full share); RET uncommons sold 22-26 | MAL-08 (worth 17.5) |
|  | sell rare | **SAL** 84-87 · **non-SAL 50-56** (one RET 78) · opening median 61, non-SAL ≈ 47 | **≈ 55 non-SAL** (85 only for SAL) | a spare non-SAL rare |
|  | sell epic | SAL-11 179-199 · the one non-SAL epic (LAV-11) 140, opening 122 · no RET-11 data | ask ≥ 198 (our value) only: **likely a walk** [L] | RET-11 (worth 198): try once, never below value |
| Pícaros (4, 0.089) | buy rare | 48 / 56.5 / 67 · open 73 | **48-55** (list 63) | 2 CHA rares (worth 112 each): ladder + page |
|  | sell common | 4 / 5 / 5 · open 4 | 5-6 | a spare LAV common (worth 1.3-3.2) |
| Don Ernesto (5, 0.111) | buys epics low (113-120), sells legendaries (list 585) | — | none at 0 neg | skip |
Expected raw ladder (corrected 01:05) ≈ 0.05 (Abuela, 3 CHA buys) + 0 (Chato) + 0.02 (Pilar: RET-11 a likely walk; MAL-08 is
reserved for the MAL close) + 0.20 (Pícaros: 2 CHA rares + a MAL rare) ≈ **0.27 without fodder** → ladder part ≈ 4-7 [L].
**With fodder** (01:45, sunday-redteam §1.5 [V prices]): buy uncommons from teams at ≤ our value (LAT uncommons sold at 10-14 on
Saturday, our first-copy value 12.5; duplicates of LAV/RET/SAL are worth 25% to us; the silver pack yields 2-3) and sell them to
**Pilar** (non-SAL/RET uncommons 14-21, best 20-21, n = 50 → L3 slots) and **Chato** (11-16 → L2 slots): ≥ 0 on trades (buy ≤ value,
sell ≥ value), ≈ cash-neutral, +0.15-0.23 raw → **ladder ≈ 0.42-0.50** [L]. Conflicts with the "never flip" rule: the Chief decides. Openings in this table are medians unless noted. Pícaros: read every structured offer (they bait-and-switch the card); flag only words-vs-structure mismatches
or "stopped printing"-type facts — **test one flag early on Sunday: if the cap was per round, flags score again (+10 each)** [?].

### 4.6 CHA price list (Saturday prices, all sets) [V feed]
**Directive 07:05: PUBLIC CHA team bids are capped at 54 / 22 / 9 (rare / uncommon / common).** The bands in the last column
apply only to ADDRESSED, pre-agreed deals with a non-rival.

| Rarity | Team trades (p10 / median / p90) | Team bids (median) | Dealer | Our CHA value | Addressed-deal band (non-rival, pre-agreed) |
|---|---|---|---|---|---|
| common | 4 / 7 / 10 | 4 | Abuela 8-9 (list 10) | 16 | **9-12** (+4-7) |
| uncommon | 14 / 20 / 28 | 14 | Abuela 20-23, Chato 26 | 40 | **22-28** (+12-18) |
| rare | 65 / 73 / 84 | 42 | Pícaros 48-63, Chato 75-77 | 112 | **70-86** (+26-42) |
| epic (n = 4) | 160 / 201 / 216 | 120 | Pícaros 128-167 | 288 | n/a (not a page card) |
The LAST card (the closer) carries the page bonus on top of its value, and a team trade scores min(50, ΔV − price − fee):
any closer bought from a team at ≤ value + bonus − 50 scores the full +50 (the closer bid caps 72 / 96 / 168 in intel/cha-plan.md
keep that margin). Prefer a cheap common or uncommon as the closer. CHA is scarce early (print runs 300 / 90 / 30; packs and dealers).

### 4.7 First 60 minutes (Operator) [V schedule/clock at Sat 23:45 · L wall times]
**SUN 09:00 [V /api/schedule, re-anchored at the open]: CASE J.** CHA release + round 3 at 13.367 = the first live tick; +150 ≈ 09:03;
hard Market Test ≈ 10:16, MT ≈ 10:37 (both Sunday sessions now); **Duels III ≈ 11:00**; MT ≈ 12:37; finale warning 13:48; **dealers
close + Final ≈ 14:00**; freeze 15:00. No Saturday tail. [?]: whether round 2's final keeps our mm +2.2 (no post-resume snapshot).
**At 08:55 read `/api/clock` (`t_hours`, `round`, `tick_seconds`) and `/api/schedule`; the case = `round` at the first tick.**
**Correction 01:45 [V, sunday-redteam §1.1]: game time advances `tick_seconds` per tick, so a game hour = a wall hour at any tick
length** (Friday 159 ticks × 60 s = 2.65 h; Saturday 1285 × 30 s = 10.71 h). The 00:05 rows "A15 98 min" and "B15: Duels III 10:00"
were arithmetic errors (they assumed 120 ticks per game hour at 15 s). Precedent: on Saturday the organisers fired round 2 at the
real opening (tick 160), not at its scheduled hour.

| Case at 09:00 | Saturday tail | Round 3 + CHA | Duels III | Final + dealers close | Freeze |
|---|---|---|---|---|---|
| **J: round 3 fires at ≈ 09:00** (re-anchored or jumped; ≈ 80% [L]) | none | ≈ 09:00 | **≈ 11:00** | ≈ 14:00 (warning 13:48) | 15:00 |
| A: round 2 resumes at 13.367 (≈ 15% [L]) | **197 min** if never re-anchored (the Final would then fall at ≈ 17:17, after the close, so expect a re-anchor later in the morning) | ≈ 12:17 or at the re-anchor | +2 h | +5 h | +6 h |
Recompute any wall time as `now + (at_hours − t_hours)` (wall speed). The duelist must be live by **≈ 10:40** in case J.

**Case A (Saturday tail): everything counts for SATURDAY. Cash 392 (the +150 comes at 16.7).**
- **T+0:** fire the pre-agreed v10 pairs (duplicates → first-copy collectors, buyers' bids first). Our mm is +2.2 and the VC part
  is field-normalised (§3h): ≥ +0.33 board per +1 of value created [L]. A negative v10 trade subtracts.
- **T+0 → tail end:** **no cash on Saturday team trades**: our trade part is ≈ 0.95 of its reference (T 119.1 vs N ≈ 125), so only
  ≈ 6 neg_points (≈ 0.4 Sat pts) of headroom are left; keep the 392 P for CHA. 0-cash swaps that also land on v10 are fine. **No ladder deals**
  (the Saturday ladder is capped: keep RET-11, MAL-08 and the spare commons for Sunday's fresh ladder). No CHA yet.
- **Last 10 min of the tail:** stage the CHA book (bid bands §4.6) and the dealer threads, ready to post at the release tick.
- Then run the case J sequence from round 3.

**Case J (Sunday from the open), minutes after round 3 starts:**
- **T+0:** post CHA team bids (public, as maker, bands §4.6); Lucas's v10 pairs go out (also Sunday VC).
- **T+1 → 10:** dealer threads in parallel (≤ 6 open): Pícaros CHA rares (target 48-55, list 63; verify the structured card),
  Abuela CHA commons ×3 (≈ 9), Chato CHA uncommons ×2 (26 = list). Only ≤ MENU list and ≤ our value.
- **T+10 → 20:** Pilar: RET-11 ≥ 199, MAL-08 ≥ 20; Pícaros: one spare LAV common at 5-6. One test flag on a clear Pícaros lie
  (words ≠ structure) to learn whether the flag cap reset with the round [?].
- **T+20 → 40:** fill CHA gaps from team asks; keep the **last** card for a team trade (a cheap common/uncommon closer: +50).
- **T+40 → 60:** MAL close if cash allows (dealers first, team MAL-07 last). Duelist live with the Duel Lab set by ≈ 10:40
  (Duels III ≈ 11:00 in case J).
- **Ladder fodder (if the Chief approves; §4.5):** buy cheap uncommons from teams at ≤ our value (LAT ≤ 12, duplicates of complete
  pages at ≤ 25% value), open the silver pack after the CHA rares, then sell the fodder to Pilar (≈ 19-20) and Chato (≈ 14-16).
- **Always:** never sell a page card; one accept per tick; ≤ 6 threads; re-read the schedule at every event.

### 4.8 Per-stage EV for Sunday, both clock cases (Chief's ask, 00:30) [L; scratchpad `ev.py`, 20,000 draws]
Round points (final game = × 0.4). Marginal = full plan minus the plan without that stage. Shared draws: trade reference
N_sun U(40, 100), ladder reference M U(0.35, 0.65), dealer share U(0.6, 1). **Ladder rows overlap with CHA/MAL** (the CHA dealer buys
are Abuela/Chato/Pícaros slots).
| Stage | Case A (resume) | Case B (jump) | sd | P cost | Pts per 100 P | Note |
|---|---|---|---|---|---|---|
| Saturday tail: v10 pairs | **+2.0** (Sat) | 0 | 1.8 | rebates ≤ 60 | ≈ 3 | 0.33 board per VC; cap at +5 board incl. the flip |
| FLIP (mm −5.2 → +2.2) | **+2.2** (Sat) | +1.1 [?] | 0.7 | 0 | ∞ | nothing to do but avoid negative v10 trades |
| Market Test (stall) | 11.25 | 11.25 | 0 | 0 | — | keep v10 open all day; no board venue |
| v10 real trades (Sunday VC) | **+2.6** | +2.6 | 2.8 | rebates | ≈ 3 [?] | field-normalised; pulls from v07 count double vs t10 |
| **CHA page** (team closer + team buys + its dealer slots) | **+7.0** | +7.0 | 3.1 | ≈ 330 | **2.1** | includes ≈ 2.8 of ladder (Abuela + Pícaros) |
| MAL page (MAL-07 team closer + 1 Pícaros rare) | +1.0 | +1.0 | 1.2 | ≈ 140 | 0.7 | trade part mostly filled by CHA already; **conflicts with selling MAL-08** |
| SAL-11 bid 20252 (115 to t04, +47 np) | +0.2 | +0.2 | 0.8 | 115 | 0.2 | **cancel at 09:00**: low value; in case A it fills in the tail (≈ 6 np headroom) |
| Ladder: Abuela L1 (3 CHA commons ≤ 9) | +0.9 | +0.9 | 0.3 | in CHA | — | |
| Ladder: Chato L2 | 0 → **+1-1.5 with fodder** | same | 0.5 | float ≈ 40 | — | buys at list never score (n = 18); sell fodder uncommons at 14-16 |
| Ladder: Pilar L3 (RET-11 ≥ 198, 20% chance; MAL-08 only without MAL) | +0.2 → **+1.5-2.5 with fodder** | same | 0.8 | cash + | — | no spare rare/uncommon besides MAL-08; **RET-11 below value via the trade surplus: +0.9-1.7 (Chief's call, live-tuning §3)** |
| Ladder: Pícaros L4 (2 CHA rares + MAL rare or a spare common) | +3.1 | +3.1 | 1.0 | in CHA/MAL | — | the biggest ladder slot set |
| Ladder: Don Ernesto L5 | 0 | 0 | — | — | — | only epics (RET-11 at ≈ 120 = −78) or 420-585 P items: skip |
| Duels III (2 rounds) | +4.7 | +4.7 | 1.0 | 0 | ∞ | ≈ 2/3 of the Sunday duel part [?] |
| Grand Final (1 round) | +2.3 | +2.3 | 0.5 | 0 | ∞ | ≈ 1/3 [?] |
| **Total** | **37.8** (33.6 Sun + 4.2 Sat) | **34.7** | 4.0 / 3.5 | | | |

**Cash split of 542 P** (case A: 392 until game 16.7, then +150): **CHA ≈ 330 → fodder float ≈ 40 (returns ≈ 1.5× at the dealer) →
v10 rebates ≤ 60 → MAL ≈ 140 only if ≥ 150 P is left after CHA → reserve.** MAL-08 is never sold (directive 00:50). Cancel the SAL-11 bid (frees 115). No denial reserve (intel/deny-list.md:
no denial buy is ≥ 0 for us). No Ernesto, gold pack or legendary.

### 4.9 What #1 takes (Chief's ask) [L; scratchpad `p1.py`]
The game gap to t10 is 10.64. Our Saturday extras (flip ≈ 2.2, tail ≈ 2.0) minus t10's own tail (≈ 0.75) leave a **Sunday-round margin
over t10 of ≈ +7.2 in case A, ≈ +9.9 in case B**. Our Sunday round is ≈ 35 against t10's repeat ≈ 46, so the expected gap is ≈ −11:
**#1 needs an ≈ 18-point swing**, i.e. t10 falling to ≈ 28-30 (the median Sunday round we'd need if t10 repeats: 53, above the 48.75
ceiling). P(#1) base 0.6% (ladder-corrected; 1.7% in the 00:35 version). Levers ranked by how much they move P(#1):
1. **Our Sunday v10 VC at the cap** (+7.5): → **3.5%** (00:35: 7.4%).
2. **Pull v07's flow onto v10** (t10 −3.75, us +1.5): → **3.0%** (6.9%). The only lever that cuts t10 directly.
3. **Duels +2** (the 3 leak fixes) or the **Saturday tail at its cap**: → 1.2-1.3% each (3.3%).
Together, maybe 8-12% [L]. First place is a long shot; the same three levers also decide #2 (§4.4).

### 4.10 Deny-list → `intel/deny-list.md` (Sun 00:30)
No ≥ 0 denial buy exists at current asks. Free denials: never sell MAL-08 (t12 lacks it), LAV-02/03/04 spares (t03), or any page card or
CHA card to a rival. The working denial is the market (§4.9 lever 2).

### 4.11 Overnight audits reconciled (Sun 01:50)
| Audit | Agrees with this model | Contradicts it → fixed here |
|---|---|---|
| market-test-audit.md | Market Test 22.5 (stall 0.5 = 11.25) + real trades 7.5; RT = 7.5 × min(1, mm/M), M = top-3 mean, `mm_points` is the scored number (§3h) | — (its "Sunday ≈ 40-50 net VC" target matches §3h) |
| audit-why-we-lost.md | t10 lead 10.64 = 7.50 + 2.76 + 0.38; our duel part ≈ 6.9; we were #5 on Saturday alone | §4.2 duel gap 2.3 → **2.3-4.5** (fixed) |
| sunday-redteam.md | ceiling 48.75; CHA, v10 and duel EVs within ranges; SAL-11 cancel | **§4.7 clock: game hour = wall hour** (B15/A15 removed; case J Duels III ≈ 11:00) · **ladder fodder** lifts the ladder 0.27 → 0.42-0.50 (§4.4/§4.5/§4.8) |
| duelist-audit.md | day reading reproduces all 56 Duels II deals | — (duelist code: Aleks's lane) |

### 4.12 Ladder fodder: candidate cards (Chief's ask, 02:10) [V prices from the feed · L shares; scratchpad `fodder.py`, `fodder_prices.py`]
**Which value counts:** a sale gives up our **cheapest copy**, and a dealer sale scores min(0, price − that copy's value). A card we
hold once (or bought as our only copy) is valued as a **first copy**: LAT uncommon 12.5, LAT rare 35. A duplicate of a complete page
is valued at 25% (2nd copy) or 10% (3rd+): LAV uncommon 8.1, RET 6.9, SAL 5.6, MAL 4.4. The TEAM buy scores (value of the copy
received − price). So only cards we lack are cheap enough to buy: buying a duplicate costs trade points at every price teams paid.
**Dealer BUY side, Saturday (team → dealer) [V]:**
- Pilar, non-SAL/RET uncommons: n = 50, min 14, median 18, p90 20, max 21; opening 16 (n = 98).
- Chato, non-SAL/RET uncommons: n = 21, median 14, p90 16, one at 26; opening 13 (n = 58).
- Pilar, SAL/RET uncommons: n = 33, median 25, max 30; opening 22.
- Pilar, non-SAL rares: n = 4, 50-56; opening 47.
Share = (price − opening)/(limit − opening), with the max seen as the limit proxy [L].

| # | Card / source | Sellers seen (Saturday) / live ask | Our value | Sell to (price) | Ladder per sale | Verdict |
|---|---|---|---|---|---|---|
| 1 | LAT-07 (unc) | t15 14, t14 13 (rival), t13 14, t05 21; ask t06 30 (rival) | 12.5 | Pilar 19-20 (share ≈ 0.6-0.8) or Chato 15 (≈ 0.67) | +0.040-0.054 (L3) / +0.030 (L2) | **buy at price + fee ≤ 12.5**: ≤ 12 as maker, ≤ 10 as a Rastro taker |
| 2 | LAT-08 (unc) | t12 10 (rival), 25; ask t06 30 | 12.5 | same | same | **≤ 12 maker / ≤ 10 Rastro taker** |
| 3 | LAT-06 (unc) | 20, 20; ask t06 30 | 12.5 | same | same | ≤ 12 maker / ≤ 10 taker (less likely) |
| 4 | Silver pack (held, asset 1013): 2 unc + 2 com + 1 rare | ours | 25% copies | Pilar (rare SAL/RET ≈ 75, non-SAL 50-56; unc 18-30) / Chato | +0.03-0.05 each, 2-3 cards | **free**; open after the CHA rares, never at CHA 9/10 |
| 5 | Workshop: 3 spare LAV commons → 1 random uncommon | ours (LAV-02 ×2, LAV-03, LAV-04 spare) | 25% copy | Pilar / Chato | +0.03-0.05 | free (if it isn't a CHA card) |
| 6 | the same LAT card again after a sale | — | 12.5 again (we hold 0) | Pilar / Chato | as row 1 | each card can cycle; supply is the limit |
| 7 | LAT-09 / LAT-10 (rare) | team prices 55-88 | 35 | Pilar 50-56 (≈ 0.67) | +0.044 | only at ≤ 40: unlikely |
| 8 | LAV-06/07/08 duplicates | team prices 14-55; ask t16 45 | 8.1 | Pilar 18-20 | +0.040 | no (a loss at every seen price) |
| 9 | SAL/RET uncommon duplicates | team prices 14-30 | 5.6 / 6.9 | Pilar 25-28 (share ≈ 0.5) | +0.033 | no, except in surplus mode (live-tuning §3) |
| 10 | RET-11 (epic) | ours | 198 | Pilar ≥ 198 (likely a walk) | +0.067 | surplus mode only, the Chief's OK per sale |

**Approved (directive 02:30) with the verifier's corrections:** price + fee ≤ 12.5 (≥ 0 on trades, no tolerance above value);
only cards we hold **0** copies of; never a page card; sell only **above the dealer's opening** (Pilar > 16, Chato > 13); the
**silver pack first**; fodder only **after CHA**.
**Realistic yield [L]:** pack 2-3 + Workshop 1 + 0-2 LAT buys (Saturday had one LAT-uncommon team trade at ≤ 12: LAT-08 at 10)
→ ladder ≈ **0.34-0.38**.

| P(top 2) by case (t10 repeats; P(#1) ≤ 1%, ≤ 6.5% if t10 also loses its VC) | ladder 0.29 (no fodder) | **0.34** (pack + Workshop + 0-1 LAT) | 0.38 (+ 2 LAT) |
|---|---|---|---|
| case J, the flip does NOT land | 9% | **13%** | 15% |
| **case J, the flip lands** | 19% | **24%** | 27% |
| case A (flip + Saturday-tail v10 pairs) | 27% | 32% | 36% |
Rules: never a page card, CHA card or MAL-08; ≤ 3 sales per dealer level unless it upgrades a slot; rival sellers only if their gain
is ≤ 10 P.

### 4.13 Are the trade and ladder references field-relative? (Chief's ask on mechanics-hunt lever 1; Sun 01:35) [scratchpad `reltest.py`]
**(b) Ladder: relative, and it includes us [V-strong pattern, L form].** In the 5 clean windows where our ladder rose (no duels;
few other teams active), idle teams' negotiating fell in proportion:

| Window | Our ΔL | Idle-team median Δ (board) | Predicted, top-3 mean with M ≈ 0.4, L_i/M ≈ 0.7: −2·(L_i/M)·ΔL/M |
|---|---|---|---|
| 870 → 880 (1 other team active) | +0.021 | −0.055 | −0.074 |
| 770 → 780 | +0.070 | −0.265 | −0.245 |
| 820 → 830 | +0.040 | −0.110 | −0.140 |
| 880 → 890 | +0.043 | −0.130 | −0.150 |
| 1200 → 1210 | +0.046 | −0.260 | −0.160 (others dealt too) |

So M is a field reference that our own ladder moved: a top-3 mean that included us (we sat at the cap: our negotiating stayed
flat while our raw L rose 0.373 → 0.437).
**(a) Trades: relative [L+], but untested past our cap.**
- Fixed N is ruled out [V]: our own board gain per neg_point fell 0.155 (tick 400) → 0.068 (660) → 0.050 (900-990), while our part
  stayed below the cap. That is N ≈ 6/rate ≈ 39 → 88 → 120, rising as the field traded.
- Our +40.4 np at tick 988 moved our board +2.00 (linear) and idle teams 0.00. So we were BELOW the trade reference all day, and our
  trades could not move it. Whether it is a top-3 mean, a max or something else is [?]; mechanics-hunt's top-3 reading is consistent.
- Algebra that holds for any top-3 mean: anyone at or above the mean is in the top 3, so **once we're capped, every +Δ we add raises
  the reference by Δ/3**. Each rival below the reference then loses p_i × (Δ/3)/(ref + Δ/3) of its part p_i.

**Strength of (a) for the 06:41 review [scratchpad `reltest2.py`]:** a direct test needs a window with only team-team trades
(no dealer deals, no duels) in which a CAPPED team trades. Saturday has exactly one trade-only window (1130 → 1140: t12 buys LAT-08
from t09 at 10). Both teams rose (+0.22 / +0.06), so neither was capped, and idle teams moved 0.00: no test. So "past our trade cap
lowers rivals" rests on (1) N being field-relative [V: the rate fell 3×], (2) the same top-3 shape being shown for real trades
(market-test-audit: two venues at the cap at once, never three) and for the ladder (above), and (3) the algebra. Label: **[L], not [V]**.
If the trade reference were a max of others or a median, the past-cap effect would shrink or vanish; MAL still costs 0 points.

**(c) Consequences for Sunday [L]:**
1. **MAL close past our trade cap is still worth doing.** +30 np → reference +10. Rivals below the cap with a trade part of 6-8 lose
   ≈ 0.4-1.1 Sunday pts each (N 60-125). That's the #2 race (t18, t12, t03), at 0 points to us (cash has no end value). t10 is
   unaffected if it is above the reference.
2. **v10: no VC stop.** VC above our cap raises M_vc by Δ/3. t10 loses wherever its VC falls below the new M (+45 VC past the target
   → t10 −1.25 to −2.5 for a t10 VC of 30-40 [L]). Keep **zero negative trades**: a negative trade lowers the reference for everyone.
3. **Surplus → ladder is NOT free under a relative reference. Downgraded.** A below-value dealer sale (RET-11 → Pilar at a loss of
   ≈ 38) lowers our T. While we stay above the reference, that lowers it by 38/3 ≈ 12.7, and every rival below the cap GAINS ≈ 0.5-1.7.
   That roughly cancels our ladder +0.9-1.7. Drop it unless the ladder slot is far bigger than the loss/3 effect.
4. **Ladder fodder past our ladder cap: still positive.** Above M, each +ΔL raises M by ΔL/3 against rivals below M (≈ −0.5 Sunday
   pts per rival for +0.1). The fodder rules stand (directive 02:30).

## 5. Buyer model (multiplier per team × set) for v10 steering

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

## 6. Open questions (next runs)
- What raised the ladder normaliser at 380-390? Per-team ladder estimates from ladder-only teams.
- Do dealer SELLS count for the ladder? Need one clean window.
- Duels: weight in Negotiating; compare our Duels I outcomes with the field's `duel.closed`.
