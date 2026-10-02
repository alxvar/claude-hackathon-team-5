# Scout (claude-sonnet-5-5, Fri 22:45)

## Top 3 actions now
1. **Reprice the MAL-06/MAL-07 sells to the live buyer, and send them to a team below us.** Offers 1853 (MAL-07 at 22) and 2173 (MAL-06 at 22) are addressed to t15, which sits #17 and has bought MAL×2. Their expiry is tick 147 (1853) and 161 (2173). t17 (#4, above us) has a MAL-09 bid at 70 and was estimated at 26 for MAL uncommons. Our value is 17.5, so a sale at 22 is about +4.5 and a sale at 26 is about +8.5. Executor: `trade.py`. Keep t15 at 22 and re-list 1853 at 24-26 once it expires. Do not send to t17 if it hands them more than we gain (t17 is climbing, +10.0 over 60 min). Confidence: med.
2. **Move the spare commons through maker-side asks to t07 and t15.** LAV-02/03/04 and SAL-02 each have 2 copies at 3.2 or 2.2. Asks of 9-10 on the spare copies exist (2174 LAV-04 at 9 to t07 is open until 161). The earlier t07 sale at tick 106 scored +7.7. Dani's table gives LAV-03/02 at 9.5 est. (+4.3) and SAL-02 at 9 est. (+4.8, t3/t6/t16/t2 buyers). Executor: `trade.py` lists 1 offer per spare copy, addressed `to` t07 or t02 (low-ranked teams). Expected: +4 to +6 each. Confidence: high.
3. **Keep the LAV-09 bid at 125 only if Lucas wants the page, and say plainly what we know.** D6 says Team 10 holds LAV-09 and has a complete page. Our bid 2353 (125, expires 154) is "to anyone". A buy from a team scores value − price − fee. The LAV-09 value is 91 until the page is measured, so 125 would be about −34 − fee unless the page bonus applies. Run `GET /api/me/value?card=LAV-09` first (needs LAV-06/07, and we hold both). If it reads ~91, cancel 2353. If ~177, the bonus is +34 to +86 and 125 is still +52. Executor: Lucas or `trade.py`. Confidence: med.

## What the climbing teams are doing
- **Team 17 (+4.1 / +10.0)** buys from teams: SAL-09 from t12 at 75 (tick 109), SAL-06 from us at 26, SAL-08 from t12 at 35 (tick 124, a page completion worth about +45). It bids 70 for MAL-09. It collects SAL and MAL.
- **Team 12 (+2.5 / +6.2)** sells rares and uncommons to teams (SAL-09 at 75, SAL-08 at 35). It collects LAV and runs a zero-fee venue.
- **Team 4 (+3.2)** buys LAV×3 and LAT×2 and unlocked Chato at tick 122. Team 8 (+1.5) bids 50 for SAL-09/10 and 29 for LAT-09.

## Threats
- **Our `neg_points` are falling:** 30.1 → 27.8 after the Chato buy of LAV-06 at 31 (−2.3). Chato buys at LAV prices of about 31 against our value of 32.5 give no gain. Stop further Chato purchases above our value.
- **t06 → t15 rare:** LAT-10 sold for 60 at tick 142, and t15 (#17) is now a LAT/MAL collector. This confirms the market for LAT rares.
- **t17 is the buyer for our MAL cards** and is climbing (+10.0). Only sell to it if the gain is clearly above the value it gets.
