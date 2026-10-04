# Speaker script · Team 5 · Sunday final pitch

Open `deck.html` (F = full screen, ← → to move). **Top 3 at 15:00 → 5 minutes, all 7 slides. Otherwise press `3` for the 3-minute cut** (skips slide 6, the loop).
Numbers marked ⟳ change at 15:00: re-run `python3 judges/pitch/sunday/race_sunday.py` (slide 1 updates itself), then update the ⟳ lines here, in `submit-story.md` and on arch C.

## 5-minute version (≈ 680 words)

**1 · From #5 to #1 · 0:00–0:30**
We're Team 5. Three humans, seven-plus Claude Code sessions and nineteen daemons we built. Friday's round closed with us sixth. Saturday afternoon we touched first. Since 12:35 today we've been first: 37.26 on the board, 3.09 ahead ⟳. Here's what we built, and what we got wrong on the way.

**2 · Architecture: the control room · 0:30–1:20**
This is the system. The three of us set the goal and the hard limits. One Claude Code session, the Chief of staff, makes every decision and logs it with its evidence. It never touches the game. Only two roles write to the game: the Operator, with the trading and dealer bots it starts, and the Duelist. Fourteen read-only daemons feed the live numbers back up. On the right, a column whose only job is to check: a fresh verifier, a duel simulator, the analysts, contrarian reviews. Everything shares one memory: git, one owner per file.

**3 · Five beliefs our data broke · 1:20–2:10**
Our first ideas were wrong in five useful ways.
We thought any trade at a gain scores. Dealer gains clip to zero and losses count in full, so pages close only through team trades.
We thought an LLM should negotiate the duels. It took 9.2 seconds a reply, 29 percent over ten, on a fifteen-second tick. So code decides and Haiku only writes the words: 57 of 68 duels closed this morning.
We believed gains were capped at 50 a round. Our own logs disproved it at 12:17.
A trade with a rival pays them too, so at 13:12 we locked the lead.
And our zero-fee market had no trades this morning, until we pushed pairs and partners onto it: six trades by 13:10.

**4 · Where the points came from · 2:10–2:45**
Here's the score by the part of the system that earned it. The Duelist: 6.75. The Operator and its bots: 17.43, from page closes, the dealer ladder and one epic. Our market: 13.08. The grey band is the Market Test every stall gets. The blue band is what our venue added on top, over two days: 4.08 more than teams with only a stall.

**5 · Built around the Bazaar · 2:45–3:25**
We also built around the game. The biggest piece is a market with more than two sides: a club matchmaker. It estimates every team's album from the public feed, matches one team's spare copy to another team's missing card, page-closers first, prices each deal between the two values so both sides gain, and is designed to rotate hosting across the members' markets. Under it: a demand model of what every card is worth to every team, a shared archive of the history the feed drops, a Market Test lab, a live reactor on the event stream, and Dani's live showcase for you.

**6 · The loop · 3:25–4:05** *(skip in the 3-minute cut)*
Underneath, it's a loop: sense, decide, act, measure, learn. One real lap from today. At 10:27 a sale didn't score. We decided gains were capped and stopped our page closer. At 12:17 a five-point sale moved the counter. Corrected at 12:22, from our own data, one hour fifty-one later, and the next +50 trade added 1.48.

**7 · What we learned · 4:05–4:50**
Technically: let code decide and the LLM talk; separate who decides, who writes and who checks; treat every belief as a bug until the data agrees.
About markets: scoring is relative, losses count while gains clip, and a market needs a matchmaker, not just a low fee.
With one more day: merge the Sunday duelist with per-opponent day weights, switch on the broker we built, and put a verifier gate on every directive.
Three humans set the limits. Claude ran the bazaar, and checked itself. Thank you.

## 3-minute cut (≈ 420 words · slides 1-2-3-4-5-7)

**1 · 0:00–0:20** We're Team 5: three humans, seven-plus Claude Code sessions. Sixth after Friday, first since 12:35 today: 37.26, 3.09 ahead ⟳.

**2 · 0:20–0:55** The system is a control room. We set the limits. A Claude Code Chief of staff decides and logs every call with its evidence, and never touches the game. Only two roles write: the Operator and its bots for trades, the Duelist for duels. Fourteen daemons read; a separate column only checks. Git is the shared memory.

**3 · 0:55–1:40** Five beliefs our data broke. Dealer gains don't score but dealer losses do, so pages close through teams. An LLM deciding duels was too slow for a 15-second tick, so code decides and Haiku writes: 57 of 68 closed. The "cap of 50" was a myth, disproved by our own logs. A trade with a rival pays them too, so we locked the lead. And our zero-fee market had no trades this morning until we pushed pairs and partners onto it.

**4 · 1:40–2:05** Where the points came from: Duelist 6.75, Operator and bots 17.43, our market 13.08, of which 4.08 is above what a plain stall gets.

**5 · 2:05–2:30** Around the game we built a market with more than two sides: a club matchmaker that estimates every album from the public feed, pairs spares with missing cards, prices between both values so both gain, and is designed to rotate hosting across members. Plus a demand model, an archive, a Market Test lab and a live showcase.

**7 · 2:30–2:58** We learned: code decides, the LLM talks; separate deciding, writing and checking; scoring is relative and a market needs a matchmaker. One more day: merge the Sunday duelist, switch on the broker, and gate every directive with a verifier. Three humans set the limits. Claude ran the bazaar, and checked itself. Thank you.

## Q&A, prepared (sources in brackets)

- **"Wasn't the v10 bounty paying for activity?"** Say it straight: we advertised a 20 P bonus for the seller of each of the first five v10 trades (the v10 ad, 11:36-13:03). The Chief flagged the fair-play risk before Lucas approved it; from 12:20 it was restricted to card bids at ≤ our value, and the one bid above value (15 P over) was cancelled unfilled. **None of the bounty bids filled: it paid nobody.** v10's fills came from our RET-01 push, Team 13's bot and Team 10's listings (CHA-11 ≈ 63 % of v10's value created). [directives 10:50, 11:25, 12:22; team/lucas.md 11:37, 12:20-12:22, 13:01; logs/v10_ad_sun.log; data/feed.jsonl]
- **"Did teams join the club?"** It was an invitation to six teams; we brokered pairs inside it (RET-01 Team 2 → Team 8 settled on v10; RET-09 Team 7 → Team 9 settled on El Rastro). Don't claim members ran our bot rule. [intel/club-pitch.md; intel/market-log.md]
- **"Where is the code?"** main, plus the live Sunday duelist on branch `duelist-loop` @ f57a002 (Aleks's lane; kept unmerged while it runs the Final; named in the submission). [git; docs/duelist-sunday-summary.md]
- **"What failed?"** The MAL page never closed (9 of 10). RET-11 sold at 240 scored 0: 240 − 13 fee − value ≈ 227 = 0. Saturday dealer buys cost −21.5 neg_points. The cap belief lasted 1 h 51 and kept the closer off for 49 min (11:33-12:22). In Duels III, 23 deals closed below a better offer the rival had already made (≈ 197 P), and 3 duels ended with no deal while the rival's offer was inside our limit (≈ 26 P). (The monitor's 3 "outside our limit" flags were day trades its price-only check misread: 11129 scored +42.2.) [score-model.md; GAME.md; directives 12:22; intel/duel-review.md]
- **"Which models?"** Duelist: code policy, Claude Haiku 4.5 writes the messages, a Sonnet fallback. Analysts: scout on Sonnet 5.5, judge on Opus 5.5. The sessions are Claude Code. [`ps`; agents/analyst; __main__.py on duelist-loop]
- **"Why does the Chief never write?"** So that every write has one owner and every decision has a log line with its evidence; the Operator session takes the operator lock by convention. [ORCHESTRATOR.md; tools/operator_lock.py]
- **"CHA-11 with Team 10, a rival?"** One trade, Lucas's call, after Team 10 had been listing on our venue: priced at 190 for a card worth 288 to us, inside both sides' values, so both gained (+1.48 each). It is why we locked the lead at 13:12: no more trades with the top five. [directives 12:50, 13:12]
