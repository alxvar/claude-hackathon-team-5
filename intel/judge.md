# Judge (claude-opus-5-5, Sat 12:25)

## Verdict
Holding the pack, losing to the leader. We are #5 at 26.4 (+3.7 over 15 min, −1.7 over 60 min). Team 12 is at 32.2 (+6.8 over 60 min), so the gap to #1 is now 5.8. Team 18 (#4) is only 0.2 ahead, and #6-#7 are within 1.0 behind us.

## Our strategies: keep / kill / scale
- **Pilar sells, offer-only (dealer bot): KEEP.**
  - Thread 710: her 16 → 17 → 18 against our 30 → 19.
  - A close at ≥ 18 is at or above our value of 17.5, so it costs 0 neg.
  - Precedent: the LAT-08 sale to Chato moved the ladder +0.017 with neg unchanged.
  - Offer 7508 expires at tick 511. If she finals at 18, offer 18.
- **Chato buys above his list: KILL (keep dead).**
  - 6 deals never moved the ladder and cost −10.0, −9.0, −2.5 and −2.3 neg.
- **Abuela below-list buys: DONE.**
  - 4 deals moved L1 (+0.014, +0.018, +0.016, +0.003), and the best 3 are filled.
  - More only if a deal beats those shares.
- **Page-closer buys from teams: SCALE on Sunday.**
  - RET-01 at 20 scored +50 (cap); LAV-05 scored +50 on Friday.
  - The LAV and RET pages are both complete. The next one is CHA.
- **Trading loop: stays stopped through Duels I.**
  - Its log shows no fills or accepts, only open/close and Friday errors.
  - No evidence that it adds anything.
- **Maker book (11 offers): KEEP, small, needs a fix.**
  - Only 2 team trades since round 2: SAL-01 +4.7 at tick 351 and MAL-03 +2.0 at tick 404. Nothing since tick 404.
  - The field is slow too: one team trade since tick 433.
  - 11 offers live against the plan's 20-30.
  - Feeding issue: see change 2.
- **Venue v10: KEEP the stall, collector-buys only.**
  - `mm_points` is −5.2 after the SAL-07 trade from t10 to t15.
  - The builder logs value_created 9.0, which is still unexplained (desk question).
- **Unopened sobre_plata (86.8): FIX.**
  - It breaks "open packs before trading" (drag of ~1-4 per trade [L]).
  - Open it after Duels I, alone in its window, and log the before/after of `/api/me`.
- **Duels:** duel score 4.37 after 47 finished, 1 no_deal visible. No baseline in the data to judge against.

## Check the scout
**Holds:**
- Pilar opens to everyone at tick 502 and opens her bids at 16.
- Her uncommon sell median is 18 over 3 deals.
- MAL-07 and SAL-08 values (17.5 and 22.5). Offer 7238 (SAL-08 to t03 at 25) exists.
- We are level 3. `mm_points` is −5.2.
- The rival notes hold: Team 12 +5.8, Team 17 SAL-09 at 75, t15's buys, t13's MAL×6/SAL×2.

**Fails:**
- "Offer 7376 MAL-07 at 30 open": stale. The live offer is 7508 at 19, and thread 710 is already mid-negotiation.
- "RET page-completion path is [Open]": false. We hold RET-01 to 10, and the tick 276 +50.0 was the page close.
- "Team 2 bids 59 for RET-10 (7262), plus a RET-02 bid": not in the metrics.
  - GAME.md has 59 from Team 15 and 9-12 from Team 2.
  - The only RET bids now are t13 at 2 (RET-01 to 05) and t04's RET-06 at 16.
- "Team 12 collects RET": its team buys are LAT×3, MAL×2, LAV×1, none RET. The RET part rests on bids only.
- "Team 14 took RET-08 from t13 at 20 (tick 370)": not in the data.

## The 3 changes with the highest expected gain
1. **Finish the L3 trio today: MAL-07 now, then MAL-06, then SAL-08.**
   - SAL-08 at ≥ 23, during Pilar's fever (~16:00-18:00). Cancel 7238 first.
   - Run one thread at a time, offer-only. Close by offering her standing bid once it is ≥ our value.
   - Effect: up to 3 L3 deals at 0 neg. At the LAT-08 rate (+0.017) that is ≈ +0.56 board each, since +0.01 ladder ≈ +0.33 board.
   - L3 weighs more than L2, but the weight is [Open].
   - Risk: sells to Pilar may not count (n=1 on Chato). Read Δladder after MAL-07 and stop if it is 0.
2. **Fix the feeding breach in the book.**
   - At 26.4, only t07 (14.9) is ≥ 10 below us. The other addressees are not: t09 21.9, t15 21.1, t06 18.9, t16 18.7, t03 17.2.
   - Our gain per fill is ≤ ~5 neg (≈ 0.5 board). A page close for the buyer is up to +50 neg (≈ 4.7 board), enough to pass us.
   - Keep the t07 offers (LAV-03/04). Let the others expire, or re-post them at the §4A page price (35-45), so that they fill only as closers that pay us.
   - Risk: we lose ~0.3 board per small fill forgone. Page gaps are not in the data.
3. **After Duels I, fill the 2 empty L2 slots before round 3.** The ladder reset at round 2 [V], so unused Saturday slots are lost.
   - Use the 11:42 protocol: SAL-06 or SAL-07 from Chato, open 24 → 26, accept ≤ 26, walk on a final above 26.
   - Effect: −3.5 neg (≈ −0.33 board) for ≈ +0.56 board of ladder.
   - Risk: his uncommon finals today are 30-31, so we will likely walk.
   - Fallback: none at ≥ value on Saturday. On Sunday, CHA buys at or below his list (worth 112 / 40 to us) cost 0.
