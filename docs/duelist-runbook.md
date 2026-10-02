# Running the duel agent

The duel agent is `agents/duelist/`, running on the model engine in `engine/`: regateo's Clock-Standing, copied over and adapted to the duel API. It doesn't depend on the regateo repo. The plan behind it is in [plan-clock-standing-on-bazaar.md](plan-clock-standing-on-bazaar.md).

## Setup (once)

1. Add `ANTHROPIC_API_KEY=...` to the repo's `.env`, next to `BAZAAR_KEY` (see `.env.template`).
2. `uv sync` at the repo root (all commands below run from there)
3. `uv run pytest`: offline tests, with a fake model and a fake game.
4. `uv run python -m agents.duelist smoke`: one turn of a made-up duel through Claude. It prints the strategist's plan, the band, the move, and each call's latency and cost. It sends nothing to the game. Add `--days` to try a two-issue duel.

## The first duel (practice session, Friday at hour 2.0, about 21:00)

The schedule says the practice duels last 12 ticks, lose 6% per tick, run 6 at a time, are price only, and don't score.

1. A few minutes before, run `uv run python -m agents.duelist probe`. It shows the clock, the duel sessions, and any live duels as raw JSON, and saves them to `logs/duelist/`.
2. When duels appear, start `uv run python -m agents.duelist run` and leave it running. It polls every 2 s, makes one decision per duel whenever the rival has moved, and sends at most one message per duel per tick. Every move is printed on one line: tick, duel, role, limit, the move, the band, and how long the decision took.
3. If the console says `can't read it` for a duel, the payload uses field names the adapter doesn't know. Open `logs/duelist/duels-*.jsonl`, find the `"event": "duel"` lines, and add the names to `agents/duelist/adapter.py` (`first(raw, ...)` lists). Ctrl-C and restart. Duels resume from the game's state.
4. Use `run --dry-run` to watch decisions without sending anything.

## Choosing the model

| Flag | Default | When to change it |
|---|---|---|
| `--model` | `claude-opus-5-5` | `claude-sonnet-5-5` if Opus is too slow for the tick |
| `--effort` | `low` | Opus 5.5 always thinks; `low` keeps a turn short |
| `--negotiator-model` | same as `--model` | `claude-sonnet-5-5` or `claude-haiku-4-5` for a faster second call |
| `--thinking-off` | off | Sonnet 5.5 only: no thinking at all (`between_tools`) |

Ticks are 60 s on Friday, 30 s on Saturday and 15 s on Sunday. A decision that takes longer than the tick minus 5 s is replaced by restating our last offer. Check the decision times printed in the practice session before Sunday.

## What to read in the log after the practice

`logs/duelist/duels-<time>.jsonl` has one JSON object per line:

| Event | What it holds |
|---|---|
| `session` | The duel session's parameters from the schedule (decay, ticks, issues) |
| `duel` | Each duel's raw payload whenever it changed. This is the documentation we don't have. |
| `new_duel` | How we read the duel, and both rendered system prompts |
| `decision` | What the agent saw, the plan, the band, the move, vetoes, each model call's latency and cost |
| `sent`, `send_error` | What the game answered |
| `finished` | The duel as the done list shows it, with the result |

Questions to answer from it, before the scored Duels I on Saturday (hour 6.5, 16 ticks):

1. What the duel payload's real field names are, and what `deadline` means (a tick number or ticks left).
2. Whether there's a message list, and how our messages are marked.
3. Whether a "round" of decay is a tick or a message.
4. How the result is scored, and how the days weight looks (for Duels II, hour 13).

## Safety rails in code

- We never offer or accept a price past our limit (`agent.final`), whatever the models say.
- We never write an amount past our limit in a message.
- An acceptance is dropped if the rival's offer changed while we were deciding.
- One acceptance per team per tick: a second one waits for the next tick.
- If the models fail or time out, we restate our last offer.
