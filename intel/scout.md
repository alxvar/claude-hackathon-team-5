# Scout (claude-sonnet-5-5, Sat 13:53)

## Top 3 actions now
1. **Operator: resume the SAL-06 buy from Abuela (thread 868) at unpause, hard cap 25, with small steps (21 → 22 → 23 → 24).**
   - Evidence: her 29 and our 21 are open at the pause (tick 630). At tick 596 she reached 25 against our 22 and closed. Our bid 9168 (21, to abuela) expires at tick 634, so re-send or move it first.
   - Effect: a 25 purchase costs about −2.5 neg (value 0.9 × 25 = 22.5). It only pays if it feeds the Pilar resale (action 2).
   - Confidence: low-med.
2. **Operator: resell that SAL-06 to Pilar at ≥ 25, offer-only, small steps, alone in its window.**
   - Evidence: Pilar paid 23 for SAL-08 (+0.019, our weakest L3 slot), while MAL-06 with small steps at 19 gave +0.040 and MAL-07 gave +0.050. Her uncommon median over the last 60 ticks is 18. The directive 12:58 plan A targets 16:00-18:00 for a "Salamanca fever".
   - Effect: replaces the +0.019 slot with possibly +0.04 (≈ +0.01 ladder ≈ +0.33 board). The resale price is not in the data; if she finals at ≤ 23, it is a net loss of about 2 neg.
   - Confidence: low. Abort if she stays below 25.
3. **Operator, or Dani at the desk: sell the four duplicate commons to Team 7 (#17, 11.3 below us, buys LAV×5).**
   - Cards: LAV-02, LAV-03 and LAV-04 (3.2 each), and LAT-04 (1.2).
   - Evidence: the profile estimates 9.5 from t07. Our live asks are at 5-7 addressed to t09, t03, t04 and t16 (offers 9100, 9101, 9102, 9103, 9136). The 9.5 is an estimate, not a bid.
   - Action: re-address those asks to t07 at 9, as maker (no fee). Cancel the duplicates first.
   - Effect: about +4 to +6 neg per card at best. Dani only points t07 at offers that are already live.
   - Confidence: med for a fill, low for the 9.5 price.
- **Lunch bargain (≥ 50 gain, ≤ 100):** nothing qualifies right now. The cheapest listed asks are LAT-06 and LAT-08 at 25 (worth about 12.5 to us), the rest are commons at 4-14, and no rare or epic ask is listed. Keep the watcher on `logs/bargains.log`.

## What the climbing teams are doing
- **Team 14 (#1, 30.8, +1.1/h):** it sells RET commons at 9 to many buyers (RET-02 → t04, RET-03 → t09, RET-01 → t15, RET-04 → t09, ticks 591-598). It also bought SAL-03 at 5 (tick 600). It collects LAV/LAT and dumps RET.
- **Team 10 (#3, +4.1/h) and Team 6 (#9, +4.6/h):** Team 10 bought MAL-10 from Team 3 at 74 (tick 585). Team 6 is the biggest 60-minute climber, but its driver is not visible in the metrics.
- **Team 15 and Team 7:** they run card-for-card swaps at 0 P: LAV-08 ↔ LAV-06 (tick 607), LAV-03 ↔ MAL-08 (613), MAL-01 ↔ SAL-02 (616). Team 15 is +1.4 per snapshot. Our v15 asks feed its venue score only if swaps or sales happen there between other teams.
- **Team 12 (#2, 29.6):** it is a strong dealer user (25 dealer trades) but fell 2.6 over 60 minutes.

## Threats
- **The gap to #1 is 2.7 (28.1 vs 30.8).** We are down 0.8 over 15 minutes while Teams 10 and 18 gain over the hour. Team 18 is 0.7 ahead of us, so a single trade could swap #4 and #5.
- **Dealer offers expire after 4 ticks.** The pause froze thread 868 and bid 9168 (expires tick 634). Check both before sending anything at unpause.
- **Team 4 bids 26-27 for RET-06 and RET-08, and 64 for LAT-09.** Selling our RET uncommons would break our RET page (each is valued 100.4 to us), so do not.
