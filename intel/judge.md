# Judge (claude-opus-5-5, Sat 15:12)

## Verdict
Falling behind: #5 at 28.1 (−0.8 in the last 15 min, +1.8 in 60 min). The gap to #1 Team 14 (30.8) has grown from 2.19 at snapshot 570 to 2.7. Team 10 (+4.1/60) and Team 18 (+2.2/60) are pulling away. Our neg_points have sat at 35.2 since tick 404, and our ladder at 0.181 since ~12:45.

## Our strategies: keep / kill / scale
- **Dealer bot, Pilar/Chato sells above value**: keep. These were our last ladder gains: MAL-07 +0.050, MAL-06 +0.040, SAL-08 +0.019, LAT-08 +0.017, all at 0 neg cost.
- **Dealer bot, SAL-06 buy loop**: kill the Abuela route.
  - Three threads, no fill: Chato 32 vs our 26, Abuela 25 vs 22, Abuela now 29 vs 21.
  - SAL-06 is worth 22.5 to us (0.9 × 25), so buying it at the cap of 25 costs −2.5 neg.
  - An Abuela deal does not fill an empty L2 slot. Directive A says Chato at list 26.
- **Trading loop**: keep, since it costs nothing, but it is idle. No measured fill since tick 404, and the log shows only open/closed events.
- **Spare asks (9 live, 6-11 P)**: keep, but they score little. The only measured spare sale is SAL-01 at 7 (+4.7). Two flags:
  - LAV-04 → t03 and LAV-03 → t04 go to LAV collectors who are only 7.6 and 4.8 points below us, so they fail the ≥ 10 feeding rule if either card closes a page.
  - Repricing these to t07 (10.8 below us) is the safe version.
- **Swaps 9172/9173**: scale. +14.3 and +3.8 by our values, against #14 and #17. They expire at tick 650, only 20 ticks after the resume.
- **In-room trades / bargain watch**: the only big scorer today was RET-01 from t10 at 20 (+50 cap). No bargain hits are logged. We have no page one card from completion (MAL, SAL and LAT are all far), so a ≥ 50 bargain candidate is not in the data.
- **Venue (v10)**: the last reading was mm −5.2 at 11:30. The current value is not in the data.

## Check the scout
- **Holds**:
  - Swap arithmetic (22.5 − 7 − 1.2 = 14.3; 7 − 3.2 = 3.8).
  - t15 and t07 traded 0 P swaps at ticks 607, 613 and 616.
  - Pilar's uncommon median is 18 over 5 deals, so ≥ 25 is unsupported.
  - Selling RET-06/08 to Team 4 at 26-27 would lose ~73 each.
  - The leader moves and the Team 6 RET-09 sale at 84 match the feed.
- **Fails**:
  - "SAL-06 worth about 26, clips to 0, costs nothing" is wrong. It is worth 22.5, so 25 costs −2.5, and dealer losses count in full.
  - "Pícaros = L4 with a head start for 3 Pilar deals" is inference, not in the data.
  - The scout ignores The Workshop ("Three spares. One surprise."). All five of our spare duplicates are committed to asks or swaps right now.

## The 3 changes with the highest expected gain
1. **Land swap 9172 (SAL-07) and use that card for the L3 upgrade instead of buying SAL-06 from Abuela.**
   - Dani nudges t15 in the room now, while the clock is paused.
   - Re-post 9172 and 9173 with a longer life (ask 2× the ticks).
   - After the swap, sell SAL-07 to Pilar offer-only at ≥ 23 in −2/−3 steps, to replace the 0.019 slot. That move earned +0.040 with MAL-06.
   - Effect: ≈ +14.3 neg (≈ +1.3 board) plus ≈ +0.02 ladder (≈ +0.7 board).
   - Risk: t15 doesn't accept, or Pilar won't reach 22.5. In that case don't sell.
2. **Run the SAL-06 ladder buy only through Chato (directive A), and drop the Abuela thread.**
   - Abuela's 29 vs our 21 earns no L2 slot and costs −2.5 at the cap.
   - Chato at list 26 costs −3.5 neg (≈ −0.33 board) for an L2 slot (≈ +1.2 board per directive, [Likely]).
   - Risk: his last price was 32, and his L2 deals above list never counted. Walk if he finals above 26.
3. **Pícaros at the resume: one offer-only thread, sells only above value, small steps.**
   - Candidates: SAL-01/03/05 (value 9), MAL-02/03 (7), LAT-03 (5).
   - Measure Δladder after the first deal before a second one. Keep 3 spares unlisted until The Workshop's rules are read.
   - Effect: not in the data. Pilar's comparable sells gave +0.02 to +0.05 ladder.
   - Risk: the level's pricing and unlock rules are unknown; never accept the opening price.
