# Scout (claude-sonnet-5-5, Sat 15:54)

## Top 3 actions now

1. **Run the Pícaros watch, then sell spares to it in offer-only mode (Operator, `abuela_bot.py --dealer picaros --offer-only`).**
   - Evidence: Pícaros was announced at tick 630 ("Quick deals. Few questions."). Our 3 Pilar deals (MAL-07 19, MAL-06 19, SAL-08 23) may unlock it early. Our ladder is 0.188, and L3 is near saturation (+0.007 on the last Pilar trade).
   - Spares to offer: SAL-01/03/05, MAL-02/03, LAT-03, and second copies, each worth ≤ 9 to us. Sell only at ≥ our value.
   - Expected effect: a new level's best 3 slots start empty. Playbook: a dealer sale above his opening bid counts, Pilar's L3 paid +0.050, and +0.01 ladder is about +0.33 board.
   - Never a deal at the opening price. Step −2/−3 and let the dealer climb.
   - Confidence: med. No menu is in the data yet.

2. **Pull the offer-only swap trades through, and keep the trader accepting swaps (Operator, `trade.py` plus the `swaps` daemon once verified).**
   - Evidence: tick 669, t08's SAL-04 for our second RET-04 gave neg_points 32.5 → 38.7 (+6.2). The swaps dry run found 43 candidates, best +10.3/+9.7.
   - Open: 9387 (to t15) and 9389 (to t07) expire at ticks 688. Repost them at 2× the ticks wanted (the server halves expiry).
   - Check before each: the counterparty is outside the top 4 (not t14, t12, t18, t10), and the RET page stays 10/10.
   - Expected effect: +2 to +6 neg_points per swap, about +0.2 to +0.6 board.
   - Confidence: med-high.

3. **Fill t07's page bids with spares as maker (Operator).**
   - Evidence: the rival profile lists t07 (#17, 10.6 below us) as the buyer for LAT-04 9.5 (+6.3), RET-04 9.5 (+4.7), and LAV-02/03/04 9.5 (+4.3 each).
   - Our LAV-02 is already offered to t07 at 0 as a swap for MAL-01. Re-ask the others at ~9, not 0. Our LAV-03/04 asks (6, to t04/t03) are too low; others ask 10 for LAV-04.
   - Feeding rule: t07 is #17, so this is fine. Do not touch t17/t01 closers without the Chief.
   - Expected effect: about +4 each, so +10 to +20 neg_points in total, capped by actual fills.
   - Confidence: med. The prices are estimates.

## What the climbing teams are doing
- **t04** (#10, +0.2) is buying RET uncommons from four sellers: RET-07 at 25 (t08), RET-08 at 27 (t18), RET-06 at 26 (t09), plus LAT-11 epic at 160 to t16. This is a RET page build at roughly uncommon list price.
- **t07** (#17, +0.3) is trading cards for cards at 0 P: RET-02 ↔ LAV-04 with t15, and MAL-01 ↔ SAL-02, plus RET-04 at 10 from t08. Swaps save cash and score for both sides.
- **t15** (+1.2 over 30 ticks, 22 team trades) is the most active swap partner. Its MAL/LAT/RET swaps give it moves without paying fees.
- **t18** (#3, +0.5) is selling RET-08 to t04 at 27 and collecting RET/LAT. It is a top-4 team, so we do not feed it.

## Threats
- **t17** bids LAV-09 47 and LAV-06 15, and 70-85 for our MAL-09. It looks like a MAL page closer, and t17 is #7 (25.5), 2.8 behind us. The Chief has already refused the MAL-09 sale, so keep holding it.
- **t13** (#6, 25.5, 57 deals, 454 listings) is lobbying everyone to trade on v03. Its venue earns value created, so keep our trades off v03.
- **Gap at the top:** t14 leads at 30.4 (we are at 28.3). Do not sell page-closers to t14, t12, t10 or t18. We gained +0.2 over 15 min while t18 gained +0.5.
