# Scout (claude-sonnet-5-5, Sat 22:07)

## Top 3 actions now
1. **Keep SAL-11 bid 18977 (115 → t04, v15, exp tick 1371) live and re-post at ≤125 if it lapses.** Operator, via trade.py/rbuy.py.
   - Evidence: GUARDRAIL 21:45 (≤125, floor 260). Our value is 162 (first copy). t04 dumps SAL. t10→t17 paid 207 for SAL-11 at tick 1296. Cash is 392.
   - Effect: about +37 to +47 neg_points before drag and fee; the directive estimates +2.3 board. Offers last half the asked ticks on Saturday, so ask for double. Confidence: med (t04 has not replied to pings).
2. **Run the RET-09 t08 → t09 match at ~100 on v10 (Lucas DMs both sides).** Lucas/Dani, from intel/matches.md.
   - Evidence: matchmaker's top match. t09 is a page-closer with RET at 9/10. t08 dumps RET. Metrics show t13 bids only 42 for RET-09/10 and t09 has no RET-09 ask. Estimated value created is about +134.
   - Effect: market-making "real trades" on our venue, not neg_points; it may also qualify us for the 10 P rebate. Do not route it to t10's venue. Confidence: med.
3. **Place the MAL-09/10 matches for t09 on v10 at ~50-56.** Lucas/Dani, from non-rival teams only.
   - Evidence: t09 bids 56 for MAL-09 (offer 19105) and MAL-10 (offer 19129). Directive: ~50 P, not 75. t15 also wants them. t10 sold MAL-06 to t09 at 20 (tick 1230) and is the likeliest seller, so keep its gain small.
   - Effect: more value created on v10 and a possible page close for t09. No neg_points for us. Confidence: low-med.

## What the climbing teams are doing
- **Team 10 (#1, 38.6, +5.0/h)** sells epics at 195-207 and buys at 205: MAL-11 from t08 at 195 (tick 1264), SAL-11 → t17 at 207 (tick 1296). Its page is closed. It has a bid of 205 on LAV-11.
- **Team 12 (#3, +1.8/15min)** pays high prices for whole-collection value. RET-11 from t06 at 216 (tick 1245), SAL-09 sold to t09 at 70, LAT-10 from t01 at 86 (tick 1304), LAT-06 from t09 at 20. It collects RET/MAL/LAT and keeps trading across sets.
- **Team 13 (+1.4)** has 86 deals and 1130 listings. It floods cheap bids on RET (4 / 13 / 42) and sold LAT-10 at 72 to t18 (tick 1332). Team 1 (+2.5) is also up.

## Threats
- **Team 12 is closing on us.** It is at 31.1 against our 30.7 and rising 1.8 per 15 minutes, while we move -0.2. RET-11 at 216 shows it pays above our 198 valuation.
- **Team 10's SAL-11 sale to t17 at 207** shows what SAL-11 is worth to others. Our 115 bid is under that, so t04 may sell elsewhere first.
- **Team 13's cheap RET bids (42 for rares)** are a lowball channel. Do not feed v03. Selling our spare RET cards at its prices would lose value.
