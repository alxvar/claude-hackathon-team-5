# Judge (claude-opus-5-5, Sat 20:06)

## Verdict
**Holding #3 but falling behind the leader.** We are 31.92 (+0.2/60 min), Team 10 is 34.2 (+2.5) and Team 6 is 32.5 (+0.8). Our gap to Team 10 grew from 1.42 (tick 1100) to 2.3. Team 12 is climbing fastest (+2.7/60, 3.5 behind). `neg_points` has been flat at 119.1 since tick 988 (~190 ticks).

## Our strategies: keep / kill / scale
- **Dealer bot: kill.** Picaros LAV-04 walked at 19:04 with 0 change. The last 8 dealer threads closed with no trade. The ladder is capped (17:45), flags are done and egg hunting has stopped.
- **Trading loop: keep, low yield.** Its last accepts were +6.2 (15:48) and +15.5 (17:46), with nothing since. It is paused from 20:25 for Duels II.
- **Our asks (6 open): keep as maker, but they are marginal.**
  - Each gains ≤2.8: LAV-03/04 at 6 vs 3.2, MAL at 9 vs 7, MAL-08 at 20 vs 17.5.
  - The whole book is ≤ ~12 neg (≈0.6 board at the 0.05/np rate measured at 17:46).
  - LAV-04 has gone unfilled since ~19:09 across t04 and t01.
  - **Risk:** LAV-04 → t01. t01 collects LAV, is 8.0 below us (the feeding rule needs ≥10) and is allied with t10 (17:45). Whether it closes t01's LAV page is not in the data. Check that before it fills.
- **In-room page trades: these were our best lever, now spent.** SAL-06 → +40.4 (tick 988). LAV, RET and SAL are complete. Dani's table shows no sale that passes the feeding rule.
- **v10 venue: scale.** It is the only lever still worth whole board points (+4.99 at tick 311 [V]). Our current asks sit on v15 and El Rastro, so they add nothing to v10.

## Check the scout
- **Holds:**
  - Board numbers.
  - The v10 +5 precedent [V tick 311].
  - The rebate settlement risk (≈ −15 if we pay a fee on a cheap card).
  - Never sell SAL/LAV/RET cards. But the right threshold is each card's value (68.6–177.1), not "≤ 85". Pilar's ~80 for rares is a loss at any price.
- **Wrong:**
  - #2 contradicts itself. Repricing MAL-08 to ≤15 sells below its value of 17.5, which is a loss.
  - The IDs are stale: the live offers are 17392 (MAL-08 at 20, not 24) and 17330 (LAV-03), not 17053/17028.
- **Unsupported:** "T10's gain comes mostly from venue/market". No component breakdown exists in the data.
- **Missed:**
  - Team 12 (+2.7/60) is the real climber.
  - Team 14 is falling (−1.3/60), not "close".

## The 3 changes with the highest expected gain
1. **Before 20:25, Dani brokers one positive value-created trade between non-rivals on v10.**
   - Buyer: t16 (#15, a RET collector) has live El Rastro bids: RET-06 at 13, LAV-07/08 at 12, RET-01/02 at 5.
   - Sellers: t13 or t08 (both dump RET/LAV) list those cards on v10 at t16's bid, and t16 accepts there. The 19:40 rebate applies.
   - Expected: mm up to +5 board [V precedent].
   - Risks:
     - Value created is negative if the buyer's multiplier is below the seller's (−5.2 at tick 398). Only proceed if t16 collects the set more than the seller does.
     - Never involve t10 or Team 3.
2. **Settle the 22:45 rebate with a MAL card we lack, bought as maker on v15 (fee 0).**
   - Rares MAL-09/10 are worth 49 each. At the 30 P cap that is about +19 neg, instead of about −15 for a cheap El Rastro card.
   - Fallback: MAL-06/07 (worth 17.5) at ≤ 17.5 scores ≥ 0.
   - The Operator reads `/api/me/value` first and bids addressed to the partner (t07 dumps MAL).
   - Risk: the partner lacks the card. Then settle at the owed amount on whatever MAL card it holds, at ≤ its value.
3. **Duels II: Aleks picks the `days` mode now.**
   - Merging the Builder's branch duelist-days-read @552819d is his call.
   - Pre-load the decay-aware close: we have ≤3 exchanges at 8%.
   - Duels II is the last scored event tonight. Its expected size is not in the data.
   - Risk: misreading `days` flips the value of every package. Use `unsure` mode if the first payload is ambiguous.
