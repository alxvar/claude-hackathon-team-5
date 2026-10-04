# Duel review

_Written by `tools/duel_monitor.py` after each wave of our duels, newest first. Advisory for Aleks (the duelist is his). Result = our surplus × (1 − decay)^rounds, rounds = min(our priced offers, theirs); "spoke" = the rival sent at least one price._

## Sun 11:26 · Duels III · tick 1970 · wave of 4 (duels 11360, 11389, 11452, 11501)

**This wave:** 4 deals / 4 finished (100%)
- Rival engaged: spoke in 4 → 4 deals (100%); spoke or accepted 4 → 4 (100%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 1 (≈0.7 P: 11452).
- Rounds and decay: 2.5 rounds per deal; result 59.9 of 79.0 P surplus → 19.1 P (24%) lost to decay.
- Latency: answered rival offers in 4.2 ticks on average (max 9; 2 of 19 the same tick); decision 0.4 s mean, 1.9 s max.
- Concessions: we moved 105 P in total, rivals 110 P.
- Rival behaviours (best → worst by our mean result): conceder: 4 duel(s), 4 deal(s), mean result 15.0 P, rival moved 27.5 P per duel.
- Best duel: 11501 vs Rival Noche (buyer): 25.5 P in 3 round(s). Worst: 11360 vs Rival Plata (seller): deal, both still 7 ticks.

**Session so far:** 32 deals / 40 finished (80%)
- Rival engaged: spoke in 34 → 31 deals (91%); spoke or accepted 35 → 32 (91%); silent 6 (1 took our opener, 5 no deal).
- In-limit offers not accepted: 3 — 11124 (seller, limit 40, vs Rival Verde): ≈14.6 P left on the table; 11352 (seller, limit 110, vs Rival Verde): ≈8.0 P left on the table; 11518 (buyer, limit 107, vs Rival Oro): ≈3.6 P left on the table.
- Deals below an earlier in-limit rival offer: 13 (≈109.1 P: 11117, 11125, 11128, 11177, 11195, 11243, 11285, 11304, 11353, 11452, 11500, 11612, 11613).
- Rounds and decay: 1.8 rounds per deal; result 817.4 of 839.0 P surplus → 21.6 P (3%) lost to decay.
- Latency: answered rival offers in 3.8 ticks on average (max 9; 14 of 126 the same tick); decision 0.4 s mean, 2.5 s max; 2 rival offer(s) never answered.
- Concessions: we moved 1044 P in total, rivals 710 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 10 duel(s), 10 deal(s), mean result 39.6 P, rival moved 0.0 P per duel · conceder: 21 duel(s), 19 deal(s), mean result 18.1 P, rival moved 35.8 P per duel · hardener (moved away): 3 duel(s), 2 deal(s), mean result 11.0 P, rival moved -13.7 P per duel · accept-only (took our opener): 1 duel(s), 1 deal(s), mean result 8.0 P · silent: 5 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 11116 vs Rival Rojo (seller): 82.9 P in 1 round(s). Worst: 11124 vs Rival Verde (seller): no_deal, 14.6 P in-limit left, both still 6 ticks.

**For Aleks:**
1. Guard: 1 deal(s) closed outside our limit (11129): block any accept/offer past the limit in code.
2. Accept earlier: 3 deal(s) lost with the rival's offer inside our limit (11124, 11352, 11518; ≈26.2 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
3. Break holds: 3 no-deal duel(s) sat still up to 6 ticks with time left (11124, 11352, 11518). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).

## Sun 11:24 · Duels III · tick 1959 · wave of 4 (duels 11372, 11388, 11500, 11518)

**This wave:** 2 deals / 4 finished (50%)
- Rival engaged: spoke in 3 → 2 deals (67%); spoke or accepted 3 → 2 (67%); silent 1 (0 took our opener, 1 no deal).
- In-limit offers not accepted: 1 — 11518 (buyer, limit 107, vs Rival Oro): ≈3.6 P left on the table.
- Deals below an earlier in-limit rival offer: 1 (≈0.8 P: 11500).
- Rounds and decay: 1.5 rounds per deal; result 37.9 of 43.0 P surplus → 5.1 P (12%) lost to decay.
- Latency: answered rival offers in 5.2 ticks on average (max 9; 1 of 13 the same tick); decision 0.4 s mean, 1.6 s max; 1 rival offer(s) never answered.
- Concessions: we moved 148 P in total, rivals 52 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 1 duel(s), 1 deal(s), mean result 30.6 P, rival moved 0.0 P per duel · conceder: 1 duel(s), 1 deal(s), mean result 7.3 P, rival moved 54.0 P per duel · silent: 1 duel(s), 0 deal(s), mean result 0.0 P · hardener (moved away): 1 duel(s), 0 deal(s), mean result 0.0 P, rival moved -2.0 P per duel.
- Best duel: 11388 vs Rival Rojo (buyer): 30.6 P in 1 round(s). Worst: 11518 vs Rival Oro (buyer): no_deal, 3.6 P in-limit left, both still 5 ticks.

**Session so far:** 28 deals / 36 finished (78%)
- Rival engaged: spoke in 30 → 27 deals (90%); spoke or accepted 31 → 28 (90%); silent 6 (1 took our opener, 5 no deal).
- In-limit offers not accepted: 3 — 11124 (seller, limit 40, vs Rival Verde): ≈14.6 P left on the table; 11352 (seller, limit 110, vs Rival Verde): ≈8.0 P left on the table; 11518 (buyer, limit 107, vs Rival Oro): ≈3.6 P left on the table.
- Deals below an earlier in-limit rival offer: 12 (≈108.4 P: 11117, 11125, 11128, 11177, 11195, 11243, 11285, 11304, 11353, 11500, 11612, 11613).
- Rounds and decay: 1.7 rounds per deal; result 757.5 of 760.0 P surplus → 2.5 P (0%) lost to decay.
- Latency: answered rival offers in 3.8 ticks on average (max 9; 12 of 107 the same tick); decision 0.4 s mean, 2.5 s max; 2 rival offer(s) never answered.
- Concessions: we moved 939 P in total, rivals 600 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 10 duel(s), 10 deal(s), mean result 39.6 P, rival moved 0.0 P per duel · conceder: 17 duel(s), 15 deal(s), mean result 18.9 P, rival moved 37.7 P per duel · hardener (moved away): 3 duel(s), 2 deal(s), mean result 11.0 P, rival moved -13.7 P per duel · accept-only (took our opener): 1 duel(s), 1 deal(s), mean result 8.0 P · silent: 5 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 11116 vs Rival Rojo (seller): 82.9 P in 1 round(s). Worst: 11124 vs Rival Verde (seller): no_deal, 14.6 P in-limit left, both still 6 ticks.

**For Aleks:**
1. Guard: 1 deal(s) closed outside our limit (11129): block any accept/offer past the limit in code.
2. Accept earlier: 3 deal(s) lost with the rival's offer inside our limit (11124, 11352, 11518; ≈26.2 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
3. Break holds: 3 no-deal duel(s) sat still up to 6 ticks with time left (11124, 11352, 11518). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).

## Sun 11:20 · Duels III · tick 1947 · wave of 4 (duels 11241, 11284, 11285, 11470)

**This wave:** 4 deals / 4 finished (100%)
- Rival engaged: spoke in 3 → 3 deals (100%); spoke or accepted 4 → 4 (100%); silent 1 (1 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 1 (≈8.1 P: 11285).
- Rounds and decay: 1.2 rounds per deal; result 98.9 of 44.0 P surplus → -54.9 P (-125%) lost to decay.
- Latency: answered rival offers in 3.9 ticks on average (max 9; 1 of 12 the same tick); decision 0.4 s mean, 1.6 s max.
- Concessions: we moved 99 P in total, rivals -14 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 1 duel(s), 1 deal(s), mean result 74.2 P, rival moved 0.0 P per duel · conceder: 1 duel(s), 1 deal(s), mean result 16.7 P, rival moved 23.0 P per duel · accept-only (took our opener): 1 duel(s), 1 deal(s), mean result 8.0 P · hardener (moved away): 1 duel(s), 1 deal(s), mean result 0.0 P, rival moved -37.0 P per duel.
- Best duel: 11470 vs Rival Luna (seller): 74.2 P in 1 round(s). Worst: 11285 vs Rival Luna (buyer): deal, both still 7 ticks.

**Session so far:** 26 deals / 32 finished (81%)
- Rival engaged: spoke in 27 → 25 deals (93%); spoke or accepted 28 → 26 (93%); silent 5 (1 took our opener, 4 no deal).
- In-limit offers not accepted: 2 — 11124 (seller, limit 40, vs Rival Verde): ≈14.6 P left on the table; 11352 (seller, limit 110, vs Rival Verde): ≈8.0 P left on the table.
- Deals below an earlier in-limit rival offer: 11 (≈107.6 P: 11117, 11125, 11128, 11177, 11195, 11243, 11285, 11304, 11353, 11612, 11613).
- Rounds and decay: 1.7 rounds per deal; result 719.6 of 717.0 P surplus → -2.6 P (-0%) lost to decay.
- Latency: answered rival offers in 3.6 ticks on average (max 9; 11 of 94 the same tick); decision 0.5 s mean, 2.5 s max; 1 rival offer(s) never answered.
- Concessions: we moved 791 P in total, rivals 548 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 9 duel(s), 9 deal(s), mean result 40.6 P, rival moved 0.0 P per duel · conceder: 16 duel(s), 14 deal(s), mean result 19.6 P, rival moved 36.7 P per duel · hardener (moved away): 2 duel(s), 2 deal(s), mean result 16.4 P, rival moved -19.5 P per duel · accept-only (took our opener): 1 duel(s), 1 deal(s), mean result 8.0 P · silent: 4 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 11116 vs Rival Rojo (seller): 82.9 P in 1 round(s). Worst: 11124 vs Rival Verde (seller): no_deal, 14.6 P in-limit left, both still 6 ticks.

**For Aleks:**
1. Guard: 1 deal(s) closed outside our limit (11129): block any accept/offer past the limit in code.
2. Accept earlier: 2 deal(s) lost with the rival's offer inside our limit (11124, 11352; ≈22.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
3. Break holds: 2 no-deal duel(s) sat still up to 6 ticks with time left (11124, 11352). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).

## Sun 11:18 · Duels III · tick 1937 · wave of 4 (duels 11266, 11267, 11280, 11305)

**This wave:** 4 deals / 4 finished (100%)
- Rival engaged: spoke in 4 → 4 deals (100%); spoke or accepted 4 → 4 (100%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Rounds and decay: 1.5 rounds per deal; result 155.0 of 119.0 P surplus → -36.0 P (-30%) lost to decay.
- Latency: answered rival offers in 4.2 ticks on average (max 9; 0 of 9 the same tick); decision 0.4 s mean, 1.5 s max.
- Concessions: we moved 26 P in total, rivals 63 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 1 duel(s), 1 deal(s), mean result 43.5 P, rival moved 0.0 P per duel · conceder: 2 duel(s), 2 deal(s), mean result 39.3 P, rival moved 32.5 P per duel · hardener (moved away): 1 duel(s), 1 deal(s), mean result 32.9 P, rival moved -2.0 P per duel.
- Best duel: 11267 vs Rival Verde (seller): 60.8 P in 1 round(s). Worst: 11305 vs Rival Sol (seller): deal.

**Session so far:** 22 deals / 28 finished (79%)
- Rival engaged: spoke in 24 → 22 deals (92%); spoke or accepted 24 → 22 (92%); silent 4 (0 took our opener, 4 no deal).
- In-limit offers not accepted: 2 — 11124 (seller, limit 40, vs Rival Verde): ≈14.6 P left on the table; 11352 (seller, limit 110, vs Rival Verde): ≈8.0 P left on the table.
- Deals below an earlier in-limit rival offer: 10 (≈99.5 P: 11117, 11125, 11128, 11177, 11195, 11243, 11304, 11353, 11612, 11613).
- Rounds and decay: 1.8 rounds per deal; result 620.7 of 673.0 P surplus → 52.3 P (8%) lost to decay.
- Latency: answered rival offers in 3.5 ticks on average (max 9; 10 of 82 the same tick); decision 0.5 s mean, 2.5 s max; 1 rival offer(s) never answered.
- Concessions: we moved 692 P in total, rivals 562 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 8 duel(s), 8 deal(s), mean result 36.4 P, rival moved 0.0 P per duel · hardener (moved away): 1 duel(s), 1 deal(s), mean result 32.9 P, rival moved -2.0 P per duel · conceder: 15 duel(s), 13 deal(s), mean result 19.8 P, rival moved 37.6 P per duel · silent: 4 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 11116 vs Rival Rojo (seller): 82.9 P in 1 round(s). Worst: 11124 vs Rival Verde (seller): no_deal, 14.6 P in-limit left, both still 6 ticks.

**For Aleks:**
1. Guard: 1 deal(s) closed outside our limit (11129): block any accept/offer past the limit in code.
2. Accept earlier: 2 deal(s) lost with the rival's offer inside our limit (11124, 11352; ≈22.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
3. Break holds: 2 no-deal duel(s) sat still up to 6 ticks with time left (11124, 11352). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).

## Sun 11:16 · Duels III · tick 1928 · wave of 4 (duels 11195, 11243, 11281, 11304)

**This wave:** 4 deals / 4 finished (100%)
- Rival engaged: spoke in 4 → 4 deals (100%); spoke or accepted 4 → 4 (100%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 3 (≈58.0 P: 11195, 11243, 11304).
- Rounds and decay: 1.8 rounds per deal; result 88.0 of 167.0 P surplus → 79.0 P (47%) lost to decay.
- Latency: answered rival offers in 3.4 ticks on average (max 9; 3 of 23 the same tick); decision 0.4 s mean, 1.8 s max.
- Concessions: we moved 40 P in total, rivals 123 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 1 duel(s), 1 deal(s), mean result 49.2 P, rival moved 0.0 P per duel · conceder: 3 duel(s), 3 deal(s), mean result 12.9 P, rival moved 41.0 P per duel.
- Best duel: 11281 vs Rival Plata (buyer): 49.2 P in 1 round(s). Worst: 11304 vs Rival Luna (buyer): deal.

**Session so far:** 18 deals / 24 finished (75%)
- Rival engaged: spoke in 20 → 18 deals (90%); spoke or accepted 20 → 18 (90%); silent 4 (0 took our opener, 4 no deal).
- In-limit offers not accepted: 2 — 11124 (seller, limit 40, vs Rival Verde): ≈14.6 P left on the table; 11352 (seller, limit 110, vs Rival Verde): ≈8.0 P left on the table.
- Deals below an earlier in-limit rival offer: 10 (≈99.5 P: 11117, 11125, 11128, 11177, 11195, 11243, 11304, 11353, 11612, 11613).
- Rounds and decay: 1.8 rounds per deal; result 465.7 of 554.0 P surplus → 88.3 P (16%) lost to decay.
- Latency: answered rival offers in 3.4 ticks on average (max 9; 10 of 73 the same tick); decision 0.5 s mean, 2.5 s max; 1 rival offer(s) never answered.
- Concessions: we moved 666 P in total, rivals 499 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 7 duel(s), 7 deal(s), mean result 35.3 P, rival moved 0.0 P per duel · conceder: 13 duel(s), 11 deal(s), mean result 16.8 P, rival moved 38.4 P per duel · silent: 4 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 11116 vs Rival Rojo (seller): 82.9 P in 1 round(s). Worst: 11124 vs Rival Verde (seller): no_deal, 14.6 P in-limit left, both still 6 ticks.

**For Aleks:**
1. Guard: 1 deal(s) closed outside our limit (11129): block any accept/offer past the limit in code.
2. Accept earlier: 2 deal(s) lost with the rival's offer inside our limit (11124, 11352; ≈22.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
3. Break holds: 2 no-deal duel(s) sat still up to 6 ticks with time left (11124, 11352). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).

## Sun 11:14 · Duels III · tick 1921 · wave of 4 (duels 11194, 11240, 11242, 11353)

**This wave:** 4 deals / 4 finished (100%)
- Rival engaged: spoke in 4 → 4 deals (100%); spoke or accepted 4 → 4 (100%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 1 (≈3.6 P: 11353).
- Rounds and decay: 2.5 rounds per deal; result 23.2 of 31.0 P surplus → 7.8 P (25%) lost to decay.
- Latency: answered rival offers in 3.6 ticks on average (max 9; 3 of 22 the same tick); decision 0.5 s mean, 1.6 s max.
- Concessions: we moved 140 P in total, rivals 174 P.
- Rival behaviours (best → worst by our mean result): conceder: 3 duel(s), 3 deal(s), mean result 7.1 P, rival moved 58.0 P per duel · holder (never moved): 1 duel(s), 1 deal(s), mean result 1.8 P, rival moved 0.0 P per duel.
- Best duel: 11194 vs Rival Azul (seller): 19.0 P in 3 round(s). Worst: 11353 vs Rival Verde (buyer): deal, both still 3 ticks.

**Session so far:** 14 deals / 20 finished (70%)
- Rival engaged: spoke in 16 → 14 deals (88%); spoke or accepted 16 → 14 (88%); silent 4 (0 took our opener, 4 no deal).
- In-limit offers not accepted: 2 — 11124 (seller, limit 40, vs Rival Verde): ≈14.6 P left on the table; 11352 (seller, limit 110, vs Rival Verde): ≈8.0 P left on the table.
- Deals below an earlier in-limit rival offer: 7 (≈41.5 P: 11117, 11125, 11128, 11177, 11353, 11612, 11613).
- Rounds and decay: 1.9 rounds per deal; result 377.7 of 387.0 P surplus → 9.3 P (2%) lost to decay.
- Latency: answered rival offers in 3.4 ticks on average (max 9; 7 of 50 the same tick); decision 0.5 s mean, 2.5 s max; 1 rival offer(s) never answered.
- Concessions: we moved 626 P in total, rivals 376 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 6 duel(s), 6 deal(s), mean result 33.0 P, rival moved 0.0 P per duel · conceder: 10 duel(s), 8 deal(s), mean result 18.0 P, rival moved 37.6 P per duel · silent: 4 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 11116 vs Rival Rojo (seller): 82.9 P in 1 round(s). Worst: 11124 vs Rival Verde (seller): no_deal, 14.6 P in-limit left, both still 6 ticks.

**For Aleks:**
1. Guard: 1 deal(s) closed outside our limit (11129): block any accept/offer past the limit in code.
2. Accept earlier: 2 deal(s) lost with the rival's offer inside our limit (11124, 11352; ≈22.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
3. Break holds: 2 no-deal duel(s) sat still up to 6 ticks with time left (11124, 11352). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).

## Sun 11:11 · Duels III · tick 1910 · wave of 4 (duels 11145, 11352, 11510, 11613)

**This wave:** 2 deals / 4 finished (50%)
- Rival engaged: spoke in 3 → 2 deals (67%); spoke or accepted 3 → 2 (67%); silent 1 (0 took our opener, 1 no deal).
- In-limit offers not accepted: 1 — 11352 (seller, limit 110, vs Rival Verde): ≈8.0 P left on the table.
- Deals below an earlier in-limit rival offer: 1 (≈5.3 P: 11613).
- Rounds and decay: 2.0 rounds per deal; result 56.9 of 72.0 P surplus → 15.1 P (21%) lost to decay.
- Latency: answered rival offers in 2.9 ticks on average (max 7; 1 of 13 the same tick); decision 0.5 s mean, 1.7 s max; 1 rival offer(s) never answered.
- Concessions: we moved 141 P in total, rivals 53 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 1 duel(s), 1 deal(s), mean result 37.9 P, rival moved 0.0 P per duel · conceder: 2 duel(s), 1 deal(s), mean result 9.5 P, rival moved 26.5 P per duel · silent: 1 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 11510 vs Rival Verde (buyer): 37.9 P in 1 round(s). Worst: 11352 vs Rival Verde (seller): no_deal, 8.0 P in-limit left, both still 4 ticks.

**Session so far:** 10 deals / 16 finished (62%)
- Rival engaged: spoke in 12 → 10 deals (83%); spoke or accepted 12 → 10 (83%); silent 4 (0 took our opener, 4 no deal).
- In-limit offers not accepted: 2 — 11124 (seller, limit 40, vs Rival Verde): ≈14.6 P left on the table; 11352 (seller, limit 110, vs Rival Verde): ≈8.0 P left on the table.
- Deals below an earlier in-limit rival offer: 6 (≈37.8 P: 11117, 11125, 11128, 11177, 11612, 11613).
- Rounds and decay: 1.6 rounds per deal; result 354.5 of 356.0 P surplus → 1.5 P (0%) lost to decay.
- Latency: answered rival offers in 3.2 ticks on average (max 9; 4 of 28 the same tick); decision 0.5 s mean, 2.5 s max; 1 rival offer(s) never answered.
- Concessions: we moved 486 P in total, rivals 202 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 5 duel(s), 5 deal(s), mean result 39.3 P, rival moved 0.0 P per duel · conceder: 7 duel(s), 5 deal(s), mean result 22.6 P, rival moved 28.9 P per duel · silent: 4 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 11116 vs Rival Rojo (seller): 82.9 P in 1 round(s). Worst: 11124 vs Rival Verde (seller): no_deal, 14.6 P in-limit left, both still 6 ticks.

**For Aleks:**
1. Guard: 1 deal(s) closed outside our limit (11129): block any accept/offer past the limit in code.
2. Accept earlier: 2 deal(s) lost with the rival's offer inside our limit (11124, 11352; ≈22.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
3. Break holds: 2 no-deal duel(s) sat still up to 6 ticks with time left (11124, 11352). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).

## Sun 11:08 · Duels III · tick 1898 · wave of 4 (duels 11144, 11176, 11177, 11612)

**This wave:** 3 deals / 4 finished (75%)
- Rival engaged: spoke in 3 → 3 deals (100%); spoke or accepted 3 → 3 (100%); silent 1 (0 took our opener, 1 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 2 (≈10.2 P: 11177, 11612).
- Rounds and decay: 2.0 rounds per deal; result 87.0 of 108.0 P surplus → 21.0 P (19%) lost to decay.
- Latency: answered rival offers in 2.6 ticks on average (max 7; 2 of 8 the same tick); decision 0.5 s mean, 1.7 s max.
- Concessions: we moved 120 P in total, rivals 100 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 1 duel(s), 1 deal(s), mean result 33.3 P, rival moved 0.0 P per duel · conceder: 2 duel(s), 2 deal(s), mean result 26.8 P, rival moved 50.0 P per duel · silent: 1 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 11612 vs Rival Oro (seller): 34.3 P in 3 round(s). Worst: 11144 vs Rival Azul (seller): no_deal.

**Session so far:** 8 deals / 12 finished (67%)
- Rival engaged: spoke in 9 → 8 deals (89%); spoke or accepted 9 → 8 (89%); silent 3 (0 took our opener, 3 no deal).
- In-limit offers not accepted: 1 — 11124 (seller, limit 40, vs Rival Verde): ≈14.6 P left on the table.
- Deals below an earlier in-limit rival offer: 5 (≈32.5 P: 11117, 11125, 11128, 11177, 11612).
- Rounds and decay: 1.5 rounds per deal; result 297.6 of 284.0 P surplus → -13.6 P (-5%) lost to decay.
- Latency: answered rival offers in 3.5 ticks on average (max 9; 3 of 15 the same tick); decision 0.5 s mean, 2.5 s max.
- Concessions: we moved 345 P in total, rivals 149 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 4 duel(s), 4 deal(s), mean result 39.6 P, rival moved 0.0 P per duel · conceder: 5 duel(s), 4 deal(s), mean result 27.8 P, rival moved 29.8 P per duel · silent: 3 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 11116 vs Rival Rojo (seller): 82.9 P in 1 round(s). Worst: 11124 vs Rival Verde (seller): no_deal, 14.6 P in-limit left, both still 6 ticks.

**For Aleks:**
1. Guard: 1 deal(s) closed outside our limit (11129): block any accept/offer past the limit in code.
2. Accept earlier: 1 deal(s) lost with the rival's offer inside our limit (11124; ≈14.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
3. Break holds: 1 no-deal duel(s) sat still up to 6 ticks with time left (11124). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).

## Sun 11:05 · Duels III · tick 1886 · wave of 4 (duels 11116, 11117, 11124, 11125)

**This wave:** 3 deals / 4 finished (75%)
- Rival engaged: spoke in 4 → 3 deals (75%); spoke or accepted 4 → 3 (75%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 1 — 11124 (seller, limit 40, vs Rival Verde): ≈14.6 P left on the table.
- Deals below an earlier in-limit rival offer: 2 (≈19.6 P: 11117, 11125).
- Rounds and decay: 1.0 rounds per deal; result 129.0 of 120.0 P surplus → -9.0 P (-8%) lost to decay.
- Latency: answered rival offers in 3.8 ticks on average (max 7; 1 of 4 the same tick); decision 0.6 s mean, 1.6 s max.
- Concessions: we moved 80 P in total, rivals 31 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 2 duel(s), 2 deal(s), mean result 41.5 P, rival moved 0.0 P per duel · conceder: 2 duel(s), 1 deal(s), mean result 23.1 P, rival moved 15.5 P per duel.
- Best duel: 11116 vs Rival Rojo (seller): 82.9 P in 1 round(s). Worst: 11124 vs Rival Verde (seller): no_deal, 14.6 P in-limit left, both still 6 ticks.

**Session so far:** 5 deals / 8 finished (62%)
- Rival engaged: spoke in 6 → 5 deals (83%); spoke or accepted 6 → 5 (83%); silent 2 (0 took our opener, 2 no deal).
- In-limit offers not accepted: 1 — 11124 (seller, limit 40, vs Rival Verde): ≈14.6 P left on the table.
- Deals below an earlier in-limit rival offer: 3 (≈22.3 P: 11117, 11125, 11128).
- Rounds and decay: 1.2 rounds per deal; result 210.6 of 176.0 P surplus → -34.6 P (-20%) lost to decay.
- Latency: answered rival offers in 4.6 ticks on average (max 9; 1 of 7 the same tick); decision 0.5 s mean, 2.5 s max.
- Concessions: we moved 225 P in total, rivals 49 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 3 duel(s), 3 deal(s), mean result 41.7 P, rival moved 0.0 P per duel · conceder: 3 duel(s), 2 deal(s), mean result 28.5 P, rival moved 16.3 P per duel · silent: 2 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 11116 vs Rival Rojo (seller): 82.9 P in 1 round(s). Worst: 11124 vs Rival Verde (seller): no_deal, 14.6 P in-limit left, both still 6 ticks.

**For Aleks:**
1. Guard: 1 deal(s) closed outside our limit (11129): block any accept/offer past the limit in code.
2. Accept earlier: 1 deal(s) lost with the rival's offer inside our limit (11124; ≈14.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
3. Break holds: 1 no-deal duel(s) sat still up to 6 ticks with time left (11124). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).

## Sun 11:02 · Duels III · tick 1874 · wave of 4 (duels 11120, 11121, 11128, 11129)

**This wave:** 2 deals / 4 finished (50%)
- Rival engaged: spoke in 2 → 2 deals (100%); spoke or accepted 2 → 2 (100%); silent 2 (0 took our opener, 2 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 1 (≈2.7 P: 11128).
- Rounds and decay: 1.5 rounds per deal; result 81.6 of 56.0 P surplus → -25.6 P (-46%) lost to decay.
- Latency: answered rival offers in 5.7 ticks on average (max 9; 0 of 3 the same tick); decision 0.5 s mean, 2.5 s max.
- Concessions: we moved 145 P in total, rivals 18 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 1 duel(s), 1 deal(s), mean result 42.2 P, rival moved 0.0 P per duel · conceder: 1 duel(s), 1 deal(s), mean result 39.4 P, rival moved 18.0 P per duel · silent: 2 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 11129 vs Rival Rojo (seller): 42.2 P in 1 round(s). Worst: 11120 vs Rival Noche (seller): no_deal.

**Session so far:** 2 deals / 4 finished (50%)
- Rival engaged: spoke in 2 → 2 deals (100%); spoke or accepted 2 → 2 (100%); silent 2 (0 took our opener, 2 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 1 (≈2.7 P: 11128).
- Rounds and decay: 1.5 rounds per deal; result 81.6 of 56.0 P surplus → -25.6 P (-46%) lost to decay.
- Latency: answered rival offers in 5.7 ticks on average (max 9; 0 of 3 the same tick); decision 0.5 s mean, 2.5 s max.
- Concessions: we moved 145 P in total, rivals 18 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 1 duel(s), 1 deal(s), mean result 42.2 P, rival moved 0.0 P per duel · conceder: 1 duel(s), 1 deal(s), mean result 39.4 P, rival moved 18.0 P per duel · silent: 2 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 11129 vs Rival Rojo (seller): 42.2 P in 1 round(s). Worst: 11120 vs Rival Noche (seller): no_deal.

**For Aleks:**
1. Guard: 1 deal(s) closed outside our limit (11129): block any accept/offer past the limit in code.
2. Answer faster: 5.7 ticks on average from a rival offer to our reply.
3. Decay-aware accept: 1 deal(s) closed below an earlier in-limit rival offer (≈2.7 P).

## Sat 22:38 · Duels II · tick 1401 · wave of 2 (duels 6140, 6141)

**This wave:** 2 deals / 2 finished (100%)
- Rival engaged: spoke in 2 → 2 deals (100%); spoke or accepted 2 → 2 (100%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Rounds and decay: 1.0 rounds per deal; result 81.0 of 88.0 P surplus → 7.0 P (8%) lost to decay.
- Latency: answered rival offers in 0.0 ticks on average (max 0; 2 of 2 the same tick); decision 8.6 s mean, 11.9 s max.
- Concessions: we moved 4 P in total, rivals 0 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 2 duel(s), 2 deal(s), mean result 40.5 P, rival moved 0.0 P per duel.
- Best duel: 6140 vs Rival Rojo (seller): 41.4 P in 1 round(s). Worst: 6141 vs Rival Noche (buyer): deal.

**Session so far:** 56 deals / 68 finished (82%)
- Rival engaged: spoke in 61 → 54 deals (89%); spoke or accepted 63 → 56 (89%); silent 7 (2 took our opener, 5 no deal).
- In-limit offers not accepted: 4 — 5618 (buyer, limit 50, vs Rival Azul): ≈3.1 P left on the table; 5622 (seller, limit 83, vs Rival Plata): ≈19.5 P left on the table; 5813 (buyer, limit 97, vs Rival Oro): ≈5.0 P left on the table; 6177 (buyer, limit 76, vs Rival Plata): ≈3.6 P left on the table.
- Deals below an earlier in-limit rival offer: 20 (≈184.1 P: 5623, 5653, 5663, 5737, 5797, 5808, 5827, 5892, 5969, 6022, 6023, 6041, 6049, 6094, 6095, 6100, 6170, 6171, 6184, 6190).
- Rounds and decay: 3.5 rounds per deal; result 1210.1 of 1552.0 P surplus → 341.9 P (22%) lost to decay.
- Latency: answered rival offers in 1.0 ticks on average (max 11; 168 of 278 the same tick); decision 7.5 s mean, 21.9 s max; 1 rival offer(s) never answered.
- Concessions: we moved 1451 P in total, rivals 1228 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 7 duel(s), 5 deal(s), mean result 19.7 P, rival moved 0.0 P per duel · conceder: 51 duel(s), 46 deal(s), mean result 19.5 P, rival moved 25.3 P per duel · hardener (moved away): 3 duel(s), 3 deal(s), mean result 15.9 P, rival moved -20.3 P per duel · accept-only (took our opener): 2 duel(s), 2 deal(s), mean result 14.1 P · silent: 5 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 5652 vs Rival Verde (seller): 52.9 P in 2 round(s). Worst: 5622 vs Rival Plata (seller): no_deal, 19.5 P in-limit left, both still 4 ticks.

**For Aleks:**
1. Accept earlier: 4 deal(s) lost with the rival's offer inside our limit (5618, 5622, 5813, 6177; ≈31.2 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
2. Break holds: 4 no-deal duel(s) sat still up to 5 ticks with time left (5618, 5622, 5813, 6177). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
3. Close in fewer exchanges: 341.9 P (22%) of deal value went to decay over 3.5 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).

## Sat 22:31 · Duels II · tick 1388 · wave of 6 (duels 6007, 6177, 6182, 6183, 6190, 6191)

**This wave:** 3 deals / 6 finished (50%)
- Rival engaged: spoke in 4 → 2 deals (50%); spoke or accepted 5 → 3 (60%); silent 2 (1 took our opener, 1 no deal).
- In-limit offers not accepted: 1 — 6177 (buyer, limit 76, vs Rival Plata): ≈3.6 P left on the table.
- Deals below an earlier in-limit rival offer: 1 (≈21.5 P: 6190).
- Rounds and decay: 2.0 rounds per deal; result 56.0 of 116.0 P surplus → 60.0 P (52%) lost to decay.
- Latency: answered rival offers in 0.8 ticks on average (max 6; 10 of 14 the same tick); decision 5.6 s mean, 15.7 s max.
- Concessions: we moved 127 P in total, rivals 71 P.
- Rival behaviours (best → worst by our mean result): conceder: 3 duel(s), 2 deal(s), mean result 17.0 P, rival moved 23.7 P per duel · accept-only (took our opener): 1 duel(s), 1 deal(s), mean result 5.0 P · silent: 1 duel(s), 0 deal(s), mean result 0.0 P · holder (never moved): 1 duel(s), 0 deal(s), mean result 0.0 P, rival moved 0.0 P per duel.
- Best duel: 6191 vs Rival Luna (seller): 47.4 P in 2 round(s). Worst: 6177 vs Rival Plata (buyer): no_deal, 3.6 P in-limit left, both still 5 ticks.

**Session so far:** 54 deals / 66 finished (82%)
- Rival engaged: spoke in 59 → 52 deals (88%); spoke or accepted 61 → 54 (89%); silent 7 (2 took our opener, 5 no deal).
- In-limit offers not accepted: 4 — 5618 (buyer, limit 50, vs Rival Azul): ≈3.1 P left on the table; 5622 (seller, limit 83, vs Rival Plata): ≈19.5 P left on the table; 5813 (buyer, limit 97, vs Rival Oro): ≈5.0 P left on the table; 6177 (buyer, limit 76, vs Rival Plata): ≈3.6 P left on the table.
- Deals below an earlier in-limit rival offer: 20 (≈184.1 P: 5623, 5653, 5663, 5737, 5797, 5808, 5827, 5892, 5969, 6022, 6023, 6041, 6049, 6094, 6095, 6100, 6170, 6171, 6184, 6190).
- Rounds and decay: 3.6 rounds per deal; result 1129.1 of 1464.0 P surplus → 334.9 P (23%) lost to decay.
- Latency: answered rival offers in 1.0 ticks on average (max 11; 166 of 276 the same tick); decision 7.5 s mean, 21.9 s max; 1 rival offer(s) never answered.
- Concessions: we moved 1447 P in total, rivals 1228 P.
- Rival behaviours (best → worst by our mean result): conceder: 51 duel(s), 46 deal(s), mean result 19.5 P, rival moved 25.3 P per duel · hardener (moved away): 3 duel(s), 3 deal(s), mean result 15.9 P, rival moved -20.3 P per duel · accept-only (took our opener): 2 duel(s), 2 deal(s), mean result 14.1 P · holder (never moved): 5 duel(s), 3 deal(s), mean result 11.4 P, rival moved 0.0 P per duel · silent: 5 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 5652 vs Rival Verde (seller): 52.9 P in 2 round(s). Worst: 5622 vs Rival Plata (seller): no_deal, 19.5 P in-limit left, both still 4 ticks.

**For Aleks:**
1. Accept earlier: 4 deal(s) lost with the rival's offer inside our limit (5618, 5622, 5813, 6177; ≈31.2 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
2. Break holds: 4 no-deal duel(s) sat still up to 5 ticks with time left (5618, 5622, 5813, 6177). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
3. Close in fewer exchanges: 334.9 P (23%) of deal value went to decay over 3.6 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).

## Sat 22:23 · Duels II · tick 1372 · wave of 6 (duels 6006, 6084, 6085, 6100, 6101, 6176)

**This wave:** 5 deals / 6 finished (83%)
- Rival engaged: spoke in 5 → 5 deals (100%); spoke or accepted 5 → 5 (100%); silent 1 (0 took our opener, 1 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 1 (≈11.1 P: 6100).
- Rounds and decay: 3.6 rounds per deal; result 67.8 of 84.0 P surplus → 16.2 P (19%) lost to decay.
- Latency: answered rival offers in 0.4 ticks on average (max 3; 13 of 18 the same tick); decision 6.9 s mean, 21.9 s max.
- Concessions: we moved 205 P in total, rivals 105 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 1 duel(s), 1 deal(s), mean result 17.5 P, rival moved 0.0 P per duel · conceder: 4 duel(s), 4 deal(s), mean result 12.6 P, rival moved 26.2 P per duel · silent: 1 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 6084 vs Rival Plata (buyer): 19.5 P in 3 round(s). Worst: 6006 vs Rival Verde (seller): no_deal.

**Session so far:** 51 deals / 60 finished (85%)
- Rival engaged: spoke in 55 → 50 deals (91%); spoke or accepted 56 → 51 (91%); silent 5 (1 took our opener, 4 no deal).
- In-limit offers not accepted: 3 — 5618 (buyer, limit 50, vs Rival Azul): ≈3.1 P left on the table; 5622 (seller, limit 83, vs Rival Plata): ≈19.5 P left on the table; 5813 (buyer, limit 97, vs Rival Oro): ≈5.0 P left on the table.
- Deals below an earlier in-limit rival offer: 19 (≈162.7 P: 5623, 5653, 5663, 5737, 5797, 5808, 5827, 5892, 5969, 6022, 6023, 6041, 6049, 6094, 6095, 6100, 6170, 6171, 6184).
- Rounds and decay: 3.7 rounds per deal; result 1073.1 of 1348.0 P surplus → 274.9 P (20%) lost to decay.
- Latency: answered rival offers in 1.0 ticks on average (max 11; 156 of 262 the same tick); decision 7.7 s mean, 21.9 s max; 1 rival offer(s) never answered.
- Concessions: we moved 1320 P in total, rivals 1157 P.
- Rival behaviours (best → worst by our mean result): accept-only (took our opener): 1 duel(s), 1 deal(s), mean result 23.2 P · conceder: 48 duel(s), 44 deal(s), mean result 19.7 P, rival moved 25.4 P per duel · hardener (moved away): 3 duel(s), 3 deal(s), mean result 15.9 P, rival moved -20.3 P per duel · holder (never moved): 4 duel(s), 3 deal(s), mean result 14.2 P, rival moved 0.0 P per duel · silent: 4 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 5652 vs Rival Verde (seller): 52.9 P in 2 round(s). Worst: 5622 vs Rival Plata (seller): no_deal, 19.5 P in-limit left, both still 4 ticks.

**For Aleks:**
1. Accept earlier: 3 deal(s) lost with the rival's offer inside our limit (5618, 5622, 5813; ≈27.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
2. Break holds: 3 no-deal duel(s) sat still up to 5 ticks with time left (5618, 5622, 5813). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
3. Close in fewer exchanges: 274.9 P (20%) of deal value went to decay over 3.7 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).

## Sat 22:16 · Duels II · tick 1357 · wave of 6 (duels 5817, 6049, 6095, 6171, 6184, 6185)

**This wave:** 5 deals / 6 finished (83%)
- Rival engaged: spoke in 5 → 5 deals (100%); spoke or accepted 5 → 5 (100%); silent 1 (0 took our opener, 1 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 4 (≈50.2 P: 6049, 6095, 6171, 6184).
- Rounds and decay: 5.6 rounds per deal; result 38.5 of 79.0 P surplus → 40.5 P (51%) lost to decay.
- Latency: answered rival offers in 0.7 ticks on average (max 4; 26 of 45 the same tick); decision 7.6 s mean, 14.9 s max.
- Concessions: we moved 154 P in total, rivals 39 P.
- Rival behaviours (best → worst by our mean result): conceder: 3 duel(s), 3 deal(s), mean result 10.2 P, rival moved 18.0 P per duel · hardener (moved away): 2 duel(s), 2 deal(s), mean result 3.9 P, rival moved -7.5 P per duel · silent: 1 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 6049 vs Rival Oro (buyer): 22.6 P in 2 round(s). Worst: 5817 vs Rival Sol (buyer): no_deal.

**Session so far:** 46 deals / 54 finished (85%)
- Rival engaged: spoke in 50 → 45 deals (90%); spoke or accepted 51 → 46 (90%); silent 4 (1 took our opener, 3 no deal).
- In-limit offers not accepted: 3 — 5618 (buyer, limit 50, vs Rival Azul): ≈3.1 P left on the table; 5622 (seller, limit 83, vs Rival Plata): ≈19.5 P left on the table; 5813 (buyer, limit 97, vs Rival Oro): ≈5.0 P left on the table.
- Deals below an earlier in-limit rival offer: 18 (≈151.6 P: 5623, 5653, 5663, 5737, 5797, 5808, 5827, 5892, 5969, 6022, 6023, 6041, 6049, 6094, 6095, 6170, 6171, 6184).
- Rounds and decay: 3.7 rounds per deal; result 1005.3 of 1264.0 P surplus → 258.7 P (20%) lost to decay.
- Latency: answered rival offers in 1.1 ticks on average (max 11; 143 of 244 the same tick); decision 7.8 s mean, 20.0 s max; 1 rival offer(s) never answered.
- Concessions: we moved 1115 P in total, rivals 1052 P.
- Rival behaviours (best → worst by our mean result): accept-only (took our opener): 1 duel(s), 1 deal(s), mean result 23.2 P · conceder: 44 duel(s), 40 deal(s), mean result 20.3 P, rival moved 25.3 P per duel · hardener (moved away): 3 duel(s), 3 deal(s), mean result 15.9 P, rival moved -20.3 P per duel · holder (never moved): 3 duel(s), 2 deal(s), mean result 13.2 P, rival moved 0.0 P per duel · silent: 3 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 5652 vs Rival Verde (seller): 52.9 P in 2 round(s). Worst: 5622 vs Rival Plata (seller): no_deal, 19.5 P in-limit left, both still 4 ticks.

**For Aleks:**
1. Accept earlier: 3 deal(s) lost with the rival's offer inside our limit (5618, 5622, 5813; ≈27.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
2. Break holds: 3 no-deal duel(s) sat still up to 5 ticks with time left (5618, 5622, 5813). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
3. Close in fewer exchanges: 258.7 P (20%) of deal value went to decay over 3.7 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).

## Sat 22:11 · Duels II · tick 1348 · wave of 6 (duels 5899, 5947, 6037, 6040, 6041, 6048)

**This wave:** 5 deals / 6 finished (83%)
- Rival engaged: spoke in 5 → 5 deals (100%); spoke or accepted 5 → 5 (100%); silent 1 (0 took our opener, 1 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 1 (≈11.6 P: 6041).
- Rounds and decay: 3.2 rounds per deal; result 129.8 of 175.0 P surplus → 45.2 P (26%) lost to decay.
- Latency: answered rival offers in 0.8 ticks on average (max 6; 10 of 16 the same tick); decision 4.8 s mean, 11.2 s max.
- Concessions: we moved 109 P in total, rivals 98 P.
- Rival behaviours (best → worst by our mean result): conceder: 5 duel(s), 5 deal(s), mean result 26.0 P, rival moved 19.6 P per duel · silent: 1 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 6040 vs Rival Azul (seller): 36.6 P in 3 round(s). Worst: 5899 vs Rival Plata (buyer): no_deal.

**Session so far:** 41 deals / 48 finished (85%)
- Rival engaged: spoke in 45 → 40 deals (89%); spoke or accepted 46 → 41 (89%); silent 3 (1 took our opener, 2 no deal).
- In-limit offers not accepted: 3 — 5618 (buyer, limit 50, vs Rival Azul): ≈3.1 P left on the table; 5622 (seller, limit 83, vs Rival Plata): ≈19.5 P left on the table; 5813 (buyer, limit 97, vs Rival Oro): ≈5.0 P left on the table.
- Deals below an earlier in-limit rival offer: 14 (≈101.5 P: 5623, 5653, 5663, 5737, 5797, 5808, 5827, 5892, 5969, 6022, 6023, 6041, 6094, 6170).
- Rounds and decay: 3.5 rounds per deal; result 966.8 of 1185.0 P surplus → 218.2 P (18%) lost to decay.
- Latency: answered rival offers in 1.2 ticks on average (max 11; 117 of 199 the same tick); decision 7.8 s mean, 20.0 s max; 1 rival offer(s) never answered.
- Concessions: we moved 961 P in total, rivals 1013 P.
- Rival behaviours (best → worst by our mean result): hardener (moved away): 1 duel(s), 1 deal(s), mean result 40.0 P, rival moved -46.0 P per duel · accept-only (took our opener): 1 duel(s), 1 deal(s), mean result 23.2 P · conceder: 41 duel(s), 37 deal(s), mean result 21.1 P, rival moved 25.8 P per duel · holder (never moved): 3 duel(s), 2 deal(s), mean result 13.2 P, rival moved 0.0 P per duel · silent: 2 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 5652 vs Rival Verde (seller): 52.9 P in 2 round(s). Worst: 5622 vs Rival Plata (seller): no_deal, 19.5 P in-limit left, both still 4 ticks.

**For Aleks:**
1. Accept earlier: 3 deal(s) lost with the rival's offer inside our limit (5618, 5622, 5813; ≈27.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
2. Break holds: 3 no-deal duel(s) sat still up to 5 ticks with time left (5618, 5622, 5813). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
3. Close in fewer exchanges: 218.2 P (18%) of deal value went to decay over 3.5 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).

## Sat 22:05 · Duels II · tick 1335 · wave of 6 (duels 5816, 5892, 5893, 5964, 5965, 6023)

**This wave:** 5 deals / 6 finished (83%)
- Rival engaged: spoke in 5 → 5 deals (100%); spoke or accepted 5 → 5 (100%); silent 1 (0 took our opener, 1 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 2 (≈7.4 P: 5892, 6023).
- Rounds and decay: 3.4 rounds per deal; result 111.1 of 144.0 P surplus → 32.9 P (23%) lost to decay.
- Latency: answered rival offers in 0.5 ticks on average (max 4; 11 of 16 the same tick); decision 6.7 s mean, 13.4 s max.
- Concessions: we moved 126 P in total, rivals 103 P.
- Rival behaviours (best → worst by our mean result): conceder: 5 duel(s), 5 deal(s), mean result 22.2 P, rival moved 20.6 P per duel · silent: 1 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 5965 vs Rival Plata (buyer): 35.9 P in 1 round(s). Worst: 5816 vs Rival Luna (seller): no_deal.

**Session so far:** 36 deals / 42 finished (86%)
- Rival engaged: spoke in 40 → 35 deals (88%); spoke or accepted 41 → 36 (88%); silent 2 (1 took our opener, 1 no deal).
- In-limit offers not accepted: 3 — 5618 (buyer, limit 50, vs Rival Azul): ≈3.1 P left on the table; 5622 (seller, limit 83, vs Rival Plata): ≈19.5 P left on the table; 5813 (buyer, limit 97, vs Rival Oro): ≈5.0 P left on the table.
- Deals below an earlier in-limit rival offer: 13 (≈89.9 P: 5623, 5653, 5663, 5737, 5797, 5808, 5827, 5892, 5969, 6022, 6023, 6094, 6170).
- Rounds and decay: 3.6 rounds per deal; result 837.0 of 1010.0 P surplus → 173.0 P (17%) lost to decay.
- Latency: answered rival offers in 1.2 ticks on average (max 11; 107 of 183 the same tick); decision 8.2 s mean, 20.0 s max; 1 rival offer(s) never answered.
- Concessions: we moved 852 P in total, rivals 915 P.
- Rival behaviours (best → worst by our mean result): hardener (moved away): 1 duel(s), 1 deal(s), mean result 40.0 P, rival moved -46.0 P per duel · accept-only (took our opener): 1 duel(s), 1 deal(s), mean result 23.2 P · conceder: 36 duel(s), 32 deal(s), mean result 20.4 P, rival moved 26.7 P per duel · holder (never moved): 3 duel(s), 2 deal(s), mean result 13.2 P, rival moved 0.0 P per duel · silent: 1 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 5652 vs Rival Verde (seller): 52.9 P in 2 round(s). Worst: 5622 vs Rival Plata (seller): no_deal, 19.5 P in-limit left, both still 4 ticks.

**For Aleks:**
1. Accept earlier: 3 deal(s) lost with the rival's offer inside our limit (5618, 5622, 5813; ≈27.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
2. Break holds: 3 no-deal duel(s) sat still up to 5 ticks with time left (5618, 5622, 5813). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
3. Close in fewer exchanges: 173.0 P (17%) of deal value went to decay over 3.6 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).

## Sat 21:58 · Duels II · tick 1321 · wave of 6 (duels 5823, 5898, 5946, 5969, 6022, 6036)

**This wave:** 6 deals / 6 finished (100%)
- Rival engaged: spoke in 5 → 5 deals (100%); spoke or accepted 6 → 6 (100%); silent 1 (1 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 2 (≈14.3 P: 5969, 6022).
- Rounds and decay: 3.0 rounds per deal; result 147.9 of 163.0 P surplus → 15.1 P (9%) lost to decay.
- Latency: answered rival offers in 1.3 ticks on average (max 11; 12 of 18 the same tick); decision 6.9 s mean, 12.1 s max.
- Concessions: we moved 128 P in total, rivals 160 P.
- Rival behaviours (best → worst by our mean result): conceder: 5 duel(s), 5 deal(s), mean result 24.9 P, rival moved 32.0 P per duel · accept-only (took our opener): 1 duel(s), 1 deal(s), mean result 23.2 P.
- Best duel: 6036 vs Rival Sol (seller): 51.1 P in 4 round(s). Worst: 5823 vs Rival Sol (buyer): deal, both still 3 ticks.

**Session so far:** 31 deals / 36 finished (86%)
- Rival engaged: spoke in 35 → 30 deals (86%); spoke or accepted 36 → 31 (86%); silent 1 (1 took our opener, 0 no deal).
- In-limit offers not accepted: 3 — 5618 (buyer, limit 50, vs Rival Azul): ≈3.1 P left on the table; 5622 (seller, limit 83, vs Rival Plata): ≈19.5 P left on the table; 5813 (buyer, limit 97, vs Rival Oro): ≈5.0 P left on the table.
- Deals below an earlier in-limit rival offer: 11 (≈82.5 P: 5623, 5653, 5663, 5737, 5797, 5808, 5827, 5969, 6022, 6094, 6170).
- Rounds and decay: 3.6 rounds per deal; result 725.9 of 866.0 P surplus → 140.1 P (16%) lost to decay.
- Latency: answered rival offers in 1.2 ticks on average (max 11; 96 of 167 the same tick); decision 8.4 s mean, 20.0 s max; 1 rival offer(s) never answered.
- Concessions: we moved 726 P in total, rivals 812 P.
- Rival behaviours (best → worst by our mean result): hardener (moved away): 1 duel(s), 1 deal(s), mean result 40.0 P, rival moved -46.0 P per duel · accept-only (took our opener): 1 duel(s), 1 deal(s), mean result 23.2 P · conceder: 31 duel(s), 27 deal(s), mean result 20.1 P, rival moved 27.7 P per duel · holder (never moved): 3 duel(s), 2 deal(s), mean result 13.2 P, rival moved 0.0 P per duel.
- Best duel: 5652 vs Rival Verde (seller): 52.9 P in 2 round(s). Worst: 5622 vs Rival Plata (seller): no_deal, 19.5 P in-limit left, both still 4 ticks.

**For Aleks:**
1. Accept earlier: 3 deal(s) lost with the rival's offer inside our limit (5618, 5622, 5813; ≈27.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
2. Break holds: 3 no-deal duel(s) sat still up to 5 ticks with time left (5618, 5622, 5813). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
3. Close in fewer exchanges: 140.1 P (16%) of deal value went to decay over 3.6 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).

## Sat 21:52 · Duels II · tick 1309 · wave of 6 (duels 5800, 5801, 5813, 5822, 5861, 6170)

**This wave:** 5 deals / 6 finished (83%)
- Rival engaged: spoke in 6 → 5 deals (83%); spoke or accepted 6 → 5 (83%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 1 — 5813 (buyer, limit 97, vs Rival Oro): ≈5.0 P left on the table.
- Deals below an earlier in-limit rival offer: 1 (≈0.6 P: 6170).
- Rounds and decay: 5.4 rounds per deal; result 87.1 of 104.0 P surplus → 16.9 P (16%) lost to decay.
- Latency: answered rival offers in 0.6 ticks on average (max 6; 28 of 43 the same tick); decision 8.5 s mean, 13.3 s max.
- Concessions: we moved 162 P in total, rivals 184 P.
- Rival behaviours (best → worst by our mean result): conceder: 6 duel(s), 5 deal(s), mean result 14.5 P, rival moved 30.7 P per duel.
- Best duel: 5822 vs Rival Rojo (seller): 33.0 P in 2 round(s). Worst: 5813 vs Rival Oro (buyer): no_deal, 5.0 P in-limit left, both still 5 ticks.

**Session so far:** 25 deals / 30 finished (83%)
- Rival engaged: spoke in 30 → 25 deals (83%); spoke or accepted 30 → 25 (83%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 3 — 5618 (buyer, limit 50, vs Rival Azul): ≈3.1 P left on the table; 5622 (seller, limit 83, vs Rival Plata): ≈19.5 P left on the table; 5813 (buyer, limit 97, vs Rival Oro): ≈5.0 P left on the table.
- Deals below an earlier in-limit rival offer: 9 (≈68.1 P: 5623, 5653, 5663, 5737, 5797, 5808, 5827, 6094, 6170).
- Rounds and decay: 3.7 rounds per deal; result 578.0 of 703.0 P surplus → 125.0 P (18%) lost to decay.
- Latency: answered rival offers in 1.2 ticks on average (max 11; 84 of 149 the same tick); decision 8.6 s mean, 20.0 s max; 1 rival offer(s) never answered.
- Concessions: we moved 598 P in total, rivals 652 P.
- Rival behaviours (best → worst by our mean result): hardener (moved away): 1 duel(s), 1 deal(s), mean result 40.0 P, rival moved -46.0 P per duel · conceder: 26 duel(s), 22 deal(s), mean result 19.2 P, rival moved 26.8 P per duel · holder (never moved): 3 duel(s), 2 deal(s), mean result 13.2 P, rival moved 0.0 P per duel.
- Best duel: 5652 vs Rival Verde (seller): 52.9 P in 2 round(s). Worst: 5622 vs Rival Plata (seller): no_deal, 19.5 P in-limit left, both still 4 ticks.

**For Aleks:**
1. Accept earlier: 3 deal(s) lost with the rival's offer inside our limit (5618, 5622, 5813; ≈27.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
2. Break holds: 3 no-deal duel(s) sat still up to 5 ticks with time left (5618, 5622, 5813). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
3. Close in fewer exchanges: 125.0 P (18%) of deal value went to decay over 3.7 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).

## Sat 21:44 · Duels II · tick 1294 · wave of 6 (duels 5812, 5826, 5827, 5860, 5968, 6094)

**This wave:** 6 deals / 6 finished (100%)
- Rival engaged: spoke in 6 → 6 deals (100%); spoke or accepted 6 → 6 (100%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 2 (≈24.3 P: 5827, 6094).
- Rounds and decay: 3.5 rounds per deal; result 171.7 of 189.0 P surplus → 17.3 P (9%) lost to decay.
- Latency: answered rival offers in 2.2 ticks on average (max 11; 18 of 37 the same tick); decision 9.5 s mean, 20.0 s max.
- Concessions: we moved 87 P in total, rivals 91 P.
- Rival behaviours (best → worst by our mean result): hardener (moved away): 1 duel(s), 1 deal(s), mean result 40.0 P, rival moved -46.0 P per duel · conceder: 5 duel(s), 5 deal(s), mean result 26.3 P, rival moved 27.4 P per duel.
- Best duel: 5826 vs Rival Sol (seller): 40.0 P in 4 round(s). Worst: 5812 vs Rival Rojo (seller): deal, both still 3 ticks.

**Session so far:** 20 deals / 24 finished (83%)
- Rival engaged: spoke in 24 → 20 deals (83%); spoke or accepted 24 → 20 (83%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 2 — 5618 (buyer, limit 50, vs Rival Azul): ≈3.1 P left on the table; 5622 (seller, limit 83, vs Rival Plata): ≈19.5 P left on the table.
- Deals below an earlier in-limit rival offer: 8 (≈67.6 P: 5623, 5653, 5663, 5737, 5797, 5808, 5827, 6094).
- Rounds and decay: 3.3 rounds per deal; result 490.9 of 599.0 P surplus → 108.1 P (18%) lost to decay.
- Latency: answered rival offers in 1.5 ticks on average (max 11; 56 of 106 the same tick); decision 8.6 s mean, 20.0 s max; 1 rival offer(s) never answered.
- Concessions: we moved 436 P in total, rivals 468 P.
- Rival behaviours (best → worst by our mean result): hardener (moved away): 1 duel(s), 1 deal(s), mean result 40.0 P, rival moved -46.0 P per duel · conceder: 20 duel(s), 17 deal(s), mean result 20.6 P, rival moved 25.7 P per duel · holder (never moved): 3 duel(s), 2 deal(s), mean result 13.2 P, rival moved 0.0 P per duel.
- Best duel: 5652 vs Rival Verde (seller): 52.9 P in 2 round(s). Worst: 5622 vs Rival Plata (seller): no_deal, 19.5 P in-limit left, both still 4 ticks.

**For Aleks:**
1. Accept earlier: 2 deal(s) lost with the rival's offer inside our limit (5618, 5622; ≈22.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
2. Break holds: 2 no-deal duel(s) sat still up to 4 ticks with time left (5618, 5622). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
3. Close in fewer exchanges: 108.1 P (18%) of deal value went to decay over 3.3 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).

## Sat 21:39 · Duels II · tick 1283 · wave of 6 (duels 5653, 5707, 5796, 5797, 5808, 5809)

**This wave:** 6 deals / 6 finished (100%)
- Rival engaged: spoke in 6 → 6 deals (100%); spoke or accepted 6 → 6 (100%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 3 (≈21.2 P: 5653, 5797, 5808).
- Rounds and decay: 3.5 rounds per deal; result 133.7 of 200.0 P surplus → 66.3 P (33%) lost to decay.
- Latency: answered rival offers in 1.0 ticks on average (max 7; 16 of 29 the same tick); decision 8.5 s mean, 14.2 s max.
- Concessions: we moved 90 P in total, rivals 140 P.
- Rival behaviours (best → worst by our mean result): conceder: 6 duel(s), 6 deal(s), mean result 22.3 P, rival moved 23.3 P per duel.
- Best duel: 5796 vs Rival Luna (seller): 40.6 P in 2 round(s). Worst: 5707 vs Rival Azul (seller): deal, both still 5 ticks.

**Session so far:** 14 deals / 18 finished (78%)
- Rival engaged: spoke in 18 → 14 deals (78%); spoke or accepted 18 → 14 (78%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 2 — 5618 (buyer, limit 50, vs Rival Azul): ≈3.1 P left on the table; 5622 (seller, limit 83, vs Rival Plata): ≈19.5 P left on the table.
- Deals below an earlier in-limit rival offer: 6 (≈43.3 P: 5623, 5653, 5663, 5737, 5797, 5808).
- Rounds and decay: 3.2 rounds per deal; result 319.2 of 410.0 P surplus → 90.8 P (22%) lost to decay.
- Latency: answered rival offers in 1.1 ticks on average (max 9; 38 of 69 the same tick); decision 8.3 s mean, 14.5 s max; 1 rival offer(s) never answered.
- Concessions: we moved 349 P in total, rivals 377 P.
- Rival behaviours (best → worst by our mean result): conceder: 15 duel(s), 12 deal(s), mean result 18.6 P, rival moved 25.1 P per duel · holder (never moved): 3 duel(s), 2 deal(s), mean result 13.2 P, rival moved 0.0 P per duel.
- Best duel: 5652 vs Rival Verde (seller): 52.9 P in 2 round(s). Worst: 5622 vs Rival Plata (seller): no_deal, 19.5 P in-limit left, both still 4 ticks.

**For Aleks:**
1. Accept earlier: 2 deal(s) lost with the rival's offer inside our limit (5618, 5622; ≈22.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
2. Break holds: 2 no-deal duel(s) sat still up to 4 ticks with time left (5618, 5622). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
3. Close in fewer exchanges: 90.8 P (22%) of deal value went to decay over 3.2 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).

## Sat 21:32 · Duels II · tick 1270 · wave of 6 (duels 5652, 5662, 5663, 5706, 5736, 5737)

**This wave:** 6 deals / 6 finished (100%)
- Rival engaged: spoke in 6 → 6 deals (100%); spoke or accepted 6 → 6 (100%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 2 (≈8.6 P: 5663, 5737).
- Rounds and decay: 3.2 rounds per deal; result 149.8 of 152.0 P surplus → 2.2 P (1%) lost to decay.
- Latency: answered rival offers in 1.6 ticks on average (max 9; 10 of 21 the same tick); decision 7.8 s mean, 13.6 s max.
- Concessions: we moved 86 P in total, rivals 120 P.
- Rival behaviours (best → worst by our mean result): conceder: 5 duel(s), 5 deal(s), mean result 28.7 P, rival moved 24.0 P per duel · holder (never moved): 1 duel(s), 1 deal(s), mean result 6.4 P, rival moved 0.0 P per duel.
- Best duel: 5652 vs Rival Verde (seller): 52.9 P in 2 round(s). Worst: 5663 vs Rival Verde (buyer): deal, both still 5 ticks.

**Session so far:** 8 deals / 12 finished (67%)
- Rival engaged: spoke in 12 → 8 deals (67%); spoke or accepted 12 → 8 (67%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 2 — 5618 (buyer, limit 50, vs Rival Azul): ≈3.1 P left on the table; 5622 (seller, limit 83, vs Rival Plata): ≈19.5 P left on the table.
- Deals below an earlier in-limit rival offer: 3 (≈22.1 P: 5623, 5663, 5737).
- Rounds and decay: 3.0 rounds per deal; result 185.5 of 210.0 P surplus → 24.5 P (12%) lost to decay.
- Latency: answered rival offers in 1.2 ticks on average (max 9; 22 of 40 the same tick); decision 8.3 s mean, 14.5 s max; 1 rival offer(s) never answered.
- Concessions: we moved 259 P in total, rivals 237 P.
- Rival behaviours (best → worst by our mean result): conceder: 9 duel(s), 6 deal(s), mean result 16.2 P, rival moved 26.3 P per duel · holder (never moved): 3 duel(s), 2 deal(s), mean result 13.2 P, rival moved 0.0 P per duel.
- Best duel: 5652 vs Rival Verde (seller): 52.9 P in 2 round(s). Worst: 5622 vs Rival Plata (seller): no_deal, 19.5 P in-limit left, both still 4 ticks.

**For Aleks:**
1. Accept earlier: 2 deal(s) lost with the rival's offer inside our limit (5618, 5622; ≈22.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
2. Break holds: 2 no-deal duel(s) sat still up to 4 ticks with time left (5618, 5622). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
3. Close in fewer exchanges: 24.5 P (12%) of deal value went to decay over 3.0 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).

## Sat 21:25 · Duels II · tick 1255 · wave of 6 (duels 5616, 5617, 5618, 5619, 5622, 5623)

**This wave:** 2 deals / 6 finished (33%)
- Rival engaged: spoke in 6 → 2 deals (33%); spoke or accepted 6 → 2 (33%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 2 — 5618 (buyer, limit 50, vs Rival Azul): ≈3.1 P left on the table; 5622 (seller, limit 83, vs Rival Plata): ≈19.5 P left on the table.
- Deals below an earlier in-limit rival offer: 1 (≈13.5 P: 5623).
- Rounds and decay: 2.5 rounds per deal; result 35.7 of 58.0 P surplus → 22.3 P (38%) lost to decay.
- Latency: answered rival offers in 0.8 ticks on average (max 5; 12 of 19 the same tick); decision 8.8 s mean, 14.5 s max; 1 rival offer(s) never answered.
- Concessions: we moved 173 P in total, rivals 117 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 2 duel(s), 1 deal(s), mean result 16.6 P, rival moved 0.0 P per duel · conceder: 4 duel(s), 1 deal(s), mean result 0.7 P, rival moved 29.2 P per duel.
- Best duel: 5616 vs Rival Verde (seller): 33.1 P in 1 round(s). Worst: 5622 vs Rival Plata (seller): no_deal, 19.5 P in-limit left, both still 4 ticks.

**Session so far:** 2 deals / 6 finished (33%)
- Rival engaged: spoke in 6 → 2 deals (33%); spoke or accepted 6 → 2 (33%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 2 — 5618 (buyer, limit 50, vs Rival Azul): ≈3.1 P left on the table; 5622 (seller, limit 83, vs Rival Plata): ≈19.5 P left on the table.
- Deals below an earlier in-limit rival offer: 1 (≈13.5 P: 5623).
- Rounds and decay: 2.5 rounds per deal; result 35.7 of 58.0 P surplus → 22.3 P (38%) lost to decay.
- Latency: answered rival offers in 0.8 ticks on average (max 5; 12 of 19 the same tick); decision 8.8 s mean, 14.5 s max; 1 rival offer(s) never answered.
- Concessions: we moved 173 P in total, rivals 117 P.
- Rival behaviours (best → worst by our mean result): holder (never moved): 2 duel(s), 1 deal(s), mean result 16.6 P, rival moved 0.0 P per duel · conceder: 4 duel(s), 1 deal(s), mean result 0.7 P, rival moved 29.2 P per duel.
- Best duel: 5616 vs Rival Verde (seller): 33.1 P in 1 round(s). Worst: 5622 vs Rival Plata (seller): no_deal, 19.5 P in-limit left, both still 4 ticks.

**For Aleks:**
1. Accept earlier: 2 deal(s) lost with the rival's offer inside our limit (5618, 5622; ≈22.6 P after decay). In code, accept any in-limit standing offer at ticks_left ≤ 2.
2. Break holds: 2 no-deal duel(s) sat still up to 4 ticks with time left (5618, 5622). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
3. Close in fewer exchanges: 22.3 P (38%) of deal value went to decay over 2.5 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).

## Sat 13:13 · Duels I · tick 606 · wave of 1 (duels 2530)

**This wave:** 1 deals / 1 finished (100%)
- Rival engaged: spoke in 1 → 1 deals (100%); spoke or accepted 1 → 1 (100%); silent 0 (0 took our opener, 0 no deal).
- In-limit offers not accepted: 0.
- Rounds and decay: 2.0 rounds per deal; result 8.8 of 10.0 P surplus → 1.2 P (12%) lost to decay.
- Latency: answered rival offers in 0.0 ticks on average (max 0; 2 of 2 the same tick); decision 5.2 s mean, 6.9 s max.
- Concessions: we moved 24 P in total, rivals 15 P.
- Rival behaviours (best → worst by our mean result): conceder: 1 duel(s), 1 deal(s), mean result 8.8 P, rival moved 15.0 P per duel.
- Best duel: 2530 vs Rival Azul (seller): 8.8 P in 2 round(s). Worst: 2530 vs Rival Azul (seller): deal, both still 5 ticks.

**Session so far:** 30 deals / 34 finished (88%)
- Rival engaged: spoke in 29 → 28 deals (97%); spoke or accepted 31 → 30 (97%); silent 5 (2 took our opener, 3 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 4 (≈10.1 P: 2296, 2461, 2522, 2585).
- Rounds and decay: 4.4 rounds per deal; result 478.9 of 591.0 P surplus → 112.1 P (19%) lost to decay.
- Latency: answered rival offers in 0.6 ticks on average (max 5; 119 of 164 the same tick); decision 5.1 s mean, 25.0 s max; 1 rival offer(s) never answered.
- Concessions: we moved 944 P in total, rivals 655 P.
- Rival behaviours (best → worst by our mean result): hardener (moved away): 1 duel(s), 1 deal(s), mean result 60.2 P, rival moved -5.0 P per duel · accept-only (took our opener): 2 duel(s), 2 deal(s), mean result 22.5 P · holder (never moved): 8 duel(s), 7 deal(s), mean result 16.2 P, rival moved 0.0 P per duel · conceder: 20 duel(s), 20 deal(s), mean result 12.2 P, rival moved 33.0 P per duel · silent: 3 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 2585 vs Rival Rojo (buyer): 60.2 P in 1 round(s). Worst: 2367 vs Rival Oro (buyer): no_deal, both still 5 ticks.

**For Aleks:**
1. Break holds: 1 no-deal duel(s) sat still up to 5 ticks with time left (2367). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
2. Close in fewer exchanges: 112.1 P (19%) of deal value went to decay over 4.4 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).
3. Silent rivals: 3 no-deal(s) with a silent rival while 2 silent rival(s) took our opener: concede on a code schedule toward a floor (keep ≥ 30% of anchor-to-limit).

## Sat 13:12 · Duels I · tick 605 · wave of 3 (duels 2415, 2531, 2585)

**This wave:** 2 deals / 3 finished (67%)
- Rival engaged: spoke in 2 → 2 deals (100%); spoke or accepted 2 → 2 (100%); silent 1 (0 took our opener, 1 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 1 (≈3.8 P: 2585).
- Rounds and decay: 1.0 rounds per deal; result 102.5 of 109.0 P surplus → 6.5 P (6%) lost to decay.
- Latency: answered rival offers in 0.0 ticks on average (max 0; 1 of 1 the same tick); decision 2.8 s mean, 5.9 s max.
- Concessions: we moved 28 P in total, rivals -5 P.
- Rival behaviours (best → worst by our mean result): hardener (moved away): 1 duel(s), 1 deal(s), mean result 60.2 P, rival moved -5.0 P per duel · holder (never moved): 1 duel(s), 1 deal(s), mean result 42.3 P, rival moved 0.0 P per duel · silent: 1 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 2585 vs Rival Rojo (buyer): 60.2 P in 1 round(s). Worst: 2415 vs Rival Rojo (buyer): no_deal.

**Session so far:** 29 deals / 33 finished (88%)
- Rival engaged: spoke in 28 → 27 deals (96%); spoke or accepted 30 → 29 (97%); silent 5 (2 took our opener, 3 no deal).
- In-limit offers not accepted: 0.
- Deals below an earlier in-limit rival offer: 4 (≈10.1 P: 2296, 2461, 2522, 2585).
- Rounds and decay: 4.4 rounds per deal; result 470.1 of 581.0 P surplus → 110.9 P (19%) lost to decay.
- Latency: answered rival offers in 0.6 ticks on average (max 5; 117 of 162 the same tick); decision 5.2 s mean, 25.0 s max; 1 rival offer(s) never answered.
- Concessions: we moved 920 P in total, rivals 640 P.
- Rival behaviours (best → worst by our mean result): hardener (moved away): 1 duel(s), 1 deal(s), mean result 60.2 P, rival moved -5.0 P per duel · accept-only (took our opener): 2 duel(s), 2 deal(s), mean result 22.5 P · holder (never moved): 8 duel(s), 7 deal(s), mean result 16.2 P, rival moved 0.0 P per duel · conceder: 19 duel(s), 19 deal(s), mean result 12.4 P, rival moved 33.9 P per duel · silent: 3 duel(s), 0 deal(s), mean result 0.0 P.
- Best duel: 2585 vs Rival Rojo (buyer): 60.2 P in 1 round(s). Worst: 2367 vs Rival Oro (buyer): no_deal, both still 5 ticks.

**For Aleks:**
1. Break holds: 1 no-deal duel(s) sat still up to 5 ticks with time left (2367). After 3 still ticks with ≥ 3 left, force a move (a concession step, or send their own price).
2. Close in fewer exchanges: 110.9 P (19%) of deal value went to decay over 4.4 rounds per deal. Accept when the gap to our last offer ≤ max(2 P, 2d/(1−d) × our surplus).
3. Silent rivals: 3 no-deal(s) with a silent rival while 2 silent rival(s) took our opener: concede on a code schedule toward a floor (keep ≥ 30% of anchor-to-limit).

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
