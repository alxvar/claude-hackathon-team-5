# Scout (claude-sonnet-5-5, Sat 10:48)

## Top 3 actions now
1. **Hold the maker book and take no accepts from 11:50 until Duels I ends** (Operator / `book.py`, trader stopped per the 10:35 directive). Evidence: 12 offers are live and expire at ticks 338-344, while `neg_points` is flat at 28.5 over 15 min and cash is 107. Duels I has 34 duels, and a missed duel deal is worth 0. Effect: protects duel surplus, with no change to `neg_points`. Confidence: high.
2. **Reprice the asks that sit above the clearing price.** The offers are addressed (to t03, t17, t01, t15 and others), so the hand-priced ones are on El Rastro.
   - SAL-08 → t03 at 26 (our value 22.5; SAL-08 clears at 24.5). Hold at 25 or above, since the floor is value+1 as maker.
   - MAL-06 and MAL-07 at 23 each, against the 24.5-26 clearing price and Team 10's MAL-07 sale to t01 at 14 (tick 311). Hold for now; they sit at about 17.5 value, and the floor is 20 per the book.
   - LAT-08 → t15 at 22 (expires 338). Value 12.5 and the clearing price for LAT uncommon is 21.5, so keep it.
   - Executor: `book.py` (it reprices after 20 unfilled ticks). Effect: about +5 to +10 `neg_points` if filled (maker, no fee). Confidence: med.
3. **Spare commons stay at 8-9.** Team 2 bids only 1-3 for LAV-02 and RET commons, and Team 13 bids 2. The live asks at 8-9 (LAV-02 → t09, LAV-03 → t07, SAL-01 → t06, SAL-02 → t16, MAL-02 → t17, MAL-04 → t15) match the clearing price of 9. Do not undercut below the book floor. Effect: about +2 to +6 each, mostly cash for CHA on Sunday (~300 P). Confidence: med.

## What the climbing teams are doing
- **Team 18 (#1, +16.3 in 60 min)**: collects RET and LAT. It paid 49 for RET-02 from t02 (tick 230), as a page-completer, and RET-02 was also taken by t15 at 10. It is the top team, so it must not receive our RET spares.
- **Team 2 (#2, +15.3 in 60 min)**: sells RET-02 (t06→t02 at 12, then t02→t18 at 49) and RET-07 (t02→t15 at 24), then bids 25 for RET-10. The pattern is buying commons at 12 and flipping them to a page-closer at 49.
- **Team 12 (#3)**: its +4.1 in 60 min is smaller than Teams 18 and 2, and it sits at 30 deals.
- **Team 14 (#5, 14 deals)**: climbing slowly (+5.9) on LAV/LAT team trades. No Team 14 trade appears in the last-12 list.

## Threats
- **Team 2** bids 25 for RET-10, and we hold the only RET rares we know of. Do not sell RET-10 (worth 149.9 to us). It would feed a top-4 team.
- **Team 13 (#6, 36 deals)** lobbies on its own venue v03 and takes value-created points from other teams' trades. Keep our book on v07 and El Rastro.
- **Our #4 lead is thin**: Team 14 is 0.9 behind (24.4 vs 23.5). Team 18 is also 6.2 ahead of us at 30.6, so a swing in either direction is possible.
