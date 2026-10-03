# Strategist (claude-opus-5-5, Sat 14:05)

## How the points really work
- **Board (Sat)** = (0.5·Fri + Sat)/1.5 on Negotiating 30 + Market 30. Judges 40 sit outside the board. Sunday (round 3) is 40% of the game. Round 2 reset `neg_points` and ladder at its start [V].
- **Duels:** 40% of Saturday Negotiating. Ours 13.93, 9 deals in the last 10.
- **Ladder:** 0.181 = L1 ≈0.055 + L2 0.017 (2 slots empty) + L3 0.050/0.040/0.019. +0.01 ≈ +0.33 board.
- **Team trades:** 35.2 neg. 1 pt ≈ 0.094 board. Capped at +50 per trade ≈ +4.7 board.
- **Market, bench:** the free stall earns half. Every board venue scored below the stall today, so the bench is flat across the field. Nobody gains there now.
- **Market, value created:** NET, floored at 0, capped at +5.0 board.
  - Ours: +4.99 after t10→t01 MAL-07, then −5.2 after t10→t15 SAL-07. It now contributes 0 (market back to 7.5).
  - Team 14's lead over us traces to one stall trade worth +3.10 [L, Analyst].
- **Gap to #1 = 2.7 board.** That is ≈ 29 neg points, ≈ 0.08 ladder, or about half the value-created cap.
- **Cheapest points by component:**
  1. Value created on v10: the only component where the field is near 0 (no team-venue trades Friday).
  2. L3 weak slot 0.019 during the Salamanca fever.
  3. L2 empty slots (+0.017 each), only through sells to Chato at ≥ our value.

## Our winning strategy
- **Saturday: make v10 the swap venue for low-ranked teams, and refill L3 in the fever.**
  - Value created up to +5 board closes the 2.7 gap alone.
  - We need ≈ +5.2 mm_points just to get back to 0.
  - One good trade on v10 (MAL-07, 7.5→12.5 market) moved +4.99.
- **Sunday: CHA page + ladder sprint in hour 1 + Duels III.**
  - CHA values: common 16, uncommon 40, rare 112, bonus 106.
  - Every team buy below value scores; dealer buys at ≤ value cost 0.
  - We already know the dealer protocols that took us from 0 to 0.181 today.
- **Why this beats the leaders:**
  - Team 14 dumps RET commons at 9 (ticks 591-598): volume, no cap events.
  - Team 10 and Team 12 rely on one-off big trades.
  - Nobody else has used a stall as a deliberate swap hub. Not in the data that anyone tries.
- **Stop:**
  - Chato buys above list. Never counted, and losses count in full.
  - LAV-11 hunting: t08's copy went to Pilar at 140 at tick 550, so the scout's item 3 is stale.
  - Spare asks at 7-9: team commons clear at 5.
  - Addressed asks on v15 unless t15 routes its swaps to v10.
  - Holding silent in dealer threads.
  - Chato L2 sales below our value (MAL to Chato at 14 = −3.5).

## Levers nobody is using yet
1. **Brokered swaps on v10.**
   - Evidence: team venues had 0 trades Friday. The only measured stall gains are ours and t14's. t15 and t07 swapped 3× at 0 P (ticks 607-616), venue not in the data.
   - Exploit: pitch dumper→collector pairs from Dani's profiles, outside the top 6:
     - t15 dumps SAL → t06/t08/t16/t09
     - t08/t06/t16 dump LAV → t07/t04/t09
     - t04/t16 dump MAL → t15
     - t04 dumps LAT → t16/t15
   - The buyer must collect the set (it shows in their bids), or the trade subtracts.
2. **Uncommon-last CHA page (cap-form bet).**
   - Evidence: both measured caps were commons, so flat 50 and 5×book are both still open.
   - Uncommon last bought from a team at ~25: value 146 → +121 if the cap is 5×book, vs +50 with a common last.
   - Cost if the cap is flat 50: about −7 (we lose a common's ~+8 gain and gain the uncommon's +15 earlier).
   - Derived from GAME.md values and clearing prices: asymmetric, +64 vs −7.
3. **Gift → ladder loop.**
   - Evidence: Abuela's gift LAT-08 became our only L2 slot (+0.017). `gift.given` seen only for t07 (Fri) and us (Sat).
   - Exploit: 5 Abuela deals early Sunday, then sell the gift to Chato above his opening bid at ≥ our value.
4. **sobre_plata held for Chamberí.**
   - Evidence: Saturday's grant pack gave RET-05 on RET's release day, so new sets appear in packs.
   - Keep it unopened until CHA is released (keeps the Chief's 13:49 call; overrides the judge's "open now"). Then open at once.

## Plan, anchored to the schedule
1. **Unpause (Operator):**
   - Renew swaps 9172/9173 if lapsed.
   - Reprice spares (LAV-02/03/04 2nd, SAL-02, LAT-04) to 5-6, addressed to collectors.
   - Keep MAL-02/04 ≥ 8.
   - SAL-06 from Abuela, preferably ≤ 23, Chief cap 25. Chato only ≤ list 26 (12:58).
2. **Now → fever (Lucas + Dani):**
   - Pitch t15 + t07 to make their next swaps on v10. In return, we keep our addressed asks on v15.
   - Then the pairs in Lever 1.
   - Measure mm_points per settlement and stop any pair that moves it down.
3. **Bench 7.0 (Market session):** stall live, recorder on. Read every team's market after each bench.
4. **Salamanca fever, game 9.15-11.15 (Operator, dealer bot, offer-only, one thread):**
   - Pilar SAL-06, then SAL-07 (if 9172 fills): open ~30, steps of −2/−3, floor 22.5 (our value).
   - Goal: replace the 0.019 and 0.040 slots (≈ +1 board).
5. **Duels II, game 11.65 (Aleks):** integrative days (his 15:30 call), ≤ 3 exchanges.
6. **Benches 13 / 14.65 hard / 15 (Market):** stall supervised.
7. **Evening (Operator):** sell spares; Saturday cash floor 100. Carry 184 + sales + the 150 grant into Sunday.
8. **Round 3 at 16.65 (Operator):**
   - Read /api/me for the reset.
   - After the CHA release: open sobre_plata.
   - Abuela 5 deals below list (CHA commons if she sells them; not in the data). Then gift/pack LAT/MAL cards → Chato L2 / Pilar L3 sells.
9. **Sunday CHA page (Operator; Lucas approves the cap bet):** rares first (team ≤ 112, or Chato ≤ value), commons next, uncommon LAST from a team. Cash floor 0 (11:35).
10. **Duels III at 18.65 (Aleks):** close fast. **Benches 17/19/21:** stall live.
11. **Judges (Lucas + Dani):** the measured-facts table plus the v10 swap-hub story.

## Hypotheses to test
- **Value created on v10 = buyer value − seller value, net.** Experiment: the first brokered swap. Metric: mm_points before and after that settlement.
- **The ladder is scored against Pilar's fever price range.** Experiment: SAL-06 sale in the fever. Metric: Δladder vs SAL-08's +0.019 (and vs MAL-06's +0.040).
- **Cap = 5×book, not flat 50.** Experiment: the CHA uncommon-last close. Metric: neg Δ of 50.0 vs >50.
- **Round 3 resets ladder, neg and duels; level 3 carries.** Experiment: read /api/me at the round event. Metric: `ladder_points`, `neg_points`, level.
- **The Abuela gift resets daily.** Experiment: the 5th Abuela deal Sunday. Metric: a `gift.given` event.
- **Packs opened after the CHA release yield CHA.** Experiment: open sobre_plata Sunday. Metric: the cards pulled.
- **A correct flag scores.** The penalty for a wrong flag is not in the data. Experiment: one flag, only on a message whose words contradict its structured offer. Metric: score Δ in an isolated window.
