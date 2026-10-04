# Speaker script · Team 5 · Sunday final pitch

Structure = the organisers' four questions (Sunday deck p10). Open `deck.html` (F = full screen; → also steps through slide 2's four reveals; `deck.html#2.3` jumps to slide 2, step 4). Slides after 3/3 are **BACKUP** for Q&A: race chart, five beliefs, impact map, around the Bazaar.
Final numbers (15:00): **37.73, #1, 1.97 ahead of Team 10** (35.76); #1 at every snapshot from 12:35 to the close; Grand Final duels 27 of 34.

| Slide | 5:00 version | 3:00 cut |
|---|---|---|
| 1 · Q1 approach (the loop) | 0:00–1:00 | 0:00–0:40 |
| 2 · Q2 + Q3 build + why (control room, 4 steps) | 1:00–3:50 | 0:40–2:30 |
| 3 · Q4 learned + one more day | 3:50–4:50 | 2:30–3:00 |

## 5-minute version (≈ 690 words)

**1 · Q1 · How we approached it · 0:00–1:00**
We're Team 5, and we finished the game first: 37.73, ahead of Team 10. Here's how we approached it: as a loop. Sense, decide, act, measure, learn, with git at the centre. One real lap. Our first idea was to let an LLM negotiate the duels. Saturday's records said it took 9.2 seconds a reply, 29 percent over ten, and today's tick is fifteen. So we decided: code decides price, day and accept, and the LLM only writes the words. We tested that first on a simulator validated on Saturday's duels, shipped it overnight, and this morning it closed 57 of 68 duels, then 27 of 34 in the Grand Final. The review and the Duel Lab then found a missed last-tick accept; we fixed it and restarted on the Duel Lab's go. We kept the LLM's words and replaced its decisions. And three humans and seven-plus Claude sessions stayed in sync through git, one file per owner, a decision log for the big calls, session-to-session messages and a status file rewritten every five minutes.

**2 · Q2 + Q3 · What we built, and why · 1:00–3:50** (→ for each step)
*Step 1, Decide (≈ 35 s).* What we built is a control room. At the top, decide: the three of us set the goals and the hard limits, and one Claude Code session, the Chief of staff, makes the big calls and logs them with their evidence. It never writes to the game.
*Step 2, Act (≈ 40 s).* Below, act. Exactly two roles trade. The Operator, a Claude Code session, runs our trades through the bots it starts: a taker, a maker book, dealer bots and page closers. And the Duelist: code decides, Haiku writes the words, with guards, an eight-second failover and parameters we change live. Solid arrows are authority; the red ones are the only writes.
*Step 3, Sense and check (≈ 40 s).* On the right, sense and check: our venue, which only posts its ads, and its Market Test recorder, the collector and the status file, Dani's dashboard and a shared archive, analysts on the Claude API, the Duel Lab simulator and fresh verifiers. Dashed arrows are data flowing back to the Chief.
*Step 4, the decisions we'd defend (≈ 55 s).* One: code decides, the LLM writes, because a fifteen-second tick doesn't wait. Two: one trader per job, and Lucas changes a hard limit only with a written guardrail line, because one key, five requests a second and one accept per tick are shared by everything we run. Three: check before you act. A fresh verifier and contrarian reviews on the big calls, the Duel Lab before every Sunday duelist start, because the author can't grade its own work.

**3 · Q4 · What we learned · 3:50–4:50** *(draft: the team rewrites the slots)*
Technically: code decides and the LLM writes; and the generator can't grade itself, a separate verifier caught what the author missed, in this deck too.
Negotiation: decay is per exchange, so silence is free; and take the good offer when it's there: by our monitor's price check, 23 deals this morning closed below an offer the rival had already made.
Marketplaces: value created, not activity, and a trade with a rival lifts them as much as you; and pushing pairs and partners moved trades, the bounty didn't.
With one more day: merge the Sunday duelist into main, switch on the broker we staged, and put a verifier gate on every directive.
Three humans set the limits. Claude ran the bazaar, and checked itself. Thank you.
*(Alternative negotiation line from the Chief, unverified [?]: "small steps earn small steps".)*

## 3-minute cut (≈ 430 words)

**1 · 0:00–0:40** We're Team 5, and we finished the game first. We approached it as a loop: sense, decide, act, measure, learn. One lap: our first idea, an LLM negotiating duels, took 9.2 seconds a reply on a fifteen-second tick. So code decides and the LLM only writes. Tested on a simulator, shipped overnight: 57 of 68 duels closed this morning. Git, a decision log and session messages kept three humans and seven-plus Claude sessions in sync.

**2 · 0:40–2:30** What we built is a control room. *(→)* Decide: we set the limits; a Claude Code Chief of staff makes the big calls with their evidence and never writes to the game. *(→)* Act: only two roles trade, the Operator with its trading bots, and the Duelist, where code decides and Haiku talks. *(→)* Sense and check: venue, collector, dashboard, analysts, the Duel Lab and fresh verifiers. *(→)* Three decisions we'd defend: code decides, because a fifteen-second tick doesn't wait; one trader per job with written limits, because the key's limits are shared; and check before you act, because the author can't grade its own work.

**3 · 2:30–3:00** We learned: code decides, the LLM writes; silence is free in a negotiation; value created beats activity, and pushing pairs moved trades where a bounty didn't. One more day: merge the Sunday duelist into main, switch on the broker, gate every directive with a verifier. Three humans set the limits. Claude ran the bazaar, and checked itself.

## Q&A, prepared (sources in brackets)

- **"Wasn't the v10 bounty paying for activity?"** Say it straight: we advertised a 20 P bonus for the seller of each of the first five v10 trades (the v10 ad, 11:36-13:03). The Chief flagged the fair-play risk before Lucas approved it; from 12:20 it was restricted to card bids at ≤ our value, and the one bid above value (15 P over) was cancelled unfilled. **None of the bounty bids filled: it paid nobody.** v10's fills came from our RET-01 push, Team 13's bot and Team 10's listings (CHA-11 ≈ 63 % of v10's value created). [directives 10:50, 11:25, 12:22; team/lucas.md 11:37, 12:20-12:22, 13:01; logs/v10_ad_sun.log; data/feed.jsonl]
- **"Did teams join the club?"** It was an invitation to six teams; we brokered pairs inside it (RET-01 Team 2 → Team 8 settled on v10; RET-09 Team 7 → Team 9 settled on El Rastro). Don't claim members ran our bot rule. [intel/club-pitch.md; intel/market-log.md]
- **"Where is the code?"** main, plus the live Sunday duelist on branch `duelist-loop` @ f57a002 (Aleks's lane; kept unmerged while it runs the Final; named in the submission). [git; docs/duelist-sunday-summary.md]
- **"What failed?"** The MAL page never closed (9 of 10). RET-11 sold at 240 scored 0: 240 − 13 fee − value ≈ 227 = 0. Saturday dealer buys cost −21.5 neg_points. The cap belief lasted 1 h 51 and kept the closer off for 49 min (11:33-12:22). In Duels III, 23 deals closed below a better offer the rival had already made (≈ 197 P), and 3 duels ended with no deal while the rival's offer was inside our limit (≈ 26 P). (The monitor's 3 "outside our limit" flags were day trades its price-only check misread: 11129 scored +42.2.) [score-model.md; GAME.md; directives 12:22; intel/duel-review.md]
- **"Which models?"** Duelist: code policy, Claude Haiku 4.5 writes the messages, a Sonnet fallback. Analysts: scout on Sonnet 5.5, judge on Opus 5.5. The sessions are Claude Code. [`ps`; agents/analyst; __main__.py on duelist-loop]
- **"Why does the Chief never write?"** So that every write has one owner and every decision has a log line with its evidence; the Operator session takes the operator lock by convention. [ORCHESTRATOR.md; tools/operator_lock.py]
- **"CHA-11 with Team 10, a rival?"** One trade, Lucas's call, after Team 10 had been listing on our venue: priced at 190 for a card worth 288 to us, inside both sides' values, so both gained (+1.48 each). It is why we locked the lead at 13:12: no more trades with the top five. [directives 12:50, 13:12]
