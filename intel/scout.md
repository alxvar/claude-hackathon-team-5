# Scout (claude-sonnet-5-5, Sun 06:59)

## Top 3 actions now

1. **Sit tight until Sunday 09:00, then run the CHA fast start and the MAL close, with no new trades tonight.**
   - Executor: Operator, per the 07:05 Sun directive (case decided at the first live tick, `CASH_FLOOR=464` for opps) and the 01:40 directive (MAL close GO whenever ≥ 150 P is left after CHA).
   - Evidence: the game is "Closed until Sunday 09:00" (tick 1445). Cash is 392, neg_points 119.1, and we are #3 (30.5 vs #2 Team 18 at 31.3).
   - Effect: the MAL close is +30 neg_points past our cap, per the directive. CHA is not quantified in the data.
   - Confidence: med.

2. **Clear the two open spare offers: LAV-03 → t04 at 6 (19979) and LAV-04 → t01 at 6 (19981). Reprice them as OPEN asks on a non-rival member venue.**
   - Executor: Operator via `trade.py`.
   - Evidence: both are addressed offers that expire at tick 1455. The directive says open asks fill 10× more than addressed ones (3.5% vs 0.3%). The spares are worth 3.2 each to us.
   - Effect: small, about +3 each over our value, with no feeding risk. t04 is #11 and t01 is #9, both ≥ 10 below us.
   - Confidence: med.

3. **Have Lucas or Dani confirm the RET-09 t07 → t09 page-finisher on v10 at 09:00 (row #1).**
   - Evidence: t07 collects RET (RET×9) and sits at 20.2, and t09 is a RET buyer (RET×5) at 23.3, 7.3 below us. The directive approves it at +67.6 VC.
   - Effect: this feeds our market-making score on v10, not neg_points. VC is value created on our venue.
   - Confidence: med.

## What the climbing teams are doing
- **Team 18 (#2, +0.8):** it collects RET/LAT and is buying LAT-10 (tick 1332, 72 P from t13). Its RET purchases are also in the "who buys" list.
- **Team 12 (#3, +0.4):** it is trading epics and rares. RET-11 came from t06 at 216 (tick 1245), LAT-10 from t01 at 86 (tick 1304) and SAL-09 at 70 (tick 1231). It also has the most team trades among the leaders, with 29 team trades overall.
- **Team 10 (#1, 37.6):** it sells epics at ~200 (MAL-11 to t10 at 195 from t08, SAL-11 to t17 at 207). It has 467 listings and is flat now.
- **Team 6:** it sells into the RET market, with RET-10 to t04 at 84 (tick 1257) and RET-06 to t07 at 30 (tick 1417). It has 969 listings, but it is falling (Δ −2.4).

## Threats
- **Team 12 (#3 in rival profiles, 30.6)** is 0.1 below us and active. RET-11 at 216 is above our 198 value, so keep our RET-11 → Pilar only at ≥ 198.
- **Team 18** is 0.8 above us and gaining. Do not feed it; its RET/LAT buying is a reason to hold our RET cards.
- **Trading on v10 and other venues** feeds those venue owners. Team 10 leads (#1) and gains from VC on its own venue. The rival profiles show no buyers that pass the feeding rule above our value, so sell nothing to the top 4.
