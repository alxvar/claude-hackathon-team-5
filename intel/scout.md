# Scout (claude-sonnet-5-5, Sat 14:14)

## Top 3 actions now
1. **Keep swaps 9172 (t15) and 9173 (t07) live, and re-time them for the unpause.** The clock has been paused since tick 630, so both offers expire at tick 650 unrefreshed. The Operator (trade.py) re-posts them at 2× the ticks wanted, since the server halves `expires_in_ticks`. Evidence: t15↔t07 swapped 3× at ticks 607-616 for 0 P, and the Operator's log shows 9172 at +14.3 and 9173 at +3.8 for us. Effect: up to ~+18 neg_points (≈ +1.7 board at 0.094) as maker, no fee. Confidence: med. Neither team is in the top 4 (t15 21.9, t07 17.3).
2. **Finish SAL-06 from Abuela (thread 868, cap 25), then sell it to Pilar at ≥ 25 with small steps.** Evidence: her 29 → 25 earlier, we held at 22 and the offer expired; the current thread is at 29, ours 21. Pilar uncommon finals are 18-19, and her SAL-08 deal closed at 23 (+0.019). Move by −2/−3 steps and never repeat a price; she mirrors step size. Effect: the buy is loss-capped (value 9×? SAL is 0.9, so 22.5; at 25 that is ≈ −2.5 neg), and the Pilar resale gives about +0.02-0.04 ladder (≈ +0.7-1.3 board). Confidence: low-med. Whether SAL-06 sells to Pilar at ≥ 25 is not in the data; her measured uncommon range is 18-23.
3. **Hold the one lunch-bargain buy slot (≥ 50 gain, ≤ 100 total) on the bargain watch.** Lucas's guardrail applies: seller outside the top 5, value re-read first. Evidence: a page-closer scored the +50 cap twice (LAV-05, RET-01). The LAV-11-style buy is the use case; LAV-11 itself (Team 8, #13) is outside the top 5. Effect: up to +50 neg (≈ +4.7 board). Confidence: low; nothing has hit `logs/bargains.log` yet.

## What the climbing teams are doing
- **Team 14 (#1, 30.8)** is a high-volume common seller: RET-01/02/03/04 sold to t15/t04/t09 at 9 each (ticks 591-598). It collects LAV/LAT and dumps MAL/RET.
- **Team 10 (#3, 28.9, +4.1 in 60 min)** bought MAL-10 from Team 3 for 74 P (tick 585). The profile shows a 197-listing book, and it is the team that sells us RET-01.
- **Team 18 (#4, 28.8, +2.2 in 60 min)** is climbing while holding steady at 29 deals. It collects RET/LAT and dumps MAL/LAV. Its +2.2 is not explained by any trade in the metrics.
- **Team 6 (#9) gained +4.6 in 60 min** and sells MAL/LAT/LAV. The trade that drove it is not in the data.

## Threats
- **Team 12 (#2) and Team 14 (#1) both collect LAT/RET.** Any RET or LAT card we sell to them feeds a top-4 team; avoid it (the feeding rule).
- **Our score is falling:** −0.8 over 15 min while the game is paused. The relative scale is moving against us. The gap to Team 14 is 2.7 points.
- **Team 13 (#7, 57 deals, −1.2) is pushing trades onto its venue v03**, and trades there feed it. We accept there only for gains ≥ 15.
