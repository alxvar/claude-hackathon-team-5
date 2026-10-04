# Scout (claude-sonnet-5-5, Sun 11:14)

## Top 3 actions now
1. **Keep the MAL-09 close alive (offer 22816, bid 48 to t08, expires tick 1930).** The mal_close.py job re-posts on expiry, one live bid at a time.
   - Evidence: t09 bids 68 P for MAL-10 (offer 23637), and we already hold MAL-10 (value 49). The Chief's 10:25 directive says MAL is the #3 race vs t18, and our trade part is not capped. Our neg_points is 0.0 → 50.0 after CHA at tick 1585, with 50.0 shown in the 15-min column.
   - Effect: the last MAL card scores about +50 only if the bid is ≤ value-when-last − 50. Everything before the last card must be ≥ 0. The effect on the board is not in the data.
   - Confidence: med. Operator, via mal_close.py. Never a dealer for the last card.
2. **Sell MAL-10 to t09 at 68 P (offer 23637) only if the MAL page stays out of reach.**
   - Evidence: the book value of MAL-10 to us is 49, so selling at 68 gives +19 gross before the fee. Our sale proceeds depend on t09 accepting, and t09 is #8 at 26.4, far below us at 32.2, so it passes the feeding rule.
   - Catch: MAL-10 is a card for our own page, so selling it kills action 1. Decide at the Chief's ≈ 12:00 MAL call.
   - Confidence: low. Operator, accept only, never a gift.
3. **Reprice the LAT-06/07/08 bids (22613/22614/22615/22813 at 9 P) to match the v10 reward and the market.**
   - Evidence: asks by others include LAT-08 at 30, and our LAT bids sit at 9. Clearing price for LAT commons is 7.5 and for LAT uncommons 21.5. The v10 reward (≤ 10 P each, ≤ 100 P total, LAT first copies) is already automated by v10_reward.py.
   - Effect: team-trade buys at ≤ value score ≥ 0. We don't lose points, and cash doesn't score. This is a low-value lever.
   - Confidence: low. Trader and book daemons.

## What the climbing teams are doing
- **t12 (#1, 34.9, +3.5 in 60 min):** it moves expensive cards: LAV-07 bought from t13 at 40 (tick 1712) and SAL-12 (legendary) sold to t16 at 380 (tick 1886). It has 78 deals and 29 team trades, and it is the #2 rival we must not feed.
- **t09 (#8, +6.9 in 60 min) and t04 (#10, +5.0):** both are broad team-trade buyers. t09 has RET×6, SAL×5, MAL×4, and t04 has RET×6, MAL×6, LAV×4. t04 also sold SAL-11 (epic) to t02 at 220 (tick 1858), which moves value. Climbing comes from volume across sets.
- **Epic trades:** RET-11 t05→t02 at 240 (tick 1730) and SAL-11 at 220 show epics trading at 220-240. Our RET-11 sale scored −119.1 neg (the reset to 0.0 at tick 1466), so the epic route is not a cap-free gain for us.

## Threats
- **t18 (#3, 32.2, tied with us at #4):** it collects CHA/RET and is the main race for #3. We feed it nothing, and cards must not go to t18 or t03.
- **t09 CHA bids are a trap:** t09 bids 15 for CHA-06/07/08 and 5 for CHA-01..05, while our CHA cards are worth 122-146 to us. t15 bids 6. Our page is complete, so these offers must not fill: a sale would cost a page.
- **v10 reward:** the Chief flagged a fair-play review risk on paying for venue activity. Our spend is capped at ≤ 100 P and ≤ 10 P per card, and each buy is ≥ 0 for us.
