# Branch `duelist-loop`: hot-reloaded params, the wave loop, a code-first policy (for Aleks, Sun 08:00)

_Builder, Sat night, on the Chief's brief. Items 1–3 change nothing until you choose them: with no
`run/duel_params.json` the duelist plays today's constants, and `--policy llm` (the default) is today's agent.
**Item 4 (the guards) is live once merged**, with an off switch (`{"GUARDS": 0}` in the params file). Full suite
green on the branch: 559 tests._

## TL;DR

| # | What | Default effect | To use it |
|---|---|---|---|
| 1 | **Hot-reloaded params**: `run/duel_params.json`, re-read every tick, bounds-checked, logged | none (no file = today's constants) | write the file, or `tools/duel_loop.py approve` |
| 2 | **Wave loop**: `tools/duel_loop.py` summarises each closed wave, compares it with the Duel Lab simulator, proposes a params diff | none (read-only; never applies) | `python3 tools/duel_loop.py watch` on any machine with the records |
| 3 | **Code-first policy**: code decides accept / hold / step and the day; one capped model call writes the words | none (`--policy llm` stays the default) | `run --policy code --negotiator-model claude-haiku-4-5` |
| 4 | **Guards on every offer** (6190): accept instead of offering worse; worth-monotonic steps; the day call on the first offer | **yes, once merged**: the last-ticks concession is capped at 25% of the gap | tune `MONO_END_SHARE` (0.5 = the simulator's preference); `{"GUARDS": 0}` turns all three off |

## Before Duels III: one param set (Chief 00:50)

- **Duels III starts with the Duel Lab's file**, simulated at its 12 ticks / 10% decay (intel/duel-lab.md, path A):
  `MIN_STEP_P` 5, `MAX_STEP_SHARE` 0.18, `LATE_SWITCH_LEFT` 2, `MONO_END_SHARE` 0.5. It's shipped as
  `docs/duels3-start.json`. Load it on the duelist's machine, validated and noted, with:
  `python3 tools/duel_loop.py approve --proposal docs/duels3-start.json --by Aleks`
- **The wave loop proposes only on sessions at 12 ticks / 10%.** Duels II's 16 / 8% waves get the summary and the
  simulator's comparison, never a proposal. The first proposal comes after wave 1 of Duels III, and it starts from the
  file above (the loop reads the params file as "today").
- The v2 runs on Duels II waves below are for reference only.

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

## 2. The wave loop (`tools/duel_loop.py`, on the Duel Lab's `tools/duel_sim_v2.py` and `tools/duel_gates.py`)

Plain `python3`, stdlib only. It reads the duelist's constants from the source files, so the checkout it runs in
defines "today". **Since 00:40 it runs on the Duel Lab's final simulator, `tools/duel_sim_v2.py`.** That simulator is
role-aware, models price plus delivery day, and is fitted on Duels II, with its five role-aware worlds `RW` and its
`POLICY_KEYS` mapping. The first, price-only copy is gone from the branch.
- The live duelist is modelled as the Duel Lab models it: the models' real closing steps, `switch_any`, and the 6190
  guards (`guard_worse`, `mono_end`) while `GUARDS` is on.
- With `--policy code` it models the code step instead.

```bash
python3 tools/duel_loop.py run --dry            # the latest closed wave: print only
python3 tools/duel_loop.py watch                 # every 60 s: a newly closed wave → intel/duel-loop.md
python3 tools/duel_loop.py approve --by Aleks    # THE one command: merge the proposal into run/duel_params.json
python3 tools/duel_loop.py approve --proposal intel/duel-loop.md --only MAX_STEP_SHARE --by Aleks   # after a pull
python3 tools/duel_loop.py revert --by Aleks     # back to today's constants
```

- **Waves:** grouped from `docs/duels` records. Within a session, duels are taken in start order and cut by
  `max_concurrent` (or the first tick's starts). A wave is closed once every duel in it has its final payload.
- **Summary:** deals, rounds, result vs surplus, decay lost, share (pie from the score jumps, when known), day outcomes
  and what the settled day cost, in-limit offers missed, and latency (model vs code, fallbacks).
- **Simulator comparison:**
  - It evaluates today's params, mapped to the simulator's keys, in the four worlds at the session's ticks and decay,
    and picks the world closest to the observed wave.
  - In that world it tries ±1 step on `MAX_STEP_SHARE`, `MIN_STEP_SHARE`, `HOLD_TICKS`, `SILENT_KEEP`, `ACCEPT_BY`
    and `OPENER_SHARE`. Each is paired against today.
  - It keeps only tweaks whose 95% CI is above 0 and that pass `params.validate` plus the cross-checks.
  - The best ones are proposed together if the set also wins.
- **The Duel Lab's live gates** (`tools/duel_gates.py`) on the session so far:
  - **REVERT** `MIN_STEP_P` → 3 when the deal rate with rivals that spoke is below 0.75 over ≥ 8 duels.
  - **STEP UP** `MIN_STEP_P` +1 (max 6) when rounds per deal > 3.5 with a deal rate ≥ 0.85.
  - A gate's diff joins the proposal and wins over a simulator tweak of the same name. It is still only applied by
    `approve`.
- **Never applied by itself.** `approve` validates, refuses on any error, writes atomically, and leaves a `_note`
  with the wave, time and approver.
- **Blocked moves:** `ACCEPT_BY` down is shown with its gain but never proposed. The simulator never has an accept
  refused, and at 1 no spare tick is left.
- **Latest real wave on v2** (Duels II wave 3.12, run at 00:40; **reference only**: Duels II's 16 / 8% now proposes
  nothing), closest world **R5** (more silent rivals and holders):
  - **The gate fired.** STEP UP: the session so far has 3.7 rounds per deal at a 0.89 deal rate, so `MIN_STEP_P`
    3 → 4. The simulator agrees: +0.006 ± 0.002.
  - **The combined proposal (+0.021 ± 0.003 a duel):** `MAX_STEP_SHARE` 0.22, `HOLD_TICKS` 2, `SILENT_KEEP` 0.2,
    `MIN_STEP_P` 4, `MONO_END_SHARE` 0.35, `LATE_SWITCH_LEFT` 3.
  - **Six changes at once is a lot.** 16 tweaks are tested at 95%, so expect about 0.8 false positives.
    `approve --only MIN_STEP_P` takes the one the live data supports, and you can add the rest after the next wave.
  - `ACCEPT_BY` 2 → 1 (+0.002) stays blocked.
- **Earlier, on the price-only v1 simulator** (Duels II wave 3.10, run tonight):

  | | Deal rate | Rounds | Score per duel |
  |---|---|---|---|
  | Observed, this wave | 0.83 | 3.6 | 0.18 (est.) |
  | Observed, session so far | 0.85 | 3.7 | 0.34 |
  | Closest world W3, predicted | 0.91 | 3.9 | 0.34 |

  - **Proposal: `MAX_STEP_SHARE` 0.25 → 0.22** (+0.0014 ± 0.0013 a duel). That runs against your "close faster"
    change, a40ced6, and is your call.
  - `ACCEPT_BY` 2 → 1 (+0.0077) is blocked.
  - Rule notes: decision p90 12.5 s is over the 10 s budget; a silent rival ended with no deal; 2 deals settled on a
    day costing us 15 P or more.
- **Honest limits:**
  - The simulator is price-only, and the world distances are close.
  - About 10 tweaks are tested at 95%, so expect about 0.5 false positives per run.
  - The share is known for only a few deals per wave.
  - Treat proposals as small nudges, not findings.

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
  | 20% | +0.015 | +0.008 | +0.004 | −0.002 |
  | 25% | +0.010 | +0.003 | −0.001 | −0.008 |

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

## 4. Guards on every offer (Chief 22:50, duel 6190): both policies

**What went wrong in 6190** (buyer, limit 143, each delivery day costs us 5 P):
- We stood at 116 on day 0 (worth 27).
- The late switch moved to their day: 66 on day 10, also worth 27.
- The model then offered **88 on day 10, worth 5**, as if the day were free: 22 P of worth in one step, 52% of the gap.
- The rival, standing at 108 on day 10 (worth −15), took it.
- It got through because the last `CLOSING_TICKS` are never cut.

**In `agent.guarded`, run by `final` on every offer from any path:**
1. **Accept instead of offering worse than theirs.** An offer worth no more to us than their standing offer (whole
   packages, days included, inside our limit) becomes an accept.
2. **Worth-monotonic concessions.** A package may never be worth less than our last sent one minus the normal step:
   `MAX_STEP_SHARE` of the gap mid-duel, and **`MONO_END_SHARE` (0.25) in the last ticks** (never less than
   `MIN_STEP_P`, never past their offer, never below our limit). The floor's price goes out on the drafted day, with
   code's plain text.
   - In 6190 the 88 on day 10 becomes **76 on day 10** (worth 17).
   - The fallback keeps its own schedule (exempt), so a duel still closes when the models fail.
3. **The day call on our first offer.** Take or give → their day (give adds what their day costs us); hold or menu →
   our best day. The strategist's band moves to keep its worth (`first_day`), and the code opener does the same.

**The cost, for your decision:** the guard caps the last-ticks concession at 25% of the gap. The simulator (Sunday's
12 ticks at 10%) finds big closing steps close deals:

| Capped at 25% in the last ticks | W1 | W2 | W3 | W4 | Deal rate |
|---|---|---|---|---|---|
| Code policy (its own last step is 0.5) | −0.004 | −0.012 | −0.012 | −0.010 | 0.90 → 0.87 |
| Today's model | +0.002 | −0.005 | −0.007 | −0.002 | |

Score per duel, against the same policy uncapped. The simulator is price-only, so it can't see 6190's day-accounting
error, which is what the guard is for. If you trust the simulator more, raise the cap from the params file:
`{"MONO_END_SHARE": 0.5}`. That keeps the guard against day errors while allowing half-gap closes.

Tests: `tests/test_duelist_policy.py`. They cover 6190's exact sequence on both paths, accept-instead (price and days),
and the first-offer day call. `tests/test_duelist.py`'s closing-tick case now expects the floor (122, not 115).

## Merge

```bash
git fetch && git checkout main && git merge --no-ff origin/duelist-loop   # after review; run all duelist tests first
```

Nothing on this branch touches a running process. After a merge and a restart:
- Items 1–3 behave exactly as today until a params file exists or `--policy code` is passed.
- Item 4's guards are on. `{"GUARDS": 0}` in `run/duel_params.json` turns them off within a tick, with no restart.

**Files** (11 commits on top of main):
- `agents/duelist/params.py` (new): the registry and the hot-reload.
- `agents/duelist/policy.py` (new): the code-first policy.
- `agents/duelist/prompts/text.md` (new): its text prompt.
- `agents/duelist/agent.py`: `respond_code`, `guarded`, `first_day`, constants.
- `agents/duelist/runner.py`: `reload_params`, the policy plumbing, `SMALL_GAP_*`.
- `agents/duelist/__main__.py`: `--policy`, `--params`, `--no-params`.
- `tools/duel_loop.py` (new), on main's `tools/duel_sim_v2.py` and `tools/duel_gates.py` (the Duel Lab's).
- Tests: `tests/test_duelist_params.py`, `tests/test_duelist_policy.py` and `tests/test_duel_loop.py` (new), plus one
  changed case in `tests/test_duelist.py`.
