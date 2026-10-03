# Scout (claude-sonnet-5-5, Sun 00:02)

## Top 3 actions now

1. **SAL-11 bid 20252 (115 → t04, v15, expires tick 1565): keep it live, raise only if needed, hard cap 125 (Lucas 21:45 GUARDRAIL).**
   - Evidence: our value is 162 for the first copy. Team 10 → Team 17 paid 207 for SAL-11 at tick 1296 (t10 sold SAL-11 for 207), and t04 asks 245 on El Rastro. Team 4 "dumps SAL" and is #11 (25.1), so we don't feed a leader. Cash is 392 against a Sunday CHA reserve of about 330.
   - Effect: a fill at 115-125 is worth about +37 to +47 neg_points (162 − price − pack drag), roughly +2.3 board per the directive. Confidence: med, because the 245 ask suggests t04 may refuse.
   - Executor: operator. Counter at ≤ 125 only, as a maker bid.

2. **Sunday 09:00: MAL close via a team trade, only if the CHA budget is under control (directive 21:20, item 3).**
   - Evidence: we hold MAL-01 to 05, 06 and 08 and lack MAL-07, 09 and 10. t09 bids 56 for MAL-09 and MAL-10 (offers 19719, 20251), and t01 bids 152 for MAL-11. The MAL page bonus is not in the data.
   - Action: the operator buys MAL-07/09/10 from teams. Per the 21:40 directive, Team 15's MAL-09/10 bids sit at about 50 P; the likeliest seller is t10, so keep its gain small.
   - Expected: the +50 cap applies to a page-closer in a fresh round. Confidence: low-med, since t09 competes for the same cards.

3. **Cancel our two stale asks and sell LAV-03/LAV-04 to a non-rival: 19979 (LAV-03 → t04 at 6) and 19981 (LAV-04 → t01 at 6) expire at tick 1455.**
   - Evidence: the spares are worth 3.2 each to us. t04 and t01 are #11 and #9, both ≥ 10 below us and not in the top 4. Their LAV set purchases (t04 LAV×4) mean they may close pages.
   - Effect: about +2.8 each, small. Confidence: med.
   - Executor: operator, re-post after expiry. Cancel only if the feeding rule changes.

## What the climbing teams are doing

- **Team 18 (#2, +1.2 in 60 min):** it collects RET and LAT. It paid 72 for LAT-10 from t13 at tick 1332, so it is building its LAT set from teams.
- **Team 12 (#4, 70 deals):** it bought RET-11 from t06 at 216 (tick 1245) and LAT-10 from t01 at 86 (tick 1304). It also bought LAV-08 from t08 at 14 (tick 1420) and LAT-06 from t09 at 20 (tick 1303). It pays high for epics and rares and cheaply for uncommons.
- **Team 10 (#1, 37.6):** it sold SAL-11 to t17 at 207 and bought MAL-11 from t08 at 195. It also bought RET-03 back at 8 from t06 (tick 1392), so it finishes pages with cheap commons.

## Threats

- **Team 6 → RET:** t06 sold RET-11 and RET-10, and it is at −2.7 over 60 min. It is dumping RET to rivals (t12, t04, t07), which hands t12 (#4) value. Don't buy RET from t06 for t12's benefit.
- **t09 competing for MAL-09/10:** it bids 56 on both. If it closes its MAL page first, our MAL close loses value. t10 sold it MAL-06 at 20.
- **Feeding t10 (#1, 37.6 vs our 30.5):** it collects LAV/RET and has the largest market (7.5 vs the top of 12.5). Don't route trades onto its venue v07 (standing rule); club deals stay on v10.
