# Judge (claude-opus-5-5, Sun 06:51)

## Verdict
**Holding, not gaining.** We are #3 at 30.5, 7.1 behind Team 10 (37.6), 0.8 behind Team 18 (31.3) and 0.1 ahead of Team 12 (30.4). `neg_points` has not moved from 119.1 since tick 988, about 450 ticks of play. The game has been closed since tick 1445.

## Our strategies: keep / kill / scale
- **Team trades: SCALE.** Every gain since tick 632 came from a team trade or a flag:
  - t07 swap, tick 904: +15.5.
  - SAL close from t08, tick 988: +40.4.
  - Nothing has landed since. Team trades are the live lever.
- **Flags: DONE.** The net is +20. Flag 8 at tick ~904+ scored 0, so the cap does not reset hourly. The 00:55 directive says flag again only if the cap reset on Sunday, so test one verified lie first.
- **Dealer bot: KEEP, but only for CHA buys at ≤ our value and the approved fodder.**
  - The Pícaros LAV-04 thread walked correctly: her final 4 equalled her opening price, and `neg_points`/ladder stayed flat.
  - The threads at ticks 1367-1370 closed without a price (egg probes, which got MAL-06 + Castizo). They cost nothing.
  - The ladder rose from 0.437 to 0.483, but the board is [L] flat on ladder moves.
- **Trading loop: KEEP, fix it.**
  - Only 2 accepts on Saturday (+6.2, +15.5).
  - It errored on `unknown_card sobre_bienvenida` every minute (a bad book entry), plus DNS errors at 22:55 and 23:24.
- **Our listings: CHANGE THE FORM.**
  - 414 listings and few fills. Only 2 offers are live, and both are addressed (0.3% fill vs 3.5% for open asks, per 00:37).
  - 19979 (LAV-03 → t04) and 19981 (LAV-04 → t01) are fine at +2.8 each only if neither card closes a LAV page:
    - t04 collects LAV and sits 5.4 below us; t01 sits 4.9 below. Neither is ≥ 10 below.
    - Whether either card is their last LAV card is not in the data.
- **In-room trades (club, v10 and v26): KEEP.** The MAL-07 bid to t15 on v26 and the 09:00 v10 list are queued. No fills are measured yet.

## Check the scout
- **Holds:**
  - The game is closed and the metrics are frozen.
  - Team 12 is 0.1 behind us.
  - Team 12 paid 216 for RET-11.
  - RET-11 goes to Pilar only at ≥ 198.
  - Pícaros print runs are scarce, so fire at the first tick of round 3.
  - Team 16's bids 20217 and 20219 exist.
- **Wrong:**
  - "v10 is a leader venue… keep spares off v10": v10 is **our** venue. GAME.md has our `mm_points` moving on v10 trades, and the 00:35 directive sets a v10 real-trades target. The conclusion (our own trades don't count as v10 VC) is right; the reason is wrong.
  - "Team 10 sells epics… MAL-11 to t10 for 195": that was t08 → t10, so Team 10 **bought** it.
  - "Clipped maker gains are small": team-trade gains are not clipped. Only dealer gains are.
  - "Feeding is not an issue, not top 4": the rule is ≥ 10 points below us. t04 and t01 fail it if the card is a page-closer.
- **Unsupported:**
  - "54 public-bid cap" for CHA rares is not in the data. 54 was Pícaros's SAL rare price.
  - The MAL-07 holder IS in the data (t15, Lucas 06:43). Its price is not.
- **Misattributed:** RET-09 t07 → t09 is approved outright. The 08:30 rivals check applies to rows #5 and #6 (t16), not to it.

## The 3 changes with the highest expected gain
1. **Treat Sunday as a fresh round and front-load the CHA start.**
   - Round 2 reset `neg_points` and the ladder to 0 at its start [V]. Expect round 3 to do the same, so 119.1 likely won't carry.
   - At tick 1 of round 3, the Operator runs the Pícaros CHA-09/10 threads on `--offer-only`. Confirm the dealer bots were restarted on e461e3b (trick guard).
   - Open `sobre_plata` (71.6, pack drag) right after the CHA release.
   - Effect: CHA values 1.6× (rare 112). A dealer buy at ≤ 112 costs 0 `neg_points` and sets up the page close.
   - Risks: a trick card, and print runs selling out.
2. **Fire the v10 list at 09:00, RET-09 t07 → t09 first.**
   - Expected effect: +67.6 VC on our venue. Per 00:35, that likely fills the whole real-trades target (+5.0 board max).
   - Hosting it does not feed a leader: neither t07 (#17) nor t09 (#16) is a rival.
   - Risk: a negative-VC trade on v10, as at tick 398 (−5.2). Only pre-agreed club pairs go on v10.
3. **Close MAL with team trades, and repair the trader.**
   - MAL close:
     - Settle MAL-07 from t15 on v26 as soon as ≥ 150 P remains after the CHA buys (01:40 directive).
     - Cash is 392 now; the round grant is not yet confirmed.
     - Expected: ≈ +30 `neg_points`, at ≈ 0.05 board per point [V Sat].
   - Trader:
     - Remove `sobre_bienvenida` from the book.
     - Start at 09:00 with `--cash-floor 9999`.
     - Re-post non-agreed spares as OPEN asks on a non-rival member venue.
     - Before re-posting LAV-03/04 to t04/t01, check they are not those teams' last LAV card.
   - Risks:
     - Paying the taker fee if we accept instead of making.
     - Feeding a page-closer to a team that fails the ≥ 10-below rule.
