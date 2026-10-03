# Duelist audit: branch `duelist-loop` (head d04a29f) before Duels III and the Final

_Independent audit, Sun 00:30, written for Aleks and Lucas. It is offline only: no live server, no API key, nothing
changed on main or on the branch. The work ran in a temporary worktree of `origin/duelist-loop`, since removed. The
replay scripts and outputs are in the session scratchpad (`replay.py`, `replay2.py`, `probes.py`, `probes2.py`,
`firstday.py`, `replay_lab.out`, `replay2.out`)._

## Verdict

**Merge: GO, with `--policy llm` (the default) and the Duel Lab file, after the two must-do items below.
`--policy code`: NO-GO until S1 is fixed.**

**Must do before 11:00:**
1. Bake the four Duel Lab values in as the code defaults, or check them at start (S3).
2. Choose how a timed-out decision falls back (S2). That risk exists on main as well, and it is the biggest one tomorrow.

## What checks out

- **Tests:** `uv run python -m pytest -q tests` on the branch gives **561 passed** (13 s).
- **Clean merge:** main has not changed `agents/`, `engine/` or the duelist tests since the merge base (73cb98d). The
  branch's `agents/duelist` code is identical to b10f9cc, the head the Duel Lab validated, except for comments.
- **The params file validates:**
  - `docs/duels3-start.json` passes through `tools/duel_loop.py approve`, written atomically to a scratch path.
  - `Params.reload()` then applies exactly `MIN_STEP_P 3→5`, `MAX_STEP_SHARE 0.25→0.18`, `LATE_SWITCH_LEFT 4→2` and
    `MONO_END_SHARE 0.25→0.5`, and the module globals change.
  - The Duel Lab's own JSON block validates too.
  - Bad values are refused: a bool, a non-integer for an int key, NaN, inf, out-of-bounds values and CROSS violations.
  - No module imports a tunable constant by value, so a hot reload reaches every reader.
- **Day reading, both roles:** `guards.worth` × (1 − d)^rounds reproduces **all 56 Duels II deal results** within
  0.1 P (29 seller deals, 27 buyer deals).
  - Buyer: the cost is w·day.
  - Seller: the bonus is w·day from day 0 (the `offset`).
- **Accept limits:**
  - Three of our accepts in one tick (1281: duels 5797, 5707 and 5809) all settled, so duel accepts aren't limited per
    team.
  - The SDK retries `rate_limited` three times.
  - The duelist uses about 1 request a second plus at most 4 sends a tick, so 4 duels at once fit the key's limit.
- **Simulator order:** `duel_sim_v2` takes the deadline accept before the late switch, as the runner does. So at
  `LATE_SWITCH_LEFT` 2 the switch fires only when their offer is outside our limit, in the simulator and live alike.
- **Code policy safety:** in the offline replay of the 514 Duels II decisions, the code policy never offered past the
  limit, never priced below 1 P, and never offered worse than their standing offer.

## Findings, by severity

### S1. `--policy code` retreats every turn on a "give" day call (code policy only)
- **The bug:** `policy.code_day` returns the premium `r.cost` on every turn while the call is "give" (policy.py:77).
  The call never changes once we are on their day. So each step adds the premium again
  (`price_at(v, target + premium, day)`, l.115), and `call != "give"` (l.110) also switches off the small-step hold.
- **Replay:** it moves away from the rival in **10 of 68 Duels II duels (38 decisions)**: 5622, 5707, 5860, 5964,
  6022, 6023, 6040, 6048, 6085 and 6191. For example:
  - 5860: 172→181 on day 0, then 169→180;
  - 6022: 81→67 on day 10, five times in a row.
- **Probe:** a buyer with a 100 limit and 1.2 per day opens at 34 on day 10, then offers 28, 22, 17 and 12 while the
  rival concedes.
- **The simulator can't see it:** its "give" is worth-neutral (`open_worth + 0 * C`, duel_sim_v2.py:229), and its code
  step has no premium.
- **Fix:** add the premium only when we are moving to their day now, and keep the hold once we are there.
  ```python
  # code_day
  if r.call == "give":
      return r.their_day, r.call, (r.cost if r.our_day != r.their_day else 0.0)
  # code_move
  if step < A.min_step(v, last, theirs) and not (call == "give" and last.days != day):
      return hold("code: small step")
  ```

### S2. At 15-second ticks, about 30% of model decisions time out, and the failover never engages (main and branch)
- **Latency:** the Duels II records hold 411 model decisions: mean **9.3 s**, p90 12.4 s.
  - **125 (30%) took over 10 s**, 78 over 11 s and 51 over 12 s.
  - The strategist alone averages 6.9 s (p90 9.95 s), and 62 of the 411 decisions made a second negotiator call.
  - At 15-second ticks the runner's budget is `max(8, tick − 5)` = **10 s** (runner.py:387).
- **What a timeout does:** it becomes `safe_move`, which never holds and is exempt from the worth floor.
  - So about 30% of turns ignore the new `MIN_STEP_P` 5 / 0.18 holds, and most of them add a round, at 10% decay.
  - The Duel Lab's +0.039 a duel assumes every decision is the model's; the simulator has no timeouts.
- **The failover can't help:** `Failover.timeout_s` is 20 s (failover.py:21, \_\_main\_\_.py:55), so the backup model
  is never asked inside a 10 s budget.
  - The runner's cancellation is a `CancelledError`, which `except (LLMError, TimeoutError)` (l.38) doesn't count. So
    the trip and its cooldown never fire either.
  - Probe: four timed-out turns in a row, failures still 0, backup calls 0.
  - During an Opus slowdown, then, every turn burns 10 s and falls back.
- **Fixes, cheapest first:**
  1. In `runner.decide`, on `TimeoutError` (and for a duel whose weight we can read), fall back to code that respects
     the holds: `policy.code_move(agent, obs)` with `policy.plain` words, after the S1 fix, instead of `safe_move`. A
     code hold then sends nothing.
  2. Count cancellations in `Failover`: `except asyncio.CancelledError: self.failures += 1; ...; raise`. Give the
     failover a budget below the decision's, for example `timeout_s=6`.
  3. Run with `--negotiator-model claude-haiku-4-5`: the negotiator is about 2.4 s today, and Haiku measured about
     1.8 s on the branch.
- **Watch** `took_s` and `FALLBACK(timeout…)` on the console in wave 1.

### S3. A missing params file silently plays the wrong set, and the loop can propose against the wrong baseline
- **A silent default:** `run/` is gitignored. A restart from another checkout or worktree, or a lost file, plays the
  code defaults with no warning.
  - Those defaults are the guards on with `MONO_END_SHARE` 0.25, `LATE_SWITCH_LEFT` 4 and `MIN_STEP_P` 3.
  - That set is the Duel Lab's "guarded baseline". The Lab puts it about 0.037 a duel below the file and about level
    with main: the file beats main by +0.033 to +0.040 and beats this baseline by +0.036 to +0.039.
  - At start the console prints only the path, not the values in force.
  - **Fix:** set the four values as the defaults in `agent.py` and keep the file for live tuning. Also print
    `params.overrides()` at start, and warn when the file is missing.
- **The wrong baseline:** `tools/duel_loop.py` evaluates "today" from the params file on the machine where it runs.
  - Run on a machine without the file, it reads `MIN_STEP_P` 3. The STEP UP gate then proposes 4, and `approve` on
    Aleks's machine, where the value is 5, would **lower** it to 4.
  - When `base_overrides` differs, `approve` only warns (duel_loop.py:956).
  - **Fix:** refuse unless `--force` when `evidence.base_overrides` differs from the current overrides. Run `watch` on
    the duelist's machine only.

### S3. The new settings would change, or hold back, the offers that 12 of 56 Duels II deals closed on
_This is the evidence risk, not a bug._ The replay put the models' real moves through the branch's `held()` and then
`guarded()`, at the file's settings (`replay2.out`):
- **Mid-duel holds:** 52 of 271 model offers become holds, because at `MIN_STEP_P` 5 / 0.18 nothing goes out under a
  ~28 P gap.
  - **7 of those 52 were the offers the deal closed on:** 5653, 5796, 5822, 5823, 5946, 6040 and 6141.
- **The closing floor raises 5 more closing offers:** 5616 (105→111), 5800 (88→93), 5893 (92→95), 6101 (75→80) and
  6190 (88→87).
- **What rides on it:** those 12 deals were worth 293 P of result. The gain depends on the simulator's belief that
  those rivals would have accepted a later or higher offer. We have no measurement of that.
- **The 6190 guard is almost inert at 0.5:** the gap is measured against a rival offer that was outside our limit on
  its day (worth −15), so half the gap is 21 P. Duel 6190's own step is cut by only 1 P. (6190 scored +3.6. At 0.25
  the guard would have sent 76 on day 10, which the rival's "108, último paso" suggests it would have refused.)
- **Mitigation:** the live gates are already built for this (`duel_gates`: revert `MIN_STEP_P` → 3 when the deal rate is
  below 0.75 over 8 duels). Run them after every wave and act on two waves.

### S3. In a days duel whose weight can't be read, the guards and the code policy treat the day as free
- **The cause:** when `day_values` is None, `worth()` ignores the day. The guards' first rule then accepts any offer
  that is better on price alone.
  - Probe: our offer is 62 on day 0; their 58 on day 10 is accepted, whatever day 10 costs us.
  - The code policy does the same on its own, from the opener to the accept.
  - The runner already leaves such duels to the models (`by_code`), but `final()` runs `guarded()` on every path.
  - It is harmless while Duels III keeps Duels II's wording ("costs you" / "adds … to your side"). It is the 6190
    failure enforced by code if the wording changes.
- **Fix:**
  - `guarded()` and `first_day()`: return early when `self.view.has_days and self.view.day_values is None`.
  - `respond_code`: use the model path for that duel.

### S3. Sellers can never offer below their nominal limit, even inside the limit on a bonus day (main and branch)
- **The cause:** `mentions_past_limit` checks amounts in the text on price only (guards.py:60), and `final()` blocks
  the whole move on it (agent.py:896).
  - Probe: a seller with limit 73 and 4.46 per day offers 70 on day 10, worth +41.6. `final()` turns it into "Let me
    think about that.", and the runner holds.
  - The same happens to the silent walk, the guard's floor price and the code policy's steps.
- **The cost:** duels 5816 and 6006 (silent rivals) froze for their last 4 ticks at 74 and 73 on day 10 and ended
  with no deal.
- **Fix:** don't flag the move's own price once `past_limit` has passed it. For example, filter out
  `p.value == move.price` in `final()`, or compare against `price_at(view, 0, move.days)`.

### S3. `first_day` changes 12 of the 68 real openers, and its "give" isn't the one the simulator played
- **Menu calls:** on a menu call it forces our best day even when the model chose their day.
  - 10 of the 12 changes were menu calls. In 9 of those 10 the model had opened on their day.
  - **8 of the 10 deals settled on their day:** 5796 (40.6), 5822 (33.0), 5809 (28.8), and also 5653, 5827, 5893,
    6049 and 6176.
  - Our day is then held until the late switch, now at 2 ticks left.
- **Give calls:** `first_day` adds a premium of C in worth (agent.py:880), so the price moves by 2C. The simulator's
  first-day give is worth-neutral.
  - In 5622 the opener moved 135 on day 5 → 157 on day 0 (seller, limit 83), and the duel ended with no deal.
- **Fix:** match the simulator: `extra = 0.0` for give. Consider leaving the model's day on a menu call; only the
  "hold" call needs our end.

### S4. Smaller issues
- **The floor's price can fall below 1 P.** On a costly day the floor goes to ≤ 0 (6095: −2 on day 10), and `final()`
  then turns it into `safe_move`.
  - Fix: as `held()` does, recompute on our last day when the price is below 1.
- **The first guard can accept a near-zero offer.** When the drafted move is itself past our limit, the first rule
  accepts any in-limit standing offer, even one worth about 0 mid-duel.
  - Fix: require `worth(move) >= 0` before converting.
- **The code policy's accept makes a text call it never sends.** `duel_accept` posts no text, and the call delays the
  accept by up to 3.5 s, which leaves more time for the rival's offer to change.
  - Fix: in `respond_code`, set the text to "Agreed." and skip `write()` for accepts.
- **The accept race (main too).** `POST /accept` takes the rival's offer as it stands at that moment.
  - Fix: compare the result's `price` with `move.price` and log any mismatch. Ideally re-read the duel just before
    the POST.
- **Restarts and the late switch.** `switched` isn't restored on a restart, and code doesn't stop a flip back to our
  day after the late switch (6190: 66 on day 10, then 122 on day 0).
  - Fix: block a change of day after `switched` (or after our last offer on their day) in `final()`.
- **An untested combination.** The code policy at `MIN_STEP_P` 5 holds under a ~42 P gap mid-duel (0.12 × gap < 5).
  That combination was never simulated.

## Can the loop switch between 2-3 sets Aleks approves in advance, by a rule after each wave, with no human present?

**Not as built. The change that makes it safe is small, about 80 lines plus one line in the runner.**

**What a hot reload does to duels already in progress:** it applies to them at their next decision.
- How it works:
  - The runner re-reads `run/duel_params.json` on every new tick (`reload_params`, keyed on the file's mtime and size)
    and sets the module globals.
  - Every rule reads those globals when it runs: holds, caps, the worth floor, the accept and deadline rules, the
    silent walk, the late switch.
  - Nothing is fixed per duel.
- Three side effects:
  1. **The prompts don't change.** The strategist's system prompt is written when the duel starts, and it states
     `LATE_SWITCH_LEFT` and `DAY_SAME_SIDE_P` (agent.py:446-454). A duel already running keeps the old numbers in its
     prompt while code plays the new ones. The facts sent each turn (`MIN_STEP_P`, `MAX_STEP_SHARE`, `CLOSING_TICKS`,
     the day rank) are current.
  2. **The records misattribute.** A duel's record stores `params` once, when the duel starts (runner.py
     `update`). A change in the middle of a duel shows only in the JSONL `params` event, so the wave loop scores that
     duel under the wrong set. A rule that switches on wave results then learns from mislabelled data.
  3. **One decision can mix the old and new values.** A decision waiting on a model call can read the old values
     before the await and the new ones after it, for example the ledger says `MIN_STEP_P` 5 and `held()` uses 6.
     This is harmless.
- **Safety holds whatever the set.** No tunable can push us past our limit: `final()` checks `past_limit`, a price of
  at least 1 P, the day 0-10 and amounts in the text, and none of those checks reads a param. Every key is
  bounds-checked, and a bad file changes nothing.

**Why it isn't ready to run without a human:**
- **Nothing applies on its own.** `run` and `watch` only propose, and `approve` is a manual command.
- **Calling `approve` from a cron would be unsafe:**
  - It **merges** the proposal into the file (`{**existing, **chosen}`), so a key from set B stays after a switch back
    to A.
  - It accepts any value within the bounds, not just a list of approved sets.
  - On a changed baseline it only warns (S3).
  - `watch` reads the params file of the machine it runs on.
- **There is no quiet moment between waves.** In Duels II, starts rolled after the first two waves, never more than
  15 ticks apart, and each duel lasted 16. So from tick 1239 to tick 1402 at least one of our duels was live on
  every tick (the records' deadlines). A wave counts as closed only once all its duels have
  finished, and by then the next wave is already playing. A switch therefore always lands in the middle of some duels.
- **One wave is noise.** With 4 duels, a single no-deal reads 0.75. The Duel Lab's own gates wait for at least 8 duels
  with a rival that spoke.

**The smallest safe change:**
1. **A list of approved sets.** Add `duel_loop.py approve-sets --file run/duel_sets.json --by Aleks`, which Aleks runs
   once before 11:00.
   - The file holds `{"A": {...}, "B": {...}, "safe": {...}}`, and each set is complete: every set lists the same
     keys.
   - Each set is checked with `params.validate` and the CROSS rules, and the file is stamped with the approver.
   - Allow sets to differ only in keys that are safe to change mid-duel: `MIN_STEP_P`, `MAX_STEP_SHARE`,
     `MIN_STEP_SHARE`, `MONO_END_SHARE`, `HOLD_TICKS` and `SILENT_KEEP`. Keep the keys the prompt states, and the
     clock keys (`LATE_SWITCH_LEFT`, `DAY_SAME_SIDE_P`, `CLOSING_TICKS`, `DECIDE_LEFT`, `ACCEPT_BY`), identical
     across sets.
2. **A switch command.** Add `duel_loop.py switch --every 15`, run **on the duelist's machine**, where the records
   are local and fresh. On each newly closed wave it:
   - runs a fixed, cumulative rule: the `duel_gates` rules mapped to set names (the REVERT gate → "safe", STEP UP → "B",
     otherwise stay);
   - requires at least 8 duels since the last switch and at most one switch per two waves, and never goes back to a
     set it just left;
   - writes `run/duel_params.json` **as a full replacement** of exactly one named set, with `write_atomic` and a
     `_note` naming the set, wave, rule and evidence; it never merges;
   - does nothing, with a warning, if the current file isn't one of the approved sets (someone edited it by hand);
   - honours a kill switch (`run/duel_switch.off`, or `--dry`) and logs each switch to `intel/duel-loop.md`.
3. **Record the set on every decision.** Add `"params": self.params.overrides() if self.params else None` to the
   `decisions=[{...}]` record (runner.py:412), and have the loop label each duel by the set it played most of its
   ticks under. This replaces true per-duel pinning, which would mean moving roughly 30 global reads into a
   per-agent snapshot: not a change for Sunday morning. Since the safe keys only move thresholds, applying a switch in
   the middle of a duel is acceptable once it is recorded.

**Without that change:** keep switching by a human. Pre-write the 2-3 sets as proposal files like
`docs/duels3-start.json`, so a switch is one command: `approve --proposal docs/<set>.json --by Aleks`.
- **List the same keys in every set.** `approve` merges, so it then overwrites every key and nothing from the old set
  remains.
- **Don't `revert` first:** the defaults could play for a tick in between.

## Offline replay (Duels II, 68 duels, 514 decisions, at the Duel Lab file's settings)

The records are at 16 ticks and 8% decay, not Sunday's 12 / 10%. Each decision is a one-step counterfactual on the
real history.

| Path | Result |
|---|---|
| Code policy (the runner's order: closing → switch → silent → `code_move` → `final`) | 225 steps, 126 small-step holds, 68 openers, 50 silent-walk steps, 31 accepts, 6 late switches; **38 give retreats in 10 duels (S1)**; 7 blocked seller offers turned into holds (5816, 6006: S3) |
| Guards on the models' real moves (`guarded` only) | 27 worth floors, 4 accept-instead. In 5618 their 46 on day 0 (worth 4) beat our 23-24 on day 5 (worth 2), and the duel ended with no deal under that night's day reading. Today's main would take it at 2 ticks left; the guard takes it at 3. |
| `held` + `guarded` at the file's settings | 193 unchanged, 52 holds, 12 floors, 11 caps, 3 accepts; 12 closing offers touched (S3) |
