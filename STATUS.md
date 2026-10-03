# Team 5 — live status

_Auto-updated by `tools/status.py` (read-only). Last update **Sat 13:23** · tick 627 (30 s/tick) · game hour 6.55 · running · today closes 23:00._

## Team: now and latest

_From `team/<name>.md`; each person writes only their own file._

**Aleks** — Duels I done for us (13:13): 30 deals of 34, 13.93 duel points, 4.4 rounds per deal. Duelist still running (since 11:27:54, eb36ec8) and idle until Duels II ≈ 18:29 (tick ≈ 1239, 68 duels, 6 at once, 8% decay, price + days). Rounds fix on branch `rounds` (da9c45c) merges by itself at tick ≥ 640; **Aleks restarts the duelist on it before Duels II**, then checks the day reading at the first days duel.
  - Sat 13:22 · **Duels I done (monitored live, no errors, no fallbacks, no restarts mid-session)**: 34 duels, **30 deals (88 %), 478.9 P** of 591 P surplus (112 P, 19 %, lost to decay); rounds per deal median 4, mean 4.4 · the split: 12 deals in ≤ 2 rounds scored 280.4 P (2585 60.2, 2584 49.8, 2531 42.3: rival took or met our number at once), 12 deals in ≥ 6 rounds kept 61 % of surplus (2461 12 rounds 20 → 9.5; 2356 10 rounds; 2460 10 rounds) · 4 no-deals: 2367 (Oro never inside our 72, lowest 83: no overlap) and **3 silent rivals** (2523 Noche, 2414 Verde, 2415 Rojo) where the code walk stopped at its 30 % floor (170/196, 71/60, 83/95) with no answer: silence costs no round, so walking on toward our limit was free; Verde accepted fast in 2447/2584, so these may be accept-only with a threshold · also: 2319 and 2494 settled on our standing number before our accept landed (both better for us) · `review` table in `docs/duels/README.md` · next: Aleks's 14:30 review → top 3 changes (candidates: silent walk to the limit; fewer, bigger steps / softer opener; days integrative per PLAN #13)
  - Sat 13:20 · **Duels I final** (34 duels) · 30 deals (88%), field 77% (220 of 286 closed) · duel points 13.93 (≈ 0.41 per duel; the jumps match each deal's share of the pie × 0.94^rounds [L]) · negotiating 15.16 → 21.12 from tick 450 to 610: +5.96, the most among the top 8 (t14 +3.86, t18 +2.59, t12 +2.51, t13 −4.43); 2nd in negotiating, 5th overall (market 7.5 is the gap) · **rounds**: 4.4 per deal, 19% of deal value lost (112 of 591 P); deals in 0-1 rounds kept 95% (mean 25.4 P), 7+ rounds kept 57% (mean 8.5 P); the new rule would have held 96 of our 171 follow-up offers · deals landed at the openers' midpoint (median 0.51; practice 0.64): tougher rivals; we conceded 944 P, they 655 · no-deals: 2367 (rival held 101 above our value 72: no overlap) and 3 silent rivals (walks to 170/196, 71/60, 83/95 never taken: likely no agent) · 4 deals below an earlier in-limit rival offer (≈10 P) · $1.62 model spend, decision 5.1 s mean, 25 s max (1 timeout) · next: restart on `rounds` before Duels II; watch the first wave for standoffs (more holds) and the day reading
  - Sat 12:52 · Duels I so far (tick 556, 23 of our duels finished, 3 live) · **21 deals of 23 (91%)**, field 80% (161/202 public results) · duel points 0 → 10.09: the jumps line up with our deals closing, each one share-sized, so points ≈ Σ our share of the pie × 0.94^rounds [L], ~0.44 per duel · **rounds are the leak**: 4.4 per deal (practice 3.5), 22% of deal value lost to decay (≈ 2.8 points); longest 2356 (10), 2318/2319 (9); our steps of 3-4 P against gaps of 50-80 (2318: 115 → 112 → 108 …) are what the Builder's `rounds` branch holds · no-deals: 2367 (rival held 101, our limit 72: likely no overlap) and 2523 (silent rival, our walk 110 → 170 never taken) · 2 fallbacks (2506 past-limit draft blocked, 2356 25 s timeout) · rivals that took our opener scored best (2446: 28 P, 0 rounds); 2296 sold at 97 after the rival had offered 101 and retreated · next: merge `rounds` after Duels I, restart before Duels II

**Dani** — Desk, still open: Q6 (do duel threads count in the 6 open conversations? Duels II runs 6 at once ≈ 18:29), venue bond cooldown length, Q7 judging, Q4 ladder "price range" (do above-list deals count?), Q3 cap flat 50 or 5×book. Answered: stale `day_closes fri` did nothing (Lucas 10:50); Round 3 + CHA re-anchored to Sun ≈ 09:29 (server, log 11:44). Room: RET holders/collectors in log 11:44; steer other teams' trades to our v10 (0% fee: one trade there took us #4 → #2 at 10:45); no sell pitches (no line in `intel/opportunities.md` is live; top 4 at tick 424: t14, t13, t18, t12, and it moves every few minutes, so check the live board). Pitch draft with Lucas during Duels I (11:59-~13:34). Dashboard on my laptop (http://127.0.0.1:8765, read-only; Duel monitor tab at `#duelmon` for Duels I/II/III) rewrites `intel/teams.md` every 10 min; it reaches GitHub when one of my Claude sessions ends a turn (`--push` is ready but off).
  - Sat 12:57 · **why we reached #3** (our `/api/me` per tick + leaderboard snapshots 450 → 570 + `intel/score-model.md`) · 22.66 #10 → **29.57 #3** (+6.91, the biggest rise in the top 8: t14 +2.71, t18 +3.32, t12 +2.55, t10 +3.86, t17 +3.18, t13 −0.03) · market flat (7.5) and `neg_points` flat (35.2): **all of it is Negotiating, 15.16 → 22.07** · since Duels I scored, Saturday Negotiating = 0.6 × (team trades + ladder) + duel part (≤ 12 Saturday points) [V, score-model 1b]; 1 Saturday point = 0.667 board · approx. split [L, score-model rates]: **(1) duels ≈ +6 board**: `duel_points` 0 → 10-11; Aleks 12:52: 21 deals of 23 (91 %) vs the field 80 %; **(2) ladder ≈ +4 board**: 4 dealer sells at no `neg_points` cost, `ladder_points` 0.055 → 0.181: LAT-08 → Chato (tick 481), MAL-07, SAL-08, MAL-06 → Pilar (508, 522, 551; Pilar is level 3, higher levels weigh more); the 11:35 ladder program copied what Team 13 did (deals at list, then Pilar); **(3) the 40 % re-weighting ≈ −3.4 board** for us, but it hurt more the teams whose Saturday came from trades: t13 (Saturday Negotiating 21.6, the highest, weak duels) 27.72 → 27.69 and #2 → #7; t02 (21.3) out of the top 8; ours was 12.75 (#8), so the cut cost us little · the jump to #3 at snapshot 560: MAL-06 → Pilar (+0.040 ladder, tick 551) + `duel_points` 8.23 → 10.09 (ticks 552-553) · fragile: Duels I runs to ≈ 13:35 and the duel part looks graded against the field [L] (snapshot 520: −0.8 with no event of ours) · pitch material: duelist 91 % deals; ladder program learned from a rival's measured path · next: watch Duels I on the Duel monitor tab, desk Q6
  - Sat 12:12 · **dashboard: new "Duel monitor" tab** (http://127.0.0.1:8765/#duelmon), the current duel session live, read-only, from data the dashboard already reads (**no extra request**: the duelist shares the team's 5 rps) · session + field progress from the feed (`duels.scheduled`, `duel.closed`), our duels from `/api/duels`, `duel_points` from `/api/me` · tiles: our duels done/total + ETA, deals, result after decay and **P lost to rounds**, `duel_points` sparkline, P left on the table, field deal rate · alerts: CRITICAL (rival's standing offer inside our limit with ≤ 2 ticks left; our offer outside our limit; we silent ≥ 4 ticks after a rival price near the deadline), WATCH (acceptable now: +X P after decay), MISSED · live table (our offer vs theirs vs limit, gap, rounds, pie left, ticks left, accept-now value; days for Duels II) · finished table · negotiating Δ per team since the session began (board doesn't split duels out) · complements Lucas's `duelmon` (phone alerts + per-wave review), doesn't replace it · restarted 12:10 on this code, 0 errors, hub on · **Duels I at tick 483:** 4/34 done, 4 deals, 36.7 P of 50 P surplus (**13.3 P, 27 %, lost to rounds**; duel 2540: 7 rounds, 6.7 of 19 lost), field 36/39 deals · seen live: duel 2506 (buyer, limit 103): rival dropped to 96 at tick 480 and we sent 98 the same tick (step computed on their previous 104); it closed at 96 anyway (4.8 P, 6 rounds), so no cost; for Aleks's rounds spec: a same-tick drop can cross our next step · next: watch Duels I on the tab, desk Q6
  - Sat 11:44 · Chief 09:55 #2-#4 re-checked, public feed to tick 424 · **#2 dashboard ETAs:** already fixed at 09:48 (`minutes_per_hour()`, `dashboard/server.py:731`); live now: Market Test 5.0 in 10 min (≈ 11:50), Duels I 5.15 in 19 min (≈ 11:59), as the Chief says; no restart needed · **#3b answered:** the stale `day_closes fri` did nothing (Lucas 10:50); `/api/schedule` now lists `day_closes sat` and `day_opens sun`, both at 16.158 [V] · **#3c answered by the server [V]:** Sat close 16.158 = 23:00 = Sun open 09:00, so Round 3 + CHA release at 16.65 ≈ **Sun 09:29**; Sunday allowance 16.7 ≈ 09:32; benches 17/19/21 ≈ 09:50/11:50/13:50; Duels III 18.65 ≈ 11:29; finale warning 21.45 ≈ 14:17; stalls close + Grand Final 21.65 ≈ 14:29; close 22.158 = 15:00; scores freeze 22.65 ≈ 15:29 (game hour = wall hour on Sunday too: 16.158 → 22.158 is 09:00 → 15:00); corrects my 10:16 "first Sunday bench ≈ 09:21" · **#3a/d/e still need the desk** (RULES.md:84 only says the bond comes back "after a cooldown") · **#4 El Retiro, facts:** **RET rare holders:** RET-09: t18 (tick 206), us (208), t15 (334); RET-10: t18 (213), us (232); all five came from El Chato and none has changed hands since · RET-11 (epic) and RET-12 (legendary): no team has one in the feed · no pack opened since RET's release (tick 160) shows a RET rare or better (the feed names each pack's best card), and the settlement numbers missing from the feed line up with pack buys and the tick-165 grant [L: the holder list is complete] · **who collects RET now:** t14 (#1, top 4) bought 6 RET commons/uncommons (ticks 332-411: RET-01/02/04/06/07/08), no rare bid yet; t13 (#2, top 4) bids RET-01..08 (to tick 415) and opened 22 dealer threads for RET-06 (ticks 239-415), no rare bid; t02 (#6) has bid for RET-10 every 10 ticks since tick 161 (live on El Rastro, tick 421) and flips RET uncommons; t06 (#14) live bid for RET-09 on v07 (tick 402); t09 (#12) bought RET-06/07 (ticks 400-406), bid RET-02..07/09/10 (tick 378); t15 (#15) holds RET-09, bought RET-06/08 (ticks 373-389); t04 (#8) buys RET from Abuela and relists them (asks RET-03/04/05/07/08, ticks 401-404) · **quiet:** t12 (#4, holds RET-01..08, lacks only the rares) since tick 217; t18 (#3, holds RET-09/10 + 8 commons/uncommons, no RET-07 seen) since tick 230 · the Chief's "Teams 2 and 12" race is now t14 and t13, both top 4 · **top 4 at tick 424: t14, t13, t18, t12** (we #9, 22.66); the Chief's list (t04, t12, t13, t17) and `opportunities.md` 11:38 (t10, t12, t13, t18) are stale · **sales:** no line in `intel/opportunities.md` is live (11:38); our RET-09/10 are page cards, not spares · next: desk (Q6, bond cooldown, Q7, Q4, Q3), pitch with Lucas in Duels I

**Lucas** — Saturday: follow `intel/saturday-plan.md` (verified Fri night by 10 analyses, 4 verifiers, a pre-mortem and a fact-check). Four sessions on Lucas's machine (`intel/saturday-sessions.md`): **Chief of staff** (the only one Lucas talks to), **Operator** (the only game writer for trades and dealers), **Builder** (tools), **Market** (recorder, broker, venue). Morning steps: `intel/morning-start.md`. Trader and analysts are stopped until the operator's 09:00 checks.
  - Sat 13:28 · Builder · dealer 'hang' root cause: dealer offers expire after 4 ticks; with his/her offer expired and us holding at cap, the loop spun silently on `if not hers` (no log, no stuck count, watchdog re-armed) · fix e875b82: log no_live_offer each tick, walk at 4 (not after accept; abuela only when her word is last), 345 pass · Operator told
  - Sat 13:21 · operator · Duels I over (~13.9 duel points); trader running · **5 asks on Team 15's stall v15** (pilot, Chief 13:10), addressed to high-multiplier collectors per intel/multipliers.json: 8867 LAV-02 → t09 8, 8868 LAV-04 → t03 8, 8869 SAL-02 → t16 7, 8871 LAT-04 → t16 6, 8919 LAV-03 → t04 8 (t06 blocked: dumps LAV); in run/book.json with venue v15 · Abuela SAL-06 at ≤ 22: her 29 → 27 → 25, held 25 → skipped (Chief's rule); chato_steady hung twice (old code and HEAD 2559725, watchdog dump empty) → repro sent to the Builder · lunch GUARDRAIL 13:15 (one bargain ≤ 100, gain ≥ 50, seller outside the top 5, cash ≥ 60): watching logs/bargains.log hits · cash 184, ladder 0.181
  - Sat 13:13 · Builder · chato_steady hang (thread 805, 4+ min silent at cap, server fine): bounded wait_tick, 8 s timeout, slow-call log, stack watchdog → logs/dealers/hang-<pid>.txt, wall-time stuck walk (2559725, 343 pass); cause not pinned (no stack) · Operator reruns on HEAD; CHA plan re-verify running

## Score

| Total | Rank | Negotiating | Market | Duel pts | Ladder pts | Bench eff. | Deals | Level | Cash | Album |
|---|---|---|---|---|---|---|---|---|---|---|
| 28.60 | 5 | 21.10 | 7.50 | 13.93 | 0.18 | 0.93 | 39 | 3 | 184 | 29/50 |

Leaderboard (snapshot at tick 620; refreshes every few minutes):

| # | Team | Score | Negotiating | Market | Deals |
|---|---|---|---|---|---|
| 1 | Team 14 | 30.77 | 21.05 | 9.72 | 29 |
| 2 | Team 12 | 29.61 | 17.11 | 12.50 | 39 |
| 3 | Team 18 | 29.23 | 21.73 | 7.50 | 29 |
| 4 | Team 10 | 29.19 | 17.12 | 12.07 | 30 |
| 5 | Team 5 | 28.60 | 21.10 | 7.50 | 39 |

## Next on the schedule

_ETA assumes no pause (a tick advances tick_seconds of game time, so a game hour is a wall hour at any pace)._

| Game hour | ETA | Action | Note |
|---|---|---|---|
| 7.00 | ~27 min | bench | The Market Test: every venue gets the same synthetic book |
| 9.00 | ~147 min | bench | The Market Test: every venue gets the same synthetic book |
| 9.15 | ~156 min | persona_patch | Salamanca fever: Doña Pilar pays 25 % over book for Salamanca until 17:30 |
| 11.00 | ~267 min | bench | The Market Test: every venue gets the same synthetic book |
| 11.15 | ~276 min | persona_patch | The fever breaks |
| 11.65 | ~306 min | duels | Duels II: price and delivery day; the pie grows for teams that trade on what each side cares about |
| 13.00 | ~387 min | bench | The Market Test: every venue gets the same synthetic book |
| 14.65 | ~486 min | bench | The hard Market Test: firmer and more impatient traders |

## Our dealer deals

_Her first = her first price in the conversation. A deal at her first price probably doesn't count as negotiated._

| Thread | Dealer | Side | Item | Her first | Our first | Deal | vs her first | Msgs | Status | Closed |
|---|---|---|---|---|---|---|---|---|---|---|
| 10 | abuela | buy | sobre_barrio | 17 | — | 17 | +0% | 1 | deal |  |
| 29 | abuela | buy | sobre_barrio | 30 | 16 | 22 | -27% | 7 | deal |  |
| 36 | abuela | buy | sobre_barrio | 30 | 16 | 22 | -27% | 9 | deal |  |
| 40 | abuela | buy | LAV-05 | 12 | 7 | 9 | -25% | 5 | deal |  |
| 45 | abuela | buy | LAV-02 | 12 | 7 | 9 | -25% | 7 | deal |  |
| 82 | abuela | buy | LAV-08 | 29 | 16 | 24 | -17% | 11 | deal |  |
| 95 | abuela | buy | LAV-07 | 29 | 16 | — | — | 2 | closed |  |
| 97 | abuela | sell | 1 card(s) | 5 | 9 | 6 | +20% | 9 | deal |  |
| 104 | abuela | sell | 1 card(s) | 5 | 9 | 6 | +20% | 7 | deal |  |
| 114 | abuela | sell | 1 card(s) | 5 | 9 | 5 | +0% | 9 | deal |  |
| 124 | abuela | sell | 1 card(s) | 5 | 9 | 5 | +0% | 9 | deal |  |
| 136 | abuela | sell | 1 card(s) | — | — | — | — | 0 | closed |  |
| 138 | abuela | buy | LAT-08 | 29 | 16 | — | — | 7 | closed |  |
| 145 | abuela | buy | LAT-07 | — | — | — | — | 0 | closed |  |
| 147 | abuela | buy | LAT-08 | 29 | 16 | — | — | 8 | closed |  |
| 160 | abuela | buy | MAL-07 | 29 | 16 | — | — | 4 | closed |  |
| 176 | abuela | buy | MAL-07 | 29 | — | 29 | +0% | 1 | deal |  |
| 190 | chato | buy | LAV-06 | 33 | 23 | — | — | 9 | closed |  |
| 203 | chato | buy | LAV-07 | 33 | 23 | — | — | 9 | closed |  |
| 214 | chato | sell | 1 card(s) | 13 | 21 | — | — | 3 | closed |  |
| 228 | chato | buy | LAV-06 | 33 | 23 | 31 | -6% | 13 | deal |  |
| 264 | chato | buy | LAV-07 | — | — | — | — | 0 | closed |  |
| 276 | chato | sell | 1 card(s) | 13 | 24 | 13 | +0% | 11 | deal |  |
| 288 | abuela | sell | 1 card(s) | 5 | — | 5 | +0% | 1 | deal |  |
| 289 | chato | buy | LAV-09 | 97 | 70 | 93 | -4% | 7 | deal |  |
| 353 | abuela | buy | RET-04 | 12 | 7 | 9 | -25% | 5 | deal |  |
| 359 | abuela | buy | RET-03 | 12 | 7 | 9 | -25% | 7 | deal |  |
| 367 | abuela | buy | RET-02 | 12 | 7 | — | — | 7 | closed |  |
| 373 | abuela | buy | RET-08 | 29 | 14 | — | — | 2 | closed |  |
| 384 | chato | buy | RET-09 | 97 | 57 | 87 | -10% | 11 | deal |  |
| 389 | abuela | buy | RET-02 | 12 | 7 | 9 | -25% | 7 | deal |  |
| 394 | chato | buy | RET-10 | 97 | 57 | — | — | 9 | closed |  |
| 412 | chato | buy | RET-10 | 97 | 57 | 86 | -11% | 11 | deal |  |
| 418 | chato | buy | RET-06 | 33 | 18 | — | — | 9 | closed |  |
| 425 | abuela | buy | RET-08 | 29 | 16 | 22 | -24% | 9 | deal |  |
| 430 | chato | buy | RET-06 | 33 | 20 | 30 | -9% | 11 | deal |  |
| 438 | abuela | buy | RET-07 | 29 | 16 | 23 | -21% | 11 | deal |  |
| 664 | chato | sell | 1 card(s) | 13 | 39 | — | — | 9 | closed |  |
| 682 | chato | sell | 1 card(s) | 13 | 30 | 14 | +8% | 15 | deal |  |
| 710 | pilar | sell | 1 card(s) | 16 | 30 | 19 | +19% | 11 | deal |  |
| 737 | pilar | sell | 1 card(s) | 16 | 30 | — | — | 9 | closed |  |
| 744 | pilar | sell | 1 card(s) | 22 | 34 | 23 | +5% | 9 | deal |  |
| 767 | pilar | sell | 1 card(s) | 16 | 30 | 19 | +19% | 11 | deal |  |
| 805 | chato | buy | SAL-06 | 33 | 22 | — | — | 7 | closed |  |
| 832 | abuela | buy | SAL-06 | 29 | 16 | — | — | 9 | closed |  |

## Abuela benchmark: every team's deals with her (public feed)

| Item | Side | All deals | Median | Min | Max | Ours | Our avg |
|---|---|---|---|---|---|---|---|
| common card | team buys | 63 | 9 | 7 | 12 | 5 | 9 |
| common card | team sells | 69 | 6 | 2 | 23 | 5 | 5.40 |
| sobre_barrio | team buys | 41 | 22 | 17 | 30 | 3 | 20.33 |
| uncommon card | team buys | 70 | 23.00 | 17 | 29 | 4 | 24.50 |
| uncommon card | team sells | 8 | 14.50 | 13 | 17 | 0 | — |

## Duels

Live: 0 · finished: 68

- {"duel": 2506, "session": 2, "status": "deal", "role": "buyer", "item": "Palacio de Cristal", "issues": ["price"], "your_days_weight": null, "days_meaning": null, "your_limit": 103, "limit_meaning": "never pay above your value", "rival": "Rival Noche", "deadline_tick": 482, "decay_per_round": 0.06, 
- {"duel": 2507, "session": 2, "status": "deal", "role": "seller", "item": "Palacio de Cristal", "issues": ["price"], "your_days_weight": null, "days_meaning": null, "your_limit": 100, "limit_meaning": "never sell below your cost", "rival": "Rival Rojo", "deadline_tick": 589, "decay_per_round": 0.06, 
- {"duel": 2522, "session": 2, "status": "deal", "role": "seller", "item": "Caf\u00e9 en Goya", "issues": ["price"], "your_days_weight": null, "days_meaning": null, "your_limit": 44, "limit_meaning": "never sell below your cost", "rival": "Rival Plata", "deadline_tick": 535, "decay_per_round": 0.06, "
- {"duel": 2523, "session": 2, "status": "no_deal", "role": "buyer", "item": "Caf\u00e9 en Goya", "issues": ["price"], "your_days_weight": null, "days_meaning": null, "your_limit": 196, "limit_meaning": "never pay above your value", "rival": "Rival Noche", "deadline_tick": 542, "decay_per_round": 0.06
- {"duel": 2530, "session": 2, "status": "deal", "role": "seller", "item": "Mercado de la Paz", "issues": ["price"], "your_days_weight": null, "days_meaning": null, "your_limit": 87, "limit_meaning": "never sell below your cost", "rival": "Rival Azul", "deadline_tick": 607, "decay_per_round": 0.06, "r
- {"duel": 2531, "session": 2, "status": "deal", "role": "buyer", "item": "Mercado de la Paz", "issues": ["price"], "your_days_weight": null, "days_meaning": null, "your_limit": 146, "limit_meaning": "never pay above your value", "rival": "Rival Sol", "deadline_tick": 609, "decay_per_round": 0.06, "ro
- {"duel": 2534, "session": 2, "status": "deal", "role": "seller", "item": "Caf\u00e9 en Goya", "issues": ["price"], "your_days_weight": null, "days_meaning": null, "your_limit": 129, "limit_meaning": "never sell below your cost", "rival": "Rival Sol", "deadline_tick": 558, "decay_per_round": 0.06, "r
- {"duel": 2535, "session": 2, "status": "deal", "role": "buyer", "item": "Caf\u00e9 en Goya", "issues": ["price"], "your_days_weight": null, "days_meaning": null, "your_limit": 219, "limit_meaning": "never pay above your value", "rival": "Rival Noche", "deadline_tick": 569, "decay_per_round": 0.06, "
- {"duel": 2540, "session": 2, "status": "deal", "role": "seller", "item": "El Mes\u00f3n de la Cava", "issues": ["price"], "your_days_weight": null, "days_meaning": null, "your_limit": 71, "limit_meaning": "never sell below your cost", "rival": "Rival Luna", "deadline_tick": 480, "decay_per_round": 0
- {"duel": 2541, "session": 2, "status": "deal", "role": "buyer", "item": "El Mes\u00f3n de la Cava", "issues": ["price"], "your_days_weight": null, "days_meaning": null, "your_limit": 108, "limit_meaning": "never pay above your value", "rival": "Rival Azul", "deadline_tick": 506, "decay_per_round": 0
- {"duel": 2584, "session": 2, "status": "deal", "role": "seller", "item": "Mercado de la Paz", "issues": ["price"], "your_days_weight": null, "days_meaning": null, "your_limit": 122, "limit_meaning": "never sell below your cost", "rival": "Rival Verde", "deadline_tick": 600, "decay_per_round": 0.06, 
- {"duel": 2585, "session": 2, "status": "deal", "role": "buyer", "item": "Mercado de la Paz", "issues": ["price"], "your_days_weight": null, "days_meaning": null, "your_limit": 160, "limit_meaning": "never pay above your value", "rival": "Rival Rojo", "deadline_tick": 607, "decay_per_round": 0.06, "r

## Dealers

| Dealer | Status | Level | Open to us | Sells | Buys | Deals/hour |
|---|---|---|---|---|---|---|
| abuela | active | 1 | True | sobre_barrio (26 P), common (10 P), uncommon (25 P) | common, uncommon | 8 |
| chato | active | 2 | True | sobre_plata (150 P), uncommon (26 P), rare (77 P) | uncommon, rare | 6 |
| pilar | active | 3 | True | sobre_oro (420 P) | uncommon, rare, epic, uncommon, rare, epic | 6 |

## Levels

- El Chato: None — Better packs and rare singles; he buys uncommon and rare cards. Open a thread with him (with: chato).
- Doña Pilar: None — A collector: she pays over book for the cards she loves and sells gold packs. Open a thread with her (with: pilar).
- Radio Rastro: None — News on air: GET /api/news (newest first; also news.posted on the live stream). Three sources: the Boletín del Bazar (the Bazaar bulletin), Radio Rastro and El Tablón, the notice board. Some items are true and the market moves as they say; some are rumours that never happen; some are just Madrid. Nothing tells you which is which.
