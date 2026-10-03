# Scout (claude-sonnet-5-5, Sat 13:31)

## Top 3 actions now

1. **Hold the SAL-06 thread, then sell to Pilar only at ≥ 25 (Operator background job, Abuela thread 868).**
   - Evidence: Abuela's offer sits at 29 against our 21, and the clock has been paused since tick 630. Her earlier finals were 25 against our 22 (tick 596), and her uncommon deals at ≤ 25 moved the ladder. Pilar's uncommon sells landed at 18, 19 and 23 and moved the ladder +0.050 / +0.040 / +0.019.
   - Effect: buying at ≤ 25 against SAL value 22.5 costs about −2.5 neg. The resale to Pilar in the 16:00-18:00 window is the ladder gain. Ladder is 0.181 and uncapped [L]. The net only pays if the Pilar price clears ≥ 25 [L]; her SAL finals have been 23-25, so the margin is thin.
   - Confidence: med-low. Fallback: walk once she mirrors our step and stops moving.

2. **Keep the 4 stall asks on v15 and the LAV-03 → t04 ask live, and re-address them after the pause (Operator, `trade.py`).**
   - Evidence: the cards are LAV-02/03/04 (value 3.2 each) and LAT-04 (1.2), listed at 5-8. They are addressed to collectors per intel/multipliers.json. The rival profile shows Team 7 (#17, 11.3 below us) collecting RET/LAV/LAT, with an estimated ~9.5 each.
   - Effect: +4 to +6 neg each as maker with no fee. These are small trades far under the 50 cap.
   - Constraint: do not sell to the top 4 (T14, T12, T18, T10). Asks to t03, t04, t09 and t16 are fine under the feeding rule.
   - Confidence: med.

3. **Bargain watch (Operator, `logs/bargains.log`): bid on a team-held card only if value − price − fee ≥ 50.**
   - Evidence: the 13:15 GUARDRAIL allows one buy up to 100 total from a team outside the top 5. Our LAV-11 buy is open (value ~234). Team 8 offered it at 117 to t02/t12/t09 and a dealer paid 140.
   - Effect: up to +50, the cap (≈ +4.7 board).
   - Constraints: re-read the value before buying. This conflicts with the 12:39 LAV-11 guardrail on cash, so use only one of the two.
   - Confidence: low-med. Whether the card is still available is not in the data.

## What the climbing teams are doing
- **Team 14 (#1, 30.8, +1.1/h)** sells commons at 9 each to many buyers, with RET-01/02/03/04 going to t04, t09 and t15 (ticks 591-598). It also dumps RET while collecting LAV/LAT. Its volume is mostly fresh deals at clearing prices.
- **Team 10 (#3, +4.1/h)** built score on its own venue v10. It has a 74 P MAL-10 buy from Team 3 at tick 585 and 197 listings. Value created on v10 counts for its market-making.
- **Team 6 (#9, +4.6/h)** has 296 listings and 19 team deals. It sold RET-09 to Team 2 for 84 at tick 504.
- **Team 15** swaps cards 1:1 at 0 P with Team 7 (ticks 607, 613, 616) and has 22 team trades. Swaps need no cash.

## Threats
- **Lunch pause (tick 630):** all our messages are blocked. Dealer offers expire after 4 ticks, so the Abuela 29 may lapse on resume.
- **Team 14 is #1 and Team 12 is #2:** both are in the top 4, and a venue trade hands them market-making value. We trail #1 by 2.7 (30.8 vs 28.1).
- **Team 4 (#10, collects LAV/RET)** bids 26-27 for RET-06/08 and 64 for LAT-09. It competes for the same RET uncommons we hold. The bids are not addressed to us.
