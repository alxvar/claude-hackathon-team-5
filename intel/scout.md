# Scout (claude-sonnet-5-5, Sat 17:54)

## Top 3 actions now

1. **SAL-06 page-closer (bid 14040, 35 P → t02 on v15, expires tick 944).** Operator keeps it live and countersigns up to 45 if t02 counters.
   - Evidence: /api/me/value SAL-06 = 82.1, page 9/10, so a 35 P close hits the +50 cap. Team trades are not capped: +15.5 neg moved `negotiating` 21.74 → 22.48 and the board 29.24 → 29.98.
   - Effect: about +47 neg, roughly +2.2 board (the directive's upper estimate; the measured rate is ~0.05/np, so ~+2.4).
   - Risk: expiry is at tick 944, about 25 ticks from tick 919. The ask must be 2× the ticks we want, and fallback is t17, then t13 at 18:20. If t02 does not hold SAL-06, the bid goes nowhere. Not in the data: whether t02 holds it.
   - Confidence: med.

2. **Room plan via Dani on v10: t02 SAL-03 → t08 and RET-03 → t07, t07 RET-01 → t09, all at ~9.**
   - Evidence: our `mm_points` moved +4.99 on a positive trade (t10 → t01 MAL-07 at 14), and the Market note says 2 trades ≈ the +5 cap. A trade to a holder with a lower multiplier or a 2nd copy goes negative (−5.2 on t15's SAL-07).
   - Effect: value created on v10 closes our market gap (7.5 vs 9.15–12.5), worth ≈ +3 board [L].
   - Dani asks the buyers to accept only after the sellers post. We never push SAL to a buyer holding a 2nd copy, and never to a rival.
   - Confidence: low-med.

3. **Spare LAV/MAL commons as maker.**
   - Offers: LAV-03 → t09 at 6 (13764, tick 933), MAL-02/05 → t15 at 9 (13715/13718, tick 931), and the LAV-02 spares (we hold three).
   - Evidence: the profile table shows t07 (#17, 10.6 below us) buying LAV ×7, RET ×5 and LAT ×4. The LAV-02 offer to t17 at 0 is not a sale (cash 0).
   - Effect: each team sale scored +2 to +4.7 neg. Re-post expiring offers at 2× ticks. Confirm t07 is still ≥ 10 below us before sending it a LAV spare.
   - Confidence: med.

## What the climbing teams are doing
- **Team 6 (#2, +3.3 in 15 min, 51 deals):** it moves RET cards among teams: RET-09 to t12 at 84 P (tick 895), RET-02 and RET-03 t12 → t06 at 6 P each (ticks 861 and 905). It also sold MAL-08 to t09 at 18 P (tick 853). That is high volume with cheap commons plus one rare flip.
- **Team 14 (#1, 31.4):** only 35 deals but the top score. It collects LAV/LAT and paid us 15 for MAL-08. Its lead comes from quality trades, not volume.
- **Team 7:** it is the busiest trader (t07: LAV ×7, RET ×5, LAT ×4). It sold RET-04 to t01, swapped with us, and bought RET/MAL commons from t03 plus LAV-10 (rare) for 38 P. It is the most active counterparty for our spares.

## Threats
- **Team 6 (30.7, #2) is 0.7 above us and rising** (+3.3 in 15 min); Team 14 is at 31.4. The board gap to #1 is 1.4.
- **t01 ↔ t10 alliance:** watch for trades on t01's venue that lift its market. t10 is at 27.7 and t01 at 28.7, both within 3.0 of us, so both count as rivals.
- **SAL-06 competition:** t10 buys SAL-06 (directive). A bid above 45 from them beats ours, and t02 may sell elsewhere. The offer expires at tick 944.
