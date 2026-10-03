# Market log (Market session; newest first)

## Sat 10:50 · FIRST TRADE ON v10: +4.99 market points [V]
- Tick 311 (10:45): Team 10 sold MAL-07 to Team 1 on v10 at 14 P (fee 0). Team 10's first offer on v10 was tick 263.
- **Our market: 7.32 (snapshot 310, = stall teams) → 12.47 (snapshot 320); stall teams 7.48. Gap +4.99 from one trade.**
- Team 12 reads exactly 12.47 too (one 7 P trade on v02). Two venues with different trades (7 P and 14 P) and the same
  gap → the value-created part looks capped or scored against the top three, like the bench [L]. If so the bar rises as
  more venues get trades: what matters is staying in the top three by value created, so keep trades coming on v10.
- Reciprocal count: v10 1 trade (14 P, with t10) · our trades on v07: 0 · v07 total: 0.

## Sat 10:20 · reciprocal venue deal with Team 10 (Chief): tracking started
- Their standing offers → our v10, ours → their v07, both 0%. Page-closing trades stay on El Rastro.
- **Baseline [V, snapshot 260]:** stall teams 6.23 · us 6.23 (+0.0) · t10 6.23 (+0.0) · t12 10.39. The market number
  drifts up every snapshot for everyone (round growth: 4.8 → 5.23 → 5.61 → 5.94 → 6.23), so attribution = our gap to
  the stall teams' number.
- v10: fee 0 since tick 230; 0 trades. Team 13 listed asks at tick 233-234 (LAV-01 5, LAT-02 6, SAL-03 9). v07: 0 trades.
- Alerts armed: ratio > 2:1 against us · no t10 trade on v10 within 30 min of their switch · crossing offers on v07
  unmatched > 3 ticks · our gap disappearing.

## Sat 10:03 · sim with staggered arrivals (first calibration, hand-set from the bench 3.0 trace) [L, model]
- `staggered-20` (20 traders, arrivals over ticks 0-10, limits 20-110, shade 0.1-0.4, short lives), 300 seeds:
  auto_clone 0.883 (real stall: 0.899), **v1 0.871 = −1.2 pp vs the stall** (worse in 52, better in 26, worst −28 pp),
  quote-oracle 0.969 (**+8.6 pp of room**). `staggered-20-firm`: 0.825 / 0.818 / 0.925.
- **Reading:** with arrivals over time, v1's extra pairs use up traders that later arrivals needed. v1 fails the gate;
  do not deploy it. The room is large, and it sits in waiting for better partners, not in matching more.
- **10:02** v10 fee → 0 from tick 230 (Lucas ran `set_fee`), announcement posted. Watching v10 trades and our market.

## Sat 10:00 · bench-h03.0 (ticks 201-217), on the free stall v10 (auto, fee 3%)
- **Ours [V]:** bench_efficiency 0.899, bench_points 0.5, market 4.8 at snapshot 220.
- **Field at snapshot 220 [V]:** all 11 stall teams 4.8. Board venues: t02 (v04), t04 (v05), t10 (v07) 4.8; t08 (v06) 4.75;
  t06 (v01) 3.66; t13 (v03, fee 1%) 2.13. **No board broker beat the stall; three did worse.** t12 (v02) 8.01.
- **Value created [V]:** the only settlement ever on a team venue is tick 203, v02, t15 bought MAL-03 from t13 at 7 P.
  t12's market went 0 → 11.49 (snapshot 210, bench still running) → 8.01 (220). So one 7 P trade is worth ~3.2 market
  points over the bench's 4.8 while no other venue has trades [L: 8.01 = 4.8 + 3.2].
- **Recording [V]:** the stall exposes `bench_offers`, but only what its engine left after crossing: 19 book states,
  12 ids seen (buyers b10-0..9, sellers b10-10..16), `recent` always empty, so no settlements. Replay proxy is 1.000 for
  every strategy: **a stall recording cannot measure a broker's edge.** Real replay evidence needs our own board venue.
- **Traders [V, 1 session]:** arrive staggered over ticks 202-211; buyers raise bids (41, 46, 51, 60, 60), sellers cut asks
  (129, 114, 106, 106), steps of 5-15 with pauses; every offer carries `expires_tick` 217 (session end, not per trader).
- **Decision:** no venue (Chief/Lucas 09:55). Stall efficiency 0.899 leaves up to ~10 pp of room, more than our sim's 5.
- **Blocked:** setting v10's fee to 0 (Chief's GO 09:59) was denied by Claude Code's permission system; needs Lucas.
- **Next:** calibrate `sim.py` on this trace; second trace at bench 5.0 (~11:50).
