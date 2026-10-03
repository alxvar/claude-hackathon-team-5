# Strategist (claude-opus-5-5, Sat 14:54)

## How the points really work
- **Day weights.** The board now is (0.5·Fri + Sat)/1.5 [V]. The final score is (0.5·Fri + Sat + Sun)/2.5, so Saturday and Sunday weigh 40% each. Round 3 starts at game hour 16.65. Sunday from 14.736 to 16.65, including the 15.0 bench, still counts for round 2 [L, schedule].
- **Saturday conversion rates:**
  - 1 `neg_point` ≈ 0.094 board.
  - +0.01 ladder ≈ 0.33 board.
  - 1 market point ≈ 0.667 board (Saturday's weight).
  - Sunday's rates are not in the data.
- **Our parts:**
  - neg 35.2 (≈3.3 board, flat since tick 404).
  - ladder 0.181 (≈6 board, flat since 12:45).
  - duel 13.93.
  - Market is at the stall bench only: value created on v10 nets −5.2, floored at 0.
- **Caps:** a team trade scores at most +50. Value created is capped at +5 market and floored at 0. The ladder counts the best 3 deals per level. Every part is relative to the leader.
- **Gaps:** −0.8 to #3 (t10), −1.5 to #2, −2.7 to #1 (t14). t14's edge ≈ one value-created trade on its stall (+3.10 board).
- **Where the field is weak:**
  1. **Value created.** Our single positive v10 trade moved market 7.5 → 12.5 (+5 ≈ +3.3 board), more than our whole gap to #1. Every board venue scored below the stall today, and Team 3 got 0.
  2. **Level 4 (Pícaros).** Every team is at 0 there, and higher levels weigh more (L3 ≈ 3× L2).
  3. **Bench.** All stalls tie, and nothing shows a broker beating it. Not a lever for us: cash 184 < the 270 bond.

## Our winning strategy
1. **Be a market maker with no broker:** pairmaking onto v10. One positive trade (seller with a low multiplier → buyer with a high one, both outside the top 5) lifts us off the floor and may hit the cap. Our two data points fit (buyer m − seller m) × book: MAL-07 +0.2×25 = +5; SAL-07 −0.4×25 = −10 [L]. We need net > +5.2, i.e. any uncommon or rare with Δm ≥ 0.4.
2. **Sunday Chamberí at 1.6.** Team buys below our value score in full:
   - common 16 vs clearing 9 → +7
   - uncommon 40 vs 24.5 → +15.5
   - rare 112 vs 70-84 → +28-42
   - page closer +50
   - Dealer buys at ≤ value cost 0 neg, and add ladder when below list.
   - At those prices the page costs ≈ 279 P (5×9 + 3×24.5 + 2×80); cash 184 + the 150 grant covers it.
3. **Ladder:** Pícaros (L4) today; rebuild every level from zero at round 3 if it resets.
- **Stop:**
  - Chato buys above 26.
  - Treating the spares book as a lever (0 fills in 226 ticks).
  - SAL-06 from Abuela, unless swap 9172 fails, and then only as fever stock at ≤ 25.
  - Selling RET/LAV page cards (t04's 26/27 bids vs our 100.4 values).
  - Packs.
  - Any board venue.

## Levers nobody is using yet
1. **Pairmaking onto v10.**
   - Evidence: of 102 team trades, v10 hosted only t10's (one positive, one negative). Where t15↔t07 swapped is not in the data.
   - Exploit: Lucas and Dani pick pairs from teams.md and multipliers.json, predict the value created, and pitch "settle it on v10".
   - Candidate pairs:
     - t08 (dumps LAV) → t09, t04 or t07.
     - t16 or t03 (dump MAL) → t15 or t02.
     - t07 (dumps SAL) → t09, t16 or t03.
   - Never a pair where the buyer's multiplier is below the seller's.
2. **Salamanca fever (game 9.15-11.15).** Pilar pays 25% over book: uncommon ≈ 31.25, rare 87.5, against team clearing of 24.5 and 74-80.
   - Pilar never offers more than she can still pay this hour, so the first sales take her cash.
   - SAL-07 from swap 9172 is our first fever sale.
3. **The unopened silver pack is our only free Chamberí pull.**
   - Sunday's grant is cash only. Saturday's pack, opened 5 ticks after RET's release, gave RET-05.
   - Keep it closed until Chamberí is released, then open it before the first CHA buy (pack drag).
4. **The Workshop, "Three spares".** Keep exactly 3 spares off the book: second copies of LAV-03, LAV-04 and SAL-02.
5. **A Chamberí uncommon as the page closer.** If the cap is 5×book, an uncommon closer scores up to 121 against 50 (see H6).

## Plan, anchored to the schedule
**Now (paused, tick 630)**
1. Operator: cancel 9101, 9136 and 9102 to keep the Workshop spares. Forgoes ≤ 0.4 board.
2. Operator: re-post 9172/9173 at tick 650 with doubled `expires_in_ticks`; Dani nudges t15 and t07 in the room. +18.1 neg ≈ +1.7 board.
3. Lucas and Dani: pitch 2 pairs for v10 with the predicted value. Up to +3.3 board.

**Resume (tick 631+)**

4. Operator: watch for Pícaros.
   - First deal alone in its window: offer-only, at ≥ our value, never at their opening price.
   - Read Δladder before a second deal.
   - Upside: three empty slots on the highest level.
5. Operator: Lucas's 12:58 plan A stands as written (Chato only at list 26, never higher).
6. Benches 7.0 / 9.0 / 11.0 / 13.0 / 14.65: stay on the stall, no action.
7. Game 9.15, operator: sell SAL-07 → Pilar, offer-only, steps of −2/−3, never jumping to her bid. It must beat our 0.019 L3 slot.
8. Game 11.65, Duels II (Aleks): give away the days the rival values more for price; at most 3 rounds.
9. All day: carry ≥ 184 cash into Sunday. Spend only on cash-neutral trades or the 13:15 bargain GUARDRAIL.

**Sunday**

10. 14.736, operator: fill the remaining round-2 Pícaros and ladder slots; pairmaking continues.
11. 16.65, Chamberí release (operator, Dani pitches the teams that dump CHA):
    - Open the silver pack.
    - Chato CHA rares at ≤ his ~86-90 finals (0 neg).
    - Maker bids to teams: rares ~80, uncommons ~25, commons ~9-10.
    - The last card from a team, per H6.
12. Round 3, if the ladder reset (operator):
    - 3 Abuela CHA commons below her list.
    - Chato sales above his opening bid.
    - Pilar sales in small steps.
    - Pícaros deals.
13. Round 3, early: the first coached positive v10 trade (if value created resets, see H2).
14. 18.65, Duels III (Aleks): fast closes, at most 3 rounds.
15. Before 20.736: cash → 0 into buys that score ≥ 0.
16. Judges (40%, Lucas and Dani): pitch the measured model (GAME.md, predicted vs measured); rehearse during Duels II.

## Hypotheses to test
1. **Value created = (buyer m − seller m) × the buyer's value, including the page bonus.**
   - Experiment: the first coached v10 trade.
   - Metric: predicted vs measured Δ`mm_points`.
2. **Value created resets at round 3.** Metric: `mm_points` right after the 16.65 round event.
3. **Pícaros unlock with 3 Pilar deals, and L4 weighs more than L3.**
   - Experiment: read our unlock at activation; make one deal.
   - Metric: Δladder vs the +0.050 of our best L3 deal.
4. **A fever SAL sale at ~31 beats the 0.019 L3 slot.** Metric: Δladder on the SAL-07 sale.
5. **The ladder resets at round 3.** Metric: `ladder_points` at the round event.
6. **The cap is flat 50 vs 5×book.**
   - Experiment: close Chamberí with an uncommon if a team ask for it is live; otherwise close with a common.
   - Metric: Δneg = 50 means flat; ≈ 121 means 5×book.
   - Downside if flat: ≈ −8.5 neg (57 vs 65.5).
   - Upside if 5×book: ≈ +62.
