# Judge (claude-opus-5-5, Sun 12:14)

## Verdict
**Gaining.** We are #2 at 33.9 (+1.7 over 60 min). t12 leads at 34.6 (−0.3), 0.7 ahead. t10 (33.3) and t18 (33.2) are 0.6-0.7 behind. t03 is the fastest climber: 31.9, +1.4 in 15 min. neg_points is flat at 50.0, the round cap, so recent gains come from duels, market and relative movement. Only v10 is measured: market 10.03 → 10.87. The rest of the attribution is not in the data.

## Our strategies: keep / kill / scale
- **Trading loop: KILL (already stopped).** The cap makes extra team-trade gains worth 0. The loop's last accept was Sat 17:46, and nothing since.
- **Dealer bot / pack_route: KEEP, minimal.**
  - LAV-08 → Pilar at 17: ladder 0.342 → 0.364.
  - LAT-05 → Pícaros at 5 (worth 5): neg and ladder both unchanged, so it was a wasted slot.
  - The ladder looks flat on the board [L, Chief Sat 17:45], so no extra effort here.
- **lat_fodder bids (LAT-06/07/08 at 9): KEEP, expect nothing.** El Rastro shows no LAT-06/07/08 asks, so the bids are unlikely to fill. Only Chato's L2 slots remain, and his 12:01 thread said "sold out".
- **MAL-09 bid 24703 (49, to t13): KEEP.** It pays bounty #1 at value (0 over), per Lucas's 11:25 GUARDRAIL and the Chief's 12:03 decision. It does not close MAL, because MAL-07 is still missing.
- **The 13:30 Pícaros MAL-09 attempt (cap 49 = value): expected 0 np.** It is harmless only if the trick guard holds.
- **v10 bounty: KEEP, and measure it.**
  - Two settlements so far: mm_points +0.9 and market +0.84.
  - Bounty #2, LAT-01 at 20 against a value of 5 (24785), is a team buy at −15 by the formula.
  - Whether the round cap absorbs that loss is not in the data. Log neg_points before and after the fill.

## Check the scout
- **"Cancel 24703": wrong.** The Chief kept it as the bounty payment, and "neg_points stay at 0" is false (they are 50.0).
- **"Run lat_fodder for the L3 slot": stale.** Ladder is 0.364, not 0.342, and Pilar's 3rd L3 slot is used. Bids 24252-54 have been replaced by 25107/25111/25112, which expire at tick 2307.
- **"Don't sell CHA": holds.** We hold no spares, and every CHA card is worth ≥ 122 to us. The bidders it cites (t07 at 8, t16 at 12) are not on the board; t09 bids 5 and 15.
- **Leaderboard: stale.** It has us behind t18; we are #2, ahead of t10 and t18.
- **Climb rates: wrong.** The scout gives t04 +7.5, t09 +5.6 and t15 +6.2. Metrics show +4.5, +2.9 and +2.8.
- **t15 → t16 CHA rares at 65: holds** (ticks 2022 and 2065).
- **Missed threat: t03,** at +1.4 in 15 min. It is not flagged.

## The 3 changes with the highest expected gain
1. **Secure the 12:37 duelist restart and the Grand Final (≈ 14:15).**
   - Confirm one instance is running f57a002 with the Duel Lab params.
   - Run the first-wave check (directive 07:25 #10).
   - Duel points (24.68) are our only uncapped negotiating lever left.
   - Risk: two copies on one key, or a SWITCH line. Escape ladder: `use A` → POLICY=llm → `--rollback`.
2. **Use the last v10 bounty slot (≤ 14 P over value) on a non-rival pair.**
   - Dani points teams below us (not t12/t10/t18/t03) at existing v10 offers.
   - Keep the recorder and broker supervised through the 12:37 bench and any later Sunday benches.
   - Expected: ≈ +0.9 mm per settlement, as measured.
   - Risk: the fair-play review the Chief flagged, and the unknown np cost of an above-value bounty fill. Measure 24785 first and size the slot by the result.
3. **Freeze neg_points at 50.**
   - No deal above value at any dealer or team until close. A dealer loss counts in full and would erase cap headroom we cannot regain.
   - Move freed operator and human time to the judges' pitch (40%). Use today's measured table: the 50 cap, the round cap, flags +10/−10, the ladder's board effect, and bounty ROI.
   - Risk: none to the score. Whether the pitch is ready is not in the data.
