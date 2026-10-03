# Judge (claude-opus-5-5, Sat 21:44)

## Verdict
Falling behind the leader, barely holding #3. We are 31.2 (−0.4 over 15 min and over 60 min). Team 10 is 37.8 (+3.9 over 60 min), and the gap of 6.6 is widening. Team 6 is 1.8 above us and Team 3 is 0.9 below. `neg_points` has been flat at 119.1 since tick 988: no scored deal in about 300 ticks.

## Our strategies: keep / kill / scale
- **Dealer bot: keep off.** The Pícaros RET-11 buy at 136 (tick 1203; value 198) scored 0 `neg_points`, as expected, and earned the L4 upgrade. Ladder 0.437 → 0.483 did not move the board ([L], Chief 17:45). The LAV-04 Pícaros walk at 19:04 was correct (her final 4, our floor 4/ask 7).
- **Trading loop: keep, but it barely acts.** Its last fills were 15:48 (+6.2) and 17:46 (+15.5). There have been no fills since, and a rate-limit hit at 21:35.
- **SAL-11 bid 18605 (115 → t04): keep.** It is a first copy worth 162 and we are the maker, so no fee. The gross gain is ≤ 47, under the 50 cap. Pack drag on our sobre_plata (72.4) will cut it: the drag on SAL-06 was 9.6, and for SAL-11 it is not in the data.
- **MAL sells (18607 MAL-03 at 9, 18616 MAL-04 at 27, 18609 MAL-08 at 20): kill.** These are our only copies of page cards, and the 21:00 directive keeps the MAL page for Sunday. MAL-04, a common, at 27 is also far above the common clearing price of 9, so it won't fill anyway.
- **LAV spare sells (18606 LAV-03 at 6, 18608 LAV-04 at 6): keep.** Our copies are worth 3.2, so a fill gains about +2.8. Scale: list the 2 extra LAV-02 (1.3 each) and LAT-03/04 (5) at clearing prices, LAV-02 near 9 and LAT near 7.5.
- **DENY reactor: keep with the `pages_complete` filter.** The 21:39 RET-02 refusal was right: the target was stale and the buy would have cost −11 and paid t06.
- **v10 matchmaker / pair ads / rebate: scale.** Real trades are 22.5 of our 30 market-making points, the largest open lever. No v10 match has filled since the ads began at 21:24. `mm_points` now: not in the data.

## Check the scout
- **Holds:**
  - SAL-11 is worth 162; 392 − 125 = 267 is above the 260 floor.
  - t09 has no RET-09 bid on the board; its bids are MAL-09/10 at 56 and SAL-06 at 24.
  - The rate-limit hit at 21:35 is confirmed in the operator log.
  - The MAL-04 at 27 price is unrealistic.
  - Team 6 is a heavy rare/epic seller (ticks 1186, 1245, 1257).
- **Unverified:**
  - t04's SAL-11 asks at 212/245 are not in the metrics ask list.
  - "t10 trades on its own venue" is not in the data.
  - Our "−0.9/60 min": metrics say −0.4.
- **Missed:**
  - There is a live **RET-09 ask at 84 on El Rastro** (maker masked). If t09 takes it there, v10 earns nothing from the top match.
  - Recommending to "hold" the MAL sells contradicts the MAL-page directive.
  - The +2.3 estimate ignores pack drag.
- **Irrelevant:** t10's LAV-11 bid versus our RET-11. These are different cards, and RET-11 goes to Pilar only at ≥ 198.

## The 3 changes with the highest expected gain
1. **Close SAL-11 before tick 1305.**
   - Action: if t04 has not countered by tick ~1300, the Operator reposts the bid at 125, the guardrail max, addressed to t04 on v15.
   - Expected gain: +47 gross at 115 or +37 at 125, minus pack drag. At ≈0.05 board per point that is about +1.4 to +2.3 board.
   - Risk: t04 holds out (no SAL-11 ask is visible); then it's 0 cost.
2. **Land RET-09 t08 → t09 on v10 now, before the El Rastro ask at 84 is taken.**
   - Action: Lucas and Dani go in person to both teams. Ask t08 to pull its El Rastro ask (if it is t08's) and relist it on v10 addressed to t09 at ~100, with the 10 P rebate.
   - Expected gain: VC ≈ +134, possibly the full real-trades mark (5.0 × min(1, VC / top-3 mean)).
   - Risk: t09 buys elsewhere. The 84-vs-100 price gap may make t09 prefer El Rastro; offer the rebate to t09 instead if needed. Neither team is a rival (#11 and #16).
3. **Clean up the maker book.**
   - Action: cancel 18607, 18609 and 18616 (the MAL page cards). Post 6-8 spare-only asks at clearing prices: LAV-02 ×2, LAV-03, LAV-04, LAT-03, LAT-04. Address them to non-rivals ≥ 10 below us, with the trader at floor 350.
   - Expected gain: about +2 to +7 `neg_points` per fill, small but it ends the 300-tick flatline.
   - Risk: low fills (5% of asks filled on Friday); keep it out of the 5 req/s budget during Duels II.
