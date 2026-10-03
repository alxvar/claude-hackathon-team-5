# Judge (claude-opus-5-5, Sat 15:45)

## Verdict
**Holding, slipping on the chasers.** We are #5 at 27.92 (−0.2 over 15 and 60 min). The gap to #1 Team 14 (30.4) narrowed from 2.7 at 15:30 to 2.48. The gap to #4 Team 10 (29.1, +0.2) widened, and Team 18 (+0.5) passed us to #3. Team-trade `neg_points` have not moved since tick 404, about 250 ticks ago.

## Our strategies: keep / kill / scale
- **L3 ladder via Pilar: KILL further round trips.**
  - Ladder went 0.181 → 0.188 (+0.007, ≈ +0.23 board). The SAL-06 buy cost −2.7 neg (≈ −0.25 board).
  - Net ≈ 0, as the operator logged. The L3 best-3 is near saturation (+0.050 → +0.019 → +0.007).
- **Dealer buys to feed the ladder (Abuela SAL-06 at 23): KILL.** This is a buy-to-resell; the plan §7.8 forbids it. Pack drag made it −2.7 instead of −0.5.
- **Dealer bot mechanics (small steps, offer-only): KEEP.**
  - SAL-06: 34 → 32 → 30, her bids 22 → 23 → 25, closed at 25 with the dealer accepting.
  - Reuse this for Pícaros, on cards we already hold.
- **Trading loop: KEEP, contribution 0.** No fill or accept appears in its last 25 events today, only open/closed. It costs nothing.
- **Maker book (9 asks): REPRICE / RETARGET.**
  - 0 fills since tick 404; the last fills were +4.7 at tick 351 and +2.0 at tick 404.
  - Three asks may break the plan's feeding rule (page closers only to teams ≥ 10 below us): SAL-01 → t06 (3.9 below, collects SAL), LAV-03 → t04 (4.7 below, collects LAV), LAV-04 → t03 (7.4 below, collects LAV).
- **Swap 9389 (LAV-02 → t07 for MAL-01): likely dead.** t07 sold MAL-01 to t04 at tick 640. Whether t07 still holds a copy is not in the data.
- **Swap 9387 (→ t15 for SAL-07): KEEP if the `want` field reads SAL-07.** The metrics render it as "for 0". If SAL-07 is missing, it is a gift: cancel it.
- **In-room trades (Dani): SCALE.** None are logged since the morning, and the room is the only path to a +50 trade.

## Check the scout
- **Holds:**
  - Team 4 is racing RET: RET-07 at 25, RET-08 at 27, RET-06 at 26 (ticks 636-656).
  - The risers are t18 +0.5 and t10 +0.2; t15 +1.2 per the profiles.
  - t17 is 2.4 below us.
  - The −2.7 neg came from the SAL-06 dealer buy.
  - LAT-09's 80 bid is not ours to fill.
  - +0.01 ladder ≈ +0.33 board.
- **Wrong: "SAL-07 holder not in the data."** GAME.md records t10 → t15 SAL-07 at tick 398. Whether t15 still holds it is not in the data.
- **Unsupported: "Team 7 buying at ~9.5."** That is the profile's estimate. t07 has no open bid in El Rastro's top bids.
- **Debatable: "RET-04 at 40 → t15 is stale."**
  - 40 is the plan's page-closer price (35-45), not a clearing-price mistake.
  - The real problem is that t15 (6.4 below us) fails the feeding rule if RET-04 is its closer.
- **Pícaros "neg 0, ladder gain unknown": holds.** Its unlock rule and prices are not in the data.

## The 3 changes with the highest expected gain
1. **MAL-09 (worth 49 to us) → Team 17 as an addressed maker ask at ≥ 99. Chief's call: this overrides its Pícaros hold and the plan's feeding rule (t17 is only 2.4 below us).**
   - Our gain is capped at +50 neg ≈ +4.7 board (0.094 per neg_point), enough to pass t14.
   - No measured ladder deal comes close (the best was +0.050 ≈ +1.65 board).
   - t17 bid 70-85 at 15:36; it is not in the current top bids, so confirm it in the room via Dani first.
   - Risk: if the card is t17's closer, its gain is (its value − 99). That exceeds ours only if its value is > 149, which is not in the data. If Dani reads t17 as much higher, raise the ask.
2. **Retarget the spares to Team 7 (#17, 10.3 below us, collects RET/LAV/LAT) at ~9 each, as maker. Dani points them at the live offers.**
   - Cards: LAV-02, LAV-03, LAV-04 2nd copies and RET-04 2nd copy (worth 2.8-3.2 each).
   - Cancel 9389 and the feeding-rule-risk asks (to t06, t04, t03) first.
   - Expected about +5-6 neg each, about +22 total (≈ +2 board).
   - Risk: t07 shows no live bids, so fills may not come.
3. **Pícaros (L4) only with cards already held, no dealer buys.**
   - Sell at ≥ our value with small steps and offer-only: SAL-03/05 (9), MAL-02/03 (7), LAT-03 (5), the 2nd copies.
   - Expected: a fresh level's best-3, ladder size not in the data, 0 neg cost.
   - Risk: an unknown unlock rule, and a Pícaros sale competing with change 2 for the same spares. Team sales come first, since they add `neg_points` and dealer sales never do.
