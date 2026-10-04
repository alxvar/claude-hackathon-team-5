# Judge (claude-opus-5-5, Sun 02:12)

## Verdict
**Holding at #3**: 30.49, 0.8 behind Team 18 (31.3), 0.1 ahead of Team 12 (30.4), and 7.1 behind Team 10 (37.6). Every team is flat over 60 min because the game is closed. At about 0.05 board per neg_point (Sat 17:46), roughly +16 neg_points passes Team 18.

## Our strategies: keep / kill / scale
- **Team-trade page closes: SCALE.** SAL-06 from t08 at 28 scored +40.4 (tick 988), our largest gain of the day. Earlier, RET-01 hit the +50 cap.
- **Card-for-card swaps (trader accepts): KEEP.** t07 SAL-07/LAT-01 gave +15.5 and t08 SAL-04/RET-04 gave +6.2. These were the loop's only accepts since 15:48; no fills since 17:46.
- **Trading loop process: FIX.** It logged "no card sobre_bienvenida" every minute (22:41-22:45), spending the shared 5 req/s on nothing. Find the source and drop it before 09:00.
- **Addressed spare asks (LAV-03 → t04, LAV-04 → t01 at 6): KILL.** Addressed asks fill at 0.3% vs 3.5% for open asks (directive 00:37). Our 414 listings produced 17 team trades.
- **Dealer threads: KEEP, narrowly.**
  - The 8 threads at ticks 1367-1370 closed with no price from us.
  - The Pícaros LAV-04 thread walked correctly at her opening of 4.
  - Ladder rose 0.437 → 0.483, but `negotiating` stayed flat across ladder 0.373 → 0.437 (Chief 17:45, [L]).
  - Run only the approved fodder (≤ 3 per level) and CHA threads. No more empty probes.
- **Flags: DONE.** Net +20; the 17:43 probe scored 0.
- **Duels**: not ours to judge.

## Check the scout
- **Holds:**
  - Team 18 +0.8/30 ticks; LAT-10 t13→t18 at 72.
  - MAL-11 t08→t10 at 195; RET-10 t06→t04 at 84; RET-11 at 216.
  - Open asks beat addressed ones.
  - The trick guard is shipped (e461e3b) and needs a bot restart.
  - t09 is ~7.2 below us.
- **Fails, #2:** "rares worth 112 vs ~54, buying below value scores" is wrong.
  - Dealer gains clip to 0 [V].
  - The tick-904 +15.5 was the t07 swap (trader log expected_gain 15.5), not the Pícaros buys.
  - The +40.4 precedent was a TEAM trade.
  - Dealer CHA buys only set up the close.
- **Fails, #3:** "Team 7 sold RET-06 at 30" is wrong. Tick 1417 is t06→t07, so t07 bought it.
- **Fails, RET-06 bid:** bidding for RET-06 is pointless. We hold RET-06 and every RET card (values include the page bonus).
- **#1 unchecked feeding rule:** t01 (25.8) and t04 (25.1) both collect LAV and are < 10 below us. Whether LAV-03/04 close their pages is not in the data.

## The 3 changes with the highest expected gain
1. **Build CHA so the LAST card comes from a team** (directive 00:46: one agreed, addressed post from a non-rival).
   - Before the close: open the silver pack (71.6 of drag) right after the CHA release. Buy the other CHA cards from Pícaros/dealers only at ≤ value (score 0, no loss).
   - Effect: up to +50 neg (≈ +2.5 board), enough to pass Team 18.
   - Risk: print runs sell out (SAL-11 9/9), and t10 flips visible bids. Keep bids capped and short-lived.
2. **Turn spares into maker sales, open asks on a non-rival member venue at 09:00.**
   - Cards: LAV-02 ×2 spare (1.3), LAV-03/04 spares (3.2), and MAL/LAT commons not needed for the MAL close. LAT-03/04 are worth 5.
   - Price at the common clearing price of 9: about +4-8 each with no fee as maker.
   - Effect: +15-30 neg, which also funds CHA.
   - Risk: a spare that closes a rival's page. Check the buyer and the feeding rule before any addressed sale.
3. **Dani sets up WhatsApp swaps: our low-value spares for CHA cards or MAL-07 from teams ≥ 10 below us.**
   - Swaps were our second-best lever (+15.5, +6.2) and save cash for the MAL GO (≥ 150 P after CHA).
   - Risk: a swap's value to the counterparty feeds a top-4 team. Never swap with t10, t18, t12 or t03.
