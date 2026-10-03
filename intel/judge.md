# Judge (claude-opus-5-5, Sat 14:39)

## Verdict
Holding, not closing the gap. We are #5 at 28.1: +1.8 over 60 min against the leader's +1.1, but −0.8 over the last 15 min. The gap is 2.7 to t14, 0.7 to #4, and only 0.3 above t17 at #6. `neg_points` has been 35.2 since tick 404, and ladder 0.181 since 12:45.

## Our strategies: keep / kill / scale
- **Pilar sells (L3 ladder): keep.** Our 3 L3 deals gave +0.050, +0.040 and +0.019 at zero neg cost. The weakest slot is SAL-08 (+0.019), so the next sale only has to beat that.
- **SAL-06 buy (Abuela and Chato): demote.** Three threads produced no deal: Chato 33→32 vs our 26, Abuela 29→25, Abuela 29 vs 21 now open. Even at the cap of 25 it costs −2.5 neg. Run it only if swap 9172 fails (see change 1).
- **Chato L2 at list 26 (12:58 plan A): not happening.** Chato stood at 32 against our 26. No L2 slot gained since 12:10.
- **Maker book of spares (9 asks): hold, then partly pull.** No team fill since tick 404, about 226 ticks. Each spare is worth 1.2-3.2 to us, so the upside is about +4 each, about 0.4 board.
- **Swaps 9172/9173: scale.** 9172 is +14.3 and 9173 is +3.8, both with teams outside the top 5 (#14, #17). The best-priced item on our book.
- **trader `loop.py`: keep running, no evidence of value.** The log shows only errors and pause events; no accepted fills are logged.
- **Bargain watch (13:15 GUARDRAIL): keep.** No hits logged. The only live high bid is t04's 64 for LAT-09, which we don't hold.
- **Unopened `sobre_plata` (92.9): open question.** GAME.md [L] says open packs before trading because each trade's score shifts 1-4. That drag will cut the swaps' +14.3/+3.8. The Chief's reason for keeping it closed is not in the data.

## Check the scout
- **Holds:**
  - Score gaps 2.7 / 1.5 / 0.7.
  - Bid 9168 at 21 vs Abuela 29.
  - Swap gains +14.3/+3.8, and t15↔t07 swapping at ticks 607/613/616.
  - Team 13 unlocked level 3 with 3 Chato deals.
  - RET-09 Team 6→t02 at 84 (tick 504); Team 18 paid 86.
  - t04's bids of 27/26 on RET-08/06.
  - Team 6 +4.6/60 min.
- **Wrong:**
  - "Team 10 sells MAL-10 from Team 3 for 74": Team 10 *bought* it.
  - "Cost ≈ −0.33 neg" for SAL-06 at 25: it is −2.5 `neg_points` (25 − 22.5), about −0.24 board at 0.094.
  - "+1.2 board per Lucas 12:58": that figure was for L2 Chato slots at list 26. An Abuela buy is L1, which already holds 3+ deals; the value is only the L3 resale.
- **Unsupported:**
  - "Team 14's ~22 listings via the Abuela route": not in the data.
  - "Pícaros = L4 with head start for 3 Pilar deals": the unlock rule is not in the data.

## The 3 changes with the highest expected gain
1. **Get SAL-07 by swap, then sell it to Pilar at ≥ 25. Drop the SAL-06 buy if the swap fills.**
   - Have Dani nudge t15 and t07 in the room now. Re-list 9172/9173 with `expires_in_ticks` doubled if they lapse at 650.
   - Then sell SAL-07 to Pilar: offer-only, steps of −2/−3 from about 30, never jumping to her bid. A sale at ≥ our value 22.5 costs 0 neg.
   - Effect: +14.3 neg (≈ +1.3 board). Replacing the 0.019 L3 slot with a MAL-06-style ~0.040 adds ≈ +0.7 board. Total ≈ +2, with no −2.5 Abuela cost.
   - Risk: t15 never accepts. In that case fall back to SAL-06 from Abuela at ≤ 25.
2. **Pícaros at resume: one measured deal first.**
   - First thread: a sell at ≥ our value, offer-only, never at their opening price, alone in its measurement window.
   - Read Δladder and Δneg before a second deal.
   - Effect: the ladder moves about +0.33 board per +0.01. A higher level weighed ~3× the one below at L3, so the upside is unknown but likely the biggest left today.
   - Risk: the unlock rule and what Pícaros buys are not in the data. Never offer page cards (RET/LAV are all page-bonused).
3. **Keep 3 spares off the book until the Workshop ("Three spares. One surprise.") posts its menu.**
   - Pull asks 9101 (LAV-04) and 9136 (LAV-03), and keep LAV-02's 2nd copy unless swap 9173 fills.
   - Cost: under about 0.4 board of foregone fills on asks unfilled for 200+ ticks.
   - Effect: preserves the option on a new level or ladder slot.
   - Risk: the Workshop does not use spares the way the teaser suggests. In that case re-list at the same prices after its menu appears.
