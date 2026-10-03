# Scout (claude-sonnet-5-5, Sun 00:53)

## Top 3 actions now
1. **Cancel SAL-11 bid 20252 (115 → t04) at the first live tick (Operator, trader.py).** Evidence: the Sat 00:21 directive (GUARDRAIL) orders this cancel in both clock cases. It would expire at tick 1565 anyway, and it is worth about +0.2 pts per 115 P against about 0.7 per 100 P for MAL. Effect: frees 115 P for CHA and MAL, no neg_points change. Confidence: high.
2. **Round 3 first tick: CHA-09 and CHA-10 from the Pícaros, target 48-52, accept ≤ 54 (Operator, simple_buy.py with --offer-only and the trick guard).** Evidence: the book says a CHA rare is worth 112 to us against the Pícaros' 48-54. The Pícaros are the only dealer that sells below our value, and print runs are short (SAL-09 at 29/30, SAL-11 at 9/9). Their 4 flagged tricks (bait and switch) make the card check mandatory before each accept. Effect: dealer buys below value are clipped to 0 neg_points, so the gain comes from the page (CHA page bonus 106) and from the later team trade that completes it. The last card should come from a non-rival team trade, which scores up to +50. Confidence: med.
3. **Sell the RET-11 epic to Pilar at ≥ 198, in round 3 only (Operator, dealer script).** Evidence: our RET-11 is valued at 198 and Team 12 paid 216 for RET-11 from Team 6 at tick 1245. Team 8 got 140 from Pilar for a LAV-11 epic. Effect: neg_points stay at 0 or clip. A sale above value only moves the ladder (0.483 now, L3 weights ≈ 3× L2). Do not sell it to Team 12 (#4), it is a top-4 team. Confidence: low-med. It depends on Pilar's floor holding and on our ladder still counting, since Chief 17:45 noted the board is flat on it.

## What the climbing teams are doing
- **Team 18 (#2, 31.3, +1.2 per hour):** collects RET and LAT. It bought LAT-10 from Team 13 at 72 (tick 1332). It is the only top-5 team rising, so a competitor for the LAT and RET rares.
- **Team 12 (#4, 30.4, 70 deals):** the busiest buyer of LAT (×8) and a regular epic buyer. It paid 216 for RET-11 (tick 1245), 86 for LAT-10 from Team 1 (1304), 20 for LAT-06 (1303) and 14 for LAV-08 (1420). High volume at or below book is working for it.
- **Team 10 (#1, 37.6, 62 deals):** sells epics at 195-207 (MAL-11 to us 195? no, to t10 at 195; SAL-11 to t17 at 207), 467 listings, and it buys RET/LAV. It scores through breadth of listings and epic sales.
- **Team 6 (#6, 971 listings, 71 deals):** it is falling (−2.7 per hour) despite its trade volume, so listing volume alone doesn't hold a score.

## Threats
- **We are #3 at 30.5, with Team 12 (30.4) and Team 18 (31.3) within 1 point.** Team 18 gained +1.2 per hour while we lost 0.4. A pause leaves us exposed, so Sunday's first trades matter.
- **Team 12 and Team 6 trade epics and RET-11 among themselves at 216.** If we sell RET-11 below 198 to a dealer we lose against that price. Don't sell cheap.
- **CHA competition:** t09 bids 56 for MAL-09 and MAL-10 (offers 20251, 19719). That is the MAL rare demand we face at the MAL close, so our MAL buy must come in at or below the 49 cap or be skipped.
