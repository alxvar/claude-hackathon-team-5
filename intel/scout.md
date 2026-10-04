# Scout (claude-sonnet-5-5, Sun 07:14)

## Top 3 actions now
1. **Keep the trader off rival venues; start only via t0 at R+10 (operator).**
   - Evidence: the game is closed until Sun 09:00 (tick 1445, "offers stay open; the clock stops"). We are #3 at 30.5, with t12 at 30.4 and t18 at 31.3. The gap to #2 is 0.8.
   - Directives: t0 (pid 92570) is armed. run/trader_ok exists. CASH_FLOOR=464, with cash at 392.
   - Effect: this protects the neg_points of 119.1. It adds nothing new.
   - Confidence: high.
2. **Add no new sales to t12, t18 or t10. Send the spare LAV-03/LAV-04 asks (6 P, addressed to t04/t01, expire tick 1455) only to non-top-4 teams (operator).**
   - Evidence: t04 (#11, 25.1) and t01 (#9, 25.8) are both below us by more than 10. t04 collects LAV/RET and t01 collects LAV/SAL/MAL. Rival profiles list no buyer above our value + 3.
   - Effect: the spares are worth 3.2 each to us, so the gain is about +2.8 each, minus the maker fee of 0. Small, but it adds neg_points.
   - Confidence: med. Both offers expire at tick 1455 and the clock is stopped, so they stay live until the game reopens. Re-list them if they lapse.
3. **Sunday CHA close: keep it addressed on El Rastro with the seller's fee added (per the 07:25 GUARDRAIL), and Pícaros rare asks ≤ 60 → 62 (operator, t0 chain).**
   - Evidence: the Pícaros picaros-rare median is 55 (Sat). Their rare list is 63. The directive cites finals of 55-60. Earlier Pícaros buys: SAL-09/10 at 54, scoring +15.5 in the tick-904 window together with other deals.
   - Effect: a closer is capped at about +50 per trade. A CHA rare is worth about 112 to us at 1.6×.
   - Confidence: med.

## What the climbing teams are doing
- **Team 18 (#2, 31.3, +0.8 per ~30 ticks) collects RET/LAT.** It bought LAT-10 from t13 at 72 (tick 1332), below the 86 that t12 paid at tick 1304. It is buying rares near 72 while dumping LAV/MAL.
- **Team 16 (#14, +0.3) buys RET.** It is the only other riser. Its prices are low (c 4, u 14, r 50) and it lists 796 offers. The feed shows no completed page from it.
- **Team 12 (#3 or #4, +0.4) bought the RET-11 epic from t6 at 216 (tick 1245) and LAT-10 at 86, LAT-06 at 20, LAV-08 at 14 (tick 1420).** Its 29 team trades come as buyer on collected sets. t12 is one of the teams we must not feed.
- **Team 10 (#1, 37.6) is flat.** It sold MAL-06 at 20 to t09 (tick 1230) and an epic at 207 to t17. It has 467 listings.

## Threats
- **t12 is 0.1 behind us (30.4 vs 30.5) and bought RET-11 at 216.** It is also buying LAT/MAL/RET. Any card we sell it moves the ranking. LAV-08 went t8→t12 at 14.
- **RET rare competition.** t07 and t04 both took RET-10 from t06 (77 and 84), and t06 sold at 84. t16 bids RET-06 at 18, and t09/t13 are also in. Our RET page is already complete, so this is mostly relevant if we sell. The CHA rares will face the same bidding competition (t01 bids 152 for MAL-11).
- **Feeding v10 (#1, 37.6).** Club deals send 2 of every 3 deals to v10, as decided. This raises the top-3 mean against us. That is a directive, so no change, but watch that mm_points does not go negative (it fell −5.2 on tick 398).
