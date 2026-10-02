# Scout (claude-sonnet-5-5, Fri 21:54)

## Top 3 actions now

1. **Reprice our two LAV-04 sells (10 P each) and SAL-06 (30 P) to the market.** Asks by others sit at 9-11 P for commons and nobody lists SAL-06 near 30. Human (Lucas) or `trade.py` does this.
   - Evidence: LOG 21:46, LAT-06 sat unsold at 30 for 15 min, then sold at 22 within ~3 min after repricing. Team trades at tick 89-92 are all 9-10 P for commons.
   - Buyers: "Who buys" shows t10 buying LAV×2 and t04 buying LAV×3. Offer LAV-04 to t04 or t10 via `to`, since their appetite for LAV is already shown.
   - Effect: small, since a common sale is price − our value (our LAV value is 1.3 × 10 = 13). Selling a common at 10 P scores negative. Check our value first, and hold any LAV card that is worth more to us than the bid.
   - Confidence: med.

2. **Keep the LAV-09 bid at 91 P (offer 1371) and have Dani/Lucas find the LAV-09 holder in the room.**
   - Evidence: only one LAV-09 exists. Team 10 bids 110 P (offer 1373) against our 91. We cannot win on price. Team 10 is #4 at 24.0 and is building the LAV page.
   - Action: do not raise the bid above 91. LOG says 100 would score −9 without LAV-06/07, and a raise feeds a leading team. Our value is 91 now, so any higher price loses points.
   - If the holder agrees to sell to us, the price must be ≤91. Otherwise accept that Team 10 gets it.
   - Effect: a win scores about 0 at 91 and positive only with the page bonus. LAV-06/07 ownership is not in the data.
   - Confidence: low.

3. **Fill the MAL and LAT rare/uncommon bids only if we hold the card or can buy it cheaply.** Bids for rares are high: MAL-09 78 P (t17), MAL-10 78 P (t17) and 75 P (t10), SAL-10 70 P (t13).
   - Evidence: SAL-10 (rare) sold t12→t18 at 80 P (tick 72), and MAL-10 sold t14→t08 at 53 P (tick 77). Big jumps came from single rare trades (65-80 P).
   - Action: check our inventory for MAL-09, MAL-10 and SAL-10. If we hold one, list it at ~78 to t17, our own value being 0.7 × 70 = 49 for MAL. The gain is about +29 P, minus fee if we accept. Use `trade.py` with `to` = t17. If we hold none, buy from Abuela only if a rare appears; whether she sells rares is not in the data.
   - Confidence: med, depends on inventory (not in the data).

## What the climbing teams are doing
- **Team 15** (not in the top 10 shown) is the heaviest buyer: LAT×10 and MAL×1. Their purchases at ticks 78, 83 and 86 are 18, 40 and 22 P bundles. They are collecting the LAT set, and the cheap LAT cards we sell score them.
- **Team 8** (#3, 25.0) buys MAL×4 and SAL×1, including MAL-10 at 53 P. They are buying rares for the MAL page.
- **Team 12** (#5) buys MAL×4: MAL-06 at 27 P and MAL-05 at 10 P (from t10).
- **Team 13** (#1, 27.8) bids 70 P for SAL-10 and bought MAL×3, SAL×1, LAT bundle at tick 83. It runs the most deals (13).

## Threats
- **Team 10** (#4) bids 110 P for LAV-09 and sells to us and others. It beats our 91 bid and is building the LAV page.
- **Team 17** has bids at 78 P on MAL-09 and MAL-10, and 26 P on MAL-07/08. These raise the MAL rare price against any buy we plan.
- **Leaders buy from us**: selling MAL or SAL cards to Teams 13 and 8 hands them value. Only sell if our gain clearly exceeds their gain, and prefer teams below us such as t4, t9 and t3. Team 4 is #6 and Team 9 is #9.
