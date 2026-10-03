# Scout (claude-sonnet-5-5, Sat 22:17)

## Top 3 actions now

1. **Keep SAL-11 bid 18977 (115 → t04) alive; re-post before it expires at tick 1371.** Operator, via trade.py or the existing repost loop.
   - Evidence: Lucas's 21:45 GUARDRAIL allows SAL-11 from Team 4 at ≤ 125 (our value 162, first copy). Team 10 sold SAL-11 to t17 at 207 (tick 1296), so a fresh bid is competing with that market.
   - Effect: about +2.3 board by Lucas's estimate. Gain at 115 is 162 − 115 = 47, but pack drag and the 50 cap apply.
   - Confidence: med. t04 bots have not replied to any ping.

2. **Take Team 9 or Team 15 page-finisher matches on v10 only where the seller is not a top-4 team.** Offer ads and brokering via Lucas or Dani, not the operator.
   - Evidence: t09 bids 56 for MAL-09 and 56 for MAL-10 (offers 19105 and 19129). Lucas's 21:40 directive has the RET-09 t08 → t09 match at about 100. Team 13 bids 42 for RET-09/10, far below the ~84-100 that t09 can pay.
   - Effect: zero neg_points for us. The Market (v10) real-trades mark is the lever, with a 10 P rebate per non-rival card sold on v10.
   - Confidence: low to med. The rebate is capped at 80 P.

3. **Sell spares to t01 and t09 via our standing asks (19326, 19328, 19330, 19331); hold RET-11 at 198 value.**
   - Evidence: 19331 is MAL-08 at 20 (our value 17.5). The LAV-03, LAV-04 and MAL-03 asks at 6-9 are close to spare value 3.2-7. Both targets are below us on the board (t01 at 25.7, t09 at 24.0). The dealer FLIP rule requires est. score ≥ +20, and nothing in the metrics shows one.
   - Effect: gain of about +2.5 neg on MAL-08. Small.
   - Confidence: med.

## What the climbing teams are doing
- **Team 18 (+1.6 in 15 min, now #5):** it buys RET/LAT. Its latest trade is LAT-10 from t13 at 72 (tick 1332), a rare below the clearing price of 70-80. Its profile shows 38 deals against our 53, so it gains from fewer, bigger trades.
- **Team 10 (#1, 38.3, +3.7 in 60 min):** it moves epics. It sold SAL-11 to t17 at 207 and bought MAL-11 from t08 at 195 (ticks 1296 and 1264). It bids 205 for LAV-11 (offer 19081). It also profits from other teams' trades on v10.
- **Team 12 (+2.5 in 60 min):** it is collecting RET/MAL/LAT. It paid 216 for RET-11 from t06 (tick 1245) and bought LAT-10 at 86 (tick 1304). It also bought LAT-06 at 20 and SAL-09 for 70 (t09 bought the SAL-09).

## Threats
- **Team 10 widens the lead.** It leads by 7.4 points and holds the epic flow (LAV-11 bid at 205). We must not route trades to v10 while it is a rival. The v10 rebate relies on non-rival sellers only.
- **t09 and t13 compete for RET cards.** t09 is a RET-09 finisher, and t13 posts bids of 42 on RET-09/10 and 4 on commons. If t09 closes RET it gains, but it sits below us on the board, so the feeding rule allows it.
- **Pack drag and the cap.** The SAL-06 buy gave +40.4, below the +50 cap. Any further trade shifts the value of our unopened silver pack (72.7).
