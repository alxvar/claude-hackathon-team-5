# Scout (claude-sonnet-5-5, Sat 23:41)

## Top 3 actions now

1. **Keep SAL-11 bid 20252 (115 → t04, v15, exp tick 1565) live; raise to ≤125 only on Sunday if unfilled** (Operator, `trade.py`).
   - Evidence: our value is 162 for the first copy; t04 is the seller of SAL (collects LAV/RET, dumps MAL/LAT/SAL); the directive cap is ≤125. A card traded between other teams (t10→t17) went at 207.
   - Risk: an ask for SAL-11 at 245 is open elsewhere, so t04 may not fill at 115.
   - Effect: a fill at 115 is about +47 neg_points (the plan's own estimate, not measured); at 125 about +37. Not in the data: whether the +50 cap applies.
   - Confidence: med.

2. **Sell our spares to the buyers whose bids are already open** (Operator, maker offers on v10 for any card the buyer needs).
   - Evidence: t09 bids MAL-09/10 at 56 and SAL-06 at 24. Our MAL spares are worth 7, and MAL-08 is 17.5. Offers 19979-19982 expire at tick 1455, before Sunday's open at tick 1445+, so re-post them on Sunday.
   - Constraint: keep the sales to non-top-4 teams. t09 is #16, fine.
   - Effect: small, +1-3 neg each, plus market value on v10 if the trade runs there. Do not sell cards we need (MAL-06 and MAL-08 are for the Sunday MAL close).
   - Confidence: med.

3. **Broker the RET-09 t08→t09 page-closer at ~100 on v10** (Lucas/Dani DM both sides; Market session reads `matches.md`).
   - Evidence: t09 is at RET 9/10 and t08 dumps RET. The matchmaker puts the club-pair value at +89 VC, 68 of it from this one trade. Market is 7.5, and the full mark needs VC near the top-3 mean.
   - Constraint: t09 is #16 and t08 is #12, neither a rival.
   - Effect: market-making (real trades 22.5), not neg_points. Our own venue gains if the trade runs there. A trade at the match price scored 1.6 board points in the club's estimate. Not in the data: the exact board effect.
   - Confidence: med.

## What the climbing teams are doing
- **Team 18 (#2, +1.2 in 60 min)** collects RET/LAT, with 16 team trades. Its latest deal: LAT-10 (rare) from t13 at 72 (tick 1332). It buys rares from teams below Chato/dealer prices.
- **Team 12 (#4)** leads team-trade volume: 29 team trades, LAT×8 bought. It took RET-11 from t06 at 216, LAT-10 from t01 at 86, LAV-08 from t08 at 14, and LAT-06 from t09 at 20 (the last two are team deals, not dealer buys). Spare cards from sellers go cheap to it.
- **Team 10 (#1, 37.6)** has the most listings (467) and was the winning seller on v10 last time. It moves epics (SAL-11 to t17 at 207, MAL-11 from t08 at 195). Its flat −0.2 / −0.3 shows the lead is stable.
- **We (+0.0 / −0.4)** gained last from the SAL-06 page close, +40.4, bought from t08 at 28 on a team ask.

## Threats
- **Team 12 (30.4) is just behind us (30.5)** and is buying epics and rares. Do not sell it page cards: LAT, RET and MAL are the sets it collects.
- **t01 bids 152 for MAL-11 (epic)**, so epic prices are rising. A RET-11 sale at under 198 would hand over value; keep the Pilar threshold at ≥198, otherwise hold.
- **A rival could take SAL-11 before us.** t17 already holds one SAL-11 at 207, and our 115 bid is low against a 245 ask. The risk is a rival outbidding us on t04's copy.
