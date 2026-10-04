# Judge (claude-opus-5-5, Sun 11:43)

## Verdict
**Holding at #4 (32.8; +0.5 over 15 min, +0.6 over 60 min).** We are closing slowly on t12 (34.7, −0.2/60) and t18 (33.0, −0.1/60), but losing ground to t10 (34.1, +1.0/60). The gap to #3 is 0.2 and to #1 is 1.9. Behind us, t04, t09 and t15 are climbing fast (+5.5 to +6.4 per 60 min, now at 27-29).

## Our strategies: keep / kill / scale
- **Team trades (all):** zero marginal value now. `neg_points` has sat at 50.0 since tick 1585 (CHA close), and the round cap of 50 is real (Chief 11:33). Further gains don't score; only losses beyond the ~29 slack would.
- **Dealer bot, common sells at 5-6 (Pícaros/Abuela, ticks 1787-1810; LAT-03 walk 10:51):** **kill.** These deals score 0 neg, and LAT-03 left the ladder at 0.342 → 0.342. Cash never scores.
- **MAL close / MAL-09 Pícaros retry:** **killed, correctly.** The Chief called NO-GO at 11:33. The retry walked at their 58 against our 44. Lucas logged "no more retries": hold to that.
- **Trading loop:** **keep idle.** Its log has no Sunday events (0 fills since Saturday 17:46). Under the cap it can only cost points.
- **Our LAT-06/07/08 bids at 9 (El Rastro, the reward leg):** keep, unscaled. They are unfilled about 7 min after posting, sit at ≤ value (LAT uncommon 12.5), and cost 0 points.
- **v10 bounty (20 P × 5, GUARDRAIL 11:38):** keep, but fix one hole (change 3). v10's value_created is still 0, and no v10 settlement appears in the data.
- **Duels:** **scale.** Duel score is 21.83 with 199 finished; it is the only Negotiating lever still uncapped. Two duels are live, so the duelist is running again after the 09:46 stop.

## Check the scout
- **Holds:**
  - The t07 bids of 8 on CHA-01..05 and t09 bids of 15 on CHA-06..08.
  - "Don't sell anything."
  - t12's SAL-12 sale at 380.
  - t18 is just ahead of us (now by 0.2, not 0.4).
- **Stale:** its #1 action (MAL close) was cancelled at 11:33. Its premise "trade part not capped" is false: the cap is 50 and `neg_points` is flat.
- **Wrong:**
  - The Pícaros' MAL-09 went 73 → **58** (our bid was 44), not 49.
  - LAV-07 went **t13 → t12** at 40 (t12 bought it); it did not sell it.
  - t02 is not #10; t13 is (27.1).
- **Missed:** t04, the fastest climber (+6.4/60, now 28.9).
- **Rank:** metrics now show t12 at #1 and t10 at #2.

## The 3 changes with the highest expected gain
1. **Have v10's broker live and supervised for the 12:00 Market Test (operator/Market session, now).**
   - Each Sunday bench is half of round 3's bench score (plan §2b), and a venue whose broker is down scores 0.
   - Our current bench efficiency is not in the data.
   - Risk: a restart close to 12:00 leaves the broker down during the test. Don't touch the code; only check that it is alive.
2. **Load the Duel Lab's Final config between Duels III and the Final (Aleks).**
   - The config is 506a2fd, ACCEPT_BY 1, MAX_STEP_SHARE 0.08, and a worth floor of 0.075 × limit in code.
   - Expected gain: +0.018 to +0.033 per duel across all 9 worlds.
   - Risk: if decay counts per tick, we lose about 0.04-0.05.
   - Run the first-wave check (no below-limit accepts, no CAN'T READ) right after wave 1.
3. **Make the v10 bounty and ad never pay a rival.**
   - **Exclude t12, t18 and t03 as bounty sellers**, alongside t10. A bid above their value scores up to +20 `neg_points` for them; the 09:28 directive already bans any v10 pair that lets t12 gain.
   - **Steer the ad text toward sales into collectors of the set.** Value created on our venue is net, and a card that moves to a lower-multiplier holder subtracts from us (Sat 11:30: +4.99 → −5.2).
   - Risk: fewer qualifying trades before the bounty slots expire. The Chief's fair-play review risk stands either way.
