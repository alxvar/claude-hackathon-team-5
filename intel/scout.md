# Scout (claude-sonnet-5-5, Sat 10:43)

## Top 3 actions now

1. **Keep the SAL-01 → t03 offer 4322 (40 P) alive and re-post it before it expires.**
   - Offer 4322 expires at tick 311, and the metrics clock reads tick 305. The Operator should re-post it now as maker, addressed to t03, on El Rastro.
   - Evidence: our SAL-01 is worth 2.2, so a fill at 40 would be about +37.8 (capped at 50). t03 is #10 at 17.3 and not in the top 4. Their SAL page bonus is about 66 × their multiplier (not in the data), so 40 is plausible.
   - Effect: up to +37.8 neg_points. Confidence: med, because t03 has not accepted yet.
   - Risk: t03 also holds our 26 P bid on SAL-08 (offer 4444). Do not pile on more asks to t03.

2. **Stay passive on accepts from 11:50 and run the book as maker only.**
   - This follows the 10:35 directive: the Operator stops loop.py at 11:50, book.py keeps posting, and no dealer threads run after 11:40.
   - Evidence: we are #4 at 24.2 (+5.0 in 15 min, +8.2 in 60 min), 0.0 duel points so far, and 34 practice duels finished. Duels I are the biggest open pool.
   - Effect: protects duel deals, since a missed duel deal counts 0. Confidence: high.

3. **Ask Dani to point t01 at offer 4448 (MAL-07 at 23) and t17 at offers 4446/4460 (MAL-06 at 23, MAL-02 at 9).**
   - Evidence: the "who buys which set" line shows t17 bought MAL×3 and t01 MAL×2. t17's MAL-09 bid at 70 is the top bid on the board. Our MAL-06/07 are worth 17.5 each, so 23 is +5.5 each.
   - Effect: about +11 neg_points for the pair, plus cash toward Sunday's CHA page. Confidence: med.
   - Note: the 11:40 dealer stop does not affect these El Rastro maker offers.

## What the climbing teams are doing
- **Team 18** (#1, 30.3, +14.7 in 60 min) pays up for RET cards. It bought RET-02 at 49 P from t02 at tick 230, and it collects RET/LAT. Its +14.7 comes with 27 deals, mostly dealer trades. Whether the 49 P buy completed a page is not in the data.
- **Team 2** (#2, 27.9, +16.4 in 60 min) is a seller and flipper. It sold RET-02 to t18 at 49 and RET-07 to t15 at 24, bought RET-02 from t06 at 12 (tick 205), and still bids 24 for RET-10. It is moving cards between teams at a markup.
- **Team 10** (#7, +4.0 in 15 min) swapped with us. It sold us RET-01 at 20 and gained 20 cash. Reciprocal-venue deals are working for both sides.
- **Team 15** is the most active buyer, with LAT×6, MAL×3 and RET×2. It is #14 at 13.2 and is the natural taker for our LAT-04, MAL-04 and LAT-08 offers.

## Threats
- **Team 2 is the RET-10 bidder at 24 P (offer 4424).** It sits in the top 4. We hold 2 copies of each of RET-09 and RET-10, but the 2nd copy is worth only 25%. Do not feed t02 or t18.
- **Our listed LAV-02/03/04 spares go to t09, t07 and t10, which are low teams.** Those spares are page-relevant for LAV collectors, so confirm the buyers do not close a page with them. The feeding table currently shows "no buyer passes the rule".
- **Offers addressed to a team are visible in the public feed.** Rivals can see our targets, and the feed shows offer 4322 at 40 P to t03 in full.
