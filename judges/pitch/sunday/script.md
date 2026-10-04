# Speaker script · Team 5 · Sunday final pitch (3:00)

Structure = the organisers' four questions (Sunday deck p10). Open `deck.html` (F = full screen; → also steps through slide 2's four reveals). Slides after 3/3 are **BACKUP** for Q&A: five beliefs, impact map, around the Bazaar. Style variants of the same 3 slides: `v2/` (Claude, Apple, Nova, Swiss).
Final numbers: **37.73, #1, 1.97 ahead of Team 10**; Saturday's close #3, 7.09 behind [V board ticks 1440, 2802].

| Slide | Time | Words |
|---|---|---|
| 1 · Q1 approach: adapt | 0:00–0:50 | ≈ 120 |
| 2 · Q2 + Q3 build + why (4 steps × ≈ 25 s) | 0:50–2:30 | ≈ 230 |
| 3 · Q4 learned | 2:30–3:00 | ≈ 75 |

**1 · Q1 · Adapt faster than the game changes · 0:00–0:50**
We're Team 5. At Saturday's close we were third, seven points behind. We finished first. How? We treated the weekend as one loop: learn, decide, act, again. Learn the rules, the organisers' changes and our own measurements. Decide: a hundred logged decisions and twenty-four guardrails in thirty-eight hours. Act: two roles trade, everything else measures. And underneath it all, real-time context: thirty-five thousand public events captured, a status file every five minutes, alerts on our phones. You can't adapt quickly without that. The tick went from sixty seconds to fifteen; we redesigned twice overnight; and we went from third to first.

**2 · Q2 + Q3 · Who decides, who acts, who checks · 0:50–2:30** (→ for each step)
*Decide.* The three of us set goals and hard limits. One Claude Code session, the Chief of staff, makes the big calls and logs them with evidence. It never writes to the game.
*Act.* Only two roles trade. The Operator runs our bots: a taker, a maker book, dealer bots, page closers, with counterparty rules. The Duelist: code decides accept, hold, step and delivery day; Haiku writes the words; guards, an eight-second failover, twenty-seven tunables we change live, tested on a five-world simulator.
*Sense and check.* Everything else is read-only: our venue and its Market Test recorder, the collector, the reactor on the live event stream, Dani's dashboard and a shared archive, the analysts, the Duel Lab and verifiers. And humans in the loop: when the system spots a deal for our market, it pings Lucas and Dani's phones, and we walk over to that team.
*Why.* Three decisions we'd defend. One: code decides, the LLM writes: 2 seconds instead of 9.4, because a fifteen-second tick doesn't wait. Two: two writers, one orchestrator, fourteen watchers, and every limit in writing. Three: we redesigned every night on the day's data and pressure-tested it: simulations, contrarian agents, verifiers on every claim, and tests: 547 for the duelist, 163 for the bots.

**3 · Q4 · What we learned · 2:30–3:00**
Technically: real-time shared context is everything; on day one we worked in silos. Negotiation: time can beat price, and people still decide; alliances in the room outweighed agent tactics. Marketplaces: trust moves trades, not fees; zero commission wasn't enough. Three humans set the limits. Claude ran the bazaar, and checked itself. Thank you.

## Q&A, prepared (sources in brackets)

- **"Wasn't the v10 bounty paying for activity?"** Say it straight: we advertised a 20 P bonus for the seller of each of the first five v10 trades (the v10 ad, 11:36-13:03). The Chief flagged the fair-play risk before Lucas approved it; from 12:20 it was restricted to card bids at ≤ our value, and the one bid above value (15 P over) was cancelled unfilled. **None of the bounty bids filled: it paid nobody.** v10's fills came from our RET-01 push, Team 13's bot and Team 10's listings (CHA-11 ≈ 63 % of v10's value created). [directives 10:50, 11:25, 12:22; team/lucas.md 11:37, 12:20-12:22, 13:01; logs/v10_ad_sun.log; data/feed.jsonl]
- **"Did teams join the club?"** It was an invitation to six teams; we brokered pairs inside it (RET-01 Team 2 → Team 8 settled on v10; RET-09 Team 7 → Team 9 settled on El Rastro). Don't claim members ran our bot rule. [intel/club-pitch.md; intel/market-log.md]
- **"Where is the code?"** main, plus the live Sunday duelist on branch `duelist-loop` @ f57a002 (Aleks's lane; kept unmerged while it runs the Final; named in the submission). [git; docs/duelist-sunday-summary.md]
- **"What failed?"** The MAL page never closed (9 of 10). RET-11 sold at 240 scored 0: 240 − 13 fee − value ≈ 227 = 0. Saturday dealer buys cost −21.5 neg_points. The cap belief lasted 1 h 51 and kept the closer off for 49 min (11:33-12:22). In Duels III, 23 deals closed below a better offer the rival had already made (≈ 197 P), and 3 duels ended with no deal while the rival's offer was inside our limit (≈ 26 P). (The monitor's 3 "outside our limit" flags were day trades its price-only check misread: 11129 scored +42.2.) [score-model.md; GAME.md; directives 12:22; intel/duel-review.md]
- **"Which models?"** Duelist: code policy, Claude Haiku 4.5 writes the messages, a Sonnet fallback. Analysts: scout on Sonnet 5.5, judge on Opus 5.5. The sessions are Claude Code. [`ps`; agents/analyst; __main__.py on duelist-loop]
- **"Why does the Chief never write?"** So that every write has one owner and every decision has a log line with its evidence; the Operator session takes the operator lock by convention. [ORCHESTRATOR.md; tools/operator_lock.py]
- **"CHA-11 with Team 10, a rival?"** One trade, Lucas's call, after Team 10 had been listing on our venue: priced at 190 for a card worth 288 to us, inside both sides' values, so both gained (+1.48 each). It is why we locked the lead at 13:12: no more trades with the top five. [directives 12:50, 13:12]
