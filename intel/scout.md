# Scout (claude-sonnet-5-5, Sat 23:25)

## Top 3 actions now
1. **Keep SAL-11 bid live overnight (maker bid on v15 to Team 4, ≤125).** Evidence: our value 162 (first copy), t04 dumps SAL, bid 19620 lapsed at tick 1432, a re-post of 115 was queued by the operator (job bz665n6tg). Asks: SAL-11 245 (another seller). Effect: ≈ +47 neg on Sunday's trade if t04 fills, about +2.3 board; ≈ +0.05 board per neg point. Executor: operator/trader bot, verify the job actually posted (check `/api/me/offers`). Confidence: med.
2. **Fill the MAL-09/MAL-10 gap for the MAL page via a team trade (Sunday, fresh round).** Evidence: open bids t09 MAL-09 56, MAL-10 56 (rivals for the same rares); we hold MAL-01-06 and MAL-08, and the page needs MAL-07/09/10. Directive: MAL close only if CHA is under budget (≈160 P), closer via Team 15's spare MAL-07, with a +50 cap counted in a new round. Executor: operator, bid addressed to the holder; ask price ≤ our value (MAL-09 17.5 × page effect). Confidence: low-med (t09 competes at 56 and is not a rival we feed).
3. **Route spare sales to non-rival teams on v10.** Sell our spares (LAV-02 ×3 at 1.3, LAV-03/04 ×2 at 3.2, MAL-03/MAL-08 offers 19979-19982 stay live overnight). Evidence: top bids t16 RET-06 18 and LAV-10 28, t08 RET-02 5. Our RET-06 is worth 100.4, so don't sell it; the t16 bid is below value. Effect: small (+0.5-1 neg per sale) plus mm_points for v10 if both parties are non-rivals. Executor: trader `trade.py` listings; the Club Castizo desk brokers. Confidence: low.

## What the climbing teams are doing
- **Team 18 (#2, +1.2 per 60 min)** buys RET/LAT: LAT-10 from t13 at 72 (tick 1332), and has 40 deals, far fewer than the leaders. It gets value with fewer, larger trades.
- **Team 12 (#4, 70 deals)** buys rares and epics: RET-11 from t06 at 216 (tick 1245), LAT-10 at 86 (tick 1304), LAT×8 overall. That is a heavy-volume page build.
- **Team 17 / Team 10** trade epics between them: SAL-11 t10→t17 at 207 (tick 1296), MAL-11 t08→t10 at 195 (tick 1264). Epic trades reach the top of the board.
- **Team 6 (#6, −2.7 per 60 min)** is dumping value: RET-10 to t04 at 84, RET-11 at 216, RET-06 to t07 at 30. It is selling to climbers.

## Threats
- **Team 10 (#1, 37.6)** is 7.1 above us and collects LAV/RET (our sets). Its market score is also fed by v10 sales, so any trade on its venue feeds it. Keep trades off v07/v03.
- **Team 18 (#2, 31.3, +0.3)** is 0.8 above us and rising, while we are flat (+0.0 / −0.4). Tick 1332 LAT-10 at 72 shows it will pay for rares; do not sell it RET cards.
- **Rival bids on MAL-09/10 (t09 at 56)** and t01's MAL-11 bid at 152 raise the cost of our MAL close; page-closer prices may exceed what we planned (≈ 50 P).
