# Judge (claude-opus-5-5, Sat 16:18)

## Verdict
**Gaining slowly, still #5.** We are at 28.6 (+0.5 over 60 min). Team 14 is at 30.1 (−0.6). The gap to #1 has narrowed from 1.94 (snapshot 680) to 1.5. We are still 0.5 behind Team 10, and Team 1 is climbing from below (+1.5/60 min, 2.2 under us).

## Our strategies: keep / kill / scale
- **Dealer ladder sells at or above our value: SCALE.**
  - LAT-08 → Chato at 14 moved ladder 0.188 → 0.200 at neg 0.
  - Pilar sales: MAL-07 +0.050, MAL-06 +0.040, SAL-08 +0.019, SAL-06 +0.007.
  - The ladder at 0.200 refutes the Analyst's "cap ≈ 0.15".
- **Dealer buy-to-resell (Abuela SAL-06 at 23 → Pilar at 25): KILL outside the fever.**
  - The buy cost −2.7 neg (pack drag), about −0.25 board.
  - The resale added +0.007 ladder, about +0.23 board, so the round trip is roughly 0.
- **Trading loop (`loop.py`): KEEP.**
  - Its only accept today, the t08 swap SAL-04→RET-04, measured +6.2, equal to its prediction.
  - No accepts since the 16:10 restart.
  - The policy guard caught the t10 MAL-09 trap.
- **Public bids on v07: KEEP, small.**
  - MAL-01 at 5 filled for +2.0 measured.
  - SAL-07 20, MAL-08 15 and LAT-02 3 are live to tick 772.
  - Each is only 2-2.5 under our value, and pack drag (−2.4 on SAL-06) can wipe that out.
- **Maker asks (7 live, addressed to t15/t16/t03/t09): KEEP, but KILL 10377 now.**
  - 10377 sells SAL-01 at 6. Since the Workshop it is our last copy, worth 9, and `can-give` says NO: −3 if it fills.
  - 10653 (SAL-02 at 11, also a last copy) has not been through `can-give`.
  - No fills on any ask; fill time is not in the data.
- **Workshop: KEEP.** It added +11.8 collection value and is not a scored deal. Repeat it whenever three same-rarity spares pile up.
- **Duels: KEEP.** 68 finished; 9 of the last 10 closed as deals; duel score 13.93.

## Check the scout
- **Holds:**
  - `can-give`: LAV-02 YES; LAV-03/04 and RET-04 NO.
  - Ladder is 0.2 with the 2nd L2 slot filled.
  - Team 1, Team 6 and Team 17 are climbing; Team 14 is falling (−0.2/−0.6).
  - Live bids: t06 68 for SAL-09, t04 65 for RET-10.
  - Team 13 bids 2 P on RET-01..05.
  - Team 10 is barred from MAL-09.
- **Wrong or stale:**
  - "t03 bids 88 for LAT-09 (offer 10700)": that bid already filled (t16→t03 at 88, tick 724). The "ask at 135" is not in the data.
  - "+4.3 per spare to t07": as maker we pay no fee, so the gain is about +6.3 at 9.5. The 9.5 price is an estimate; t07 paid 10 for RET-05 at tick 712.
  - Dani's table predates the Workshop: LAT-04 and SAL-01/02 are single copies now, not spares.
  - "+0.02 to +0.04 per good L3 deal" is overstated. L3 already holds 4 deals and only the best 3 count, so a new deal adds only its excess over the 3rd slot (+0.019).
  - "Team 2 pays 84 for RET-09" is from tick 504 and is not evidence that RET rare demand is "rising".

## The 3 changes with the highest expected gain
1. **MAL-06 → Pilar now, then SAL-08 in the fever (18:03-20:03).**
   - How: `abuela_bot.py --dealer pilar`, ask from ~30 in −2/−3 steps, offer-only close, alone in its window. MAL-06 floor ≥ 19.
   - SAL-08 only if the price is ≥ 22.5. The Chief must first take it off `run/reserved.json`.
   - Effect: replacing the +0.019 slot with a MAL-06-style +0.040 is about +0.021 ladder, roughly +0.7 board (at +0.01 ≈ +0.33). A fever SAL sale adds only if it beats +0.040.
   - Risk: whether the fever lifts Pilar's price range (and so our share) is not in the data. Pilar allows 6 deals per team per hour.
2. **Duels II, ≈ 20:33: adopt Duel Lab #1 (concede 15% of the gap per step, cap 18%).**
   - Effect: +1.8 to +3.9 duel points over 68 duels (modelled). Converting duel points to board is not in the data.
   - Risk: the model's out-of-sample miss. Aleks decides; the Builder codes it by 19:30.
3. **Clean the maker book and sell the true spare.**
   - Cancel 10377 (saves −3 neg).
   - Run `can-give SAL-02` before 10653 can fill.
   - Post LAV-02 at 10, addressed to t07 (#17, 11 below us; passes the gap-6 rule).
   - Effect: about +6.8 neg, roughly +0.6 board, if it fills.
   - Risk: it may close t07's LAV page (up to +4.7 board for them). That still leaves t07 far below us, so it is allowed.
