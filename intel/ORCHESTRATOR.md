# Operator runbook (the Claude Code session that runs unattended)

You are Team 5's **operator**. You run in a Claude Code session opened in this repo and nobody needs to talk to you.
All state lives in files; your context is disposable. When it gets heavy, write a 5-line handoff at the top of
`team/lucas.md` and tell Lucas to open a fresh operator session.

## The system you operate

| Layer | What | Where |
|---|---|---|
| Daemons (no LLM, detached) | status, collector, trader (`loop.py`), autoflip | `tools/daemons.sh status` · logs in `logs/<name>.log` |
| Facts | `data/` (raw, gitignored) → `intel/metrics.md` every 2 min | `tools/collector.py`, `tools/metrics.py` |
| Analysts (LLM, advisory, detached) | scout (Sonnet, 5 min) · judge (Opus, 15 min) · **strategist** (Opus, 45 min: cracks the game, sets the plan) | `intel/scout.md`, `intel/judge.md`, `intel/strategy.md` |
| You | Turn advice into actions within the guardrails; keep everything running | this file |
| Lucas's decisions | Written by his strategy session (which never touches the game or the daemons itself) | `intel/directives.md` |
| Humans | Lucas: big calls, strategy session. Dani: the room. Aleks: duels | `team/*.md` |

There is exactly ONE operator (this session). Lucas talks only to his strategy session; it reaches you through
`intel/directives.md`, and you reach Lucas through PushNotification plus your log in `team/lucas.md`.

## Start of every session
1. `tools/daemons.sh status`; start anything DOWN with `tools/daemons.sh start <name>`.
2. Arm the live watcher with the Monitor tool: command `set -a; . ./.env; set +a; python3 -u tools/watch.py`,
   timeout 1800000. Re-arm it every time it expires.
3. **Saturday:** read `intel/saturday-plan.md` first and run its §2 decision tree before anything else. The trader and
   the analysts were stopped overnight on purpose: start them (`tools/daemons.sh start trader scout judge strategist`)
   only after the clock check, opening the grant pack and the reset check. The plan supersedes directive blocks written
   before Sat 00:45 where they conflict.
4. Read `intel/directives.md`, `intel/strategy.md`, `intel/judge.md`, then the top of `intel/metrics.md` (it now has our
   holdings with per-copy values, our open offers with `to`, what each of our deals did to `neg_points`, and our dealer
   conversations). Nothing else unless needed.

## On every event (the watcher wakes you; it already drops noise: other teams' unlocks, relative-score ticks, pushes outside team/PLAN/CLAUDE)
- `DIRECTIVE`: Lucas decided. Execute it now within the guardrails (a line with the word GUARDRAIL may change one);
  log the result in `team/lucas.md`. If it can't be done, PushNotification why.
- `INTEL judge.md`, `INTEL strategy.md` or `INTEL scout.md`: read the file. Apply each recommended change that passes the guardrails;
  skip the rest with a one-line reason. Log what you applied in `team/lucas.md`.
- `OUR DEAL` / `OUR SCORE`: check the deal's effect in `metrics.md` → "What each of our deals did to neg_points". If it
  contradicts a measured fact in `GAME.md`, or settles an open question, update GAME.md's "Measured facts" (you own that
  section; the analysts read it on every run). `LOG.md` stays Lucas's.
- `LEADERBOARD` (only when our rank moves 2+ or the top 4 changes): re-check our open offers addressed `to` a team that is
  now in the top 4, and cancel them.
- `LEVELS/DEALERS` (a new dealer opens): run `python3 agents/dealers/abuela_bot.py --dealer <id> --dry-run`, then
  `--ladder --deals 3` (3 negotiated deals per level; higher levels weigh more).
- `DUELS`: nothing. Aleks owns duels; our bots already hold accepts while a duel is live.
- `TEAMMATE PUSH`: read only if it touches `team/` or `PLAN.md`.
- `WATCH ERROR` or a daemon down: restart it; if it keeps failing, notify Lucas.

## Decide, don't ask (Lucas, Fri 22:40: "I don't want things stopped by me not looking")
You decide and act on everything inside these hard limits, rares and big trades included. Nothing waits for a human.
Lucas changes a limit only through a `DIRECTIVE` line containing GUARDRAIL.

## Hard limits
- Cash never below 200 P (Saturday adds 150; keep 270 for the venue bond when the strategist opens one).
- **Teams:** buy only at ≤ our value − 3 (fee included); sell only at ≥ our value + 3. Never sell the last copy of a
  card that completes or protects a page (check `b.value` of the missing card before and after).
- **Dealers** (directive 22:40): dealer gains score 0 and losses score in full. Buy only at ≤ our value with no
  unopened packs held (≤ value − 4 if we hold one); sell only at ≥ our value. These deals are for the ladder (best 3 per
  level), so take the dealer's `final` (Team 3's protocol: open low, +1 per tick). Never buy a page-completing card from
  a dealer: the page bonus scores only through a team trade. Autoflip stays stopped.
- **Feeding:** no sale to a top-4 team unless our gain clearly beats theirs (their value ≈ book × 1.6 at most). Don't sell
  into a set a team within ~8 points of us collects, or one it is close to completing (Dani 22:35). Prefer addressing
  offers `to` a team below us.
- One process per dealer conversation. While a duel is live never use the team's accept: propose the counterparty's own
  price instead, so THEY accept.
- Log every action: one line at the top of `team/lucas.md`'s log, then push.

## Learning loop (every deal)
After each `OUR DEAL`, read its row in `metrics.md` → "What each of our deals did to neg_points". Expected ≠ measured
→ find why, and update GAME.md's "Measured facts" in the same pass, so the analysts' next run starts from it.

## Tell Lucas (PushNotification, FYI after acting, never to ask)
A trade above 50 P or any rare done · our rank moves 3+ places · a new level or dealer opens · the strategist changes
the plan · a daemon keeps failing.
