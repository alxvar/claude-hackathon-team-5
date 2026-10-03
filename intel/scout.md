# Scout (claude-sonnet-5-5, Sat 21:41)

## Top 3 actions now
1. **SAL-11 from Team 4 (bid 18605, 115 P, expires tick 1305).** Lucas's 21:45 directive allows up to 125 P on v15 with the floor at 260. The Operator raises to ≤125 if t04 counters, or the watcher auto-accepts the counter.
   - Evidence: our value for SAL-11 is 162 (first copy). Cash is 392, so 392 − 125 = 267, above the 260 floor. t04 dumps SAL, and its asks are SAL-11 at 212 and 245, which are far above our bid.
   - Effect: about +2.3 board by Lucas's estimate. Per-trade neg_points are not in the data beyond that.
   - Confidence: med. t04's asks are 212-245, so it may not sell at 125. The bid expires at tick 1305.
2. **Broker RET-09 t08 → t09 at ~100 on v10 (Lucas/Dani DM both sides; the matchmaker holds the line).** t09 is a RET page-closer, and t09 is #16 at 22.4, so the feeding rule is met. t08 dumps RET.
   - Evidence: matchmaker VC ≈ +134. Real-trades market points are 5.0 × min(1, VC / top-3 mean) so far. The v10 rebate is 10 P for an uncommon/rare sold by a non-rival.
   - Effect: market-making only, not neg_points. Possibly the full real-trades mark if VC counts.
   - Confidence: med. Both parties must agree. Note: t09's RET-09 bid is not on the board; t09's visible bids are MAL-09/10 at 56 and SAL-06 at 24.
3. **Hold the cheap duplicate sales as the swap desk.** These are our open offers, all addressed:
   - 18606: LAV-03 at 6 → t04
   - 18607: MAL-03 at 9 → t09
   - 18608: LAV-04 at 6 → t01
   - 18609: MAL-08 at 20 → t01
   - 18616: MAL-04 at 27 → t02 (expires tick 1297)
   - Evidence: t09 bids MAL-09/10 at 56, and Team 15's MAL-09/10 bids are ~50 P. None of these cards are MAL rares.
   - Effect: small. Each sells a spare above its value (2nd LAV copies are worth 3.2; MAL-03 is worth 7). The Operator should reprice MAL-04 at 27 against the 24.5-26 uncommon clearing level. MAL-04 is a common worth 7, so 27 is far above the 9 common clearing price and is unlikely to fill.
   - Confidence: low-med.

## What the climbing teams are doing
- **Team 10 (#1, 38.0, +2.7/15 min):** bought MAL-11 epic from t08 at 195 (tick 1264). It holds the top bid at LAV-11 205 (offer 18361). It runs a 443-listing book and trades on its own venue. Its RET page is already closed.
- **Team 6 (#2):** dumps epics and rares to other teams: RET-11 → t12 at 216 (tick 1245), RET-10 → t04 at 84 (tick 1257), RET-10 → t07 at 77 (tick 1186). It has 826 listings and 34 team trades. It is the highest-volume seller.
- **Team 12 and Team 9:** t12 paid 216 for RET-11. t09 bought SAL-09 from t12 at 70 (tick 1231) and MAL-06 at 20 (tick 1230).
- **Team 13:** buys small and swaps at scale. MAL-01/MAL-02 swapped at 0 (tick 1202), plus several 3-14 P deals.

## Threats
- **Team 10 is leading and gaining** (+4.0 in 60 min vs our −0.9). It bids 205 for LAV-11 and our RET-11 is worth 198 to us. Do not sell it below 198, and do not sell to t10.
- **MAL-09/10 competition:** t09 bids 56 each, t04 bids 55 and 45, and t15 ~50. If MAL closes Sunday, expect pressure on the price. Not in the data: who holds the MAL rares.
- **Rate limit:** our shared 5 req/s was hit at 21:35. A burst of restarts could block the SAL-11 counter.
