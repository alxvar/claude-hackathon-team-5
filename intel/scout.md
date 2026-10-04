# Scout (claude-sonnet-5-5, Sun 13:01)

## Top 3 actions now
1. **Hold the lead: no trades with t10/t12/t18/t03/t04 until 15:00 (GUARDRAIL 13:12).** Operator and trader/opps keep El Rastro floors at 0 (floors_1330.sh). Evidence: we lead at 37.21, t10 is at 34.77 and t12 at 34.19. Our neg_points rose 52.2 → 104.8 (CHA-11 at 190, +50). Effect: protects about 2.4 points of margin. Confidence: high.
2. **MAL-09 (the MAL page closer): let 26452 (t08, 75) expire at tick 2347. mal09_repost.py then does ONE re-post to t01 at 60 on El Rastro (Operator).** Do not buy from t09, who was bidding 56. Evidence: MAL-09's value when last is 95.4, so 75 gives +20.4. The Pícaros held at 58 against our 44, so we walked. Effect: the page-completing trade is capped at +50, so the MAL page would add at most +50 neg_points if the price is at or below (value when last − 50). At 60 the trade does not reach +50 unless the value-when-last is 110 or more, which is not in the data. Confidence: low-med.
3. **Chato L2 fodder: keep bids 26654/26656/26658 (LAT-06/07/08 at 14, value 12.5). lat_fodder sells each fill to Chato at ≥14 or better. Cancel unfilled bids at 13:55 (Operator).** Evidence: our earlier LAT-08 sale to Chato at 14 gave ladder +0.017, and current asks are LAT-06 at 30 and LAT-07 at 29, well above our bid. Effect: ladder +0.017 per fill (ladder 0.364). Cost is about −1.5 np per fill, and the ladder is flat for the board [L], so confidence is low.

## What the climbing teams are doing
- **t01 is a flipper.** It sold LAV-04 at 6 and CHA-06/CHA-08 at 15 each to t09, and traded RET-09 with t17 (t17→t01 at 40, then t01→t17 at 85). It is the only name in these trades that stands to profit from price gaps, and it is not in the top 10 by score.
- **t10 (#2, 34.8, +0.6 over 15 min) is flipping epics.** It sold CHA-11 to t06 at 184 and to us at 190, and its v10 trades feed our market-making score. It also still holds MAL-09, and we are not buying from it.
- **t09 is buying CHA** (CHA-06 and CHA-08 from t01 at 15 each) and has a bid on CHA-07 at 15. It is at 29.0, 8.2 below us.
- **t17 closed RET rares at 85** (RET-09 from t01, 85) and also bought RET-06 from t09 at 19. It bids 112 for LAV-11.

## Threats
- t10 is 2.4 behind. Our own CHA-11 purchase gave it a sale at 190, and by our own estimate (a [L] label) it nets about +10. Any further contact with it feeds it.
- t12 gained +7.03 at the Saturday close and sits 3.0 behind us. t03 holds an open bid of 162 for SAL-11. Neither can be fed.
- MAL-09 is contested: t09 was bidding 56, and t01 holds it. If t08 fills before 2347 at 75, the +20.4 is ours, but a rival buying it first kills our closer.
