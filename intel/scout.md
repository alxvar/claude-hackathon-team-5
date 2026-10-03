# Scout (claude-sonnet-5-5, Sat 14:56)

## Top 3 actions now

1. **Arm the Pícaros watch for the resume (Operator).** Announced at tick 630: "Quick deals. Few questions." No menu yet.
   - Evidence: we hold three Pilar deals (MAL-07 19, MAL-06 19, SAL-08 23). Ladder is 0.181, and Pilar's MAL deals gave +0.050 and +0.040. Ladder is worth ≈ +0.33 board per +0.01 (Directives 12:13).
   - Action: poll /api/dealers/picaros every 20 s and use `--offer-only` for sells at ≥ our value only.
   - Candidates: SAL-01/03/05 (value 9), MAL-02/03/04 (7), LAT-03 (5).
   - Expected effect: neg 0, ladder up to about +0.02-0.05 if a new level pays like Pilar. Pícaros being level 4 is not in the data.
   - Confidence: med.

2. **Keep swaps 9172 (→ t15) and 9173 (→ t07) live until tick 650, and add swaps (Operator, trade.py).**
   - Evidence: t15↔t07 swapped three times at ticks 607-616 at 0 P (LAV-08/LAV-06, LAV-03/MAL-08, MAL-01/SAL-02). t15 collects LAT/MAL and dumps LAV and SAL. t07 is #17 with 17.3, so it is not a feed risk. Our estimates: 9172 gives us about +14.3, 9173 about +3.8.
   - Expected effect: the cap-free team-trade gain is about +18 neg if both fill, at 0 fee as maker.
   - Confidence: med. t15 is #14 and t07 is #17, both safe to trade with.

3. **Sell spare commons to Team 7 (#17, 11.3 below us) at ≥ 9 as maker (Operator).**
   - Evidence: the buyer table shows LAT-04 +6.3 and LAV-02/03/04 +4.3 each at an estimated 9.5. Our values are 1.2-3.2.
   - Our live asks are at 6-7 to t03/t04/t16 (9101, 9136, 9102, 9025). Reprice or re-address them to t07 at 9, and cancel the 0 P swap duplicates first.
   - Expected effect: about +4 neg per card, about +0.4 board each at 0.094. The 9.5 price is an estimate, not a bid.
   - Confidence: low-med.

## What the climbing teams are doing
- **Team 10 (#3, +4.1 in 60 min)** is a seller and posts on its own venue: MAL-10 from Team 3 for 74 P at tick 585. It dumps SAL/LAT/MAL and collects LAV. Directives say Team 10 posts SAL-10 → t06.
- **Team 18 (#4, +2.2)** collects RET/LAT (prices c 9, u 23, r 75). It bought SAL-10 at 80 earlier and is trading the RET commons that t14 dumps: RET-02 and RET-04 at 9.
- **Team 14 (#1, +1.1)** collects LAV/LAT and dumps MAL/RET. At ticks 591-598 it sold four RET commons at 9 to t04, t09 and t15. This is steady volume at the clearing price.
- **Team 6 (#9, +4.6)** has 296 listings and a rare price of 79. It sold RET-09 to Team 2 for 84 at tick 504.

## Threats
- **Team 14 and Team 12 lead (30.8 and 29.6) and we are #5 at 28.1 (−0.8 in 15 min).** Do not feed them our LAV spares: t14 collects LAV/LAT, so LAV-02/03/04 must not go to it.
- **Team 13 (#7) bids RET-01/02/03 at 2 P and has 57 deals.** It is a low-value sink for our RET cards and it owns venue v03. Do not trade there.
- **Pilar's uncommon price is flat at a median of 18, and Abuela holds SAL-06 at 29 against our 21 (bid 9168 expires at tick 634).** The SAL-06 buy for the ladder is stalled while the clock is paused.
