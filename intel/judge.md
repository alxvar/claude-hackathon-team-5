# Judge (claude-opus-5-5, Sat 20:55)

## Verdict
Falling behind the top 2 and holding #3. We are at 31.64 (−0.0 over 60 min) against t10 34.0 (+1.9) and t6 32.6 (+1.1), so the gap to #1 is now 2.4. Behind us, t3 (30.0), t14 and t18 (29.9) sit 1.6-1.7 back. `neg_points` has been flat at 119.1 since tick 988 (~213 ticks without a scoring deal).

## Our strategies: keep / kill / scale
- **Dealer bot: KILL** (except DENY or a non-closer card we need). Ladder is capped (0.437, negotiating flat), dealer gains clip to 0, and the last thread (Pícaros LAV-04) walked with 0 change.
- **Trading loop: KEEP.** It made 2 accepts today (+6.2 at 15:48, +15.5 at 17:46), both clean, and it is idle now only because of the pause.
- **Maker asks (5 open): KEEP the LAV spares, KILL the MAL ones.**
  - LAV-04 → t01 at 6 and LAV-03 → t04 at 6: each is ≈ +2.8 if filled, but LAV-04 has gone unfilled since 19:29. Reprice per plan §4A.
  - MAL-02 (→ t08 at 40), MAL-03 (→ t09 at 9) and MAL-08 (→ t01 at 20, unfilled since before 19:29) are single copies of a 6/10 page. See change 1.
- **In-room page closes: SCALE.** The SAL close (t08, SAL-06 at 28) was +40.4, the only big mover of the evening. RET, LAV and SAL are complete; MAL is the only page left within reach.
- **Flags: DONE.** Net +20, and the probe at 17:43 scored 0.
- **v10 market push: KEEP.** It is the directives' decisive lever. Our current `mm_points` is not in the data, so no fill evidence can be judged.

## Check the scout
- **Holds:**
  - Leaderboard gaps: 2.4 to #1, 1.6-1.7 over t3, t14 and t18.
  - The 5 asks go to non-top-4 teams.
  - t2 climbed +2.6 in 15 min, including MAL-10 from t13 at 30.
  - t7 collects RET×8 and LAV×7.
  - t6's RET sales at 77 and 84.
  - t10's LAV-11 bid at 205.
  - Ladder capped, and payday lets rivals afford page closers.
- **Fails:**
  - #2: t09's bid is for MAL-06 specifically, and El Rastro bids are per card, so MAL-08 cannot fill it. Selling MAL-08 also gives up a MAL page card.
  - #3: t13's 2 P bids are for RET and LAT commons, not LAV-02. The only LAV-02 price signal is one trade at 3 (tick 1194).
- **Missed:**
  - t10 is pulling away (+1.9/60 min).
  - Our 213 ticks without a scoring deal.
  - MAL-10 changed hands at 30, which makes a MAL page close affordable.

## The 3 changes with the highest expected gain
1. **Close the MAL page with payday cash (520 P).**
   - **What we need:** MAL-06, 07, 09 and 10. Values: uncommon 17.5, rare 49, bonus 46.4; the last card is worth ≈ 95 to us.
   - **Hold the cards:** cancel the MAL asks 17650, 17696 and 17392 to keep MAL-02, 03 and 08.
   - **Buy the first three at ≤ our value as maker bids:**
     - addressed to non-rival holders, on v15 or El Rastro;
     - sellers: t13 dumps MAL, t12 sold MAL-08 at 14, t02 holds MAL-10;
     - Dani finds the holders via the feed's `offer.listed` and the room.
   - **The last card must be a team trade** (a dealer close loses the bonus). Any price ≤ 45 hits the +50 cap.
   - **Effect:** ≈ +20 to +50 neg ≈ +1 to +2.4 board at ~0.05/np, enough to pass t6.
   - **Risk:** t09 bids 20 and 56 for the same cards, so it races us. Overpaying the non-closers, or ending with a partial page, costs (price − value). Stop if a rare goes above ~55.
2. **Arm DENY now that every team has +400 P.**
   - A single close by t3, t14 or t18 (≈ +2.4 board) takes our #3.
   - Analyst page alerts at 9/10 go to the Chief's DENY line (cap 35 P, team seller, never a rival's venue).
   - **Risk:** each denial is ≈ −1 board. Only act on a confirmed last card.
3. **Resume the maker book and v10 the moment the pause lifts** (Chief clears `run/hold-writes`).
   - Reprice asks unfilled for 10+ min (LAV-04, LAV-03).
   - Add the LAV-02 spares (×3, worth 1.3 each) as maker asks at ~3 to non-rivals.
   - Re-post the v10 ads to non-rivals, using the rebate guardrail.
   - **Effect:** a few neg points, plus up to +5 market if one positive-value-created trade lands on v10.
   - **Risk:** a trade that moves a card to a lower-multiplier holder makes v10's value created negative (tick 398: −5.2). Keep the radar's rival test.
