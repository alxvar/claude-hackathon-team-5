# Scout (claude-sonnet-5-5, Fri 22:40)

## Top 3 actions now

1. **Reprice our open sells to the bids that exist; do not wait on t15.** Offers 1853 (MAL-07 at 22), 2173 (MAL-06 at 22), 1869 and 1870 are all addressed `to t15`. Offers 1853, 1869 and 1870 expire at tick 147. t15 is #17 (4.7 points) and its fills so far are LAT×5, MAL×2, so it is a real buyer. Our value is 17.5 for each MAL, so 22 gives +4.5 each. Lucas can re-list MAL-06 and MAL-07 at 22-23 as open asks (`trade.py`, no `to`) so t17 and t13 (buys MAL×4) can also fill. Never sell to t13 (leader, rank 1). Expected effect: +4.5 to +5.5 per MAL, so about +9 to +11 for the pair. Confidence: med.

2. **Hold the LAV-09 bid of 125 (offer 2353) and run the free test.** Run `GET /api/me/value?card=LAV-09` once. We hold LAV-06, LAV-07, LAV-08 and LAV-10, so check whether LAV-09 shows ~177 (page bonus) or 91. Evidence: t17 gained about +45 at tick 124 for a page-completing SAL-08 bought from a team at 35. D6 says Team 10 holds LAV-09 and has a complete page. Its 110 bid is gone, and t02 bids only 22 for LAV-09. If the value is 91, cancel the 125 bid: paying 125 would score −34 on a card worth 91 (neg_points counts value − price), so the bid only makes sense at ~177. If it is ~177, Lucas asks the room for the holder; a team sale scores value − price − fee. Confidence: low-med.

3. **Sell the cheap spare commons into open asks and bids near 9-10.**
   - LAV-04 at 9 to t07 (offer 2174) is already out. Our copies are worth 3.2 each, so +5.8.
   - Add LAV-02 and LAV-03 spares at 9.5 to t07 or t09 (team 9 is a LAV buyer). Evidence: t07 bought LAV-02 at 10, LAV-05 at 9 and LAV-04 at 9 (ticks 105-107).
   - Also SAL-02 spare (worth 2.2) at 9 to t03, t06 or t16, which all collect SAL. Each is +4 to +6 per copy; Dani's table estimates +4.3 to +4.8.
   - Keep these offers maker-side so the other team pays the fee. Confidence: med-high.

## What the climbing teams are doing
- **Team 17 (+10 over 60 min):** buys MAL and SAL uncommons and rares from teams: SAL-09 at 75 from t12 (tick 109), SAL-06 at 26 from us (tick 119), SAL-08 at 35 from t12 (tick 124), MAL-07 at 26 from t15 (tick 98). The page bonus of about +45 came from the SAL-08 trade.
- **Team 12 (+6.2):** sells SAL rares to teams (SAL-09 for 75, SAL-10 for 80 earlier) and uncommons (SAL-08 at 35), and collects LAV. It also runs the 0-fee venue v02 (D6).
- **Team 13 (leader, +2.3):** has the most deals (23) and buys MAL×4 and SAL×2. It dumps LAT/SAL/MAL. Chato levels are opening for the field (t02, t04, t08, t16 unlocked), which erodes our ladder cap.

## Threats
- **Our neg_points fell 30.1 → 27.8** after buying LAV-06 from Chato at 31 (worth 32.5, −2.3 including the fee). Do not buy more from Chato at 31 or higher; LAV-07 closed with no deal, which is correct.
- **Leaders buy our sell targets:** t13 buys MAL×4 and t17 sits above us. Offering MAL to t17 at 22 feeds #4, but for +4.5 each that is acceptable. Do not offer to t13, t12 or t08.
- **LAV buyers (t04, t07, t10, t14, t09, t01) are all crowding the same LAV page.** A team seller of LAV-09 may not exist, so the 125 bid may never fill. Cancel it on a test result of 91.
