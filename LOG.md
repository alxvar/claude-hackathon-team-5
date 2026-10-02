# Team log

**One line per run, experiment or decision. Newest on top.** Format: `time · who · what · result · next`.
Pull before you add a line and push right after. Live numbers are in `STATUS.md` (auto-updated); why we do things is in `PLAN.md` and `CROSSWALK.md`.

## Findings so far (keep this list short; update it, don't append)

1. **Abuela's opening price changes from one conversation to the next.** For the same pack she opened at 17 P in some conversations and at 30 P in others. From 30 she came down to 22 P in steps that kept shrinking (−5, −2, −1).
2. **Other teams pay a median of 17 P for a pack (13 deals); we paid 22 P twice.** Their 17s look like her low opening. Next time she opens low, counter once just under her price and then accept: still cheap, and it counts as negotiated.
3. **Abuela pays teams about 9 P for a common** (median of 2 deals, thin data). Our spare copies are worth about 1 P to us, so selling her a spare brings in cash and a dealer deal. The other route is listing them on El Rastro at 10 P for another team.
4. **Single commons are the cheapest dealer deals:** 9 P each against her 12 P opening, and the same ladder credit per deal as a 22 P pack.
5. **The first Market Test (game hour 3.0) falls after tonight's 23:00 close**, so the first one runs Saturday morning. The practice duels (game hour 2.0) are still tonight, at about 22:20.

## Log

- Fri 20:50 · Lucas · `tools/status.py` writes `STATUS.md` every 5 min (score, deals, Abuela benchmark from every team's deals, duels, schedule) · live on GitHub · everyone reads it before asking
- Fri 20:47 · Lucas (bot) · `abuela_bot.py --deals 2`: LAV-05 and LAV-02 bought at 9 P each (she opened at 12; we went 7 → 8 → 9) · 4 negotiated deals in total, cash 321 P, rank 3 · next: sell spares to Abuela, tune the opening counter against the benchmark
- Fri 20:38 · Aleks · starter stopped; Abuela handed to Lucas's bot · Aleks on the practice duels
- Fri 20:31 · team · `PLAN.md` agreed: one owner and one live script per job (duels: Aleks; dealers and market: Lucas; Dani: judges, organisers, notes)
- Fri ~20:20 · Aleks · starter re-run twice: two packs at 22 P after real haggling (she opened at 30 and came down 30 → 25 → 23 → 22) · negotiated deals
- Fri ~20:12 · Aleks · `starter_agent.py`: pack at 17 P, her first offer, accepted with no counter · probably not a negotiated deal
- Fri ~20:10 · organisers · game clock started (60 s ticks)
- Fri 20:10 · Lucas · `CROSSWALK.md` (research × sims × rules) checked by an independent verifier; 3 major flags fixed
