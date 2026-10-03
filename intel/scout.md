# Scout (claude-sonnet-5-5, Sat 14:19)

## Top 3 actions now

1. **Close the two swaps already on the book (offers 9172 → t15, 9173 → t07, both expire tick 650). Executor: Operator, via `trade.py`; Lucas can nudge t15 and t07 in the room.**
   - Evidence: t15↔t07 swapped 3× at ticks 607-616 (0 P each). 9172 gives LAT-04 (2nd) + MAL-04 for SAL-07, about +14.3 for us. 9173 gives LAV-02 (2nd) for MAL-01, about +3.8.
   - Effect: about +18 neg_points if both fill, with no fee as maker. Both counterparties are #14 and #17, far below us.
   - Confidence: med. The game clock is paused at tick 630, so expiries may slip.

2. **Hold the SAL-06 Abuela thread 868 (her 29, our 21) only up to cap 25, and don't chase it with a Chato buy.**
   - Evidence: Abuela's SAL-06 offer went 29 → 27 → 25 and stopped at 25 against our 22. Chato offered 32 against our 26. Pilar's uncommon sale median is 18, and the Chief's plan has us re-selling to Pilar at ≥25.
   - Expected effect: a buy at ≤25 costs 0 neg_points if SAL-06 is worth ≥25 to us. Its ladder value comes only from the Pilar resale, which is uncertain. Resale at 25 vs her 18 median is not in the data as achievable.
   - Confidence: low. The resale price is unverified, and her finals land around 18-19 for uncommons.

3. **Pilar sells: move spare uncommons to her with small steps (−2/−3) and offer-only, to lift the L3 ladder (now 0.181).**
   - Evidence: MAL-06 at 19 with small steps gave +0.040, while SAL-08 after a jump gave +0.019. Pilar's median uncommon sale is 18 over 5 deals in the last 60 ticks.
   - Effect: roughly +0.02 to +0.04 ladder per sale, replacing our weakest L3 slot. Only sell at ≥ our value. This needs a spare uncommon, and our holdings list shows none outside the page sets (the SAL-07 from action 1 would be one).
   - Executor: the Operator with `abuela_bot.py --dealer pilar --ladder --offer-only`.
   - Confidence: med.

## What the climbing teams are doing
- **Team 14 (#1, 30.8)** sells RET commons at 9 to t04, t09 and t15 (ticks 591-598) while it collects LAV/LAT. It also buys SAL-03 at 5. It is a steady volume seller of dumps.
- **Team 15 and Team 7** swap card-for-card at 0 P (ticks 607-616, LAV-08↔LAV-06, LAT-03↔MAL-08, MAL-01↔SAL-02). Each side moves a dump for a collected card.
- **Team 10 (#3, +4.1 per hour)** bought MAL-10 at 74 (tick 585) and sells SAL (SAL-10 → t06, per Lucas's plan). Team 6 (+4.6 per hour) lists 296 offers.

## Threats
- **Team 13 (#7, 57 deals)** is bidding 2 P for our RET commons (RET-01/02/03). It is a lowball and nothing to fill; it also runs the v03 venue.
- **Team 4** bids 27 and 26 for RET-08 and RET-06 and 64 for LAT-09. It competes for RET uncommons, and we hold RET-06/07/08 for our page.
- **Our score is slipping:** −0.8 in 15 min, with Team 10 (+4.1) and Team 18 (+2.2) rising within 1-2 points of us. The lunch pause freezes this, but anything that feeds #1-#4 is a threat.
