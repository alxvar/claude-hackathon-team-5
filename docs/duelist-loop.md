# Branch `duelist-loop`: hot-reloaded params, the wave loop, a code-first policy (for Aleks, Sun 08:00)

_Builder, Sat night, on the Chief's brief. Nothing here changes a live duel until you choose it: with no
`run/duel_params.json` the duelist plays today's constants, and `--policy llm` (the default) is today's agent.
Full suite green on the branch._

## TL;DR

| # | What | Default effect | To use it |
|---|---|---|---|
| 1 | **Hot-reloaded params**: `run/duel_params.json`, re-read every tick, bounds-checked, logged | none (no file = today's constants) | write the file, or `tools/duel_loop.py approve` |
| 2 | **Wave loop**: `tools/duel_loop.py` summarises each closed wave, compares it with the Duel Lab simulator, proposes a params diff | none (read-only; never applies) | `python3 tools/duel_loop.py watch` on any machine with the records |
| 3 | **Code-first policy**: code decides accept / hold / step and the day; one capped model call writes the words | none (`--policy llm` stays the default) | `run --policy code --negotiator-model claude-haiku-4-5` |

## 1. Hot-reloaded params (`agents/duelist/params.py`)

- `SPEC` lists every tuning constant: where it lives (agent / runner / policy), bounds, and the simulator's key.
  Today's values are the defaults, read from the modules at start.
- The runner re-reads the file at start and on every new tick, and only when its mtime or size changed.
  - **Applying:** a valid set is applied by setting the module globals. Every function reads them at call time, so no
    other code changed.
  - **Logging:** every change is logged (`params: MAX_STEP_SHARE 0.25 -> 0.2` on the console, plus a `params` event
    in the JSONL log), and each new duel's record carries `params` (the overrides) and `policy`.
  - **Refusing:** a file with an unknown key, a non-number, a bound or cross-check failure
    (`MIN_STEP_SHARE <= MAX_STEP_SHARE`, `ACCEPT_BY <= DECIDE_LEFT`, …) or broken JSON changes **nothing**. The last
    good set stays and the console says why.
  - **Reverting:** deleting a key reverts it; deleting the file reverts all.
- Flags: `--params PATH` (or env `DUEL_PARAMS`), and `--no-params` for today's constants with nothing read.
- **The file is on the duelist's machine** (your checkout's `run/`). Run `approve` there, or point `--params` at a path
  you sync.
- One refactor, same behaviour: `runner.small_gap`'s literal `2.0` and `2` are now `SMALL_GAP_P` and
  `SMALL_GAP_ROUNDS`.
- The strategist prompt names some constants (`LATE_SWITCH_LEFT`, `DAY_SAME_SIDE_P`). A new value reaches the prompt
  of duels that start after it, and code rules at once.

## 2. The wave loop (`tools/duel_loop.py`)

_(filled in below when the build lands)_

## 3. Latency and the code-first policy (`agents/duelist/policy.py`)

**Profile** (docs/duels records, model decisions only):

| Session | n | mean | p50 | p90 | max | > 10 s | strategist | negotiator | 2nd negotiator call |
|---|---|---|---|---|---|---|---|---|---|
| Practice | 49 | 6.5 s | 6.1 | 8.1 | 14.2 | 4% | 4.1 s | 2.4 s | 4% |
| Duels I | 272 | 6.2 s | 6.0 | 7.1 | 14.5 | 1% | 4.0 s | 2.2 s | 3% |
| Duels II | 270 | **9.2 s** | 9.0 | 12.4 | 20.0 | **29%** | **6.9 s** | 2.4 s | **14%** |

**Diagnosis:**
- The strategist call is three quarters of the time.
- The negotiator's veto-and-retry adds a second call in 14% of Duels II decisions.
- At 15 s ticks the runner's budget is `max(8, tick − 5)` = 10 s, so about a third of Duels II's model moves would have
  become timeout fallbacks.

**`--policy code`:**
- Code decides the move; `respond_code`, then `policy.write`, makes **one** text call capped at `TEXT_TIMEOUT_S` (3.5 s).
- The guards check the words: no claims, no stray or past-limit numbers, no agreement words unless accepting.
- A bad, slow or failed text becomes code's plain words ("I can do 76 P."). There is never a retry.
- A hold makes no call at all.
- `final` checks the limit as always.
- The runner's code rules are untouched and still come first: deadline / small-gap accepts, the silent walk, the late
  day switch.

**Measured** (`smoke --policy code`, one call each):

| Text model | Latency | Result |
|---|---|---|
| Opus, low effort | 3.29 s, 3.16 s | words went out |
| Opus, low effort, first call | over 3.5 s | cut to plain words (likely a cold connection) |
| Haiku 4.5 | **1.77 s** | words went out |

So a code-first decision is code time plus at most 3.5 s, and about 2 s with `--negotiator-model claude-haiku-4-5`
(recommended). With Opus, consider `TEXT_TIMEOUT_S` 4.0 via the params file.

**The moves** (all tunable in `run/duel_params.json`):

| Move | Rule | Param (default) |
|---|---|---|
| Opener | this share of the limit away from it, **in price**, on our day | `OPENER_SHARE` 0.42 |
| Mid-duel step | this share of the gap, cut to `MAX_STEP_SHARE`, held below `min_step` | `CODE_STEP_SHARE` 0.12 |
| Last `CLOSING_TICKS` | this share of the gap | `END_STEP_SHARE` 0.5 |
| Accept | when theirs is worth at least ours (ratio below 1.0 = earlier), or within `ACCEPT_NEAR_P` of our step's landing | `ACCEPT_RATIO` 1.0 = off, `ACCEPT_NEAR_P` 2 P |
| The day | the day rules' call: take or give their day (give = worth up by its cost), else hold ours (a menu holds ours; the words may name theirs) | n/a |
| Floor | never past our limit on the day; never a price below this | `MIN_PRICE` 1 P |

The opener uses 0.42 because that was the Duels I median; Duels II's model opened at 0.51, and the simulator slightly
prefers lower.

**Evidence:**
- **Simulator** (`tools/duel_sim.py`, Sunday's 12 ticks at 10% decay, 6,000 duels a world, paired against today's
  model steps capped at 25%, all CIs ±0.003):

  | Code step | W1 | W2 | W3 | W4 |
  |---|---|---|---|---|
  | 12% (the default) | +0.008 | +0.010 | +0.010 | +0.009 |
  | 15% | +0.013 | +0.009 | +0.008 | +0.005 |
  | 20% | | | | loses |
  | 25% | | | loses | loses |

  The deal rate is unchanged and rounds fall about 0.1. `ACCEPT_RATIO` is neutral at 0.85+ and slightly worse at 0.75.
- **Replay of Duels II's 287 model decisions** through `code_move`:
  - Never past the limit, and never a price below 1 P.
  - Where both offered, code against the model, in worth to us: openers median −1 P (p10 −21, p90 +11); steps median
    +1 P (p10 −5, p90 +10).
  - The model accepted 10 offers that code wouldn't have: worth 62–93% of ours, with 3–7 ticks left, and all closed.
  - Code would offer in 57 of the model's 94 holds.
  - The first replay caught a bug, now fixed: a worth-based opener carried the seller's day bonus (`DayValues.offset`,
    up to 51 P at day 10) and opened at 67 on a 69 limit, or at −2 P.

**What it gives up:**
- The strategist reading the rival's words: bluffs, deadlines, a rival that states a floor.
- Using the scenario's market text for the opener.
- The model's earlier closes, which `ACCEPT_RATIO` can restore.

**First check if you try it:**
1. `uv run python -m agents.duelist run --dry-run --policy code --negotiator-model claude-haiku-4-5` on a live wave.
2. Watch `took_s` and the `text` meta (how often plain words replace the model's).

## Merge

```bash
git fetch && git checkout main && git merge --no-ff origin/duelist-loop   # after review; run all duelist tests first
```

Nothing on this branch touches a running process. A merged checkout behaves exactly as today until a params file
exists or `--policy code` is passed.
