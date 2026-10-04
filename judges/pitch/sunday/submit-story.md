# /submit story · Team 5 (paste below the line · FINAL numbers, 15:00)

---

**Team 5: a control room of Claude Code sessions, where code decides and the LLM talks.**

**What we built.** Three humans set goals and hard limits. A Claude Code "Chief of staff" makes the big calls and logs them with their evidence in `intel/directives.md`, and never touches the game. Only two roles trade: the Operator (and the bots it starts) and the Duelist; the Market session only posts our venue's ads. Read-only daemons collect the feed, the score and the event stream; a separate check column (a verifier subagent, a duel simulator, analysts on the Claude API, contrarian reviews) audits big calls. Git is the shared memory: one owner per file.

**Why this way.** Our first duelist let an LLM decide: 9.2 s per reply, 29 % over 10 s, on a 15 s tick. The Sunday duelist lets code decide price and delivery day while Claude Haiku 4.5 only writes the words (≈ 2 s), with an 8 s failover and hot-reloaded parameters: 57 of 68 Duels III closed. Splitting deciding, writing and checking let us correct our own beliefs fast: the "cap of 50" on trade gains was refuted by our own logs in 1 h 51.

**Built around the Bazaar.** A club matchmaker, our market with more than two sides: it estimates every team's album from the public feed and shared want-lists, matches one team's spare to another's missing card (page-closers first), prices between both values so both sides gain, and is designed to rotate hosting across members' markets. Plus a demand model of what every card is worth to every team (no LLM), a shared Neon archive, a Market Test recorder and offline broker simulator, a live reactor on the public event stream, sequenced page closers (one addressed bid at a time) and Dani's live judges' showcase.

**Result.** #6 at Friday's final; #3 and 7.09 behind Team 10 at Saturday's close; #1 from 12:35 Sunday to the close: **37.73, 1.97 ahead of Team 10** (the game's 60; the judges' 40 not included). Duels III closed 57 of 68 deals (84 %), the Grand Final 27 of 34 (79 %), both above the field.

**One more day.** Merge the Sunday duelist into main; switch on the broker we staged; put a verifier gate on every directive.

**Where to look.** `judges/pitch/sunday/` (deck, architecture), `agents/duelist/` on main + the live Sunday duelist on branch `duelist-loop` @ f57a002, `tools/`, `hub/`, `dashboard/`, `intel/directives.md`, `LOG.md`.
