# Judge (claude-opus-5-5, Sun 07:22)

## Verdict
Holding at #3 (30.49): 0.8 behind #2 Team 18, 0.1 ahead of #4 Team 12, and 7.1 behind Team 10. `neg_points` has sat at 119.1 since tick 988, so 457 ticks of Saturday evening added nothing while Team 18 rose +0.8.

## Our strategies: keep / kill / scale
- **Dealer bot: keep for CHA only; kill ladder-only threads.** Its last thread (LAV-04 to the Pícaros) walked at her 4 against our floor, with `neg_points` and ladder flat. Ladder rose 0.437 → 0.483 with a flat board [L, Chief 17:45]. CHA rares (worth 112) at Pícaros ≤ 62 cost nothing in `neg_points` and build the page.
- **Trading loop: keep and fix.** Its only scoring actions were 2 swaps (+6.2 at 15:48, +15.5 at 17:46). Since then it logged:
  - 5 `unknown_card sobre_bienvenida` errors in 4 min (22:41-22:45);
  - DNS failures at 22:55-23:24.
- **Our bids and listings: correctly empty (0 open).** LAV asks 19979/19981 were cancelled per the 07:25 directive. Nothing is unfilled.
- **Team trades (pages): scale.** Every large gain came from team trades: SAL close +40.4, t07 swap +15.5, RET cap test +50.
- **Flags: dead.** The cap was reached; flag 8 scored 0 after an hour.
- **Club / v10 trades: cannot judge.** `mm_points` are not in the live metrics.
- **Duels (Aleks): not ours to change.** Score 35.39 over 136 duels; 2 of the last 10 ended no_deal (6177, 6182).

## Check the scout
- **Holds:**
  - t12 is 0.1 behind us; t18 is +0.8 per ~30 ticks (teams.md).
  - RET-10 sold t06 → t04 at 84 and t06 → t07 at 77; t01 bids 152 for MAL-11.
  - Our RET page is complete (RET-01..11 held).
  - Pícaros rare median 55 (n=1).
- **Wrong / stale:**
  - It says the LAV-03/04 asks are live until tick 1455. They were cancelled at 07:15, metrics show 0 open offers, and directive 07:25 (4) sends LAV-04 to the Pícaros and LAV-02×2 + LAV-03 to the Workshop. Drop its action 2.
  - It cites t0 pid 92570; t0 is now pid 22755.
  - It credits the +15.5 at tick 904 to the Pícaros SAL-09/10 buys at 54. That +15.5 is the t07 swap (trader log). Dealer gains clip to 0.
- **Unflagged risk:** it notes CASH_FLOOR=464 against cash of 392 without seeing the problem. Any floor above our cash blocks every buy (change 1).

## The 3 changes with the highest expected gain
1. **Confirm t0 starts the trader and opps on `run/floors.env` 110/110, not CASH_FLOOR=464.**
   - Why: the 07:06 and 07:05 lines say 464. Directive 07:25 (6) replaced it with ≈ 100-120, and the operator wrote 110/110 at 07:15. With cash at 392, a 464 floor freezes every buy until the grant arrives.
   - How: the operator greps t0.sh before 08:45.
   - Effect: restores the only automated scorer, which earned +6.2 and +15.5 per swap.
   - Risk: spending into the CHA budget. The floor already reserves the planned spend.
2. **Run the CHA closer exactly as directed.**
   - Plan: open `sobre_plata` (71.6) plus the grant pack before the closer. Then buy the last CHA card from a non-rival team, addressed on El Rastro, with the seller's fee added.
   - Effect: up to +50 `neg_points`, the cap. The CHA page bonus is 106. Measured analog: SAL close +40.4, held below 50 by pack drag.
   - Risk: t10 or t01 hold the last copies (the watcher drops those bids). Print runs may run out (SAL-11 9/9), so keep the closer a common.
3. **Fix the trader's `sobre_bienvenida` lookup and add a DNS/network check before R.**
   - Why: the repeated errors burn the shared 5 req/s key, which ran at 73-92% load with everything on. That load hits Duels III and the Final.
   - Effect: protects the 35.39 duel score and the trader's accept window.
   - Risk: a code change before the open. Run the existing tests (528 green) and restart only via t0.
