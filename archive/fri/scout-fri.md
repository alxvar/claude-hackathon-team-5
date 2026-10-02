# Scout (claude-sonnet-5-5, Fri 23:01)

## Top 3 actions now
1. **Sell the LAV-10 second copy to a team bidder; keep LAV-09.** We hold LAV-09 and LAV-10. Metrics show our LAV-09/10 at 177.1 each, so both look page-boosted. Open bids: t15 bids 20 for LAV-10 (offer 2628), t15 bids 7 and t02 bids 8 for LAV-09. D5 cited "t04 bids 85" for LAV-10, but that bid is not in today's top bids, so it is gone or stale. Action: Lucas checks `GET /api/me/value?card=LAV-10` and asks the room (Lucas/Dani) for a LAV buyer: t04, t07 and t14 collect LAV (t10 holds a complete page already). A sale scores price − our value, and that value may be 177 with the page, so **do not sell below 177 unless the check shows ~22.75**. Confidence: low. Expected effect: not in the data.
2. **Our 2 open sells expire at tick 161: relist them.** Offers 2173 (MAL-06 at 22, to t15) and 2174 (LAV-04 at 9, to t07). Run `trade.py` to relist MAL-06 at 26-28: t17 buys MAL (3 trades) and the t17 SAL-06 sale scored +6.0. Asks by others: MAL-06 28 and MAL-07 30 are on the book. Expected: +5.5 each against our value of 17.5, worth about +0.8 board points each. Keep them maker-side (D8: accepts freeze during duels). Confidence: med.
3. **Sell spare commons to Team 7 and the team bidders at 9-10.** Spares: LAV-02, LAV-03 and LAV-04 (2 copies each, value 3.2), LAT-04 (1.2), SAL-02 (2.2). Team 7 (#13, buyer for LAV/LAT) bought LAV-05 at 9. Our LAV-04 sold at 9 for +7.7. Asks at 8-10 show the market level. Expected: +4 to +7 each, `trade.py` list `to` the buyer. Confidence: med.

## What the climbing teams are doing
- **Team 17 (+9.6/60 min)** buys MAL/SAL from teams: SAL-09 at 75 from t12 (tick 109), SAL-06 from us at 26, SAL-08 at 35 (tick 124, page bonus ~+45), MAL-08 at 28 (tick 147). It now bids 70 for MAL-09.
- **Team 12 (+6.9)** sells SAL/MAL/LAT to the climbers (SAL-09 75, SAL-08 35) and collects LAV. It is a leader, so don't feed it.
- **Our own jump (+6.1/15 min)** came from one team buy: LAV-05 at 8 from t06 gave +50.0 `neg_points` at tick 152, probably the page bonus. Chato buys scored −2.3 and −2.0.

## Threats
- Team 10 holds a complete LAV page. t04, t07 and t14 also collect LAV and compete for the same sellers.
- t13 (30.0) and t12 (27.9) lead; t13 buys MAL×4 and SAL×2 from teams. Do not sell them MAL/SAL.
- Team 17 bids 70 for MAL-09 and t18 bids 62 for LAT-09/10. We hold neither, so those are for pack pulls only (D5).
