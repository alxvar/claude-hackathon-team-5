# Scout (claude-sonnet-5-5, Sat 14:40)

## Top 3 actions now

1. **Pícaros watch at the resume (Operator, armed).** Pícaros ("Quick deals. Few questions.", announced tick 630) is probably L4. We hold 3 Pilar deals: MAL-07 19, MAL-06 19, SAL-08 23. Poll `/api/dealers/picaros` every 20 s and run one offer-only thread per card, selling only at ≥ our value. Candidates: SAL-01/03/05 (9 each), MAL-02/03/04 (7), LAT-03 (5). Evidence: ladder is 0.181 and uncapped. Pilar paid +0.050 and +0.040 on small steps, versus +0.019 after a jump. Expected effect: +0.02-0.05 ladder per good deal, roughly +0.7-1.6 board at 0.33 board per 0.01. Confidence: med. The menu, price range and unlock rule are not in the data.

2. **Keep swaps 9172 (→ t15) and 9173 (→ t07) live, and widen them (Operator, `trade.py`).**
   - Evidence: t15 and t07 swapped 3× at ticks 607-616 for 0 P. The swaps are LAT-03↔MAL-08, LAV-08↔LAV-06 and MAL-01↔SAL-02.
   - Our offers: LAT-04 + MAL-04 for SAL-07 (+14.3 to us), and LAV-02 for MAL-01 (+3.8).
   - Neither t15 (#14, 21.9) nor t07 (#17, 17.3) is a leader, so we feed no one. Both offers expire at tick 650.
   - Effect: about +18 neg_points if both fill, at no fee as maker. Confidence: med.
   - Also reprice the 4 spares that Dani's table puts at ~9.5 est. for Team 7 (LAT-04, LAV-02/03/04). Our current asks are 7. Move them to 9 addressed to t07 (+4 to +6 each). Confidence: low-med, because it is only an estimate.

3. **Sell RET-02 or RET-03 to a RET collector? No. Hold the page and bid for SAL-06 only at ≤ our value.**
   - Our bid 9168 (21 for SAL-06 to Abuela) expires at tick 634. Abuela's thread is at 29 vs our 21, and she held 25 earlier.
   - Only continue at a cap ≤ 25 with small steps. Per the Chief's rule, skip if she holds.
   - The lunch bargain guardrail stays armed: a team buy ≥ 50 net, from a seller outside the top 5, scores up to +50 (≈ +4.7 board).
   - Confidence: low on SAL-06, med on the bargain watch.

## What the climbing teams are doing
- **Team 10 (+4.1/h, #3):** it sells SAL-10 and buys MAL-10 from Team 3 for 74 (tick 585). The Analyst's gap-to-t14 attribution credits t14's lead to one value-created trade on its stall.
- **Team 14 (#1, +1.1/h):** it collects LAT/LAV and dumps RET/MAL, selling RET commons at 9 (ticks 591-598 to t04, t09, t15). It runs 16 team and 13 dealer trades at Abuela −19.5%. Steady volume with low prices is working.
- **Team 6 (#9, +4.6/h):** 19 team trades and 296 listings, selling MAL/LAT/LAV into SAL buyers. The Rastro volume lines up with its climb.
- **Team 15 and Team 7:** they run card-for-card swaps at 0 P (ticks 607-616). Both gain value without paying cash or fees.

## Threats
- **Team 12 (#2):** it is climbing against us, with 40 deals. It sells SAL/LAV at r 76, so it competes with us for Pilar and SAL fever.
- **Team 18 (#4) and Team 4:** Team 4 bids 27 and 26 for RET-08/RET-06, our page uncommons (we value them at 100). Team 4 already holds one RET card, so don't feed it.
- **Gap to #1:** 2.65 board points (30.8 vs 28.15). We fell 0.8 in 15 min while idle during the pause. Pícaros and Workshop menus are not in the data, so rivals unlocking first would extend the gap.
