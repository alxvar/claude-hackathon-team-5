# Judge (claude-opus-5-5, Sat 19:17)

## Verdict
**Slipping, now #2.** Us 31.68: flat over 15 min, +1.7 over 60 min (the SAL close). Team 10 leads at 32.0 (+4.4/60) and passed us. Team 6 sits 0.1 behind us. Team 18, at 30.4 and +2.4/60, is the fastest climber within 3.0 of us.

## Our strategies: keep / kill / scale
- **Dealer bot (ladder sells): KILL.** At 19:01-19:05 all 3 threads walked; each dealer went final at its opening bid. Ladder has been flat at 0.437 since 17:45, and the cap is [L].
- **Egg hunting: KILL (already stopped).** egg.found at tick 1047 left neg_points at 119.1 (unchanged since tick 988), and Don Ernesto paid nothing.
- **Trading loop: KEEP, idle.** It made 2 accepts on Saturday (15:48 +6.2, 17:46 +15.5). Its logged errors are Friday's. It costs nothing to leave running.
- **Maker book: SCALE.** Only 7 offers are live, against the plan's 20-30, and none filled from tick 988 to 1082 (neg_points flat at 119.1).
  - If all fill: MAL-02/03/05 at 9 (worth 7) +6, LAV-03 at 6 (3.2) +2.8, LAV-04 at 8 (3.2) +4.8, MAL-08 at 23 (17.5) +5.5. That is ≈ +19 neg_points.
  - Team sales do score: SAL-01 at 7 gave +4.7 at tick 351.
- **LAV-02 → t01 at 0 (offer 16078): KILL.** It is a sure −1.3 to us and a gift to Team 10's ally. Nothing in the data says it is a v10 value-created play.
- **In-room page closes: KEEP the method, but no targets are left.**
  - The SAL close at 28 P gave +40.4, the best trade of the day.
  - LAV, RET and SAL are complete. MAL is 6/10 and LAT 2/10, so no cheap close remains until CHA on Sunday.
- **v10 / market: UNMEASURED.** None of the metrics show our mm_points or any v10 trade since tick 398 (which went to −5.2). The 17:45 room plan (t02/t07 sellers on v10) has no recorded result.

## Check the scout
- **Holds:**
  - Team sales of low-multiplier spares score.
  - MAL-08 → t01 passes the feeding rule (t01 is #12 at 24.1).
  - The scout correctly says t09's value for MAL-03/LAV-03, and the venue, are not in the data.
  - No dealer rare sale beats our value (Pilar's median is 79 against our 149.9).
  - Never buy packs.
- **Stale or wrong:**
  - "We are #1, lead 0.1": false at 19:15. We are #2, 0.3 behind t10.
  - MAL-08 is now offer 16225 at 23, not 16001 at 24. LAV-04 is now 16224 at 8.
  - t07's RET-09 bid is 16127, not 16030. The top RET-09 bid is t09 at 51 (16212).
  - The threat list omits t18 (within 1.3, +2.4/60). Under the 17:25 rule, t18 is a rival.
- **Minor:** t10 is +4.4/60 (not +3.9), and t18 has 37 deals (not 36). These do not change conclusions.

## The 3 changes with the highest expected gain
1. **Make the maker book fill, and widen it.**
   - Dani walks t09, t15, t04 and t01 to accept the live offers.
   - Operator cancels 16078 and adds asks for our LAV spares (LAV-02 ×3 worth 1.3, LAV-03 and LAV-04 second copies) at 6-9 to t07. Team 7 has made 7 LAV buys and sits at 21.9, so it passes the feeding rule.
   - Effect: ≈ +19-30 neg_points, roughly +1-1.5 board at 0.05/np [L], which is enough to retake #1 from 0.3 behind.
   - Risk: never selling the last copy of a page card (values show which copies are spares); offers expire at ticks 1097-1122.
2. **DENY watch on t10 first, then t06 and t14.**
   - Analyst reads t10's bids and offer.listed events for its last missing RET/LAV card. t10 just bought RET-03 from t06 at tick 1033, and its score rose +2.0 around then.
   - Chief issues DENY lines under the 19:05 GUARDRAIL: cap 35, cash 120 ≥ 85, so one deny at most.
   - Chief asks Lucas whether t18 joins the DENY list; today it is not on it.
   - Effect: blocks ≈ +2.4 board for a rival, at about −1 board to us.
   - Risk: a wrong read of their album burns our only deny.
3. **Measure v10 before spending more room time on it.**
   - Market session posts current mm_points and v10's trade count within 10 min. Then Dani either runs the 17:45 room plan (t02 → t08, t07 → t09 at ~9 on v10) or drops it.
   - Effect: up to ≈ +3 board [L, Market] if value created is positive.
   - Risk: a negative-VC trade, like tick 398 (mm 4.99 → −5.2). Check each buyer's multiplier against the seller's before Dani pitches.
