# Scout (claude-sonnet-5-5, Sat 16:15)

## Top 3 actions now
1. **Sell spare commons to Team 7 (#17, 10.6 below us).** Offer our spare LAV-02, LAV-03, LAV-04 and RET-04 at ~9 each, as maker, addressed to t07. Executor: Operator via `trade.py`. Run `python3 tools/policy.py can-give <REF>` first: it said LAV-02 YES, LAV-03/04 and RET-04 NO.
   - Evidence: Dani's table shows gains of +4.3 to +4.7 each at an estimated 9.5.
   - Caveats: the price is an estimate, not a live bid; t07 has few trades, and t07 collects RET/LAV/LAT.
   - Effect: about +4 neg_points per card (≈ +0.4 board). Confidence: med for LAV-02 only, low for the others until the policy check clears them.
2. **Fill the empty ladder slots with dealer sells at or above our value.** Our ladder is 0.2, with the second L2 slot filled at 14.
   - Spare MAL-06 (17.5, policy YES): sell to Pilar at ≥ 19. Step our ask −2/−3 from ~30 and let her climb; never jump to her bid. Pilar MAL-06 earlier gave +0.040 with small steps. Executor: `abuela_bot.py --dealer pilar`, alone in its window, offer-only close.
   - Salamanca fever (Pilar +25% over book, 18:03-20:03) is the window for SAL-08 (reserved, worth 22.5) and any SAL bought below value.
   - Effect: ladder +0.02 to +0.04 per good L3 deal (≈ +0.7 to +1.3 board at +0.01 ≈ +0.33 board), neg 0. Confidence: med.
3. **Place a bid on Team 3's LAT-09 ask (rare, ~88 P bid, asks at 135) only if we hold no LAT page.** LAT is our lowest multiplier (0.5), so this is not for us. Instead, sell into the live bids for cards we hold and don't need.
   - t03 bids 88 for LAT-09 (offer 10700); we don't hold it. t06 bids 68 for SAL-09 and t04 bids 65 for RET-10. We hold RET-10 (149.9 to us), so we do not sell it.
   - Real action: let the open bids (10569 SAL-07 20, 10570 MAL-08 15, 10572 LAT-02 3) run to tick 772. Reprice only if they have not filled by ~tick 745.
   - Effect: small, +2 per fill. Confidence: low.

## What the climbing teams are doing
- **Team 1 (+1.2 / 15 min, #6) with only 19 deals:** it buys MAL×4 and SAL×4 from teams. That is few deals but cheap, clean value gains.
- **Team 6 (+1.0, #9) and Team 17 (+0.8, #7):** t17 buys MAL×4 and SAL×3. Team 6 sells to us (MAL-01 at 5 at tick 714) and lists 305 cards, so volume and low-multiplier dumping is its engine.
- **Team 15 (+1.2 in Dani's profile, 22 team trades):** it buys LAT×6, MAL×4, RET×3 and SAL×3 and posts many small deals. It is a safe counterparty.
- **Team 14, #1 at 30.1:** its score is falling (−0.2 / −0.6). Its lead is one value-created trade, so the board is compressing.

## Threats
- **Team 10 (#4, 29.1, +0.4)** is chasing a MAL page. It bid for our MAL-09 via its SAL-10 swap offer. Never give it MAL-09 (reserved); our bids on v07 help only its capped market score.
- **Team 4 bids 65 for RET-10** (offer 9866) and Team 2 pays 84 for RET-09. Rare demand for RET is rising, so Chato's 86-87 sale price is no longer a bargain. Page-closer sales are only allowed to teams ≥ 6 below us.
- **Team 13 (#8, 58 deals, 2 P bids on RET-01..04)** is trying to pick up our RET commons at dump prices. Do not sell it anything. Team 17 is also barred (Lucas's 15:55 policy).
