# Scout (claude-sonnet-5-5, Sat 22:01)

## Top 3 actions now
1. **Keep SAL-11 bid 18977 live (115 → t04, v15, exp tick 1371) and raise to ≤125 only if t04 counters.**
   - Evidence: Lucas's 21:45 GUARDRAIL allows ≤125 for a first copy worth 162 to us. t10 sold SAL-11 to t17 at 207 (tick 1296), so the epic market is ~205.
   - Executor: operator, with watcher auto-accept (floor 260). Our cash is 392.
   - Effect: dealer-free team buy; the gain is capped at 50, and the pack drag lowers it slightly. About +40 neg_points, ≈ +2.3 board per the directive. Confidence: med (t04 has not replied to pings).
2. **Broker RET-09 t08 → t09 (~100 on v10) via Lucas/Dani DMs, and post the t09 MAL-09/10 bids (56 each) as ads.**
   - Evidence: t09 holds RET 9/10 and bids 56 on MAL-09 and MAL-10 (offers 19105, 19129). t08 dumps RET and asks 84 on RET-09 (El Rastro). t06 sold RET-10 to t04 at 84 (tick 1257).
   - Executor: Lucas/Dani by DM, plus the matchmaker ads already running.
   - Effect: a market-making lever (the 22.5 real-trades share), not neg_points. The rebate is 10 P per card, paid only after a non-rival sells on v10. Confidence: med. t09 is #15 at 23.1, so it passes the feeding rule.
3. **Take any BUY line from the reactor: a team ask on a card we lack, gain ≥15 after fee, cash ≥350 afterwards.**
   - Evidence: we hold LAT-03/04 and MAL-08 as low-value spares. Our missing cards are MAL-06/07/09/10 (MAL page; Sunday priority), and t09 bids 56 for MAL-09/10, which competes with us.
   - Executor: operator via rbuy.py (team seller, first copy, non-rival venue, cash-only).
   - Effect: up to +50 per page-closer. The MAL page is parked for Sunday, so tonight only take true bargains. Confidence: low-med.

## What the climbing teams are doing
- **t10 (#1, 38.5, +4.5 in 60 min)** trades epics: sold SAL-11 to t17 at 207 (tick 1296) and bought MAL-11 from t08 at 195 (tick 1264). Its LAV-11 bid is 205 (offer 19081). It still collects LAV/RET and dumps SAL/LAT/MAL.
- **t12 (#3, 30.8, +2.5)** buys RET-11 from t06 at 216 (tick 1245), SAL-09 from t12... correction: t12 sold SAL-09 to t09 at 70 (tick 1231), and bought LAT-10 from t01 at 86 and LAT-06 from t09 at 20 (ticks 1303-1304). Its Abuela rate is −22%.
- **t17 (#8, +1.8)** paid 207 for SAL-11, a high-price epic close, and bids 150 for MAL-11 (offer 19048).
- **t13 (#9)** is the busiest trader (85 deals): many cheap bids at 2-13 P on RET and LAT commons/uncommons, and a 42 P bid for RET-09/10.

## Threats
- **t09** bids 56 for MAL-09/10, competing with our Sunday MAL close. It is also one card from a RET page via RET-09.
- **t12 (#3, +1.1/15 min)** is closing on us, 30.8 vs our 30.6, and is now a rival. Never route trades through its stall.
- **Our score is slipping (−0.6/15 min, −1.0/60 min)** while neg_points sit flat at 119.1. Only SAL-11 or a team trade moves them tonight.
