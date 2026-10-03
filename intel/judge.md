# Judge (claude-opus-5-5, Sat 14:56)

## Verdict
**Falling behind.** We are #5 at 28.1 (−0.8 over 15 min), 2.7 behind Team 14 (30.8, +0.3); the gap was 2.19 at 12:58. `neg_points` has been flat at 35.2 since tick 404 and the ladder at 0.181 since 12:45. Only duels (13.93) moved.

## Our strategies: keep / kill / scale
- **Dealer sells for the ladder (Pilar/Chato, offer-only): keep.** Four sells took the ladder from 0.072 to 0.181 at 0 neg cost. The weakest L3 slot is SAL-08 (+0.019), and L2 has 1 of 3 slots filled (LAT-08 +0.017).
- **SAL-06 buy for resale (Abuela, cap 25): kill above 22.**
  - Chato closed at 32 and Abuela held 25, which is her list price, so the buy adds no L1 ladder (our 4th L1 deal paid only +0.003).
  - At 25 we pay 2.5 above its value of 22.5, so neg drops by 2.5.
  - Resale at 25 or more to Pilar has one data point (Team 4); ours closed at 23. Plan §7.8 forbids buying to resell without a live bid.
- **Swaps 9172 (→t15) and 9173 (→t07): keep.** Together they are worth +18.1 neg at our values, with no fee as maker. They also bring SAL-07, the spare uncommon Pilar wants.
- **Maker book (9 asks): hold; do not scale yet.**
  - 0 fills in 226 ticks (neg flat since tick 404); we run 9 offers against the plan's 20-30.
  - Team-to-team commons now clear at 5 (ticks 595-610), below our 6-11 asks.
- **Asks on Team 15's stall v15: kill if still unfilled at tick 650.** Their value created scores for Team 15, not us, and 0 have filled since 13:21.
- **Trading loop (`loop.py`): keep, low value.** No accepts logged on Saturday, only pause and connection events. It costs nothing.
- **Team page buys: scale the pattern.** RET-01 at 20 from t10 scored +50.0, the only large gain since the reset. The 13:15 bargain watch has 0 hits so far.
- **Unopened sobre_plata (92.9): open question.** Unopened packs shift every trade's score by ~1-4 [L]. The Chief's reason for holding it is not in the data.

## Check the scout
- **Holds:**
  - Swap arithmetic: SAL-07 22.5 − 1.2 − 7 = +14.3; MAL-01 7 − 3.2 = +3.8.
  - Neg flat since tick 404.
  - A dealer sale above our value costs 0 neg, and it scores ladder only above the dealer's opening bid.
  - Team 6 sold RET-09 to t02 at 84; Team 14 sold RET commons at 9.
- **Partly holds:** the Pícaros early unlock. The L2 precedent (3 Abuela deals) is real, but our 3 Chato deals did not unlock L3, and Pícaros' level and unlock rule are not in the data.
- **Does not hold:**
  - "Abuela welcome price ≤ 25": not in the data; GAME.md says the welcome price did not reset Saturday [L].
  - The SAL-06 plan omits the −2.5 neg cost of buying at 25.
  - "Team 10's v10 stall earns value created": v10 is our venue, last measured at −5.2 `mm_points`.
  - The swap's feeding-rule check: t15 is only 6.2 below us, not ≥ 10. It is fine only if LAT-04/MAL-04 don't close its page.
- **Missed:** The Workshop ("Three spares. One surprise."). Our book and swaps commit all 5 of our second copies.

## The 3 changes with the highest expected gain
1. **Make the first 3 deals at the new dealer level count (Los Pícaros, at resume).**
   - Sell only at or above our value: SAL-01/03/05 at ≥ 9, MAL-02/03 at ≥ 7, LAT-03 at ≥ 5.
   - Step −2/−3, offer-only, never at the opening price, one thread per window; measure Δladder after the first deal.
   - **Effect:** L3 paid ~3× L2; three empty slots at a higher level are likely the largest lever left. The size is not in the data.
   - **Risk:** Pícaros may not buy commons, or may need an unlock we lack. Walk after 4 ticks with no live offer.
2. **Route SAL-07 from swap 9172 to Pilar, and drop the SAL-06 buy.**
   - If 9172 fills: sell SAL-07 to Pilar at ≥ 23 in small steps (the MAL-06 pattern paid +0.040) to replace SAL-08's +0.019 slot.
   - Cancel the Abuela SAL-06 job, or cap it at 22.
   - **Effect:** +14.3 neg (≈ +1.3 board at 0.094) plus up to +0.02 ladder (≈ +0.66 board).
   - **Risk:** t15 lets the swap expire at tick 650; Pilar's SAL final stays at 22-23.
3. **Hold 3 spares out of the book until The Workshop's menu is read.**
   - Keep LAV-02, LAV-03 and LAV-04 (second copies, 3.2 each).
   - Pull 9101 and 9136. Keep the swaps, since they gain more per card.
   - **Effect:** gives up at most ~+12 of unfilled asks for an unknown "surprise". The book has not filled in 226 ticks anyway.
   - **Risk:** the Workshop turns out worthless and we delay ~+4 per spare. Re-list as soon as its terms appear.
