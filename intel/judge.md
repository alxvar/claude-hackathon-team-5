# Judge (claude-opus-5-5, Fri 21:55)

## Verdict
Holding at #8: 17.8 vs leader Team 13 at 27.8 (gap 10.0), 1.8 behind #7. `neg_points` has been flat at 26.3 for 15 min. The board's +0.0 over 60 min for every team contradicts our own 16.6 → 26.3 jump at 21:46, so the leaderboard score column may be stale. Verify it before trusting the deltas.

## Our strategies: keep / kill / scale
- **Dealer bot:** keep for the ladder only (0.064, level 1). The MAL-07 thread stalled at Abuela 27 vs our 19 with no deal logged, and dealer deals don't move `neg_points`. Fire Chato's 3 ladder deals the moment he opens.
- **Trading loop (`loop.py`):** suspect it is dead. Its only logged event is a `rate_limited` error at 21:50:30, with no fills since. The server also restarts around tick 94. Restart it with throttling.
- **Autoflip:** scale. It is live, but no flip events have appeared since 21:45. Its ≥8 threshold blocks the open flips. t17 bids 26 for MAL-07/MAL-08, and accepting gives 26 − 17.5 (25×0.7) − 2.3 fee = +6.2 per fill. Cash spent at Abuela never enters `neg_points`.
- **LAV-09 bid at 91:** kill, unless Lucas confirms we hold LAV-06/07. Team 10 now bids 110, so ours won't fill and no longer blocks them. Even if it filled, 91 − 91 = 0 points.
- **LAV-04 asks at 10 ×2:** keep only for spare copies (2nd copy worth 3.25, so +6.75). A first copy is worth 13, so selling at 10 loses 3. Time unfilled: not in the data.
- **SAL-06 ask at 30:** reprice. No SAL-06 bid exists, and uncommons trade at 22–27 between teams. A spare (worth 5.6) at 22 scores +16.4. A first copy (worth 22.5) must stay ≥25. Copy count: not in the data; check `/api/me`.
- **In-room trades:** scale. The big movers are rares (65–80 P), and only humans can find holders.

## Check the scout
- **Holds:** a MAL rare is worth 49 to us, so don't bid above it. Selling one into t17's 78 bid gains about 24–29. Team 18 is #2 with 9 deals after the SAL-10 trade at 80. t15 bought LAT ×10. Team 13 buys MAL/SAL and Team 10 buys LAV. `neg_points` is flat at 26.3.
- **Wrong:** "our MAL-09/10 bids at 38". Those bids are owner "?", and our open offers list only LAV-04 ×2, SAL-06, and LAV-09.
- **Wrong:** "keep LAV-09 at 91 because Team 10 bids 90". That is stale; Team 10 now bids 110.
- **Wrong:** "SAL-06 value not in the data". It is 22.5 for a first copy or 5.6 for a 2nd; only the copy count is missing.
- **Wrong:** "others are catching up". Every team shows +0.0.
- **Misframed:** Team 15 is not in the top 10, so selling LAT to it does not feed a leader. Team 18 (#2) and Team 8 (#3) are the ones to avoid.

## The 3 changes with the highest expected gain
1. **Lower the autoflip threshold to ≥5 and target t17's MAL-07/MAL-08 bids at 26.** t17 is not a leader.
   - Effect: about +6.2 per fill; two fills is roughly +12, a 46% lift on 26.3. It fits inside the 8 deals/hour cap and 380 cash.
   - Risk: the bid vanishes mid-flip, as Team 8's 35 bid did. We would then hold a 27-P card. That costs cash only (zero points), and the card can be relisted.
2. **Dani and Lucas find the MAL-09/MAL-10 holders in the room. Buy at ≤60, then sell to t17 with an ask addressed `to` t17 at 78, so t17 accepts and we pay no fee.**
   - Effect: the buy leg scores 49 − price and the sell leg 78 − 49, so about +18 net at a 60 buy, or +29 if we already hold one. Skip t18's LAT-09/10 bids at 55, because t18 is #2.
   - Risk: t17 pulls its bid after we buy, leaving the buy leg at −11.
3. **Right after the tick-94 restart, check and restart `loop.py`, autoflip, and the collector with backoff under 5 req/s. Cancel the LAV-09 bid in the same pass.**
   - Effect: protects every automated gain. Verifying the collector also tells us whether the leaderboard is actually stale.
   - Risk: low; we may lose a few ticks of fills while restarting.
