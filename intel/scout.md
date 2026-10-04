# Scout (claude-sonnet-5-5, Sun 02:10)

## Top 3 actions now

1. **Hold the line until Sunday 09:00 (game closed; Sat 23:00 → Sun 09:00).** Metrics at tick 1445: `neg_points` 119.1, flat for 15 min, #3 at 30.5 vs #2 Team 18 at 31.3. Nothing new can score tonight. Operator: leave the two open asks, 19979 (LAV-03 → t04 at 6) and 19981 (LAV-04 → t01 at 6), both expiring at tick 1455. Re-list them as OPEN asks on v10 at 09:00 (directive 00:37: open asks fill 10× more often than addressed ones, 3.5% vs 0.3%). Effect: about +1-2 neg_points, because our value for these cards is 3.2 each. Confidence: med.

2. **Sunday 09:00: CHA rares first, from the Pícaros at round 3's first tick, in --offer-only mode (Operator).**
   - Evidence: Pícaros sold SAL-09 and SAL-10 at 54 each (tick 904 line, +15.5 together with the t07 swap). Print runs run out (SAL-11 9/9). Our CHA value is 1.6×, so rares are worth 112 against a dealer price of about 54.
   - Buying below value scores. Check card and rarity before accepting (the trick guard is not in the dealer code per the red team; the 01:15 log says e461e3b adds it, so the Operator restarts the bots to load it).
   - Effect: up to the +50 per-trade cap on the page-closing trade. The +40.4 SAL-06 close at tick 988 is the precedent. Confidence: med.

3. **RET-09 t07 → t09 on v10 (row #1, approved), plus a bid on RET-06 (t16 bids 18 for it; asks cost us).**
   - Evidence: t07 is #17 at 20.2 with `collects RET` and RET×9 buys. Team 7 sold RET-06 at tick 1417 for 30. t09 is 7.3 below us, which meets the ≥ 6 rule.
   - Action: the Operator brokers it; Lucas and Dani confirm with the humans on WhatsApp first (the matchmaker's raw list had 6/20 wrong buyers).
   - Effect on us: none directly, since it is v10 value created (+67.6 VC). Confidence: med.

## What the climbing teams are doing
- **Team 18 (#2, +0.8 per 30 ticks)** buys RET/LAT: LAT-10 from t13 at 72 (tick 1332), and it has 23 dealer trades. It is closing the LAT and RET rare pages and sits 0.8 above us.
- **Team 12 (#4)** is the heaviest buyer of the high-value cards: RET-11 epic at 216 (tick 1245), LAT-10 at 86 (tick 1304), LAT-06 at 20 (tick 1303), and LAV-08 from t08 at 14 (tick 1420). It has 70 deals, buying LAT×8.
- **Team 10 (#1, 37.6)** collects LAV/RET, with MAL-11 epic at 195 and SAL-11 epic sold to t17 at 207. It holds the lead through volume (62 deals, 467 listings) and its own venue.
- **Team 6** sells RET rares and epics at 77-84 (RET-10 at 84 to t04, tick 1257; RET-11 at 216), so RET rares are priced at 70-85 on the market.

## Threats
- **Team 18 at 31.3 against our 30.5 (gap 0.8)**: any card we sell to t18 or t12 feeds a team above us. Keep both on the do-not-feed list.
- **Bids are visible**: addressed offers show in full in the feed. Keep CHA page bids short-lived and capped at the dealer accept price.
- **Dealer prices are drifting against us**: Chato's uncommon buy median is 13 and his rare/uncommon sells are above our value. Do not open dealer threads for anything other than CHA cards or ladder fodder.
