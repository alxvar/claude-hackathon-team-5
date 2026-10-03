# Judge (claude-opus-5-5, Sat 19:01)

## Verdict
Holding, not gaining: #3 at 31.68, 0.12 behind Team 14 (31.8). Our +1.7 over 60 min beats Team 14 (+0.3) and Team 6 (+0.9), but we are −0.3 in the last 15 min (idle drift since #1 at 31.97 at 18:30). Team 10 is level with us at 31.7 after +3.3 in 15 min.

## Our strategies: keep / kill / scale
- **Bargains daemon plus taker accepts by hand: SCALE.** The SAL-06 ask at 28 scored +40.4 neg, worth +1.99 board. It is our only large win since 17:45.
- **Ladder sells, job bxpdvaqj5 (MAL-08 → Pilar, LAT-04 / LAV-04 → Pícaros): CUT TO ONE TEST.**
  - /api/me still reads ladder 0.437, so the "fell below its cap" premise is not shown.
  - At 17:45, three ladder deals moved ladder 0.373 → 0.437 and left `negotiating` flat.
  - The Pícaros LAT-04 thread shows her bid at 4 against our 12, for a card worth 5 to us.
- **Trading loop: KEEP.** The last fill was the t07 swap at 17:46 (+15.5 measured). Since then: no errors and no fills.
- **Maker asks to t09 and t15 (MAL at 9, LAV-03 at 6): KEEP.** Each is +2 to +2.8 if filled, with no fee for us. None has filled; 15458 has been live since about tick 1000 at least.
- **Offer 15667 (LAV-02 at 0 to t01): KILL, do not repost.**
  - It loses 1.3.
  - t01 collects LAV and sits only 7.6 below us, so it fails the ≥10 feeding rule.
  - t01 is allied with t10, which is level with us.
- **v10 value-created pushes (ad job, Dani): KEEP, but no measured effect.**
  - Since 17:40 the trade list shows no settlement on v10.
  - The t03 → t09 LAV deal never appeared.
  - t15 posted one sale, with 0 settlements.
- **Unopened silver pack: COSTING US.** Pack drag took the SAL close from the +50 cap to +40.4. The pack fell 87.1 → 76.5 since 18:20.

## Check the scout
- **Holds:**
  - Team 10 is the fastest climber (+3.3 / +3.9). Its MAL-10 at 74 (tick 585) and RET-03 at 12 (tick 1033) are confirmed.
  - Team 16 bought t15's RET cards at ticks 1022-1023.
  - The earlier Pilar sells scored +0.050 and +0.040.
  - We have 3 complete pages.
  - Skipping LAV-05 at 5 is correct: a duplicate is worth 3.25 to us, less than 5 + fee.
- **Does not hold:**
  - "Ladder 0.437, dropped 0.28": the ladder reads 0.437, unchanged. The 0.28 is a board drop, not ladder release, and its source is not in the data.
  - "Board effect low": stronger than that. It measured 0 on three deals at 17:45.
- **Stale:** "v10 7.5 vs 9.15-12.5" is the 17:50 figure. No current `mm` figure exists in the metrics.
- **Wrong:**
  - "MAL needs only MAL-09/10": we also lack MAL-06 and MAL-07 (both sold to Pilar). MAL is 4 cards from a page.
  - "LAT-02 at 8" is no bargain: our value is 5, and 8 + fee 2 nets −5.

## The 3 changes with the highest expected gain
1. **Duels II (about 20:33): verify the day reading live.**
   - Action: Aleks runs `--days-read auto`, checks the first 2-3 settled `days` duels against predicted surplus, and flips the switch if they read backwards.
   - Expected gain: the Duel Lab puts it at +0.47/duel if right vs −0.18/duel if backwards, over 68 duels. This is the largest swing left on Saturday.
   - Main risk: too few early duels to tell the two readings apart.
2. **Ladder: one measured MAL-08 sale, then decide.**
   - Action: sell only MAL-08 to Pilar (floor 18 ≥ its value of 17.5). Read `negotiating` at the next refresh, about 10 ticks later.
   - If it is flat, stop job bxpdvaqj5 (LAT-04 and LAV-04 included) and cancel 15762.
   - Expected gain: 0 to a small ladder move, and it saves Operator attention and accepts before Duels II.
   - Main risk: we lose a small gain if the cap really did reset.
3. **Decide the silver pack before any further card buy (Chief, before Sunday's CHA purchases).**
   - Every acquisition we make while it stays unopened loses value to pack drag (≈9.6 on SAL-06).
   - Weigh that drag against pulling CHA cards on Sunday by opening it after the release.
   - Expected gain: the avoided drag on each CHA buy. The size of a CHA pull is not in the data.
   - Main risk: opening before the CHA release forfeits any CHA pull.
