# Judge (claude-opus-5-5, Sat 13:49)

## Verdict
Holding #5 at 28.1 and 2.7 behind Team 14. Over 60 min we gained more than the leader (+1.8 vs +1.1), but Team 10 (+4.1) and Team 18 (+2.2) gained more than us, and we lost 0.8 in the last 15 min.

## Our strategies: keep / kill / scale
- **Pilar sells (dealer bot, offer-only, small steps): SCALE.** Ladder rose 0.055 → 0.181 today: MAL-07 +0.050, MAL-06 +0.040, SAL-08 +0.019 (that one after a jump), with 0 neg cost. Our L3 slot is the cheapest lever we have.
- **Chato L2 buy at list 26: KILL.** Two threads failed (805 and the one at tick 577: his 33 → 32 vs our 26). None of our above-list Chato buys ever moved the ladder. The only L2 that counted was a sale (LAT-08 at 14, +0.017).
- **SAL-06 from Abuela (cap 25): KEEP, but tied to the Pilar resale only.**
  - Three threads so far, no deal (29 → 25, held).
  - At 25 the buy costs −2.5 neg (our value is 22.5).
- **Trading loop: KEEP, no evidence.** trader.jsonl shows 0 buys or sells on Saturday, only open/closed events. Its thresholds (+3 / +6) never triggered.
- **Maker book (9 asks): KEEP but REPRICE.**
  - The last fill was at tick 404 (MAL-03 +2.0). The last sale was tick 351 (SAL-01 +4.7).
  - 226 ticks since then with no neg movement.
  - Team-to-team commons now clear at 5 (ticks 595-610); our asks sit at 7-9.
- **In-room / addressed team buys: KEEP.** RET-01 from t10 at 20 hit the +50 cap (tick 276). The lunch bargain watch has logged 0 hits, and no ask on El Rastro qualifies (the highest is LAT-06 at 25).
- **Duels (Aleks): KEEP.** 9 deals in the last 10, 13.93 duel points. The Duels II integrative change is Aleks's call at 15:30.

## Check the scout
- **Holds:**
  - Pilar's uncommon band 16-19 (median 18 over 5).
  - The ladder figures +0.050 / +0.040 / +0.019.
  - LAV-11 lost to Pilar at 140.
  - Team 14 selling RET commons at 9 (ticks 591-598).
  - Team 15's 0-P swaps with t07.
  - The 2.7 gap to #1.
  - The mm_points swing from +4.99 to −5.2.
- **Wrong: "neg_points unchanged if bought at ≤ value".** The cap is 25 but SAL-06 is worth 22.5 to us, so a buy at 23-25 costs −0.5 to −2.5.
- **Wrong: "sell to Pilar at ≥ 25".** Her SAL final was 23. Team 4 got 25 once; that is not our base case.
- **Wrong: "Team 10 rose trading on its own venue v10".** GAME.md shows v10 trades moving OUR mm_points.
- **Wrong card in the swap list.** Tick 613 was LAV-03↔MAL-08, not LAT-03.
- **Gap: "Pilar sells of spares".** We hold no spare uncommons; every LAV and RET uncommon is a page card worth 100+. Any L3 sale needs a card we buy or pull first.
- **Irrelevant evidence for the bargain watch.** "t04 LAT-09 bid 64" is a bid, not an ask we could buy.

## The 3 changes with the highest expected gain
1. **Open the sobre_plata pack (worth 92.9 unopened) as soon as the API allows. Operator.**
   - Any pulled uncommon or rare outside our complete LAV/RET pages becomes a free Pilar L3 candidate (offer-only, steps of −2/−3, close only at ≥ our value).
   - Effect: removes the unopened-pack drag (~1-4 per trade [L]). It may replace the weak SAL-08 slot (+0.019) without a −2.5 buy: ≈ +0.02 ladder ≈ +0.7 board at 0.33 per 0.01.
   - Risk: the contents are unknown; opening itself scores nothing.
2. **SAL-06 chain, with tighter limits. Operator.**
   - Buy from Abuela at ≤ 23 instead of 25: cost ≤ −0.5 neg.
   - Resell to Pilar opening ~30 and stepping −2/−3; floor 23 (her SAL final).
   - Skip this chain if the pack (change 1) yields a Pilar candidate.
   - Effect: replaces the +0.019 slot with up to +0.040 ≈ +0.7 board for about −0.05 board of neg.
   - Risk: her second-thread finals run lower (MAL-06 second thread ended at 17). Then we hold SAL-06 at no extra loss.
3. **Reprice the spare book toward clearing. Operator via book/trade.py.**
   - Spares to 5-6: LAV-02/03/04 seconds (worth 3.2), SAL-02 (2.2), LAT-04 (1.2). Gain +1.8 to +4.8 each, ≈ +12-15 neg ≈ +1.1-1.4 board if all fill.
   - Retarget to buyers who collect the set: LAV → t04/t07/t09; LAT → t16/t15.
   - Pull MAL-02 and MAL-04 → t15: t15 dumps MAL at 5, and our single copies are worth 7, so never sell them below 8.
   - Risk: still no fills (asks have taken a median of 4 ticks only 5% of the time). Reprice again after 10 min.
