# Scout (claude-sonnet-5-5, Sun 09:58)

## Top 3 actions now
1. **RET-11 → t02 at 240 (offer 21583, El Rastro, addressed, exp tick 1653).** The operator and Dani already have this live.
   - Evidence: our RET-11 is worth 198 to us, and t02 had bid 240 for it. t13's asks at 248 and 235 lapsed.
   - Effect: about +42 to the collection value. Our `neg_points` sit at the 50 cap, so the gain is likely capped or relative-only [L].
   - Dani should message t02 now. The offer expires at tick 1653, 40 ticks from now.
   - If it lapses, the fallback is 230, or Pilar at ≥198 only from 13:30 (Lucas's rule).
   - Confidence: med.
2. **Keep the bids for LAT-06/07/08 at 9 (offers 20331, 20332, 20680).** The operator keeps them live.
   - Evidence: LAT-06/07/08 are all asked at 30 by others, and t12 collects LAT.
   - Effect: a LAT card is worth 5 to us, so a 9 bid is a loss of about 4 each. These bids fit no page, so cancel them.
   - Check first that they are not meant to fill a LAT page for the ladder. If nothing in the data says so, cancel.
   - Confidence: low.
3. **Sell to the bidders for CHA-06/07/08 and CHA-09 only if the price clears our value.** Do not do this.
   - Evidence: t04 bids 20 and t09 bids 15 for CHA-06/07/08. CHA-09 draws 69. Our values are 146 and 218, because of the page bonus.
   - Effect: selling would break our completed CHA page. Do not sell.
   - Confidence: high.

   A better third action is the Workshop. Use spare copies of MAL, LAT or SAL (LAV-04 3.2, SAL-04 2.2) to make a card of the next rarity. The Saturday result was +11.8 collection value, with no neg or ladder change. It is executable via `POST /api/taller`.
   - Confidence: med.

## What the climbing teams are doing
- **t12 (#2, +1.3/15 min):** gets cheap cards from other teams: LAV-08 from t08 at 14, LAT-06 from t09 at 20 and LAT-10 from t01 at 86. It bought RET-11 from t06 at 216. It also bought 8 LAT cards and 2 MAL cards, and it collects RET/MAL/LAT.
- **t18 (#3):** closed its CHA page with a team trade, CHA-01 from t13 at 72. It also sold SAL-11 to t13 at 238. We copied the CHA-close method.
- **t8 (+1.3):** 78 deals. It is selling LAV/RET/LAT, which feeds t12's LAT/RET collection.

## Threats
- t12 is gaining, with a score of 32.2 against our 30.5. t18 is at 31.1, 0.6 above us and about 1.4 behind t12. Never sell LAT-08, MAL-03 or MAL-08 to t12, and keep every club pair on v10.
- t10 (#1, 33.3) collects LAV/RET. Our open RET-09/10 are bid at 68 by t09, but do not sell RET cards to t10.
- The ladder is capped, since 0.172 is near the expected cap of ~0.15 [L], so more dealer deals add little. The dealers close at 14:00.
