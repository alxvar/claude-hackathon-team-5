# Scout (claude-sonnet-5-5, Sat 11:30)

## Top 3 actions now

1. **Stop all trader accepts before 11:50 (Duels I), per the 10:35 directive.** Executor: operator stops loop.py at 11:50 and dealer threads at 11:40. Book.py keeps posting as maker. Evidence: the 34 duels have all finished, and the 11:30 metrics show 0 live duels. A missed duel deal is 0. The score fell 7.1 in 15 min (22.4, #7), so a collision would hurt more. Effect: protects the duel share (40% of Negotiating's duel part). Confidence: high.

2. **Re-address MAL-06 and MAL-07 to t17 at 26 (our value 17.5, +8.5 each) or to t15 at 21.** Executor: operator, by hand on El Rastro. Evidence: t17 bids MAL-09 at 70. t17 is a MAL/SAL buyer (MAL×3, SAL×3 in the metrics) and is 10.4 below us in intel/teams.md. We hold MAL-06 and MAL-07 now (offers 6112 at 20 to t17, 5813 at 21 to t15). t09 bids MAL-06 at 17 and bought MAL×2 plus MAL-07 at 17. Effect: ~+3 to +8 neg_points per fill, and the maker route pays no fee. Confidence: med. Check first that neither team is within 10 of us, because the board has changed since the 11:02 rankings.

3. **Sell LAV-02, LAV-03 and LAV-04 spares to t09 or t07 at 9-10 (value 3.2).** Executor: operator via book.py. Evidence: t09 just bought LAV-04 from t18 at 9 (tick 353) and has a LAV need; asks by others sit at LAV-04 10 (×4) and LAV-03 9 (×2). Our asks to t07 at 5-6 are below the going rate. Effect: ~+4 to +6 each (price − 3.2). Confidence: med. Avoid t14, who collects LAV and may be a closer. Check that t09 and t07 are not within 10 of us.

## What the climbing teams are doing
- **Team 1 (+7.0/h)** buys rares from teams: SAL-10 from t01 to t06 at 76, and LAT-09 t01→t16 at 68. It trades few cards (17 deals) at the top of the rare range.
- **Team 10 (+5.4/h)** buys LAV×2 from teams. It also sells (SAL-07 to t15 at 26) and pushes public bids on v07.
- **Team 16 (+5.5/15 min)** got LAV-10 sold to t06 at 82 and LAT-09 at 68. It sells rares for 68-82 against Chato's ~89.
- **Team 13 (#1)** ranks high on team-trade volume (MAL×6 plus SAL×2 buys) and lobbies for v03 trades.

## Threats
- **Team 13 and Team 18 lead (27.7, 26.6).** Any SAL/MAL page-closer sold to t13 feeds the leader. Keep MAL/SAL sales addressed to t17/t15/t03 only.
- **Our drop to #7 (22.4) comes with cash stuck at 114.** Public bids on SAL-04 and MAL-03 are small and tie up cash near the 100 floor.
- **Rare prices on El Rastro (SAL-09 64-68, MAL-09 70, RET-10 36 bid by t02) are not clearing against us.** t02 bids 36 for RET-10, which we hold at 149.9 value; we should not sell it.
