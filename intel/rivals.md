# How Team 13 and Team 18 score, and what to copy (Builder, Sat 12:00; independently verified; now the Analyst's)

_Sources: `data/feed.jsonl` (settlements de-duplicated by id; Friday = ticks < 159), `/api/dealers` menus (Saturday's;
Friday deals are judged against them), the leaderboard (tick 420), our `/api/me` (11:50) and the hub's demand model
(`hub.team_mult`, run 124). **Estimates** ("est.") are book × multiplier − price at the hub's multipliers [L]. They
**ignore copy marginals** (a 2nd copy is worth 25%, a 3rd 10%) and page bonuses, so they are biased low on sales of
duplicates and on page closes. Example: our SAL-01 sale at 7 is est. −2.0 but measured **+4.7** [V]. Verified deltas
are used wherever they exist. Raw counts cross-check exactly with the leaderboard's deal counts (45 / 28 / 35)._

## Live (Analyst; newest first)

### Sat 12:42 · snapshot 540
- Board: **t14 32.96 (#1)** · t12 30.53 · **t10 29.56 (#3, +3.6)** · t18 29.40 · t17 29.33 · t13 28.23 · **us 27.49 (#7)**.
- **t14 back to #1:** duels (part 6.4 → ~12.6 incl. deals) + Pilar LAT-08 at 20 (best uncommon share seen) + Chato BUY LAT-10
  at 86 (above list 77) that completed its LAT page (pages 1 → 2). A page closed through a DEALER scores 0 neg_points (gains
  clipped) [L]: not a play to copy.
- **t10 (#3):** duels 5.0 → 10.3 plus two Pilar sells at the top of her range (SAL-08 24, RET-08 25).
- **t04 sells patiently:** SAL-08 → Pilar at 25 (opened 40, 6 messages) vs our 23 (copied in the 12:42 note to the Chief).
- t12 is sliding in duels (12.0 → 9.5).

### Sat 12:30 · snapshot 510 (Duels I running)
- Board: t12 31.91 · **t17 29.29 (#2, +2.5)** · t14 28.85 · t13 27.71 · t18 27.48 · **us 27.03 (#6)** · t10 25.98 · t01 25.97.
- **t17 closed its MAL page** [V: pages 1 → 2]: bought MAL-10 from **t18** at 70 + 5 fee as taker on El Rastro (tick 508).
  Saturday part +4.7 in that window (page close ≈ 0.6 × 0.235 × 50 ≈ 7 minus duel slippage). t18 (#5) sold a page-closer to a
  top-3 rival for ~+20 neg_points.
- **The field is copying the dealer-sell ladder play** [V feed, 509-513]: t08 MAL-06 → Pilar 17, t16 LAT-07 → Pilar 17,
  t14 LAT-08 → Pilar 20, t10 SAL-08 → Pilar 24, t06 LAV-08 → Chato 13, t07 LAT-10 ← Chato 89. All teams are level 3 now.
  If the ladder part is graded against the field, every rival's deal lowers what ours is worth: do ours early.
- t13 is the weakest top team in duels (duel part 8.3 → 5.4); t14 9.9 → 6.4. t12 and t01 lead the duel part (~11.5-11.9).

### Sat 12:12 · snapshot 480 (Duels I running)
- Board: **t12 32.19** · t14 31.16 · t13 29.68 · t17 26.77 · t18 24.88 · **us 24.76 (#6)** · t10 24.0 · t04 23.9.
- Duels now carry 40% of Saturday Negotiating (intel/score-model.md §1b); the moves since 460 are mostly duels. Duel part
  (Saturday points, max 12): t12 12.0, t15 10.3, t14 9.9, t09 8.8, t13 8.3, t03 8.3, **us 8.2**.
- **t12 (#1):** full duel part from the first wave, plus market 11.74 (v02 value created). It buys LAT duplicates from t15 on
  others' venues (v14 tick 418, v17 tick 433), which feeds those venues' owners, not itself.
- **t13's Pilar-Abuela loop [V feed, ladder effect L]:** sells an uncommon to Pilar, rebuys the same card from Abuela below
  list: Pilar SELL LAV-08 @18 (t462), LAV-06 @18 (t467); Abuela BUY LAV-08 @23 (t469), LAV-06 @23 (t474). Same holdings at
  the end, −5 P and about −5 neg_points per card (≈ −0.47 board), bought ladder at level 3 (sell) and level 1 (buy ≤ list).
- **t17 (#4):** market 10.26 from one trade on its v17 stall (t15 → t12 LAT-01 at 7); cut the stall's fee to 0 at tick 429.
- t18 dropped to #5: its duel part fell 7.9 → 5.0.

## The board [V, leaderboard tick 420]

| Team | Rank | Score | Negotiating | Market | Deals |
|---|---|---|---|---|---|
| t14 | #1 | 29.05 | 17.19 | 11.86 | |
| t13 | | 27.72 | **24.39** (top) | 3.33 | 45 |
| t18 | | 26.66 | 19.16 | 7.5 | 28 |
| us (t05) | | 22.66 | 15.16 | 7.5 | 35 |

- Market leaders: t10 12.5, **t14 11.86**, t12 11.74.
- Our parts [V, /api/me]: neg_points 35.2, ladder 0.055, duels 0, bench 0.5, **mm_points −5.2**.
- Hub multipliers [L]. Each team has the same six numbers (1.6, 1.3, 1.1, 0.9, 0.7, 0.5) shuffled (RULES.md:24),
  so MAL and SAL can't both be 1.6.
  - **t13:** MAL 1.35 / SAL 1.35, most consistent with {1.6, 1.3}; LAV 1.07, RET 0.91, LAT 0.59.
  - **t18:** RET 1.51 (likely 1.6), LAT 1.21, SAL 1.17, LAV 0.70, MAL 0.67.

## 1. Dealer deals [V counts and prices]

| | Friday | Saturday | Buys vs list | Unlocks |
|---|---|---|---|---|
| **t13** | 15: 7 Abuela buys, 6 Abuela sells, 2 Chato sells | 15: 3 Abuela buys (packs), 8 Abuela sells, 2 Chato buys, 1 Chato sell, 1 Pilar sell | never above list: Abuela 8 below (5 packs), 2 at; Chato 2 **at** list (LAV-06/07 at 26) | Chato t98 ("6 deals with abuela"); **Pilar t262 ("3 deals with chato")** |
| **t18** | 8: 6 Abuela buys, 1 Chato buy, 1 Chato sell | 8: 6 Abuela buys, 2 Chato buys | Abuela 10 below, 2 at; Chato 3 above (LAT-08 32, RET-09/10 86) | Chato t98 ("3 deals with abuela"); no Pilar |
| **us** | 15: 7 Abuela buys, 5 Abuela sells, 2 Chato buys, 1 Chato sell | 8: 5 Abuela buys, 3 Chato buys | Abuela 11 below, 1 above (MAL-07 29, = Abuela's Friday opening ask); every Chato buy above list (31, 93, 87, 86, 30) | Chato t98 ("6 deals with abuela"); no Pilar |

- **t13 sells commons to Abuela** [V]. 14 sales at 5-6 P: t13 opens at 20-22, she bids 5, and it ends after 5-7
  rounds. They look like spare copies [L]: it sold two copies each of SAL-01 and LAT-04, and SAL-05 and MAL-01 while
  holding earlier copies. A spare sold at ≥ its 25% value scores ≥ 0.
- **The Pilar unlock is unexplained [?].** t13's 4 Chato deals before her level activated (tick 262):
  - 2 buys at exactly list. t13 stepped LAV-06 from 9 and LAV-07 from 12 up to 26, and **Chato accepted t13's number**.
  - 2 sales where **t13 accepted Chato's final** (LAT-09 at 46 after his opening 39, MAL-06 at 15 after 13).

  The server says "3", but "at or below list counts" predicts 4 and "below list only" predicts 2. Who accepted is a
  possible confound. We had 0 at-or-below-list Chato deals, and our one sale was at his opening bid (RULES.md:35: never
  counts). **Not a GAME.md change**: n = 1, and RULES.md:35 only says "a negotiated one does".
- Level 2 [?]. t18's "3" matches its 3 card buys before t98 with its 2 packs left out; t13's "6" matches 5 card buys
  plus 1 sale. Our "6" doesn't fit cleanly: 3 card buys, 4 sales (2 at her opening bid), and MAL-07 at her opening ask
  (t98, settled just before the unlock event).
- Opening prices: the scan matched threads by asset id, which misses buy threads (dealer sell offers name the card by
  type). Counts are unaffected; per-deal opening prices for buys aren't reported here.

## 2. Team trades [V prices; est. L, biased low on duplicates and page closes]

| | Friday | Saturday | Notes |
|---|---|---|---|
| **t13** | 9 (6 buys, 3 sells), est. +122 | 6 (2 buys, 4 sells), est. +22 | Buys in its high sets at or near clearing: SAL-09 at 74 (+20), SAL-10 at 70 (+24), MAL-10 at 65 (+30, t331), MAL commons at 6 (+7.5 each). Sells LAT: LAT-09 at 65 (+24), LAT-01+07 at 40 (+19). Saturday sales est. −6.5, −8.5, −2.7 (likely duplicates, so better than that [L]). All on El Rastro but two small sales on t12's v02. |
| **t18** | 9 (2 buys, 7 sells), est. −2 | 3, est. −31 *excluding the page bonus* | RET-02 bought at **49** from t02 as maker (it posted the bid). Its negotiating rose **16.25 → 22.08** between ticks 220 and 230 [V leaderboard], which fits a capped +50 page close, not −34 [L]. It sold SAL-01 and MAL-04 twice each (duplicates [L]). It scores on pages [L]. |
| **us** | 9 (3 buys, 6 sells), est. +40 incl. the LAV close | **+56.7 measured** [V]: RET-01 page close +50.0, SAL-01 +4.7, +2.0 | Friday LAT/MAL uncommon sales near clearing est. +8.5, +9.5, +8.5. |

**What t13 does that we do less** [L]: trade by trade, it buys cards of the sets it values most (MAL/SAL) at or near
clearing and sells cards of the set it values least (LAT): est. +7 to +30 on its best trades, some negative ones too.
It never pays a dealer above list.

## 3. Venues and value created

- t13's **v03** (board, opened t129; fee 0% since t251/t316) has had **0 trades** [V]. t13 promotes it with
  announcements every 10-20 ticks, including a "Club welcome" offer of spare commons at 5 P. t18's **v18** stall (3%,
  auto): 0 trades [V]. Neither scores much market: t13 3.33, t18 7.5.
- Our **v10** (0% since t230): 2 trades by other teams [V].
  - t10 → t01, MAL-07 at 14: est. +5.0, measured +4.99.
  - t10 → t15, SAL-07 at 26: est. −2.8, measured **−10.19** (mm_points 4.99 → −5.2) [V].

  The hub's t15 SAL estimate rests on n = 3: the value-created estimates hit 1 of 2 [L]. Value created is copy-weighted in
  `tools/v10_radar.py` since b3b0e61.

## 4. Three plays we're not making (handed to the Analyst)

1. **Sunday: buy CHA from teams, not dealers** [L].
   - A dealer buy below our value scores 0 (gains clipped, GAME.md). A team buy scores value − price.
   - Per card, as maker at clearing (9 / 24.5 / 70): **+7 / +15.5 / +42**. At the plan's bids (10 / 25 / 80):
     +6 / +15 / +32. A taker pays 2 / 3 / 5 more in fees.
   - Ceiling ≈ +150 if all nine non-closing cards came from teams at clearing. The closing card is capped at +50 in
     total (not on top).
   - Realistic: supply-dependent (minted 0; teams get CHA from packs and dealers).
   - Changes intel/cha-plan.md: team bids from the release, dealers as a timed fallback.
2. **Sell our low-multiplier cards at clearing to non-top-4 collectors** [L].
   - Ceiling ≈ +60 neg_points if every listing fills. Holdings per /api/me 11:50; LAT at its own clearing 7.5 / 21.5,
     MAL/SAL at 9 / 24.5.
   - Expect a fraction: 5% of asks fill, 9% of bids (GAME.md).
   - The book asks a spare LAT-04 at 4, SAL-02 at 4 and LAV-03 at 5, against clearing ~7.5-9: raising them adds
     ≈ +11 if they fill.
   - The trader's min-gain-sell 6 refuses a collector's 9 P bid for a spare LAT-04 **on El Rastro** (9 − 2 fee − 1.2 =
     5.8). On a 0% venue it nets 7.8 and is accepted.
3. **Stop paying dealers above list** [?].
   - Our 5 Chato buys paid **44 P over list** and earned no ladder or unlock. t13's at-list Chato buys came with an
     early Pilar unlock (consistent with, not proof of, a price-vs-list rule).
   - Cost 0; saves the premium. For Sunday's CHA rares: bid Chato at list (77) before paying more.

**Epics and legendaries:** none has traded, been pulled as a pack's best card, or been offered for sale [V]. Signs of
demand: t12 bid 88 for SAL-11 (t105); t06 posted swap offers wanting LAV-12 (t395) and SAL-12 (t396). `bargains` pages
Lucas if one is offered at value − price − fee ≥ 20.
