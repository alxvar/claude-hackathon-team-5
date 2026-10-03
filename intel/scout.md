# Scout (claude-sonnet-5-5, Sat 10:22)

## Top 3 actions now

1. **Close RET-07 from Abuela (bid 4124 at 21, expires tick 268; her last 24, ours 21).** Operator: step 21→22→23 with warm words, cap 24 (value 27.5).
   - Evidence: RET-08 closed at 22 from her 29→23, and RET-07 sits at her 24 with our bid at 21.
   - Effect: `neg_points` stays 0 (dealer gain), ladder about +0.003. It is a prerequisite for the RET page.
   - Confidence: high. Re-post the bid if it expires at tick 268.

2. **Buy RET-01 on El Rastro, the cap test card.** Operator posts a public bid at 20 and does not address it to t13, so the card goes to whichever team holds it.
   - Evidence: t13 bids 2 P for RET-01, -02 and -03, so it is a junk bidder, not a holder. The metrics show no RET-01 ask or trade, so a holder is not in the data.
   - Effect: it completes the page (value 72.9 bonus). Expected +50 if the cap is flat, +62 if 5×(p+f), +38 if value ≤ 6×book. The result goes into GAME.md.
   - Confidence: med. Fallback: Dani asks the room who holds RET-01, and the Operator raises to 30.
   - Check first: the page completes only if no RET card is missing, and RET-07 is still open.

3. **Open a Chato deal for level 3 only if the Pilar menu is worth it.** Level 3 Doña Pilar activated at tick 262 and Team 13 already holds it ("3 deals with chato"). Her terms are cut off in the data ("a collector: she pays over b…").
   - Evidence: we have 3 negotiated Chato deals today (87, 86, 30). Check `GET /api/me` to see whether level 3 is unlocked for us.
   - Action: the Operator reads Pilar's menu. Her "pays over book" language suggests she buys, so the Operator offers spares she may take, such as LAV-02/03/04 worth 3.2 each and SAL-01/02 worth 2.2 each.
   - Confidence: low. Her price list is not in the data. Do not sell anything below its value until the menu is read.

## What the climbing teams are doing

- **Team 18 (#1, 29.0, +8.0 in 15 min)** is buying RET. It paid 49 P for RET-02 from t02 at tick 230, against a clearing price of about 11, so it is a page-completer buyer and a competitor for our RET cards.
- **Team 2 (#3, +5.1 in 15 min, +18.4 in 60 min)** is trading RET with t15 (RET-07 at 24 at tick 234) and sold RET-02 to t18 at 49. It also bids 20 and 18 for RET-10/09. It is positioned as a RET intermediary.
- **Team 15** is buying LAT×6, MAL×3, RET×2 from teams, mostly at ≤10 P. It also took RET-07 and RET-02, so it is a RET competitor on cheap cards.
- **Team 13 (#4)** reached level 3 first. It also lobbied traders onto its own venue, which feeds it market points.

## Threats

- **Team 18 and Team 2 both buy RET.** If one holds RET-01 and the other is a RET collector, our last common may cost more than the 20 we bid. Stay on El Rastro and do not use v07.
- **Level 3 already opened for Team 13.** If Pilar's early-bird prices move, they will have first pick.
- **Our maker book moved to v07 (Team 10, #9).** Four of our asks vanished on 10:00-10:17 and the cause is unknown. A page-completing sale must never go on a venue.
