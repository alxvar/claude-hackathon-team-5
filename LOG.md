# Team log

**One line per run, experiment or decision. Newest on top.** Format: `time · who · what · result · next`.
Pull before you add a line and push right after. Live numbers are in `STATUS.md` (auto-updated); why we do things is in `PLAN.md` and `CROSSWALK.md`.

## Who is doing what

Each person keeps a **Now** line and a log in their own file: `team/aleks.md`, `team/dani.md`, `team/lucas.md`. `STATUS.md` shows all three, refreshed every 5 minutes. **Write only in your own file.** This file (findings, experiments, history) is maintained by Lucas.

## Experiments: how we beat the leaders, not copy them

Team 10 leads with one lever: buying from Abuela the cards of its high-value sets. We stack every lever the rules score. Each row has an owner and a metric from the server; results go in the last column.

| # | Lever | Owner | Status | Metric | Result |
|---|---|---|---|---|---|
| E1 | Buy from dealers what is worth more to us than its price (now: LAV uncommons, worth 32.5 P to us, ~23 P from Abuela) | Lucas (bot) | **stopped 21:16**: LAV-08 bought at 24, but dealer buys add ~0 `neg_points` (finding 0); LAV-06/07 now bid from teams | `neg_points` and `negotiating` before vs after each deal (bot logs both) | — |
| E2 | Sell to dealers what is worth little to us (6 spare copies worth ~1 P; Abuela pays 5-13) | Lucas (bot, `--no-buy --sell-spares`) | running since 21:16: cash for team trades, plus ladder | same | — |
| E3 | Trade with other teams: multipliers differ up to 3x between teams, so our low-value cards (LAT, MAL) are worth more to someone else, and LAV-09 (rare) is worth 91 P to us. Only 1 team-to-team trade in the whole game so far | Lucas (`agents/trader/trade.py`, `loop.py` autopilot) | **live since 21:14; autopilot since 21:20** | value gained at our private values (rules: Negotiating) | Teams 8, 13 and 14 jumped from ~11 to 22-26 points with ONE rare traded between teams at 65-70 P. Ours: accepted 6 P for a spare MAL-02 (worth 1.8 to us); listed SAL-06 32, MAL-08 26, LAT-07 21, LAT-06 22 (worth 12.5-22.5 to us); bid 70 for LAV-09 (worth 91 to us) |
| E4 | Flag dealers whose words don't match their structured offer (*"a correct flag scores, a wrong one costs"*) | Lucas (bot) | when a dealer that lies appears | flag points | — |
| E5 | Be first with each new dealer, value-first (higher levels weigh more; our negotiated deals give us the head start) | Lucas (bot, `--dealer`) | ready | ladder + `neg_points` | — |
| E6 | Duels: Clock-Standing on the duel API, decay-aware closing, two issues for Duels II | Aleks | practice duels ~22:20 | duel share | — |
| E7 | Market: record the real bench book at the first Market Test, then a broker that beats the stall | Lucas | Saturday morning | bench efficiency | sim: the stall beats both naive alternatives; need real data |

**Live loop:** `tools/watch.py` runs on Lucas's machine and wakes his Claude Code on every change: leaderboard, our score, our deals, new dealers or levels, duels, teammate pushes. Each experiment's result lands here within minutes.

## Findings so far (keep this list short; update it, don't append)

0. **MEASURED: `neg_points` only counts trades between teams, at our private values, net of fees.** Dealer deals barely move it: buying LAV-08 from Abuela (worth 32.5 to us, paid 24) added ~+0.3, while selling MAL-08 to a team (worth 17.5, sold at 26) added ~+8.5. Dealer deals feed the ladder (best 3 per level, small: +0.005 for LAV-08). **So: buy cards worth a lot to us from TEAMS, not dealers; use dealers for the ladder and for cash.** Team 10 leads with 29.1 (we have 12.0) by buying uncommons of its valuable sets from Abuela at 23-24 P (LAV-06, LAV-07, MAL-07), building a full LAV page. Our private `neg_points` is −8.5, almost surely from the 3 packs: random cards, mostly duplicates worth little to us. **Rule: buy what is worth more to us than its price, sell what is worth less, no more packs.** For us that's LAV (each LAV uncommon is worth 32.5 P to us; LAV-09 rare is worth 91 P and would complete our LAV page).
1. **Abuela follows a fixed pattern** (50 conversations from all teams, public feed, ticks 4-36). When she opens high (pack 30 P, uncommon 29, common 12) she ends at about **73-75% of her opening** (pack ~22, uncommon ~21, common ~9). She concedes most in her first two moves, then 1 P at a time, and our step size barely changes this. **When she opens low (pack 17, some commons 7) she doesn't move at all.**
2. **Our Abuela deals already land at her floor.** We're 2nd at 12.46, against 12.50 for 1st. Only our best 3 deals per level count, so **more Abuela deals add almost nothing.** Effort goes to the next dealers (higher levels weigh more), the market and the duels.
3. **Selling to her:** she bids about 5 or 12-13 P and mostly holds. One team pushed her from 12 to 16 by asking 35 and stepping down 3 P at a time. Our spare copies are worth about 1 P to us.
4. **El Rastro has nothing worth buying at our values** (32 listings at tick 35; commons flooded at 12 P). Check again on Saturday, when El Retiro comes out and teams chase full pages.
5. **Our private `neg_points` shows −8.5 and we can't explain it.** Question for the organisers: what is it, and does it pull our negotiating score down?
6. **The first Market Test (game hour 3.0) falls after tonight's 23:00 close**, so it runs Saturday morning. The practice duels (game hour 2.0) are still tonight, at about 22:20.

## Log (history up to Fri 21:18; new lines go in `team/<name>.md`)

- Fri 21:15 · Lucas · **measured:** MAL-08 sold to a team at 26 P (+~8.5 `neg_points`) vs LAV-08 bought from Abuela at 24 P (+~0.3) · team trades are the lever, dealer buys aren't (finding 0 rewritten) · bid 24 P for LAV-06 from teams instead of buying it from Abuela · `neg_points` −8.5 → +2.7
- Fri 21:12 · Lucas · **calibration:** sold the spare MAL-02 for 6 P → `neg_points` −8.5 → −6.1 (+2.4) and cash +4 (we paid the 2 P fee as the accepting side) · confirms `neg_points` = value gained at our private values, net of fees (6 − 2 fee − 1.75 lost ≈ +2.3) · when we accept, we pay the fee; when they accept our listing, they do
- Fri 21:14 · Lucas · E3 live: the jump of Teams 8/13/14 came from rare cards traded between teams at 65-70 P, not from Abuela · accepted MAL-02 for 6 P; 4 uncommons listed at ~9 P above our value; bid 70 P for LAV-09 · cash floor for the venue bond relaxed to ~200 tonight (no venue possible before level 2; Saturday adds 150 P)
- Fri 21:12 · Lucas · `tools/watch.py` live watcher (score, leaderboard, deals, dealers, duels, pushes) + experiments table E1-E7 · next: E3 (team trades) while E1-E2 run
- Fri 21:07 · Lucas (bot) · dealer bot reworked: buys by value minus expected price, logs score per deal; running: LAV-08 and LAV-07, then 7 spare sales, then LAV-06 · next: check neg_points per deal to confirm finding 0
- Fri 21:05 · Lucas · `broker/sim.py`, an offline Market Test: **the free stall's best-bid-vs-best-ask beats both alternatives I tried** (most pairs: 0.92 vs 0.95 efficiency; waiting: 0.48) in every trader model · beating the stall needs real limit estimates, so we record the real book at the first Market Test before building more
- Fri 21:02 · Aleks · duelist moved out of `bazaar-kit/` to `agents/duelist/`; LLM engine split into `engine/` (`Model` interface + Claude provider); our deps now in the root `pyproject.toml`, kit's back to the organisers' · 14 offline tests pass · next: run with `uv run python -m agents.duelist` from the repo root
- Fri 21:00 · Lucas · mined all teams' Abuela conversations from the public feed · she ends at ~73-75% of a high opening and never moves from a low one; our deals are at her floor (findings 1-3) · next: bot ready for the next dealer, then the market broker
- Fri 20:50 · Lucas · `tools/status.py` writes `STATUS.md` every 5 min (score, deals, Abuela benchmark from every team's deals, duels, schedule) · live on GitHub · everyone reads it before asking
- Fri 20:47 · Lucas (bot) · `abuela_bot.py --deals 2`: LAV-05 and LAV-02 bought at 9 P each (she opened at 12; we went 7 → 8 → 9) · 4 negotiated deals in total, cash 321 P, rank 3 · next: sell spares to Abuela, tune the opening counter against the benchmark
- Fri 20:38 · Aleks · starter stopped; Abuela handed to Lucas's bot · Aleks on the practice duels
- Fri 20:31 · team · `PLAN.md` agreed: one owner and one live script per job (duels: Aleks; dealers and market: Lucas; Dani: judges, organisers, notes)
- Fri ~20:20 · Aleks · starter re-run twice: two packs at 22 P after real haggling (she opened at 30 and came down 30 → 25 → 23 → 22) · negotiated deals
- Fri ~20:12 · Aleks · `starter_agent.py`: pack at 17 P, her first offer, accepted with no counter · probably not a negotiated deal
- Fri ~20:10 · organisers · game clock started (60 s ticks)
- Fri 20:10 · Lucas · `CROSSWALK.md` (research × sims × rules) checked by an independent verifier; 3 major flags fixed
