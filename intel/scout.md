# Scout (claude-sonnet-5-5, Sat 11:04)

## Top 3 actions now

1. **Hold the line during Duels I (stop accepts from 11:50; trader stop job already queued).** Operator verifies the background job fires and that book.py stays maker-only. Evidence: 34 duels finished, 0 live, Duels I opens at 11:30 and the accept is shared per tick (directive 10:35). A missed duel deal scores 0, while trader accepts gain only +1.9 to +7.7 each. Effect: protects the duel share, which is the only big neg source left, since RET is done at +28.5. Confidence: high.

2. **Keep the 16 addressed asks, but re-check the buyer against the top 4 at the 11:03 snapshot before each repost.** Top 4 is now t13, t18, t5 (us), t2. t12 is #5, so it is not blocked by the rank rule but it is 1.5 below us. Cards stay addressed:
   - MAL-06 → t17 at 21 (4722/5053 family).
   - MAL-07 → t01 at 21.
   - SAL-08 → t03 at 25.
   - LAT-08 → t15 at 18.
   Evidence: t01 bought MAL-07 at 14, MAL-06 at 20 and SAL-07 at 23 (ticks 311-321), so it is buying uncommons at 14-23. Our MAL-06/07 are worth 17.5 each, so 21 yields about +3.5 each. Cut to 19-20 if unfilled by tick ~370, since 14-20 is the filled range. Executor: book.py with MIN_GAIN_SELL=2. Confidence: med.

3. **Bid for RET-10-class rares from teams only; do not buy any more from Chato.** There are no extra RET cards needed: we hold RET-01 to RET-10. The RET spares have no value to us except as 2nd copies (25%), so no action is needed there. Instead, if Lucas wants cash for CHA Sunday (~300 P, we hold 107), sell the surplus 2nd copies listed in 4735-4747 and 5080/5081 at 4-7 each, addressed to t07/t16/t15/t09/t06. Evidence: cash 107, floor 100, the 2nd copies are worth 1.2-3.2 each, and t02 bids only 1-4 for commons. Effect: +1 to +3 neg each, plus market value for Team 10's v07. Confidence: low-med.

## What the climbing teams are doing
- **Team 13 (#1, +7.0/15 min):** 41 deals, 6 MAL trades and 2 SAL trades, and it bought MAL-10 from t09 at 65 (tick 331). It unlocked Pilar at tick 262 via 3 Chato deals. It is a MAL/SAL page-builder buying rares at below-book prices.
- **Team 1 (+4.2/15 min):** it bought MAL-07 at 14 from t10 (tick 311), SAL-07 at 23 from t02 and MAL-06 at 20 from t04 within 10 ticks. That is cheap uncommon-set building from several sellers; it has only 14 deals but is climbing.
- **Team 4 (+4.2/15 min):** it sold MAL-06 at 20 and RET-05 at 8 (tick 321), and it buys LAV and LAT. It is cashing out spares while it builds.
- **Team 2 (#4):** it buys cheap across sets (RET-05 at 8, LAT-07 at 13, RET-06 at 14 at ticks 321-332). Its open bids are at 1-4 for commons and 28 for RET-10, so it is picking up low-ball fills.

## Threats
- **Team 13 is #1 at 28.8, we are #3 at 27.9, so the gap is 0.9.** Any MAL/SAL spare sold to t17/t03/t01 is fine, but MAL-09 (t17 bids 70) and SAL-09 (t02 bids 65) show page-closer demand around the leaders. Do not supply those.
- **Team 18 is #2 at 28.6 and collects RET/LAT.** Our 2nd-copy RET and LAT cards must not go to t18 or t15 without checking. t15 collects LAT/RET/MAL, and 4738, 4747 and 4971 are addressed to it, so confirm t15 is not feeding t18 or t14.
- **El Rastro common bids are collapsing (t02 at 1-4).** That is below our floor, so the 2nd-copy commons will mostly not fill. They may clear only through the v07 addressed asks.
