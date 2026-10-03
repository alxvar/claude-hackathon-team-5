# Judge (claude-opus-5-5, Sat 23:36)

## Verdict
Holding #3 but stalled. 30.49, +0.0 over 15 min and −0.4 over 60 min. `neg_points` has been flat at 119.1 since tick 988 (≈457 ticks). Gaps: t18 is +0.8 ahead and climbing (+1.2/60 min); t12 is 0.1 behind; t10 is 7.1 ahead and flat.

## Our strategies: keep / kill / scale
- **Dealer bot: kill for Sunday except CHA buys at ≤ value.** The last thread (LAV-04 to Pícaros, 19:04) walked with 0 Δ. The ladder rose 0.437 → 0.483 but the board stayed flat (Chief 17:45). Flags are capped and done.
- **Trading loop: keep and restart on HEAD (918f823).** Its last fills were +6.2 (15:48) and +15.5 (17:46). Since then it logged only `sobre_bienvenida` errors and the 22:50-23:24 outage.
- **Spare asks 19979-19982: let them lapse at tick 1455.** No fills. Max gain ≈ +2.5 each. None of t04, t01 or t09 is ≥ 10 below us (Dani's table: "no buyer passes the feeding rule").
- **SAL-11 bid 20252 (115 → t04): keep the target, fix the timing (see change 1).** Unfilled since 21:45 under 19620/20252. Value 162 → +47 at 115, before pack drag.
- **In-room / Club Castizo on v10: scale.** Market is 7.5 (stall), the top is 12.5, and nobody beat the stall in six benches. The 22.5 "real trades" part is untouched, and the club engine is paused awaiting Lucas's go.
- **Duels (Aleks): keep.** 8 of the last 10 Duels II duels were deals; duel points 35.39.

## Check the scout
- Holds: MAL-07/09/10 are missing. t09 bids 56 on both MAL rares. t10 sold SAL-11 at 207 and bought MAL-11 at 195. t12 is #4 at 30.4. +47 = 162 − 115 at 0 fee as maker.
- Partly wrong: "cash 392 covers CHA ≈ 330". After 115 we hold 277; it covers CHA only with Sunday's +150 (427, per the 22:47 log). The 21:45 guardrail floor of 260 holds.
- Wrong: "never feed top 4 (t10, t06, t12, t14)". The board's top 4 is t10, t18, us, t12. t06 is #6 and t14 #7.
- Missed: t18, the only climber, is not listed as a threat.
- Wrong: re-posting spares to t04/t01/t09. They fail the ≥10-below feeding rule.
- Wrong: "MAL, never dealers" contradicts directive 21:00 ("dealer buys of MAL-09/10/06 first").
- Wrong: "MAL page value not in the data". It is 66.25 × 0.7 = 46.4 bonus.
- Missed: the round-reset risk on 20252 (change 1).

## The 3 changes with the highest expected gain
1. **CHA page from 09:00 (Lucas #1, ≈330 P → +3.2-5.6 final [L]).**
   - Check `/api/me` for the round-3 reset first.
   - Open the sobre_plata once CHA is released, before any team trade (pack drag cost SAL-06 ≈ 9.6).
   - Buy CHA commons, uncommons and rares at ≤ value: 16 / 40 / 112.
   - Buy the cheapest common last, from a non-top team, as maker.
   - Risk: CHA rares are scarce, and high-multiplier rivals outbid us.
2. **SAL-11: cancel 20252 now if the server allows it while closed; re-post 115 → t04 only after the reset shows in `/api/me`.**
   - Why: Saturday's reset fired at tick 160, after doors opened. A fill at tick 1446 may land before Sunday's reset and be wiped. Sunday's reset timing is not in the data.
   - Counter cap ≤ 125.
   - Effect: +37-47 `neg_points` ≈ +1.9-2.3 board (0.05 per point, Sat 17:46).
   - Risk: t04 fills elsewhere during the gap.
3. **Lucas gives the Builder the explicit go for the Club Castizo engine before 09:00. Lucas/Dani broker RET-09 t07 → t09 on v10 at open.**
   - Both are far below us (20.2 and 23.3); the Market list values it at +68 VC.
   - Effect: sim +89 VC ≈ 3.9-4.8 of 5 [L]. Only lever toward the 22.5.
   - Risk: an alliance rule change (contingency 18:40) stops it. Pay club bonuses only on settled v10 deals.
