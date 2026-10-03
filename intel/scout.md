# Scout (claude-sonnet-5-5, Sat 15:22)

## Top 3 actions now
1. **Pícaros watch at the resume (Operator, 20 s poll of `/api/dealers/picaros` and our unlocked list).** Evidence: tick 630 `level.announced` Los Pícaros, "Quick deals. Few questions." The menu is not in the data, so the unlock rule and prices are not in the data either. Our 3 Pilar deals are MAL-07 19, MAL-06 19 and SAL-08 23. Offer-only, no deal at the opening price, sell only at ≥ our value. First candidates are SAL-01/03/05, MAL-02/03 and LAT-03 (values 9, 9, 9, 7, 7, 5). Effect: a new ladder level. The ladder is 0.181 and +0.01 ≈ +0.33 board; the size of the gain is not in the data. Confidence: low-med.
2. **Keep swaps 9172 (→ t15) and 9173 (→ t07) alive and have Dani point both teams at them in the room (both expire tick 650).**
   - 9172 gives LAT-04 (2nd) + MAL-04 for SAL-07, +14.3 for us. t15 is #14 at 21.9, which passes the feeding rule.
   - 9173 gives LAV-02 (2nd) for MAL-01, +3.8 for us. t07 is #17 at 17.3.
   - Evidence: t15↔t07 swapped 3 times at ticks 607-616 for 0 P (LAV-08/LAV-06, LAV-03/MAL-08, MAL-01/SAL-02).
   - Effect: up to +18 neg_points (≈ +1.7 board at 0.094). It is a swap, so there is no fee and no ask cost. Confidence: med.
3. **SAL-06 from Abuela, thread 868 (Operator resume job).**
   - Her offer is 29, ours 21, cap 25. Her earlier thread ended 29 → 25 and she held 25 (ticks 596, 629). Step +1/+2 and never repeat a price. Bid 9168 at 21 expires at tick 634.
   - At ≤ 25 the cost is about −0.33 neg (the Sat 12:58 directive's figure). Resell to Pilar at ≥ 25 with small steps for an L3 slot (≈ +1.4 board, Analyst).
   - Risk: Pilar's uncommon median is 18 over 5 deals in the last 60 ticks, and her best finals were 19-23. A resale at ≥ 25 is unproven. If Abuela holds at 25, walk.
   - Confidence: low-med.

## What the climbing teams are doing
- **Team 14 (#1, +1.1/60 min, 29 deals):** it sells RET commons at 9 to the RET buyers (RET-02 → t04, RET-03 and RET-04 → t09, RET-01 → t15, ticks 591-598). It also buys SAL-03 at 5 (t06 → t14, tick 600) while it collects LAV/LAT. Many small clean trades.
- **Team 10 (#3, +4.1/60 min):** MAL-10 from Team 3 for 74 P (tick 585). It is also the venue v10 owner, so trades there feed it.
- **Team 6 (#9, +4.6/60 min, 34 deals):** the metrics give no trade-level cause. The profile says it buys SAL and dumps MAL/LAT/LAV.
- **Team 15 and Team 7 swap pairs for 0 P** (ticks 607-616). That is the same lever as action 2.

## Threats
- **Top 4 are within 2.7 points of us:** #1 at 30.8, #2 at 29.6, #3 at 28.9, #4 at 28.8, against our 28.1 (#5). We are down 0.8 over 15 min, so keep idle losses small.
- **t13 (#7, falling 1.2/15 min) has lowball bids at 2 P** on RET-01/02/03 (offers 9156-9158). That is not a price signal. t04 bids 26-27 for RET-06/08, which we need for our page, so do not sell them.
- **Venue v10 (Team 10, #3):** trades there feed a top-3 team. Use El Rastro or v15 for swaps, as now.
