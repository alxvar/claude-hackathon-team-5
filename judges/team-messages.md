# Mensajes para el chat del equipo

## Para Lucas (+ Aleks) — 22:35: por qué caemos

Why we dropped #8 → #9 (data in team/dani.md, 22:35):
1. The score is RELATIVE. Teams that don't trade still lose ~0.2-0.5 per snapshot because others gain. Our neg_points went UP (26.3 → 30.1) while our score went DOWN (17.8 → 16.5). Standing still = falling, so we need a steady flow of positive trades.
2. Autoflip's MAL-07 buy cost −2.8 score (already fixed, finding 13).
3. We fed the team that passed us: SAL-06 to Team 17 at 26. Team 17 collects SAL (also bought SAL-09 and SAL-08) and jumped 15.5 → 23.7, now #3. The guardrail only protects the top 3. Proposal: no sales into a set a team collects if it is within ~8 points of us or close to completing that page.
4. Our trades are small (+4 to +8); the big jumps come from rares and full pages.
Also: intel/teams.md is live (rival profiles every 10 min, from my dashboard). For now it reaches GitHub only when my Claude pushes.

# (Fri 22:10)

## Para Lucas

Lucas, 4 things from my side:
1. Correction for the judge: bids #984-988 (SAL-07 18, SAL-08 18, MAL-07 14, MAL-09 38, MAL-10 38) ARE ours. The feed's offer.listed at tick 69 has actor t05; your collector started later, so it shows "?". Team 17 bids 78 for MAL-09/10 and 26 for MAL-07, so ours neither fill nor block. Cancel or keep on purpose.
2. Analysts: besides the timer (5/15/45 min), wake the judge/strategist on events too (we get outbid, a dealer opens, a rival changes sets). Your watch.py already detects most of them.
3. Cost: scout + judge + strategist + operator run all weekend (~30 game hours). Check the Console spend after 1 hour and multiply by 30 before Sunday. My $100 is the Sunday reserve.
4. My dashboard (dashboard/, read-only, public routes WITHOUT the team key, so it doesn't use our 5 req/s) was already built when PLAN said not to. I'll use it to write intel/teams.md as you asked. OK if it writes that file every ~10 min?

## Para Aleks

Aleks, 2 ideas for the duelist:
1. Pick the model from the clock automatically: read tick_seconds each turn. 60 s → Opus, 30 s → Sonnet, 15 s → Haiku or Sonnet without thinking. Budget = tick − 5 s. You measured Opus at 6-10 s, so Sunday needs the switch.
2. After tonight's practice, learn ACROSS duels: from docs/duels/, how rivals open (as a % of the final price), how much they concede per round, when they close. Put those numbers in the strategist prompt as priors before Duels I on Saturday.
I'll ask the organisers' desk whether the pie shrinks per tick or per message, and how a deal outside your limit is penalised.
