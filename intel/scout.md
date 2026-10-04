# Scout (claude-sonnet-5-5, Sun 08:16)

## Top 3 actions now

1. **Hold the CHA fast start and the 08:45 t0 chain; no new trades before doors open.**
   - Executor: operator's t0 job (pid 22755), as armed.
   - Evidence: metrics at 08:14 read "Closed until Sunday 09:00", with no open offers, cash 392 and neg_points 119.1.
   - Directives: Pícaros CHA rares ≤ 57, then 60, then 62. Every page closer goes on El Rastro, addressed, with the seller's fee added.
   - Effect: a CHA page closer is worth at most +50 per trade (cap). Confidence: med.

2. **Sell the spare commons on El Rastro, but only to teams ≥ 10 points below us.**
   - Spares: LAV-02 ×3 (1.3 each), LAV-03 ×2 and LAV-04 ×2 (3.2 each), LAT-03 and LAT-04 (5 each). The 07:15 plan sends LAV-02 ×2 and LAV-03 to the Workshop at C, so keep those.
   - Evidence: asks on the board for LAV-02 10, LAT-04 9 and LAT-02 9 show cards of this kind listed at about 9-10. Team 8's bid for RET-02 is 5, but Team 8 is not a page-closer buyer.
   - Executor: the maker book via `trade.py`. Buyers must pass the feeding rule; the current table shows none above our value + 3.
   - Effect: the gain per sale is price minus our value, about +5 to +7 each on LAV spares if a buyer appears. Confidence: low (no qualifying buyer yet).

3. **Do not dump below value for the ladder.**
   - Evidence: the ladder rose 0.373 → 0.437 while `negotiating` stayed flat at 21.88, and flags are spent (8 tried, 3 scored).
   - Directive 01:40 withdrew the RET-11 surplus→ladder option; RET-11 goes to Pilar only at ≥ 198.
   - Action: keep RET-11 (value 198) unsold unless Pilar bids ≥ 198. The operator checks the Pilar bid on Sunday.
   - Effect: avoids a below-value loss. Confidence: med.

## What the climbing teams are doing

- **Team 12 (#4 in metrics, #3 in Dani's profile, 70 deals).** It bought RET-11 (epic) from t06 for 216 P at tick 1245, plus LAT-10 from t01 at 86 and LAT-06 at 20. Its trades are epics and rares.
- **Team 18 (#2, 31.3, Δ +0.8 in Dani's profile).** It bought LAT-10 from t13 at 72 at tick 1332. It sits just above us, so its rare purchases at 72 are the price reference.
- **Team 10 (#1, 37.6).** It sold MAL-06 at 20 to t09, sold SAL-11 (epic) to t17 at 207, and bought MAL-11 (epic) at 195 from t08 at tick 1264. It also bought RET-03 at 8 from t10→t06 at tick 1392, so its flow is epics at ~200.
- **Team 6 (71 deals).** It sold RET-10 (rare) to t04 at 84 and RET-06 (uncommon) to t07 at 30. It sells RET cards at above-book prices, which is where our RET buys would meet it.

## Threats

- **Team 10 leads at 37.6, 7.1 above us.** It holds the club venue at v10, and club deals go half to v10 and half to members' markets, so each club trade feeds it. Keep page closers on El Rastro.
- **Team 17 and Team 1 hold the leaderboard's #8 and #9 slots (25.8 and 25.6).** Both are buyers for SAL and MAL. Dani's "buyer" tags name MAL/LAV/SAL for Team 17. Avoid selling SAL page-completers to them unless they are ≥ 10 below us.
- **Public bids on CHA cards.** The feed shows addressed offers in full, and directive 07:40 keeps ≥ 0 bids public. Team 10 and Team 01 can see them and hold cards we need, so cancel any bid for a CHA card they hold.
