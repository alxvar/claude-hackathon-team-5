# Judge (claude-opus-5-5, Sat 15:28)

## Verdict
**Holding at #5, not catching up.** We are at 28.15, 2.65 behind #1 Team 14 (30.8).
- Over 60 min we gained +1.8 against Team 14's +1.1, so the gap to #1 closes about 0.7/h.
- Team 10 (+4.1) and Team 18 (+2.2) passed us in the same hour.
- We lost 0.8 in the last 15 min.
- `neg_points` has been flat at 35.2 since tick 404, which is 226 ticks with no scoring trade.
- Ladder has been flat at 0.181 since 12:45.

## Our strategies: keep / kill / scale
- **Pilar sells (dealer bot, offer-only): keep.** MAL-07 19, MAL-06 19 and SAL-08 23 all closed at or above our value. They took the ladder from 0.072 to 0.181 at 0 neg cost, and they are the best-evidenced lever of the day.
- **SAL-06 from Chato at list 26 (directive A): kill.** He held 33 → 32 and the thread closed (tick 577). Never above his list.
- **SAL-06 from Abuela: keep, but only at ≤ 25.**
  - She went 29 → 25 and held 25 (tick 596). Thread 868 is open at 29 vs our 21.
  - Bid 9168 at 21 expires at tick 634.
  - If she holds above 25, walk.
- **Trading loop and maker book (9 asks): scale down and re-aim.** Zero fills in 226 ticks.
  - Single-copy asks are priced at or above our value against a common clearing price of 5 (team trades at ticks 595-610). They cannot gain:
    - SAL-01 at 11 (value 9)
    - LAT-03 at 7 (value 5)
    - MAL-02 at 9 (value 7)
  - The MAL-02 ask is addressed to t15, which sold its own MAL-02 at 5 at tick 602, so it has no buyer.
- **Swaps 9172 → t15 (+14.3) and 9173 → t07 (+3.8): scale.** Both are maker trades with no fee, and both partners pass the feeding rule (t15 #14, t07 #17). Both expire at tick 650.
- **Bargain-buy guardrail (13:15): keep, no action.** No ask on the board qualifies (LAT-06/08 at 24-25 vs value 12.5; RET-04 at 12, which we already hold).
- **In-room trades (Dani): not visible in the data since tick 404.** The swaps need him now, while the clock is paused.
- **Unopened sobre_plata (92.9):** this is Chief's call. The reason for holding it is not in the data. It adds a 1-4 point drag to each trade's score.

## Check the scout
**Holds:**
- Pilar deals at 19 / 19 / 23.
- Swap gains: +14.3 = 22.5 − (1.2 + 7); +3.8 = 7 − 3.2. +18 neg ≈ +1.7 board.
- Bid 9168 expires at tick 634.
- Pilar's uncommon median is 18 over 5 deals.
- t14 sells RET commons at 9 (ticks 591-598).
- t10's MAL-10 buy at 74.
- t04's RET-06/08 bids at 26-27 (we keep both cards).
- The top 4 are within 2.7 points of us.
- Pícaros' unlock rule and prices are correctly marked "not in the data".

**Wrong:**
- "SAL-06 at ≤ 25 costs about −0.33 neg." The −0.33 in the directive is board points at list 26 (3.5 neg × 0.094). At 25 the cost is −2.5 neg ≈ −0.24 board.

**Missed:**
- Our MAL-02 ask targets a seller of MAL-02.
- SAL-07 from swap 9172 is a free Pilar-sale vehicle. It makes buying SAL-06 a second step, not the first.
- The book has been dead for 226 ticks.

## The 3 changes with the highest expected gain
1. **Close the swaps during the pause.**
   - Dani pitches t15 and t07 in the room now, pointing at 9172 and 9173.
   - Operator re-posts both before tick 650, asking 2× the wanted ticks because the server halves them.
   - Effect: +18 neg ≈ +1.7 board.
   - Risk: t15 keeps SAL-07 for itself. The partners are low-ranked, so no leader is fed.
2. **SAL-07 → Pilar first, then decide on SAL-06.**
   - Once SAL-07 arrives, sell it to Pilar offer-only, alone in its window: open around 30, step −2/−3, accept only ≥ 22.5. Measure Δladder against our weakest L3 slot (SAL-08, +0.019).
   - Buy SAL-06 from Abuela at ≤ 25 and repeat only if that measurement moves the ladder.
   - Effect: about +1.4 board per slot [L, Analyst].
   - Risk: Pilar's finals of 18-23 sit below 22.5. Walk rather than sell under value.
3. **Free the cards for the new levels.**
   - Cancel the asks on SAL-01, LAT-03 and MAL-02. They have no buyer at those prices and are our Pícaros candidates for sells at ≥ value. Cancel each card's team ask before its dealer thread.
   - Hold LAV-03, LAV-04 and SAL-02 off the book until The Workshop's menu ("Three spares") is read at the resume. If it is worse, sell them as maker at about 5 to teams ≥ 10 points below us, for about +2-4 neg each.
   - Effect: a possible new ladder level; its size is not in the data.
   - Risk: Pícaros or the Workshop pay less than our values. Then nothing is lost but 226 ticks of unfilled asks.
