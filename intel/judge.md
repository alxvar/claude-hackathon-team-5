# Judge (claude-opus-5-5, Sat 19:50)

## Verdict
Falling behind the leaders. We are #3 at 31.92 (+0.0 over 15 min, −0.1 over 60 min), and neg_points has sat at 119.1 since tick 988. Over the same 60 min, t10 gained +5.7 (now 34.0, 2.1 ahead) and t06 gained +1.1 (32.8, 0.9 ahead). Below us, t18 (30.3, +1.5) and t03 (29.8) are both inside 3.0 of us, so both now count as rivals.

## Our strategies: keep / kill / scale
- **Dealer bot: kill.** No dealer deal since tick 904. The last 8 threads all closed with no deal; Pícaros LAV-04 walked correctly at her opening of 4. Ladder is flat at 0.437 and adds nothing to the board.
- **Trading loop: keep.** Its two accepts today scored +6.2 (15:48) and +15.5 (17:46), with zero losses. It goes idle when the 20:25 Duels II stop job runs.
- **In-room team trades: scale.** This is the best lever of the day. The SAL close scored +40.4 and the t07 swap +15.5, and team trades are the only measured board mover (≈ +0.05 board per neg_point).
- **Addressed spare asks (6 live): keep, low value.**
  - At best they add ≈ +2 to +3 neg_points each: LAV-04 at 6 vs value 3.2, MAL at 9 vs 7.
  - LAV-04 has gone unfilled through t04 and t01 since ~19:09.
  - MAL-08 has gone unfilled at t01 since 19:09; its price has stepped 24 → 20.
- **v10 market push: keep, unverified.** Our current mm_points are not in the data, so the room plan and the rebate have no measured result yet.
- **Denial buys (DENY line): no action seen.** No t14/t06/t10 page alert is in the data.

## Check the scout
- **Holds:**
  - neg_points flat since tick 988.
  - t10 +5.7 over 60 min.
  - t14 1.6 behind us.
  - t09 bids MAL-06 at 20 and t04 at 19.
  - t07 bought RET-09 at 66 and RET-08 at 24.
  - The rebate costs ≈ −0.7 board unless it settles on v15 with a card we lack.
  - Six live asks, all to non-rivals.
- **Stale or wrong:**
  - "16871 MAL-08 at 21" is gone. The live offer is 17053 at 20.
  - t18's LAT-10 bid is offer 17066, not 16562.
  - "t10 +1.1 in 15 min" is wrong: the metrics say +0.2. "t06 +1.3 in 15 min" is also wrong: −0.1 over 15 min, +1.1 over 60.
  - "21 is above t01's median of 21.5" is false on its face.
  - "negotiating flat 21.88" is a 17:45 reading. Current negotiating is not in the data.
- **Missed:** t18 and t03 entered the 3.0 rival band.

## The 3 changes with the highest expected gain
1. **Find out why t10 gained +5.7 in an hour, then push v10 value created before 20:25.**
   - Market session: read t10's negotiating and market components from the leaderboard and post the result to the Chief within 10 min.
   - Dani: get the 17:45 room plan executed, only for trades where the buyer's multiplier is above the seller's: t02 SAL-03 → t08 and RET-03 → t07; t07 RET-01 → t09 on v10.
   - Effect: ≈ +5 board if one collector trade lands (t10 got +4.3 and we got +5 from one trade).
   - Risk: a dump trade turns our value created negative (−5.2 at tick 398), and every v10 sale also accrues the 5 P rebate.
2. **Move MAL-08 from t01 to t09 at 20 as maker (v15).**
   - t09 bids 20 for MAL-06, is 12 below us, and passes the ≥10 feeding rule. t01 is 7.9 below and allied with t10.
   - Effect: +2.5 neg_points, and it ends 40 min unfilled at t01.
   - Risk: t09 lacking MAL-08 is not in the data, so it may not fill either.
3. **Aleks: decide on PLAN #24 (days-read branch) before Duels II at ~20:33.**
   - Run the 439 tests plus one replay on a recorded `days` payload, then merge or explicitly reject the branch. Do not leave it unmerged by default.
   - Effect: Duels II is the main remaining negotiating lever named at 17:50. The size of the gain is not in the data.
   - Risk: a wrong days reading flips the value of every `days` duel.
   - Either way, the rebate settlement at 22:45 must go through v15 (fee 0) on a card we lack, worth ≥ the amount owed, so it nets ≈ 0.
