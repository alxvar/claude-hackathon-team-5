# Scout (claude-sonnet-5-5, Sat 22:28)

## Top 3 actions now

1. **Keep the SAL-11 bid on t04 alive: bid 19620 (115 → t04, expires tick 1432); if it lapses, re-post at ≤ 125 on v15 with 2× ticks. Operator/trade.py.**
   - Evidence: the 21:45 GUARDRAIL allows SAL-11 at ≤ 125. Our value is 162, so the gain is ≈ +37 over the price. Cash is 392, above the 350 floor. Team 10 sold SAL-11 to t17 at 207 (tick 1296), so t04 may be a dumper but is not the only holder.
   - Expected: about +30-37 neg_points (the 50 cap does not bind). Pack drag is ≈ −2. At ≈ 0.05 board per neg point this is ≈ +1.5-2.3 board.
   - Confidence: med. t04 has not answered any bids.

2. **Offer RET-11 (epic, our value 198) only if someone bids ≥ 198; otherwise HOLD. Human: Lucas/Dani.**
   - Evidence: t12 paid 216 for RET-11 (tick 1245). Team 10 bids 210 for LAV-11 and t17 bids 150 for MAL-11. Selling below 198 loses in full.
   - Expected: no gain unless the bid is ≥ 198. Selling to t12 (#4) or t10 (#1) would feed a top-4 team, so no.
   - Confidence: low. It is a hold rule, not an opening.

3. **Sell our spare duplicates to non-rival buyers (Operator, maker offers).**
   - Evidence: the open offers (LAV-03 6 → t04, MAL-03 9 → t09, LAV-04 6 → t01, MAL-08 20 → t01) are live until tick 1385. t09 bids 56 for MAL-09/10 and 24 for SAL-06. t01 and t04 are not top 4.
   - Details: our SAL-06 is a complete-page card and stays reserved. Price MAL-06/08 near 20, which is above our value of 17.5; the market bid for uncommons is ≈ 24. Only the spares (2nd/3rd copies at 1.3-3.2) are safe to sell.
   - Expected: each sale gains the price minus the 1.3-3.2 duplicate value, about +3-6 per sale, and also helps the 10 P rebate/v10 desk goals. Selling MAL-08 could break the MAL page, so confirm it is not needed first.
   - Confidence: med.

## What the climbing teams are doing
- **Team 18 (#5, +1.9 in 30 ticks)** collects RET/LAT. It bought LAT-10 from t13 at 72 (tick 1332) and sells LAV/MAL. Its +0.1 over 15 min is small, but it is buying rares below the 77 book.
- **Team 4 (#10, +2.2/hr)** has 75 deals, the most on the board. It buys RET×6, MAL×5, LAV×4 and LAT×3 from teams, and took RET-10 from t06 at 84 (tick 1257). The volume looks like a team-trade grind.
- **Team 1 (#9, +2.4/hr)** has 33 deals and buys MAL×4 and SAL×4. It sold LAT-10 to t12 at 86 (tick 1304).
- **Team 10 (#1, +2.6/hr)** leads at 37.9. It sold SAL-11 at 207 and MAL-11 at 195 as a dealer-like flipper. It also bids 210 for LAV-11.

## Threats
- **Team 10 bids 210 for LAV-11.** Epic prices are rising, so our RET-11 hold is right. Do not route trades to its v10.
- **t09 is racing for MAL-09/10 at 56 P.** Team 15 also wants them, and the match is ~50 P. Don't feed the top 4.
- **We are #3 at 30.9, only 0.3-0.8 above #4-#6.** Team 12 (30.6) and Team 18 (30.1) are within 1 point, so a stale SAL-11 bid or idle accepts could cost a rank.
