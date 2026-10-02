# Scout (claude-sonnet-5-5, Fri 22:50)

## Top 3 actions now
1. **Cancel bid 2563 (76 for LAV-09 to chato) unless we hold LAV-06/07/08 and test `GET /api/me/value?card=LAV-09` first.** We hold LAV-06, 07, 08, so run the test now (human or `trade.py`). Evidence: Chato's price is 97 → 95, our bid is 76, and Chato ladder purchases above our value subtract (MAL-07 −11.8). Team 10 already holds LAV-09, so this may be a different copy. Effect: if the value is ~91, we avoid a possible loss. If ~177, a dealer buy still scores 0 and only a TEAM seller scores. Confidence: med.
2. **Sell the spare commons to teams, maker-side, at the market's bid.** Offers 2173 (MAL-06 at 22 to t15) and 2174 (LAV-04 at 9 to t07) expire at tick 161, so relist them at the same price. Add LAV-02, LAV-03 and the second copy of LAT-04 at 9-10 (team asks sit at 9-10). Evidence: LAV-04 at 9 to t07 gave +7.7, and SAL-06 at 26 gave +6.0. A 2nd copy is worth only 25% of book, so we gain about +4 to +6 each. Executor: `trade.py` list. Confidence: high.
3. **Ask Lucas to sell MAL-07 and MAL-06 to t17 (rank #4, collects MAL/SAL).** t17 bid 70 for MAL-09 and bought MAL-08 at 28 (tick 147). Ask 26-28 addressed `to` t17, so they pay the fee. Our value is 17.5, so the gain is +8.5 to +10.5 each. t17 is above us but 5 places below the leaders, and the sale is small. Confidence: med.

## What the climbing teams are doing
- Team 17 (+9.5 over 60 min) buys MAL and SAL from teams: SAL-09 at 75 (tick 109), SAL-06 at 26 (tick 119), SAL-08 at 35 (tick 124), MAL-08 at 28 (tick 147). Our SAL-06 sale to them scored +6.
- Team 12 (+5.6) sells SAL rares and uncommons to t17 and t18 (SAL-09 at 75, SAL-08 at 35). It also buys LAV cheap (LAV-05 at 7 from t15, tick 149) and runs the zero-fee venue v02.
- Team 13 (leader, 23 deals) is mostly a MAL/SAL buyer (MAL×4, SAL×2). Our dealer flips lost points (neg_points 27.8 → 19.8), so we should not copy that.

## Threats
- Our neg_points fell 27.8 → 19.8 at tick 147 (−8.0), from the Chato sell of LAT-08 at 13 (worth 12.5) and the Abuela sell of LAV-05 at 5. Do not sell to dealers. Team bids for LAT-08 were ~22 est. (Team 15).
- Team 10 holds LAV-09 and a complete page, and t04, t07, t14, t09 and t1 are all collecting LAV. LAV-06/07/08 cards could be worth more to them, but never sell them to Team 12, which is a leader and also collects LAV.
- The ladder part is at its cap (~12.4) and erodes as others fill Chato slots. Our score fell −3.0 over 15 min while neg_points dropped, so avoid any further dealer deals above our value.
