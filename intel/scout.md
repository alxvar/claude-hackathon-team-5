# Scout (claude-sonnet-5-5, Sat 15:38)

## Top 3 actions now

1. **Pícaros (new persona, L4) the moment its menu opens.** Executor: Operator, with the armed watch (20 s poll of /api/dealers/picaros).
   - Evidence: "Los Pícaros" was announced at tick 630 ("Quick deals. Few questions."). We already hold 3 Pilar deals: MAL-07 19, MAL-06 19, SAL-08 23.
   - Candidates (none are held for our pages): SAL-01 (2.2), SAL-02 (2.2), SAL-03/05 (9), MAL-02/03/04/05 (7), LAT-03 (5), LAT-04 2nd (1.2), LAV-02/03/04 2nd (3.2), MAL-09 (49).
   - Rule: sell only at ≥ our value, small steps, offer-only, never at the opening price.
   - Effect: a new level's ladder slots are empty. Pilar pays ~3× L2 (+0.050 vs +0.017), so expect about +0.02–0.05 ladder. How much a higher level pays is not in the data.
   - Confidence: med.

2. **Close the swap offers 9172 (→ t15) and 9173 (→ t07) before they expire at tick 650.** Executor: Operator, via trader.py (re-post addressed offers if they lapse).
   - Evidence: t15 and t07 swapped 3 times at ticks 607-616 for 0 P. 9172 gives LAT-04 (2nd) + MAL-04 and was priced at 0 P, which looks like a swap ask for SAL-07.
   - Check first: Team 15 is not top 4, #14, 21.5, so we are not feeding a leader.
   - Effect: 9172 is worth about +14.3 neg_points if it fills (Operator's estimate). It is the only live offer with real size.
   - Confidence: low-med. No reply is visible yet.

3. **Sell the 2nd-copy commons to Team 7 (#17, 10.6 below us), maker only.**
   - Cards: LAT-04 (value 1.2), RET-04 (2.8), LAV-03/02/04 (3.2 each) at ~9.5 est. (profile's estimate, not a live bid).
   - Evidence: the profile lists +4.3 to +6.3 gain each. Open asks 9101 (LAV-04 at 7 → t03) and 9136 (LAV-03 at 7 → t04) already exist.
   - Fix: 9173 (LAV-02 → t07) is the only offer to t07; repost LAT-04, RET-04, LAV-03 and LAV-04 to t07 at 9 once 9136/9101 lapse (ticks 665-667).
   - Effect: about +4 neg_points each. Spares count at only 25% of value, so we give up little.
   - Confidence: med.

## What the climbing teams are doing
- **Team 15** is #14 (21.5, +1.2 over 30 ticks) and the field's busiest trader: 22 team trades, 284 listings. Its trades are 0 P swaps with t07 (ticks 607-616), converting duplicates into page cards without paying fees.
- **Team 4** is active: 48 deals, LAT-11 epic sold to t16 at 160 (tick 631), RET-07 bought at 25 (tick 636), and 3 bids for LAT-09 (64), RET-08 (27) and RET-06 (26). It is buying exactly our RET cards, so those are our holdings to watch.
- **Team 12** (#2, +0.1) trades broadly (41 deals) and is the one top-4 team still rising.

## Threats
- **Team 4's RET bids at 26-27** cover the same cards we need, so it is competing for RET uncommons.
- **t17 bids 70-85 for MAL-09 (our rare, value 49).** Selling would add roughly +21 to +36 over value, but it is likely t17's page closer, and the feeding rule says no. Team 17 is #6, 25.8, 2.2 below us, and the "≥ 10 below" threshold is not met. Chief's call.
- **Team 14 leads at 30.7 and collects LAV/LAT.** LAV-09 and LAV-10 are our rares, so never sell it LAV cards.
