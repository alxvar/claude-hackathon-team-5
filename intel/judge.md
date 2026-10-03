# Judge (claude-opus-5-5, Sat 18:45)

## Verdict
**Gaining, but the lead rests on one trade.** We are #1 at 32.0 (+2.0 in 15 min, +2.6 in 60 min). Team 6 is at 31.7 (+0.3 behind us) and Team 14 at 31.5 (+0.5 behind). The whole 15-min gain is the SAL close: +40.4 neg → +1.99 board, about 0.049 per neg point.

## Our strategies: keep / kill / scale
- **Bargains daemon plus taker accept: SCALE.**
  - It produced the biggest gain of the day: the SAL-06 ask at 28 gave +40.4 at tick 988.
  - Nothing qualifies on El Rastro now. LAV-05 at 5, SAL-04 at 10 and RET-10 at 84 would all be 2nd copies worth 2-19 to us.
- **Addressed maker bids for page closers: KILL.** Bids 14040, 14268, 14557 and 14889 (35-50 P to t02, t13 and t17) went about 30 min with no fill.
- **Trading loop: KEEP.**
  - Today it made 2 accepts, both swaps: +6.2 (SAL-04/RET-04) and +15.5 (SAL-07/LAT-01, the tick 904 window).
  - The errors in its log (rate_limited, sobre_bienvenida) are Friday's and stale.
- **Dealer bot: KILL.**
  - The ladder is capped: negotiating stayed flat at 21.88 while the ladder went 0.373 → 0.437.
  - The MAL-08 → Chato thread was cancelled at 17:45.
  - Any SAL sale to Pilar now books the page bonus as a loss.
- **Our 4 open asks (MAL commons at 9, LAV-03 at 6): KEEP small.**
  - As maker they gain about +2 to +2.8 each; no fills are in the data yet.
  - The t15 asks break §4A if the card closes t15's MAL page: t15 is 8.0 below us, not ≥ 10. Whether it lacks MAL-02/05 is not in the data.
- **v10 room plan and Team 15 posting script: KEEP, with no result yet.** There have been 0 v10 settlements since 17:40 (commission N = 0). Our current mm_points are not in the data.
- **Flags: KILLED, correctly.** Flag 8 scored 0.

## Check the scout
- **Holds:**
  - Ladder and flags are spent.
  - SAL cards stay reserved.
  - T6 and T14 are 0.3 and 0.5 behind us.
  - T12 trades heavily without gaining (−2.9 in 60 min).
- **Wrong:**
  - **Workshop as a gain.** The Workshop moves neither neg_points nor the ladder [V 16:15], so it adds 0 board. LAT-03 and LAT-04 are single copies, not spares. The LAV-03 spare is already committed to offer 15196.
  - **Opening the pack now.** GAME.md keeps the pack for the CHA release. What a pull is worth is not in the data, and opening it scores nothing by itself.
  - **"Asks to t15/t09 lift mm_points."** Our own trades never count as value created between *other* teams. These asks pay only their small neg gain.
  - **"T10 bid on RET-09 at 30 (offer 15314)."** It is not on the board: the top bid shown is 13.
  - **"T6 sold RET-03 to t12 (tick 905)."** It was t12 → t06, so T6 bought.
  - **"T18 buying RET (LAT-01 to t07)."** T18 sold that LAT-01.
  - **"T16 RET bids at 5."** The board shows 4.

## The 3 changes with the highest expected gain
1. **Get one positive-VC, non-rival trade on v10 before the next bench.**
   - How: Dani, in person, takes the first pair from intel/v10-suggestions.md: the buyer's multiplier must beat the seller's, and neither team may be within 3.0 of us or in the top 6.
   - Effect: about mm 0 to +5 [L, Market], the lever the 17:40 directive put at about +3 board.
   - Risk: negative value created (the SAL-07 t10 → t15 trade cost −5.2), so check the multipliers before anyone accepts.
2. **Sell the LAV spares to t07 and t09 as maker.**
   - Spares: LAV-02 (worth 1.3), LAV-03 and LAV-04 (3.2 each).
   - Buyers: t07 (21.9, 10.1 below us, bought LAV ×7) and t09 (19.4); both pass the feeding rule.
   - Price: addressed asks at 9, the clearing price for commons, on El Rastro or v15, never a rival venue. Raise to 35-45 only if Dani confirms a page gap.
   - Effect: about +6 to +8 neg each, so ≈ +1 board if three fill.
   - Risk: only 5% of asks filled on Friday. Reprice after 10 min.
3. **Pin the bargains daemon to every El Rastro ask with value − price − fee ≥ 3, plus a human taker accept.**
   - Check each maker in the feed's `offer.listed` event first: the public boards mask makers.
   - Effect: it is the only lever left that pays in tens of points.
   - Risk: accepting from a rival (t06, t14, t03, t10) lifts them as well. Skip their asks.

Hold the silver pack and the Workshop until the Chief rules: neither moves the board tonight.
