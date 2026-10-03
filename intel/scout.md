# Scout (claude-sonnet-5-5, Sat 10:53)

## Top 3 actions now

1. **Keep the cash and the book for Sunday's CHA page; don't chase more dealer deals.**
   - Action: the Operator leaves the 15 addressed asks on book.py (floor 100). Cash is 107; CHA needs ~300 P.
   - Evidence: neg_points 28.5, score 29.05 (#2). Our dealer deals this round (Chato RET-09 at 87 and RET-10 at 86, RET-06 at 30) cost −21.5, and none moved the ladder.
   - Effect: the book adds cash. A fill scores roughly price − value, about +1 to +4 each. Expected neg_points effect is small. Confidence: med.

2. **Sell LAT-08 (worth 12.5) to a team, not to a dealer.**
   - Action: offer 4648 is LAT-08 → t15 at 20, live until tick 358. Leave it, and don't lower it below 15.
   - Evidence: t15 is the heaviest LAT buyer in the metrics (LAT×6) and sits #14 in the profiles, so it passes the feeding rule. LAT cards cleared at 8 and 5 recently.
   - Effect: a fill at 20 gives about +7.5 against our value, and about +20 cash toward CHA. Confidence: med.

3. **Use Abuela for ladder points after Duels I (resume ~12:10); Abuela is the only dealer that moved the ladder.**
   - Action: the Operator buys only cards we still lack at or below Abuela's list price, and only if they sit below the dealer's list price. We hold all 10 RET cards and most LAV, so spare cards are the only candidates. Skip a deal if there is no need for the card.
   - Evidence: every below-list Abuela deal moved the ladder (+0.014 to +0.018); ladder is now 0.055. Chato deals never did. Abuela's recent prices were uncommon 23 and common 6.
   - Effect: about +0.003 to +0.018 ladder per deal. It adds no neg_points. Confidence: low-med.

## What the climbing teams are doing

- **Team 18 (#1, 30.2, +17 per hour)**: 27 deals. It is collecting RET/LAT and bought RET-02 from t02 at 49 (tick 230).
- **Team 2 (#3, 28.5, +14.5 per hour)**: 24 deals. It is buying RET cards on El Rastro: RET-07 at 24 (tick 234) and RET-05 at 8 (tick 321). It also holds a bid on RET-10 at 26.
- **Team 1 (#8, +4.0 in 15 minutes)**: it is cheaply buying MAL and SAL uncommons from other teams: MAL-07 at 14 (t10), SAL-07 at 23 and MAL-06 at 20.

## Threats

- **Team 2 is bidding 26 for RET-10 (offer 4701)** and 4 for RET-03, so it is building RET. It is top 4 and #3, so we must not feed it. We hold RET-10 as part of our completed page, so we must not sell it.
- **Team 13 bids 2 for each of our five RET commons** (offers 4569, 4624, 4729, 4744, 4758). Whether it is hunting a RET page is not in the data. Never sell it RET.
- **Our spare offers sit at 4-9 P** (LAV-03 5, SAL-02 4, LAT-04 4). They are cheap, and a page-closer at that price would hand a rival up to +50. Keep them addressed only to teams outside the top 4. Never address them to t12, t14, t18 or t02.
