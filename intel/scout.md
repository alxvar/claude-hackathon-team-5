# Scout (claude-sonnet-5-5, Sat 13:36)

## Top 3 actions now

1. **Run the SAL-06 buy from Abuela (thread 868) once the clock resumes.**
   - Executor: operator's background job. Cap 25, small steps. Then sell SAL-06 to Pilar at ≥ 25 with small steps, offer-only (playbook rules 1-2).
   - Evidence: open bid 9168 is 21 for SAL-06. Abuela is at 29 (tick 629). Her earlier thread ended 25 against our 22. Pilar paid 23 for SAL-08 (her final) and Team 4 got 25.
   - Effect: a Pilar sale at ≥ our value costs 0 neg_points. The best earlier L3 slot was +0.040 (MAL-06). Our L3 slots are +0.050, +0.040 and +0.019, so a new deal above +0.019 would replace the weakest.
   - Confidence: med. Abuela held 25 against our 22 last time, and the game clock has been paused since tick 630.

2. **Keep the 9 stall asks live; reprice the ones aimed at weak buyers.**
   - Executor: operator's book daemon. Targets are listed asks 9100 LAV-02 → t09 at 7, 9101 LAV-04 → t03 at 7, 9136 LAV-03 → t04 at 7, 9102 SAL-02 → t16 at 6 and 9103 LAT-04 → t16 at 5.
   - Evidence: these copies are worth 1.2-3.2 to us. The recent +4.7 (SAL-01 at 7 to t03) and +2.0 (MAL-03 at 5 from t04) were comparable small team-trade gains. Team 7 (#17) is the page-gap buyer for LAV/LAT, with an estimated 9.5 and a gain of +4.3 to +6.3.
   - Effect: roughly +4 neg_points per sale, about 0.4 board at 0.094 per point.
   - Feeding check: Team 7 is 11.3 below us, so it passes the rule. t03, t04, t09 and t16 are all outside the top 4 and below us, but I have no gap or page-closer data for them.
   - Confidence: med.

3. **Watch for a bargain-buy hit (13:15 GUARDRAIL).**
   - Executor: operator, reading logs/bargains.log.
   - Evidence: the best open bid is t04's 64 for LAT-09, and t04 also bids 27 and 26 for RET-08 and RET-06. We hold no LAT-09, so those bids are no use to us.
   - Conditions to act: seller outside the live top 5, value − price − fee ≥ 50, total ≤ 100. No qualifying ask is visible in the El Rastro snapshot (cheapest asks are commons at 4-14).
   - Effect: up to +50 neg_points (about +4.7 board) if a hit appears.
   - Confidence: low.

## What the climbing teams are doing
- **Team 14 (#1, 30.8, +1.1/h)** sells commons on El Rastro. Its RET commons went at 9 P (ticks 591-598: RET-02, -03, -01, -04 to t04, t09, t15, t09). It also bought SAL-03 at 5 (t06 → t14, tick 600).
- **Team 10 (#3, +4.1/h) and Team 6 (#9, +4.6/h)** are the 60-minute climbers.
  - t10 bought MAL-10 at 74 (tick 585), and our venue's mm_points moved from SAL-07 → t15.
  - t06's recent big trade was RET-09 sold to t02 at 84 (tick 504).
- **Team 15** trades heavily (22 team trades) via 0-P swaps with t07 (ticks 607, 613, 616). Swaps cost no cash and score for both sides. Team 13 also stacks LAV-08 and MAL from t07/t04 at 5-20 P.
- **Team 18 (#4, +2.2/h)** has 13 team and 16 dealer trades and collects RET/LAT. It paid 86 for RET-09 at tick 206.

## Threats
- **Team 14 (#1)** collects LAV/LAT and is already 2.7 points ahead of us. Never sell LAV or LAT to it; its LAT-09 purchase was at 65.
- **t04 (#10)** has standing bids of 27 and 26 for RET-08/-06, and Team 2 collects RET. Both are below us, but our RET cards are not for sale: they are worth 100-150 to us.
- **Team 13** keeps RET-01..03 bids at 2 P and has the most dealer activity (39 dealer trades) and listings (435). It is #7 at 25.5 but fell −3.3 in an hour, so it is not a feeding risk.
