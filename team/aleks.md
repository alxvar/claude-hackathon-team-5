# Aleks — duels

**Now:** Duels: Clock-Standing (`agents/duelist/`) verified offline and against Claude; next: live run in the practice duels (game hour 2.0, ~22:20) with full logging.

**Touches:** `agents/duels/`, duel endpoints only.

## Log (newest on top: `time · what · result · next`)

- Fri 21:25 · duelist checks: 14 offline tests pass; `probe` reads clock + schedule; `smoke` failed (`.env` had CLAUDE_API_KEY, engine reads ANTHROPIC_API_KEY; renamed locally), then works: Opus decision 6-10 s, ~$0.007/turn, `--days` OK · Sunday's 15 s tick leaves a 10 s budget, too tight for Opus · next: `run` live in the practice, then read the payload
