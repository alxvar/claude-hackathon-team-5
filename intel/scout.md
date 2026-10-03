# Scout (claude-sonnet-5-5, Sat 16:51)

## Top 3 actions now

1. **SAL-10 from Los Pícaros (Operator, `abuela_bot.py --dealer picaros`, offer-only, structure check card:SAL-10, cash only).**
   - Evidence: the 16:46 walk came at their 60 FINAL against our 56 cap; the retry (open 44, +3 steps) was scheduled for 16:51. The metrics show conversation tick 779 "SAL-10: 73 → 60, ours 50, closed". Last time SAL-09 closed at 54 (73 → 56) and moved the ladder 0.200 → 0.270.
   - Guardrail: floor 60, buy at ≤ 63 (Lucas's 16:43 limit, corrected by the Chief).
   - Expected: about +0.07 ladder (L4 slot 2), 0 neg_points if the price is ≤ our 63. Resell to Pilar in the fever (18:04, ~85).
   - Confidence: med. Their final of 60 is inside our cap of 63, so a +3-step approach to ~60 should work.

2. **Flag only checkable false facts in a live Pícaros thread (Operator).**
   - Evidence: neg_points went 43.2 → 53.2 → 63.2 → 73.2 (+10 each on ticks 766, 769, 773). Tick 774 was −10 for a posture-line flag. The 7225 flag on a closed thread scored 0.
   - Action: flag only a card or price that differs from the structured offer, or a false print-run or "last one" claim, and only while the thread is open. No finality talk.
   - Expected: +10 neg_points per correct flag (≈ +0.7 board each).
   - Confidence: high on false facts, low on closed threads.

3. **Sell the spare commons to Team 7 (#17), Team 3 or Team 16 as maker (Operator via `trade.py`).**
   - Evidence: Team 7 is 10.6 points below us and its prices are c 9.5. Our spares are worth 1.2-3.2 to us. Estimated gains per the profile table: LAT-04 +6.3, RET-04 +4.7, LAV-03/02/04 +4.3 each. Team 16's bids (RET-01 and RET-02 at 5, MAL-03 at 1) also look usable.
   - Action: our 5 open offers already cover LAV-03/04, SAL-01/02 and LAT-03, so add LAT-04, RET-04, LAV-02 to Team 7. Maker means no fee.
   - Expected: about +4 neg_points each (small). Our own RET-04 is worth 83.9 as a page card; the table's 2.8 refers to the spare copy.
   - Check: confirm the copy is a true spare with `tools/policy.py can-give`.
   - Confidence: med.

## What the climbing teams are doing
- **Team 6 (+3.8 / +4.7):** a value-created stall seller. It bought SAL-09 from Team 15 at 68 (tick 781) and RET-04 at 5 (tick 766). It keeps buying SAL (×4).
- **Team 1 (+1.2 / +4.5, now #3):** only 23 deals, but it buys MAL ×4 and SAL ×4. Quality over volume.
- **Team 3 (+7.3 in 60 min):** bought LAT-09 at 88 from t16 (tick 724) and SAL-05 at 8, plus Pilar and L4 deals. It is buying rares from other teams.
- **Team 16 (+4.0 / 60 min):** it unlocked L4 at tick 761 (2 Pilar deals), sold LAT-09 at 88, and now bids RET and LAV commons at 1-5.

## Threats
- **Team 14 (#1, 30.6) vs our 30.0:** it was in the group unlocked to L4 at tick 781, so it is about to take the same Pícaros ladder slots we are working. Never trade with it.
- **Team 6 is rising fast** (+3.8 in 15 min) and is buying the same SAL rares we want. Do not sell SAL page cards to it or to Team 1.
- **Pícaros SAL-10 supply:** it opens to all at ~17:33, after which every team competes for the L4 slots and the 73 → 60 band. Our window is before then.
