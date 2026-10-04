# Scout (claude-sonnet-5-5, Sun 10:28)

## Top 3 actions now

1. **MAL page close, last card via ONE addressed El Rastro bid to a non-rival (t13 or t15).**
   - Non-last MAL cards: Pícaros MAL-09 → MAL-10 at ≤ 49 (value, 0 neg, L4); we hold MAL-06 and MAL-08 and are missing MAL-07, MAL-09 and MAL-10.
   - Last card: bid ≤ value-when-last − 50. Evidence: Sunday 10:25 directive (GO), t15 sold MAL-07 to t03 at 9 P (tick 1647), t13 buys MAL×9.
   - Expected effect: +50 neg_points at the cap. Our trade part is not capped (Analyst M5), but the metrics show neg_points stuck at 50.0 after the RET-11 sale.
   - Executor: operator (trade.py bid); Dani nudges t13/t15. Confidence: med.

2. **Do not post more RET-11-type sales or buys until the neg_points question is answered.**
   - RET-11 sold at 240 (tick 1730), but neg_points is still 50.0.
   - Ask the Analyst whether the Sunday round is capped at 50 or only lagging. The board refreshes every ~10 ticks.
   - If capped, extra +50 closers add nothing to our own score. Then MAL is worth only the relative-reference effect (directive 01:40) and cash should not be spent past that.
   - Executor: Analyst check, then operator. Confidence: med.

3. **Spend the 660 P cash only on non-negative uses; keep ≥ 50.**
   - Cash scores nothing. Dealers close ~14:00-14:15.
   - Use order from the directives: floors, then MAL if it scores, then ladder upgrades ≤ value, then non-rival asks ≤ value − 10.
   - Open asks from t16 (LAT-06 21, LAT-07/08 30) are not at our value, so skip them.
   - Executor: operator (trader/opps). Confidence: low-med.

## What the climbing teams are doing
- **t12 (#1, 35.1, +3.7/15 min)** trades the most. 29 team trades: LAT×8, buys RET (RET-11 for 216), and bought LAV-07 from t13 at 40 (tick 1712).
- **t18 (#3, +1.9/15 min, +4.0/60 min)** closed CHA with CHA-01 from t13 at 72 (tick 1513) and sold SAL-11 to t13 at 238. t13 brokers closers: SAL-10 to t09 at 68 and to t03 at 108.
- **t03 (#5, +1.8/15 min)** buys SAL-10 at 108 and MAL-07 at 9 (tick 1647).
- **t02** is paying 240 for RET-11 and 72 for CHA-05, so it is a buyer with cash (relevant only for non-closers).

## Threats
- t12 at 35.1 is 3.4 ahead of us and gaining fastest. Do not sell it LAT-08, MAL-03 or MAL-08 (its known gaps).
- t18 (32.9) is 1.2 ahead and t03 (29.8) is 1.9 behind us. A MAL closer must not go to either of them.
- Open public CHA bids (t16 67 for CHA-09, 64 for CHA-10; t09 at 15 for CHA-06/07/08) are for cards we hold. They are not a threat, only cards we could sell if the value drops (we value them at 218/146).
- Selling past our own cap still raises the field's reference (directive 01:40), so any gain we hand to the top 3 counts against us.
