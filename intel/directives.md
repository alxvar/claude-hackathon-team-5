# Directives (Lucas's strategy session → operator, analysts, teammates)

_Written by the strategy session. It never touches the game: no trades, no bots. The operator executes inside its guardrails; anything involving a rare or >50 P still needs Lucas. Newest block on top. Labels: **[Verified]** measured on our own deals or read from the server; **[Likely]** fitted or inferred; **[Open]** unknown._

## Fri 22:47 — LAV page plan (replaces the LAV-09 bid; execute now, in order)

- 22:47 · Cancel our LAV-09 bid 2353 now and close Chato thread 276 (LAT-08). Goal: a TEAM trade completes the LAV page (~+87 `neg_points`) and Chato gives us a ladder slot on the way. Steps 1-3 below, in order.
- 22:47 · Why: the page bonus only scores when a team trade completes the page (Team 17 +~45 at tick 124 via a team; Team 10 ~0 via Chato). Make the cheap common LAV-05 the last card, not LAV-09. Bid-125 route: +52 if ever filled. This route: about +78 plus a ladder slot.
- 22:47 · Step 1: sell our only LAV-05 now, fastest route (Abuela sell thread, accept her first bid ~5; costs about −8). GATE for step 2: value?card=LAV-09 must read ~91, not 177.
- 22:47 · Step 2: Chato, buy LAV-09: open 70, +3 per tick, accept his offer or `final` at ≤93 (Team 10 got 90, Team 14 93). Costs ≤ −2 because the page is still open. Never accept while LAV-09 reads 177.
- 22:47 · Step 3: right after LAV-09 settles, buy LAV-05 from a team: accept the cheapest ask ≤15 (offer 2398 at 8 now). If none, public bid 12 (fills overnight). Check value?card=LAV-05 ≈ 99 first. Expected ≈ +89.
- 22:47 · Abort: if Chato is not at ≤93 by tick 156, close it, buy LAV-05 back at ≤10 and re-post the LAV-09 bid at 125 overnight. If a LAV-09 arrives from a team at any point, stop and skip Chato: that trade already scored.
- 22:47 · From now on never sell a LAV page card (each sale would lose the ~86 bonus). Spare copies only: the second LAV-02, LAV-03 and LAV-04.
- 22:47 · Selling rule (replaces "never sell to the top 4"): sell into any bid where price − our copy value − fee ≥ 3. Selling to the #1 team: also require our gain ≥ (our neg_points ÷ ~130) × their max gain (book × 1.6 − price). Feeding #1 only hurts us through the score denominator.
- 22:47 · Rares from packs (Lucas's question, decided): sell a rare to the best bid when it is not part of a page we are completing and the selling rule passes. Today none qualify: our only rare, LAV-10, is in the LAV page.
- 22:47 · Saturday lever: page bonus = 66.25 × our multiplier. Build pages with dealer buys at ≤ our value (score 0, no loss), finish with one team-bought common. Targets: RET (73), Sunday CHA (106). Skip SAL, MAL and LAT pages: their rares cost more than the bonus.
- 22:47 · Cash: no venue bond Saturday morning unless the broker beats `auto` in replay. RET page needs ~300 P and CHA ~300 P, and the bond would lock 270.
- 22:47 · Bots hold accepts only during SCORED duel sessions. In the practice, `hold_accept_duel_live` held Chato's 31 for 7 ticks (22:24-22:30); the server does not freeze accepts, our bots chose to.

## Corrections to the 22:32 block (independent verification, 22:45)
- D1 confirmed: packs opened at 22:42, `neg_points` unchanged at 27.8, and LAV-06 at 31 cost exactly the predicted −2.3.
- D2: Chato is not a flat 13 on uncommon sales. He moved to a 15 `final` for Team 13 (MAL-06, tick 128). His rare pattern: holds 97 for ~3 offers, then about −1 per tick, `final` around 89-93 after 6-7 offers. "Mirrors 1:1" is wrong.
- D3: "dealer gains score 0" rests on one derived case (LAV-08) plus RULES ("value you gained in trades with other teams"). Treat it as [Likely]. The step-2 gate makes our plan safe either way.
- D6: four team venues exist: v01 Team 6 (0.5%), v02 Team 12 (0%), v03 Team 13 (1%), v04 Team 2 (0%, `auto`). Team 10's complete page comes from `/api/leaderboard` `pages_complete` (1).
- D7: the leader's `neg_points` is fitted per snapshot (85 → 130 between ticks 90 and 125); it is not a test of the model. At tick 130 our ladder part is ~10.7, the leader ~130, and one `neg_point` is ~0.135 board points. Duel points are outside the model.
- D8: the accept freeze is our bots' own rule, not the server's (see the 22:47 line above).

## Fri 22:40 — act on these now, in order (format: time · decision with limits · why)

- 22:40 · OPEN both packs now (assets 320 and 427) before any other deal; read `neg_points` before and after (expect no change) · the −2.3 on LAV-06 was pack drag, not a dealer penalty: 32.5 − 3.8 (unopened packs lose value when we add a card) − 31 = −2.3, the number D1 gave before the trade.
- 22:40 · THEN Chato, buy LAV-07 with Team 3's protocol: open at 13, +1 per tick, never accept above 29, take his `final` at 29 (it comes after ~6 of our moves; threads 234 and 253). Skip it if a pack gave us LAV-07 · our 31 deal moved the ladder 0; Team 3's 29 deal took them to the ladder cap.
- 22:40 · GUARDRAIL: dealer buys are allowed again when price ≤ our value (packs open) or ≤ value − 4 (packs unopened). "No dealer buys at all" is the wrong lesson · dealer gains score 0 and dealer losses score in full, so a buy at or below value costs nothing and can fill a ladder slot.
- 22:40 · After LAV-07 lands, run `GET /api/me/value?card=LAV-09` and log the number. Never buy LAV-09 from Chato · Team 17 completed its SAL page with a TEAM trade at tick 124 and gained about +45 on a card worth +5 to them, so a page bonus does score through team trades. This replaces D3's "likely not".
- 22:40 · Ladder is the leak tonight: our ladder part fell from ~12.4 to ~10 since tick 125 because rivals closed Chato deals (Teams 3, 12, 13, 14). Prioritise the LAV-07 deal over every listing until 23:00 · board 16.5 → 13.9 with our `neg_points` almost flat.

## Fri 22:32 — directives

**D1. Open both packs (asset 320 `sobre_barrio`, asset 427 `sobre_bienvenida`) before accepting anything from Chato.**
- Why: `neg_points` tracks our whole collection value, unopened packs included. Every new card we acquire lowers the packs' expected value, and that loss is booked. **[Verified]** SAL-08 bought at 18 (worth 22.5) scored +1.9, not +4.5; SAL-06 sold at 26 scored +6.0, not +3.5. Both gaps are the pack effect (2.6).
- With the packs unopened, LAV-06 at 31 from Chato scores about −2.3 (32.5 − 3.8 pack drag − 31), and dealer losses count. Break-even is ~28.7 unopened, 32 opened.
- The welcome pack has a 40% rare slot. Team 12 pulled SAL-09 from theirs and sold it at 75; Team 13 pulled LAT-09. Ours has sat unopened since tick ~98.
- Measure: `neg_points` before and after opening. Expected change 0 (pack luck never counts). If it moves, stop and log it.

**D2. Chato: take LAV-06 and LAV-07, then stop for tonight. No rare from him.**
- **[Verified, feed, 14 threads]** He opens 33 (uncommon), 97 (rare), 188 (silver pack). The 26/77/150 menu is not his price. He never moves first, ignores our first two moves, then mirrors our step 1:1. He accepted 90 from Team 10 while standing at 92. He gave Team 12 a `final` at 91 after erratic offers.
- 32 is not his floor: he was at 31 with us and with Team 1 and still moving. For LAV-07 open at 19 and step +2 each tick; expect ~28.
- He buys uncommons at a flat 13 (4 threads, never moved). Selling him MAL-06/07 loses 4.5. He does haggle on rares (paid Team 13 46 for LAT-09, from 39).
- Third level-2 slot: wait for a RET uncommon on Saturday (worth 27.5). Only the share of his range counts, so a cheap card fills a slot as well as a rare.

**D3. Do not buy LAV-09 from Chato to complete the LAV page.**
- **[Verified]** Dealer deals with a gain score 0; dealer deals with a loss score the full loss. Three Abuela sales above our value: 0 each. LAV-08 at 24 (worth 32.5): 0. MAL-07 at 29 (worth 17.5): −11.8.
- So a page bonus arriving through a dealer purchase would be capped at 0 anyway.
- **[Corrected 22:40]** A page bonus does score when the completing trade is with a team: Team 17 gained about +45 at tick 124 (SAL-08 from Team 12 at 35). Size for us: between +34 and +86, unmeasured. Team 10 finished LAV through Chato at tick 113 and moved only +2.1.
- Free test once we hold LAV-06 and LAV-07: `GET /api/me/value?card=LAV-09`. If ~177, tell Lucas: the only route that could score is a TEAM seller (Team 7 lists LAV-09 at 110). If 91, drop the page for good.

**D4. Do not start the duelist on this machine.** **[Verified]** Aleks has run it since 22:20:02 (his log, and all 6 live duels carry our tick-120 openers). A second process on the same key would double-send.

**D5. If a pack gives a rare, ask Lucas with these numbers ready** (ask addressed `to` the bidder, so they pay the fee):
- MAL-10 → t17 bids 78 (worth 49: +29). MAL-09 → t08 bids 66 (+17).
- LAV-10 second copy → t04 bids 85 (a duplicate is worth 22.75: +62). LAV-09 → keep.
- LAT-09/10 → t18 bids 55 (+20). SAL rares: no bid above our 63, hold.

**D6. Facts the intel files have wrong (fix in `GAME.md` and the analyst context).**
- Two team venues exist: `v01` Team 6 (50 bps, board, tick 100) and `v02` Team 12 "El Duende · zero fee" (0 bps, board, tick 113). "Nobody has a venue" and "the 0-fee venue is unused" are stale. `metrics.py` should list venues and `pages_complete`.
- Team 10 holds LAV-09 (from Chato at 90) and has a complete page. Its 110 bid is gone.
- `strategy.md` 22:18: "sell MAL-07 to Chato above 17.5" is impossible (he pays 13) and would score 0 even if it happened.

**D7. Score model, for every analyst.** **[Likely, fits 7 of our snapshots within ±0.15]**
- Negotiating ≈ ladder part (max 12.5; ours ~12.4, at the cap) + 17.5 × our `neg_points` ÷ the leader's `neg_points`.
- Leader ≈ 120. Ours 30.1 → ~4.4. One `neg_point` tonight ≈ 0.15 board points.
- The ladder cap moves up as the field fills Chato slots, so our 12.4 erodes if we stay at level 1.

**D8. Saturday.**
- All our accepts freeze while a duel is live. Duels I is ~34 duels, 3 at a time, 16 ticks each: over an hour with no dealer accepts and no taker-side trades. Finish dealer deals before hour 6.5 and keep our offers maker-side (the other team accepts).
- Venue: keep the plan. Free stall for the first bench, record `bench_offers`, open a board venue only if our broker beats `auto` in replay.

**D9. Sunday (CHA, 1.6×).** Buy CHA from TEAMS with public bids a few P above the dealer price. A dealer purchase below value scores 0; the same card from a team scores value − price.

## Open questions for the organisers (Dani)
1. The clock will read ~2.6 at 23:00, but round 1 ends at 4.0. Does Saturday open at 4.0? Does the 3.0 Market Test run, and in which round?
2. Does a complete page count in Negotiating, or only in the album?
3. Do `neg_points` and the ladder reset each round?
