# Judge (claude-opus-5-5, Sun 03:14)

## Verdict
**Holding at #3, unverified.** Score 30.49, flat over 15 and 60 min because the game is closed. We trail Team 10 (37.6) by 7.1 and Team 18 (31.3) by 0.8. Team 12 is 0.1 behind at 30.4. `neg_points` has sat at 119.1 since tick 988.

## Our strategies: keep / kill / scale
- **Team trades (page closes, swaps): SCALE.** These are our only live neg lever.
  - SAL-06 from t08 at 28 gave +40.4 (tick 988).
  - The t07 swap gave +15.5 and the t08 swap +6.2.
  - Nothing has scored since tick 988.
- **Dealer bot / ladder fodder: KEEP, but only inside GUARDRAIL 00:44.**
  - The ladder rose 0.437 → 0.483, but `negotiating` stayed flat from 0.373 to 0.437 (Chief 17:45, [L]), so the board gain is unproven.
  - The Pícaros LAV-04 walk at a final of 4, against a floor of 4 and value 3.2, was correct: no loss.
- **Trading loop: KEEP, sells-only.**
  - Its last accept was at 17:46. Since then its log shows only errors: `unknown_card sobre_bienvenida` once a minute, then DNS failures.
  - Cash is 392, below the planned `CASH_FLOOR=464`, so it cannot buy anyway.
- **Addressed spare asks (19979 LAV-03 → t04, 19981 LAV-04 → t01, at 6): KILL.**
  - Addressed asks fill at 0.3% vs 3.5% for open ones (directive 00:37).
  - Both buyers collect LAV and sit only 4.9-5.4 below us, so they fail the "≥ 10 below" feeding rule if the card closes a page. Whether it would is not in the data.
- **Flags: DONE.** Net +20; the cap was confirmed at 17:43.
- **Duels:** 35.39. This is Aleks's lane, not ours to run.

## Check the scout
**Holds:**
- CHA fast start via Pícaros with `--offer-only`; rare value 112 (70 × 1.6); public bid cap 54.
- Spare gains of about +5-8 as maker: LAV-02 is worth 1.3 and LAV-03/04 3.2, against prices of 9-10.
- Team 18 Δ +0.8; ≈ +0.05 board per `neg_point`; the ladder and flags are spent.

**Wrong:**
- "Pilar sold MAL-09 at 56 to us": the metrics show **we sold** MAL-09 to Pilar at 56 (tick 904).
- "t07, t04 and t16 are low enough to receive cards": only t07 (20.2) is ≥ 10 below us. t04 (25.1) and t16 (23.7) are not, and teams.md marks both "no page closers".
- "Open asks on v10": directive 00:37 puts our own spares on a **non-rival member's** venue, because our own trades never count as v10 VC.
- "Don't sell to t10/t12/t18" contradicts open asks, which anyone can take.

**Missing:**
- MAL needs MAL-07, MAL-09 and MAL-10 (we sold MAL-09).
- The scout ignores the cash maths. 392 − CHA case C (282) = 110, below the 150 MAL gate. Case A (242) leaves exactly 150.
- 00:46 and 00:40 give different CHA case-B costs (250 vs 288). Which figure is current is not in the data.

## The 3 changes with the highest expected gain
1. **Run the CHA close at 09:00 as directed, and buy the LAST CHA card from a team.**
   - Page bonus 66.25 × 1.6 = 106, which scores only through a team trade. The cap is 50, so expect ≈ +50 np ≈ +2.5 board.
   - Before 09:00, confirm the dealer bots were restarted on e461e3b (the trick guard).
   - Risk: a Pícaros bait-and-switch, or print runs selling out to faster rivals.
2. **Fund the MAL go before 10:00. The 01:40 gate needs ≥ 150 P after CHA.**
   - Post open maker asks at 9 (under the rival LAV-02 ask at 10) on a non-rival member's venue: LAV-02 ×3, one LAV-03, one LAV-04, LAT-03, LAT-04.
   - Never sell the MAL commons.
   - Expected: about +5-8 np per fill, and the MAL close's +30 np past our cap (directive).
   - Risk: an open ask completes a top-4 team's page. Team 10 collects LAV. Check its LAV gaps first; if unknown, hold the LAV spares.
3. **Fix the trader before its 09:00 restart and re-check the cash floor.**
   - Fix the `sobre_bienvenida` lookup (it errors every minute) and confirm DNS/API reachability.
   - Set `CASH_FLOOR` from the actual CHA case, not 464, which already exceeds our 392 cash.
   - Follow 01:30: stop trader, swaps and opps at T−5 before Duels III.
   - Expected: no missed fills in the 09:00-11:00 accept window.
   - Risk: a wrong floor lets the loop spend CHA/MAL cash. The `--exclude 'CHA-*,MAL-*'` setting limits that.
