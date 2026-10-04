# Scout (claude-sonnet-5-5, Sun 05:28)

## Top 3 actions now

1. **Hold at the 09:00 open and run the CHA fast start (Operator, simple_buy.py with --offer-only on every Pícaros thread).**
   - Evidence: we sit #3 at 30.5 with 119.1 neg_points and cash 392, and the game is closed until Sunday 09:00. The 00:55 red-team fixes put both CHA rares from Pícaros at the first tick of round 3, with the trick guard and `--offer-only` active. CHA is worth 1.6× to us (rare 112, per the plan).
   - Effect: dealer deals pay only through the ladder (0.483 now). Team-trade CHA buys below value score as gains. Cap is 50 per trade.
   - Confidence: med.

2. **Page-closing team trades are the only lever that still moves the board (about +0.05 board per neg point).**
   - Evidence: tick 988, SAL-06 from t08 at 28 gave +40.4 neg_points (119.1 total). The 09:00 v10 list's row #1 is RET-09 t07→t09, a page finisher approved by the directives.
   - Action: Operator posts addressed or open bids for CHA and MAL page closers, only from non-rivals. Always check `/api/me/value` first. The MAL close is GO when ≥150 P is left after CHA (directive 01:40).
   - Effect: up to +50 per closer. The cap on the MAL close is unknown.
   - Confidence: med.

3. **Sell the spares OPEN, not addressed (Operator/trader, sells-only until 09:00).**
   - Evidence: the 00:37 directive says open asks fill 10× more than addressed ones (3.5% vs 0.3%). Our two overnight offers are addressed: 19979 LAV-03 at 6 to t04 and 19981 LAV-04 at 6 to t01. Both expire at tick 1455. Spare copies are worth 1.3-3.2 to us.
   - Action: relist LAV-02 (×3, worth 1.3 each), LAV-03 and LAV-04 as open asks on v10 or El Rastro at about 9-10. Open El Rastro asks for common spares are at 9-10 now (e.g. RET-03 at 10, LAV-02 at 10). Never sell to the top 4.
   - Effect: small, positive neg_points plus value created on v10. Also check t04 and t01 against the feeding rule before filling.
   - Confidence: low-med.

## What the climbing teams are doing
- **Team 10 (#1, 37.6)** moves epics between teams at 195-216 P: MAL-11 from t08 at 195 (tick 1264) and SAL-11 sold to t17 at 207 (tick 1296). It collects LAV/RET, with 467 listings and 62 deals. It also benefits from trades on its own venue v10.
- **Team 18 (#2, 31.3)** collects RET/LAT and buys LAT-10 from t13 at 72 (tick 1332), so it takes rares at or below the clearing price of about 70. It has 40 deals, fewer than us (53).
- **Team 12 (#4, 30.4)** is the most active buyer of epics and rares. It bought RET-11 from t06 at 216 (tick 1245) and LAT-10 from t01 at 86 (tick 1304). It also bought LAT-06 from t09 at 20 and LAV-08 from t08 at 14, with 70 deals.
- **Team 6** sells RET cards to many teams: RET-10 to t04 at 84, RET-06 to t07 at 30, RET-03 from t10 at 8. Its 969 listings show that volume of listings drives its deals.

## Threats
- **Team 10 (37.6) leads us by 7.1 points.** Every trade on v10 feeds its market-making score. Keep v10 trades to positive net value, in line with the 01:10 club split.
- **t07 → t09 RET-09 and rival page closers.** t07 and t09 both collect RET (t07 has 9 RET buys). Another team may close first, since RET-09 and RET-10 are in demand (t16 bids 28 for LAV-10 and 18 for RET-06).
- **Epic prices: t01 bids 152 for MAL-11, and Pícaros buys epics at 140.** A team bid for an epic must beat what a dealer pays, about 140 (GAME.md). Our RET-11 (198) goes to Pilar only at ≥198 (directive).
