# Judge (claude-opus-5-5, Sat 12:42)

## Verdict
Falling behind the leaders: #7 at 26.7, +4.4 in 60 min against Team 14 +9.7 and Team 17 +10.3. We are 4.9 behind #1 and 1.2 behind #6 (Team 10, +3.1 in 15 min). `neg_points` has sat at 35.2 since tick 404 (133 ticks), so all recent gain came from the ladder and duels.

## Our strategies: keep / kill / scale
- **Dealer ladder sells (offer-only): SCALE.** Ladder went 0.055 → 0.141 with 0 neg cost: LAT-08 to Chato +0.017, MAL-07 to Pilar +0.050, SAL-08 to Pilar +0.019. Empty slots remain: one at L3 and two at L2 (only LAT-08 counts there).
- **Chato buys above list: KILL (already done).** RET-09/10/06 cost −21.5 neg and never moved the ladder. The RET page closer (+50) paid it back.
- **Page-closer team buys (RET-01 from t10 at 20 → +50.0; LAV-11 now): SCALE.** This is the only lever that has moved `neg_points` materially today.
- **LAV-11 maker bid (100, then 110 and 120, addressed to t08): KEEP.** It runs under the 12:39 GUARDRAIL. It has not filled yet, and t08's 125 ask expired at tick 540.
- **10 addressed spare asks: SHRINK.** No fills since tick 404. LAV-04 at 6 is already the cheapest of five asks (the other four are at 10), so price is not the blocker; nobody wants the cards. Each fill is worth only +3 to +6.
- **Trading loop (`loop.py`): VERIFY or KILL.** Its log shows nothing after "open" at 10:32: no Saturday accepts, so no evidence it adds anything.
- **Duelist (Aleks): KEEP.** Duel points rose 4.4 → 6.2 → 6.99 during Duels I.
- **Venue v10: HOLD.** Last read was `mm_points` −5.2. Only collector-buys there (11:31 rule).

## Check the scout
- **Holds:**
  - Team 17 and Team 14 climbing via MAL/SAL and LAT/RET buys.
  - Team 12 trading with t15 (ticks 418 and 433).
  - t06's 99 bid on LAV-09: don't sell; worth 177 to us.
  - t13's 2 P RET bids are a trap.
  - We are 1.2 behind t10.
- **Does not hold: "ladder saturating near 0.15".** The data fits closing distance above the dealer's opening, not deal count:
  - MAL-07: her opening 16, closed 19 → +0.050.
  - SAL-08: 22 → 23 → +0.019.
  - LAT-08: 13 → 14 → +0.017.
  - So the 0.15 cap is [L] with no support, and the L3 third slot is still empty.
- **Does not hold: #1, floor 17.** That breaks the 12:13 rule ("MAL-06/07 → Pilar at ≥ 18"; worth 17.5 to us). The floor stays 18.
- **Does not hold: #3, reprice spares up to 8-9.** Asks at 6 sit unfilled while rival asks at 10 also sit unfilled. Raising the price cannot fix missing demand.
- **#2, cash ≥ 200: incomplete.** It ignores the LAV-11 GUARDRAIL, which allows cash to drop to ~30 for that one trade. LAV-11 is a below-value buy, so it is consistent with "below-value buys only".

## The 3 changes with the highest expected gain
1. **Close LAV-11 now, with Dani as the push.**
   - Dani goes to Team 8 (#16) in person: "Our bid for LAV-11 is live on El Rastro, addressed to you; accept it." He points only at the live bid (100, stepping to 120).
   - Before the fill, the operator opens our unopened `sobre_plata` (value 91.1) alone in its own window. That keeps the epic cap test clean: +50 means flat cap, +114 means 5×book.
   - Gain: +50 neg ≈ +4.7 board.
   - Risk: our addressed bid shows in the public feed, so Team 14 (#1, collects LAV) may buy it first. Cash falls to ~45 and must climb back to 100 after. The effect of opening the pack on `neg_points` is not in the data.
2. **MAL-06 to Pilar for the third L3 slot.**
   - Cancel ask 7941 first, then one offer-only thread alone in its window under the 11:55 Duels I limit.
   - Descend faster from 30 so we reach 18 before her round-4 final. Walk if she finals at 17.
   - Gain: +0.017 to +0.05 ladder ≈ +0.6 to +1.6 board (at 0.33 board per 0.01), 0 neg cost.
   - Risk: second threads close lower; she may final at 17 again.
3. **Test the two empty L2 slots with a zero-cost spare.**
   - Cancel the spare's team ask first, then sell one spare common to Chato offer-only, above his opening bid. Candidates: LAV-02, LAV-03 or LAV-04 second copies (worth 3.2) or the LAT-04 second copy (worth 1.2). This fits the 12:13 rule (price ≥ value).
   - Measure the ladder change. Repeat once if it beats +0.01.
   - Gain: up to ~+0.017 each (LAT-08's rate) ≈ +0.56 board, 0 neg cost.
   - Risk: whether Chato buys commons, and at what price, is not in the data. If he doesn't, nothing is lost.
