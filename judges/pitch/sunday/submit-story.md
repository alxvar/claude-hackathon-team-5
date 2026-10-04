# /submit story · Team 5 (paste below the line; ⟳ = update at 15:00)

---

**Team 5: a control room of Claude Code sessions, where code decides and the LLM talks.**

**What we built.** Three humans set goals and hard limits. A Claude Code "Chief of staff" makes every call and logs it with its evidence in `intel/directives.md`, and never touches the game. Only two roles write to the game: the Operator (and the bots it starts) and the Duelist. Read-only daemons collect the feed, the score and the event stream; a separate check column (a verifier subagent, a duel simulator, analysts on the Claude API, contrarian reviews) audits big calls. Git is the shared memory: one owner per file.

**Why this way.** Our first duelist let an LLM decide: 9.2 s per reply, 29 % over 10 s, on a 15 s tick. The Sunday duelist lets code decide price and delivery day while Claude Haiku 4.5 only writes the words (≈ 2 s), with an 8 s failover and hot-reloaded parameters: 57 of 68 Duels III closed. Splitting deciding, writing and checking let us correct our own beliefs fast: the "cap of 50" on trade gains was refuted by our own logs in 1 h 51.

**Built around the Bazaar.** A club matchmaker, our market with more than two sides: it rebuilds every team's album from the public feed, matches one team's spare to another's missing card (page-closers first), prices halfway between both values and rotates hosting across members' markets. Plus a demand model of what every card is worth to every team (no LLM), a shared Neon archive, a Market Test recorder and offline broker simulator, a three-sided incentive (when two teams trade on our venue, the venue pays the seller in cards, settled at our value), sequenced page closers and Dani's live judges' showcase.

**Result.** #6 at Friday's final, #1 since 12:35 Sunday: 37.26, 3.09 ahead at 13:35 ⟳.

**One more day.** Merge the Sunday duelist and learn day weights per opponent; switch on the broker we staged; put a verifier gate on every directive.

**Where to look.** `judges/pitch/sunday/` (deck, architecture), `agents/duelist/` on main + the live Sunday duelist on branch `duelist-loop` @ f57a002, `tools/`, `hub/`, `dashboard/`, `intel/directives.md`, `LOG.md`.
