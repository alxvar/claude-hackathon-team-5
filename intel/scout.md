# Scout (claude-sonnet-5-5, Sun 12:00)

## Top 3 actions now

1. **Cancel bid 24703 (MAL-09 at 49, to t13) if it is still unfilled and the Chief hasn't re-approved it. Operator, via `trade.py`.**
   - Evidence: the Sun 11:48 directive says the MAL close is NO-GO because the 50 cap on team-trade gains makes a closer add 0. Our neg_points are already 50.0 (cap reached via CHA-05). The Sun 11:57 log shows the same bid used as bounty #1 at 49, which equals our value.
   - Effect: neg_points stay at 0. Paying 49 for a card worth 49 returns nothing. Only keep it if the Chief confirms it as the bounty payment.
   - Confidence: med.

2. **Run `lat_fodder.py` for the empty ladder slots. Operator.** Bids 24252-54 (LAT-06/07/08 at 9) stay live until tick 2152. A filled LAT uncommon goes first to Pilar above 16, then to Chato above 13.
   - Evidence: ladder is 0.342 (L3 +0.050 and +0.040 per deal; L2 +0.017). The Chief's log shows 1 L3 slot and 3 L2 slots empty. Other teams' asks: LAT-06 and LAT-07 at 30, LAT-01..05 at 8.
   - Method: use small steps (−2/−3), never jump to her bid, and never trade at the opening price.
   - Effect: roughly +0.05 ladder if a Pilar slot fills. Per the Chief's 17:45 note, the ladder did not move the board, so the value is small.
   - Confidence: med.

3. **Sell spare LAT/MAL cards into the open CHA-card bids only where we gain, and only to teams ≥ 10 below us.**
   - Evidence: the Rival profiles' "Who to sell what to" table says no buyer passes the feeding rule above our value + 3 yet. t07 (#17) bids 8 for CHA-01..05, t09 bids 15 for CHA-06/07/08, and t16 bids 12 for CHA-05. We hold CHA-01..10, with no spares listed.
   - Effect: none now. Do not sell.
   - Confidence: high.
   - Check later: t13 is the only team asking MAL cards at 10, from the MAL×9 pattern. Selling our worthless MAL commons (value 7) at ≥ 10 as maker gains ≈ +3 each, but under the 50 cap that scores 0. Cash does not score either, so skip it.

## What the climbing teams are doing
- **t04 (+7.5 in 60 min, 89 deals)** is the most active team. It buys RET×6, MAL×6, LAV×4 and LAT×3 through team trades, so volume is pushing it up.
- **t09 (+5.6) and t15 (+6.2)** are climbing. t15 sold CHA-10 and CHA-09 to t16 at 65 each (ticks 2022, 2065), which is value gained from other teams. t15 bids on RET/MAL.
- **t16** is now a CHA collector, buying CHA×3 at 65 for rares. It is at 20.5, so it is far below us and not a threat.

## Threats
- **t12 (#1, 34.4) and t10 (#2, 33.5):** we trail t12 by 1.5. t10 owns v10's rival venue. Any pair we route through a rival's venue feeds them, so keep our club trades on v10 or a member market.
- **t18 (#3, 33.1):** 0.2 ahead of us. It collects CHA/RET, so give it no closer.
- **t13 (#10 on the board, 102 deals)** is the field's closer broker and holds MAL-09. Our 49 bid is below Pícaros' last ask (58). Its sales to t17 on v10 give us only +0.9 mm_points per trade.
