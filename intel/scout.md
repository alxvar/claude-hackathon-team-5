# Scout (claude-sonnet-5-5, Sun 04:57)

## Top 3 actions now

1. **Wait for Sunday 09:00 and run the CHA fast start (Operator, `simple_buy.py`).**
   - Evidence: the game is closed until Sunday 09:00, and cash is 392. CHA (1.6) is the largest multiplier. The directive allows the Pícaros CHA rares at the first tick of round 3, with `--offer-only` and a card and rarity check. Public CHA bids are capped at 54 for rares, 22 for uncommons and 9 for commons.
   - Effect: CHA values are ≈ 112 for a rare against ≈ 54 paid, so these are page-building buys with no dealer loss. The CHA page bonus is not in the data for us.
   - Confidence: med.

2. **Close the MAL page once ≥ 150 P is left after CHA (directive 01:40).**
   - Evidence: we hold MAL-01 to 05, MAL-06 and MAL-08 and still lack MAL-07, MAL-09 and the MAL rares/epic. That gap is not in the data, so check `/api/me/value` first. Neg_points is 119.1 and a close adds up to +50 (cap), or +40 under pack drag as the SAL close showed (+40.4 at tick 988). Open the silver pack first to reduce drag.
   - Counterparty: MAL-11 (epic) has traded t08→t10 at 195, and t01 bids 152. Don't feed t10.
   - Effect: ≈ +30-50 neg_points, which is ≈ +1.5-2.5 board points at 0.05 board per neg_point (Saturday's rate, [V]).
   - Confidence: med.

3. **Keep the open overnight asks live and place open asks for spares.**
   - Evidence: open asks fill 10× more than addressed ones (3.5% vs 0.3%). Our two addressed asks (19979 LAV-03 at 6 → t04, 19981 LAV-04 at 6 → t01) expire at tick 1455. The spares are worth 3.2 each, so any fill above 3.2 + fee is a gain.
   - Action: Operator re-posts them OPEN (not addressed) on El Rastro or a non-rival member's venue. The spare LAV-02 (3 copies at 1.3) can also go on an open ask at 10 (like the existing ask for LAV-02 at 10).
   - Effect: small, +2-5 neg_points at best.
   - Confidence: low.

## What the climbing teams are doing
- **Team 18 (#2, +0.8 over 30 ticks)** collects RET/LAT and bought LAT-10 from t13 at 72 (tick 1332). That is a rare bought below the book price of 70 × its multiplier, which is page-building at a small cost.
- **Team 12 (#4 on the board, +0.4)** is the most active: 70 deals. It bought RET-11 for 216 (tick 1245), LAT-10 at 86, LAT-06 at 20 and LAV-08 at 14. It is stacking epics and rares from teams that dump them.
- **Team 10 (#1, 37.6)** moved SAL-11 at 207 to t17 (tick 1296) and MAL-06 at 20 to t09. It also holds a MAL-11 at 195. It dominates both the trades and venue v10.
- **Team 6 (#6)** lists 969 offers but drops 2.4 points. Volume without selective value is not climbing.

## Threats
- **Team 10 (#1, 37.6, 7.1 above us)** leads, and everything we do on v10 feeds its market score. Its value created on v10 also counts for it. Keep sales off venues it controls.
- **Teams 18 (31.3) and 12 (30.4)** sit within ±1 of us and are still gaining. A rival that closes MAL or CHA before us costs us relative score.
- **Cash on hand (392) is idle until 09:00.** Dealers close ≈ 14:00 Sunday, so any dealer buys must happen before then.
