# Judge (claude-opus-5-5, Sat 14:23)

## Verdict
Holding #5, but losing ground to the leaders: 28.1 against t14's 30.8, a 2.7 gap (2.19 at the 12:58 snapshot). We gained +1.8 over 60 min, while t10 gained +4.1 and t18 +2.2 and are now 0.7-0.8 above us. `neg_points` has been flat at 35.2 since tick 404 and the ladder flat at 0.181 since 12:45.

## Our strategies: keep / kill / scale
- **Pilar sells (L3 ladder): keep.** They gave +0.050, +0.040 and +0.019 at 0 neg. The ladder is flat only because we have no spare uncommon left to sell.
- **Chato SAL-06 buy at list 26 (directive A): kill.** His 33 → 32 against our 26 closed at tick 577. His uncommon finals are 30-31 and have never reached list.
- **Abuela SAL-06 at cap 25: scale down.**
  - SAL-06 is worth 22.5 to us (25 × 0.9), so a buy at 25 scores −2.5 neg.
  - Our L1 slots are already full (RET-08 at 22 added only +0.003). The buy's only purpose is resale to Pilar.
  - If swap 9172 fills, SAL-07 is that resale card at no cost. Then drop the SAL-06 cap to 22.
- **Trading loop: keep running, but there is no evidence it earns.** Its last 25 log lines are errors and clock events, with zero accepts.
- **Maker book (9 offers, against the plan's 20-30): keep prices and don't chase fills.**
  - The last team fill was tick 404 (+2.0); 226 ticks have passed with none.
  - Commons cleared at 5 at ticks 595-610, below our values for MAL (7) and SAL (9), so cutting to fill would lose.
- **Card-for-card swaps: scale.**
  - 9172 gains +14.3 and 9173 gains +3.8, both as maker.
  - Each one is worth 4× our best ask (≤ +3.8). Swaps are the only 0-P fill route seen in the field (t15↔t07, ticks 607-616).
- **Lunch bargain buy (GUARDRAIL 13:15): keep watching.** No qualifying hit is in the data.

## Check the scout
- **Holds:** the swap gains (LAT-04 1.2 + MAL-04 7 for SAL-07 22.5 = +14.3; LAV-02 3.2 for MAL-01 7 = +3.8); no maker fee; t15 at #14 and t07 at #17; L3 small steps beat jumps (+0.040 vs +0.019); no spare uncommons in our holdings.
- **Wrong: "SAL-06 at ≤ 25 costs 0 neg if worth ≥ 25".** It is worth 22.5, so the buy costs −2.5.
- **Wrong: "resale at 25 not in the data".** Pilar paid Team 4 25 for SAL and us 23 for SAL-08. The 18 median the scout cites is mostly MAL.
- **Wrong: Team 4's RET-06/08 bids are a threat.** Our RET page (01-10) and LAV page (01-10) are both complete. Those bids are irrelevant, since selling would break a page worth ~100 per card.
- **Wrong: "the lunch pause freezes the slip".** We went 28.6 at 13:22 → 28.1 now with the tick frozen at 630.
- **Overstated: "+0.02-0.04 per Pilar sale".** Only the best 3 count, so a new sale gains only its excess over the 0.019 slot.
- **Missed:**
  - The new levels announced at tick 630: The Workshop («Three spares. One surprise.») and Los Pícaros.
  - Every duplicate spare we own is currently on the book.
  - The unopened sobre_plata (92.9) still distorts each trade by ~1-4. The Chief already ruled on it; flagged only as noise in our measurements.

## The 3 changes with the highest expected gain
1. **Get the two swaps filled at unpause.**
   - Dani or Lucas pitch t15 (SAL-07 for LAT-04 + MAL-04) and t07 (MAL-01 for LAV-02) in the room. The Operator re-posts both if the tick passes 650.
   - Expected: about +18 neg, roughly +1.7 board at 0.094 per point.
   - Risk: the pack drag lowers the measured score; neither team is near us, so feeding risk is nil.
2. **Hold three spares for The Workshop.**
   - The Operator cancels 9101 (LAV-04), 9136 (LAV-03) and 9102 (SAL-02). With the swaps taking LAT-04 and LAV-02, exactly three duplicates stay unlisted.
   - Read the Workshop's rules at unpause before selling any of them.
   - Expected: the payoff is not in the data. The cost is at most ~11 neg (≤ 3.8 each) and only if those asks would have filled, which none has since tick 404.
   - Risk: the Workshop may be worthless. We can still sell the spares afterwards.
3. **Fill the empty L2 slots with sells to Chato at ≥ our value.**
   - Cancel 9025, then sell LAT-03 (value 5) to Chato with the offer-only flag, stepping down from above his opening bid.
   - The rule comes from 12:13: a sale above his opening bid moved LAT-08 by +0.017 at 0 neg.
   - Expected: about +0.017 ladder (≈ +0.56 board at 0.33 per 0.01) per slot, two slots open. Apply the same playbook to Los Pícaros' empty slots once they unlock.
   - Risk: whether Chato buys commons at all is not in the data. If he doesn't, we walk at zero cost.
