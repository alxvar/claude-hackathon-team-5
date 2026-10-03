# Scout (claude-sonnet-5-5, Sat 12:07)

## Top 3 actions now

1. **Ladder test: sell LAT-08 to Chato at ≥14, offer-only.** The operator is already queued for it at 12:06:40.
   - Executor: operator, using `dealer_sell.py` in offer-only mode. Do not accept his opening 13. Let him accept our offer at his standing price.
   - Evidence: the last Chato uncommon buy ended 13 → 14 with our ask at 30. LAT-08 is worth 12.5 to us, so a deal at 14 loses nothing (dealer gains are clipped to 0).
   - Our L2 ladder is ~0 and +0.01 ladder ≈ 3.5 neg_points. Our ladder is 0.055 vs Abuela's +0.015 per deal.
   - Effect: neg_points unchanged. Measure Δladder_points alone in its window and continue only if it moves. Confidence: med.
   - Caveat: open offer 7011 asks 30 and expires at tick 478. His final of 14 is above our value but is also his buy list, so this counts as "at list".

2. **Collector sales on El Rastro: keep the six asks live.**
   - Executor: `book.py`, already running. Cards: LAT-04 to t15 at 4, LAV-04 to t07 at 7, LAV-03 to t07 at 6, LAV-02 to t09 at 6, MAL-04 to t15 at 9, MAL-02 to t15 at 9.
   - Evidence: the +4.7 (SAL-01 at 7) and +2.0 (MAL-03 at 5) deals were clean. Our spares are worth 1.2-3.2 each.
   - Effect: about +2 to +4 neg_points per fill, with the maker paying no fee. Make sure buyers are collectors so the venue value is not negative.
   - Suggested edit: LAT-04, LAT-08 and LAT-03 have a bidder in Team 7 (#17, 12.2 below us, collects LAV/LAT). Asks of 9-10 are within Team 7's median price (c 9.5), but not for LAT-04 as listed (4 to t15).
   - Confidence: med.

3. **RET-10 and SAL-09 are the only live rare bids. Hold the RET cards; do not feed.**
   - Evidence: t02 bids 53 for RET-10 and 69 for SAL-09. We hold RET-09 and RET-10 at 149.9 each.
   - Action: do nothing with RET rares. Team 2 (#6 on the Dani list, near us) is the only RET bidder, at 53.
   - Effect: avoids a loss of ~97. Confidence: high.

## What the climbing teams are doing
- **Team 12 (#1, +5.9/15 min):** collects RET/MAL and dumps SAL/LAV. It bought LAT-07 at 19 and LAT-01 at 7 from t15 (ticks 418, 433). Its trades are few but its dealer count is 37, so the ladder is its lever.
- **Team 9 (+8.2/h, #9):** a run of buys at tick 380-383 (MAL-07 at 17, SAL-08 at 20, MAL-04 at 8, SAL-05 at 8) from t06/t02/t12, all at or below clearing price.
- **Team 17 (+7.6/h, #4):** collects MAL/SAL/LAV. The data shows only 20 deals, so it is not volume-driven. Mechanism not in the data.
- **Team 13 (#2):** 48 deals. Per Lucas's directive, its lead is Friday plus ladder from buying at Chato's list price and unlocking Pilar early.

## Threats
- Value created on our venue can turn negative. A sale to a non-collector (like t10 → t15 SAL-07) cost us −5.2 mm_points.
- Team 2 collects RET/MAL/LAT and bids RET-10 at 53 and SAL-09 at 69. It could race us for cards we sell to collectors, so check the top 4 before each post.
- Team 12 jumped +5.9 in 15 minutes and sits above us at #1. Selling it anything page-closing, especially MAL/RET, feeds the leader.
