# Scout (claude-sonnet-5-5, Sat 20:43)

## Top 3 actions now

1. **Hold all writes until the pause ends; then keep only non-feeding sales and the open v15/v05 asks.**
   - Evidence: game paused at tick 1201. Payday gave every team +400 P, and cash is now 520. Dani's file says "no buyer passes the feeding rule above our value + 3 yet".
   - Our offers 17392 (MAL-08 to t01 at 20), 17586 (LAV-04 to t01 at 6), 17660 (LAV-03 to t04 at 6) and 17696 (MAL-03 to t09 at 9) already stand. Offer 17650 (MAL-02 to t08 at 40) expires at tick 1214.
   - Executor: Operator, once the Chief clears run/hold-writes.
   - Effect: about 0 to +2 neg_points from clearing spares. Confidence: med.

2. **Do not spend on the dealers' epics or Don Ernesto's vault (reachable after Payday) unless the price is at or below our value.**
   - Evidence: dealer deals score min(0, ΔV − price), so a gain clips to 0 and a loss counts in full. Dealers pay only through the ladder, which is capped for us (negotiating flat 21.88 while ladder went 0.373 → 0.437).
   - Pilar's epic price is a median of 187. t10 bids 205 P for LAV-11 (offer 17778). We value LAV-11 at book 180 × 1.3 = 234 before any page bonus; buying from a team below that is the only +EV route.
   - Executor: Operator, a maker bid on El Rastro or v15 addressed to the holder. Ceiling: our value minus fee.
   - Effect: capped at +50 per trade. Confidence: low. The holder is unknown and t10 is already bidding 205.

3. **Take the live asks that gain at least 3 over our value; that is the only lever left for neg_points.**
   - Evidence: team trades still move the board (the t07 swap's +15.5 neg_points gave +0.05 board per neg_point), and SAL-06 gave +40.4. Our page gaps are MAL-06/07/09/10 (rares MAL-09/10 are the largest).
   - t09 bids 56 for MAL-09/10, which signals scarcity. Two MAL rares have just traded between other teams: MAL-10 t13→t02 at 30 P (tick 1191), which is cheap for us.
   - Action: Operator bids addressed to t02 for MAL-10, with a ceiling at our value minus the maker's fee of 0. Our MAL multiplier is 0.7, so the value is about 49 plus the pack-drag effect. Run `value?MAL-10` first.
   - Effect: small, since MAL is 0.7×. Confidence: low.

## What the climbing teams are doing
- **t02 (#9, +2.6 in 15 min)** bought MAL-10 at 30 P from t13 (tick 1191). Its mix is RET×3, MAL×3, and it is buying cheap rares from a dumper.
- **t07** is the heaviest buyer of RET (8 team buys) and LAV (7). It took RET-10 from t06 at 77 (tick 1186), RET-09 from t04 at 66 (tick 1125) and RET-08 at 24 (tick 1057). It is also reaching for RET page closers.
- **t12** is buying LAT cheaply (LAT-09 at 55, LAT-07 at 14) and also sells uncommons at 10-14. It collects RET/MAL.

## Threats
- **t10 (#1, 34.0)** bids 205 P for LAV-11 and now holds 400 P more. Do not route any trade to its venue v10 or v07.
- **t06 (#2) and t03 (#4)** are within about 1.6-1.9 board of us. They collect SAL and LAV, and t06 sells RET rares at 77. Any LAV/SAL card we sell to them feeds a rival.
- **Payday cash** lets t13 and t14 afford closers. t14 (LAV/RET) is 1.7 below us and already says "100% sure". Watch for DENY lines from the Chief.
