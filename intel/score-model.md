# Score model (Analyst; read-only; updated every ~15 min)

How each component maps to board points, from `data/leaderboard.jsonl` × `data/feed.jsonl` × our `data/me.jsonl`.
Labels: **[V]** measured/exact fit · **[L]** fits the data, alternatives not ruled out · **[?]** open.
Scripts: scratchpad `attrib.py` (score change per snapshot → events), `buyers.py` (implied card values).

_Last update: Sat 12:12 (tick 481), snapshot 480. Earlier stamps in this file's history (12:15-12:50) were mislabelled; the real times were 11:55-12:08. Rival detail: intel/rivals.md (Analyst-owned)._

## 1. Board = Friday × Saturday blend [V]

- **board = (0.5·Fri + w·Sat) / (0.5 + w)**, w = min(1, (tick − 160)/161), for Negotiating and Market separately.
  Fit on the stall teams' market (11 snapshots, ticks 220-320): the implied w gives (tick − 160)/w = 161.0 ± 0.2 every time.
  Saturday has counted in full since **tick 321**: today the board is **(0.5·Fri + Sat)/1.5**.
- Fri = each team's board at tick 160 (frozen; Fri market = 0 for everyone). **1 Saturday point = 0.667 board.**
- Gap to t13 from Friday alone: (29.94 − 19.99)/3 = **3.32 board, fixed**. Saturday-only Negotiating now (tick 440):
  t13 21.6 · t01 19.3 · t02 21.3 · t18 19.2 · t14 16.8 · t16 15.3 · t09 13.3 · **t05 12.75** · t04 12.6 · t17 8.8 · t10 8.1 · t12 8.0.

## 1b. Duels are 40% of Saturday Negotiating [V, snapshot 470]

- When the first Duels I deals scored, five teams with no duel yet had their Saturday part scaled by exactly **0.600-0.602**
  (t03 8.09→4.86, t10 8.13→4.89, t14 16.76→10.06, t15 8.25→4.96, t16 15.27→9.17).
  **Saturday Negotiating = 0.6 × (team trades + ladder) + duel part**, duel part ≤ 12 Saturday points (= 8.0 board);
  t12 sits at exactly 12.01 → graded against the field's best (max or top-3 mean) [L].
- **Rates after the re-weighting:** 1 neg_point ≈ **0.094 board**; +0.01 ladder ≈ **+0.33 board**; a +50 page close ≈ **+4.7 board**;
  the full duel part = **8.0 board**. The §2 table below is pre-duel (multiply its Saturday points by 0.6).

## 1c. Duels I (live; session 2 from tick 459, 306 duels, decay 0.06, ends ≈ 13:35)

Duel part = Saturday Negotiating − 0.6 × the team's Saturday part at snapshot 460 (exact for teams with no non-duel events;
t13 and t04 have dealer deals in the window). Full = 12 Saturday points = 8.0 board.

| Snapshot | t12 | t15 | t14 | t09 | t13 | t03 | **t05** | t08 | t17 | t02 | t04 | t07 | t01 | t18 | t16 | t06 | t10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 470 | 12.0 | 0 | 0 | 10.5 | 7.4 | 0 | **6.5** | 10.2 | 5.9 | 6.3 | 6.5 | 0 | 7.9 | 7.9 | 0 | 0.4 | 0 |
| 480 | 12.0 | 10.3 | 9.9 | 8.8 | 8.3 | 8.3 | **8.2** | 7.8 | 7.5 | 7.3 | 6.8 | 6.6 | 6.5 | 5.0 | 4.2 | 3.1 | 2.0 |

- The part is relative [V]: t09 10.5 → 8.8 and t08 10.2 → 7.8 while the field closed more deals. Our `duel_points` 0.78 → 2.0
  mapped to 6.5 → 8.2 (not linear) → graded against the leader / top 3 [L].
- Deal rate [V feed]: field 36/39 = 92%; ours 4/4. By item: Mercado de la Paz 11/13, Café en Goya 6/7, the rest 100%.
- Ours (result = surplus × 0.94^rounds): 2296 sell 97 vs cost 87, 6 rounds → 6.9 (31% lost to decay) · 2297 buy 161 vs 175,
  4 rounds → 10.9 (22%) · 2314 buy 68 vs 75, 1 round → 6.6 (6%; the rival had offered 100) · 2540 sell 90 vs 71, 7 rounds →
  12.3 (35%).

## 2. Negotiating (Saturday part) = team trades + ladder (+ duels once Duels I scores)

| Part | Our raw | → Saturday pts | → board | Label |
|---|---|---|---|---|
| Team trades (`neg_points`) | 35.2 | 0.235 per point → 8.3 | 0.157 per point → 5.5 | [V] rate: MAL-03 +2.0 → +0.47 Sat (tick 404, idle field) |
| Ladder | 0.055 | **≈ 4.5** (≈ 82 Sat per 1.0 ladder point) | ≈ 3.0 | [L] remainder: 12.75 − 8.3 |
| Duels | 0 | — | — | [?] weight unknown; starts with Duels I |

- **Negative `neg_points` are floored at 0** [V]: RET-01 took us −21.5 → +28.5 (+50) but the board showed only +28.5 worth
  (+7.94 Sat at 0.279 then). Same signature on t13 before 340 and t07/t09/t10/t11 early Saturday (Saturday part ≈ 0).
- **Both parts are relative to the field** [L]: the trade rate fell 0.279 → 0.245 → 0.235 Sat/point (ticks 280 → 360 → 410)
  as others' trade totals rose; at 350 everyone idle rose together when t02 (then a top trader) lost ~15 points on Chato
  buys above list → consistent with a top-3-mean normaliser, capped at 1. Not proven.
- **The ladder normaliser jumped ~70% at snapshots 380-390** [L]: our `ladder_points` stayed 0.055, yet our ladder part fell
  ≈ 7.7 → 4.5 Saturday points (−2.1 board) while the trade rate moved only −4%. Every team with ladder fell (t13 −4.1 Sat,
  t18 −5.3, t14 −5.0, us −3.2); t01/t09 (≈ no ladder) did not. **Which deals raised the normaliser: [?]** (no Pilar settlement
  in 361-392; candidates: t17's Abuela commons at 8, t15's RET uncommons at 23/25).
- **Marginal value of the ladder now** [L]: 4.5 Sat for 0.055 → **+0.01 ladder ≈ +0.8 Sat ≈ +0.54 board ≈ 3.5 neg_points**.
  Our Abuela commons at 9 gave +0.014-0.018 each (≈ +0.8-1.0 board at today's rate) **if they still beat our best three
  at that level** (only the best 3 per level count; RULES).

### t13's lead over us (24.39 vs 15.16 = 9.23 board)
| Source | board | Evidence |
|---|---|---|
| Friday (frozen) | **+3.3** | Fri 29.94 vs 19.99 [V] |
| Saturday team trades | **≈ +1.5-2.1** | t13 Saturday part flat at 12.5 from 220 to 330 through every normaliser move that hit traders → t13 trades ≤ 0 (floored) until MAL-10 (tick 331, from t09 at 65 + 5 fee, +10.76 Sat ≈ +46 pts, a near-cap page/rare buy). Est. t13 trades ≈ 46-50 vs our 35.2 [L] |
| Saturday ladder | **≈ +3.7-4.4** | t13 = 12.5 Sat **from the ladder alone** at 330 (vs our 7.5 then); after the 380-390 cut ≈ 10 vs our 4.5 [L]. t13 never pays a dealer above list; it is the only level-3 team (Pilar since tick 262) |
| Market | t13 3.33 (bench below stall), ours 7.5 | t13 has no value-created and a bad broker [V] |

**Read:** of t13's Saturday edge, roughly 2/3 is the ladder and 1/3 one page-closing trade. The Friday 3.3 can't be recovered;
the ladder can.

### Ladder rule test ("at or below the dealer's MENU list counts, above doesn't") [L, holds on every case checked]
- MENU (`/api/dealers`, keyless): Abuela sells common 10, uncommon 25, pack 26 (opening 30); Chato uncommon 26, rare 77, silver 150; Pilar gold 420. Buy-side lists are not published.
- Ours: 5 Abuela buys ≤ list all moved `ladder_points`; 6 Chato buys > list (87, 86, 30, Fri 93/31) never did [V on us].
- t13's Pilar unlock ("3 deals with chato", tick 262) does NOT fit cleanly [?]: before 262 t13 had 4 Chato deals, 2 buys at
  exactly list (LAV-06/07 at 26, Chato accepted t13's number) and 2 sells at Chato's final above his opening (LAT-09 46 vs 39,
  MAL-06 15 vs 13). "≤ list buys + above-opening sells" predicts 4, "below list only" 2; the server says 3. Our 3 Chato buys
  above list unlocked nothing [V]. Friday Chato unlock counts (t98) are ambiguous on whether packs / the welcome price count.
- Dealer SELLS: at the dealer's opening bid they never moved our ladder [V: Fri LAT-08 to Chato at 13, LAV-05 to Abuela at 5,
  ladder stayed 0.064]. Above the opening bid: counts toward unlocks [L: t13's Friday "6 deals with abuela" = 5 buys + its LAT-04
  sell at 6 vs her 5], ladder effect unmeasured **[?]**. Opening bids seen: Abuela 5 common / 12 uncommon; Chato 13 uncommon / 39 rare. t13's +2.1 Sat at 350 (two Abuela sells at 6)
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
- Field gaps' sources [V feed]: t14 +4.36 = v14 tick 418, t15 → t12 LAT-07 at 19; t17 +2.76 = v17 tick 433, t15 → t12
  LAT-01 at 7 (t15 sells LAT duplicates into t12's first copies); t10 = v07: t05 → t03 SAL-01 (351), t04 → t05 MAL-03 (404);
  t12 = v02: t13 → t15 MAL-03 (203), RET-02 (234).
- To pin the hurdle: log `score.mm_points`, `bench_points`, `venue.value_created` in `data/me.jsonl` on every change.

## 4. Buyer model (multiplier per team × set) for v10 steering

Method: implied ΔV of each team-trade side from its Saturday-part jump ÷ 0.235 (clean windows only) + price/book of bids and
buys (a floor). Every team has the same six multipliers {1.6, 1.3, 1.1, 0.9, 0.7, 0.5} shuffled over CHA/LAV/RET/SAL/MAL/LAT.
Validation: our own MAL-03 buy reads 0.70 by this method — our true MAL multiplier is 0.7 [V].

| Set | High (buy from us / on v10) | Low (sellers, avoid as buyers) |
|---|---|---|
| **LAV** | t06 1.3-1.6 (bid 1.19, paid 1.17, LAV-10+SAL-10 jump) · t09 ≥1.3 (LAV-09 at 89, LAV-04 jump) · t12 ≥1.3 (LAV-06 at 31) · t03 ≥1.1 (bid 1.01) · t04 ~1.2 (paid 1.23) · t14 high (top-4) | **t16 0.7** (sold LAV-10 at 82, clean: lost 49.9) · t02 ≤0.5 |
| **MAL** | t13 1.6 (MAL-10 jump, top-4) · **t17 ≥1.3** (bid MAL-09 85 = 1.21, paid 1.24) · t09 ~1.1 (MAL-07 jump) · t01 ~0.9 (MAL-06 jump) | **t10 ~0.5** (sold MAL-07 at 14, lost 9.9) · t02 ≤0.6 · t15 0.7 · us 0.7 |
| **LAT** | **t15 1.3-1.6** (buys LAT×6; its LAT dups read as 25%/10% copies of 1.3-1.6) · t16 1.1-1.3 (LAT-10 at 91, LAT-09 jump) · t14 1.1-1.3 (LAT-03 jump 1.22; top-4) · t03 ~0.9-1.1 (bid 0.93) | t02 0.5 (bids 0.52) · **t12 0.7-0.9** (LAT-05 9.0, LAT-07 18.7, LAT-01 7.0: it *buys* LAT, but as a ~0.7-0.9 set) · us 0.5 |
| **SAL** | **t03 ~1.3** (SAL-01 jump 1.37, bid 1.06) · t06 1.3-1.6 · t16 ~1.3 (bid 1.11, paid 1.29) · t01 ≥1.1 (bought SAL-10, -07, -08) | **t15 ~0.5** (SAL-07 on v10: 13.8 = 0.55) · t10 ~0.9-1.1 · t12 dumps · us 0.9 |
| **RET** | t18 high (RET-02 at 49, page) · t15 ~1.3 (RET-07 at 24) · t02 ~1.2 | t13 (sells RET at 10-20) |

**Safest high-value pairs for v10** (buyer outside the top 4; seller holds a dup or a low-multiplier copy):
- LAT: **t15's LAT dups → t16 (1.1-1.3) or t03 (~1.0)**. t15 collects LAT, so its 2nd/3rd copies are worth 25%/10% to it;
  that pattern is exactly what fed v14 (+4.36) and v17 (+2.76) through t12.
- MAL: **t10's or our MAL → t17 (≥1.3)**, then t09.
- SAL: **t15's SAL → t03, t06 or t16**.
- LAV: **t16's LAV → t06, t09, t03 or t04**.
- Never as buyers: t15 for SAL, t10/t02 for MAL, t16 for LAV, t02 for LAT; t12 only for LAT dups, never a first copy from a ≥0.9 holder (value created goes negative, see v10 tick 398).

Caveats: a team at the trade cap or floor shows no jump (t01 since ~380 [L], t09/t10 early); windows with ladder moves
(380-390) inflate or deflate the implied values. The CHA multiplier is unknown for every team until Sunday.

## 5. Open questions (next runs)
- What raised the ladder normaliser at 380-390? Per-team ladder estimates from ladder-only teams.
- Do dealer SELLS count for the ladder? Need one clean window.
- Duels: weight in Negotiating; compare our Duels I outcomes with the field's `duel.closed`.
