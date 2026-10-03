# Scout (claude-sonnet-5-5, Sat 11:51)

## Top 3 actions now

1. **Hold the trader's accepts through Duels I. Keep the maker book live and unchanged.**
   - Evidence: the trader stopped at 11:50 and duels run ~11:30-13:05. We have 0 live duels and 34 finished, with `duel` 0.0. Our 13 asks are addressed to collectors and expire ticks 461-482; the 6 oldest (6426-6459) expire at 461-464.
   - Action: the operator re-posts the expiring asks (6426-6459) as maker before tick 461, asking for 2× the ticks wanted, since the server halves them. Candidates: MAL-02 9 → t01, SAL-08 25 → t03, LAT-04 4 → t15.
   - Effect: maker fills use the buyer's accept, so no fee and no conflict with duels. Small gains of +2 to +6 each. Confidence: med.

2. **Ladder test right after Duels I (~13:30): one Chato uncommon at his list 26.**
   - Evidence: all 6 of our Chato deals were above his list (RET-09 87 and RET-10 86 vs 77; RET-06 30 vs 26). Our ladder is 0.055 and Abuela's below-list deals moved it +0.014 to +0.018. Team 13 bought LAV-06/07 from Chato at 26 = list, then unlocked Pilar at tick 262.
   - Action: the operator runs `abuela_bot.py --dealer chato` for SAL-07/06. Open 24, step +2, hold silent, accept ≤ 26, walk on a final above 26. Do it alone in its window and compare `ladder_points` before and after.
   - Effect: cost about −3.5 neg_points (SAL worth ~22.5). If the ladder moves, do 2 more and then Pilar. Confidence: low-med.

3. **Dani places LAT-08 (ask 20) and the commons with Team 7 (#17, 12.2 below us, collects LAV/LAT).**
   - Evidence: the teams.md table gives LAT-08 21 est. (+5.5) and LAT-04 9.5 est. (+6.3) to Team 7. Our asks to t07 (6427 at 6, 6622 at 8) are unfilled.
   - Action: Dani tells Team 7 in person that the addressed offers are waiting. Our LAT-08 ask 6609 at 20 is addressed to t03. Add a LAT-08 ask to t07 only if Team 7 is not a top-4 rival. It is not (#17).
   - Effect: +4 to +6 per fill. Confidence: low. Team 7 has 5 trades in total and has not filled for 50 min.

## What the climbing teams are doing
- **Team 14 (#1, +7.2 in 15 min)** collects LAV/RET/LAT and has only 21 deals. It has bought RET-08 from t13 at 20 (tick 370) and has 4 LAT and 2 RET trades. It gains through page-completing buys, not volume.
- **Team 17 (+4.0 in 15 min, #7)** buys MAL×3/SAL×3. We sold it SAL-06 on Friday. It is climbing again with 19 deals.
- **Team 13 (#2)** has 45 deals, the most of any team. Its path: buy at Chato's list (26), unlock Pilar early, sell above his buy list. Its neg is 24.3 vs our 14.9 (snapshot 390).
- **Team 6** is active on rares: LAV-10 from t16 at 82 (tick 375) and SAL-10 from t01 at 76 (tick 376). It sits at #14, so it is not a threat.

## Threats
- **Feeding Team 13 via v10-style venue trades.** A negative-value trade on our own venue cost us −5.2 mm_points. Only collector-buys-from-non-collector trades go on our venue.
- **SAL-09 bids at 68-69 (t02, t06).** If either closes a SAL page, it is a top-4 or climbing buyer. We hold no SAL-09, so there is no action.
- **Rank slide:** we are #10 (22.7) with Team 4 (+0.5) and Team 17 (+4.0) closing. The gap to #7 is 0.7. A fill on any of the asks above matters.
