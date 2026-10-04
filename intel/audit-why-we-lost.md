# Why we finished behind on Friday and Saturday (independent audit, Auditor A, Sun ~01:00)

Written with no prior context, read-only. Sources: `data/leaderboard.jsonl` (snapshots 90-1440), `data/feed.jsonl`
(27,162 public events, settlements de-duplicated by id), `data/me.jsonl`, RULES.md, GAME.md, score-model.md, directives,
LOG.md, market-log.md, duel-review.md, docs/duels-1-review.md, intel/rivals.md. Scripts: scratchpad `load.py`, `ladder.py`.
Labels: **[V]** read from the data or plain arithmetic on it · **[L]** inference that fits the data but isn't proven · **[?]** open.

**Units.** Board = (0.5·Fri + Sat)/1.5 since tick 321 (score-model §1, an 11-snapshot fit). So a team's Saturday round =
1.5 × board − 0.5 × Friday board, and the game total so far = 0.5·Fri + Sat. **Final game score = (0.5·Fri + Sat + Sun)/2.5, so
1 Sunday round point = 0.4 final points.** Every "Sunday pts" figure below is out of Sunday's 60-point round.

## TL;DR

1. **Our #3 is a Friday legacy. On Saturday alone we were #5** (35.74), behind t10 45.99, t18 37.31, t03 37.21, t06 36.80 [V].
   If every team repeats its Saturday on Sunday, we finish **#4**: t18 84.20 · t03 81.71 · **us 81.47** · t06 79.94 [V arithmetic].
   The race for #2 is against t18, t03 and t06, not just against t10.
2. **t10's 10.64-point lead = market 7.5 + Saturday negotiating 2.76 + Friday 0.38** [V]. "70% market" is right at the close,
   but the time path says something else: at tick 1230 (21:12) **we led t10 on Saturday negotiating by 3.87**. Duels II and the
   trades t10 made during it swung **6.6 points** in about 2.2 hours (21:12 → 23:24) [V]; 3.7 of that came in 20 ticks with no deal by either team
   (our Duels II wave-1 day-reading bug) [V numbers, L attribution]. So market and duels together are more than the whole lead.
3. **Our market part was 0, largely for reasons we chose** [V counts, L cause]: 381 of our 389 Saturday listings were addressed
   (30 of 35 team-venue fills came from open offers), 261 of the addressed ones sat on t10's v07 and t15's v15, and v10 got 2
   fills all day, both from t10, one of which wiped our score. Right after our own v07 trades, t10's market went +4.34 board
   (tick 351) and back to its cap (tick 714) [V numbers, L cause].
4. **The top teams kept dealing; we stopped.** After our SAL close at 18:32 (tick 988) we made **1 deal**; t10 made 26, t06 19,
   t12 17 [V]. t10 made both of its epic team trades (MAL-11 at 195, SAL-11 at 207) inside Duels II.
5. **"Never flip a dealer card" is too broad.** t06 (RET rares and RET-11 from the Pícaros, sold to teams at 77-216), t10
   (SAL-11 155 → 207) and t10/t12/t18 (Pícaros → Pilar cycles in the Salamanca fever) made money and ladder from dealer flips.
   Autoflip failed because it bought above value with no buyer lined up, not because flipping is wrong.
6. **Friday:** about 25 neg_points of avoidable losses (packs, dealer buys above value) cost ≈ 3.9 Friday board ≈ 1.9 game
   points [L]. That's more than our whole gap to t18 (1.16).

---

## 1. The board split by day and component [V]

| Team | Fri board | Sat round | Sat negotiating | Sat market | Game so far (0.5·Fri + Sat) | Board 1440 | Sat rank |
|---|---|---|---|---|---|---|---|
| t10 | 20.75 | **45.99** | 27.24 | **18.75** | **56.37** | 37.58 | 1 |
| t18 | 19.16 | 37.31 | 26.06 | 11.25 | 46.89 | 31.26 | 2 |
| **t05** | 19.99 | 35.74 | 24.49 | 11.25 | 45.73 | 30.49 | **5** |
| t12 | **27.82** | 31.72 | 20.85 | 10.88 | 45.63 | 30.42 | 9 |
| t03 | 14.60 | 37.21 | **28.08** | 9.12 | 44.51 | 29.67 | 3 |
| t06 | 12.67 | 36.80 | 19.01 | 17.80 | 43.14 | 28.76 | 4 |
| t14 | 18.06 | 32.48 | 18.52 | 13.95 | 41.51 | 27.67 | 7 |

Readings:
- **Market [V]:** 11.25 Saturday points = the free stall's bench (half points). Everything above it is value created (VC) on
  the team's venue. Seven teams ended above the stall line: t10 +7.5 (the most anyone reached), t06 +6.55, t09 +5.09, t16 +3.99,
  t14 +2.70, t17 +1.71, t08 +1.42. We, t18, t01, t04, t15, t02, t07 and t11 have +0. t03 (9.12), t13 (10.15) and t12 (10.88) are
  below the stall line; for t03 the cause is its own board venue losing bench points [V market-log], for t12/t13 likely the same [L].
- **Negotiating [V]:** t03 28.08 > t10 27.24 > t18 26.06 > **us 24.49** > t01 23.03. We were 4th.
- **Friday [V]:** t13 29.94 (it hit 30.00 at tick 120 and held), t12 27.82, t17 22.03, t10 20.75, t04 20.49, **us 19.99 (#6)**.

**If Sunday repeats Saturday [V arithmetic]:** t10 102.36 · t18 84.20 · t03 81.71 · **us 81.47** · t06 79.94 · t12 77.35.
We're #3 today only because of Friday; on Saturday form we fall behind t18 and t03.

## 2. Team 10 vs us, component by component

### 2.1 Gap table (game-total points, 0.5·Fri + Sat)

| Component | t10 | Us | Gap | Label | Evidence |
|---|---|---|---|---|---|
| Friday (×0.5) | 10.38 | 10.00 | **+0.38** | V | board at tick 160 |
| Saturday market: bench | 11.25 | 11.25 | 0 | V | both at stall level all six sessions (t10's board broker never moved its market at a bench end: market-log) |
| Saturday market: value created | 7.50 | 0 | **+7.50** | V | t10 at 12.5 board from tick 720 to the close; ours floored at 0 since tick 400 |
| Saturday negotiating, total | 27.24 | 24.49 | **+2.76** | V | |
| ↳ duel part | ≥ 9.2 | ≈ 6.9 | **+2.3 to +4.5** | L | lower bound: t10's trade + ladder parts can't exceed 18. Upper: the 1240-1260 window (below) and rivals.md's "2.3-3.0 board" (= 3.5-4.5 Saturday points) |
| ↳ team trades + ladder | ≤ 18 | ≈ 17.6 | **−1.7 to +0.4** | L | if the duel gap is ~4, we were *ahead* here |
| **Total** | 56.37 | 45.73 | **10.64** | V | |

Correction to score-model §4.2: it says "duels ≈ +2.3 Saturday points" while rivals.md says "≈ 2.3-3.0 **board**"; those
differ by 1.5×. My window data fits the larger one. Read the lead as **≈ 70% market + ≈ 30-40% duels − a small edge of ours on
trades/ladder/Friday**.

### 2.2 The time path matters more than the end state [V numbers, L causes]

Saturday-equivalent negotiating (Saturday points, de-blended per snapshot):

| Tick (wall) | t10 | Us | Us − t10 | What happened |
|---|---|---|---|---|
| 460 (12:00) | 8.13 | 12.75 | +4.62 | before Duels I |
| 630 (13:25) | 14.84 | 20.98 | +6.14 | Duels I + our Pilar/Chato ladder sells |
| 1000 (18:34) | 13.40 | 26.76 | +13.36 | our SAL page close (+40.4 np) |
| 1100 (19:24) | 20.57 | 26.27 | +5.70 | t10: cheap RET page close + fever ladder cycles |
| 1230 (21:12) | 22.78 | 26.65 | **+3.87** | Duels II starts at 1239 |
| 1260 (21:27) | 24.95 | 25.09 | +0.14 | **window 1240-1260: no deal by either team; t10 +2.18, us −1.56 = 3.74 swing** [V]; cause [L]: our wave 1 opened every duel at day 5 (fix live from tick 1256, score-model §1g) |
| 1440 (23:24, close) | 27.24 | 24.49 | **−2.76** | t10 also did MAL-11 (195) and SAL-11 (207) team trades in this window; we had 0 deals from tick 1210 to the close |

Our duel_points rose 13.93 → 35.39 in Duels II while our board negotiating *fell* 24.43 → 22.99 [V]: every part is graded
against the field, so a duel session where others gain more costs us even with a good deal rate.

### 2.3 What t10 actually did [V feed]
- **Venue:** opened a *board* venue v07 "fair broker, 0 fee" at tick 179. It drew 552 listings (t08 204, **us 135**, t06 104, t04 55)
  and 11 fills: 4 ours, 6 by t06 as maker, 1 t04 → t09. It held the VC cap from tick 720 to the close.
- **Our venue:** listed 73 offers on v10 (mostly addressed): 2 fills, MAL-07 → t01 (+4.99 for us) then SAL-07 → t15 (VC −10.19,
  our market 12.5 → 7.5 at tick 400, never recovered; the −10.19 comes from score-model's mm_points fit [L], while
  `venue_value_created` stayed +9.0).
- **Ladder by cycling:** five Pícaros → Pilar round trips with SAL rares (buy 52-57, sell 75-86; four inside the fever, ticks
  1094-1178, one at 1316-1327), plus two silver-pack SAL-10 pulls sold to Pilar at 74-75: high-share L3 and L4 slots and
  +20-30 P per trip.
- **Cheap page close:** RET-09/10 from the Pícaros at 59/53 (≤ list 63), RET-04 from Abuela at 10, then the last card RET-03 from
  t06 at 12 on El Rastro (team trade → page bonus). We paid **Chato 87 and 86** for the same two rares in the morning (−19 np, 0 ladder).
- **Epic trades:** MAL-11 bought from t08 at 195 as maker (tick 1264); SAL-11 bought from the Pícaros at 155 and sold to t17 at
  207 (tick 1296).
- **Gifts as inventory:** 4 Abuela gifts on Friday/Saturday; it sold one (MAL-06) to t09 at 20 at tick 1230 (+1.02 board in that window).
- Eggs: 5 (the most, tied with t08). Not scored, but one paid a pack and a card.

## 3. t18, t03, t06, t12: what each did better [V feed, L reading]

| Team | Where it beat us | How |
|---|---|---|
| **t18** (+1.16 game, the #2 race) | Saturday negotiating +1.57 | Few, big trades, **all 163 listings open** on El Rastro; LAT-10 from t13 at 72 (tick 1332, +1.92 board; likely its LAT page close [L]); SAL-11 bought from the Pícaros at 139, sold to Pilar at 199 in the fever; MAL-10 sold to t17 at 70. Same stall market as us |
| **t03** (−1.22 behind us, but won Saturday negotiating) | Saturday negotiating +3.59 | Strongest Duels I of the top teams (+7.0 Saturday points in windows with no t03 deal, vs our +3.3); a 5-card bundle trade (tick 844). **Lost 2.13 Saturday points** by replacing its stall with board venue v20 (0 on a bench session) |
| **t06** (Saturday round 36.80 > ours) | Market +6.55 | VC from only 3 trades on its v01 (incl. SAL-10 t12 → t08 at 76); 870 listings, **all open**; 25 Saturday team trades; a RET pipeline: Pícaros RET-09/10 at 52-58 → teams at 77-84, RET-11 137 → t12 at 216; SAL-11 to Ernesto for an L5 slot. Weak duels (its negotiating fell 21.61 → 19.01 in Duels II) |
| **t12** (Friday 27.82) | Friday +7.83 board | Sold SAL rares from a low-multiplier set to collectors in the first two hours: SAL-10 80 (→ t18), SAL-09 75 (→ t17), SAL-08 35. Saturday market: its v02 took 11 fills, then two cheap page-card sales by t07 wiped its VC (12.43 → 7.5 at tick 910) |
| **t13** (Friday 29.94) | Friday | Rare trades in hour one: LAT-09 sold 65, SAL-09 bought 74, SAL-10 bought 70, our MAL-08 at 26 |

**Bench (Market Test) [V]:** not a differentiator. In six sessions no venue beat the free stall; t10's board broker matched it;
t03 and t12 lost points with board venues. Keeping the stall was right.

## 4. Our explanations, challenged

**4.1 "70% of t10's lead is market."** True at the close (7.5 of 10.64) [V], misleading as a diagnosis:
- It's **our** zero, not t10's magic: seven teams ended above the stall line, t16 on a plain stall and t09 on a 0% venue
  with 6 fills; we didn't.
- It hides the duels: we led negotiating by 3.87 at 21:12 and lost the lead in Duels II (§2.2).

**4.2 "Our 10:18 venue deal fed t10."** True, and understated [V]:
- We were maker on all 4 of our v07 fills.
- Our SAL-01 sale at 351 was the only v07 trade before t10's market went 7.50 → 11.84 [V numbers; cause L, the field reference can move].
- Our MAL-01 buy at 714 took it 12.01 → 12.50, back to the cap (the only v07 trade in that window [V]; the cause is [L],
  since the field reference can also move). The 15:55 directive had said "our trades on v07 add ~0 to it".
- In return, t10's two v10 trades netted us 0.
- We posted 128 addressed listings on v07 between 10:20 and 16:05 (ticks 260-712).

**4.3 "Our ladder is capped."** Partly:
- The 850-890 test was real (+0.064 ladder, board flat) [V].
- The Analyst saw it slip back below the cap at 1030 [L], and the field kept filling L3/L4 after that.
- Our raw 0.483 has **L5 = 0 of 0.333 possible and L2 = 0.029 of 0.133** [V score-model fit].
- On Sunday the ladder resets, so "capped" no longer describes anything. What matters is how fast we reach Sunday's reference.

**4.4 "Our trade part is ≈ 0.95 of its cap (N ≈ 125)."** The N comes from two events [L]. If N is a top-3 mean, the late
+50-class trades by t10/t06/t12/t18 (MAL-11, SAL-11, RET-11, LAT-10) raised it, so ours probably eroded below 0.95 by the
close. Our board negotiating fell in windows with no events of ours [V].

**4.5 "Never a dealer flip."** Too broad [V scoring identity from GAME.md rules + L on others' holdings]:
- A flip scores min(0, v − p_dealer) + min(50, p_team − v − fee), where v is our value of the card.
- When v ≤ p_dealer and the team leg stays under 50, that is simply **p_team − p_dealer − fee**: the spread. The dealer buy
  also fills a ladder slot when it's ≤ the MENU list.
- t06 ran it four times (ticks 895, 1186, 1245, 1257; its SAL-11 Pícaros 143 → Ernesto 120 was dealer-to-dealer and a loss, for an L5 slot);
  t10 once with an epic.
- Autoflip lost because it bought *above* our value from Abuela and the team bids vanished before it could sell. That is an
  execution failure (no buyer lined up), not an economic one.
- The deck's "one team −189" is consistent with buying above value [?].

**4.6 "Duels: upper-mid, the fixes are in."** The data says duels are a third of the t10 gap:
- The wave-1 day bug alone: a 3.7-point swing in 20 ticks [L].
- Four conceded rival days, never priced: ≈ 85 P forgone (score-model §1g).
- Long thin-margin haggles of 7-9 rounds.

**4.7 "Eggs and badges don't score."** Correct (RULES). Two notes:
- The Sunday plan opens with the Pícaros egg ("no tricks for you… today").
- t10 still received "they stopped printing it yesterday" lies from the Pícaros at ticks 1370 and 1422, *after* its egg at 1231 [V].
  So the egg doesn't remove every flaggable lie, but it may remove the bait-and-switch, the cleanest flag class [?].
- Probe one flag **before** triggering the egg.

## 5. What we missed entirely

**5.1 Open offers do almost all the filling, and liquidity decides value created [V].** Saturday listings → fills by venue:

| Venue | Owner | Listed | Open | Addressed | Fills | Biggest makers |
|---|---|---|---|---|---|---|
| El Rastro | house | 5,316 | 4,415 | 901 | 89 | t16 811, t06 693, t13 584, t08 550 |
| v07 | t10 | 552 | 162 | 390 | 11 | t08 204, **t05 135**, t06 104 |
| v02 | t12 | 420 | 329 | 91 | 11 | t07 94, t14 73, t13 72 |
| v21 | t09 | 236 | 49 | 187 | 6 | t08 131, t12 52 |
| v15 | t15 | 160 | 0 | 160 | **0** | **t05 133** |
| **v10** | **t05** | 111 | 17 | 94 | **2** | t10 73, t13 25 |

- Market-log: 30 of 35 team-venue fills were open offers; the takers are board-scanning bots.
- Our Saturday listings: **381 of 389 addressed**, 261 of those on v07/v15. Result: 8 Saturday team trades.
  t06 had 25, t15 24, t07 23, t12 20, t04 20.
- The 10:30 "asks stay addressed" rule (to avoid handing a top-4 team a page-closer) cost both volume and venue traffic.

**5.2 We went idle [V].**
- Deals after tick 988 (18:32): t10 26, t06 19, t12 17, t13 17, … t03 3, **us 1**.
- From tick 1210 to the close: 0 deals of any kind, despite "21:45 bots back on during Duels II".
- The Payday +400 at 20:37 was meant to be spent. Holding cash for Sunday is a defensible choice, but it was never checked
  against what the field was doing with it.

**5.3 The same rarity is cheaper at higher dealer levels [V].**

| Rarity | Pícaros (L4) | Chato (L2) |
|---|---|---|
| Rare | 48-67 (list 63) | 75-96 (list 77) |
| Epic | 128-167 | none |

- We bought RET-09/10 from Chato at 87/86: −19 np and no ladder. t10 bought the same cards from the Pícaros at 59/53: 0 np and two L4 slots.
- **The round is scored on its end state** (RULES "counts in full once its day is over"), so closing RET at 10:27 instead of
  17:30 earned nothing extra [L]. Speed pays only when supply is scarce: CHA rares have 30 copies.

**5.4 Timed events are scoring windows [V feed].**
- Salamanca fever, Pilar +25% on SAL (ticks 939-1179): t10, t12 and t18 cycled Pícaros SAL rares and epics into Pilar
  (t18: SAL-11 139 → 199).
- Radio "Chato pays above usual for rare MAL, one hour" (tick 403): nobody used it.
- Radio "Abuela pays more for uncommons until teatime" (943).
- El Tablón's rumours were false ("Abuela stops buying commons": she bought 28 more after tick 763; the legendary for a
  hello; the LAV reprint). The Boletín's saint's-day packs never appeared in the feed either. Treat news as a prompt for one
  probe, not as a fact.

**5.5 Friday losses were self-inflicted [V me.jsonl + feed].**
- 3 packs bought at 17-22 (start −8.5 np, unopened until tick 136 → drag).
- MAL-07 autoflip at 29, worth 17.5: −11.8 measured (−11.5 on value, the rest pack drag).
- LAV-06 from Chato above list, LAV-09 at 93: ≈ −4.
- Total ≈ −25 np. At Friday's measured rate (+50 np → +7.79 board on the LAV close) that's ≈ 3.9 Friday board ≈ 1.9 game points [L].
- **Enough to be #2 today** (gap to t18: 1.16).
- Meanwhile the Friday leaders made one to three rare trades at collector prices (65-80) in the first two hours; we made none.

**5.6 Gifts and eggs are inventory [V].** Abuela gift cards (t13 got 5; t06, t07, t08, t10, t14, t15 got 4; us 2) and egg cards/packs score 0 when
received, but a team sale of them scores. t10 sold its gift MAL-06 at 20.

## 6. Ten lessons for Sunday, ranked by expected points

Stakes are Sunday round points (×0.4 = final points). Today's gaps in final points:

| Team | Gap to us (final points) |
|---|---|
| t10 | 4.26 ahead |
| t18 | 0.46 ahead |
| t12 | 0.04 behind |
| t03 | 0.49 behind |
| t06 | 1.04 behind |

**1. Get value created on v10: it's the biggest component we score 0 on.** Stake: **+2-5 Sunday points, up to 7.5** (+0.8-3.0 final);
×3 if the deck's "real trades 22.5" holds [?].
- Get the heavy listers' bots to route to v10 (Saturday listings): t13 1,157 (949 open), t08 1,098 (411 open), t06 870 (all open),
  t16 820. Each needs only a
  default-venue switch: "0%, crossed every tick".
- Ask for **open** offers, buyers' bids first.
- Duplicates go to collectors only: an auto stall crosses value-destroying trades too, as t10's SAL-07 showed.
- No paid volume ("volume and friends count for nothing").

**2. Duels III + Final: close the duel gap.** Stake: **+1.5-3** (+0.6-1.2 final). Our Saturday duel part was ≈ 6.9/12 against
t10's ≥ 9.2.
- Hard-assert on the first closed duel of each session that `pred == points` (day direction), and auto-revert to SAFE if not.
- Price every day concession (≥ C + ~C), never accept the rival's day unpriced.
- Stop 7-9-round haggles on margins under ~11.
- Keep decision latency under one 15 s tick.

**3. Open listings, not addressed ones.** Stake: **+1.5-3**. Sunday's trade part (9 points) starts at 0 and needs ~125 np.
- Duplicates go up as open asks at collector prices on El Rastro (or a non-rival's venue).
- CHA commons and uncommons get open bids.
- Only page-closer bids stay addressed, and short-lived.

**4. Run dealer → team spread flips, buyer first.** Stake: **+1-3**.
- Only when a team bid already sits on the book (or a buyer has agreed), v ≤ the dealer price, and the dealer price ≤ the MENU list
  (that also fills a ladder slot).
- Templates: t06's RET (Pícaros 52-58 → teams 77-84), t10's SAL-11 (155 → 207).
- Never against a complete page of ours: a 2nd copy is worth 25%, so the buy leg costs.

**5. Zero listings on rival venues; put a stop-loss on any reciprocity.** Stake: deny t10 0.5-4.
- One of our trades on v07 was worth up to +4.3 board to t10 (tick 351).
- Keep the 17:30 rule. For any venue swap, audit trade by trade and kill it after the first negative trade or a 2:1 imbalance.

**6. Don't go idle during duels or after a page close.** Stake: **+1-2**.
- Trader and dealer threads run through Duels III and the Final (duel limits are separate).
- Alert if 30 minutes pass with no settlement.
- Spend the cash before the dealers close: unspent cash scores 0.

**7. Buy CHA rares at the cheapest level.** Stake: **+1-2** (avoids ~−20 np and adds L4 slots).
- Pícaros at 48-63 (at or under list 63) are 0 np and an L4 slot each; some Pícaros rare sales went at 64-67, above list, which don't count. Chato is above list: a counted loss and no ladder.
- Check the structured card every time: they bait and switch.

**8. Probe flags before the Pícaros egg.** Stake: **0 to +2.2** (≈ 3 × 10 np if the cap is per round; EV ≈ +1).
- Flag only words that contradict the structured offer, or "stopped printing" / "last one in Madrid" claims.
- One wrong flag costs −10.

**9. Watch for events with a ready playbook.** Stake: **+0.5-2**.
- Watch `announcement` and `persona_patch` (both came true on Saturday); test any news item with one small probe first.
- Keep one or two first-copy rares of a non-page set liquid for a fever-type window.

**10. Hard loss guards, the Friday lesson.** Stake: avoids **−1 to −3**.
- Code-level refusals: buys above our value (except a pre-paired flip leg), packs, dealer buys of 2nd copies, any sale from a
  complete page (the deck says −130).
- Open every pack or egg pack at once (unopened packs drag every trade).

**On #2 (t18 is 1.16 game points ahead):**
- t18's Saturday round beat ours by 1.57 with the same stall market, so lessons 1, 2 and 3 decide it.
- Deny page-closers to t18, t03 and t06 only. Everyone else is a counterparty whenever our gain ≥ theirs.
- The blanket "top 6 / within 3.0 / 3× gain" rule cut our volume more than it protected us [L].

## 7. Caveats
- **Duels:** the feed carries no team on `duel.closed`, so every duel part here is inferred from leaderboard windows [L].
  Windows mix duels with normaliser drift.
- **Feed completeness:** settlement ids have gaps (333 of 1,126 missing), but the feed count equals the leaderboard
  `deals` for the six teams checked (t10 62, t06 71, t18 40, t03 32, t12 70, us 53; t04 differs by 1). So the trade data is
  near-complete [V]; the gaps are something else (private or non-trade).
- **The 22.5 question:** the market split is from the board fit (bench 22.5, VC 7.5). The organisers' deck says Market Test 7.5 +
  real trades 22.5; the stall teams' 11.25 doesn't fit the deck's reading [?]. Either way, value created is our largest missing component.
- **Flags:** no team's flags are public; the "≈ 3 scored per team" cap is from our own probes. Its reset rule (per round?) is unknown [?].


_Independent verification (fresh subagent, own scripts on the raw files): all 14 numeric claims PASS; fixes applied for
wall-clock times around Duels II, the open-offer wording, the 261/268 count, t06's flip count, gift counts, label hygiene._
