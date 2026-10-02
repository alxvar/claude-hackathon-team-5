# Aleks — duels

**Now:** Duels: Clock-Standing (`agents/duelist/`) goes live in the practice duels (game hour 2.0, ~22:20; 12 ticks, 6% decay, 6 at once) with Opus as strategist and Sonnet 5.5 as negotiator (backups + supervisor: `agents/duelist/supervise.sh`), every duel recorded in `docs/duels/`; after it: `review`, read `intel/judge.md`, push.

**Touches:** `agents/duelist/`, `docs/duels/`, duel endpoints only.

## Log (newest on top: `time · what · result · next`)

- Fri 22:20 · duelist live for the practice duels on this laptop (`.env` added, `uv sync` via `~/.local/bin/uv`): smoke OK (Opus + Sonnet 5.5 negotiator 2.5 s), probe OK, `supervise.sh --negotiator-model claude-sonnet-5-5` started 22:20:02, session read (12 ticks, decay 0.06, price) · running · next: watch the duels, then `review` and push `docs/duels/`
- Fri 22:09 · duelist fallbacks: backup model per role (Opus→Sonnet, Sonnet→Haiku; primary skipped 2 min after 2 failures), code fallback now concedes on a schedule and accepts their in-limit offer instead of restating forever, poll/payload errors no longer stop the loop, `agents/duelist/supervise.sh` restarts a dead process · 17 tests pass, live dry-run starts with both backups · next: practice via `supervise.sh --negotiator-model claude-sonnet-5-5`
- Fri 22:07 · smoke, faster negotiator: strategist (Opus) 4.4 s / 3.8 s + negotiator Sonnet 5.5 2.6 s ($0.005/turn) or Haiku 4.5 1.4 s ($0.005/turn); duels decide concurrently (one task each) · ~7 s with Sonnet, ~5 s with Haiku, both inside Sunday's ~10 s budget; Haiku is the fallback if the live turns run slower · next: `run --negotiator-model claude-sonnet-5-5` in the practice
- Fri 22:00 · duelist now keeps a record of every duel in the repo (`docs/duels/duel-<id>.json`: payloads, decisions with latency and cost, sends, refusals, final result), sweeps the done list every minute so a restart loses nothing, saves the feed's duel events (to unmask aliases) and our duel points; `review` writes one table · 15 tests pass, live sweep OK · next: practice duels, then `review` and push `docs/duels/`
- Fri 21:25 · duelist checks: 14 offline tests pass; `probe` reads clock + schedule; `smoke` failed (`.env` had CLAUDE_API_KEY, engine reads ANTHROPIC_API_KEY; renamed locally), then works: Opus decision 6-10 s, ~$0.007/turn, `--days` OK · Sunday's 15 s tick leaves a 10 s budget, too tight for Opus · next: `run` live in the practice, then read the payload
