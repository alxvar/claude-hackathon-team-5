# Standings (Analyst; refreshed hourly)

_Final Saturday snapshot 1440 (Sat 23:00, doors closed; clock paused at game 13.367 in round 2). Source: `/api/leaderboard`
(keyless) + the board fit in `intel/score-model.md` §1._

**Final formula [V, organisers' desk]:** game = (0.5·Fri + Sat + Sun)/2.5 on 60 points (Negotiating 30 + Market 30),
plus judges on 40. Board now = (0.5·Fri + Sat)/1.5 for each part [V fit], so a team's round score = Negotiating + Market
for that day: **Fri** = board at tick 160 (frozen; market was 0 for everyone), **Sat** = 1.5 × board − 0.5 × Fri.

**Headline:** board #3 at 30.49. On 0.5·Fri + Sat: t10 56.37 · t18 46.89 · **us 45.73** · t12 45.63 · t03 44.51 · t06 43.14.
t10 is 10.6 ahead (its v07 value created at the cap is 7.5 of it); **#2 is a three-way race with t18 (+1.16) and t12 (−0.10)**.
Our mm_points flipped −5.2 → +2.2 at the close (score-model §3h): ≥ +1.05 (up to +3.3) Saturday points if it lands [L], and
Saturday's round may continue Sunday morning (score-model §4.7).

## 1. Round scores (snapshot 1440, sorted by 0.5·Fri + Sat)

| Team | Board rank | Fri (frozen) | Sat Negotiating | Sat Market | **Sat total** | 0.5·Fri + Sat |
|---|---|---|---|---|---|---|
| t10 | #1 (37.58) | 20.75 | 27.24 | 18.75 | 45.99 | 56.37 |
| t18 | #2 (31.26) | 19.16 | 26.06 | 11.25 | 37.31 | 46.89 |
| **t05** | #3 (30.49) | 19.99 | 24.49 | 11.25 | 35.74 | 45.73 |
| t12 | #4 (30.42) | 27.82 | 20.85 | 10.88 | 31.72 | 45.63 |
| t03 | #5 (29.67) | 14.60 | 28.08 | 9.12 | 37.20 | 44.51 |
| t06 | #6 (28.76) | 12.67 | 19.01 | 17.80 | 36.82 | 43.14 |
| t14 | #7 (27.67) | 18.06 | 18.52 | 13.95 | 32.48 | 41.51 |
| t17 | #8 (25.82) | 22.03 | 14.77 | 12.96 | 27.73 | 38.73 |
| t01 | #9 (25.65) | 8.39 | 23.03 | 11.25 | 34.28 | 38.47 |
| t13 | #10 (25.02) | 29.94 | 12.40 | 10.15 | 22.56 | 37.53 |

## 2. Gaps: what we must win Sunday by

| Rival | Our Sat lead | Sunday margin we need (> 0 = beat them by this) |
|---|---|---|
| t10 | −10.25 | **+10.63** |
| t18 | −1.57 | **+1.16** |
| t12 | +4.02 | **−0.10** |
| t03 | −1.46 | **−1.23** |
| t06 | −1.08 | **−2.59** |
| t14 | +3.27 | **−4.23** |
| t17 | +8.01 | **−7.00** |
| t01 | +1.46 | **−7.26** |

Rule: we finish ahead of a rival when 0.5·ΔFri + ΔSat + ΔSun > 0 (Δ = us − them). Every Saturday point added in a Sunday-morning
tail counts 1:1, and so does every Sunday point. Friday counts half. P(#1) ≤ 4% in every variant. P(top 2) in case J (round 3 at ≈ 09:00, the flip lands): **≈ 19% without
ladder fodder, ≈ 24-27% with the approved fodder** (ladder ≈ 0.34-0.38); 13-15% if the flip doesn't land (score-model §4.12).

## 3. Rivals' Sunday upside [L]

| Rival | Saturday round | Where its points came from | Sunday risk to us |
|---|---|---|---|
| t10 | 45.99 (≈ ceiling 48.75) | duels strong, trades + ladder ≈ caps, **v07 VC at the cap (+7.5)** | repeats unless v07's flow dries up |
| t18 | 37.31 | negotiating 26.06 (duels + ladder), stall only | no venue VC; beatable via v10 VC |
| t12 | 31.72 | Friday 27.82 (best), v02 board venue below the stall | weak Saturday; its v02 VC can come back |
| t03 | 37.20 | negotiating 28.08 (best duels/ladder), v20 below the stall | strong negotiator; market weak |
| t06 | 36.82 | market 17.80 (v01 VC ≈ cap) | Friday 12.67 holds it back |

## 4. Our Sunday levers (detail: score-model §4.3, first hour §4.7)

| Lever | Sunday round pts | Cost |
|---|---|---|
| v10 value created (pairs: duplicates → first copies) | 0 → 7.5 (field-normalised, §3h) | 0 P |
| Saturday tail, if the clock resumes at 13.367 (v10 pairs only; trade part has ≈ 6 np headroom) | up to ≈ +4 Saturday pts | 0 P |
| Duels III + Grand Final | ≈ 7 → 8-9 | 0 P |
| CHA page (team closer +50) + CHA dealer buys ≤ list (ladder: Abuela + Pícaros) | ≈ +7 (incl. ladder ≈ 2.8) | ≈ 330 P |
| Fresh ladder sells (MAL-08 → Pilar ≥ 20, spare non-SAL rare → Pilar ≈ 55, spare common → Pícaros 5; RET-11 only ≥ 198) | +1.5-3 | cash + |
| MAL close | +1-3 | ≈ 160 P |
