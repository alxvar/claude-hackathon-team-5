# Scout (claude-sonnet-5-5, Sat 16:20)

## Top 3 actions now

1. **Sell SAL-08 (uncommon, worth 22.5) to Pilar at ≥ 23, offer-only, small steps (−2/−3), operator + `abuela_bot.py --dealer pilar`.**
   - Evidence: Pilar's earlier SAL-08 sale at 23 (her 22, 22, 23 final) gave ladder +0.019, and her SAL-06 sale at 25 gave +6.2 neg. Dealers' uncommon prices are 19-25 (metrics).
   - Salamanca fever runs 18:03-20:03 (Pilar +25% over book). SAL-08 is reserved, so wait for the window and sell there for ≥ 28.
   - Effect: 0 neg cost as long as price ≥ 22.5, and it can fill an L3 slot. Ladder is 0.2 and may be near the cap [L, ~0.15 estimate, uncertain].
   - Confidence: med.

2. **Sell spares only to safe teams (t03, t15, t16, t09), as maker: MAL-05 9 → t15 (10215), LAV-04 6 → t03, SAL-02 11 → t16, LAT-03 7 → t03.**
   - Evidence: these offers are already live. A team sale of SAL-01 at 7 booked +4.7 neg, and a bid of 5 for MAL-01 booked +2.0.
   - Policy-compliant: the Chief's list names t16, t15, t03, t09 as safe. `tools/policy.py can-give` says SAL-01, LAV-03/04 and RET-04 are NO, so check it before adding anything new. Only MAL-05, MAL-02, SAL-02 and LAT-03 are free to give.
   - Effect: roughly +2 to +5 neg each (≈ +0.2 to +0.5 board). Small but free.
   - Confidence: med.

3. **Run the Team 10 reciprocity bids and watch for fills: 10569 SAL-07 at 20, 10570 MAL-08 at 15, 10572 LAT-02 at 3, all on v07 until tick 772.**
   - Evidence: the MAL-01 fill at 5 added +2.0 neg and gave Team 10 (#4) its first fill on our venue. t10 "market at the cap" per the Chief.
   - Effect: each fill scores value − price, about +2 to +2.5 per bid at 2-2.5 under our value.
   - Confidence: low-med. Fills are not guaranteed, and I can't verify that these bids don't feed t10.

## What the climbing teams are doing
- **Team 1 (+1.5/h, #6, only 19 deals):** it buys MAL ×4 and SAL ×4 in team trades, i.e. fewer, targeted trades. Its listed holdings are in the "buyer for SAL/LAV/MAL" profile.
- **Team 6 (+1.3/h, #9):** it posts the top bid on the board, SAL-09 at 68, and sells RET-06 to t04 at 26. It trades volume (39 deals, 305 listings).
- **Team 17 (+0.5/h, #7):** it collects MAL/SAL/LAV and bids 15 for LAV-06. It is a rival (policy: never trade where it gains more than we do).
- **Team 8** is flipping commons at 4-5 (LAV-05, MAL-04, LAT-04) and bids 5 for RET-01/02/03. It is #13, so not a threat.

## Threats
- **Compressed board:** #1-#4 are within about 1.5 of us (30.1, 30.0, 29.2, 29.1 vs our 28.65). Team 14 is falling (−0.6/h) while we rise. Any gift to them is costly.
- **RET-10/RET-09 market:** Team 4 bids 65 for RET-10 and RET-09 is asked at 86. Our copies are worth about 150 each (page bonus), so don't sell them. They are the page-closing cards.
- **Feeding t13/t17:** Team 13 (#8, 58 deals, 26.1) keeps bidding 2 for our RET commons. Refuse these; we gain nothing and it grows through volume.
