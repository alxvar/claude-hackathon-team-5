# Scout (claude-sonnet-5-5, Fri 22:16)

## Top 3 actions now
1. **Sell MAL-07 (uncommon, held) to a team at ≥21 P** via `trade.py` list. We bought it at 29 (worth 17.5 to us). Evidence: t15→t17 at 26 P at tick 98, MAL-06 t07→t15 at 21 P at tick 103, and Team 17 and Team 8 are both buying MAL (t17 MAL×2, t08 MAL×4). Effect: +3.5 to +8.5 neg_points at a 21–26 price, which partly offsets the −11.8 from the buy. Price at the market bid level (LOG: LAT-06 filled in ~3 min). Confidence: med.
2. **Buy LAV-06/07 from El Chato at ≤29 P each** via `abuela_bot.py --dealer chato`. Our value is 32.5 each, so we only buy below value. Evidence: Chato is open and we're early (Lucas 22:03). Our ladder score is 0.064 and the best 3 deals per level count, so these fill the level-2 ladder. Effect: ladder up, and ≈+3.5 each only if the price is ≤29. Skip any item priced above our value. Confidence: med (the Chato menu prices aren't in the data, only "chato rare 90, 1 trade").
3. **Hold LAV-09; do not chase.** Human (Lucas/Dani) asks the room who holds LAV-09 (only one exists). Our value is 91. Evidence: Team 4 bids LAV-10 at 85, and an ask for LAV-09 sits at 110 while Team 10 bid 110. Buy only at ≤91 from a team. Effect: a rare trade is the +8 to +15 type jump, but we'd gain nothing above 91. Confidence: low.

## What the climbing teams are doing
- Team 12 (+4.5 in 15 min) sells rares to the leader and to Team 17: SAL-09 to t17 at 75 P (tick 109) and SAL-08 to us at 18 P (tick 102). It also hit level 2 with 4 abuela deals. Single rare sales drive its gain.
- Team 17 (+2.3 / +3.2) is a heavy buyer: it paid 75 for SAL-09 and 26 for MAL-07, and holds the MAL-09 bid at 78. It also bought MAL-04 at 10 and MAL-06/07 uncommons.
- Team 6 (+2.8) sells commons to Team 7 at 9–10 P (LAV-02, LAV-04, LAV-05, ticks 105–107). Small, steady sales.
- Team 13 (#1, 18 deals) concentrates on MAL×4 and SAL×2, and bought SAL-10 rare at 70 P (tick 98).

## Threats
- Team 13 leads at 27.8 and buys MAL×4 and SAL. Selling it MAL cards feeds the leader, so sell MAL-07 to a lower-ranked team (Team 17 at #9, or Team 8 at #3, only if the price is clearly above our value).
- Team 10 bids 110 for LAV-09 and is building the LAV page. It can outbid us, and we shouldn't pay above 91.
- Our neg_points is dropping (26.3 → 24.1). Any further dealer buy above our value costs points. Keep autoflip off.
