# Judge (claude-opus-5-5, Sat 16:01)

## Verdict
Holding, slightly gaining: #5 at 28.34 (+0.4 / 15 min, +0.2 / 60 min). Gap to #1 t14 is 1.94 (t14 −0.4 / 60 min) and to #4 t10 is 0.3. neg_points went 32.5 → 38.7 in 15 min; ladder is 0.188.

## Our strategies: keep / kill / scale
- **Dealer bot, Pilar sells of held cards**: keep. The SAL-06 sale at 25 was clean (neg unchanged, ladder +0.007). The shares are shrinking, though: +0.050, +0.040, +0.019, then +0.007.
- **Dealer round trips (buy from Abuela, resell to Pilar)**: kill. SAL-06 cost −2.7 neg (pack drag) for +0.007 ladder, which is break-even at best. Abuela L1 is full, so the buy added no ladder.
- **Trading loop**: keep. It made 1 accept since the resume, the t08 swap at +6.2, exactly as predicted. Before that it was idle.
- **Our maker book**: scale. There are only 6 live asks against the plan's 20-30. Fills since the morning: SAL-01 → t03 (+4.7) and MAL-03 buy (+2.0). 9554 (MAL-02 at 9) expires at 698 unfilled, and two other asks already sit at MAL-02 9.
- **Manual swaps 9387/9389**: kill the reposting. Both were posted twice and expired unfilled at tick 688.
- **Bargain-buy guardrail (≥50 gain, ≤100 P)**: no candidate in the data. Keep the monitor; no action.
- **MAL-09 / LAT-08 holds for Pícaros**: these follow the Chief's call. t17 bids 70-85 for MAL-09, so we would gain 36 against its up-to-50 as a closer. That trade is barred by the 15:55 policy; correct.

## Check the scout
- **Holds**:
  - SAL-01 → t03 gave +4.7.
  - All 6 asks are addressed to safe teams.
  - t13 bids 2 P for RET commons.
  - #1-#4 are within 2 of us.
  - Team 2 bought RET-09 at 84; its SAL-09 bid is at 69.
- **Wrong: "RET-04 spare" (action 2).** The swap at tick 669 gave away our 2nd RET-04. Holdings now show a single RET-04 at 83.9, so selling it breaks the RET page. Dani's table (tick 631, "2 copies") is stale.
- **Wrong: "t07 bought MAL-03 and MAL-01".** The feed shows t07 *sold* both, to t04. t07's 9.5 is a median estimate, not a live bid, so +15-20 neg is overstated (only 4 eligible cards, about +4 each, unfilled).
- **Wrong: Team 4 "building the RET page".** It also sold RET-06 to t09 at 28 (tick 683), so it is flipping as well as collecting.
- **Not in the data**: Team 2's 63 bid.
- **Unsupported: "Let Pilar fill on below-list sells"** (action 3). The measured rule for sells is a price *above the dealer's opening bid*, with small steps.

## The 3 changes with the highest expected gain
1. **Fill an empty L2 (Chato) slot at zero neg cost.**
   - Move: sell LAT-08 (value 12.5) to Chato, offer-only at ≥ 14, alone in its window, small steps.
   - Evidence: the same move measured +0.017 ladder (≈ +0.56 board at 0.33 per 0.01). Our other Saturday Chato deals were buys above list and never counted, so 2 slots are likely empty.
   - Risk: it uses the card the Chief reserved for Pícaros L4, whose value is not in the data. The Chief decides. His second thread may final at 13 (MAL-07 walked at 13-14); walk below 14.
2. **Scale the maker book from 6 to ~15-20 asks, addressed to safe teams that collect the set.**
   - Cards:
     - 2nd LAV-02 (3.2) → t09/t07 at 6-8
     - LAT-04 ×2 (1.2) → t16/t15/t03 at 4-6
     - MAL-03/04/05 (7) → t15 at 8-9
     - SAL-03/04/05 (9) → t08 at 10-11
   - Re-post 9554 before 698. Price at or under others' asks (LAV-04 10, MAL-04/05 9, LAT-04 4).
   - Expected: +2 to +5 neg per fill (≈ +0.19-0.47 board), no fee as maker.
   - Risk: low fill rate (Friday filled 5% of asks); check each buyer's set progress for closers; never list the last RET/LAV copies.
3. **Replace the manual swaps with the `swaps` daemon once the 2 verifiers clear it.**
   - Expected: dry-run best +10.3 / +9.7 neg.
   - Settings: safe-team counterparties only, El Rastro or a bottom-team venue (v11 was fine).
   - Risk: the engine is unverified; a swap can hand a buyer its page closer, so apply the feeding rule (≥ 6 below) per leg.
