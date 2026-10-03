# Scout (claude-sonnet-5-5, Sat 20:38)

## Top 3 actions now
1. **Hold all writes until the Chief clears the pause** (tick 1201, ~10 min; 20:16 operator flag run/hold-writes). Then re-read cash and the schedule. The Payday announcement is cut off after "Only deals sc…", so the scoring condition is **not in the data**. The Chief or Dani should read the full text at the front before any spend of the 400 primas. Cash is 520 now, so the floor of 85 is no constraint. Confidence: high.
2. **Re-post the live spare asks with doubled expiry** (executor `trade.py`, operator, after clearance). Offers 17392 (MAL-08→t01, 20), 17650 (MAL-02→t08, 40), 17660 (LAV-03→t04, 6) and 17696 (MAL-03→t09, 9) expire at ticks 1214-1237. LAV-04→t01 at 6 (17586) runs to 1232. Per the Saturday expiry rule, ask 2× the ticks you want.
   - Evidence: the buyers are #12, #14, #13 and #16, all ≥10 below us. The values to us are 17.5, 7, 3.2, 7 and 3.2.
   - Effect: price − value as neg_points, about +2.5 for MAL-08, +2.8 for LAV-04 and +2 for MAL-03 if they fill. MAL-02 at 40 is far above the 9 clearing price, so expect no fill.
   - Confidence: med on fills, low on size.
3. **Do not sell SAL-09 or SAL-10 to t09's bids (68 each, offers 17770 and 17771).** They are worth 122.6 to us and the SAL page is closed, so a sale books a loss of ~55 plus the page bonus. Keep ignoring bids below value. Pilar's epic at 187 and rare at 80 are dealer deals, which clip gains to 0. Only the capped ladder (flat across 0.373 → 0.437) can reward them, so skip them. Confidence: high.

I found no team-trade buy opportunity above the +3 threshold in the El Rastro snapshot.
- The cards asked at 8 (LAT-01..05) are worth about 5 to us.
- RET-09 at 84 would be a second copy worth 25% of 77, about 19.
- No team ask on the MAL cards we lack is visible. A MAL-page close (we hold 5 MAL commons plus MAL-08 and miss MAL-06, 07, 09, 10) is not priced in the data. Cost estimate: not in the data.

## What the climbing teams are doing
- **Team 2 (+2.6 in 15 min, #9):** bought MAL-10 (rare) from t13 at 30 (tick 1191). It bought RET-09 from t06 at 84 earlier and "collects RET".
- **Team 7 (RET collector, #17):** the buy mix is RET×8 and LAV×7. It bought RET-09 from t04 at 66 (tick 1125), RET-10 from t06 at 77 (tick 1186) and RET-08 from t09 at 24. It is stacking RET rares and uncommons through team trades, likely for a page close. It is at 21.2, so it is no threat to our rank.
- **Team 10 (#1, 34.0) and Team 6 (#2, 32.6):** t10 holds 12 team trades but 40 dealer trades and 427 listings. It stays on the top of the board even at −0.2, so the gap to #2 is 1.0 and to #1 2.4. Team 6 has 30 team trades and the most listings among the top 4 (758). Both are ahead of us on volume.
- **Team 13 (dumper, 23 team / 56 dealer trades, 778 listings):** it sells LAT/LAV/MAL cheaply (MAL-10 at 30, SAL-07 at 18, LAV-02 at 3 in ticks 1191-1194). It is a cheap source for MAL cards if we choose a MAL close later.

## Threats
- **Payday, 400 primas to every team:** a second purse lets rivals buy page cards and epics. The top 4 (#1 t10, #2 t6, #4 t3, #5 t14) will spend it on Pilar and Los Pícaros epics and on team trades. Our gap to #2 may widen if we idle.
- **t09 (#16) bids 68 for SAL-09/10 and 20 for SAL-06/MAL-06.** It is not a rank threat, but the bids show it wants SAL rares, so do not feed it page cards.
- **Team 3 (#4, 30.0, +0.3):** it is 1.6 behind us and has the highest negotiating score (24.49 at tick 850). It collects SAL/LAT/LAV and buys at its own prices (c 6, u 28, r 81).
