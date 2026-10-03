# Scout (claude-sonnet-5-5, Sat 22:22)

## Top 3 actions now

1. **Keep SAL-11 bid 18977 (115 → t04, v15) alive; repost if it lapses.**
   - It expires at tick 1371, the metrics are at tick 1368, and the directive allows up to 125 (floor 260).
   - Evidence: our first-copy value is 162, t04 dumps SAL, and t10 sold SAL-11 to t17 at 207 (tick 1296).
   - Executor: operator, using the repost loop. If t04 counters at ≤125, the watcher auto-accepts.
   - Effect: +37 or more of ΔV before the pack drag, which is below the 50 cap, and about +2.3 board per the directive. Confidence: med (no t04 reply so far).

2. **Sell our spare commons and uncommons to bidders on v10 or El Rastro as maker.**
   - Our open asks: LAV-03 at 6 → t04, MAL-03 at 9 → t09, LAV-04 at 6 → t01, MAL-08 at 20 → t01.
   - Evidence: t09 bids 56 for MAL-09 and MAL-10, so t09 is collecting MAL. t04 bids 5 for LAV-02, and we hold three copies worth 1.3 each. Re-offer LAV-02 at 5 → t04 as maker.
   - Do not sell MAL-06 (17.5): we hold only one copy.
   - Effect: small, about +2 to +5 neg_points each, since they sell above our spare value (a 2nd copy is 25%, a 3rd 10%). Confidence: med.
   - The MAL-03 ask at 9 → t09 is worth +2 against our value of 7, and t09 is not a top-4 team.

3. **Hold RET-11 (value 198) and don't sell below 198.**
   - Evidence: t06 sold RET-11 to t12 at 216 (tick 1245), and t10 bids 210 for LAV-11. Dealers compete for epics.
   - Directive: RET-11 goes to Pilar only at ≥198, otherwise we keep it.
   - Selling to t12 would feed a top-4 team, so no.
   - Effect: 0 on neg_points unless the sale clears 198 (value gain clipped). Confidence: med.
   - Alternative: sell to t17, who bids 150 for MAL-11. That only helps if t17 also bids on RET-11, and the data doesn't show it. Not in the data.

## What the climbing teams are doing
- **Team 18 (#5, +1.9 in 15 min)** buys rares from other teams: LAT-10 from t13 at 72 (tick 1332), LAT/RET collector. Its scale of gain is small (30.1), and it sits 0.8 below us.
- **Team 10 (#1, 38.1)** collects epics and sets, buying MAL-11 at 195 from t08 and selling SAL-11 at 207 to t17. Its v10 flow gives it market-making points, so we are steering other teams away from v10.
- **Team 1 (+2.2 in 60 min)** is the biggest 60-minute climber below us, and t17 (+1.7) is next. Both are at 26-27 and buy LAV/SAL/MAL.
- **Team 12 (#4)** bought RET-11 at 216, LAT-10 at 86 and SAL-09 (from t12 to t09 at 70, tick 1231). It is a rival and we skip it on ads.

## Threats
- **t10 leads by 7.2 points and is still gaining** (+3.5/60 min). Any trade that routes onto v10 or hands it a card feeds it. Never sell to t10.
- **Team 18 is 0.8 points behind us** and gaining fastest (+1.9). RET-10 bids at 42 from t13 and rare asks of 84 show RET rares are cheap, so t18 could pass us.
- **Our own score is flat (-1.0/60 min)** because the ladder is spent and flags are capped. Only team trades and the SAL-11 buy add neg_points now, and the SAL-11 bid expires within 3 ticks.
