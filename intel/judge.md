# Judge (claude-opus-5-5, Sun 06:20)

## Verdict
**Holding at #3 at 30.5** (game closed since tick 1445; every Δ is 0). We trail t10 by 7.1, lead t18 by −0.8 (they are ahead by 0.8), and lead t12 by 0.1. `neg_points` has been flat at 119.1 since tick 988.

## Our strategies: keep / kill / scale
- **Team trades and swaps: SCALE.** They are the only measured board movers: swap t07 +15.5 (≈ +0.74 board), SAL-06 from t08 +40.4. Together that is 55.9 of our 119.1 `neg_points`.
- **Trading loop: KEEP, fix.** Saturday gave 2 accepts (+6.2, +15.5). Since 22:41 it has logged the error `unknown_card sobre_bienvenida` once a minute, so it is polling a card that doesn't exist. Patch it before the 09:00 restart (CASH_FLOOR=464 per log 00:40).
- **Dealer bot (ladder and fodder): KEEP at low priority, inside the 00:44 GUARDRAIL.**
  - Ladder is at 0.483, but the board did not move across ladder 0.373 → 0.437 ([L], Chief 17:45).
  - Dealer deals never add `neg_points`.
  - The last thread (LAV-04 to Pícaros, her final 4 = her opening) walked correctly: 0 loss.
- **Unpriced dealer threads (8 closed at ticks 1367-1370, egg probes): KILL as standalone threads.** Badge and egg score effect: not in the data. Eggs go inside priced messages only (directive 00:55).
- **Flags: KILL.** The cap is spent: the probe on 8507 scored 0. Net +20 total.
- **Our listings: KILL the addressed micro-asks.**
  - LAV-03 → t04 and LAV-04 → t01, both at 6. Our gain is 2.8 each, below the +3 bar in Dani's table.
  - Neither buyer is ≥ 10 below us: t01 is 4.9 below, t04 is 5.4 below.
  - Both collect LAV, so the card may close their page. They would book up to +50; we book +2.8.
  - Both lapse at tick 1455 anyway.
- **Duels: not ours.** Session 3: 8 deals and 2 no-deals in the last 10. Duel points 35.39.

## Check the scout
- **Holds:**
  - Cash 392, CHA ×1.6, the CHA fast-start order and the +50 cap.
  - Gaps: 7.1 to t10, t18 and t12 within a point.
  - Flags exhausted; TRICK guard e461e3b needs a dealer-bot restart.
  - t12's LAT×8 buys and LAV-08 at 14; t07 RET×9 buys.
  - Our RET-01/03 are page cards at 83.9: don't sell.
- **Wrong:**
  - "t10 bought RET-03 at 8 from our side": the trade at tick 1392 was t10 → t06. t10 *sold* it, and we weren't in it.
  - "t06 and t07 both chase RET": t06 *sold* RET-11, RET-10, RET-09 and RET-06. t06 is a RET supplier.
  - "+2.8 may not score as dealer-style gains": these are team trades, so the gain counts. The real problem is the feeding rule and the +3 bar, which the scout missed.
  - "Approve row #1": already APPROVED at 01:00. t09 (#16, 23.3) is no rival.
- **Unverified:** "re-list OPEN at ≥ 6". Open listing conflicts with the feeding rule for LAV collectors t01, t04 and t14 unless the card is not a page-closer for them, and that is not in the data.

## The 3 changes with the highest expected gain
1. **CHA fast start at round 3's first tick, with dealer bots restarted on e461e3b before 08:58.**
   - Pícaros CHA-09/CHA-10 with `--offer-only`, the capped public bids, then the silver pack.
   - Effect: CHA rares are worth 112 to us; the Pícaros rare median is 55, so no dealer loss. The page-closer team trade is worth up to +50.
   - Risk: print runs run out (SAL-11 9/9), and Pícaros trick offers if the restart is missed.
2. **Maker team trades and swaps as the main engine; MAL close GO once ≥ 150 P is left after CHA (directive 01:40).**
   - Our spares go on open asks on a non-rival member venue. Never a page card, never a top-4 buyer.
   - Stop the trader at T−5 before Duels III.
   - Effect: ≈ +0.05 board per `neg_point` (Sat 17:46 measurement); the MAL close is +30 `neg_points` past our cap.
   - Risk: feeding t10, t18 or t12; the loop's error fires once a minute.
3. **v10 at 09:00: RET-09 t07 → t09 first, then rows #2/#3 at 08:30-gated.**
   - Effect: +67.6 VC, likely the full real-trades share (5.0 board per directive 00:37).
   - Risk: VC is net. Tick 398 went to −5.2 when a card moved to a lower-multiplier holder, so confirm t09 is page-finishing (approved as such) before it fires.
