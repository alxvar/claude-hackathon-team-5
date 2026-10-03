# Duel review

_Written by `tools/duel_monitor.py` after each wave of our duels, newest first. Advisory for Aleks (the duelist is his). Result = our surplus × (1 − decay)^rounds, rounds = min(our priced offers, theirs); "spoke" = the rival sent at least one price._

## Sat 12:15 · Duels I · tick 491 · wave of 3 (duels 2315, 2366, 2506)

**This wave:** 3 deals / 3 finished (100%)
- Rival engaged: spoke in 3 → 3 deals (100%); spoke or accepted 3 → 3 (100%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Rounds and decay: 4.0 rounds per deal; result 18.9 of 24.0 P surplus → 5.1 P (21%) lost to decay.
- Latency: answered rival offers in 1.4 ticks on average (max 5; 11 of 22 the same tick); decision 6.4 s mean, 8.9 s max.
- Concessions: we moved 115 P in total, rivals 38 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 2 duel(s), 2 deal(s), mean result 7.0 P, rival moved 0.0 P per duel · conceder: 1 duel(s), 1 deal(s), mean result 4.8 P, rival moved 38.0 P per duel.
- Best duel: 2315 vs Rival Oro (seller): 7.5 P in 1 round(s). Worst: 2506 vs Rival Noche (buyer): deal.

**Session so far:** 7 deals / 7 finished (100%)
- Rival engaged: spoke in 7 → 7 deals (100%); spoke or accepted 7 → 7 (100%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 1 (≈4.7 P: 2296).
- Rounds and decay: 4.3 rounds per deal; result 55.6 of 74.0 P surplus → 18.4 P (25%) lost to decay.
- Latency: answered rival offers in 0.8 ticks on average (max 5; 29 of 43 the same tick); decision 6.4 s mean, 14.5 s max.
- Concessions: we moved 219 P in total, rivals 154 P.
- Rival behaviours (best → worst by our mean result): conceder: 4 duel(s), 4 deal(s), mean result 8.7 P, rival moved 38.5 P per duel · holder (never moved): 3 duel(s), 3 deal(s), mean result 6.9 P, rival moved 0.0 P per duel.
- Best duel: 2540 vs Rival Luna (seller): 12.3 P in 7 round(s). Worst: 2506 vs Rival Noche (buyer): deal.

**For Aleks:**
1. Close in fewer exchanges: 18.4 P (25%) of deal value went to decay over 4.3 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).
2. Decay-aware accept: 1 deal(s) closed below an earlier in-limit rival offer (≈4.7 P).

## Sat 12:07 · Duels I · tick 475 · wave of 4 (duels 2296, 2297, 2314, 2540)

**This wave:** 4 deals / 4 finished (100%)
- Rival engaged: spoke in 4 → 4 deals (100%); spoke or accepted 4 → 4 (100%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 1 (≈4.7 P: 2296).
- Rounds and decay: 4.5 rounds per deal; result 36.7 of 50.0 P surplus → 13.3 P (27%) lost to decay.
- Latency: answered rival offers in 0.1 ticks on average (max 1; 18 of 21 the same tick); decision 6.6 s mean, 14.5 s max.
- Concessions: we moved 104 P in total, rivals 116 P.
- Rival behaviours (best → worst by our mean result): conceder: 3 duel(s), 3 deal(s), mean result 10.0 P, rival moved 38.7 P per duel · holder (never moved): 1 duel(s), 1 deal(s), mean result 6.6 P, rival moved 0.0 P per duel.
- Best duel: 2540 vs Rival Luna (seller): 12.3 P in 7 round(s). Worst: 2314 vs Rival Oro (buyer): deal, both still 5 ticks.

**Session so far:** 4 deals / 4 finished (100%)
- Rival engaged: spoke in 4 → 4 deals (100%); spoke or accepted 4 → 4 (100%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 1 (≈4.7 P: 2296).
- Rounds and decay: 4.5 rounds per deal; result 36.7 of 50.0 P surplus → 13.3 P (27%) lost to decay.
- Latency: answered rival offers in 0.1 ticks on average (max 1; 18 of 21 the same tick); decision 6.6 s mean, 14.5 s max.
- Concessions: we moved 104 P in total, rivals 116 P.
- Rival behaviours (best → worst by our mean result): conceder: 3 duel(s), 3 deal(s), mean result 10.0 P, rival moved 38.7 P per duel · holder (never moved): 1 duel(s), 1 deal(s), mean result 6.6 P, rival moved 0.0 P per duel.
- Best duel: 2540 vs Rival Luna (seller): 12.3 P in 7 round(s). Worst: 2314 vs Rival Oro (buyer): deal, both still 5 ticks.

**For Aleks:**
1. Close in fewer exchanges: 13.3 P (27%) of deal value went to decay over 4.5 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).
2. Decay-aware accept: 1 deal(s) closed below an earlier in-limit rival offer (≈4.7 P).

## Sat 09:37 · session 1 · tick 176 · wave of 1 (duels 278)

**This wave:** 1 deals / 1 finished (100%)
- Rival engaged: spoke in 1 → 1 deals (100%); spoke or accepted 1 → 1 (100%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 1 (≈2.3 P: 278).
- Rounds and decay: 10.0 rounds per deal; result 2.7 of 5.0 P surplus → 2.3 P (46%) lost to decay.
- Latency: answered rival offers in 0.0 ticks on average (max 0; 10 of 10 the same tick); decision 6.0 s mean, 7.8 s max.
- Concessions: we moved 24 P in total, rivals 0 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 1 duel(s), 1 deal(s), mean result 2.7 P, rival moved 0.0 P per duel.
- Best duel: 278 vs Rival Oro (buyer): 2.7 P in 10 round(s). Worst: 278 vs Rival Oro (buyer): deal.

**Session so far:** 19 deals / 34 finished (56%)
- Rival engaged: spoke in 20 → 17 deals (85%); spoke or accepted 22 → 19 (86%); silent 14 (2 took our opener, 12 no deal).
- In-limit offers not accepted: 1 — 181 (buyer, limit 85, vs Rival Verde): ≈10.6 P left on the table.
- Deals below an earlier in-limit rival offer: 3 (≈6.7 P: 227, 228, 278).
- Rounds and decay: 3.5 rounds per deal; result 415.3 of 491.0 P surplus → 75.7 P (15%) lost to decay.
- Latency: answered rival offers in 0.1 ticks on average (max 1; 61 of 71 the same tick); decision 5.3 s mean, 14.2 s max.
- Concessions: we moved 368 P in total, rivals 228 P.
- Rival behaviours (best → worst by our mean result): accept-only (took our opener): 2 duel(s), 2 deal(s), mean result 26.5 P · conceder: 12 duel(s), 11 deal(s), mean result 20.6 P, rival moved 19.0 P per duel · holder (never moved): 8 duel(s), 6 deal(s), mean result 14.3 P, rival moved 0.0 P per duel · silent: 12 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 199 vs Rival Oro (buyer): 46.8 P in 2 round(s). Worst: 181 vs Rival Verde (buyer): no_deal, 10.6 P in-limit left.

**For Aleks:**
1. Accept earlier: 1 deal(s) lost with the rival's offer inside our limit (181; ≈10.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
2. Break holds: 2 no-deal duel(s) sat still up to 9 ticks with time left (103, 104). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
3. Close in fewer exchanges: 75.7 P (15%) of deal value went to decay over 3.5 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).

## Sat 09:36 · session 1 · tick 175 · wave of 3 (duels 271, 272, 277)

**This wave:** 3 deals / 3 finished (100%)
- Rival engaged: spoke in 3 → 3 deals (100%); spoke or accepted 3 → 3 (100%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Rounds and decay: 5.3 rounds per deal; result 48.1 of 61.0 P surplus → 12.9 P (21%) lost to decay.
- Latency: answered rival offers in 0.1 ticks on average (max 1; 15 of 16 the same tick); decision 5.4 s mean, 8.0 s max.
- Concessions: we moved 88 P in total, rivals 21 P.
- Rival behaviours (best → worst by our mean result): conceder: 1 duel(s), 1 deal(s), mean result 18.0 P, rival moved 21.0 P per duel · holder (never moved): 2 duel(s), 2 deal(s), mean result 15.1 P, rival moved 0.0 P per duel.
- Best duel: 271 vs Rival Noche (seller): 23.5 P in 1 round(s). Worst: 277 vs Rival Plata (seller): deal, both still 4 ticks.

**Session so far:** 18 deals / 33 finished (55%)
- Rival engaged: spoke in 19 → 16 deals (84%); spoke or accepted 21 → 18 (86%); silent 14 (2 took our opener, 12 no deal).
- In-limit offers not accepted: 1 — 181 (buyer, limit 85, vs Rival Verde): ≈10.6 P left on the table.
- Deals below an earlier in-limit rival offer: 2 (≈4.4 P: 227, 228).
- Rounds and decay: 3.2 rounds per deal; result 412.6 of 486.0 P surplus → 73.4 P (15%) lost to decay.
- Latency: answered rival offers in 0.2 ticks on average (max 1; 51 of 61 the same tick); decision 5.3 s mean, 14.2 s max.
- Concessions: we moved 344 P in total, rivals 228 P.
- Rival behaviours (best → worst by our mean result): accept-only (took our opener): 2 duel(s), 2 deal(s), mean result 26.5 P · conceder: 12 duel(s), 11 deal(s), mean result 20.6 P, rival moved 19.0 P per duel · holder (never moved): 7 duel(s), 5 deal(s), mean result 16.0 P, rival moved 0.0 P per duel · silent: 12 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 199 vs Rival Oro (buyer): 46.8 P in 2 round(s). Worst: 181 vs Rival Verde (buyer): no_deal, 10.6 P in-limit left.

**For Aleks:**
1. Accept earlier: 1 deal(s) lost with the rival's offer inside our limit (181; ≈10.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
2. Break holds: 2 no-deal duel(s) sat still up to 9 ticks with time left (103, 104). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
3. Close in fewer exchanges: 73.4 P (15%) of deal value went to decay over 3.2 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).
