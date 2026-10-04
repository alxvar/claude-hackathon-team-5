# /submit story · Team 5 (paste below the line; ⟳ = update at 15:00)

---

**Team 5: a control room of Claude Code sessions, where code decides and the LLM talks.**

**What we built.** Three humans set goals and hard limits. A Claude Code "Chief of staff" makes every call and logs it with its evidence in `intel/directives.md`, and never touches the game. Only two processes write to the game: the Operator (trades, dealer bots) and the Duelist. Fourteen read-only daemons collect the feed, the score and the event stream; a separate check column (a fresh verifier subagent, a duel simulator, API analysts on Claude, contrarian reviews) audits plans before big calls. Git is the shared memory: one owner per file.

**Why this way.** Our first duelist let an LLM decide: 9.2 s per reply, 29 % over 10 s, and every exchange costs decay. The Sunday duelist lets code decide price and delivery day while Claude Haiku 4.5 only writes the words (≈ 2 s), with an 8 s failover and hot-reloaded parameters: 57 of 68 Duels III closed. Splitting deciding, writing and checking let us correct our own beliefs fast: the "cap of 50" on trade gains was refuted by our own logs in 1 h 51.

**Built around the Bazaar.** A club matchmaker, our market with more than two sides: it rebuilds every team's album from the public feed, matches one team's spare to another's missing card (page-closers first), prices halfway between both values and rotates hosting across members' markets. Plus a demand model of what every card is worth to every team (no LLM), a shared Neon archive, a Market Test recorder and offline broker simulator, a first-trades bounty paid in cards at no more than our value, and Dani's live judges' showcase.

**Result.** #5 on Friday, #1 since 12:35 Sunday: 37.26, 3.09 ahead at 13:35 ⟳.

**One more day.** Merge the Sunday duelist and learn day weights per opponent; switch on the broker we staged; put a verifier gate on every directive.

**Where to look.** `judges/pitch/sunday/` (deck, architecture), `agents/duelist/` on main + the live Sunday duelist on branch `duelist-loop` @ f57a002, `tools/`, `hub/`, `dashboard/`, `intel/directives.md`, `LOG.md`.
