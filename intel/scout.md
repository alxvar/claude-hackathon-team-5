# Scout (claude-sonnet-5-5, Sat 10:58)

## Top 3 actions now

1. **Hold the accept line from 11:50 (Duels I) and keep the maker book live.**
   - Action: Operator confirms the trader stop at 11:50 and keeps `book.py` posting as maker. Our deals sit at 33 and the score is 27.8 (#2), up +3.6 in 15 min. We stay in the race by not losing duel accepts.
   - Evidence: the directive says "102 duels today; a missed duel deal is 0". Our 34 finished duels show 10 deals in the last 10 listed.
   - Effect: protects duel points. neg_points are unchanged because the maker book is flat at 28.5.
   - Confidence: high.

2. **Re-price the Team 15 asks and sell the LAT/MAL spares toward clearing.**
   - Action: Operator reposts via `book.py` (maker, no fee). Targets: LAT-08 → t15 at 20 (live offer 4648; worth 12.5), MAL-06 → t17 at 22 and MAL-07 → t01 at 22 (worth 17.5 each).
   - Evidence: team trades cleared MAL-07 t10→t01 at 14, MAL-06 t04→t01 at 20 and LAT-07 t14→t02 at 13. Our asks of 22 for MAL-06/07 sit above those clears. t15 is the top LAT buyer (LAT×6).
   - Effect: roughly +2 to +5 neg_points per fill (price − value), plus cash toward the CHA page (~300 P). Cash is 107.
   - Confidence: med. Drop MAL-06/07 to 20-21 if they have not filled by tick 363.

3. **Bid for RET-10 and the cheap RET leftovers only if they are a spare copy.**
   - Action: no new buy. Team 2's bid of 27 for RET-10 (offer 4867) shows who values our second copies. Operator keeps the extra RET commons and uncommons unlisted.
   - Evidence: t02 (#3, top 4) bids RET-10 27 and RET-03 3. t13 bids 2 on each RET common.
   - Effect: avoids feeding the #3 team. We have no 2nd RET copies listed, so there is no gain from selling. Hold.
   - Confidence: med.

## What the climbing teams are doing
- **Team 18 (#1, 28.3):** collects RET/LAT. It has 27 deals and 11 team trades; the tick 234 sale t13→t15 and the RET-05 t04→t02 at 8 show RET commons clearing at 8-10.
- **Team 2 (#3, 27.2):** buys across sets. Tick 320 SAL-07 at 23, tick 329 LAT-07 at 13, tick 332 RET-06 sold on to t14 at 14, and bids of 68 for SAL-09 and 27 for RET-10. It is a collector with a broad bid book.
- **Team 1 (+3.9 in 15 min, #8):** accumulates MAL/SAL uncommons below value: MAL-07 at 14, MAL-06 at 20, SAL-07 at 23. This is a buyer for our MAL spares.
- **Team 13 (39 deals):** MAL-10 rare bought at 65 (t09→t13) at tick 331. It keeps trading on its own venue.

## Threats
- **Team 18 (#1) and Team 2 (#3) are within 0.6 of us.** Any page-closer or cheap spare sold to them feeds the leaders. The feeding rule excludes them.
- **Team 2 is buying RET cards** (RET-05, RET-06) and bids 27 for RET-10. It may be closing a RET page, which would raise its score by up to +50.
- **Clearing prices are below our asks.** Asks of 22 for MAL-06/07 sit above the 14-20 clears. The book will not fill unless we step down.
