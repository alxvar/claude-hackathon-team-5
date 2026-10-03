# Judge (claude-opus-5-5, Sat 19:34)

## Verdict
Falling behind the top two: 31.9, #3. t10 is at 33.8 (+5.4/60 min) and t6 at 32.9 (+1.2), while we sit at −0.0/60 min. The gap to #1 widened from 1.4 (19:28) to 1.9. `neg_points` has been flat at 119.1 since tick 988 (~124 ticks).

## Our strategies: keep / kill / scale
- **Dealer bot:** KILL. The ladder is capped (negotiating flat across 0.373 → 0.437), dealer gains clip to 0, and the last thread (Picaros LAV-04, 19:04) walked at 119.1 → 119.1.
- **Trading loop:** KEEP until the 20:25 Duels II stop. Last fills: swap +6.2 (15:48) and +15.5 (17:46), with 0 accepts since.
- **Spare-sale book (7 asks):** RETARGET. It has had 0 fills since tick 988, and its prices (6-9 on commons) earn +2 to +4 neg at best (≈0.1-0.2 board each).
- **MAL-04 ask (16545, to t02 at 27):** t02 is 9.3 below us, which fails the ≥10 feeding rule if MAL-04 closes t02's page. Fix: cancel it, or re-post at ≤12 (others' MAL asks sit at 12).
- **In-room team trades:** SCALE. They produced our two biggest gains of the day: SAL-06 close +40.4 (tick 988) and the t07 swap +15.5 (tick 904).
- **Flags:** KILL, already done. Net +20, and the 17:43 probe scored 0.
- **DENY line:** KEEP ARMED, no trigger in the data. The live RET-09 bids are from t07 (#16) and t09 (#17), not top-3 rivals.
- **v10 / market:** SCALE. It is the stated decisive lever: our market is 7.5 vs 9.15-12.5 for rivals (17:50), and one positive-value trade measured +4.99 at tick 311.
- **Duels:** KEEP. 68 finished, duel score 13.93; the board-point weight is not in the data.

## Check the scout
- **Holds:**
  - Don't sell RET-09/10: worth 149.9 each vs bids of 59/51.
  - Neg flat at 119.1, and ladder and flags spent.
  - t18's rise is "not in the data".
  - DENY has no trigger.
- **Wrong or unsupported:**
  - "t10's climb comes from team trades and the t01 alliance": its only visible trade in the window is RET-03 at 12 (tick 1033). The source of +5.4/60 min is not in the data; a market/venue gain is more consistent with our measurements than trades.
  - "Chato rare median 29 is a price rivals can use": that line is a team *selling* to Chato, not a price anyone can buy at.
  - "If t07/t09 get RET-09 they gain on us" is noise: they are #16/#17.
  - Stale numbers: t10 has 47 deals, not 45; we are 1.9 behind t10, not 1.4, and 1.5 ahead of t14, not 0.5.

## The 3 changes with the highest expected gain
1. **Push v10 trades before 20:25, when the v10 ad job stops.**
   - Action: Dani gets non-rival sellers to list on v10, with buyers of higher multiplier (collectors per teams.md: t07/t09/t16/t02 for RET) accepting. Rebate per the 19:40 GUARDRAIL.
   - Settlement: settle the rebate on our fee-0 venue against a card we lack, so the settlement nets ≈0 instead of ≈−15 neg (the Operator's concern). One candidate: MAL-06/07, worth 17.5 to us; t04 bids MAL-06 at 19.
   - Effect: market 7.5 → ~12.5, i.e. up to +5 board (measured once).
   - Risk: a card moving to a lower-multiplier holder makes the value created negative (tick 398: −5.2). Vet each pair with the radar first.
2. **Re-price LAV spares as page-closers to t07 (21.8, 10.1 below us; buys LAV×7).**
   - Action: post our spare LAV-02/03/04 (worth 1.3/3.2/3.2) as maker asks addressed to t07 at 35-40, after Dani confirms in person which LAV card t07 lacks. Cancel 16601/16654 for those cards.
   - Effect: each fill scores ≈ +32 to +38 neg ≈ +1.5 to +1.8 board at the measured 0.048/np.
   - Risk: t07's missing card is not in the data. If t07 doesn't need it, there is no fill, and t07 is 0.1 above the feeding line, so re-check its score before posting.
3. **Duels II days decision before ~20:33.**
   - Action: Aleks merges or rejects PLAN #24 (`duelist-days-read`) and sets DAYS_READ explicitly. Today it is "auto", untested on a live `days` payload.
   - Effect: protects the duel score (13.93 so far) across 68 duels; the board weight is not in the data.
   - Risk: a wrong days reading flips value on every package. Run the 439 tests plus one dry payload before the start.
