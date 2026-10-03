# Duel review

_Written by `tools/duel_monitor.py` after each wave of our duels, newest first. Advisory for Aleks (the duelist is his). Result = our surplus × (1 − decay)^rounds, rounds = min(our priced offers, theirs); "spoke" = the rival sent at least one price._

## Sat 13:04 · Duels I · tick 589 · wave of 4 (duels 2414, 2461, 2507, 2584)

**This wave:** 3 deals / 4 finished (75%)
- Rival engaged: spoke in 3 → 3 deals (100%); spoke or accepted 3 → 3 (100%); silent 1 (0 took our opener, 1 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 1 (≈1.0 P: 2461).
- Rounds and decay: 6.7 rounds per deal; result 63.2 of 79.0 P surplus → 15.8 P (20%) lost to decay.
- Latency: answered rival offers in 0.1 ticks on average (max 1; 17 of 19 the same tick); decision 4.8 s mean, 9.2 s max.
- Concessions: we moved 138 P in total, rivals 82 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 1 duel(s), 1 deal(s), mean result 49.8 P, rival moved 0.0 P per duel · conceder: 2 duel(s), 2 deal(s), mean result 6.7 P, rival moved 41.0 P per duel · silent: 1 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 2584 vs Rival Verde (seller): 49.8 P in 1 round(s). Worst: 2414 vs Rival Verde (seller): no_deal.

**Session so far:** 27 deals / 30 finished (90%)
- Rival engaged: spoke in 26 → 25 deals (96%); spoke or accepted 28 → 27 (96%); silent 4 (2 took our opener, 2 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 3 (≈6.3 P: 2296, 2461, 2522).
- Rounds and decay: 4.7 rounds per deal; result 367.6 of 472.0 P surplus → 104.4 P (22%) lost to decay.
- Latency: answered rival offers in 0.6 ticks on average (max 5; 116 of 161 the same tick); decision 5.3 s mean, 25.0 s max; 1 rival offer(s) never answered.
- Concessions: we moved 892 P in total, rivals 645 P.
- Rival behaviours (best → worst by our mean result): accept-only (took our opener): 2 duel(s), 2 deal(s), mean result 22.5 P · holder (never moved): 7 duel(s), 6 deal(s), mean result 12.5 P, rival moved 0.0 P per duel · conceder: 19 duel(s), 19 deal(s), mean result 12.4 P, rival moved 33.9 P per duel · silent: 2 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 2584 vs Rival Verde (seller): 49.8 P in 1 round(s). Worst: 2367 vs Rival Oro (buyer): no_deal, both still 5 ticks.

**For Aleks:**
1. Break holds: 1 no-deal duel(s) sat still up to 5 ticks with time left (2367). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
2. Close in fewer exchanges: 104.4 P (22%) of deal value went to decay over 4.7 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).
3. Silent rivals: 2 no-deal(s) with a silent rival while 2 silent rival(s) took our opener: concede on a code schedule toward a floor (keep ≥ 30% of anchor-to-limit).

## Sat 12:54 · Duels I · tick 568 · wave of 4 (duels 2460, 2473, 2495, 2535)

**This wave:** 4 deals / 4 finished (100%)
- Rival engaged: spoke in 3 → 3 deals (100%); spoke or accepted 4 → 4 (100%); silent 1 (1 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Rounds and decay: 3.8 rounds per deal; result 70.2 of 92.0 P surplus → 21.8 P (24%) lost to decay.
- Latency: answered rival offers in 0.8 ticks on average (max 4; 12 of 20 the same tick); decision 4.2 s mean, 8.2 s max.
- Concessions: we moved 160 P in total, rivals 100 P.
- Rival behaviours (best → worst by our mean result): conceder: 2 duel(s), 2 deal(s), mean result 23.8 P, rival moved 50.0 P per duel · accept-only (took our opener): 1 duel(s), 1 deal(s), mean result 17.0 P · holder (never moved): 1 duel(s), 1 deal(s), mean result 5.6 P, rival moved 0.0 P per duel.
- Best duel: 2535 vs Rival Noche (buyer): 33.6 P in 4 round(s). Worst: 2473 vs Rival Rojo (buyer): deal.

**Session so far:** 24 deals / 26 finished (92%)
- Rival engaged: spoke in 23 → 22 deals (96%); spoke or accepted 25 → 24 (96%); silent 3 (2 took our opener, 1 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 2 (≈5.4 P: 2296, 2522).
- Rounds and decay: 4.5 rounds per deal; result 304.4 of 393.0 P surplus → 88.6 P (23%) lost to decay.
- Latency: answered rival offers in 0.7 ticks on average (max 5; 99 of 142 the same tick); decision 5.4 s mean, 25.0 s max; 1 rival offer(s) never answered.
- Concessions: we moved 754 P in total, rivals 563 P.
- Rival behaviours (best → worst by our mean result): accept-only (took our opener): 2 duel(s), 2 deal(s), mean result 22.5 P · conceder: 17 duel(s), 17 deal(s), mean result 13.0 P, rival moved 33.1 P per duel · holder (never moved): 6 duel(s), 5 deal(s), mean result 6.3 P, rival moved 0.0 P per duel · silent: 1 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 2535 vs Rival Noche (buyer): 33.6 P in 4 round(s). Worst: 2367 vs Rival Oro (buyer): no_deal, both still 5 ticks.

**For Aleks:**
1. Break holds: 1 no-deal duel(s) sat still up to 5 ticks with time left (2367). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
2. Close in fewer exchanges: 88.6 P (23%) of deal value went to decay over 4.5 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).
3. Silent rivals: 1 no-deal(s) with a silent rival while 2 silent rival(s) took our opener: concede on a code schedule toward a floor (keep ≥ 30% of anchor-to-limit).

## Sat 12:46 · Duels I · tick 552 · wave of 3 (duels 2446, 2447, 2472)

**This wave:** 3 deals / 3 finished (100%)
- Rival engaged: spoke in 2 → 2 deals (100%); spoke or accepted 3 → 3 (100%); silent 1 (1 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Rounds and decay: 1.0 rounds per deal; result 67.6 of 72.0 P surplus → 4.4 P (6%) lost to decay.
- Latency: answered rival offers in 0.5 ticks on average (max 1; 1 of 2 the same tick); decision 3.9 s mean, 8.5 s max.
- Concessions: we moved 50 P in total, rivals 20 P.
- Rival behaviours (best → worst by our mean result): conceder: 1 duel(s), 1 deal(s), mean result 28.3 P, rival moved 20.0 P per duel · accept-only (took our opener): 1 duel(s), 1 deal(s), mean result 28.0 P · holder (never moved): 1 duel(s), 1 deal(s), mean result 11.3 P, rival moved 0.0 P per duel.
- Best duel: 2447 vs Rival Verde (seller): 28.3 P in 2 round(s). Worst: 2472 vs Rival Sol (seller): deal.

**Session so far:** 20 deals / 22 finished (91%)
- Rival engaged: spoke in 20 → 19 deals (95%); spoke or accepted 21 → 20 (95%); silent 2 (1 took our opener, 1 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 2 (≈5.4 P: 2296, 2522).
- Rounds and decay: 4.6 rounds per deal; result 234.2 of 301.0 P surplus → 66.8 P (22%) lost to decay.
- Latency: answered rival offers in 0.7 ticks on average (max 5; 87 of 122 the same tick); decision 5.6 s mean, 25.0 s max; 1 rival offer(s) never answered.
- Concessions: we moved 594 P in total, rivals 463 P.
- Rival behaviours (best → worst by our mean result): accept-only (took our opener): 1 duel(s), 1 deal(s), mean result 28.0 P · conceder: 15 duel(s), 15 deal(s), mean result 11.6 P, rival moved 30.9 P per duel · holder (never moved): 5 duel(s), 4 deal(s), mean result 6.4 P, rival moved 0.0 P per duel · silent: 1 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 2534 vs Rival Sol (seller): 29.7 P in 4 round(s). Worst: 2367 vs Rival Oro (buyer): no_deal, both still 5 ticks.

**For Aleks:**
1. Break holds: 1 no-deal duel(s) sat still up to 5 ticks with time left (2367). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
2. Close in fewer exchanges: 66.8 P (22%) of deal value went to decay over 4.6 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).
3. Silent rivals: 1 no-deal(s) with a silent rival while 1 silent rival(s) took our opener: concede on a code schedule toward a floor (keep ≥ 30% of anchor-to-limit).

## Sat 12:44 · Duels I · tick 548 · wave of 3 (duels 2494, 2523, 2534)

**This wave:** 2 deals / 3 finished (67%)
- Rival engaged: spoke in 2 → 2 deals (100%); spoke or accepted 2 → 2 (100%); silent 1 (0 took our opener, 1 no deal).
- In-limit offers not accepted: 0.
- Rounds and decay: 3.0 rounds per deal; result 44.7 of 55.0 P surplus → 10.3 P (19%) lost to decay.
- Latency: answered rival offers in 0.1 ticks on average (max 1; 6 of 7 the same tick); decision 3.1 s mean, 7.5 s max.
- Concessions: we moved 89 P in total, rivals 14 P.
- Rival behaviours (best → worst by our mean result): conceder: 2 duel(s), 2 deal(s), mean result 22.4 P, rival moved 7.0 P per duel · silent: 1 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 2534 vs Rival Sol (seller): 29.7 P in 4 round(s). Worst: 2523 vs Rival Noche (buyer): no_deal.

**Session so far:** 17 deals / 19 finished (89%)
- Rival engaged: spoke in 18 → 17 deals (94%); spoke or accepted 18 → 17 (94%); silent 1 (0 took our opener, 1 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 2 (≈5.4 P: 2296, 2522).
- Rounds and decay: 5.2 rounds per deal; result 166.6 of 229.0 P surplus → 62.4 P (27%) lost to decay.
- Latency: answered rival offers in 0.7 ticks on average (max 5; 86 of 120 the same tick); decision 5.8 s mean, 25.0 s max; 1 rival offer(s) never answered.
- Concessions: we moved 544 P in total, rivals 443 P.
- Rival behaviours (best → worst by our mean result): conceder: 14 duel(s), 14 deal(s), mean result 10.4 P, rival moved 31.6 P per duel · holder (never moved): 4 duel(s), 3 deal(s), mean result 5.2 P, rival moved 0.0 P per duel · silent: 1 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 2534 vs Rival Sol (seller): 29.7 P in 4 round(s). Worst: 2367 vs Rival Oro (buyer): no_deal, both still 5 ticks.

**For Aleks:**
1. Break holds: 1 no-deal duel(s) sat still up to 5 ticks with time left (2367). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
2. Close in fewer exchanges: 62.4 P (27%) of deal value went to decay over 5.2 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).
3. Decay-aware accept: 2 deal(s) closed below an earlier in-limit rival offer (≈5.4 P).

## Sat 12:36 · Duels I · tick 532 · wave of 3 (duels 2430, 2431, 2522)

**This wave:** 3 deals / 3 finished (100%)
- Rival engaged: spoke in 3 → 3 deals (100%); spoke or accepted 3 → 3 (100%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 1 (≈0.6 P: 2522).
- Rounds and decay: 4.3 rounds per deal; result 23.8 of 32.0 P surplus → 8.2 P (26%) lost to decay.
- Latency: answered rival offers in 0.0 ticks on average (max 0; 13 of 13 the same tick); decision 5.6 s mean, 8.9 s max.
- Concessions: we moved 68 P in total, rivals 51 P.
- Rival behaviours (best → worst by our mean result): conceder: 3 duel(s), 3 deal(s), mean result 7.9 P, rival moved 17.0 P per duel.
- Best duel: 2522 vs Rival Plata (seller): 9.7 P in 7 round(s). Worst: 2430 vs Rival Oro (buyer): deal, both still 7 ticks.

**Session so far:** 15 deals / 16 finished (94%)
- Rival engaged: spoke in 16 → 15 deals (94%); spoke or accepted 16 → 15 (94%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 2 (≈5.4 P: 2296, 2522).
- Rounds and decay: 5.5 rounds per deal; result 121.9 of 174.0 P surplus → 52.1 P (30%) lost to decay.
- Latency: answered rival offers in 0.7 ticks on average (max 5; 80 of 113 the same tick); decision 6.1 s mean, 25.0 s max; 1 rival offer(s) never answered.
- Concessions: we moved 455 P in total, rivals 429 P.
- Rival behaviours (best → worst by our mean result): conceder: 12 duel(s), 12 deal(s), mean result 8.4 P, rival moved 35.8 P per duel · holder (never moved): 4 duel(s), 3 deal(s), mean result 5.2 P, rival moved 0.0 P per duel.
- Best duel: 2541 vs Rival Azul (buyer): 14.5 P in 6 round(s). Worst: 2367 vs Rival Oro (buyer): no_deal, both still 5 ticks.

**For Aleks:**
1. Break holds: 1 no-deal duel(s) sat still up to 5 ticks with time left (2367). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
2. Close in fewer exchanges: 52.1 P (30%) of deal value went to decay over 5.5 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).
3. Decay-aware accept: 2 deal(s) closed below an earlier in-limit rival offer (≈5.4 P).

## Sat 12:29 · Duels I · tick 519 · wave of 3 (duels 2319, 2356, 2357)

**This wave:** 3 deals / 3 finished (100%)
- Rival engaged: spoke in 3 → 3 deals (100%); spoke or accepted 3 → 3 (100%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Rounds and decay: 8.3 rounds per deal; result 21.7 of 36.0 P surplus → 14.3 P (40%) lost to decay.
- Latency: answered rival offers in 0.4 ticks on average (max 4; 19 of 26 the same tick); decision 6.1 s mean, 25.0 s max.
- Concessions: we moved 91 P in total, rivals 145 P.
- Rival behaviours (best → worst by our mean result): conceder: 3 duel(s), 3 deal(s), mean result 7.2 P, rival moved 48.3 P per duel.
- Best duel: 2357 vs Rival Noche (buyer): 9.7 P in 6 round(s). Worst: 2319 vs Rival Oro (buyer): deal.

**Session so far:** 12 deals / 13 finished (92%)
- Rival engaged: spoke in 13 → 12 deals (92%); spoke or accepted 13 → 12 (92%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 1 (≈4.7 P: 2296).
- Rounds and decay: 5.8 rounds per deal; result 98.1 of 142.0 P surplus → 43.9 P (31%) lost to decay.
- Latency: answered rival offers in 0.8 ticks on average (max 5; 67 of 100 the same tick); decision 6.2 s mean, 25.0 s max; 1 rival offer(s) never answered.
- Concessions: we moved 387 P in total, rivals 378 P.
- Rival behaviours (best → worst by our mean result): conceder: 9 duel(s), 9 deal(s), mean result 8.6 P, rival moved 42.0 P per duel · holder (never moved): 4 duel(s), 3 deal(s), mean result 5.2 P, rival moved 0.0 P per duel.
- Best duel: 2541 vs Rival Azul (buyer): 14.5 P in 6 round(s). Worst: 2367 vs Rival Oro (buyer): no_deal, both still 5 ticks.

**For Aleks:**
1. Break holds: 1 no-deal duel(s) sat still up to 5 ticks with time left (2367). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
2. Close in fewer exchanges: 43.9 P (31%) of deal value went to decay over 5.8 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).
3. Decay-aware accept: 1 deal(s) closed below an earlier in-limit rival offer (≈4.7 P).

## Sat 12:23 · Duels I · tick 507 · wave of 3 (duels 2318, 2367, 2541)

**This wave:** 2 deals / 3 finished (67%)
- Rival engaged: spoke in 3 → 2 deals (67%); spoke or accepted 3 → 2 (67%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Rounds and decay: 7.5 rounds per deal; result 20.8 of 32.0 P surplus → 11.2 P (35%) lost to decay.
- Latency: answered rival offers in 1.1 ticks on average (max 5; 19 of 31 the same tick); decision 5.8 s mean, 8.1 s max; 1 rival offer(s) never answered.
- Concessions: we moved 77 P in total, rivals 79 P.
- Rival behaviours (best → worst by our mean result): conceder: 2 duel(s), 2 deal(s), mean result 10.4 P, rival moved 39.5 P per duel · holder (never moved): 1 duel(s), 0 deal(s), mean result 0.0 P, rival moved 0.0 P per duel.
- Best duel: 2541 vs Rival Azul (buyer): 14.5 P in 6 round(s). Worst: 2367 vs Rival Oro (buyer): no_deal, both still 5 ticks.

**Session so far:** 9 deals / 10 finished (90%)
- Rival engaged: spoke in 10 → 9 deals (90%); spoke or accepted 10 → 9 (90%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 1 (≈4.7 P: 2296).
- Rounds and decay: 5.0 rounds per deal; result 76.4 of 106.0 P surplus → 29.6 P (28%) lost to decay.
- Latency: answered rival offers in 0.9 ticks on average (max 5; 48 of 74 the same tick); decision 6.2 s mean, 14.5 s max; 1 rival offer(s) never answered.
- Concessions: we moved 296 P in total, rivals 233 P.
- Rival behaviours (best → worst by our mean result): conceder: 6 duel(s), 6 deal(s), mean result 9.3 P, rival moved 38.8 P per duel · holder (never moved): 4 duel(s), 3 deal(s), mean result 5.2 P, rival moved 0.0 P per duel.
- Best duel: 2541 vs Rival Azul (buyer): 14.5 P in 6 round(s). Worst: 2367 vs Rival Oro (buyer): no_deal, both still 5 ticks.

**For Aleks:**
1. Break holds: 1 no-deal duel(s) sat still up to 5 ticks with time left (2367). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
2. Close in fewer exchanges: 29.6 P (28%) of deal value went to decay over 5.0 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).
3. Decay-aware accept: 1 deal(s) closed below an earlier in-limit rival offer (≈4.7 P).

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
