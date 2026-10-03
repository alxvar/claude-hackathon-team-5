# Judge (claude-opus-5-5, Sun 01:41)

## Verdict
Holding at #3 with 30.49, 7.1 behind Team 10 (37.6) and 0.8 behind Team 18. Team 12 is 0.1 behind at 30.4. `neg_points` has been flat at 119.1 since tick 988, about 450 ticks with no scoring deal.

## Our strategies: keep / kill / scale
- **Team trades (Rastro asks and bids)**: SCALE. They are our only Saturday scorers after the flags: t07 swap +15.5 (tick 904), t08 SAL-06 close +40.4 (tick 988), worth about +0.05 board per point. After 414 listings, only 2 addressed asks are live (19979, 19981), and addressed asks fill 0.3% vs 3.5% for open asks.
- **Trading loop**: KEEP, but fix it before 09:00.
  - It made 2 accepts all Saturday (6.2 and 15.5).
  - Its log ends in an `unknown_card sobre_bienvenida` error every minute (22:41-22:45) and repeated DNS failures (22:55-23:24).
- **Dealer bot, CHA buys and fodder sales**: KEEP within the directives.
  - Ladder rose 0.437 → 0.483, but `negotiating` did not move across ladder 0.373 → 0.437 [L, Chief 17:45]. Log the board after each fodder sale.
- **Pícaros spare sales**: KILL. The LAV-04 thread ended with her final 4 = her opening (no ladder) against our value 3.2, and she was walked from.
- **Idle dealer threads**: KILL. The 1367-1370 threads all closed at the dealer's first price with no price from us. They are no gain and use thread slots.
- **Flags**: DONE. Net +20, and the cap was confirmed at 17:43.
- **In-room / club trades on v10**: KEEP per directive 01:10. There are no negatives so far (directive 01:40).

## Check the scout
- **Holds**:
  - Offers 19979/19981 at 6 vs value 3.2, expiring at tick 1455.
  - Round-2 reset precedent (67.8 → 0).
  - CHA rare value 112.
  - Cash 392 below the 464 floor, so the trader is sells-only.
  - Open-vs-addressed fill rates.
  - t16's 18 bid for RET-06 is below our 100.4.
  - The SAL close at +40.4.
- **Wrong: Team 10 and epics.** "Team 10 sells epics… MAL-11 to t10 at 195". t10 BOUGHT MAL-11 from t08; it sold SAL-11 at 207.
- **Wrong: v10.** "Don't route club trades through v10… Team 10's venue" confuses our venue v10 with Team 10. Our `mm_points` moved on v10 trades (ticks 311 and 398), and directive 01:10 puts 2 of 3 club deals there.
- **Weak: Team 18 "below the ~86 others paid".** That rests on one trade (t12 at 86).
- **Conflict: sell LAV-02 spares.** Directive 00:44 sends 3 spare LAV commons to the Workshop. Saturday's Workshop gave +11.8 collection value, against about 3.9 total for selling 3 × 1.3. Sell only the LAV spares left after the Workshop.
- **Missed: MAL cash gap.** Cash 392 − CHA case-B 288 = 104, below the ≥150 P MAL GO threshold (directive 01:40). The Sunday grant size is not in the data.

## The 3 changes with the highest expected gain
1. **Fund the MAL close before CHA spending locks cash (Operator, 09:00).**
   - Post every non-page spare as an OPEN ask on a non-rival member venue: LAT-03/04 at value 5; leftover LAV commons after the Workshop.
   - RET-11 to Pilar only at ≥198.
   - Re-check cash against 150 + CHA cost after the grant.
   - Effect: makes the +30 np MAL close possible (directive 01:40).
   - Risk: thin fills (3.5%); the grant may already cover the gap.
2. **Fix and verify the trader before the restart (Builder).**
   - Remove the stale `sobre_bienvenida` reference.
   - Run one dry tick with `CASH_FLOOR=464 --max-ratio 0.8 --exclude 'CHA-*,MAL-*'`.
   - Confirm no errors for 5 minutes.
   - Effect: the only auto-capture of below-value asks, which was worth +21.7 on Saturday.
   - Risk: a bad restart burns accepts during the CHA fast start, so run it after the first CHA tick.
3. **Treat the round-3 reset check as the gate for every sale (Operator, first tick).**
   - If `neg_points` resets, Saturday's 119.1 is banked and every CHA card bought at ≤ value scores from zero, so run CHA first, fodder after.
   - If it carries, also post the 2 LAV asks as open, not addressed.
   - Effect: avoids misallocating the first accepts.
   - Risk: none beyond a few ticks of delay.
