# Scout (claude-sonnet-5-5, Sun 05:43)

## Top 3 actions now

1. **Hold the two overnight addressed asks and check them at 09:00 (Operator, `trade.py`).** LAV-03 → t04 at 6 (offer 19979) and LAV-04 → t01 at 6 (offer 19981) both expire at tick 1455.
   - Evidence: our spare copies are worth 3.2 each, so a sale at 6 is a small gain. t04 and t01 are #11 and #9, both ≥ 10 below us.
   - Relist as OPEN asks after expiry. Directive 00:37: open asks fill 10× more often (3.5% vs 0.3%).
   - Effect: about +2.8 each at best, so small. Confidence: med.

2. **Sunday 09:00 CHA fast start, then the MAL close (Operator, `simple_buy.py` and `abuela_bot.py --offer-only` for Pícaros).**
   - Evidence: neg_points 119.1, cash 392, and CHA is our 1.6× set. The directives say MAL close is GO at ≥ 150 P left after CHA. The MAL close is +30 np past our cap, which lowers t18/t12/t03.
   - Evidence from the rivals: t07, t10 and t12 were the ones moving epics and rares (RET-11 t06→t12 at 216). MAL-07 and MAL-09 are the cards still missing from our MAL page, MAL-06/08 are already held.
   - Effect: up to +50 per page-closing team trade (cap). Confidence: med; the prices are not in the data.

3. **Execute v10 row #1, RET-09 t07 → t09, as the 09:00 list says (Operator and Lucas by WhatsApp).**
   - Evidence: the directive says "+67.6 VC", and the listing is approved. It scores market-making for us, not neg_points.
   - Pre-check: t09 is #16 at 23.3, far below us. That satisfies the feeding rule.
   - Effect: likely fills v10's real-trades target alone. Confidence: med; the buyer's agreement is not confirmed in the data.

## What the climbing teams are doing
- **Team 18 (#2, 31.3, +0.8 per 30 ticks):** it collects RET/LAT. It bought LAT-10 from t13 at 72 (tick 1332), a team that dumps LAT, and sits below Team 10's 37.6.
- **Team 12 (#4, +0.4):** it buys LAT×8 and bought RET-11 (epic) from t06 at 216. It is cheap-buying LAT-06 (20) and LAV-08 (14) and LAT-10 (86). Its prices are c 7 / u 18 / r 76 / e 216.
- **Team 10 (#1, 37.6):** it sells epics (MAL-11 at 195, SAL-11 at 207) and uncommons (MAL-06 at 20), and has 62 deals. It is the top team and a venue owner.
- **Team 16 (+0.3, #14):** it sits low but shows positive changes, with 4 RET buys. It bids LAV-10 at 28 and RET-06 at 18, both far below our values (149.9 and 100.4), so there is nothing for us there.

## Threats
- **Team 10 (#1, 37.6):** it leads by 7.1 points and its dealers' epic trades grow its value; do not feed it. It collects LAV/RET, the same sets as us.
- **RET and LAV cards are contested.** t07 (RET×9, LAV×7), t04 (RET×6) and t09 (RET×5) are buying them; epics sell above 195, so a bid below ~198 for RET-11 loses.
- **We are #3 at 30.5, with Team 12 at 30.4 just behind.** One team trade of +10 np moves roughly +0.05 board per neg point, so a small gap can flip. Idle time costs us: the scores are relative and fall when others gain.
