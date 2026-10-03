# Scout (claude-sonnet-5-5, Sat 11:41)

## Top 3 actions now

1. **Re-address LAT-04, LAV-02/03/04 and LAT-08 to Team 7 (the only addressee that meets the collector rule and the feeding rule) at 9-10 / 21; the Operator does it via book.py/trade.py.**
   - Evidence: the rival table shows Team 7 (#17, 10.5) collects LAV/LAT, 11.9 below us, with gains LAT-04 +6.3, LAT-08 +5.5 and LAV-02/03/04 +4.3 each. The Operator's log says "no fill there in 50 min" on commons at 9 to t07.
   - Current offers 6224/6227/6425/6427 already go to t07 at 6-10 and have not filled, and Team 7 has only 5 listings and 5 team trades. Whether it has cash is not in the data.
   - Effect: about +4 to +6 neg_points each if it fills; each fill is at most +4.3 in the table, so the total is under +25.
   - Confidence: low-med. Dani should tell Team 7's humans in the room that the offers exist.

2. **After Duels I (~13:30), run the Chato ladder test: one SAL-06/07 buy at his list of 26, alone in its window (Operator, abuela_bot `--dealer`).**
   - Evidence: all 6 of our Chato deals were above his list and none moved the ladder (0.055). Every Abuela deal below list did move it. Team 13 bought at list 26 and unlocked Pilar at tick 262.
   - Effect: cost about −3.5 neg_points. If the ladder moves, do 2 more, then Pilar.
   - Confidence: med that it will move; ladder weights are not in the data.

3. **Keep MAL-06/07 (value 17.5) and SAL-08 (value 22.5) at 20-24 addressed to collectors. Do not sell to t15 or any dumper.**
   - Evidence: the SAL-07 trade at tick 398 (t10 → t15 at 26; t15 dumps SAL) took our mm_points from +4.99 to −5.2 and us from #3 to #7. Offers 6223 (t17, collects MAL/SAL/LAV) and 6238/6240 (t15, collects RET/LAT/MAL) are fine. Offer 6222 (SAL-08 at 24 to t03, which collects SAL/LAT/LAV) is fine too.
   - Effect: it protects the market-making score; the sales add about +2 each.
   - Confidence: med.

## What the climbing teams are doing
- **Team 14 (#1, 29.1, +7.2 in 15 min)** is a LAV/RET/LAT collector with 21 deals. It bought RET-08 at 20 from t13 (tick 370) and has 4 LAT and 2 RET team buys, so it is paying small prices for cheap page cards.
- **Team 1 (+6.5 / 60 min)** buys MAL×4 and SAL×4 and sold LAT-09 at 68 to t16 at tick 386 and SAL-10 at 76 to t06 at tick 376. It takes rares from teams at about 70, not from dealers.
- **Team 6 (#13 in the profiles, +4.1)** has 17 team trades, the most of any team. It paid 82 for LAV-10 (tick 375) and 76 for SAL-10, and it keeps a standing public SAL-09 bid at 68.
- **Team 13** has 45 deals and unlocked Pilar early with Chato deals at list price.

## Threats
- **Our score fell 4.7 in 15 min to #9** (market 12.5 → 7.5, mm_points −5.2). Team 10 (#5) is on v10 and trades with others there, so further negative trades could cost us again.
- **RET rares:** t02 bids 42 for RET-10 and t09 bids 8 for RET commons. We hold RET-01 to RET-10 (every RET card but the page's last one). The page needs RET-11 or RET-12 if they exist; this is not in the data. Do not feed t18, t12 or t14, which collect RET and sit in the top 4 or close.
- **Top-4 membership shifts every snapshot** (Team 14 is now #1). Re-check before each addressed sale of a set card.
