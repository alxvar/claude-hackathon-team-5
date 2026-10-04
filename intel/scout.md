# Scout (claude-sonnet-5-5, Sun 03:10)

## Top 3 actions now

1. **Wait for Sunday 09:00, then run the CHA fast start (Operator).** Take both CHA rares from Los Pícaros at the first tick of round 3, with `--offer-only` and a card/rarity check before accepting.
   - Evidence: red-team 00:55 says print runs run out (SAL-09 29/30, SAL-11 9/9). Our CHA multiplier is 1.6, so rares are worth 112 against dealer prices of about 54. The game is closed until 09:00 and cash is 392.
   - Effect: positive neg_points only from team trades, because dealer gains clip to 0. Pícaros bait-and-switch is a known risk (flag 7160), hence `--offer-only`.
   - Confidence: med.

2. **Keep the two overnight addressed asks live and post open asks for spares (Operator, trader sells-only).** Offers 19979 (LAV-03 → t04 at 6) and 19981 (LAV-04 → t01 at 6) expire at tick 1455.
   - Evidence: open asks fill 10× more than addressed ones (3.5% vs 0.3%, directive 00:37). Our spares are worth 3.2 each. The El Rastro asks include LAV-02 at 10, which is above our value of 1.3.
   - Action: relist LAV-02 (3 copies, 1.3 each), LAV-03 and LAV-04 as open asks at about 9-10 on v10, after the checks.
   - Effect: a small positive; selling a spare gives about +5 to +8 each. Do not sell to t12, t18 or t10, since the top 4 are never to be fed.
   - Confidence: med.

3. **Close the MAL page at 09:00 if at least 150 P is left after CHA, then post the RET-09 t07 → t09 club deal on v10.** The MAL go is in directive 01:40.
   - Evidence: we hold MAL-01 to 06 and MAL-08, and need MAL-07, MAL-09 and more. Pilar sold MAL-09 at 56 to us on Saturday. Directive 01:00 approves row #1, RET-09 t07 → t09 (+67.6 VC).
   - Effect: MAL close adds about +30 np past our cap, which lowers t18/t12/t03 relative to the field, by about 0.4-1.1 Sunday pts each. The v10 VC is market-making, not neg_points.
   - Confidence: med/low.

## What the climbing teams are doing
- **Team 18 (#2, +0.8 per 30 ticks)** collects RET/LAT. It bought LAT-10 from t13 at 72 (tick 1332). It is the nearest rival ahead of us, 31.3 vs 30.5.
- **Team 12 (#4, +0.4)** is a heavy buyer of LAT: ×8 team trades. It bought RET-11 at 216 (tick 1245), LAT-10 at 86 (tick 1304), LAT-06 at 20, and LAV-08 at 14 (tick 1420). It also sold SAL-09 to t09 at 70.
- **Team 10 (#1, 37.6)** has 467 listings and 62 deals. It sold SAL-11 at 207 (tick 1296) and MAL-11 to us... no, it bought MAL-11 at 195 (tick 1264). It sells epics and wins on volume as a maker.
- **Team 16 (#14, +0.3)** is a RET buyer with 796 listings. Its bid of 28 for our LAV-10 looks low against our value of 177.1.

## Threats
- Teams 18, 12 and 10 are within 7 points of us, and 12 is about 0.1 behind. Any page-closing card we sell to them feeds them. Only RET/LAV collectors t07, t04 and t16 are low enough to receive cards.
- Our duel score is 35.39 but our `negotiating` is flat. The ladder (0.483) and flags are spent, and only team trades and v10 move the board (≈ +0.05 board per neg_point).
- t10 held the SAL-11 epic and is also the seller of MAL-06 to t09. Rival teams bidding for CHA cards at the first tick can outpace us, because print runs are limited.
