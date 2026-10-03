# Running the duel agent

The duel agent is `agents/duelist/`, running on the model engine in `engine/`: regateo's Clock-Standing, copied over and adapted to the duel API. It doesn't depend on the regateo repo. The plan behind it is in [plan-clock-standing-on-bazaar.md](plan-clock-standing-on-bazaar.md).

## Setup (once)

1. Copy `.env.example` to `.env` and fill in `BAZAAR_KEY` and `ANTHROPIC_API_KEY`.
2. `uv sync` at the repo root (all commands below run from there)
3. `uv run pytest`: offline tests, with a fake model and a fake game.
4. `uv run python -m agents.duelist smoke`: one turn of a made-up duel through Claude. It prints the strategist's plan, the band, the move, and each call's latency and cost. It sends nothing to the game. Add `--days` to try a two-issue duel.

## The first duel (practice session, Friday at hour 2.0, about 21:00)

The schedule says the practice duels last 12 ticks, lose 6% per round, run 6 at a time, are price only, and don't score.

1. A few minutes before, run `uv run python -m agents.duelist probe`. It shows the clock, the duel sessions, and any live duels as raw JSON, and saves them to `logs/duelist/`.
2. When duels appear, start `uv run python -m agents.duelist run` and leave it running. It polls every 2 s while a duel is live (every 10 s, at most a third of a tick, while none is: the team key's 5 requests a second are shared) and decides for a duel (at most once per tick) when the rival has moved, on each of the last 3 ticks whatever the rival does, and when neither side has moved for 3 ticks after the rival's first offer (their offer unchanged, nothing sent by us; a rival repeating its offer has not moved). It sends at most one message per duel per tick. Every move is printed on one line: tick, duel, role, limit, the move, the band, and how long the decision took.
3. If the console says `can't read it` for a duel, the payload uses field names the adapter doesn't know. Open `logs/duelist/duels-*.jsonl`, find the `"event": "duel"` lines, and add the names to `agents/duelist/adapter.py` (`first(raw, ...)` lists). Ctrl-C and restart. Duels resume from the game's state.
4. Use `run --dry-run` to watch decisions without sending anything.

## Choosing the model

| Flag | Default | When to change it |
|---|---|---|
| `--model` | `claude-opus-5-5` | `claude-sonnet-5-5` if Opus is too slow for the tick |
| `--effort` | `low` | Opus 5.5 always thinks; `low` keeps a turn short |
| `--negotiator-model` | same as `--model` | `claude-sonnet-5-5` or `claude-haiku-4-5` for a faster second call |
| `--thinking-off` | off | Sonnet 5.5 only: no thinking at all (`between_tools`) |

Ticks are 60 s on Friday, 30 s on Saturday and 15 s on Sunday. A decision that takes longer than the tick minus 5 s is replaced by code's move (`agent.safe_move`, see Fallbacks). Check the decision times printed in the practice session before Sunday.

## Watching it live: the monitor

`~/.local/bin/uv run --project . python -m agents.duelist monitor`, then open http://127.0.0.1:8766 (`--port` for another; `--records <folder>` replays saved records). Read-only and keyless: it never touches the team key or the duelist, so it can run beside it on any laptop with the repo.

- **Live duels:** one card per duel: ticks left, our limit, both standing offers, the gap, rounds, what taking their offer would score now, a chart of both sides' offers against our limit, and the transcript with our decision under each of our messages (band, latency, cost, the strategist's read; tags for code rules: deadline, small gap, silent rival, their price) and the holds (decided, nothing sent).
- **Finished:** every duel of the session with result, price, points and rounds; click a row for its transcript. A deal or a no-deal pops a notice as it lands.
- **All duels in the game:** the game publishes other teams' duels only as they close (`duel.closed`: duel, item, deal or no deal; no teams, prices or messages), so the panel shows the session's progress, every closing as it comes, ours marked, and the deal rate by item, ours against the field's.
- The header says whether the duelist runs (the pid in `logs/duelist/run.lock` is alive), when it last wrote a record, its errors in the last 30 minutes, and the next duel session's tick and minutes away.
- Our duels come from `docs/duels/` as the duelist rewrites them (it trails the game by the duelist's 2 s poll); the field from the public feed every 5 s.

## Records: every duel, kept in the repo

`run` also writes one `docs/duels/duel-<id>.json` per duel: the session, how we read it, every raw payload, every decision (latency, cost, what the agent saw), what we sent and what the game answered, refusals, and the game's final payload. Once a minute it also sweeps the done list, so a duel that a crash or a restart missed is still saved (with the final payload only). Two timelines sit next to the records: `feed.jsonl` (the public feed's duel events, which may name the team behind an alias) and `scores.jsonl` (our duel points whenever they move).

After each session: `uv run python -m agents.duelist review` writes `docs/duels/README.md`, one row per duel (rival, role, limit, our first and last offer, price, the day in days duels, surplus, points (the game's `result`), `pred` (the result our own reading gives: it should equal points), decision seconds, spend, fallbacks). Then commit and push `docs/duels/`, so the team and the next session learn from it.

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

1. What the duel payload's real field names are, and what `deadline` means (a tick number or ticks left). **Answered:** `deadline_tick` is a tick number, the tick the duel closes on.
2. Whether there's a message list, and how our messages are marked. **Answered:** `messages`, ours `"from": "you"`.
3. Whether a "round" of decay is a tick or a message. **Answered:** a round is one message from each side, priced or not: `result` = our surplus × (1 − `decay_per_round`)^`rounds`, `rounds` = min(our messages, theirs). Friday's records suggested priced offers only (all our messages had a price); Saturday's practice 277 settled it: three no-price messages, three rounds. Sending nothing is the only free hold.
4. How the result is scored, and how the days weight looks (for Duels II, hour 13). Open: `your_days_weight` and `days_meaning` were null in the practice. What we do until we see them: see "Duels II: the delivery day" below.

## Safety rails in code

- We never offer or accept a price past our limit (`agent.final`), whatever the models say.
- We never write an amount past our limit in a message.
- An acceptance is dropped if the rival's offer changed while we were deciding.
- One acceptance per team per tick: a second one waits for the next tick.
- Code accepts a standing offer inside our limit without asking the models (`runner.closer`), price-only duels:
  - **deadline:** one per tick, earliest deadline first, then the bigger surplus, so every such offer is accepted by 2 ticks left (duel 181 lost 10.6 points by not accepting);
  - **small gap:** when their offer answers ours and the gap is at most max(2 P, 2d/(1−d) × our surplus), what one more round risks (duel 199: 97 against our 96).
- When our acceptance must wait (the team's one acceptance this tick is spent), we offer the rival its own price instead, so it accepts, but only when that adds no round (we have sent at least as many messages, priced or not) or on the last tick (`runner.their_price`).
- A hold sends nothing (`runner.is_hold`): a model move that is a message without a price, or an offer at our standing price and day, is logged as a hold and not sent. Practice 278: we answered Rival Oro's repeated 111 every tick, 10 rounds, 2.7 points instead of 4.7.
- When the strategist holds (its target is our standing offer, on our day), an offer the negotiator drafts a point or two off it is turned back into our standing offer (`agent.held`, rule "plan holds") and so not sent; an accept still goes through (Dani's 10:16 audit).
- Fewer rounds per deal (`docs/duelist-rounds-spec.md`): once both sides have offered, a concession smaller than max(3 P, ¼ of the gap in worth) is held (rule "small step"), and after 4 priced offers a concession is held unless their offer moved at least that much since our last one (rule "offer budget"). Accepts, the opener, the last 3 ticks and the code moves (close, their price, silent walk, fallback) are exempt. The ledger tells the strategist both numbers.
- A rival that repeats its standing offer (same price and day), or sends no price, has not moved (`runner.signature`): we don't answer it. The hold breaker counts ticks since their offer last changed, we sent, or we decided, so against a rival that repeats every tick it still fires every 3 ticks, and the strategist steps once or holds.
- A rival that has said nothing since our opener (price-only duels) is played by code, no model (`agent.silent_move`): from half the duel's ticks left, our offer walks in equal steps from the opener to a floor that keeps 30% of the opener's distance from our limit, reached 2 ticks before the end. Silence adds no round, so the steps cost price only. The moment the rival sends anything, the models take over. Example, 16 ticks, selling at cost 86 with opener 125: 122, 118, 114, 110, 106, 102, 98 over the last 8 to 2 ticks.
- One duelist per machine: `run` takes a lock (`logs/duelist/run.lock`); a second one exits with code 3 and `supervise.sh` stops. Across machines, the console prints `WARNING ... another duelist` when the game shows a priced message from our side this process didn't send.
- After a restart, our messages in the game count as sent: no re-sent offers (181 re-sent 50 and 54 on Friday).
- Decay and rounds come from the duel itself (`decay_per_round`, `rounds`); the session's name and ticks from the feed's `duels.scheduled`, never from the schedule (which lists only sessions still to come).
- Ticks left count the ticks we can still move on: the duel closes on its `deadline_tick`, so the last move is on the tick before.
- Days duels: limits on the whole package (price and day), never a priced message without a day, and code's rules only when we can read the day weight (see below).
## Duels II: the delivery day

Duels II settles a price and a delivery day from 0 to 10. Each side has a private weight per day (`your_days_weight`, explained by `days_meaning`), and a priced message without a day is refused (`missing_days`). Nobody has seen either field filled in yet, so `agents/duelist/days.py` reads the likely shapes into what each day is worth to us:

| The game sends | We read |
|---|---|
| a list of 11 numbers, or a dict keyed by day `"0"`..`"10"` | the value of each day |
| a number `w` and words with a direction ("each day later costs you 2") | `w` per day toward the days the words prefer; a cost word turns the direction around |
| a negative number | `w` × day: the early days are worth more |
| a positive number and no direction | a guess: each day counts at the worse of the early and late readings (best day 5) |
| `{"per_day": 2, "prefers": "early"}` or `{"best_day": 3, "per_day": 1.5}` | per day toward that direction, or away from that day |
| anything else | can't read it: limits on price alone and the models play the duel (as before) |

Every value is stated against our best day, so a day costs 0 or more. If the game counts the day as a cost, that is exact; if it counts it as a bonus, we are on the safe side by a constant.

What changes when the weight can be read:
- **Limits are on the whole package.** A deal's worth to us is the price's margin over our limit minus what its day costs us (`guards.worth`). The band is clamped to the limit on the strategist's day, `final` refuses any offer or acceptance worth less than nothing, and every priced move carries a day from 0 to 10.
- **The code rules cover days duels.** Deadline accept, small-gap accept (the gap in worth, days included), offering the rival its own package when our accept must wait, and the silent-rival walk (on price, our day kept).
- **The strategist sees the reading.** It gets the weight, the game's words, our reading, a table of what each day costs, and facts on what each side's day costs us. The negotiator sees none of it.
- **Our default day is our best day,** not day 5.

**At the first Duels II duel**, the console prints how we read the weight: `duel 7 vs ...: buyer, limit 100 P, ..., days: 2 per day (direction from the game's words): each day after day 0 costs you 2`. If it says `CAN'T READ`, or the direction looks wrong against `days_meaning` (in `logs/duelist/duels-*.jsonl`, `"event": "duel"`), fix `read_days` in `days.py`, add the payload to the tests, run them, restart. **After the first wave**, run `review`: for each deal, `pred` (our reading's result) should equal `points` (the game's `result`), as it does on all 11 of Friday's deals. A difference means the reading is off.

## Fallbacks, layer by layer

1. **A model fails or is slow:** each role has a backup model (`engine/failover.py`): Opus → Sonnet, Sonnet → Haiku, Haiku → Sonnet. The primary gets 20 s; after 2 failures in a row it is skipped for 2 minutes. `--no-failover` turns this off.
2. **Both models fail, or the decision runs past the tick minus 5 s:** code plays (`agent.safe_move`). It concedes a share of the gap toward our limit (or their offer, if better), a larger share as the clock runs out, and accepts their standing offer once it is inside our limit and within 2 P of that concession. On the last tick it offers our limit. It never goes past the limit.
3. **A bad payload or a failed read:** that duel or that poll is skipped and logged; the loop goes on.
4. **The process dies:** run it under the supervisor, which restarts it after 5 s. The game keeps each duel's messages and `docs/duels/` keeps our records, so it picks the duels up again:
   `agents/duelist/supervise.sh --negotiator-model claude-sonnet-5-5`
   It keeps the laptop awake (`caffeinate`) and uses `~/.local/bin/uv` (a pyenv shim named `uv` can shadow it and fail). Detached, so it outlives the terminal:
   `nohup agents/duelist/supervise.sh --negotiator-model claude-sonnet-5-5 >logs/duelist/supervise-$(date +%Y%m%d-%H%M).log 2>&1 </dev/null &`
   Stop it supervisor first, or it restarts the run: `pkill -f duelist/supervise.sh; pkill -f 'agents.duelist run'`. Check: `ps aux | grep agents.duelist`. A process started before Sat 08:05 has no lock: stop it before starting a new one.
5. **The duelist can't run at all:** `uv run python -m agents.duelist run --no-failover --model claude-haiku-4-5` from any team laptop with the `.env`. Only one duelist may run at a time (one key, one accept per tick).
