# Scout (claude-sonnet-5-5, Sat 10:32)

## Top 3 actions now

1. **Sell RET-surplus and keep the book addressed, but watch the fills: re-check the 11 asks (4248-4258) against clearing.**
   - Evidence: our asks sit at clearing (SAL-08 27 vs clearing 24.5, MAL-06 25, MAL-07 24, commons 9-10). Asks by others show LAT-04 at 7-9, LAV-03 at 9, LAV-04 at 10. Only 5% of asks filled on Friday.
   - Action: the Operator drops SAL-08 (4248) toward 25 and MAL-07 (4250) toward 24-25 after about 10 ticks unfilled. book.py already steps toward the floor after 20 ticks.
   - Effect: each fill adds cash toward Sunday's CHA page (~300 P). Our value for these spares is 1-3, so the neg_points effect is small (a few points). Confidence: med.

2. **Answer the open RET-10 and RET-07 bids from Team 2 only if the card is a spare. We hold no spare RET-07 or RET-10, so do nothing.**
   - Evidence: t02 bids RET-10 22 and RET-07 19. We hold exactly one copy of each, worth 149.9 and 100.4 to us (page bonus).
   - Action: do not sell. Team 2 is #3, a top-4 team, and our RET-10 is not a spare.
   - Effect: avoids feeding a leader. Confidence: high.

3. **Take any team ask on a card we lack (LAT, SAL, MAL) only at gain ≥ 3, and test a high-value bid for MAL-09 (t17 bids 70).**
   - Evidence: t17 bids 70 for MAL-09 (rare) and t04 bids 52 for LAT-09 (rare). Neither is ours: MAL is 0.7× and LAT is 0.5×.
   - Action: ask Lucas or Dani in the room whether anyone holds MAL-09 or LAT-09. We have no copy, so there is nothing to sell. Not in the data otherwise.
   - Effect: none for us. Skip.
   - Confidence: low.

The one real opening is Pilar at about 12:20, after Duels I. Use it for ladder and cash only. Sell spares only, and keep any ladder deal below her list price [L]. Confidence: med.

## What the climbing teams are doing
- **Team 2 (+19.9 in 60 min, #3)** bought RET-02 from t13 and RET-07 from t02. Its RET-02 at 49 P to t18 and RET bids (RET-10 22, RET-07 19) show it collecting RET. Its profile also lists 102 listings.
- **Team 18 (#1, +10.5 in 60 min)** bought RET-02 at 49 P from t02 (tick 230). It collects RET/LAT, and its Abuela rate is −19%. It is the leader and a direct RET competitor.
- **We climbed #6 → #4 (+4.9 in 15 min)** on the RET-01 page close (+50.0, capped). Page-closing from a team at a low price is the recipe that is working.
- **Team 14 (+0.9 / +5.0)** collects LAV/LAT, so it holds the LAT trades (t15→t14 LAT-03 at 8 P at tick 261).

## Threats
- **Team 2 and Team 18 bid for RET-10 and RET-07.** If anyone reads our addressed offers on the feed (35 such events Friday), they can target our RET cards. We hold all ten of the page, so the risk is only to unclosed spares.
- **Leaders on rival venues.** Team 13 lobbies for trades on v03. Our book sits on Team 10's v07 (#7) and is not feeding the top 4. Keep it that way.
- **Score drift.** Team 13 fell −7.4 in 60 min, and Teams 12 and 13 are the top-4 venue owners. Our #4 lead over Team 14 is 0.9 points, which is thin. Any further neg_points must come from the book or from page-closers.
