# Strategist (claude-opus-5-5, Sat 15:42)

## How the points really work
- **Board now** = (0.5·Fri + Sat)/1.5 [V]. **Final** = (0.5·Fri + Sat + Sun)/2.5, so Saturday and Sunday are 40% each. Judges (40) are not on the board.
- **Negotiating** has three parts:
  - Duels: 40% of Saturday Negotiating [V]. Ours is 13.93; the field's duel figure is not in the data.
  - Team trades: 1 `neg_point` ≈ 0.094 board [V]. Capped at 50 per trade, so the best possible trade is ≈ +4.7 board.
  - Ladder: +0.01 ≈ +0.33 board [V]. Best 3 deals per level count; higher levels weigh more.
- **Market-making** has two parts:
  - Bench: the free stall earns half; full points go to the top-3 mean. Every board venue scored below the stall today, so the bench is nearly flat across the field. No cheap edge on Saturday.
  - **Value created on our venue:** net across trades, capped at +5.0 board, floored at 0 [V].
    - Team 14's single trade on its stall gave +3.10. That trade is more than our 2.7 gap to #1.
    - We are at −5.2 `mm_points`, which shows as 0 on the board. We need more than +5.2 net value created just to start counting.
    - One page-closing trade between two other teams on our stall earned +4.99 [V tick 311]. This is the cheapest board point left.
- **Round boundaries (from `/api/schedule`):**
  - Round 3 fires at hour 16.65, Sunday 11:34, not at 09:00.
  - Sunday 09:00-11:34 still counts for Saturday's round. That includes the hard Market Test (09:34) and the 09:55 bench, at 15 s ticks.
  - Round 3 runs only ~3.4 h (to 15:00) but weighs exactly as much as Saturday's 14 h. Sunday points are worth about 4× per hour.
  - Round 3 resets neg, ladder and value created (as round 2 did at tick 160). Its benches are 11:55 and 13:55; whether 21.0 runs after close is not in the data. Its only duel session is Duels III (13:34).
- **Where the field is weak:**
  - Value created on venues: only Team 14 shows a score from it.
  - The L4 ladder (Pícaros): empty for everyone.
  - Round 3's first hour: it opens to whoever is staged.

## Our winning strategy
1. **Saturday: become a matchmaker, not a trader.**
   - Dani steers mutually useful trades between other teams onto our stall, to get back above the −5.2 floor and toward +5.
   - The **sellers** must be teams that dump the set, sold to collectors. A card moving to a lower-multiplier holder subtracts (t10 → t15 SAL-07 cost us 10.2).
2. **MAL-09: the largest single trade we can still make.**
   - Worth 49 to us; t17 bids 70-85 [scout].
   - An ask at **99** as maker makes our gain (+50) ≥ t17's capped gain (≤ 50).
   - At 85 we bank +36 (≈ +3.4 board → ~31.4). t17 would end at ≤ ~30.5, still below us, and the sale also passes Team 14 (30.7).
   - The 85 floor breaks plan §4A's "≥ 10 below us" margin (t17 is 2.2 below). **Lucas decides the floor.** The Chief held MAL-09 for Pícaros; one ladder slot (~+1.65 board at L3 rates) is worth less than +3.4.
3. **Sunday: win round 3 by being staged at 11:34.**
   - Build the CHA page through dealers at or below list. Each deal fills a ladder slot and adds a page card; CHA values (16/40/112) are above dealer prices.
   - Take the last card from a team (+50 cap).
   - Carry a "ladder kit" over the reset: cards sellable at ≥ our value for each level, plus cash.
   - Arrange one positive value-created trade on our stall in round 3 (it starts at 0).
4. **Stop doing these:**
   - Single-copy maker asks: 0 fills in 226 ticks.
   - Abuela → Pilar round trips (break-even; L3 is near saturation).
   - Any dealer buy above list.
   - Any board-venue spend on Saturday.

## Levers nobody is using yet
- **Value created by matchmaking between others.**
  - Evidence: 109 team trades, almost all on El Rastro (nobody scores); only t14 shows the component.
  - Use: Dani pairs teams below us and outside the top 4, in their own interest, on our stall:
    - SAL dumpers t04, t07, t02 → SAL collectors t06, t08, t01.
    - t13 (dumps RET) → t04's live RET-06/08 bids (26-27).
    - t15 ↔ t07 swaps posted on our stall instead of El Rastro or v15.
  - Never use a top-4 team as a party. Our stall's fee vs El Rastro's 5% + 1 is not in the data: Operator reads `/api/venues` for the pitch.
- **Round 3's late start.**
  - Evidence: nobody's plan in the data treats 09:00-11:34 as Saturday.
  - Use: maker trades and the two benches Sunday morning bank into Saturday. At 11:34 we fire pre-queued dealer threads on all levels at once.
- **Salamanca fever (18:03-20:03; Pilar pays 25% over book).**
  - Use: SAL-08 (worth 22.5) at ~31 brings cash for CHA, plus a ladder-slot check against our weakest L3 slot.
- **Pícaros L4.**
  - Use: fill its 3 slots with commons and spares at ≥ value, not with MAL-09.

## Plan, anchored to the schedule
1. **Now-15:54 (Lucas, Operator).**
   - Lucas decides the MAL-09 floor.
   - Operator posts an ask at 99 addressed to t17 on El Rastro, then steps −3 every ~10 min to the floor.
   - Expected +36 to +50 neg (+3.4 to +4.7 board).
2. **15:40-18:00 (Dani, Operator).**
   - Dani brokers the pairs above onto our stall. Operator logs `mm_points` per settlement.
   - Target: net > +5.2, then up to +5 board.
   - Swaps 9387/9389 stay live to tick 688.
3. **15:54 bench (Market):** stay on the stall; recorder on.
4. **Pícaros opens (Operator, armed watch).**
   - Offer-only, small steps, sell at ≥ value: MAL-02/03/04/05 (7), LAT-03 (5), SAL-03/05 (9).
   - Measure Δladder on the first deal and continue only if it moves.
5. **~16:40, Abuela gift pack:** auto-open, alone in its window.
6. **Workshop menu:** hold 3 spares (2nd LAV-02/03/04) until it is read. If it is worse, sell them as maker to t07 (+2-4 neg each).
7. **18:03-20:03 fever (Operator).**
   - SAL-08 → Pilar, opening ~34, steps −2/−3, floor 23.
   - Keep it only if Δladder > 0; the cash goes to the CHA fund either way.
8. **20:33 Duels II (Aleks).**
   - Integrative play: give away days the rival values, take price, ≤ 3 rounds.
   - The trader keeps running (Lucas 12:50).
9. **21:00-23:00 (Operator).**
   - Sell no CHA-fund cards below value; target cash ≥ 186.
   - Keep the round-3 ladder kit: LAT-08 (Chato ≥ 14), commons and spares (Abuela/Pícaros ≥ value).
10. **Sunday 09:00 (Operator, Dani).**
    - Re-read `/api/schedule`.
    - Maker book and matchmaking until 11:34 (Saturday credit).
    - Hard test 09:34 on the stall.
11. **Sunday 11:34-11:40 (Operator).**
    - Open all dealer threads at once at 15 s ticks (Abuela 8/h, Chato 6/h, Pilar 6/h).
    - Buy CHA below list; take rares from teams if ≤ 112.
    - Leave the last CHA card for a team trade (+50).
    - Dani lines up one positive trade between others on our stall.
12. **Sunday 13:34 Duels III (Aleks):** the only duel session in round 3; close within ≤ 3 rounds at 10% decay.
13. **Before 15:00:** cash to 0 into non-negative CHA buys. Lucas and Dani pitch the judges with the measured-facts table.

## Hypotheses to test
- **Our stall's value-created trades lift `mm_points` above the −5.2 floor.**
  - Test: the first brokered pair.
  - Metric: `mm_points` and `market` per settlement.
- **Round 3 resets value created and the ladder.**
  - Test: read `/api/me` at 11:35 Sunday.
  - Metric: `mm_points`, `ladder_points` = 0.
- **A Pilar fever sale counts on a fever-raised range.**
  - Test: one SAL-08 sale, alone in its window.
  - Metric: Δladder compared with our weakest L3 slot (+0.019).
- **Pícaros' ladder weight exceeds L3 (+0.050 best).**
  - Test: one common sale at ≥ value.
  - Metric: Δladder.
- **An Abuela SELL above her opening bid moves L1, as Chato's did.**
  - Test: one 2nd-copy sale (value 1.2-3.2) on Sunday after the reset.
  - Metric: Δladder.
- **The MAL-09 floor.**
  - Test: ask 99 → 85.
  - Metric: the fill price, `neg_points` Δ, and t17's board change versus ours.
