# Scout (claude-sonnet-5-5, Sun 05:12)

## Top 3 actions now

1. **Hold the overnight asks; do not start new trades before the Sun 09:00 clock check.** Game is closed ("Closed until Sunday 09:00"). Our open offers 19979 (LAV-03 → t04 at 6) and 19981 (LAV-04 → t01 at 6) expire at tick 1455. Operator re-posts them OPEN (not addressed) on a non-rival member's venue, per the 00:37 listings directive (open asks fill 3.5% vs 0.3% addressed). Evidence: both spares are worth 3.2 to us, and the board shows no buyer passing the feeding rule. Effect: about +0.5 `neg_points` each, trivial. Confidence: high that it is safe, low on the gain.

2. **At the first tick of round 3, run the CHA page via Pícaros and the public bids capped at dealer accept prices (rares ≤ 54), under the 00:55 red-team fixes.** Executor: Operator with `--offer-only` and a card check. Evidence: CHA is our 1.6× set, so a rare is worth 112 against Pícaros' 54-55 (metrics: picaros rare median 55). Cash is 392 and the CHA need is 242-282 (case A/B/C). The cap is 50 per trade, and our SAL page close scored +40.4 (t08 SAL-06 at 28). Effect: up to +50 per page-completing trade; a CHA page-closer should land +40-50. Confidence: med (print runs run out, and Pícaros tricks need the guard).

3. **Row #1 of the v10 list: RET-09 t07 → t09 (page finisher for t09, approved).** Operator posts it addressed at 09:00. Evidence: directive 01:00 says +67.6 VC on v10. t09 is 7.3 below us, which meets the ≥ 6 rule. t09 is ranked #16 at 23.3, so the leaders are not fed. Effect: no `neg_points` for us (VC goes to mm_points, which is worth at most the 7.5 real-trades share). Confidence: med; the holder check is still unconfirmed for t07 (owners are masked, `/api/cards` shows "a team").

## What the climbing teams are doing
- **Team 18 (#2, 31.3, Δ +0.8)** collects RET/LAT and bought LAT-10 at 72 from t13 (tick 1332). That is below the 86 t12 paid at tick 1304, so it buys rares under the market price.
- **Team 12 (#4, 30.4, Δ +0.4)** bought RET-11 (epic) at 216 from t06 (tick 1245), LAT-10 at 86, LAT-06 at 20, LAV-08 at 14 (tick 1420), and SAL-09 at 70 for t09. It is a high-volume, many-set buyer (70 deals).
- **Team 10 (#1, 37.6)** has 467 listings, bought MAL-11 at 195 from t08 (tick 1264), and sold SAL-11 at 207 to t17. It feeds epics around while sitting on a 7-point lead.
- **Team 16 (#14, Δ +0.3)** is climbing slowly on RET buys. It is a candidate for the RET-01/RET-03 sales (rows #5/#6), subject to the rival check at 08:30.

## Threats
- **t12 (#4, 30.4) is 0.1 behind us and a heavy buyer** of RET and LAT cards. It paid 216 for the epic RET-11, so Pilar's price for our own RET-11 (hold for ≥ 198) can be undercut by teams.
- **Ladder and flags are spent**: ladder 0.483 moves nothing on the board and the flag cap is hit, so only team trades and CHA still move our rank. t12 is within 0.1 of us.
- **Leader t10 (37.6)** gains from any trade on its venue. Keep our own deals on El Rastro or non-rival members' venues.
