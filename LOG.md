# Team log

**One line per run, experiment or decision. Newest on top.** Format: `time · who · what · result · next`.
Pull before you add a line and push right after. Live numbers are in `STATUS.md` (auto-updated); why we do things is in `PLAN.md` and `CROSSWALK.md`.

## Now: who is doing what (each owner keeps their own line current)

| Who | Working on now | Touches | Next |
|---|---|---|---|
| **Aleks** | Duels: Clock-Standing on the duel API (`duels`, `duel_say`, `duel_accept`), on Claude, for the practice duels (~22:20). _Aleks: please confirm or correct this line_ | `agents/duels/`, duel endpoints | Push the bench code; log what you run in the practice |
| **Lucas** (+ Claude Code) | 1) **Dealer bot running (21:25):** buys LAV uncommons (worth 32.5 P to us, about 23 P from Abuela), sells our 7 spare copies, and logs the score before and after every deal. 2) Market Test broker, offline (`broker/sim.py`) | `agents/dealers/`, `broker/`, `tools/`, `STATUS.md`; dealer and market endpoints only | Read the practice duels; tune the broker |
| **Dani** | Five questions to the organisers' desk (the four in `PLAN.md`, plus: what is `neg_points`?). Writes the answers here | `LOG.md` | The story for the judges |

## Findings so far (keep this list short; update it, don't append)

0. **Score is about value at OUR private values, not just haggling** (likely; checking it deal by deal). Team 10 leads with 29.1 (we have 12.0) by buying uncommons of its valuable sets from Abuela at 23-24 P (LAV-06, LAV-07, MAL-07), building a full LAV page. Our private `neg_points` is −8.5, almost surely from the 3 packs: random cards, mostly duplicates worth little to us. **Rule: buy what is worth more to us than its price, sell what is worth less, no more packs.** For us that's LAV (each LAV uncommon is worth 32.5 P to us; LAV-09 rare is worth 91 P and would complete our LAV page).
1. **Abuela follows a fixed pattern** (50 conversations from all teams, public feed, ticks 4-36). When she opens high (pack 30 P, uncommon 29, common 12) she ends at about **73-75% of her opening** (pack ~22, uncommon ~21, common ~9). She concedes most in her first two moves, then 1 P at a time, and our step size barely changes this. **When she opens low (pack 17, some commons 7) she doesn't move at all.**
2. **Our Abuela deals already land at her floor.** We're 2nd at 12.46, against 12.50 for 1st. Only our best 3 deals per level count, so **more Abuela deals add almost nothing.** Effort goes to the next dealers (higher levels weigh more), the market and the duels.
3. **Selling to her:** she bids about 5 or 12-13 P and mostly holds. One team pushed her from 12 to 16 by asking 35 and stepping down 3 P at a time. Our spare copies are worth about 1 P to us.
4. **El Rastro has nothing worth buying at our values** (32 listings at tick 35; commons flooded at 12 P). Check again on Saturday, when El Retiro comes out and teams chase full pages.
5. **Our private `neg_points` shows −8.5 and we can't explain it.** Question for the organisers: what is it, and does it pull our negotiating score down?
6. **The first Market Test (game hour 3.0) falls after tonight's 23:00 close**, so it runs Saturday morning. The practice duels (game hour 2.0) are still tonight, at about 22:20.

## Log

- Fri 21:25 · Lucas (bot) · dealer bot reworked: buys by value minus expected price, logs score per deal; running: LAV-08 and LAV-07, then 7 spare sales, then LAV-06 · next: check neg_points per deal to confirm finding 0
- Fri 21:20 · Lucas · `broker/sim.py`, an offline Market Test: **the free stall's best-bid-vs-best-ask beats both alternatives I tried** (most pairs: 0.92 vs 0.95 efficiency; waiting: 0.48) in every trader model · beating the stall needs real limit estimates, so we record the real book at the first Market Test before building more
- Fri 21:00 · Lucas · mined all teams' Abuela conversations from the public feed · she ends at ~73-75% of a high opening and never moves from a low one; our deals are at her floor (findings 1-3) · next: bot ready for the next dealer, then the market broker
- Fri 20:50 · Lucas · `tools/status.py` writes `STATUS.md` every 5 min (score, deals, Abuela benchmark from every team's deals, duels, schedule) · live on GitHub · everyone reads it before asking
- Fri 20:47 · Lucas (bot) · `abuela_bot.py --deals 2`: LAV-05 and LAV-02 bought at 9 P each (she opened at 12; we went 7 → 8 → 9) · 4 negotiated deals in total, cash 321 P, rank 3 · next: sell spares to Abuela, tune the opening counter against the benchmark
- Fri 20:38 · Aleks · starter stopped; Abuela handed to Lucas's bot · Aleks on the practice duels
- Fri 20:31 · team · `PLAN.md` agreed: one owner and one live script per job (duels: Aleks; dealers and market: Lucas; Dani: judges, organisers, notes)
- Fri ~20:20 · Aleks · starter re-run twice: two packs at 22 P after real haggling (she opened at 30 and came down 30 → 25 → 23 → 22) · negotiated deals
- Fri ~20:12 · Aleks · `starter_agent.py`: pack at 17 P, her first offer, accepted with no counter · probably not a negotiated deal
- Fri ~20:10 · organisers · game clock started (60 s ticks)
- Fri 20:10 · Lucas · `CROSSWALK.md` (research × sims × rules) checked by an independent verifier; 3 major flags fixed
