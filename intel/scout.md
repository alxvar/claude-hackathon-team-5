# Scout (claude-sonnet-5-5, Sat 11:46)

## Top 3 actions now

1. **Hold the Chato ladder test until after Duels I (~13:30); no accepts from our bots before then.**
   - Action: the Operator buys one uncommon (SAL-06/07) from Chato at list 26. Open 24, +2 steps, accept ≤ 26, walk on a final > 26. Run it alone in its window.
   - Evidence: all 6 of our Chato deals were above his list and none moved the ladder (0.055). Team 13 bought at list 26 and unlocked Pilar at tick 262. Neg 24.3 vs our 14.9 at snapshot 390 (Lucas's directive).
   - Effect: at most −4 neg_points. If ladder_points move materially, do 2 more Chato deals, then Pilar.
   - Confidence: med.

2. **Sell our low-value spares to collectors only, on El Rastro.** The Operator already has 13 asks live.
   - Cards: LAT-08 at 21, SAL-08 at 25, MAL-06/07 at 20, and the spare commons at 4-11.
   - Evidence: the 13 open offers expire at ticks 446-464. Team 7 (#17, 12.2 below us) is the only listed buyer passing the feeding rule (LAT-04 +6.3, LAT-08 +5.5, LAV-02/03/04 +4.3 each). The last sale, SAL-01 at 7 (tick 351), scored +4.7.
   - Effect: +2 to +6 neg_points per fill. Refresh expiring asks; the book daemon does this.
   - Caveat: Team 7's asks haven't filled in 50 min (log 11:32). Re-address LAV-04 and similar commons to Team 1 or Team 9 if they bid, since both are collectors.
   - Confidence: med.

3. **Sell SAL-08 to Team 3 at 25 (offer 6447), and LAT-08 at 21 (offer 6425).**
   - Evidence: Team 3 (#13, 17.8) collects SAL/LAT/LAV and is 4.9 points below us, and the 10-point feeding gap is not met. The Operator planned SAL-08 for Pilar before 17:30 as the alternative.
   - Action: keep both offers live. If Team 3 hasn't taken SAL-08 by ~16:00, move it to Pilar.
   - Effect: ~+2.5 for SAL-08 (value 22.5, ask 25) and +8.5 for LAT-08 (value 12.5, ask 21).
   - Confidence: low-med.

## What the climbing teams are doing

- **Team 14 (#1, 29.1, +7.2 in 15 min)** collects LAV/RET/LAT. It has only 10 team trades and 21 deals overall, so the jump likely comes from page bonuses or Duels, not volume [not in the data].
- **Team 13 (#2)** trades most (45 deals). It bought MAL×6 and SAL×2 on teams-trade, dumps LAT/LAV/RET, and unlocked Pilar early with 3 Chato deals. It bids for rares: t17 has MAL-09 at 85.
- **Team 1 (+6.3/60 min) and Team 4 (+4.6)** do rare swaps and commons for pages. Team 1 sold SAL-10 for 76 and LAT-09 for 68. Team 4 sold MAL-03 to us at 5 and collects LAV/RET.
- **Teams 6 and 9** are consolidating pages: Team 6 bought LAV-10 for 82 and SAL-10 for 76; Team 9 bought MAL-07, MAL-04 and SAL-05 within ticks 380-383.

## Threats

- **Team 14 and Team 13 are the leaders.** Any collector sale to Team 14 (LAV/RET/LAT) feeds #1 and breaks the rule, so no LAT/LAV asks go to it.
- **Team 2 bids 42 for RET-10, and Team 9 bids 8 for RET commons.** Both collect RET and could close the page before us. Our RET page holds 10 cards, so we are not racing for a card.
- **Value created on v10 is net and can be negative.** The −5.2 hit on mm_points, with t10 now top 4. Keep v10 trades to collector buys only.
