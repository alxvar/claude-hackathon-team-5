# Judge (claude-opus-5-5, Sat 12:59)

## Verdict
**Gaining:** #3 at 29.6, +6.9 in 60 min vs Team 14 (#1, 31.8) +2.7 and Team 18 +3.3, so the gap to #1 is 2.2. The gain came from the ladder (0.141 → 0.181) and duels (11.35). `neg_points` has been flat at 35.2 since tick 404, with no team-trade gain for about 170 ticks.

## Our strategies: keep / kill / scale
- **Pilar ladder sells, small steps, offer-only:** KEEP. MAL-07 +0.050 and MAL-06 +0.040 cost 0 neg; the jump on SAL-08 gave only +0.019. We have no spare uncommons left to sell.
- **Chato buys above list:** stays KILLED. Six deals, 0 ladder, −21.5 neg on Saturday.
- **Epic chase (LAV-11):** KILL. Pilar paid 140 while we stepped 100 → 120. Any epic bid must clear ~140.
- **Our 9 addressed asks (4-11 P):** KEEP but FIX. The last team fill was tick 351 (SAL-01 +4.7), and each ask is worth only +2 to +3.
  - SAL-01 → t06 at 11 breaks the feeding rule if SAL-01 closes t06's page: t06 is #10, only 5.6 below us, and collects SAL.
- **Trading loop:** UNVERIFIED. Its log shows nothing after tick 285 (10:32), although the operator says it was restarted at 12:52. No fills are visible.
- **In-room page-closers:** SCALE. RET-01 from t10 at 20 scored +50, our best trade today.
- **Duels (Aleks):** keep. 11.35 points; 9 of the last 10 ended in a deal.
- **Venue v10:** hold. `mm_points` went to −5.2 after a dump to a lower-multiplier team, and nothing has been measured since.

## Check the scout
- **Claim 1 (finish the RET page) is false.** Holdings show RET-01..10 all held. The +50 at tick 276 was the page close, so the bonus is already counted. Drop it.
- **Claim 2 ("past the ~0.15 ladder cap") is false.** MAL-06 added +0.040 starting from 0.141 → 0.181.
  - True: L3 has 3 deals and we hold no MAL/SAL uncommons.
  - Pilar's median is 23 over 13 trades, not 22 over 15.
- **Claim 3 holds** (offer prices, t04's RET-02 bid at 10, RET-05 asks at 12, don't sell RET cards), except for the t06 feeding issue above.
- **Rival notes, wrong:**
  - The LAV-10 buy at 82 from t16 was Team 6's, not Team 14's.
  - t06 sold RET-09 to t02 at 84; it did not buy it.
- **Rival notes, correct:** t06's bids (LAV-09 at 99, SAL-09 at 68), t12's trades, and t13's 2 P RET sweep.

## The 3 changes with the highest expected gain
1. **Fill the 2 empty L2 slots (only LAT-08's +0.017 counts there).**
   - First, one offer-only Chato sell of a spare worth ≤ his bid (LAT-03 worth 5, LAT-04 1.2, LAV spares 3.2), alone in its window. That costs 0 neg. Whether Chato buys commons is not in the data.
   - If he doesn't, use the 11:35 directive: one Chato SAL uncommon buy at list 26 (−3.5 neg ≈ −0.33 board). Walk at 27.
   - Effect: ≈ +0.017 ladder ≈ +0.56 board per slot (12:13 rate).
   - Risk: list buys never counted before. Measure Δladder after the first deal and stop if it is 0.
2. **Reprice LAV spares as page-closers, not at 6.**
   - Dani asks t07 and t09 in the room whether LAV-02/03/04 is their last missing LAV card.
   - If yes, and the team is ≥ 10 below us and not top 4, re-list at 30-40 addressed to them as maker (plan §4A).
   - Effect: +26.8 neg vs +2.8 per fill ≈ +2.3 board each.
   - Risk: no team lacks them, so revert to 6.
   - Cancel 8247 (SAL-01 → t06) unless SAL-01 is not t06's closer.
3. **Upgrade L3's weakest slot (SAL-08, +0.019): a one-shot test.**
   - Buy one SAL uncommon from Abuela at ≤ 22 (value 22.5, so 0 neg; below her list 25, so it may also count for L1).
   - Resell it to Pilar with −2 steps, offer-only, at ≥ 23.
   - Keep the cycle only if Δladder > 0.
   - Risk: Pilar opens SAL near 22, so the share stays small. Cash moves ~±2.
   - Keep cash ≥ 170 for Sunday's CHA page; never sell LAV-09/10 or RET-09/10 into t06's bids.
