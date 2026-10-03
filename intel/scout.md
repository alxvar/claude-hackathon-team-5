# Scout (claude-sonnet-5-5, Sat 09:46)

## Top 3 actions now
1. **Buy RET rares from teams, not Chato.** Place short-lived (≤20 ticks) bids addressed `to` Team 15 (RET collector, bid 59 per GAME.md) and Team 2 (collects RET, bids 10-12 for RET-09/10, so it probably holds none to sell). Start at ≤70, ceiling 74 (our value is 77). Executor: operator via `trade.py` bid. Evidence: Chato's rare list is 77 with 82-93 finals, which is −5 to −13 each against our 77. Team 13 and Team 12 both collect RET and are top 4, so we cannot feed them. Effect: each rare bought at ≤74 is ≥ 0 neg_points; from Chato it costs 5-13. Confidence: low-med, since the metrics show no RET rare listed by any team.
2. **Finish cheap RET commons and uncommons through Abuela, then use that to reach level 3.** Bid 9 for RET-03 is open (offer 3256, expires tick 195; the ladder bot's last Abuela quote was 10, ours 9). RET-04 closed at 9 (worth 11). Keep patience to the `final`, never repeat the same price (directive 09:46), and keep at most 2 dealer threads. Evidence: Abuela deals are the only ones that moved our ladder (0 → 0.014). Effect: about 0 neg_points per deal, small ladder gain, progress to the 3 negotiated deals for the level-3 early start. Confidence: med-high.
3. **Re-price or retarget the maker book so it fills before tick 237.** Our 14 offers sit at 8-10 for commons and 26-33 for uncommons. Only two buyers show real demand: Team 16 for the SAL-03/05 and Team 7 for the MAL-02/04 packages (both addressed at price 0, which is wrong). Fix: reprice 3245/3246 to ~9 each card (clearing price for common is 9). Cancel SAL-08 → t02 at 33 (uncommon clears at 24.5) or drop it to 26. Do not touch t14: it is a LAV/LAT buyer and rank #3 on the board, so it is a leader. Evidence: previous sales scored +7.7 (LAV-04 at 9) and +6.0 (SAL-06 at 26). Effect: each spare that fills is about +2 to +8 neg_points. Confidence: med.

## What the climbing teams are doing
- **Team 2 (+6.3 in 15 min, the only mover up):** sold SAL-10 at 72 to t01 (tick 163), LAV-07 at 55 to t14 (tick 161) and SAL-02 at 9 to t01. It sells rares and uncommons to others while bidding low (10-12) for RET rares. Its 12 dealer trades are the most among the climbers.
- **Team 13 (#1, 30 deals):** buys MAL×5 and SAL×2 from teams (tick 166: MAL-07 from t17 at 25) and lists 47 offers. It is also lobbying to move trades onto its venue v03.
- **Team 14 (#3, steady -0.5 while the field falls about -4.5):** it holds its position by buying LAT×3 and LAV, e.g. LAT-08 from t01 at 25 (tick 182). It is the team to watch for LAV competition.

## Threats
- **Our neg_points reset to 0 while the field also reset.** We are #6 (15.4), only 0.2 behind Team 10 (15.2) and 1.7 behind Team 4 (17.1). Any +6 trade moves us.
- **Cash:** 393 P against the 370 floor. The venue bond (270) and the RET page (~280) cannot both be funded until the floor drops to 100.
- **Public feed leak:** our addressed RET bids are visible. Team 15 (RET collector, 59 bid) can see them and outbid us, so keep page-critical bids short-lived.
