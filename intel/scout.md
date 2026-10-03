# Scout (claude-sonnet-5-5, Sun 00:18)

## Top 3 actions now

1. **Hold the overnight SAL-11 bid (offer 20252, 115 → t04 on v15) and raise it only at 09:00 if t04 hasn't accepted.** The directive ceiling is ≤125 (floor 260 for this buy only). Evidence: our value is 162 for a first copy; t04 dumps SAL; t10 sold SAL-11 to t17 at 207 (tick 1296), and Team 4's ask sits at 245. Effect: +2.3 board per the directive, about +35-45 neg_points before pack drag (not in the data). The bid expires at tick 1565. Executor: Operator via trade.py. Confidence: med.

2. **Close the MAL page on Sunday, not before (Operator).** Closer: Team 15's spare MAL-07 via a team trade. Evidence: we hold MAL-01..06 and MAL-08 and need MAL-07, 09 and 10, and t09 bids 56 for MAL-09/10 (offers 19719, 20251). Do dealer buys of MAL-09/10 first and take the closer last as a maker bid. A closer scores at most +50 (cap) in a fresh round. The MAL page bonus is 25% × 265 × 0.7 ≈ 46, so a closer is worth ≤ 50 + price. Confidence: med. The bid must undercut t09's 56. Do not bid against t09 above value.

3. **Sell the duplicate commons for page-closer prices to teams ≥ 10 points below us, and route them via v10 swaps (Lucas/Dani).** Evidence: LAV-03/04 asks are live at 6 (offers 19979 to t04, 19981 to t01). No team in the rival table passes the feeding rule above our value + 3. We hold spares worth 1.3-3.2: LAV-02 ×3 at 1.3, LAV-03 and LAV-04 ×2 each at 3.2. Effect: small (+2 or so each, cf. +2.0/+2.5 past team buys) but it feeds Club Castizo and v10 volume. Confidence: low-med.

## What the climbing teams are doing
- **Team 18 (#2, +1.2/60 min)**: it collects RET/LAT, bought LAT-10 from t13 at 72 (tick 1332), and the rival table shows it as the only top-5 team still rising. It is buying rares from teams below the dealer price, which is the same recipe we use.
- **Team 12 (#4)**: heavy LAT buyer (×8) and a recent page-style buyer. It bought RET-11 from t06 at 216 (tick 1245), LAT-10 from t01 at 86 and LAV-08 from t08 at 14 (tick 1420), so it picks up cheap uncommons and epics from dumping sellers.
- **Team 10 (#1, 37.6, flat or slightly down)**: a venue owner that also dumps SAL/MAL/LAT. It sold SAL-11 to t17 at 207 and holds epics. Its lead is 7 points and no longer growing.
- **t07 and t04 (RET buyers ×9 and ×6)**: they are filling RET pages. Team 4 dumps MAL/LAT/SAL, which makes it a source for our SAL-11 and MAL cards.

## Threats
- **Team 12 and Team 18 are within 1 point of us** (30.4 and 31.3 vs our 30.5). Another RET/LAT page close by either one would pass us. Do not sell them RET or LAT closers.
- **t09 bids 56 for MAL-09/10 and 24 for SAL-06**, so it competes with us for MAL rares. t09 is also the buyer of the RET-09 closer from t08/t07 (~100), a trade that helps v10 but leaves t09 closer to a page.
- **Round 3 CHA release.** Our cash is 392 against the Sunday CHA reserve (floor 350). The SAL-11 buy up to 125 eats into that. CHA rares from the Pícaros target 48-52 (accept ≤ 54); stay under budget there.
