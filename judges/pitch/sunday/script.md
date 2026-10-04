# Speaker script · Team 5 · Sunday final pitch

Open `deck.html` (F = full screen, ← → to move). **Top 3 at 15:00 → 5 minutes, all 6 slides. Otherwise press `3` for the 3-minute cut** (skips slide 5, the loop).
Numbers marked ⟳ change at 15:00: re-run `python3 judges/pitch/sunday/race_sunday.py` and update the line on slide 1 and here.

## 5-minute version (≈ 610 words)

**1 · From #5 to #1 · 0:00–0:30**
We're Team 5. Three humans and one laptop running seven-plus Claude Code sessions and nineteen daemons. Friday night we closed fifth. Saturday afternoon we touched first. Since 12:35 today we've been first: 37.26 on the board, 3.09 ahead ⟳. Here's what we built, and what we got wrong on the way.

**2 · Architecture: the control room · 0:30–1:30**
This is the system. The three of us set the goal and the hard limits. One Claude Code session, the Chief of staff, makes every decision and logs it with its evidence. It never touches the game. Only two processes write to the game: the Operator, which runs our trades and dealer bots, and the Duelist. Fourteen read-only daemons feed the live numbers back up. On the right, a column whose only job is to check: a fresh verifier, a duel simulator, the analysts, contrarian reviews. And everything shares one memory: git, one owner per file, so nobody overwrites anybody.

**3 · Five beliefs our data broke · 1:30–2:30**
Our first ideas were wrong in five useful ways.
We thought any trade at a gain scores. Dealer gains clip to zero and losses count in full, so pages close only through team trades.
We thought an LLM should negotiate the duels. It took 9.2 seconds a reply, and every exchange costs ten percent. So code decides and Haiku only writes the words: 57 of 68 duels closed this morning.
We believed gains were capped at 50 a round. Our own logs disproved it at 12:17.
A trade with a rival pays them too, so at 13:05 we locked the lead.
And a zero-fee market got zero trades, until a small first-trades bounty, paid in cards.

**4 · Where the points came from · 2:30–3:15**
Here's the score by the part of the system that earned it. The Duelist: 6.75. The Operator and its bots: 17.43, from page closes, the dealer ladder and one epic. Our market: 13.08. The grey band is the Market Test every stall gets. The blue band is what our venue added on top: 4.08 more than teams with only a stall.

**5 · The loop · 3:15–4:00** *(skip in the 3-minute cut)*
Underneath, it's a loop: sense, decide, act, measure, learn. One real lap from today. At 10:27 a sale didn't score. We decided gains were capped and stopped our page closer. At 12:17 a five-point sale moved the counter. Corrected at 12:22, from our own data, one hour fifty-one later, and the next +50 trade added 1.48.

**6 · What we learned · 4:00–4:45**
Technically: let code decide and the LLM talk; separate who decides, who writes and who checks; treat every belief as a bug until the data agrees.
About markets: scoring is relative, losses count while gains clip, and a market needs its first trade.
With one more day: merge the Sunday duelist with per-opponent day weights, switch on the broker we built, and put a verifier gate on every directive.
Three humans set the limits. Claude ran the bazaar, and checked itself. Thank you.

## 3-minute cut (≈ 400 words · slides 1-2-3-4-6)

**1 · 0:00–0:20** We're Team 5: three humans, one laptop, seven-plus Claude Code sessions. Fifth on Friday, first since 12:35 today: 37.26, 3.09 ahead ⟳.

**2 · 0:20–1:00** The system is a control room. We set the limits. A Claude Code Chief of staff decides and logs every call with its evidence, and never touches the game. Only two processes write: the Operator for trades, the Duelist for duels. Fourteen daemons read; a separate column only checks. Git is the shared memory.

**3 · 1:00–1:50** Five beliefs our data broke. Dealer trades don't score gains, they only lose, so pages close through teams. An LLM deciding duels was too slow, 9.2 seconds, so code decides and Haiku writes: 57 of 68 closed. The "cap of 50" was a myth, disproved by our own logs. A trade with a rival pays them too, so we locked the lead. And a zero-fee market needed a first-trades bounty to get trades at all.

**4 · 1:50–2:20** Where the points came from: Duelist 6.75, Operator and bots 17.43, our market 13.08, of which 4.08 is above what a plain stall gets.

**6 · 2:20–2:55** We learned: code decides, the LLM talks; separate deciding, writing and checking; scoring is relative and a market needs its first trade. One more day: merge the Sunday duelist, switch on the broker, and gate every directive with a verifier. Three humans set the limits. Claude ran the bazaar, and checked itself. Thank you.

## Q&A, prepared (sources in brackets)

- **"Wasn't the v10 bounty paying for activity?"** It was paid in cards at ≤ our value, never cash above value, for the first five v10 trades, at most two per seller, and announced in the v10 ad. The Chief flagged the fair-play risk before Lucas approved it, and from 13:01 it refused sellers among our rivals. [directives 10:50, 13:01; team/lucas.md 11:37, 12:22]
- **"Where is the code?"** main, plus the Sunday duelist on branch `duelist-loop` (f57a002), which is not merged yet ⟳ (merge before 16:00 or name the branch in the submission). [git; docs/duelist-sunday-summary.md]
- **"What failed?"** The MAL page never closed (9 of 10). RET-11 sold at 240 scored 0: its value had risen to ≈ 227. Saturday dealer buys cost −21.5 neg_points. The cap belief kept the closer off for almost two hours. [impact.json; GAME.md; directives 12:22]
- **"Which models?"** Duelist: code policy, Claude Haiku 4.5 writes the messages, a Sonnet fallback. Analysts: scout on Sonnet 5.5, judge on Opus 5.5. The sessions are Claude Code. [`ps`; agents/analyst; __main__.py on duelist-loop]
- **"Why does the Chief never write?"** So that every write has one owner and every decision has a log line with evidence; the Operator holds the operator lock, and an arbiter in code gives a scored duel priority on the team's one accept per tick. [ORCHESTRATOR.md; tools/arbiter.py]
