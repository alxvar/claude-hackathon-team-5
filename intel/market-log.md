# Market log (Market session; newest first)

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
