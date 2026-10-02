# Scout (claude-sonnet-5-5, Fri 22:35)

## Top 3 actions now

1. **Reprice our sells to the live bids, via `trade.py` list (maker-side, no fee).**
   - SAL-06: t06 bids 23 (offer 2134). We no longer hold SAL-06 (sold to t17 at 26), so skip it.
   - MAL-06 / MAL-07: our offers 2173 and 1853 are at 22 and addressed to t15. t15 bought MAL-07 at 26 (tick 98) and MAL-06 at 21 (tick 103). Asks elsewhere: MAL-07 30 (one ask). Keep them at 22 for t15.
   - Value is 17.5 each, so +4.5 each at 22.
   - LAV-04 (our 2nd copy, value 3.2) is at 9 to t07. t07 bought LAV-04 at 9 (tick 106). The expected gain is ≈+5.8.
   - Confidence: med. t15 and t07 are below us on the board (t15 is last; t07 is #13 in the profiles).

2. **Sell LAT-03 and LAT-04 (value 5 each) to t08 or t14, not just t15.**
   - Offers 1869 and 1870 at 10 are addressed to t15. t08 bids LAT-07 at 18 and collects LAT. t14 buys LAT×2.
   - t08 is #3 and ahead of us, but the gain is only ≈+5 each. Never hand a leading team more value than we gain, so keep t15 as the target and let the offers run (expire tick 147).
   - Confidence: low-med.

3. **Hold the rare plan (D5) and ask Lucas to find holders now.**
   - Open bids: LAT-09 and LAT-10 at 55 each (offers 1157/1158), SAL-09 and SAL-10 at 37 each.
   - We hold none of these. Only a pack can produce them.
   - If we open `sobre_bienvenida` (worth 46.1) or `sobre_barrio` (14.6) and get a LAT rare, sell it into the 55 bid (≈+20, per D5).
   - Confidence: low. It depends on pack luck.

## What the climbing teams are doing
- **Team 17 (+7.3 / +10.5):** buys SAL and MAL from teams at fair prices. It bought SAL-09 from t12 at 75 (tick 109), SAL-06 from us at 26 (tick 119) and SAL-08 from t12 at 35 (tick 124). It also paid 26 for MAL-07 (tick 98).
- **Team 12 (+5.2 / 60 min):** sells SAL to Team 17, with rares at 75 and an uncommon at 35 (up from the 18 it sold SAL-08 to us for at tick 102). It collects LAV.
- **Chato unlock wave:** t02, t04, t08 and t16 unlocked level 2 between ticks 121 and 132. The ladder cap erodes as the field fills slots (D7).

## Threats
- **Our Chato buy (tick 131):** LAV-06 at 31 (worth 32.5) cost −2.3 `neg_points`. Do not buy LAV-07 from Chato at 31, since it scores below 0.
- **We feed Team 17:** it is a top-3 team and took SAL-06 from us at 26. Do not sell SAL to t17 or t12 again.
- **Score slipping:** we are #9 at 14.9 (−1.5 in 15 min). Teams #10 and below are within about 2.4 points of us.
