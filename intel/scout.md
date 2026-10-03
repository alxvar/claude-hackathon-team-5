# Scout (claude-sonnet-5-5, Sat 18:21)

## Top 3 actions now
1. **Close the SAL page with SAL-06 (team trade only).**
   - Action: keep maker bid 14557 (50 P, to t13, expires tick 973). The Operator's job at 18:21 cancels it and posts 50 → t17. The t02 ask watcher stays armed (≤ 60, floor 85). Dani keeps pushing t02 at 50 in person.
   - Evidence: /api/me/value SAL-06 = 82.1, page 9/10. Bid 14557 expires at tick 973 and the metrics are at tick 971. Cash is 151 and the GUARDRAIL floor is 85 for this close only.
   - Effect: about +32 neg_points at 50 P (82.1 − 50), with the cap at 50. Board ≈ +0.05 per np (Sat 17:46 measure, [V]), so ≈ +1.6 board.
   - Confidence: med. t02 anchors at 120 and t13 has not answered.
   - Re-post the bid now so it does not lapse at tick 973. Ask for 2× the ticks, because the server halves `expires_in_ticks`.
2. **Push the v10 market lever to catch t06 and t14 (we are #3 at 30.0; t06 is 31.7).**
   - Action: Dani asks t09 to accept our posted sells (MAL-03 at 9, LAV-03 at 6), and the Operator posts the MAL/RET spares for t15 only where t15 holds 2 copies. All of it goes on v10 or v15, never on a rival's venue.
   - Evidence: 17:40 directive, "1 trade ≈ mm 0 to +5, 2 ≈ the +5 cap". Our gap is market, not negotiating. A card moving to a lower-multiplier holder subtracts, so the 2nd-copy rule applies.
   - Effect: up to +5 mm_points, ≈ +3 board [L].
   - Confidence: low-med.
3. **Do nothing with the free-LAV-02 and LAV-04 asks, and let the three 0-price offers expire (ticks 976-980).**
   - Action: no re-post. Those spares are worth 1.3-3.2 to us. They fed the swap/page-completion pitches, but the feeding-rule table shows no buyer that passes (≥ 10 below us).
   - Evidence: "no buyer passes the feeding rule". Value created is net and can go negative.
   - Effect: avoids feeding rivals.
   - Confidence: med.

## What the climbing teams are doing
- **Team 6 (#1, 31.7, +4.4 per hour):** collects SAL and sells MAL/LAV/LAT. It has 555 listings and 52 deals. It sold RET-09 to t12 at 84 (tick 895) and RET-03 for 6 (tick 905). Volume as a maker plus rare sales is working.
- **Team 14 (#2, 31.5):** collects LAV and RET, and buys LAT cheaply. At tick 946 it bought RET-03 from t02 for 7 P, and at tick 939 it swapped SAL-04 for MAL-05 with t16. Small swaps and low-price commons.
- **Team 3 (#4, 29.6, +0.4):** its negotiating score is the highest. It sold LAV-03 to t04 at 6 (tick 904) and MAL-02 to t17 at 3 (tick 929). Its sells are cheap and it is not at the bottom for dealers (Abuela −23.2%).

## Threats
- **t02's anchor at 120 for SAL-06, plus Pilar's fever price of ~31 for SAL.** If the rivals are slow, the page close stays open.
- **Team 3 (29.6) and Team 10 (28.3) are 0.4 and 1.7 behind us.** Do not feed either of them. t10 is allied with t01 and must get nothing.
- **Team 6 and Team 14 are 1.7 and 1.5 ahead.** Any v10 trade that helps t09 or t15 is fine, but never trades that lift their venues or their page closes.
