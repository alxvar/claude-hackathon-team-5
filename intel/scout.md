# Scout (claude-sonnet-5-5, Sun 06:13)

## Top 3 actions now

1. **Hold position until Sun 09:00 and run the CHA fast start first** (Operator; Pícaros CHA-09/CHA-10 threads at round 3's first tick, --offer-only, plus capped public bids). Evidence: the directives say the print runs run out (SAL-09 29/30, SAL-11 9/9). We hold 392 P cash and the CHA multiplier is 1.6. The game is closed until Sunday 09:00 (tick 1445), so nothing live moves overnight. Effect: CHA page close, with the cap at +50 per trade. Confidence: high.

2. **Keep the two open addressed asks, LAV-03 at 6 → t04 (19979) and LAV-04 at 6 → t01 (19981)** (both expire at tick 1455). Evidence: our spare copies are worth 3.2 each, so a 6 sale is above value. Neither buyer is a top-4 team, but t04 and t01 are among the buyers collecting LAV (per the profiles). Effect: about +2.8 each, which may not score as dealer-style gains. Confidence: low. Offers stay open while the clock stops, so re-list them OPEN at ≥ 6 on a non-rival venue if they lapse (open asks fill about 10× more often).

3. **Sell RET-03 / RET-01 only if the buyer is not a top-4 team. Do not feed t10.** Evidence: t10 is #1 at 37.6 and bought RET-03 at 8 from our side of the market (tick 1392, t10→t06). The asks RET-03 10 and RET-01 8 sit on El Rastro. Both are page cards worth 83.9 to us, so we should not sell them. Actual action: Operator checks `/api/me/value` before any ask is touched, and approves directive row #1 (RET-09 t07 → t09, +67.6 VC on v10, which is our venue's value-created score). Confidence: med.

## What the climbing teams are doing
- **t12 (#4, 30.4)** is buying LAT (8 team buys) and high-end cards: RET-11 epic from t06 at 216 (tick 1245), LAV-08 from t08 at 14 (tick 1420), LAT-10 at 86 (tick 1304). It is converting cash into epics and rares from teams.
- **t10 (#1, 37.6)** is selling to others as well as buying: MAL-11 epic bought from t08 at 195 (tick 1264), SAL-11 sold to t17 at 207 (tick 1296), MAL-06 sold to t09 at 20 (tick 1230). It runs 467 listings and 46 dealer trades, so it is volume-driven.
- **t06 and t07 trade RET heavily**: t07 has 9 RET team buys, and RET-06 went t06→t07 at 30 (tick 1417). Both are chasing the RET page, so RET cards are in demand.

## Threats
- **t10 leads by 7.1 points** (37.6 vs 30.5), and t18 (31.3) and t12 (30.4) are within a point of us. A MAL close past our cap is the relative-score lever the directives approve (≥ 150 P left after CHA).
- **t07 and t09** compete for the RET page: t07 buys RET (×9) and t09 buys RET (×5). The directives plan RET-09 t07 → t09 on v10, so check that it does not feed a rival.
- **The Pícaros trick offers**: the dealer-code TRICK guard shipped (e461e3b) but needs a bot restart. Until it is loaded, every Pícaros thread runs --offer-only. Flags are exhausted (a Sat 17:43 probe scored 0).
