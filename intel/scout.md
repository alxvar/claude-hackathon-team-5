# Scout (claude-sonnet-5-5, Sun 09:27)

## Top 3 actions now
1. **Close the Abuela CHA commons (CHA-02..05) at ≤ 9, using the Operator's `abuela_bot.py --dealer`.**
   - **Evidence:** CHA-01 closed at 8 (her 12 → 8), and the L1 ladder went 0.057 → 0.075 in that window. The CHA-02 thread 2258 is open (her 12 → 10, ours 6).
   - **Method:** small steps, never jump to her bid.
   - **Effect:** neg_points 0 (gain clipped, value 16 vs price ≤ 9); ladder +0.015-0.018 each. Confidence: high on the ladder, low on board effect (Chief 17:45 note: ladder is flat for the board).
2. **Keep the public CHA uncommon bids alive: 20329 (CHA-08 at 22, expires 1550) and 20536 (CHA-06 at 21, expires 1569).** The Operator renews them before expiry at no more than 22 (the public hard limit).
   - **Evidence:** our value is 40 (CHA-07 shows 40). A fill with us as maker means no fee, so about +18 neg_points per card, less pack drag.
   - **Caveat:** the asks list shows no CHA ask from any team right now, and the open bids are ours only. Fills depend on a seller appearing.
   - **Page closer:** goes addressed on El Rastro with the seller's fee added (07:25 directive).
   - **Confidence:** med.
3. **Finish the Pilar fodder: LAV-07 spare (ask 30 to Pilar, offer 20599, expires 1502).** The Operator re-posts it before expiry with steps of −2/−3, floor 17.
   - **Evidence:** LAT-06 → Pilar at 18 (her 16 → 18, ours 30 → 26) gave L3 +0.022. Earlier steady steps gave +0.040.
   - **Effect:** neg_points 0, ladder +0.02. Confidence: med.

## What the climbing teams are doing
- **t12 (#2, +2.0 in 15 min, 70 deals)** buys cheap, mostly LAT: LAT-10 from t01 at 86 (tick 1304), LAT-06 from t09 at 20, LAV-08 from t08 at 14, RET-11 from t06 at 216. Its profile lists LAT as 8 buys, and the Sat close added +7.03.
- **t10 (#1, 34.8, −2.8)** is falling but still leads. Its profile says it collects LAV/RET.
- **t13 (90 deals, 24.4)** trades volume: SAL-11 epic from t18 at 238 (tick 1494) and SAL-10 from t13 → t09 at 68. Its trades don't move it up; its score is flat (−0.6).
- **We're #3 (+0.3).** Everyone else dropped 0.6-2.8 while our CHA setup held at neg 0.0.

## Threats
- **t12 (#2) is the one racing us.** Never sell it LAT-08, MAL-03 or MAL-08; its gaps are LAT/MAL/RET. We hold LAT-01/03/04 and MAL-01..05; none go to t12 or to any rival.
- **t03's bid for SAL-10 at 92 (offer 20570).** We hold SAL-09 and SAL-10 (value 122.6 each), so a sale at 92 loses about 30 and feeds #5. Don't take it.
- **Club routing:** keep every club pair on v10 or a member market, never v02/v07/v18.
