# Aleks — duels

**Now:** Duels: Clock-Standing (`agents/duelist/`) verified offline and against Claude; next: live run in the practice duels (game hour 2.0, ~22:20) with full logging.

**Touches:** `agents/duelist/`, `docs/duels/`, duel endpoints only.

## Log (newest on top: `time · what · result · next`)

- Fri 22:00 · duelist now keeps a record of every duel in the repo (`docs/duels/duel-<id>.json`: payloads, decisions with latency and cost, sends, refusals, final result), sweeps the done list every minute so a restart loses nothing, saves the feed's duel events (to unmask aliases) and our duel points; `review` writes one table · 15 tests pass, live sweep OK · next: practice duels, then `review` and push `docs/duels/`
- Fri 21:25 · duelist checks: 14 offline tests pass; `probe` reads clock + schedule; `smoke` failed (`.env` had CLAUDE_API_KEY, engine reads ANTHROPIC_API_KEY; renamed locally), then works: Opus decision 6-10 s, ~$0.007/turn, `--days` OK · Sunday's 15 s tick leaves a 10 s budget, too tight for Opus · next: `run` live in the practice, then read the payload
