# Scout (claude-sonnet-5-5, Sun 05:58)

## Top 3 actions now

1. **Open the CHA page at the first tick of round 3 (Sun 09:00), Pícaros rares first, on `--offer-only`.**
   - Executor: Operator, with `simple_buy.py` and the dealer bots.
   - Cash is 392 P. CHA is our 1.6× set, with 106 P page bonus (GAME.md: CHA 106).
   - Directive 00:55: the Pícaros CHA rares go in parallel with the capped public bids. Print runs run out (SAL-09 29/30, SAL-11 9/9).
   - Check card and rarity before each accept. The Pícaros trick guard is not yet in the dealer code.
   - Effect: a page-closing team trade can score up to +50 (cap, V). Saturday's SAL close scored +40.4.
   - Confidence: med-high.

2. **RET-09 t07 → t09 (v10 club deal) at 09:00.** Directive 01:00 approves it.
   - Executor: Operator addresses it, Lucas confirms with t09 by WhatsApp.
   - Evidence: t09 is #16 at 23.3, 7.3 below us at 30.5, so the ≥ 6 rule holds. t09 buys RET×5. The directive estimates +67.6 value created on v10.
   - Effect: on our mm_points, not neg_points. It likely fills v10's real-trades share (7.5 of the 30 market-making points).
   - Confidence: med.

3. **Sell the spare cards, open on a non-rival member's market.** Our spares are LAV-02 ×3, LAV-03/04 ×2, MAL commons and LAT-03/04.
   - Executor: trader with `--cash-floor 9999` (sells only), or `trade.py`.
   - Evidence: open asks fill 10× more often than addressed ones (3.5% vs 0.3%).
   - Our two overnight addressed asks, LAV-03 → t04 and LAV-04 → t01 at 6, expire at tick 1455. Repost them OPEN.
   - Target prices come from the El Rastro bids: t08 bids 5 for RET-02 and LAT-08, and t16 bids 28 for LAV-10.
   - Effect: small, about +1 to +2 P each, which funds CHA.
   - Never sell a page card (directive).
   - Confidence: low-med.

## What the climbing teams are doing
- **Team 18 (#2, 31.3, +0.8 in 30 ticks)** collects RET/LAT. It bought LAT-10 from t13 at 72 (tick 1332), and the same card went t01→t12 at 86 (tick 1304).
- **Team 12 (#4, 30.4)** is buying epics and rares from other teams: RET-11 from t06 at 216 (tick 1245), SAL-09 from t12, LAT-10, LAT-06 and LAV-08. It has 70 deals, the most of the top 5 on the board.
- **Team 10 (#1, 37.6)** buys by the page: MAL-06 at 20, MAL-11 at 195 and SAL-11 at 207, and it has the most listings (467). It also hosts v10-style club trades. Our 119.1 neg_points came mostly from +40.4 (SAL-06 at 28, tick 988) and +15.5 (tick 904), both team trades.
- Team 3 and Team 12 get no board gain from dealers. Team trades are the live lever (ladder is spent, flags are spent).

## Threats
- **Team 10 (#1, 37.6) is 7.1 above us.** Every trade on its venue feeds it. Keep our spares on non-rival venues and never feed the top 4.
- **RET-09/10 contention.** RET-10 sold t06→t04 at 84 (tick 1257), and t15/t16/t02 all collect RET. Chato's rare list is 77, so a team bid for a CHA rare must beat what dealers pay.
- **The Pícaros trick risk.** The guard isn't in the code yet, and the flag cap is spent (probe on 8507 scored 0). Check every offer by hand.
