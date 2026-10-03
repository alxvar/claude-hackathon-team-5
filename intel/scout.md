# Scout (claude-sonnet-5-5, Sat 20:59)

## Top 3 actions now

1. **Pícaros epic buy (RET-11 ≤ 155, else LAV-11), Operator, before tick 1230 (Duels II starts ~tick 1239).**
   - Evidence: the 21:00 GUARDRAIL fixes the floor at 350 and cash is 520. Pilar's epic median is 187 and t10 bids 205 for LAV-11. The directive says 0 neg at our value.
   - Effect: neg_points ≈ 0 (a dealer buy never adds). It is only an L4 upgrade, and the ladder is capped (negotiating flat 21.88).
   - Confidence: low-med. Whether the buy is worth doing at all is not in the data.

2. **Keep v15/El Rastro asks live to sell spares to non-top-4 teams (Operator; Dani points the buyers at them).**
   - Evidence: our open asks are MAL-08 at 20 and LAV-04 at 6 to t01, LAV-03 at 6 to t04, MAL-03 at 9 to t09 and MAL-02 at 40 to t08.
   - Effect: small positive neg_points per fill. MAL-02 at 40 to t08 is the only one with real upside, and it expires at tick 1214, so re-post it if it lapses. The rival profiles list no buyer that passes the feeding rule above our value + 3.
   - Confidence: med on the mechanism, low on size.

3. **Sunday MAL page, prepared tonight (Operator, Chief's plan).**
   - Evidence: Team 15's spare MAL-07 is the planned closer (directive 21:00). Bids are up: t09 bids 56 for MAL-09 and MAL-10, and t13 sold MAL-10 to t02 at 30 (tick 1191).
   - Effect: a page close is capped at +50 and is worth most in a fresh round. Tonight, buy MAL-09/10/06 from dealers only at ≤ our value (0.7 × 70 = 49 for a rare, 17.5 for an uncommon).
   - Confidence: med.

## What the climbing teams are doing
- **Team 2 (#9, +2.6 per 15 min)**: it bought RET-09 from Team 6 for 84 earlier, and at tick 1191 it bought MAL-10 from t13 at 30 P. These look like cheap rare buys toward pages.
- **Team 7 (#17)**: it is the heaviest team buyer (RET×8, LAV×7). Its latest buys are RET-08 at 24, RET-09 at 66 (from t04) and RET-10 at 77 (from t06). They suggest a RET page push from a team that is low on the board.
- **Team 10 (#1, 34.0)**: its 60-minute change is +1.9 and it bids 205 for LAV-11. It is spending its payday on epics.
- **Team 12 (#7)**: it is active at +1.0 per 60 min. It buys LAT cheaply from t15 (LAT-09 at 55, LAT-07 at 14) and sells LAT-08 to t09 at 10.

## Threats
- **Team 10 (#1) and Team 6 (#2)** lead us by 2.4 and 1.0 points. Never route trades to their venues, because t10's SAL-07 on v10 already wiped our mm_points.
- **Payday gives rivals +400 P.** Rivals can now pay for their page closers. Team 9 bids 56 for MAL-09/10 and 20 for MAL-06/SAL-06, so it competes with us for the MAL cards. Team 17 bids 150 for MAL-11.
- **Duels II starts ~21:17.** Our API budget is shared at 5 req/s, so writers stay stopped. Check that the duelist is running.
