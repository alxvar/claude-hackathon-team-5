# Scout (claude-sonnet-5-5, Sat 11:56)

## Top 3 actions now

1. **Chato ladder test: SELL MAL-07 to Chato in offer-only mode, only if Duels I leaves ≤2 threads open (Operator, `abuela_bot.py --dealer chato --offer-only`).**
   - Evidence: the Analyst model (11:56) says every dealer deal at or below the MENU list counted, and +0.01 ladder ≈ +0.54 board. Our ladder is 0.055 and our Chato best-3 are all 0. Chato's uncommon buy list is 13 and his sell menu is 26. MAL-07 is worth 17.5 to us and ask 6621 is addressed to t15 at 20.
   - Effect: ≤3 neg_points of loss, plus cash. Measure Δladder on the first deal and continue (MAL-06, LAT-08) only if it moves; a Chato SELL at or below his buy list has not been tested yet.
   - Pull our t15 asks on that card first so it is not double-sold.
   - Confidence: med-low. The pattern is [L], and a sell sits on the other side of his book.

2. **Hold the maker book to collectors below us; keep 6447 SAL-08 at 25 → t03 and 6609 LAT-08 at 20 → t03 live (book.py).**
   - Evidence: t03 is #13 (17.8), collects SAL/LAT, and prices u 28. Our SAL-08 is worth 22.5, so +2.5 on a maker fill with no fee. SAL-08 also expires at tick 463, so it needs a re-post at 25 with a 2× ticks ask. Only Team 15 and Team 7 appear as sell-side targets elsewhere (est. gains +4 to +6 on LAT-04, LAV-02/03/04 at 9.5 to t07).
   - Effect: about +2 to +6 neg_points per fill, with no feeding risk.
   - Confidence: med.

3. **Price check on the t15 asks (6620 MAL-04 at 9, 6621 MAL-07 at 20, 6681 MAL-06 at 20, 6682 MAL-02 at 9).**
   - Evidence: t15 (#15, 15.9) collects RET/LAT/MAL and prices u 23, c 8. Chato's uncommon sell price is 14 over 3 deals, the El Rastro uncommon clearing is 24.5 and MAL is 26. We value MAL-06/07 at 17.5, so 20 gives +2.5 each. MAL-04 and MAL-02 are worth 7, so 9 gives +2.
   - Effect: about +9 neg_points if all four fill. If unfilled for 10 minutes, drop commons by 1 (to 8).
   - Confidence: med-low. Only 9% of bids fill.

## What the climbing teams are doing
- **Team 14 (#1, +5.4 in 15 min, 21 deals).** It collects LAV/RET/LAT and bought RET-08 from t13 at 20 at tick 370, below our RET uncommon value. Its jump with only 21 deals suggests ladder or value points rather than volume [L].
- **Team 17 (+3.8 in 15 min, 20 deals).** It buys MAL×3 and SAL×3 as a collector. Its rise past us is why the 11:54 re-addressing moved MAL-06/02 off it.
- **Team 13 (45 deals, #2).** It buys MAL×6 and SAL×2. It unlocked Pilar early via "3 deals with chato" at tick 262, and its lead is Friday +3.3 + Saturday ladder ~+4. Its own deal volume feeds its venue v03.
- **Team 6** is closing SAL: it bought SAL-10 at 76 from t01 and LAV-10 at 82 from t16, and has SAL×3 in total. Public top bids are SAL-09 at 69 (t02) and 68 (t06).

## Threats
- **Feeding t15 and t03:** both are low-ranked, so they are safe today. Re-check the top 4 before each post, because t17 and t01 just rose above us.
- **We are #10 at 22.66, down 6.4 in an hour.** Ranks 6-9 (24.5, 23.9, 23.2, 22.7) sit within 1.8 points. The ladder gap, not trade volume, is the lever.
- **Value created on v10 can go negative (mm_points −5.2).** t10 is now top 4, so no v07 offers. Trades on v10 should only be collector-buys.
