# Judge (claude-opus-5-5, Sun 10:40)

## Verdict
Holding #4 and closing on #3. We are at 32.4: t18 is 0.6 ahead (33.0), t10 1.1 ahead (33.5), t12 2.6 ahead (35.0). Over 15 min we gained +2.8, second only to t12's +4.0. Over 60 min we gained +2.2 against t12 +3.5 and t03 +2.9 (t03 is 2.7 behind and gaining).

## Our strategies: keep / kill / scale
- **CHA page close (team trade): KEEP, done.** CHA-05 from t02 at 72 took neg 0 → 50.0 (cap). The 9 other cards came from dealers at 0 neg.
- **Cash sales of high-value cards: KILL.** RET-11 sold to t02 at 240 (taker, fee 13) was expected at +29 and measured 0 (neg 50.0 → 50.0). It turned the card into cash, which scores nothing.
- **Dealer bot at the Pícaros (L4): KEEP, change one thing.**
  - MAL-10 at 46 moved the ladder 0.172 → 0.253 (+0.081) with 0 neg.
  - MAL-09 was a bait and switch twice (threads 2595, 2617). The trick guard held both times. The Pícaros route for MAL-09 is dead.
  - LAT-03 sell (thread 2632) is stepping 12 → 11 (−1). The playbook says −2/−3; −1 invites an early low final.
- **MAL close (directive 10:25): KEEP, with a constraint.** We hold MAL-01..06, 08 and 10. MAL-09 (value 49) can now only come from a team. Its holders are not in the data. If neg is capped at 50 this round, the close's payoff is only the reference effect (directive 01:40).
- **Public LAT-06/07/08 bids at 9 (ladder fodder): KEEP, but not working.** 0 fills. Others ask 21/30/30, so the gap is wide. Card value: 12.5 for LAT-07/08 (no Sunday value reading for LAT-06).
- **Trader `loop.py`: CHECK liveness.** Its last Sunday line is 00:36 "closed": no Sunday accepts and no Sunday errors. Weekend total: 2 accepts (+6.2, +15.5).
- **Maker book: under-used.** 3 open offers against the plan's 20-30. Few cards are safe to sell, though: only the LAV-04 and SAL-04 spares and LAT-01/03/04.
- **v10 / t13 pact: evidence not in the data.** No v10 fill counts reported. mm went 7.33 → 9.73 from the bench payout.

## Check the scout
- **Holds:**
  - t12 is the fastest climber (35.0, +4.0/15).
  - t13 brokers closers (SAL-10 → t09 at 68, → t03 at 108; CHA-01 → t18 at 72).
  - t03 bought MAL-07 at 9.
  - t02 is a cash buyer (RET-11 240, CHA-05 72).
  - Don't feed t12 LAT-08/MAL-03/MAL-08.
- **Stale:**
  - "Missing MAL-07, 09, 10": MAL-10 was bought at 46 (10:33).
  - "Pícaros MAL-09 at ≤ 49": a bait and switch twice, no real sale.
  - Cash 660: now 614.
  - "t18 1.2 ahead": now 0.6.
  - "t03 1.9 behind": now 2.7.
- **Wrong or contradicted:**
  - "Trade part not capped (M5)": the RET-11 sale measured 0. Note that Saturday's neg reached 119.1, so a per-round cap of 50 would be a Sunday change (t12's bug fix?). The cause is not in the data.
  - t16's CHA-09 bid is 64, not 67.
  - t10 (#2, 33.5) is missing from the scout's threat list.

## The 3 changes with the highest expected gain
1. **Duelist live before Duels III (~11:00, about 20 min away).**
   - Lucas's log says it was stopped on Aleks's machine at 09:46, and Sunday duel points read 0.0. A missed session scores 0 on the duel share of Negotiating 30.
   - Aleks runs `--status`/`--check`, then follows the escape ladder (directive 07:25 #11).
   - Risk: two copies on one key. Confirm the old one is stopped first.
2. **Flag both Pícaros bait-and-switch messages (threads 2595 and 2617).** Use `POST /api/flags` with the message whose words say MAL-09 while the structured give is MAL-07 or MAL-06.
   - Saturday paid +10 for exactly this lie type.
   - Saturday's past-cap flag scored 0, not −10, so the downside is about 0.
   - Expected +10 to +20 neg if the flag cap resets per round and neg is not capped at 50. A 0 result also answers the cap question.
   - Risk: the message_id must be the structured offer, not a posture line.
3. **Fill the empty ladder slots, highest level first.** Sunday so far has L1 ×3 (full), L2 ×0, L3 ×2 (Pilar), L4 ×2 (Pícaros), L5 ×0 (Banco's menu: not in the data). A missing deal counts 0.
   - L4: finish LAT-03 with −2/−3 steps.
   - L3: Pilar takes the LAV-04 or SAL-04 spare.
   - L2: Chato buys uncommons at 14. Raise the LAT-07/08 bids from 9 to ≤ 12 (value 12.5) so a fill gives Chato fodder.
   - Sell only at ≥ value; never a dealer's opening price.
   - Expected: about +0.02 to +0.05 ladder per slot (Saturday's L2 and L3 deals).
   - Risk: diminishing returns, and the 4-tick offer expiry ends threads if we hold silent.
