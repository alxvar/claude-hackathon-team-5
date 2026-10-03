# Strategist (claude-opus-5-5, Sat 11:39)

## How the points really work
- **Board** = Negotiating 30 + Market-making 30 + Judges 40 per round. Friday counts 20 %, Saturday 40 %, Sunday 40 %. All game parts are relative to the field: t13 sits at the top with 27.7; we are #7 with 22.35, a gap of 5.35.
- **Negotiating** = duels + ladder + team-trade value. How the three are weighted against each other is not in the data.
  - 1 `neg_point` ≈ 0.16 board [L]. Ours: 35.2.
  - Each team trade is capped at +50 [V]. Dealer deals only ever score ≤ 0 [V].
- **Market-making** = bench (the stall earns half; full points go to the top-3 mean) + NET value created on our venue v10.
  - One collector-buy on v10 gave +4.99 mm, moving our market score 7.5 → 12.5 (≈ 31 `neg_points` at 0.16).
  - One dump trade (t10 → t15, SAL-07) wiped it out: mm −5.2, #3 → #7. **One venue trade ≈ 60 % of a 50-cap page, at zero cost to us.**
- **Ladder**: best 3 deals per level, higher levels weigh more, a missing deal counts 0.
  - Ours is 0.055, all from level 1. Our level 2 (Chato) and level 3 (Pilar) slots are empty.
  - Board points per ladder point: not in the data.
- **Judges 40** is the biggest block. Its format is not in the data (desk Q7 has no answer in our files).
- **Round reset** [V Sat]: `neg_points` and ladder go to 0 at each round start; holdings carry over. The Sunday 16.65 round resets them again. Today's `neg_points` only score until 23:00.
- **Where the field is weak (cheapest points)**:
  1. Duels: 102 scored duels today, every team still at 0.
  2. Venue value: Friday's 4 team venues had 0 trades; the stall teams sit at 7.5.
  3. Ladder levels 2-3 are empty for us.

## Our winning strategy
Own the three uncapped, empty components. Stop grinding 2-5 point spares as the main engine.
1. **Duels I/II**: zero accept collisions, close fast. This is the largest pool open to everyone today.
2. **Make v10 the venue for collector bids and duplicate sales**, from teams ranked below us. Every positive trade there is worth ~+5 board. Our two pages took a whole day for +100 `neg_points` (≈ 16 board).
3. **Sunday CHA from TEAMS, not dealers.**
   - CHA cards are worth 16 / 40 / 112 to us; clearing prices are 9 / 24.5 / 70.
   - So each card bought from a team scores +7 / +15.5 / +42; a dealer buy scores 0.
   - Use dealers only below list (ladder slots) or for cards no team sells. Close the page with a common bought from a team (+50).
   - Each P carried into Sunday ≈ 0.64 `neg_points` [directive]: Saturday cash is Sunday score.
4. **Ladder levels 2-3**: zero-loss sells only.

**Why this beats the leaders:** t13 wins on trade volume (45 deals) and on lobbying for v03. Volume never counts, and the cap stops page plays at 50. Duels and venue value have no cap and are empty.

**Stop:**
- Dealer buys of cards we don't need.
- loop.py taker accepts (no measured value).
- Any offer on a top-4 venue (v07 while t10 is top 4).
- Public asks.
- Building SAL/MAL/LAT pages: cash is at the floor, SAL rares trade at 64-80 against our value of 63, and a MAL rare is worth only 49 to us.

## Levers nobody is using yet
1. **v10 as a 0-fee venue for bids.**
   - Evidence: all 46 Friday trades went through El Rastro. Live rival bids sit there today: t17 MAL-09 at 70, t06 SAL-09 at 68, and t09's 8 bids. Whoever fills a bid there pays ceil(5 %) + 1, which is 5 P on 70.
   - Pitch (Dani/Lucas): "re-post your bid on v10: the seller pays no fee, so it fills sooner."
   - A collector's bid filled by a willing seller creates value. Pitch only teams ranked below us (t04, t14, t16, t17, t03, t15, t06, t08, t09, t07).
2. **Duplicates sold to lackers always create value.**
   - A second copy is worth 25 % to its holder. A lacker values it at 100 % × m, which is at least 50 % (lowest multiplier 0.5). Any such trade on v10 is positive, whatever the multipliers.
   - Rivals' asks on El Rastro (LAV-04 at 10 ×4, LAT-04 at 9 ×2, MAL-02 at 8 ×2) look like duplicates. Pitch: "list your duplicates on v10."
3. **Card-for-card swaps.**
   - Evidence: the 83 team trades in the feed are all for cash, and we are at the cash floor.
   - Offer our duplicates (LAV-02/03/04, SAL-02, LAT-04, worth 1.2-3.2 to us) for first copies we value: SAL-04 (9), MAL-01/05 (7), and CHA on Sunday (16).
   - Maker side, addressed to collectors outside the top 4.
4. **Fill ladder slots with sells.**
   - Evidence: Chato's uncommon buys from teams have a median of 14 over 2 deals, i.e. rivals sell at his opening, which doesn't count.
   - LAT-08 (worth 12.5): sell protocol, open ≥ 39, step −2/−3, his final is 15-16 [V]. Zero loss.
   - SAL-08 (worth 22.5) to Pilar during the fever: book 25 × 1.25 = 31.25. Zero loss, +31 P.
5. **Sunday runs fast [L].**
   - Game hour = 1.33 + tick/120 fits both tick 160 and tick 409.
   - With 15 s ticks, Sunday game time runs 2× wall time: CHA ≈ 09:15, bench 17.0 ≈ 09:25, Duels III ≈ 10:15.
   - Have CHA bids pre-written and post them on the release tick.

## Plan, anchored to the schedule
Wall time ≈ game hour + 6.83 (fits "Duels II ≈ 18:29").

| # | When | Who | Move | Expected impact |
|---|---|---|---|---|
| 1 | 11:40 / 11:50 | Operator | Dealer threads off at 11:40, loop.py off at 11:50; book.py keeps posting as maker | Protects 34 scored duels |
| 2 | Duels I, 11:59 (5.15) → end | Aleks | Duelist live | Duel share |
| | | Dani + Lucas | Walk the addressed asks (fills use their accept) and pitch v10 bids and duplicates to teams below us | +5 board per positive v10 trade |
| | | Market | Log the sign of every v10 trade; page Lucas on a negative one | |
| | | Lucas + Dani | Draft the judges' pitch | Judges 40 |
| 3 | After Duels I (Pilar open to all at 12:20) | Operator | LAT-08 to Chato if t03 hasn't filled it at 25 | One level-2 ladder slot, 0 loss |
| | | Operator | MAL-06/07 stay on teams (t17/t15) | +3.5 to +8.5 each |
| 4 | Fever, ≈ 16:00 → 17:30 (organiser text; schedule says ≈ 18:00) | Operator | SAL-08 to Pilar at ≥ 31 | Level-3 slot + cash |
| 5 | Benches 13:50, 15:50, 17:50, 19:50, hard 21:29, 21:50 | Market | Keep the stall. No board venue today: 270 P against cash 109 and floor 100 | — |
| 6 | Duels II, 18:29 | Operator, Aleks | Zero dealer threads, no taker accepts; days logic | Duel share |
| 7 | 19:30 → 23:00 | Operator | Sell spares to collectors as maker; duplicate swaps | Cash ≥ 170 (cha-plan) |
| 8 | Sun 09:00 | Operator | Re-read clock and schedule. On the release tick: maker bids for all 10 CHA page cards at 9 / 24.5 / 70 | +7 / +15.5 / +42 each |
| | | Operator | Dealers only below list (Abuela 10/25, Chato 26/77) for 3 ladder slots per level | Ladder |
| | | Operator | Last common from a team | +50 |
| | | Dani | Pitch v10 for CHA duplicates | Venue value |
| | by 14:00 | Operator | Cash floor → 0 (GUARDRAIL) | — |
| 9 | Duels III (game 18.65) | All | Same freeze as Duels I | Duel share |

## Hypotheses to test
- **Venue value per trade is linear, not saturating.** Test: the next positive v10 trade. Decides by Δmarket: ≈ +5 again → venue pitching outranks every other lever.
- **The −5.2 deficit must be repaid before market rises above 7.5.** Test: the same trade. Decides by `mm_points` after it.
- **A Chato sale above his opening fills a level-2 slot.** Test: LAT-08. Decides by Δ`ladder_points`.
- **A Pilar sale fills a level-3 slot.** Test: SAL-08 in the fever. Decides by Δ`ladder_points`.
- **A swap scores value in − value out.** Test: one duplicate-for-first-copy swap. Decides by Δ`neg_points` vs the prediction.
- **Board value of duels.** Test: the first Duels I results. Decides by `duel_points` vs our score change; sets the accept-freeze priority.
- **Sunday tempo.** Test: `/api/clock` at Sun 09:00. Decides by game hour vs tick; sets every Sunday time in the plan.
- **Teams actually supply CHA.** Test: count CHA asks and bids in the first 60 ticks after release. If none, switch to dealers below list.
