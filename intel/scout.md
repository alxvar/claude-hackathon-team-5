# Scout (claude-sonnet-5-5, Sat 16:36)

## Top 3 actions now

1. **Cash in the SAL-07 bid (offer 10569, bid 20, expires 772). Operator, trader.py.**
   - Evidence: the bids board lists t03 SAL-10 (rare) 73 (offer 11505) and t06 SAL-09 68 (offer 11579), and both teams are outside the top 5. Our MAL-09 (rare, worth 49) is a different card. Lucas has told us not to recommend a MAL-09 sale below 55 to Pilar.
   - Action: let 10569 ride, and re-bid at 20 only if it lapses. It is a gain-≥3 buy only if our SAL-07 value is above 23; re-read /api/me/value first. Confidence: low on the value.
   - Effect: roughly +1 to +3 neg_points per fill.

2. **Sell spare commons as maker to Team 7 and other low teams. Operator, book daemon.**
   - Evidence: Team 7 (#17, 10.6 below us) values commons at ~9.5. Our spares are worth 1.2-3.2: LAT-04 +6.3, RET-04 +4.7, LAV-02/03/04 +4.3 each.
   - Action: list LAT-04 and LAV-02 at 9 addressed to t07 (maker, no fee). Run `tools/policy.py can-give` first. Today it returns YES for LAV-02 only. LAV-03/04 and RET-04 are NO because they are page copies, so do not sell them.
   - Effect: about +4 to +6 neg_points per fill, roughly +0.4 to +0.6 board points. Confidence: med.

3. **Spend the level-4 unlock (3 deals with Pilar, announced at tick 761). Operator, abuela_bot.py with `--dealer`.**
   - Evidence: the ladder pays most at higher levels (L3 ≈ 3× L2). The Pícaros persona opened at level 4 for t05, t08, t09, t10 and t16.
   - Action: try a level-4 sale of a spare uncommon above our value (MAL-06 at 17.5 or SAL-08 at 22.5). Step -2/-3, never jump to the dealer's bid, and use offer-only to close.
   - Effect: a clipped-gain sale costs 0 neg_points, and the ladder is 0.2 now. The level-4 price range is not in the data, so keep the first test small. Confidence: low.

## What the climbing teams are doing

- **Team 3 (+1.6 / +7.0 in 60 min)** is buying rares from the field and selling its own commons. It bought LAT-09 at 88 from t16 (tick 724), and it bids 73 for SAL-10 (offer 11505). It sold SAL-01 to us at 7 and appears to keep buying. It is #7, 0.9 below us, and rising.
- **Team 16 (+1.2 / +4.5)** takes lots of cards, mostly cheap. It bought a rare and RET-06 at 14 (tick 711), and now bids RET-07 at 15, LAV-06 at 12, RET-02 at 5 and RET-01 at 5. It has 32 deals.
- **Team 1 (+1.1 / +3.3)** reached #6 with only 21 deals. Its page purchases are MAL×4 and SAL×4, so it is a page-building team.

## Threats

- **Team 14 (#1)** bought our MAL-08 at 15 at tick 760. It gained little from the card, but this is a top-5 trade. Lucas's 15:55 policy says no trades with the live top 5 unless our gain is ≥ 3× theirs, so check the policy before any repeat.
- **Teams 3 and 1** are at 27.7 and 28.5, within 0.9 and 0.1 of us. Do not feed them page-closers. The policy limit is ≥ 6 below us, and neither is.
- **Level-4 unlocks went to t08, t09, t10 and t16 as well.** Several rivals can now race for the same ladder slots.
