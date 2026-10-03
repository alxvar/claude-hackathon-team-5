# Scout (claude-sonnet-5-5, Sat 16:46)

## Top 3 actions now

1. **Close the SAL-10 buy from Los Pícaros (offer 11903, thread open).**
   - Action: Operator, offer-only with small steps, cap 56 (GUARDRAIL cap ≤ 63, floor 70). Check that the structure is exactly card:SAL-10 for cash only. Their price is 73 → 73 against our 44, so step +2/+3 and never jump to their price.
   - Evidence: SAL-09 at 54 moved the ladder 0.200 → 0.270 (+0.070) with 0 neg. Offer 11903 expires at tick 784, so it needs a fresh offer.
   - Effect: a second L4 slot, about +0.05-0.07 ladder (≈ +1.4 board per the directive). neg_points stays 0 as long as the price is ≤ 63, our value of SAL-10.
   - Confidence: med.

2. **Flag only live Pícaros threads, and only on false facts or words ≠ the structured offer.**
   - Action: Operator, on the open SAL-10 thread. Flag a message only if it has a checkable false fact (print run, "last one") or a card/price mismatch with the structured offer. Never flag finality or deadline talk.
   - Evidence: neg_points 43.2 → 53.2 → 63.2 → 73.2, then −10 → 63.2 (the church-bell flag). Flag 5 (7225) on a closed thread scored 0 so far.
   - Effect: +10 neg per correct flag (≈ +0.7 board each).
   - Confidence: med. Whether a flag on a closed thread counts is open.

3. **Sell page-closer spares to Team 7 only (#17 in profiles, 10.6 below us).**
   - Action: Operator on El Rastro, addressed `to` t07, after `tools/policy.py can-give`.
   - Evidence: our only LAT-04 spare shows value 1.2 vs est. 9.5, so +6.3 by the profile table. The same table gives LAV-02, LAV-03 and LAV-04 +4.3 each and RET-04 +4.7. Our own asks to t03/t16/t09 (offers 11377, 11379, 11426, 11460, 11530) are already live.
   - Effect: about +4 to +6 neg per sale.
   - Confidence: med. The 9.5 prices are estimates, not live bids. The profile data is from tick 631 and may be stale, so check can-give and Team 7's current standing first.

## What the climbing teams are doing
- **Team 3 (+7.2 in 60 min, #7)** and **Team 16 (+4.2)** are buying: Team 16 took LAT-09 (rare) at 88 from t16→t03 (tick 724) and has bids up on RET-07, LAV-06, RET-01 and others (8-15 P). Their rises come from cheap team trades and bids.
- **Team 1 (+3.8 in 60 min, #4)** buys MAL×4 and SAL×4 in team trades, a steady diet of commons.
- **Team 14** accumulates cheap commons from sellers (RET-04 from t06 at 5, tick 766; LAT×4, RET×3). It is #2, 0.2 behind us.

## Threats
- **Board compression:** #2 Team 14 is 0.2 behind us and #3-#5 are within 1.0. A drop in neg_points would cost us the lead.
- **Pícaros SAL rares are going to the field:** Team 8, 9, 10 and 16 unlocked L4 at tick 761, and Team 10 is already a top-5 team. Public SAL-10 bids (t06 has 68 on SAL-09) make the price drift up.
- **Flag copying:** the Pícaros lies are in the public feed, so the field will copy the flag lever soon and the +10s will dry up. Use them now.
