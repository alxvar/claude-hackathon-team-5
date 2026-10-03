# Scout (claude-sonnet-5-5, Sat 17:23)

## Top 3 actions now

1. **Hold the SAL-09/SAL-10 → Pilar sale for the 18:06 fever job (open 100, −2, accept ≥ 85).** Do not sell early.
   - Executor: the Operator's existing job.
   - Evidence: the fever runs ~18:04-20:04, Pilar pays +25% over book for SAL. Our SAL-09 and SAL-10 are worth 63 each, so ≥ 85 clears our value with a gain that clips to 0. Pilar's dealer prices in the metrics (median 70 rare sell, 20 uncommon) show no competing demand yet.
   - Effect: neg_points ±0 (gains clip), cash +~170. Funds the Sunday CHA page.
   - Confidence: high.

2. **Sell the 3 free LAV-02 spares and the LAV-03/04 spares to Team 7 (#17, 10.6 below us), as maker, at 9 P. Fall back to Team 9 if Team 7 does not fill.**
   - Executor: Operator via trade.py, with policy.check.
   - Evidence: offers 12921 and 12960 are 0 P swaps expiring at ticks 856/858. Team 7 buys LAV×7 and RET×5 in team trades. Rival profiles show Team 7 as a buyer, est. price 9.5. Our values are 1.3-3.2, so the gain is about +4.3 each (est.).
   - Effect: ~+4 neg each, ~+0.6 board in total. The Page-closer rule is met because Team 7 is ≥ 6 below us.
   - Confidence: med. The price is an estimate and there is no live Team 7 bid.

3. **Replace the 0 P LAV-02 swaps with priced asks, and keep MAL-02 and MAL-05 → t15 at 9.**
   - Executor: Operator book daemon.
   - Evidence: the 0 P swaps expire now. Team 15 is a safe partner (#14, 21.5) and has made 22 team trades. Team 16 bids 5-15 for RET commons and uncommons, but those are our page cards, so no.
   - Effect: roughly +2 neg per MAL (value 7 → 9 P, est.). It costs nothing if they do not fill.
   - Confidence: low-med.

## What the climbing teams are doing

- **Team 3 is up +3.1 in 60 min (#3, 29.2).**
  - It bought LAT-09 (rare) from t16 at 88 at tick 724.
  - At tick 844 it took LAV-10 from t07 at 38 P (bundled with 4 commons it gave).
  - Its negotiating score of 24.49 is the highest on the board. Its sets are SAL/LAT/LAV.
- **Team 14 leads (30.4, +0.5).**
  - It has 34 deals.
  - It collects LAV/LAT and sold us MAL-08 at 15.
  - It reached L4 at tick 781 (2 Pilar deals). The Pícaros ladder is now crowded: t10, t16, t14 and t15 all unlocked L4.
- **Team 6 is up +2.3 in 60 min (#7).**
  - It resold SAL-09 from t15 at 68 (tick 781).
  - It dumped MAL-01 to us at 5.
  - It shows 45 deals, almost all small team trades.
- **Team 7 is soaking up LAV/RET commons.**
  - LAV×7, RET×5.
  - It is receiving the page cards from Team 3 and Team 16 (LAV-07 at 44).
  - It is the right low-ranked buyer for our spares.

## Threats

- **Team 3 sits 0.14 behind us (29.24 vs 29.38) and is trading on LAV and rares.**
  - Our LAV-06/07/08 and LAV-09/10 are worth 118.6 and 177.1 to us.
  - Do not sell Team 3 any LAV card.
  - The 0 P LAV swaps to t07/t09 are fine: they are ≥ 6 below us.
- **We are #2 behind Team 14 (30.4), with a 1.0 gap.** Our 15-min change is −0.4 while Team 3 gained +1.0, so we are being overtaken through passive drift. Flags are capped at 0 (the last three scored 0, and −10 came from one wrong flag), so there are no more cheap neg_points there.
- **Team 10 (#6, 1.33 below us) is not blocked in the daemons: TOP_N is 5.** SAL-10 sits on v10 at 160. Per Lucas's 17:25 rule, no alert may nudge a third team to accept a rival offer. Ask the Builder to set TOP_N=6.
