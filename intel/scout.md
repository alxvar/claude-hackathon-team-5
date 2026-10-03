# Scout (claude-sonnet-5-5, Sun 00:13)

## Top 3 actions now

1. **Keep SAL-11 bid 20252 (115 → t04, v15, expires tick 1565); be ready to raise to ≤125 at Sunday open (Operator, `trade.py`, maker).**
   - Evidence: the directive (Sat 21:45) allows ≤125 against our value of 162 (first copy). t10 sold SAL-11 to t17 at 207 (tick 1296), and an ask for SAL-11 at 245 is open on El Rastro. Cash is 392.
   - Effect: a fill at 115-125 is about +37 to +47 neg_points, below the +50 cap. About +2.3 board per the directive.
   - Caveat: the 115 bid is the same price level that t04's own ask of 245 shows is not yet clearing.
   - Confidence: med.

2. **Sunday 09:00: buy CHA rares from the Pícaros at 48-52 (≤54). Operator, `abuela_bot.py --dealer`, with the trick guard on.**
   - Evidence: CHA rare value is 112 for us. The dealer-lab ladder file says the Pícaros accept rares at ≤54, not 62. The Pícaros rare median was 55 in the last 60 ticks. Sunday budget is about 330 P for the CHA page, from cash 392 + 150.
   - Effect: a dealer buy at or below our value adds 0 to neg_points but builds the page. The last card should come from a team trade as maker, for the +50 cap and the page bonus (CHA 106).
   - Confidence: med. The page effect is [L].

3. **Don't spend on MAL yet. Lucas/Dani: buy Team 15's spare MAL-07 via a team trade only after the CHA budget is secured.**
   - Evidence: MAL bids are open from t09 (MAL-09 and MAL-10 at 56 P, offers 19719 and 20251). Their cost is unmeasured. t09 is rank #16 at 23.3, so it passes the feeding rule. Directive: MAL stays Sunday, as a fresh round.
   - Effect: a page-closer gives about +50 at most. The page bonus is not shown for MAL.
   - Confidence: low.

## What the climbing teams are doing
- **Team 18 (#2, +1.2 over 60 min)** collects RET/LAT and bought LAT-10 from t13 at 72 (tick 1332). It makes few team trades (16 team / 23 dealer), so its gain is selective and per-trade.
- **Team 12 (#4)** is buying epics and rares: RET-11 from t06 at 216 (tick 1245) and LAT-10 from t01 at 86 (tick 1304). It also took LAT-06 and LAV-08 (at 14) from t09 and t08. It holds 29 team trades, the most of the top 4, and it buys across sets (LAT×8).
- **Team 10 (#1, 37.6, falling −0.3)** sold SAL-11 at 207 and MAL-06 at 20, and bought MAL-11 at 195 from t08. Its lead is still 6.3 points over us.
- **Team 6** is down −2.7 over 60 min while selling RET-10 at 84 and RET-06 at 30.

## Threats
- **Team 12 (#4, 30.4) is 0.1 below us** and is buying epics and rares. RET-03 (10) and RET-01 (8) asks are open; they are not worth chasing for us.
- **Team 9 is bidding on MAL rares and SAL-06 (24)** against our MAL close. The likeliest MAL seller is t10, so keep its gain small.
- **Feeding v10:** t10 (#1) owns v10, and our v10 plan is the swap desk. Keep it to non-rival pairs, as the Club Castizo rules say.
