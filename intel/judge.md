# Judge (claude-opus-5-5, Sun 01:10)

## Verdict
Holding #3 but slipping. 30.49 (−0.4/60 min) vs Team 10 at 37.6 (gap 7.1) and Team 18 at 31.3 (+1.2/60 min, gap 0.8). Team 12 is 0.1 behind at 30.4. Our neg_points have been flat at 119.1 since tick 988 (≈ 457 ticks without a scoring deal).

## Our strategies: keep / kill / scale
- **Team trades (page closers, in-room swaps): SCALE.** They are the only deals that moved neg_points Saturday: RET-01 +50.0, swap +15.5, SAL-06 from t08 +40.4. They also moved the board (≈ +0.05 per neg point, tick 910). LAV, RET and SAL are complete. MAL lacks MAL-07, MAL-09 and MAL-10, and CHA starts Sunday: those are the remaining levers.
- **Dealer bot / ladder: KEEP, as fodder only, after the CHA buys** (directive 00:44). Ladder rose 0.437 → 0.483. Board effect of the ladder was flat at 17:45 [L]. The bot behaved correctly: the Pícaros LAV-04 sale was walked at final 4 = opening, neg unchanged. The 8 threads at ticks 1367-1370 were all first = last with no price from us, so no ladder gain.
- **Trading loop: KEEP sells-only (cash floor 9999) until the cap patch is tested.**
  - It made only 2 accepts all Saturday (+6.2, +15.5).
  - Its log is mostly errors: `sobre_bienvenida` unknown_card ×5, and DNS failures 22:55-23:24. Check connectivity before 09:00.
- **Addressed asks 19979 / 19981 (LAV-03 / LAV-04 at 6): KILL.**
  - Addressed asks fill at 0.3% vs 3.5% for open asks (directive 00:37). These have no fill.
  - The gain is at most 2.8 P each, and the cards are better used as Workshop input.
- **SAL-11 bid 20252 (115): KILL at the first tick, as ordered.** It has not filled: the ask is 245 and the last trade was 207.
- **v10 venue VC: KEEP, zero negatives.** Saturday netted +4.99 then −5.2 (t15 dumping SAL). The target is 40-50 net by the close.
- **Duelist (Aleks): KEEP.** The last 10 session-3 duels gave 8 deals and 2 no-deals. Duel points are 35.39.

## Check the scout
- **Holds:**
  - SAL-11 cancel facts (ask 245, last trade 207).
  - RET-09 t07 → t09 is approved, and t07 is at 20.2.
  - t08 is only 5.4 below us, so we do not fill its bids.
  - Team 18 bought LAT-10 from t13 at 72.
  - Team 12 bought LAV-08 at 14 from t08.
- **Fails:**
  - "Team 10's venue v10 hosts the club deals" is wrong. v10 is OUR venue: the tick 311 and 398 trades on v10 moved our mm_points.
  - Team 12's LAT-06 came from t09, not t08.
  - "Team 12 racing us (+0.4)" is stale: the metrics show −0.1/15 min and −0.1/60 min. The real climber is Team 18.
  - "CHA needs 242-384 P" is stale. The current figures are A 242 / B 250 / C 282 (Lucas log 00:46).
  - Workshop "at 09:00" conflicts with the directive, which runs the Workshop and fodder AFTER the CHA buys.
- **Holds with a caveat:** the Workshop input LAV-02 ×2 + LAV-03 keeps at least 1 copy of each card. It is legal, and its neg effect is 0 [V].

## The 3 changes with the highest expected gain
1. **CHA page at round 3's first tick, closed by a team trade.**
   - How: Pícaros rares at ≤ 54, in parallel with capped public bids. Leave the last (cheapest) card for one addressed, agreed post from a non-rival, as maker.
   - Effect: up to +50 neg (the cap) on the closer. That is ≈ +2.5 board at the 17:46 rate [L].
   - Risk: print runs running out (SAL-11 was 9/9), or a rival flip of the last card.
2. **v10 row #1 (RET-09 t07 → t09) as the first trade of the day.**
   - How: WhatsApp-confirmed and addressed; then rows #5 and #6 after the 08:30 rival check.
   - Effect: +67.6 VC. It likely fills v10's real-trades target (full real trades = +5.0 board).
   - Risk: t07 or t09 not confirming. Any negative-VC trade on v10, like Saturday's −5.2, wipes the gain.
3. **MAL close, go/no-go at 10:30 on the M5 line.**
   - How: rares (value 49) only at ≤ 49 from Pícaros or teams. MAL-07 last, from a team.
   - Effect: the page bonus is 46.4 (66.25 × 0.7). The neg gain on the closer is capped at 50. The exact net is not in the data until the prices are known.
   - Risk: cash, since CHA comes first. A rare above 49 is a full dealer loss.
