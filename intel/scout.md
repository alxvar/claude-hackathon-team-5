# Scout (claude-sonnet-5-5, Sat 12:02)

## Top 3 actions now

1. **Chato ladder test: sell MAL-07 (17.5 value) to Chato, offer-only, after Duels I (trader restarts after 12:10).**
   - Evidence: Chato buys uncommons at 13 (his list; the 458 conversation was 13 → 14 against our 30, closed without a deal). The Analyst's model says every dealer deal at or below the menu list counted. Our best 3 Chato ladder deals are all 0, and +0.01 ladder ≈ 3.5 neg_points.
   - Executor: operator with `abuela_bot.py --dealer chato --offer-only`; one thread, alone in its window, and never at his opening price.
   - Effect: a loss of ≤ 3 neg_points (MAL-07 is worth 17.5 against his ~14-15 buy price) buys a measurable Δladder. Continue with MAL-06 and LAT-08 only if it moves.
   - Confidence: med-low. Our ladder is 0.055 and the pattern is only [L].

2. **Hold the 11 addressed asks (6605-6881) to collectors and keep them short-lived.**
   - The buyers are t09, t03, t15, t07, t06 and t16 (t17 and t01 were pulled as they are above us). All are below us on the board.
   - Expected gain, from the 5 rows in the metrics sell table: LAT-04 +6.3, LAT-08 +5.5, LAV-02/03/04 +4.3 each, about +25 neg_points if all fill. Gains are not capped at the trade level.
   - Executor: `book.py` is already running. Re-check the top 4 before each post (t14 collects LAV/LAT, so no LAV-02/03/04 or LAT sale to t14).
   - Confidence: med. Only a few asks have filled so far (SAL-01 at 7, MAL-03 at 5), and the market asks are 9-10 for commons.

3. **Pilar ladder (L3), from ~12:21: sell SAL-08 (22.5) and spare uncommons to her.**
   - Evidence: the Pilar uncommon sale median is 18 over 1 trade, and she pays over book for SAL/RET. The Sat 11:56 directive puts Pilar after the Chato test.
   - Executor: operator, offer-only, at ≥ our value and her list buy price. Level 3 may be locked for us (we have 0 Chato deals that count), so first test whether she opens.
   - Effect: L3 ladder weighs more per the rules, but the weight is not in the data.
   - Confidence: low.

## What the climbing teams are doing
- **Team 17 (+3.8 in 15 min, +7.0 in 60 min)** is a MAL/SAL/LAV collector. It bought SAL-07 from Team 10 at 26 (tick 398) and has MAL×3, SAL×3 buys. It is now above us.
- **Team 14 (+5.9 in 60 min)** is #2, buying LAT×4, RET×2 and LAV×1. The tick 370 RET-08 at 20 from Team 13 (to Team 14) is a below-value buy.
- **Team 13 (+2.2 in 15 min)** is #1 with 45 deals. It buys MAL×6 and SAL×2 from teams, and its ladder runs through Chato and Pilar deals at list.
- **Team 6** is buying rares from teams: SAL-10 at 76 (from t01) and LAV-10 at 82 (from t16).

## Threats
- **Rare bids vs us:** Team 2 bids SAL-09 at 69 and RET-10 at 50, Team 6 bids SAL-09 at 68. Our own RET-10 is worth 149.9 to us. Do not sell it.
- **Value created on v10 can go negative:** our `mm_points` is −5.2 after the t10 → t15 SAL-07 trade. Keep v10 trades collector-to-collector only.
- **Feeding Team 14 and the other top 4:** t13 bids 2 P for our RET commons (2 each), and t14 collects LAV/RET/LAT. No sales to the top 4.
