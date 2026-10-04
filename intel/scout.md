# Scout (claude-sonnet-5-5, Sun 10:44)

## Top 3 actions now
1. **Land the MAL-09 bid (offer 22688, addressed to t13 on v21), then the last MAL card.** Executor: Lucas's `mal_close.py` (pid 79615), which posts on v21 at ≤ value − 1.
   - Evidence: we hold MAL 01-06, 08 and 10, so only 07 and 09 are missing. MAL-10 is worth 49, so the 48 offer is ≥ 0 even with fee. The Pícaros bait-and-switched MAL-09 twice. Directive 10:25 Sun says MAL close GO.
   - Effect: the non-last card scores about +0 to +1. The LAST card must be bought at ≤ value-when-last − 50 to bank +50 (our trade part is not capped per the Analyst).
   - Confidence: med. t13 has been silent on its threads all weekend.
2. **Push the L4 ladder with the Pícaros: LAT-01/03 at ≥ 5, then the dups (LAV-04 and SAL-04 spares).** Executor: the dealer bot / `dups.sh` (pid 74498).
   - Evidence: LAT-04 to the Pícaros at 5 took the ladder from 0.253 to 0.311. The L4 slots now read 0.075/0.081/0.058, so a new sale only counts if it beats 0.058. Their opening and final of 4 never count, so keep the floor at 5.
   - Effect: ladder +0.01 to +0.03 at best. Metrics show the board `negotiating` flat while the ladder rose (21.88 unchanged across ladder 0.373 → 0.437), so the board gain is [L] small.
   - Confidence: low-med.
3. **Do not post anything else for t16 or t09 CHA cards. Cancel or hold bid 21791 (LAT-06 at 9, expires 1815).**
   - Evidence: the public CHA bids of t16 (CHA-09/10 at 64) and t09 (5-15) are all below our values (122-218).
   - Effect: keeps our cash (614) for MAL and avoids dumping value. Do the cash-neutral dup sales only to non-rival counterparties.
   - Confidence: med.

## What the climbing teams are doing
- **Team 12 (#1, 34.8, +3.8 in 60 min)** is a heavy dealer-and-team trader: 76 deals, collects RET/MAL/LAT. It bought LAV-07 from t13 at 40 (tick 1712) and MAL-06 from t12→t04 at 17.
- **Team 18 (#3, +2.0 in 60 min)** collects CHA/RET. It bought CHA-01 from t13 at 72 (tick 1513), a page closer. It also sold SAL-11 to t13 at 238.
- **t13 is the broker of closers** (99 deals): SAL-10 → t03 at 108 and CHA-01 → t18 at 72. It sits at #6, so its sales feed t18 and t03, who are racing us.
- **Team 8 (+3.5 in 60 min)** has 83 deals and sold LAV-08 → t12 at 14.

## Threats
- **t18 sits 1.0 ahead of us (33.1 vs 32.1)** and t03 is 2.6 behind. Neither may get a MAL or CHA page-closer from us. All our MAL sales go only to non-rivals.
- **t13 has not answered our MAL-09 bid and refused El Rastro.** Every closer it brokers feeds a #2-#3 rival, and a v24 pact would give it value-created points if we trade there. Keep v24 OFF until v10 holds VC from t13.
- **Cash and clock:** the Pícaros' MAL asks are bait-and-switch, so MAL-07/09 are only available via team trades. Dealers close at 14:00 and the bid expires at tick 1914, so re-post in time.
