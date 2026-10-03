# Market log (Market session; newest first)

## Sun 00:30 · CORRECTION to the 21:15 entry: the deck split was backwards [V, intel/market-test-audit.md]
- The Payday slide reads **Market Test 22.5 + Real trades 7.5**, not 7.5 + 22.5. The 21:15 entry took the numbers from
  the 21:10 directive. Consequences: (1) the stall's 7.5 on the board is HALF the Market Test, not its maximum: the other
  11.25 round points are unclaimed by every team; (2) +5.0 on the board is the FULL real-trades score (7.5 round points =
  3.0 final on Sunday): there is no 22.5 to unlock on v10.
- Unchanged: keep the stall (no broker of ours beats it in the sims; 51 rival board sessions, none above it); the
  real-trades fit (top-three mean); spares only, no negative trade.
- Changed: "the bench is maxed, no broker upside" is withdrawn. The upside exists; we have no broker that takes it. Desk
  question now: does one venue beating the stall by a hair get full Market Test points?
- VC scale: Saturday's top-three mean was ≤ ~15 units (audit §3b); my first sim assumed ~60-150. Sunday's target is
  about 30-50 net VC at the close, not 170. `mm_points` read +2.2 at the close with no new trade [V], market still 7.5.
- `intel/market-sunday.md` §0 (negotiation model; two verifier passes applied), §1, §4 and §6 rewritten accordingly.

## Sat 22:50 · bench-h13.0 (ticks 1401-1414), on the stall v10: Saturday's last
- **Ours [V]:** bench_efficiency 0.854 (0.899 · 0.933 · 0.878 · 0.891 · 0.886 before), bench_points 0.5, market 7.5.
- **Field at snapshot 1420 [V]:** t10 12.5 · t06 11.87 · t09 10.89 · t16 10.16 · t14 9.3 · t17 8.64 · t08 8.45 · stall
  teams 7.5 (us, t18, t15, t11, t07, t04, t02, t01) · t12 7.25 · t13 6.77 · t03 6.08. Six benches, nobody above the stall.
- **Saturday's market result for us: 7.5 of the 12.5 seen at the top.** The whole gap is real trades: v10 had 2 fills
  all day (+4.99, then −10.2), mm −5.2. The rebate (21:15-23:00) got no listing; 0 P owed.
- Sunday plan: `intel/market-sunday.md`.

## Partner audit · Sat 22:38 · tick 1401 · snapshot 1400: stall teams 7.5 · us 7.5 (+0.00)
- **Team 15** (v15, market 7.5 = +0.00): on v10 0 open offers, 1 trades (26 P) · ours on v15: 5 open offers, 0 trades (0 P)
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
- **Team 10** (v07, market 12.5 = +5.00): on v10 0 open offers, 2 trades (40 P) · ours on v07: 0 open offers, 4 trades (32 P)
  - v10 trade tick 311: [('MAL-07', 't10', '→', 't01')] at 14
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
  - our trade on v07 tick 351: [('SAL-01', 't05', '→', 't03')] at 7
  - our trade on v07 tick 404: [('MAL-03', 't04', '→', 't05')] at 5
  - our trade on v07 tick 714: [('MAL-01', 't06', '→', 't05')] at 5
  - our trade on v07 tick 760: [('MAL-08', 't14', '→', 't05')] at 15
- **Team 3** (v20): no deal yet, nothing on v10.
- **Alerts:** Team 15: 0 offers and 0 trades on v10, 385 min after the deal; Team 15: no open offer on v10 now (1 trades so far); Team 15: offer imbalance, ours on v15 5 vs theirs on v10 0; Team 10: no open offer on v10 now (2 trades so far)
- **Rebates owed (10 P a card sold on v10 since tick 1228, max 2 per team, cap 80; rivals t10 t06 t14 t03 t18 t13 t17 excluded, t01 t16 re-checked at payout):** none · total 0 P

## Partner audit · Sat 22:08 · tick 1341 · snapshot 1340: stall teams 7.5 · us 7.5 (+0.00)
- **Team 15** (v15, market 7.5 = +0.00): on v10 0 open offers, 1 trades (26 P) · ours on v15: 5 open offers, 0 trades (0 P)
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
- **Team 10** (v07, market 12.5 = +5.00): on v10 0 open offers, 2 trades (40 P) · ours on v07: 0 open offers, 4 trades (32 P)
  - v10 trade tick 311: [('MAL-07', 't10', '→', 't01')] at 14
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
  - our trade on v07 tick 351: [('SAL-01', 't05', '→', 't03')] at 7
  - our trade on v07 tick 404: [('MAL-03', 't04', '→', 't05')] at 5
  - our trade on v07 tick 714: [('MAL-01', 't06', '→', 't05')] at 5
  - our trade on v07 tick 760: [('MAL-08', 't14', '→', 't05')] at 15
- **Team 3** (v20): no deal yet, nothing on v10.
- **Alerts:** Team 15: 0 offers and 0 trades on v10, 355 min after the deal; Team 15: no open offer on v10 now (1 trades so far); Team 15: offer imbalance, ours on v15 5 vs theirs on v10 0; Team 10: no open offer on v10 now (2 trades so far)
- **Rebates owed (10 P a card sold on v10 since tick 1228, max 2 per team, cap 80; rivals t10 t06 t14 t03 t18 t13 t17 excluded, t01 t16 re-checked at payout):** none · total 0 P

## Partner audit · Sat 21:38 · tick 1281 · snapshot 1280: stall teams 7.5 · us 7.5 (+0.00)
- **Team 15** (v15, market 7.5 = +0.00): on v10 0 open offers, 1 trades (26 P) · ours on v15: 6 open offers, 0 trades (0 P)
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
- **Team 10** (v07, market 12.5 = +5.00): on v10 0 open offers, 2 trades (40 P) · ours on v07: 0 open offers, 4 trades (32 P)
  - v10 trade tick 311: [('MAL-07', 't10', '→', 't01')] at 14
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
  - our trade on v07 tick 351: [('SAL-01', 't05', '→', 't03')] at 7
  - our trade on v07 tick 404: [('MAL-03', 't04', '→', 't05')] at 5
  - our trade on v07 tick 714: [('MAL-01', 't06', '→', 't05')] at 5
  - our trade on v07 tick 760: [('MAL-08', 't14', '→', 't05')] at 15
- **Team 3** (v20): no deal yet, nothing on v10.
- **Alerts:** Team 15: 0 offers and 0 trades on v10, 325 min after the deal; Team 15: no open offer on v10 now (1 trades so far); Team 15: offer imbalance, ours on v15 6 vs theirs on v10 0; Team 10: no open offer on v10 now (2 trades so far)
- **Rebates owed (10 P a card sold on v10 since tick 1228, max 2 per team, cap 80; rivals t10 t06 t14 t03 t18 t13 t17 excluded, t01 t16 re-checked at payout):** none · total 0 P

## Partner audit · Sat 21:07 · tick 1221 · snapshot 1220: stall teams 7.5 · us 7.5 (+0.00)
- **Team 15** (v15, market 7.5 = +0.00): on v10 0 open offers, 1 trades (26 P) · ours on v15: 3 open offers, 0 trades (0 P)
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
- **Team 10** (v07, market 12.5 = +5.00): on v10 0 open offers, 2 trades (40 P) · ours on v07: 0 open offers, 4 trades (32 P)
  - v10 trade tick 311: [('MAL-07', 't10', '→', 't01')] at 14
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
  - our trade on v07 tick 351: [('SAL-01', 't05', '→', 't03')] at 7
  - our trade on v07 tick 404: [('MAL-03', 't04', '→', 't05')] at 5
  - our trade on v07 tick 714: [('MAL-01', 't06', '→', 't05')] at 5
  - our trade on v07 tick 760: [('MAL-08', 't14', '→', 't05')] at 15
- **Team 3** (v20): no deal yet, nothing on v10.
- **Alerts:** Team 15: 0 offers and 0 trades on v10, 295 min after the deal; Team 15: no open offer on v10 now (1 trades so far); Team 10: no open offer on v10 now (2 trades so far)
- **Rebates owed (5 P a card sold on v10, cap 30):** Team 8 0 P · Team 7 0 P · total 0 P

## Sat 21:15 · the Payday deck reconciled with our data (deck: "Market-making 30 = Market Test 7.5 + Real trades 22.5")
- **Market Test = 7.5 = what every stall team already shows [L].** When the top three are the stall, "half" and "full"
  coincide: the bench is maxed. A better broker has no upside. Board-venue question closed.
- **Real trades formula [L, strong]: points = 5.0 × min(1, VC / mean VC of the top three venues).** Fit at snapshot 560
  (Team 6's rare lands): predicted t14 3.11, t12 3.02, t17 1.97; observed 3.10, 3.02, 1.96. Full mark seen all day: 5.0,
  never 22.5 [?: desk question].
- **VC = the two teams' gains = buyer's value − seller's value** (price cancels). Our SAL-07 trade: 25 × (0.5 − 0.9) =
  −10.0 vs the measured mm swing −10.19 [V swing, L cause].
- **Swaps settle on stalls by acceptance [V]:** 13 card-for-card settlements today, two on Team 7's stall v11. Neither
  the auto engine nor the starter broker pairs two mirror swap offers (cash ask × cash bid only).
- **Payday [V]:** +400 P to every team at 20:37; Sunday +150 P at 09:00, new round. Re-score: keep the stall, no bond.
- **Sunday design:** v10 = swap desk. Pair-finder (wants × duplicates) from the radar; hand the 3-5 best two-way
  duplicate swaps their exact offers at 09:00; duplicates only; page-finishers only for teams well below us.

## Partner audit · Sat 20:08 · tick 1187 · snapshot 1180: stall teams 7.5 · us 7.5 (+0.00)
- **Team 15** (v15, market 7.5 = +0.00): on v10 0 open offers, 1 trades (26 P) · ours on v15: 4 open offers, 0 trades (0 P)
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
- **Team 10** (v07, market 12.5 = +5.00): on v10 0 open offers, 2 trades (40 P) · ours on v07: 0 open offers, 4 trades (32 P)
  - v10 trade tick 311: [('MAL-07', 't10', '→', 't01')] at 14
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
  - our trade on v07 tick 351: [('SAL-01', 't05', '→', 't03')] at 7
  - our trade on v07 tick 404: [('MAL-03', 't04', '→', 't05')] at 5
  - our trade on v07 tick 714: [('MAL-01', 't06', '→', 't05')] at 5
  - our trade on v07 tick 760: [('MAL-08', 't14', '→', 't05')] at 15
- **Team 3** (v20): no deal yet, nothing on v10.
- **Alerts:** Team 15: 0 offers and 0 trades on v10, 278 min after the deal; Team 15: no open offer on v10 now (1 trades so far); Team 10: no open offer on v10 now (2 trades so far)
- **Rebates owed (5 P a card sold on v10, cap 30):** Team 8 0 P · Team 7 0 P · total 0 P

## Sat 20:08 · bench-h11.0, on the stall v10
- **Ours [V]:** bench_efficiency 0.886 (0.899 · 0.933 · 0.878 · 0.891 before), bench_points 0.5, market 7.5 = stall teams.
- **Field at snapshot 1180 [V]:** t10 12.5 · t06 11.9 · t09 10.94 · t14 9.33 · t07 9.17 · t17 8.66 · t16 8.63 · t08 8.52
  · stall teams 7.5. No market above 12.5 has ever appeared: nobody beats the stall on the bench. Stay on the stall.
- **Bench split of rivals [L, from snapshots at bench ends; bench part = 15 × average bench points]:** t10 = stall level
  every session (its market never moves at a bench end); t06 ≈ 0.38 at 3.0, then ≈ 0.5 (its market creeps up at each
  bench end). All of t10's 5.0 above the stall is value created at the cap.
- v10: empty since tick 941, no fill since tick 398; mm −5.2. Rebates owed: 0 P.
- Next: bench 13.0 (~21:55), the hard bench at 14.65 (~23:34 if the clock runs on), then 15.0.

## Partner audit · Sat 19:38 · tick 1126 · snapshot 1120: stall teams 7.5 · us 7.5 (+0.00)
- **Team 15** (v15, market 7.5 = +0.00): on v10 0 open offers, 1 trades (26 P) · ours on v15: 4 open offers, 0 trades (0 P)
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
- **Team 10** (v07, market 12.5 = +5.00): on v10 0 open offers, 2 trades (40 P) · ours on v07: 0 open offers, 4 trades (32 P)
  - v10 trade tick 311: [('MAL-07', 't10', '→', 't01')] at 14
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
  - our trade on v07 tick 351: [('SAL-01', 't05', '→', 't03')] at 7
  - our trade on v07 tick 404: [('MAL-03', 't04', '→', 't05')] at 5
  - our trade on v07 tick 714: [('MAL-01', 't06', '→', 't05')] at 5
  - our trade on v07 tick 760: [('MAL-08', 't14', '→', 't05')] at 15
- **Team 3** (v20): no deal yet, nothing on v10.
- **Alerts:** Team 15: 0 offers and 0 trades on v10, 248 min after the deal; Team 15: no open offer on v10 now (1 trades so far); Team 10: no open offer on v10 now (2 trades so far)
- **Rebates owed (5 P a card sold on v10, cap 30):** Team 8 0 P · Team 7 0 P · total 0 P

## Partner audit · Sat 19:08 · tick 1066 · snapshot 1060: stall teams 7.5 · us 7.5 (+0.00)
- **Team 15** (v15, market 7.5 = +0.00): on v10 0 open offers, 1 trades (26 P) · ours on v15: 4 open offers, 0 trades (0 P)
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
- **Team 10** (v07, market 12.5 = +5.00): on v10 0 open offers, 2 trades (40 P) · ours on v07: 0 open offers, 4 trades (32 P)
  - v10 trade tick 311: [('MAL-07', 't10', '→', 't01')] at 14
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
  - our trade on v07 tick 351: [('SAL-01', 't05', '→', 't03')] at 7
  - our trade on v07 tick 404: [('MAL-03', 't04', '→', 't05')] at 5
  - our trade on v07 tick 714: [('MAL-01', 't06', '→', 't05')] at 5
  - our trade on v07 tick 760: [('MAL-08', 't14', '→', 't05')] at 15
- **Team 3** (v20): no deal yet, nothing on v10.
- **Alerts:** Team 15: 0 offers and 0 trades on v10, 218 min after the deal; Team 15: no open offer on v10 now (1 trades so far); Team 10: no open offer on v10 now (2 trades so far)

## Partner audit · Sat 18:38 · tick 1006 · snapshot 1000: stall teams 7.5 · us 7.5 (+0.00)
- **Team 15** (v15, market 7.5 = +0.00): on v10 0 open offers, 1 trades (26 P) · ours on v15: 2 open offers, 0 trades (0 P)
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
- **Team 10** (v07, market 12.5 = +5.00): on v10 0 open offers, 2 trades (40 P) · ours on v07: 0 open offers, 4 trades (32 P)
  - v10 trade tick 311: [('MAL-07', 't10', '→', 't01')] at 14
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
  - our trade on v07 tick 351: [('SAL-01', 't05', '→', 't03')] at 7
  - our trade on v07 tick 404: [('MAL-03', 't04', '→', 't05')] at 5
  - our trade on v07 tick 714: [('MAL-01', 't06', '→', 't05')] at 5
  - our trade on v07 tick 760: [('MAL-08', 't14', '→', 't05')] at 15
- **Team 3** (v20): no deal yet, nothing on v10.
- **Alerts:** Team 15: 0 offers and 0 trades on v10, 188 min after the deal; Team 15: no open offer on v10 now (1 trades so far); Team 10: no open offer on v10 now (2 trades so far)

## Sat 18:20 · who trades on team venues, and why (research for the Chief) [V from the feed]
- 35 trades on team venues all day, single cards. v07 (t10) 10: 4 ours, 5 with Team 6 as maker, 1 RET-06 uncommon
  t04 → t09 at 28. v01 (t06) 3: SAL-10 rare t12 → t08 at 76, LAT-06 uncommon at 20, LAT-05 at 5. v02 (t12) 10: Team 14's
  RET commons at 9 (5 fills in 7 ticks) and Team 7's duplicates. v14 (t14) 1: LAT-07 uncommon at 19.
- **Scores come from a handful of uncommon/rare trades, not volume.**
- **30 of 35 fills were open offers; addressed offers rarely fill.** Takers are board-scanning bots (t12, t08, t04,
  t09, t14, t06). Listings go where the maker's bot is configured: t08 ~470 listings over five venues, t15/t14/t13/t07
  on v02. v10: 111 listings (73 from t10, mostly addressed), 2 fills.
- **The cliff explained [L, Team 12's own announcement, tick 938]:** "two sales of page cards at 6-11 P destroyed value
  on this venue"; v02's fee goes to 10% + 5 P a card. A seller selling a card out of a page carries the large negative.
- **Actions sent:** (1) pitch v10 to v02's makers now (t14, t07, then t13, t15, t08); (2) open asks, not addressed,
  duplicates only; (3) announcements naming a concrete pair, uncommons and rares first.

## Partner audit · Sat 18:06 · tick 942 · snapshot 940: stall teams 7.5 · us 7.5 (+0.00)
- **Team 15** (v15, market 7.5 = +0.00): on v10 0 open offers, 1 trades (26 P) · ours on v15: 3 open offers, 0 trades (0 P)
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
- **Team 10** (v07, market 12.5 = +5.00): on v10 0 open offers, 2 trades (40 P) · ours on v07: 0 open offers, 4 trades (32 P)
  - v10 trade tick 311: [('MAL-07', 't10', '→', 't01')] at 14
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
  - our trade on v07 tick 351: [('SAL-01', 't05', '→', 't03')] at 7
  - our trade on v07 tick 404: [('MAL-03', 't04', '→', 't05')] at 5
  - our trade on v07 tick 714: [('MAL-01', 't06', '→', 't05')] at 5
  - our trade on v07 tick 760: [('MAL-08', 't14', '→', 't05')] at 15
- **Team 3** (v20): no deal yet, nothing on v10.
- **Alerts:** Team 15: 0 offers and 0 trades on v10, 156 min after the deal; Team 15: no open offer on v10 now (1 trades so far); Team 10: no open offer on v10 now (2 trades so far)

## Sat 18:06 · bench-h09.0 (ticks 922-935), on the stall v10
- **Ours [V]:** bench_efficiency 0.891 (3.0 0.899 · 5.0 0.933 · 7.0 0.878), bench_points 0.5, market 7.5 = stall teams.
- **Field at snapshot 930 [V]:** t10 12.5 · t06 12.05 · t09 9.67 · t14 9.53 · t07 9.35 · t17 8.78 · t08 8.62 · stall
  teams 7.5 · t13 6.08 · t03 4.75. Still no venue above the stall on the bench. Decision: stay on the stall.
- **Team 12 fell off the same cliff we did [V]:** market 12.43 (snapshot 900) → 7.5 (910), after two small trades on
  its v02 by Team 7: RET-04 → t01 at 6 (tick 898) and LAT-01 → t08 at 6 (tick 903). v02 had ~12 positive trades
  before. One cheap common trade wiping a venue's whole value-created score does not fit a plain sum of small values:
  some trades carry a large negative (seller breaking a page? buyer's duplicate?) [?]. Every trade on v10 is a risk
  until the desk explains mm_points.
- Team 15: approved offer 13773 (MAL-07 → t02 at 14) listed tick 893, unfilled, expires tick 941. Other two not listed.

## Partner audit · Sat 17:30 · tick 870 · snapshot 870: stall teams 7.5 · us 7.5 (+0.00)
- **Team 15** (v15, market 7.5 = +0.00): on v10 0 open offers, 1 trades (26 P) · ours on v15: 2 open offers, 0 trades (0 P)
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
- **Team 10** (v07, market 12.5 = +5.00): on v10 0 open offers, 2 trades (40 P) · ours on v07: 0 open offers, 4 trades (32 P)
  - v10 trade tick 311: [('MAL-07', 't10', '→', 't01')] at 14
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
  - our trade on v07 tick 351: [('SAL-01', 't05', '→', 't03')] at 7
  - our trade on v07 tick 404: [('MAL-03', 't04', '→', 't05')] at 5
  - our trade on v07 tick 714: [('MAL-01', 't06', '→', 't05')] at 5
  - our trade on v07 tick 760: [('MAL-08', 't14', '→', 't05')] at 15
- **Team 3** (v20): no deal yet, nothing on v10.
- **Alerts:** Team 15: 0 offers and 0 trades on v10, 120 min after the deal; Team 15: no open offer on v10 now (1 trades so far); Team 10: no open offer on v10 now (2 trades so far)

## Partner audit · Sat 16:59 · tick 810 · snapshot 810: stall teams 7.5 · us 7.5 (+0.00)
- **Team 15** (v15, market 7.5 = +0.00): on v10 0 open offers, 1 trades (26 P) · ours on v15: 5 open offers, 0 trades (0 P)
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
- **Team 10** (v07, market 12.5 = +5.00): on v10 0 open offers, 2 trades (40 P) · ours on v07: 0 open offers, 4 trades (32 P)
  - v10 trade tick 311: [('MAL-07', 't10', '→', 't01')] at 14
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
  - our trade on v07 tick 351: [('SAL-01', 't05', '→', 't03')] at 7
  - our trade on v07 tick 404: [('MAL-03', 't04', '→', 't05')] at 5
  - our trade on v07 tick 714: [('MAL-01', 't06', '→', 't05')] at 5
  - our trade on v07 tick 760: [('MAL-08', 't14', '→', 't05')] at 15
- **Team 3** (v20): no deal yet, nothing on v10.
- **Alerts:** Team 15: 0 offers and 0 trades on v10, 90 min after the deal; Team 15: no open offer on v10 now (1 trades so far); Team 15: offer imbalance, ours on v15 5 vs theirs on v10 0; Team 10: no open offer on v10 now (2 trades so far)

## Partner audit · Sat 16:29 · tick 750 · snapshot 750: stall teams 7.5 · us 7.5 (+0.00)
- **Team 15** (v15, market 7.5 = +0.00): on v10 0 open offers, 1 trades (26 P) · ours on v15: 3 open offers, 0 trades (0 P)
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
- **Team 10** (v07, market 12.5 = +5.00): on v10 2 open offers, 2 trades (40 P) · ours on v07: 3 open offers, 3 trades (17 P)
  - 10819 sells LAV-04 at 6 → Team 13 (est -2.8 NEGATIVE)
  - 11182 sells SAL-08 at 28 → Team 3 (est -13.8 NEGATIVE)
  - v10 trade tick 311: [('MAL-07', 't10', '→', 't01')] at 14
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
  - our trade on v07 tick 351: [('SAL-01', 't05', '→', 't03')] at 7
  - our trade on v07 tick 404: [('MAL-03', 't04', '→', 't05')] at 5
  - our trade on v07 tick 714: [('MAL-01', 't06', '→', 't05')] at 5
- **Team 3** (v20): no deal yet, nothing on v10.
- **Alerts:** Team 15: 0 offers and 0 trades on v10, 60 min after the deal; Team 15: no open offer on v10 now (1 trades so far); Team 10: offers on v10 with negative estimated value: [10819, 11182]

## Sat 16:05 · bench-h07.0 (ticks 680-697, after the lunch pause 13:25-15:29), on the stall v10
- **Ours [V]:** bench_efficiency 0.878 (3.0: 0.899, 5.0: 0.933), bench_points 0.5, market 7.5 = stall teams, unchanged.
- **Field at snapshot 700 [V]:** t12 12.5 · t10 12.01 · t06 11.89 · t14 9.51 · t07 9.33 · t09 8.84 · t17 8.77 · stall
  teams 7.5 · t08 7.47 · t13 6.08 (5.49) · t03 4.75 (3.61). Seven venues now carry value created; t07 and t09 are new.
  The stall teams' number did not move, so no venue pulled the top-three bench mean above the stall [L].
- Recording: leftovers only (22 states, 13 ids). No replay evidence. Decision: stay on the stall.

## Partner audit · Sat 15:59 · tick 690 · snapshot 690: stall teams 7.5 · us 7.5 (+0.00)
- **Team 15** (v15, market 7.5 = +0.00): on v10 0 open offers, 1 trades (26 P) · ours on v15: 3 open offers, 0 trades (0 P)
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
- **Team 10** (v07, market 12.01 = +4.51): on v10 1 open offers, 2 trades (40 P) · ours on v07: 0 open offers, 2 trades (12 P)
  - 10027 sells LAV-04 at 13 → Team 3 (est -1.8 NEGATIVE)
  - v10 trade tick 311: [('MAL-07', 't10', '→', 't01')] at 14
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
  - our trade on v07 tick 351: [('SAL-01', 't05', '→', 't03')] at 7
  - our trade on v07 tick 404: [('MAL-03', 't04', '→', 't05')] at 5
- **Team 3** (v20): no deal yet, nothing on v10.
- **Alerts:** Team 10: offers on v10 with negative estimated value: [10027]

## Partner audit · Sat 13:32 · tick 630 · snapshot 630: stall teams 7.5 · us 7.5 (+0.00)
- **Team 15** (v15, market 7.5 = +0.00): on v10 0 open offers, 1 trades (26 P) · ours on v15: 5 open offers, 0 trades (0 P)
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
- **Team 10** (v07, market 12.07 = +4.57): on v10 0 open offers, 2 trades (40 P) · ours on v07: 0 open offers, 2 trades (12 P)
  - v10 trade tick 311: [('MAL-07', 't10', '→', 't01')] at 14
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
  - our trade on v07 tick 351: [('SAL-01', 't05', '→', 't03')] at 7
  - our trade on v07 tick 404: [('MAL-03', 't04', '→', 't05')] at 5
- **Team 3** (v20): no deal yet, nothing on v10.
- **Alerts:** Team 15: offer imbalance, ours on v15 5 vs theirs on v10 0; Team 10: no open offer on v10 now (2 trades so far)

## Partner audit · Sat 13:11 · tick 603 · snapshot 600: stall teams 7.5 · us 7.5 (+0.00)
- **Team 15** (v15, market 7.5 = +0.00): on v10 0 open offers, 1 trades (26 P) · ours on v15: 0 open offers, 0 trades (0 P)
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
- **Team 10** (v07, market 12.07 = +4.57): on v10 0 open offers, 2 trades (40 P) · ours on v07: 5 open offers, 2 trades (12 P)
  - v10 trade tick 311: [('MAL-07', 't10', '→', 't01')] at 14
  - v10 trade tick 398: [('SAL-07', 't10', '→', 't15')] at 26
  - our trade on v07 tick 351: [('SAL-01', 't05', '→', 't03')] at 7
  - our trade on v07 tick 404: [('MAL-03', 't04', '→', 't05')] at 5
- **Team 3** (v20): no deal yet, nothing on v10.
- **Alerts:** Team 10: no open offer on v10 now (2 trades so far); Team 10: offer imbalance, ours on v07 5 vs theirs on v10 0

## Sat 13:00 · who earns value created, and the broker verdict
- **Trades on team venues since 11:30 [V]:** v14 (t14's stall) tick 418 LAT-07 t15 → t12 at 19 → t14 +4.36 · v17
  (t17's stall) tick 433 LAT-01 t15 → t12 at 7 → t17 +2.76 · v01 (t06) tick 556 SAL-10 rare t12 → t08 at 76 →
  t06 +2.33 → +4.14 and every other venue diluted ~25%. The part is relative to the best venues, top = 5.0 [L].
- 10 team-venue trades all day, single cards; Team 15 is in 6, Team 12 in 5.
- **Team 3's 7.5 → 3.61 is bench, not value created [L]:** it opened its own venue v20 and scored 0 on bench 5.0
  (Team 1 opened v19). So negative mm_points still look floored at zero.
- **Broker variants on the staggered sim (1,500 sessions) [L, model]:** overlap threshold 3/8/15: −0.7/−2.5/−6.5 pp;
  wait for age 2/3: −3.7/−9.9; wait until quotes stop moving: −37; wait one tick: +0.04 (noise). **Nothing beats the
  stall.** No board venue: the gate is not met and cannot be met with what we have.

## Sat 12:50 · reciprocal check (snapshots 520-560) [V]
- No new trade on v10 or v07 since tick 404: v10 2 trades (40 P, both t10 selling) · ours on v07 2 (12 P). Ratio 1:1.
- Market: us 7.5 (= stall teams, mm_points −5.2 unchanged) · t10 12.5 → 12.06 at snapshot 560 with no new trade on
  v07, so the value-created part moves with the field (relative scoring) [L].
- No alert conditions. Open: the desk's answer on mm_points vs value_created.

## Sat 12:00 · bench-h05.0 (ticks 441-458), on the stall v10 (auto, fee 0)
- **Ours [V]:** bench_efficiency 0.933 (3.0: 0.899), bench_points 0.5, market 7.5 = the stall teams' number, unchanged.
- **Field at snapshot 460 [V]:** t10 12.5 · t14 11.86 · t12 11.74 · t17 10.26 · t06 9.83 · stall teams 7.5 · t08 7.46 ·
  t13 5.49 (was 3.33) · t03 3.61 (was 7.5). Bench and value created are now mixed in `market`, so a board broker
  beating the stall can no longer be read off the leaderboard; none is visibly above it. t14 and t17 are STALLS with
  a gap: stalls with trades score value created too.
- **Recording [V]:** again leftovers only (21 states, 15 ids, no settlements); replay proxy is degenerate (0.000).
  Same trader shape as 3.0: staggered arrivals over ~10 ticks, lives of 1-6 ticks, steps of 1-8 with pauses.
- **Open contradiction [V both]:** our venue detail says `value_created` 9.0 (2 trades), our score says `mm_points`
  −5.2. The 11:31 reading "the second trade destroyed value" rests on mm_points only; the two fields measure different
  things and the formula is unpublished → desk question. t03 (stall) fell 7.5 → 3.61, so "negative floored at zero"
  is not safe either.
- Reciprocal count: v10 2 trades (40 P, both t10 as seller) · ours on v07 2 (SAL-01 sold to t03 at 7; MAL-03 bought
  from t04 at 5).
- **Decision:** stay on the stall. No replay evidence is possible from it; sim says v1 is worse than the stall.

## Sat 11:31 · v10 gap LOST: a value-destroying trade [V]
- Tick 398 (11:29): Team 10 sold SAL-07 to Team 15 on v10 at 26 P. **Our mm_points: −5.2 (/api/me); market 12.5 → 7.5**
  at snapshot 400 (= stall teams; a negative total looks floored at zero [L]). t10 12.5, t12 12.5, t06 9.99.
- **Value created can be negative**: buyer's private value minus seller's. t15 does not collect SAL [L, Dani's profiles].
- An auto stall crosses any crossing pair, so we cannot filter. Recovery needs > 5.2 of positive value on v10: sales
  from a non-collector to a collector of that set; a page-completing buy is the largest.
- Count: v10 2 trades (40 P, both with t10) · ours on v07 1 (7 P).

## Sat 11:10 · reciprocal check (snapshot 360) [V]
- **Market: us 12.5 (#1 in market) · t12 12.39 · t10 11.84 · t06 9.39 · stall teams 7.5 · t08 7.41 · t13 3.33.**
- v10: 1 trade (t10 → t01, MAL-07, 14 P, tick 311). v07: 1 trade, ours (t05 ↔ t03, SAL-01, 7 P, tick 351). **Ratio 1:1.**
- Our trade on v07 gave Team 10 +4.34 at the next snapshot (7.5 → 11.84); our gap stays +5.0.
- The stall teams' number has been flat at 7.5 since snapshot 330 (it grew 4.8 → 7.5 before): the bench part looks
  fully grown; our +5.0 has not moved since the first trade [L: capped, or we set the top].
- Gaps differ by venue (+5.0 us, +4.89 t12, +4.34 t10, +1.89 t06), so value created is graded, not all-or-nothing [L].

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
