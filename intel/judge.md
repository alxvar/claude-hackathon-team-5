# Judge (claude-opus-5-5, Sat 09:56)

## Verdict
**Falling behind.** We are 15.29 (#6), −4.7 over 60 min. Leader Team 12 is 32.2, +4.3 over 60 min, so the gap widened by about 9 to 16.9. #3 (Team 14, 17.2) is only 1.9 ahead. Our only Saturday score is `neg_points` −10.0 (RET-09 bought from Chato at 87).

## Our strategies: keep / kill / scale
- **Chato steady-step (RET rares): keep.** RET-09 landed exactly as predicted (−10.0). RET-10 is running (his 97→97→96, ours 57→60→63, cap 88). He is the only RET rare source, since no team pulled or asked one.
- **Abuela ladder bot: keep, but only for RET needs.** 3 deals moved the ladder 0 → 0.048 at 0 `neg_points`. With best-3 per level, a 4th level-1 deal at 9 adds nothing unless it closes cheaper.
- **Chato for ladder: kill as a standalone.** That is 4 Chato deals with 0 ladder movement. Only buy from him for cards we need (directive: 3 RET uncommons, cap 28).
- **Trading loop: keep, verify it is alive.** No Saturday entries in its log since the 09:55 restart; the last lines are Friday errors.
- **Maker book: scale and reprice.** 14 offers against the plan's 20-30, 0 fills in 17+ min.
  - Our spares at 10 compete with public asks at 9 (LAV-03 ×2) and 10 (LAV-04 ×3).
  - Addressed offers are visible only to their addressee.
- **Swaps 3245/3246: keep.** SAL-03+SAL-05 (18) → RET-07 (27.5) is +9.5; MAL-02+MAL-04 (14) → RET-08 (27.5) is +13.5. Whether t16/t07 hold those cards: not in data.
- **In-room trades (Dani): no evidence of any today.** teams.md lists no buyer that passes the feeding rule.
- **Ignoring t03's 64 bid for LAV-09 (worth 177): correct.**

## Check the scout
- **Holds:**
  - Team 2 bids low for RET rares (13, 15) and RET-04 (7).
  - Our book is unfilled.
  - The venue bond and the RET page competed for cash (now settled by the 09:55 GUARDRAIL).
- **Wrong, #2:** the "0 P" offers are card-for-card swaps; the metrics renderer hides the `want`. Cancelling them throws away +9.5 / +13.5.
- **Wrong, #3:**
  - RET-02 is already held.
  - RET-06/07/08 are uncommons (Abuela opened RET-08 at 29), not commons.
  - RET-01 is reserved for the cap test at ~20; a bid at 6 breaks the test's separation.
  - Last RET team trade: 12, not 2-7.
- **Wrong, #1 (partly):**
  - SAL-08 has already moved to t16 (offer 3536).
  - t16 is 9.2 below us, not 10.5.
  - "+12 if t16 accepts" is wrong: as maker we gain 33 − 22.5 = +10.5; the fee is theirs.
  - Even if SAL-08 completes t16's page, t16 stays below us (6.1 + ≤8). Acceptable.
- **Stale:** cash 384 / floor 370 / ladder 0.032. Now 288 / 100 / 0.048.
- **Wrong:** "Team 2 the only climber". Team 12 is +7.4 over 15 min.

## The 3 changes with the highest expected gain
1. **Finish RET within cash, in order, before Duels I (tick ~309, ~49 min).** Order: RET-10 (cap 88) → 3 Chato uncommons (cap 28) → RET-01 from a team at ≈20 as the last card.
   - Cash math: 288 − 88 − 84 − 22 = 94, below the 100 floor. Start the third uncommon only after a maker sale adds ≥ 6 P.
   - Effect: plan estimate +24 to +45 `neg_points` (≈ +4 to +7 board) if the ~50 cap and the page bonus via a team trade hold. It also gives the level-3 early start.
   - Risk: the cap form ([L], n=1). The accept arbiter may freeze accepts during Duels I.
2. **Reprice and widen the maker book now (directive: reprice after 10 min unfilled).**
   - Spares (worth 3.2): reprice the 10 asks to 9 and add more of them, addressed only to teams outside the top 4.
   - Keep the SAL-08 and MAL-06/07 asks (+10.5 and +8.5 each, fee-free as maker); they fund change 1.
   - Post RET-01 as a public bid at ~20, ≤20 ticks, only once it is the last card.
   - Risk: a page-completer reaching a team only 6-9 below us (t01, t07, t09, t15). Their gain then exceeds ours, but none of them overtakes us.
3. **Builder: show `want` for swaps in metrics, and timestamp the scout's inputs.**
   - Effect: prevents cancelling +23 of live swaps, and stops recommendations built on stale cash, floor and ladder numbers.
   - Risk: none to the game; it costs Builder time before Duels I.
