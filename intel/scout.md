# Scout (claude-sonnet-5-5, Sat 13:42)

## Top 3 actions now
1. **Do not trade or step during the lunch pause (tick 630 onward). Prepare the SAL-06 → Pilar plan.** Executor: Operator, with the background job that resumes at unpause.
   - Evidence: the clock paused at tick 630. Abuela thread 868 is open (her 29, our 21), and our bid 9168 for SAL-06 at 21 expires at tick 634.
   - Cap is 25 (Chief). Abuela held 25 against our 22 in thread 832, so buy only if she reaches ≤ 25 in small steps, then sell to Pilar at ≥ 25.
   - Effect: roughly +0.019 to +0.040 ladder if it closes (Pilar MAL-06 +0.040, SAL-08 +0.019). neg_points unchanged if bought at ≤ value. Confidence: med.
2. **Pilar sells at ≥ our value with small steps (−2/−3), using offer-only mode, for the L3 ladder slots.** Executor: abuela_bot `--dealer pilar --ladder --offer-only`.
   - Evidence: Pilar deals at 19 (+0.050), 19 (+0.040) and 23 (+0.019 after a jump). Ladder is 0.181, uncapped so far.
   - Cards: only spares worth less than her price. Her price band is 16-19 for uncommons.
   - Effect: replace the weakest L3 slot, about +0.01 to +0.02 ladder. Confidence: med.
3. **Watch `logs/bargains.log` for the lunch GUARDRAIL buy.**
   - Conditions: seller outside the top 5, not a dealer; value − price − fee ≥ 50; total ≤ 100; value re-read first.
   - Evidence: the +50 cap measured twice (RET-01 at 20 from t10; LAV-05 at 8). Top bids now include t04 LAT-09 at 64.
   - Effect: up to +50 neg_points (≈ +4.7 board). Confidence: low, because no hit is logged.
   - Also keep our 5 asks on v15 and the t04 LAV-03 ask live. Gains are small (+4 to +6 each).

## What the climbing teams are doing
- **Team 14 (#1, 30.8, +1.1/60 min):** it sells RET commons at 9 to t04, t09 and t15 (ticks 591-598) and collects LAV/LAT. We have no evidence of a dealer edge, only volume.
- **Team 10 (#3, +4.1/60 min):** it lists 197 offers, bought MAL-10 at 74 (tick 585) and runs 30 deals. Its score rose while trading on its own venue v10, where Team 15 and Team 10 trade (our v10 notes).
- **Team 18 (#4, +2.2/60 min):** it collects RET/LAT and is a top-4 team, so we never feed it.
- **Team 15 (#14, +1.4):** it ran swaps at 0 P with t07 (ticks 607, 613, 616: LAV-08↔LAV-06, LAT-03↔MAL-08, MAL-01↔SAL-02) and has 22 team trades. Card-for-card swaps score both sides without cash.

## Threats
- **Team 14 is ahead by 2.7 board and still gaining** while we fell 0.8 in 15 min. Do not sell it LAV/LAT cards; our spares are dumped only to teams ≥ 10 below us.
- **LAV-11 was lost to Pilar.** Dealers pay about 140 for epics (Team 8 sold at 140), so team bids must beat that.
- **Value created on our venue can go negative:** mm_points swung +4.99 → −5.2 when a card moved to a lower-multiplier holder. Do not steer trades onto v10 without checking this.
