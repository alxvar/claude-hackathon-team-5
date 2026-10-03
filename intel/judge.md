# Judge (claude-opus-5-5, Sat 12:08)

## Verdict
**Falling behind.** We are #7 at 23.6: −5.3 over 60 min while #1 Team 12 gained +5.7 (now 32.2, 8.6 ahead). neg_points has been flat at 35.2 for 15 min, ladder 0.055, mm_points −5.2.

## Our strategies: keep / kill / scale
- **Dealer bot, Chato ladder sells (offer-only): keep, but get a measurement.**
  - MAL-07 walked at his FINAL 14. That was correct: 14 − 17.5 = −3.5, over the ≤3 loss limit.
  - The LAT-08 thread is live (ask 30 → 27, floor 14). Two tests and still no Δladder reading.
- **loop.py: keep stopped until Duels I ends.**
  - Its log has no Saturday fills (last entries 10:31-10:32 open/closed). The only measured fill today was a public bid (MAL-03 at 5, +2.0).
- **book.py maker asks: keep, but fix addressing.**
  - Two fills today (SAL-01 +4.7, MAL-03 +2.0). None in the ~70 ticks since tick 404.
  - Only 11 live offers vs the plan's 20-30.
  - LAV-02 is addressed to t09, which sits 0.6 below us and rising +8.2/h. That breaks the feeding rule.
- **RET/LAV pages: done.** All 10 cards of each are held, and RET-01 scored the +50 cap. Hold the rares: t02 bids 53 for RET-10, which is worth 149.9 to us.
- **In-room trades (Dani): no evidence in the logs today.** No sale or buy is attributed to the room since tick 276.
- **Venue/stall: keep the stall.**
  - Bench 5.0 efficiency was 0.933.
  - The venue detail shows value_created 9.0, but mm_points is −5.2. That gap is unexplained; the desk question is right.

## Check the scout
- **Holds:**
  - LAT-08 at 14 costs 0 neg_points (value 12.5; dealer gains clip to 0).
  - SAL-01 +4.7 and MAL-03 +2.0 were clean.
  - Selling RET-10 at 53 would lose ~97.
  - t09 is +8.2/h and t17 is +7.6/h.
- **Does not hold:**
  - "Keep the six asks live" misses that LAV-02 → t09 now feeds a team right below us that collects LAV.
  - "14 is his buy list, so it counts as at list": Chato's Saturday buy list is not in the data. Friday's was 13, and 13 is also his opening, which never counts.
  - "Team 12's dealer count is 37": 37 is total deals. teams.md shows 12 team / 23 dealer.
  - "Collector sales protect venue value": our asks are on El Rastro (forced at 11:37), so they don't touch v10's value created.

## The 3 changes with the highest expected gain
1. **Epic hunt in the room (Lucas/Dani), under the 11:17 GUARDRAIL.**
   - Target: RET-11 (198 to us), RET-12 (495) or LAV-11 (~234), from a team outside the top 4, off top-4 venues.
   - Limits: price + fee ≤ 80 (cash 109 → floor 20). Re-read /api/me/value and accept via trade.py only if the gain is ≥ 40.
   - Effect: up to +50 neg_points (cap [V]), the largest single move available.
   - Risk: no holder exists. No epic ask appears in the data.
2. **Finish the ladder test, then scale it.**
   - When Chato FINALs 14 on LAT-08, offer 14 so he accepts. Measure ladder_points alone in its window.
   - If it moves: next SAL-08 to Pilar from ~12:21, at ≥ 22.5 (her uncommon buy median was 18 over 2 sales; the set is not in the data). Never MAL-06/07 below 14.5.
   - Effect: +0.01 ladder ≈ +0.54 board [L]. Sales also lift cash toward the ≥170 Saturday close for Sunday's CHA page.
   - Risk: a sale near his opening may earn ~0 range share. Stop after one zero reading.
3. **Pull 6605 (LAV-02 → t09) now; re-address it to t07 at 6-7.**
   - t07 is #17, 13 below us, and collects LAV.
   - Before reposting the t15, t03, t06 and t16 asks, read their current scores: none appear in the top-10 metrics. Keep only those ≥ 10 below us.
   - Effect: protects against handing a climber a capped closer (+50 to them) for our +2.8.
   - Risk: t07 already holds our LAV-03/04 asks, so the extra ask may not fill.
