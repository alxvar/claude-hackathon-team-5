# Judge (claude-opus-5-5, Sat 16:51)

## Verdict
Gaining. We are #1 at 30.02 (+1.6 in 15 min, +2.1 in 60 min), but the lead is thin: Team 14 is 0.2 behind (29.8, −0.5/60 min). Team 1 (+3.8/60) and Team 3 (+7.2/60, now 2.2 below us) are climbing fastest.

## Our strategies: keep / kill / scale
- **Pícaros flags: KEEP, narrowed.** `neg_points` went 43.2 → 73.2 from three correct flags, then −10 to 63.2 from the "church bell" flag. Flag 5, sent on a closed thread, has scored 0 so far. Flag only messages on a live thread.
- **Pícaros L4 buys: SCALE.** SAL-09 at 54 moved the ladder 0.200 → 0.270 with 0 neg. The SAL-10 thread walked when their 60-FINAL met our cap of 56. Their 60 is below our value of 63, so it was a missed slot.
- **Pícaros common sell threads: KEEP as flag vehicles only.** SAL-05 sits at our ask 20 vs their bid 4; Taxi Blanco and Tienda de Discos both closed with no deal. No neg cost so far.
- **Cheap common buys from teams: KEEP, but not from the top 5.** MAL-03 (+2.0) and MAL-01 (+2.0) were clean. MAL-08 came from t14 (+2.5 for us); t14's gain is not in the data, so the 15:55 "≥ 3× theirs" rule cannot be confirmed.
- **Maker asks addressed to t03/t16/t09: HOLD the low-risk ones; recheck t03 and t16.**
  - The 5 asks gain about 2-3 each.
  - SAL-01 to t03 at 7 measured +4.7.
  - t03 is now 2.2 below us and t16 is 3.6 below, both inside the 15:55 page-closer gap of 6.
- **Trading loop: KEEP.** Its only action since 15:29 was a swap accept (SAL-04 → RET-04), expected +6.2. Measured +6.2 at tick 669, but that window also includes a Pilar sale.
- **Duels: no change needed.** 68 finished, duel score 13.93. Aleks owns this, not us.

## Check the scout
- **Holds:**
  - The flag sequence (43.2 → 73.2 → 63.2) matches the metrics.
  - Flag 5 on a closed thread scoring 0 matches.
  - Team 14 is 0.2 behind.
  - Team 1 is +3.8/60 min.
  - Team 14 bought RET-04 from t06 at 5.
  - Teams 8, 9, 10 and 16 unlocked L4 at tick 761.
- **Stale:**
  - The SAL-10 status "73 → 73 vs our 44" is old. The log shows 73 → 67 → 63 → 60-FINAL vs our 56.
  - The "floor 70" is also outdated: the Chief set 60 for this buy (log 16:46).
- **Wrong:**
  - **RET-04 is not a spare.** We hold one copy at 83.9, and it is a RET page card. Selling it breaks the page. Strike it from the sell table.
  - **LAT-04 is not a spare either.** We hold one copy at 5, not 1.2; the spare went into the Workshop.
  - **LAV-02 is worth 1.3 per copy, not 3.2.**
  - **Team 7's 9.5 price is a tick-631 estimate**, not a live bid. Team 7's current standing is not in the data.
  - **Team 16 did not buy LAT-09.** It sold it to t03 at 88; Team 3 is the buyer.
  - **"t06 has 68 on SAL-09" is a settled trade** (t15 → t06), not a live bid.

## The 3 changes with the highest expected gain
1. **Retry SAL-10 at ≤ 60 (their last final). Open 44, step +3, offer-only, structure exactly card:SAL-10 for cash.**
   - First, the Chief writes the floor-60 change as a GUARDRAIL line; `directives.md` still says 70.
   - Effect: about +1.4 board per the directive [L], and 0 neg because 60 ≤ 63.
   - Risk: Pícaros open to everyone around 17:33, so the price may drift up. Never exceed 63.
2. **Take the third L4 slot by selling a spare LAV-02 (3rd copy, worth 1.3) to Pícaros.** Open high, step −2/−3, offer-only, floor = value.
   - Their common bids are 4, which is still above our 1.3, so any deal costs 0 neg.
   - A sale above the dealer's opening bid moved the ladder at Chato (+0.017).
   - The same thread is a live flag vehicle, as the 16:39 directive asks.
   - Risk: the ladder share from a low-range deal is small (not in the data). The Pícaros deals-per-hour limit is not in the data.
3. **Protect the lead.**
   - No sales of RET or LAV page cards: the book must never list single copies.
   - Pull the asks to t03 (LAV-04, LAT-03) unless `tools/policy.py can-give` passes with t03's current gap.
   - No buys from t14, t12, t1 or t10 (the top 5).
   - Effect: avoids handing a +50 page closer to a team 2-4 points behind us.
   - Risk: we give up about +2-3 per sale.
