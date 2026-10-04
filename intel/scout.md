# Scout (claude-sonnet-5-5, Sun 10:59)

## Top 3 actions now
1. **MAL-07 (last or non-last card), addressed bid to t03 on El Rastro. Done by the mal_close.py executor, or by Lucas by hand.**
   - Evidence: the feed shows MAL-07 went t15→t03 at 9 P (tick 1647). Our plan "MAL-07 → t15" is stale, and t03 holds it.
   - Price: ≤ 17 while it is a non-last card (value 17.5). If it is the last MAL card, the cap is value-when-last − 50. Get that value from `/api/me/value`; the figure is not in the data.
   - Effect: closes the MAL page at ~+50 neg_points (the trade part is uncapped per the Analyst).
   - t03 (#5, 29.1) bought at 9, so a low bid does not feed it. Check t03's price against its own value before posting.
   - Confidence: med.
2. **Keep MAL-09 bid 22816 (48, to t08, expires tick 1930) alive.**
   - Repost ~15 ticks before expiry if it is unfilled.
   - Once MAL-07 is held, make MAL-09 the last card and lower the price to ≤ value-when-last − 50.
   - Our MAL-09 value is 49 (MAL-10 is worth 49 and is a rare); the page bonus comes on top of that.
   - Effect: +47 to +50 neg_points in total. A previous Pícaros attempt was a bait-and-switch, so use team trades only.
   - Confidence: med-low, since t08 has been silent all weekend.
3. **Defend #3: sell nothing and accept nothing.**
   - We are #3 at 32.4. t10 is 0.2 behind (32.2) and t18 is 1.0 ahead (33.4).
   - Ignore the t16/t07/t09 bids on CHA-06..10 (15-64 P). Our copies are worth 146-218 each and we have no spares.
   - Do not accept asks on LAT/LAV/SAL commons. We hold the pages and the cards are worth ≤ 5 to us.
   - Effect: protects 50 neg_points and the page bonuses. Confidence: high.

## What the climbing teams are doing
- **t12 (#1, 34.6, 77 deals):** buys LAT×8 in team trades and holds RET-11 (216 P from t6, tick 1245). It closed LAV-07 from t13 at 40 (tick 1712).
- **t18 (#2, +2.3 in 60 min):** collects CHA and RET and bought a CHA card. Its SAL-11 sale to t13 was at 238 P. It is our #3 rival.
- **t02 (#9, +2.3 in 60 min):** is buying epics: RET-11 from us at 240 (tick 1730) and SAL-11 from t04 at 220 (tick 1858). It also bought CHA-05 from us (tick 1585). Epics and page closers lift teams quickly.
- **t13 (#6, 99 deals, 1192 listings):** is the most active trader and a broker. It is +2.4 in 60 min, so it is climbing through volume.

## Threats
- **t03 (#5, 29.1):** holds MAL-07, our missing MAL card, and buys SAL/LAT/LAV. It is 3.3 behind us. Do not sell it any SAL/LAT/LAV page closer.
- **t18 (#2):** collects CHA and RET and is rising. Any card we sell or any v10 pair that helps t18 or t12 narrows the gap.
- **t13 and t10:** t13 is #6 on activity, and v10 reward buys must exclude t10/t13 per the Chief. t10 is 0.2 behind us but falling (−0.9 in 15 min).
