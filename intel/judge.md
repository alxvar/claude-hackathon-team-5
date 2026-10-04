# Judge (claude-opus-5-5, Sun 14:50)

## Verdict
**Holding #1, but the lead is shrinking.** At 13:12 we led t10 37.21 to 34.77, a gap of 2.44. At 14:48 it is 37.7 to 35.8, a gap of 1.9. Over the last 60 min t10 gained +0.9 and we gained +0.5. Over the last 15 min t10 gained +0.5 and we lost 0.1. t12 (34.5) and t03 (34.2) are flat. `neg_points` have stayed at 104.8 since tick 2318.

## Our strategies: keep / kill / scale
- **Dealer bot:** finished. The stalls closed at 14:01 and the ladder is final at 0.364 (Chato L2 never filled). Nothing to run.
- **Trading loop (floor 0, El Rastro, rivals excluded):** keep it running until 15:00. It is harmless: its last fill was the t07 swap on Saturday (+15.5) and it has made no Sunday fills.
- **Our bids and listings:** we have 0 offers live.
  - CHA-11 at 190 scored +50 at tick 2318, the best trade of the day.
  - The LAT-06/07/08 bids at 14 expired unfilled.
  - The MAL-09 chain is dead. Six addressed bids (60, then 75, to t01/t09/t15) lapsed with no counter, so MAL stays at 9/10.
- **In-room trades:** these produced the only Sunday gains: CHA-05 +50, CHA-11 +50, MAL-07 +2.6. Scale them for the last 12 minutes (see change 1).
- **Duelist (Grand Final wave):** untouched per the 13:12 guardrail. Duel points read 35.84 with 0 live.

## Check the scout
- **Holds:** the 0 open offers, dealers closed, and neg at 104.8.
- **Holds:** no lever is left in the El Rastro asks. LAT-01/05 at 8 are first copies worth 5 to us, and LAT-07/08 at 19 are worth 12.5. A buy at either price is a loss.
- **Holds:** every page is complete except MAL, with only MAL-09 missing.
- **Holds:** t10 is climbing on epic trades (RET-11 at 216 at tick 2757).
- **Wrong:** the scout says rivals are "+0.0 over 15 min" and puts t10 at 35.2. The metrics show t10 at 35.8 and +0.5 in 15 min, so the threat is understated.
- **Stale:** the scout puts t03's SAL-11 bid at 215 (29255). The live bid is 216 (29308). t09 is +2.2 over 60 min, not +1.7.
- **MAL-09 maths is muddled:**
  - The scout calls MAL-09's rarity "not in the data", then values it as a common.
  - The data says MAL-09 is a rare. Card 09 is a rare in every set (LAV-09, RET-09, SAL-09), and the Pícaros and Pilar priced MAL-09 at 56-73.
  - So its value as our last MAL card is about 49 + 46.4 ≈ 95. A bid at 45 or less would score +50 (Lucas's 12:50 figure).
- **Unrealistic:** the scout suggests a ≤ 49 bid now. The same holders already ignored 60 and 75, so a 49 bid will almost certainly not fill.

## The 3 changes with the highest expected gain
1. **Close MAL-09 in the room, by 14:55.**
   - Lucas or Dani asks t01, t09 and t15 face to face to fill a fresh addressed El Rastro bid at 75. That is the Chief's 13:58 cap; do not exceed it. The operator posts the bid only for the team that says yes.
   - Expected gain: about +20 `neg_points` (95 − 75; we are the maker, so no fee). At Saturday's measured rate of about 0.05 board points per neg point, that is roughly +1 board point, half of t10's gap.
   - Risks:
     - The seller's gain cannot be quantified (not in the data). t09 is 6.9 below us and climbing, so check t09 is still ≥ 5 below us before it fills.
     - Never t10, t12, t03, t18 or t04.
2. **Freeze everything else (13:12 guardrail).**
   - No public bids at all. A public MAL-09 bid could be filled by t10, which holds a copy it bought at tick 967.
   - No sales of our cards: every El Rastro bid on them (CHA bids at 5-15) is far below our value.
   - Leave the trader on, rivals excluded.
   - Expected effect: protects the 1.9 lead. Risk: none beyond the opportunity cost.
3. **Judges (40% of the score): Dani confirms the `/submit` story is filed now.**
   - Use the tick-2516 call for "built something outside the Bazaar" (the market recorder, the opportunities desk, the measured-facts table).
   - Its deadline and weight are not in the data, so do it before 15:00.
   - Expected effect: it is the largest score component still open.
   - Risk: a rushed text. Reuse `docs/demo.md` and GAME.md's [V] facts rather than writing anything new.
