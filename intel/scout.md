# Scout (claude-sonnet-5-5, Sat 17:02)

## Top 3 actions now
1. **Sell page-closer spares to Team 7 (#17, 17.6, 10.6 below us), as maker, addressed offers.**
   - Cards: LAT-04 (est. 9.5), RET-04 (9.5), LAV-03/LAV-02/LAV-04 (9.5).
   - Evidence (rival profiles): our value 1.2-3.2 each, est. gain +4.3 to +6.3. Team 7 collects RET/LAV/LAT and buys LAV×7, RET×3, LAT×2.
   - Caveat: the 9.5 prices are estimates, not live bids.
   - Executor: `trade.py` list `to` t07, with 2× the ticks we want (Saturday halves expiry). Do not offer to t03/t16/t09 below 9: their LAV-04 at 6 and LAV-03 at 6 are weak.
   - Effect: about +4 each in neg, ≈ +0.6 board each. Confidence: med.
2. **Re-price the SAL-10 ask (offer 12179, 93 to t08, expires 819).**
   - Evidence: the Pilar fever opens 18:04 (~85 expected). t08 is #13, so it is a safe buyer. Recent SAL-09 trades: 68 (t15→t06), and Picaros paid us 54. No team has bid 93.
   - Action: let 12179 lapse. Re-list SAL-10 to t08 at ~80 as maker with 100 ticks to expiry, and keep the fever job to Pilar (open 100, take ≥ 85) as the fallback.
   - Effect: our value is 63, so a sale at ≥ 75 is 0 neg (gains are clipped to 0). It funds the Sunday cash target (~245 per the directive), not neg_points. Confidence: med.
3. **Keep the SAL-09 sale for the fever and sell MAL-09 to Pilar at ≥ 55 (17:30 job).**
   - Evidence: MAL-09 is worth 49 to us. The Pícaros rare median is 58 (6 deals). Pilar's rare median is 70 (1 deal). A sale above 49 is 0 neg, plus a possible L3 ladder slot.
   - Executor: operator job, step −2, never jump to her bid (SAL-08 got only +0.019 after a jump).
   - Effect: ladder up to about +0.02-0.05, and it frees cash. Confidence: med.

## What the climbing teams are doing
- **Team 1 (#3, +3.9/h) and Team 3 (#6, +6.1/h)**: Team 3 bought LAT-09 at 88 from t16 (tick 724), plus SAL×2 and LAT×2. Team 3 is also our SAL buyer for commons, so we have fed it small deals.
- **Team 6 (#7, +3.7/h, +2.2 in 15 min)**: bought SAL-09 at 68 from t15 (tick 781), sold us MAL-01 at 5, and bought RET-04 from us side-channel. It is the most active trader (45 deals, 305 listings), buying SAL×4.
- **Team 16 (#9, +4.7/h)**: sold LAV-07 at 44 to t07 and LAT-09 at 88 to t03. It bids RET-07/LAV-06 at 12-15 on El Rastro. It unlocked L4 at tick 761, the same ladder route we used.
- **Picaros L4 is now crowded**: t09, t10, t14, t15, t16 all unlocked (ticks 761-802), which matches the Analyst's note that SAL-10's L4 slot netted only ~+0.36 board.

## Threats
- **Team 14 (#1, 29.8)** is 0.1 ahead of us and collects LAV/LAT. It is the leader to avoid feeding, and it buys MAL-08 from us (+2.5, small).
- **Team 1 (#3, 29.1)** is 0.6 behind us and rising fastest (+3.9/h), with 23 deals only. Never sell it SAL/LAV/MAL page cards.
- **Cash is 72 against the Sunday target of ~245.** It all depends on the fever resales landing at ≥ 85. Salamanca teams are the buyers, and t16 and t08 are both low-ranked, which makes them safe.
