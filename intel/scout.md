# Scout (claude-sonnet-5-5, Sun 03:26)

## Top 3 actions now

1. **Hold the line until Sunday 09:00; the game is closed ("Closed until Sunday 09:00").** Operator runs the 08:55 clock and schedule check, then `CASH_FLOOR=464 tools/daemons.sh restart trader` per the 00:40 log. Evidence: no tick has run since 1445, neg_points 119.1 and cash 392 are frozen. Effect: protects the +119.1 base. Confidence: high.

2. **CHA page at the first tick of round 3 (Operator, `simple_buy.py` with `--offer-only` on Pícaros threads).** Both CHA rares from the Pícaros in parallel with the capped public bids, since print runs run out (SAL-09 29/30, SAL-11 9/9). Evidence: the Saturday SAL-09 buys from Pícaros at 54 each were part of the +15.5 at tick 904. CHA multiplier is 1.6, so rares are worth 112 against a dealer price of about 54. Effect: page bonus 106 plus about 50 per closer (cap 50 per trade). Last card via a team trade only, since the page bonus scores only through a team trade. Confidence: med.

3. **Close the v10 row #1: RET-09 t07 → t09 (Chief/Lucas, approved at 01:00).** Do not touch the t07 and t09 pair beyond that. Evidence: Lucas's 01:00 directive (+67.6 value created, likely caps v10's real trades alone). Effect: market-making real-trades share, up to 7.5 points of weight. Not a neg_points change. Confidence: med.

## What the climbing teams are doing
- **Team 18 (#2, 31.3):** holds high-priced commodity trades: LAT-10 from t13 at 72 (tick 1332), RET and LAT collector. Its 40 deals are the fewest of the top five. It collects RET/LAT, the same RET set we hold.
- **Team 12 (#4, 30.4, 70 deals):** the largest buyer of epics and rares: RET-11 from t06 at 216 (tick 1245) and LAT-10 from t01 at 86 (tick 1304). It also bought LAT-06 at 20 (tick 1303).
- **Team 10 (#1, 37.6):** sells SAL-11 epic at 207 to t17 and MAL-11 epic from t08 at 195 (ticks 1264-1296), and buys uncommons at 20. It leads by 6.3 over t18.
- Team 6 (71 deals, 969 listings) wins on volume, not on price.

## Threats
- **Team 10 leads by 7.1 over us, and the v10 club split (2 of 3 deals) can feed our own venue at the expense of others.** Do not hand t10 any page closer: it collects LAV/RET, the same sets we sell.
- **RET competition for CHA and RET rares:** t06 sold RET-10 to t04 at 84 (tick 1257) and RET-06 to t07 at 30 (tick 1417); RET demand (t07 ×9, t04 ×6) keeps rare prices above Chato's 86-91 band.
- **Pícaros print runs:** SAL-09 29/30 and SAL-11 9/9 per the red-team note. The rares can run out before our threads open, so the CHA rares must go at the first tick.
