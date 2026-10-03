# Judge (claude-opus-5-5, Sat 17:40)

## Verdict
Holding #2 and losing ground to the leader. We are 29.4 (+0.0 over 15 min, +0.8 over 60 min). Team 14 is 30.9 (+0.6 / +1.0), so the gap is 1.5 and widening. Team 1 is 29.2, only 0.2 behind, and gained +0.4 in 15 min. Our `neg_points` have been flat at 63.2 since tick 774.

## Our strategies: keep / kill / scale
- **Ladder deals (Pícaros L4, Pilar L3): SCALE.** Ladder went 0.200 → 0.394 since 16:43 at 0 neg: SAL-09 +0.070, MAL-09 +0.021. This is our only climbing lever right now.
- **MAL-08 → Chato job (thread 1278): KILL.** His uncommon buy final is 14 [V] (15-16 only with an open ≥ 39 and −2/−3 steps). Our floor is 18 and we step −1, which he mirrors. It will walk, and it holds a dealer slot until 18:06.
- **Flag probe ≥ 17:42: KEEP, as a bounded probe.** Results so far: +30 (n=3), −10 (n=1), then three 0s at 16:53. Stop at the first 0 or −10.
- **Maker book (6 offers): KEEP, but it is near-idle.**
  - No team fill since tick 760 (MAL-08 buy, +2.5).
  - MAL-02/05 to t15 at 9 are undercut by El Rastro asks at 7-8.
  - Gains are ≤ +2 each. Let them expire at tick 896; don't reprice.
- **Trading loop: KEEP, running.** Its last accept was 15:48 (swap, +6.2), nothing since. It costs nothing.
- **SAL rares → Pilar fever (job b1iw7l644, accept ≥ 85): KEEP, but add a fallback** (change #2 below).
- **v10 room plan (Dani): KEEP, per Lucas 17:40.** No current `mm_points` reading is in the data. The last measured v10 trade went +4.99 → −5.2.

## Check the scout
- Holds: the fever window 18:04-20:04; Pilar rare median 56 (n=1); the flag tallies (53.2, 63.2, 73.2, then −10); the t14/t03/t01 rival warnings.
- Wrong direction on Pícaros: "picaros uncommon (team sells) 12" means Pícaros buys at 12. "73 → 54-56" was Pícaros selling to us.
- Wrong ladder history: 0.394 came from MAL-09 → Pilar (0.373 → 0.394), not from the Pícaros deals.
- Wrong direction on MAL-08: we bought it from t14 (t14→t05 at 15) and scored +2.5. We did not sell to t14.
- Wrong on Team 6: t06 sold MAL-08 (t06→t09); it did not buy it.
- Unmeasured: "fever ~85, cash +170". The 85 is [L] from the directive. At the normal 65-70 the cash is +130-140.
- Stale: "Team 7 is #17, safe". That comes from the 15:30 profile; recheck rank before any sale to t07.
- Rolling-hour flag cap: a hypothesis only. A count cap (~3 per team) fits the data equally well.

## The 3 changes with the highest expected gain
1. **Cancel the MAL-08 Chato thread and move MAL-08 to Pilar before 18:06.**
   - How: offer-only, ask ~30, steps of −2/−3, floor 18 (value 17.5). Pilar's uncommon buy median is 18 over 6 deals.
   - Effect: 0 neg. It can replace our weakest L3 slot (≈0.019-0.021) with up to ~0.040; the small-step MAL-06 sale did that [V, n=1].
   - Risk: Pilar's 6 deals per hour cap and a thread collision with the 18:06 fever job. It must finish or walk by 18:04.
2. **Give the fever job a fallback.**
   - How: if Pilar walks at ≥ 85, retry each SAL rare at a floor of 63 (our value) with −2 steps. Never jump to her bid: the jump gave SAL-08 +0.019, against +0.040 for small steps.
   - Effect: 0 neg in every case. Cash +126-170 for Sunday's CHA page, plus a possible L3 slot upgrade.
   - Risk: the fever price is unmeasured. A rigid ≥ 85 floor could strand both rares at 19:50.
3. **Before each v10 room trade (Market Test ~17:55), Dani confirms in person that the buyer does not already hold the card.**
   - Why: a 2nd copy makes value created negative. This is what happened at tick 398 (−5.2, rank #3 → #7) and is why SAL-10 → t08 was barred.
   - Effect: Lucas's ≈ +3 board [L] instead of a possible drop.
   - Risk: no API shows other teams' albums, so we rely on teams' own word. Skip any trade where the buyer is unsure.
