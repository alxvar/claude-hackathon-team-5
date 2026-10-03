# Scout (claude-sonnet-5-5, Sat 11:09)

## Top 3 actions now

1. **Sell LAT-08 (worth 12.5) to Team 3 at ~25, addressed, as maker, on v07.**
   - Our offer 4971 asks 18 to t15, and it expires at tick 378. Replace it or add a second offer.
   - Evidence: teams.md shows t03 at #11, 11.4 below us, collecting LAT with an est. bid of 28 (gain +12.5). Others are at 21-23. t03 also took SAL-01 at 7 at tick 351.
   - Effect: about +10 neg_points at 25 (25 − 12.5 − 0 fee as maker). That is above our 18 ask (+5.5).
   - Confidence: med. The 28 is an estimate, not an open bid.
   - Executor: Operator, with book.py.

2. **Keep the 2nd-copy commons posted to the non-top-4 buyers, and let loop.py accept. Do not post publicly.**
   - Cards: LAV-02, LAV-04, LAT-04, SAL-02, MAL-02, MAL-04, plus the already-posted LAV-03 at 5-7.
   - Evidence: asks by others sit at 7-10 for LAV-04, LAT-04 and MAL-02. Our offers at 4-7 are below that, so they fill quickly. Our values are 1.2-3.2, so each sale nets about +3 to +6 (SAL-01 at 7 gave +4.7).
   - Effect: roughly +3 to +6 each. Reprice the cheap ones (4745-4747 at 4-5) up to 8-9 for t07, t15 and t16, which are all far below us (#17, #12, #15).
   - Confidence: med.
   - Executor: Operator.

3. **Bid for RET-10 or RET-09 only from a team, at ≤ 74.**
   - Evidence: t02 (top 4, #5) has a live bid for RET-10 at 29, so it is hunting RET rares. We already hold both rares, so there is nothing to buy. Action: do not sell RET-01 through RET-08 spares to t02, t12 or t18. They collect RET and a closer feeds them.
   - Effect: it protects our relative score; it adds no neg_points.
   - Confidence: high.
   - Executor: Operator. Note that t13's bid of 2 for RET-01 is noise.

## What the climbing teams are doing

- **Team 13** (+8.4 in 15 min, #2): it is buying MAL/SAL rares and uncommons. MAL-10 came from t09 at 65 (tick 331). It has 6 MAL and 2 SAL buys, and dumps LAT/LAV/RET. It also unlocked Pilar early with 3 Chato deals (tick 262).
- **Team 1** (+5.7 in 15 min, +8.3 in 60 min): it buys many uncommons cheaply. MAL-07 at 14 (tick 311), SAL-07 at 23 (tick 320) and MAL-06 at 20 (tick 321) are all at or below clearing. Metrics show t01 with MAL×4 and SAL×4.
- **Team 4** (+5.6 in 15 min): it sells uncommons to t01 (MAL-06 at 20) and RET-05 to t02 at 8. It also buys LAV×3 and LAT×3, so it is trading both ways at clearing prices.
- **Team 2** (#5): it keeps many bids open (SAL-09 at 62, RET-10 at 29, RET-02/03 at 4-5) and is buying RET and LAT cheaply.

## Threats

- Team 2 is bidding RET-02/03 and RET-10, and for LAV-02/LAV-04. It is a top-4 RET collector, so our RET and LAV spares must not go to it.
- Team 13 is #2 and collects MAL/SAL. Our MAL-06 and MAL-07 offers (to t17 and t01) are fine, but never post public MAL/SAL asks.
- Our SAL-08 ask of 25 to t03 expires at tick 363, and t03 may spend its cash on LAT-08 first. Both asks are addressed offers, which the public feed shows in full, so rivals can see our targets.
