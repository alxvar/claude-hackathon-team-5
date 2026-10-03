# Scout (claude-sonnet-5-5, Sat 23:46)

## Top 3 actions now

1. **SAL-11 bid 20252 (115 → t04, v15, expires tick 1565): keep it, and raise toward 125 only if t04 doesn't fill at Sunday's open. Executor: operator/trader.**
   - Evidence: t04 dumps SAL. Our value for SAL-11 is 162 (first copy). Team 17 paid 207 for SAL-11 (tick 1296, t10→t17). An ask of 245 is standing.
   - Directive cap: ≤ 125, floor 260.
   - Effect: a fill at 115-125 is about +37-47 on Sunday's trade part, roughly +2.3 board. Confidence: med.
   - Caveat: the maker bid is public in the feed (`offer.listed`). Keep it short-lived if a rival shows interest.

2. **CHA page at 09:00 Sunday: rares from the Pícaros (target 48-52, ≤ 54), and the last card from a team. Executor: operator via `abuela_bot.py --dealer`; Lucas/Dani find the holder.**
   - Evidence: the dealer-lab note puts the Pícaros rare accept at ≤ 54 (SAL-09/10 bought at 54 on tick 904). Dealer prices (last 60 ticks): Pícaros rare median 55. Cash is 392 (Sunday +150 gives ≈ 540); the CHA budget is ≈ 330.
   - Effect: CHA rare value is 112 or more per card, so dealer buys cost no neg_points. The page close through a team trade can add up to +50. Analyst range: +3.2-5.6 final [L]. Confidence: med.

3. **Hold the MAL close and the club: don't sell RET-09 or the other RET cards. Lucas/Dani push the t08→t09 RET-09 match onto v10, using our own spares only.**
   - Evidence: t09 collects RET/SAL/MAL and has bids up for MAL-09/10/SAL-06 (56/56/24). Match list: +89 VC on v10, 68 of it from one trade (RET-09 t07→t09). Market is 7.5, and the 22.5 real-trades part scales with VC.
   - Effect: market-making points, not neg_points. Our own spares stay unsold: the open asks LAV-03 → t04 at 6 and LAV-04 → t01 at 6 are worth about 3.2 each, so they are fine.
   - Confidence: low-med.

## What the climbing teams are doing

- **Team 18 (#2, +1.2/60 min) is buying LAT-10 rares from other teams:** t13→t18 at 72 on tick 1332, against t01→t12 at 86 for the same card. It collects RET/LAT and has 40 deals, which are quality buys rather than volume. It sits 6.3 below Team 10.
- **Team 10 (#1, 37.6) holds its lead by selling epics to team buyers:** MAL-11 at 195 (t08→t10), SAL-11 at 207 (t10→t17). It also posted 467 listings. Its score drifted -0.3/60 min, so it is not rising.
- **Team 12 (#4, 30.4) buys big and cheap:** RET-11 at 216 (t06→t12), LAT-10 at 86, LAT-06 at 20, LAV-08 at 14 (t08→t12). It has 70 deals and is 0.1 behind us.
- **Team 6 is the biggest dumper:** 71 deals, -2.7 over 60 min, selling RET-10 at 84 and RET-11 at 216. Its RET cards are sold, so t06 is a source, not a rival.

## Threats

- **Team 12 is 0.1 behind us:** they sit at #4 (30.4) with a 29-team-trade record, and our dead-heat #3 spot is exposed. Their RET-11 purchase at 216 is above our 198 value, so we should not buy RET-11.
- **SAL-11 competition:** t17 already holds one, and the 245 ask on El Rastro shows the market sits above our 125 cap. If t04 sells elsewhere, we lose the +2.3 board.
- **Feeding t10 (#1, 37.6):** keep v10 club deals to members only. A non-member sale on v10 would hand the venue owner value. Note that t10 holds the lead in the table above, even though the directive lists it among the club's non-rivals. Check this before any v10 routing.
