# Scout (claude-sonnet-5-5, Sat 15:27)

## Top 3 actions now

1. **Watch for the Pícaros menu at the resume and run the Pilar-style ladder there (Operator).**
   - Evidence: tick 630 announced Los Pícaros ("Quick deals. Few questions.") and The Workshop. Our three Pilar deals are MAL-07 at 19, MAL-06 at 19 and SAL-08 at 23. The ladder is at 0.181 and a Pilar deal moved it +0.050 (L3).
   - Action: use the existing 20 s poll of /api/dealers/picaros. Sell spares only at ≥ our value, step −2/−3, and use `--offer-only` (never a deal at the opening price). Candidates: SAL-01/03/05, MAL-02/03 and LAT-03. Cancel the card's team ask first (e.g. 8776 SAL-01, 9087 MAL-02, 9025 LAT-03).
   - Effect: ladder gain only (neg unchanged, since gains are clipped). Confidence: med; Pícaros' rules are not in the data.

2. **Close the SAL-06 buy only at ≤ 25, then sell it to Pilar (Operator).**
   - Evidence: Abuela's thread is at 29 against our 21 (tick 629, open). Her earlier path was 29 → 25 with 25 held. Our bid 9168 (21, to abuela) expires at tick 634. Directive 12:58 moves A and B target Salamanca fever and a Pilar resale.
   - Action: move in small steps and never repeat a price; walk if no live offer for 4 ticks. Resell to Pilar at ≥ 25.
   - Effect: roughly +0.017 to +0.04 ladder if the Pilar sale replaces our weak L3 slot (≈ +1.4 board in the Analyst's model). Neg ≈ 0 if the buy is ≤ our value. Confidence: med.

3. **Keep swaps 9172 and 9173 live and chase small team sells (Operator, Dani).**
   - Evidence: t15↔t07 swapped 3× at ticks 607-616 at 0 P. 9172 (LAT-04 + MAL-04 → SAL-07, +14.3 for us) and 9173 (LAV-02 → MAL-01, +3.8) expire at tick 650. Team 7 (#17, 17.3) is the only buyer that passes the feeding rule, with a 9.5 est. for LAT-04, LAV-02/03/04 (+4.3 to +6.3 each).
   - Action: Dani pitches Team 7 on the LAV commons already addressed to others. Repost at the resume if they lapse.
   - Effect: about +4 to +14 neg_points. Confidence: low-med, since no counterparty has accepted yet.

## What the climbing teams are doing
- Team 14 (#1, 30.8, +1.1 in 60 min) is selling cheap commons to many buyers. It sent RET-02, RET-03, RET-01 and RET-04 to t04, t09 and t15 at 9 P each (ticks 591-598). It collects LAV/LAT and dumps RET/MAL. That is a high volume of small trades, 29 deals.
- Team 10 (#3, +4.1 in 60 min) bought MAL-10 from Team 3 at 74 P (tick 585), on its own venue. It is the top gainer after Team 6, with only 30 deals.
- Teams 15 and 7 swap card-for-card at 0 P (ticks 607-616). Both sides gain and no fee is paid.
- Team 6 (#9, +4.6 in 60 min) holds 19 team trades and 296 listings. Its gain is unexplained in the data.

## Threats
- Team 13 (#7) and Team 4 (#10) are bidding on RET cards. t04 bids 27 for RET-08 and 26 for RET-06 (our values are 100.4), and t13 bids 2 P on RET commons. This signals interest in our RET page; do not sell those cards.
- Our score is slipping (−0.8 in 15 min) while Team 14 and Team 12 sit above us. Team 14 has the lead on a Friday base we cannot match. Rank #5 → #4 needs +0.7 against Team 18 (28.8).
- Abuela's SAL-06 held at 25-29 while our cap is 25. If it does not move, the thread dies after 4 ticks and the slot is wasted.
