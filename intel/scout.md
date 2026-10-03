# Scout (claude-sonnet-5-5, Sat 12:23)

## Top 3 actions now

1. **Pilar sells: MAL-07 then MAL-06, offer-only, ask 30, steps of 3, floor 18, Operator via `abuela_bot.py --dealer pilar --offer-only`.**
   - Evidence: Pilar is open to all at tick 502, and her uncommon final is 18-19 (metrics: "pilar uncommon (team sells): median 18 over 3"). Offer 7376 (MAL-07 at 30 to pilar) is still open and expires at tick 507, so re-post it with a longer life: ask 2× the ticks wanted. MAL-07 and MAL-06 are each worth 17.5 to us, so a close at ≥18 costs 0 neg.
   - Effect: a sell above her opening bid (16) should move the L3 ladder. The Chato LAT-08 precedent moved it +0.017 (≈ +0.33 board per 0.01). Our level is 3.
   - Confidence: med (n=1 for sells moving the ladder; the Pilar rate is unmeasured).
   - Measure the ladder delta after the first deal and stop if it does not move. The thread must be alone in its window and the offer-only rule applies.

2. **Sell SAL-08 to Pilar only at ≥ 23 (our value is 22.5).** Operator, offer-only.
   - Evidence: the t03 offer 7238 at 25 is still open. The directive 12:13 says SAL-08 → Pilar. Her SAL fever is not yet confirmed by the metrics.
   - Effect: a possible second ladder deal at no neg cost. If t03 accepts at 25, we gain +2.5 over value with no neg effect. Cancel 7238 before opening the Pilar thread.
   - Confidence: low-med.

3. **Hold the RET page: do not sell RET-09/10 or RET-06/07/08.** We hold all of RET 01-10 (RET-01 to 05, RET-06/07/08, RET-09/10). Team 2 bids 59 for RET-10 (offer 7262), well below our value of 149.9. Decline it.
   - Evidence: the metrics list RET holdings at 83.9-149.9 per card. Selling at 59 would be a large loss.
   - Effect: protects the value of the collection. Our LAV page is complete (LAV-01 to 10 held), so check whether our extra RET cards close the RET page via a team trade, which scores up to +50 per trade.
   - Confidence: high on "no sale". The RET page-completion path is [Open]: its gaps are not in the data.

## What the climbing teams are doing
- **Team 12 (#1, +5.8 in 15 min)** collects RET/MAL and dumps SAL/LAV. It has 24 dealer trades with Abuela at −23.1%, and the feed shows trades such as SAL-05 to t09. It is ahead of us and is not to be fed.
- **Team 17 (#6, +1.7 / +6.4 over 60 min)** buys MAL×3 and SAL×3 from teams and earlier took SAL-09 at 75. It is on the page path for MAL/SAL.
- **Team 14 (#2)** collects LAV/RET/LAT. It bought LAT×4 and RET×2 and took RET-08 from t13 at 20 (tick 370).
- **Team 15 (#12 in rivals, +4.7)** has 17 team trades, buys LAT×6, MAL×3 and RET×2, and is the main MAL/LAT sink for our spares.

## Threats
- **Team 2 and Team 18 buy RET** (Team 18 collects RET/LAT). They may compete for the RET cards we hold, and Team 2 has bids on RET-02 and RET-10.
- **Team 13 (#3) keeps feeding on venue trades** (MAL×6 and SAL×2 buys). Avoid selling it MAL/SAL, and do not trade on v03.
- **Our `mm_points` is −5.2.** A sale to a lower-multiplier buyer on v10 reduces it. Only collector-buys should happen on our venue.
