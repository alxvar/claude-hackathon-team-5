# Scout (claude-sonnet-5-5, Sun 12:46)

## Top 3 actions now

1. **MAL-09 closer: keep 26022 live (t08, 60, exp tick 2308) and re-post to t13 at 60 on expiry (mal09_bid.py, Operator).**
   - Evidence: MAL is 9/10 and value-when-last is 95.4, so a 60 bid gives about +35 (neg 54.8 → ~90). Picaros walked at 56-58 against our 44 cap, so a team seller is the only route. Cash is 647.
   - Effect: about +35 neg_points, which is ≈ +1.75 board at 0.05/pt.
   - Caveat: the price must stay ≤ 95.4 − 50 = 45.4 for the full +50 clip. At 60 it is +35.
   - Confidence: med. A fill depends on t08 or t13 holding MAL-09; no holder is confirmed in the metrics.

2. **CHA-11 (epic): hold bid 25784 (t08, 240, exp tick 2303). If it lapses, re-post once at 240 to t08 (cha11.py, Operator).**
   - Evidence: CHA-11 is worth 288 to us, so 240 gives +48. t10 sold CHA-11 to t06 at 184 (tick 2228). Epics bid on El Rastro now: t03 184 (SAL-11), t17 112, t07 99.
   - Effect: about +48 neg_points.
   - Caveat: t16 refuses and t10 is a rival, so t08 is the only sensible seller. The Chief noted t08 "sells at 240".
   - Confidence: med.

3. **Raise the 12 P bids for LAT-06/07/08 (25488, 25564, 25565) as ladder fodder. Re-check Pilar and Chato first.**
   - Evidence: the Pilar sale of Teatro Valle-Inclán at 17 closed as a deal at tick 2105. Chato's LAT-08 sale at 14 moved the ladder +0.017. Pilar's L3 ladder pays about 3× L2.
   - Effect: ladder +0.02-0.05, but `negotiating` stayed flat while the ladder rose (21.88 unchanged across ladder 0.373 → 0.437). Treat the board effect as ~0.
   - Confidence: low. Do this only if cash is left after actions 1 and 2.

## What the climbing teams are doing
- **Team 6** (+1.4 over 15 min) bought CHA-11 from t10 at 184 (tick 2228) and LAT-09 from t01 at 44 (tick 2129). It is closing pages with epic and rare buys.
- **Team 16** is stacking CHA. It took CHA-10 and CHA-09 from t15 at 65 each (ticks 2022 and 2065) and CHA-01 from t13 at 40 (tick 2189). Its listed gains are mostly small.
- **Team 1** bought RET-09 at 40 and RET-10 at 33 from t17 (ticks 2265, 2268), well under the 70 rare book. It is a buyer of cheap RET rares.
- **Team 10** is level with us (34.2 vs 35.4). Its v10 value_created jumped to 114.4 through the CHA-11 sale.

## Threats
- **Team 10 (#2, +0.8)** and **Team 12 (#3, 34.1)** are within about 1.3 points of us. Never sell them a closer. Team 10's CHA-11 sale to t06 fed its own venue.
- **Team 18** has bids out for MAL-09 and MAL-10 at 25 (offers 25495, 25496), plus LAV-09/10 at 35. It is a possible competitor for MAL-09, but its bid is too low to win against our 60.
- **Our own CHA-11 ask** collides with t06, which just bought an epic at 184. If t08 sells the card to t06 first, the +48 is gone.
