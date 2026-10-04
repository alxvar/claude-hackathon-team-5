# Scout (claude-sonnet-5-5, Sun 12:30)

## Top 3 actions now
1. **MAL closer: MAL-09 from t08 on El Rastro (bid 25451 at 48, exp tick 2310); MAL-07 last from t15.** Executor: mal_close.py / Lucas.
   - Evidence: the Pícaros walked twice (first 73, last 56-58 against our 44-48). MAL page is the live +50 lever, and Lucas's 12:22 directive is "MAL closer GO". The 12:22 correction shows the +50 is per trade, not a round cap.
   - Rule: MAL-07 last only at ≤ value-when-last − 50, addressed to t15 (non-rival), seller's fee added. Our bid 25512 for MAL-07 at 15 is public; keep it ≥ 0.
   - Effect: up to +50 neg_points. Confidence: med (MAL-09's holder is unconfirmed, and t18 bids 25 for MAL-09/10 against our 48).
2. **Sell spare RET-03-type copies only to non-rivals; buy LAT-09/10 at ≤ 31 (bids 25417/25419).**
   - Evidence: t01 paid t06 44 P for LAT-09 at tick 2129, above our 31 bid. LAT-09/10 are rares worth ~35 to us (0.5 × 70). The bids are likely to stay unfilled at 31.
   - Action: keep the bids and do not raise above value. Raise only if the Chief wants ladder or LAT fodder.
   - Effect: ≥ 0 neg_points, low. Confidence: low.
3. **CHA-11 (epic we lack, value 288): bid 25638 to t08 at 220 (exp 2275). Re-post to t16 on expiry.** Executor: cha11.py.
   - Evidence: t10 bids only 100 for CHA-11 (offer 25486). Team trades on El Rastro paid 220 for SAL-11 (t04→t02, tick 1858) and t03 bids 184. Dealers paid ~140 for an epic.
   - Rule: 220 = min(220, value − 50) is a +50 trade. Do not outbid t10 or t18 on v10 or a member venue (feeds leaders).
   - Effect: +50 if it fills. Confidence: med-low.

## What the climbing teams are doing
- **t12 (#1, 34.2)** has the most deals (82) and collects RET/MAL/LAT. It bought RET-11 for 216 at tick 1245 and sold SAL-12 (legendary) to t16 for 380 at tick 1886. It is closing pages through large trades.
- **t04 (+4.5 in 60 min, 91 deals)** is the highest-volume buyer: RET×6, MAL×6, LAV×4, LAT×3. It sold SAL-11 (epic) to t02 for 220 at tick 1858.
- **t03 (+1.9 in 60 min)** buys SAL×3 and LAT×2. It bids 184 for SAL-11 (offer 25611). It is #5, 1.3 behind us.
- **t16 and t13 are trading CHA.** t15→t16 CHA-10 at 65 (tick 2022) and CHA-09 at 65 (tick 2065); t13→t16 CHA-01 at 40 (tick 2189). t16 is not a top-4 team.

## Threats
- **t12 leads us by 0.6 (34.2 vs 33.6)** and t10 trails by 0.2. Never sell them LAT-08, MAL-03 or MAL-08, and no page closers. Our trend is −0.3 over 15 min.
- **t18 (#4, 1.0 behind)** bids 35 for LAV-09/10 and 25 for MAL-09/10. It competes with us for MAL-09 and sits in the top 4, so give it no MAL closer.
- **t03 (#5) is 1.3 behind us** and is gaining (+0.4 in 15 min, +1.9 in 60 min). It bids for SAL/LAT epics and rares, so it is the one to defend against.
