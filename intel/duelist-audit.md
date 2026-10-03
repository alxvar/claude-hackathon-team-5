# Duelist audit: branch `duelist-loop` (head d04a29f) before Duels III and the Final

_Independent audit, Sun 00:30-01:00, written for Aleks and Lucas._
- _**Scope:** offline only. No live server, no API key, nothing changed on main or on the branch. The work ran in a
  temporary worktree of `origin/duelist-loop`, removed when it was done._
- _**Sources:** the replay scripts and outputs are in the session scratchpad (`replay.py`, `replay2.py`, `probes*.py`,
  `firstday.py`, `replay_lab.out`, `replay2.out`)._
- _**Checked:** an independent verifier pass audited this file against the code and those outputs. Its 9 minor flags
  are fixed here._
- _**Reconciled with the Duel Lab's SUNDAY v2 (00:35)**, which recommends either the "v2" set (`MIN_STEP_P` 8,
  `MAX_STEP_SHARE` 0.12, `LATE_SWITCH_LEFT` 0, `OPEN_WAIT` 0, `MONO_END_SHARE` 0.25) or the "SAFE" set (5 / 0.18 / 2,
  `MONO_END_SHARE` 0.25). Both validate on d04a29f; I re-checked them._

## Verdict

**Merge: GO, with `--policy llm` (the default) and the params set Aleks picks (SAFE or v2), after the must-do items
below. `--policy code`: NO-GO until S1 is fixed and openers are set per role.**

**Must do before 11:00:**
1. **Make the chosen set the code defaults**, or at least warn loudly when the params file is missing (S3: `run/` is
   gitignored, and a missing file silently plays the old constants).
2. **If v2 is chosen, fix the strategist prompt at `LATE_SWITCH_LEFT` 0** (S3). The prompt would tell the model "with
   0 ticks left … your system offers their day", a move that never happens.
3. **Make the timeout fallback a deliberate choice** (S3). About 30% of model decisions would time out at 15-second
   ticks, and the backup model never engages.

## What checks out

- **Tests:** `uv run python -m pytest -q tests` on the branch gives **561 passed** (13 s).
- **Clean merge:** main has not changed `agents/`, `engine/` or the duelist tests since the merge base (73cb98d).
  `git diff b10f9cc d04a29f -- agents/` shows comment-only changes.
- **The params files validate:**
  - `docs/duels3-start.json` passes through `tools/duel_loop.py approve` (to a scratch path), and `Params.reload()`
    applies exactly its four changes to the module globals.
  - The Duel Lab's SAFE and v2 sets pass `params.validate` and the CROSS rules.
  - Bad values are refused: a bool, a non-integer for an int key, out-of-bounds values and CROSS violations. NaN for an
    int key raises inside `validate` instead (see S4); the effect is still that nothing is applied.
  - No module imports a tunable constant by value, so a hot reload reaches every reader.
- **Day reading, both roles:** `guards.worth` × (1 − d)^rounds reproduces **all 56 Duels II deal results** within
  0.1 P (29 seller deals, 27 buyer deals).
  - Buyer: the cost is w·day.
  - Seller: the bonus is w·day from day 0 (the `offset`).
- **Accept limits:**
  - Three of our accepts in one tick (1281: duels 5797, 5707 and 5809) all settled, so duel accepts aren't limited per
    team.
  - The SDK retries `rate_limited` three times.
  - The duelist polls 2 reads every 2 s and sends at most one message per duel per tick.
- **Simulator order:** `duel_sim_v2` takes the deadline accept before the late switch (l.201, then l.245), as the
  runner does.
- **Code policy safety:** in the offline replay of the 514 Duels II decisions, the code policy never offered past the
  limit, never priced below 1 P, and never offered worse than their standing offer.

## Findings, by severity

### S1. `--policy code` retreats every turn after a "give" day call (code policy only)
- **The bug:** `policy.code_day` returns the premium `r.cost` on every turn while the call is "give" (policy.py:77).
  The call doesn't depend on our day, so it never changes once we are on their day. Each step then adds the premium
  again (`price_at(v, target + premium, day)`, l.115), and `call != "give"` (l.110) also switches off the small-step
  hold.
- **Replay:** after the move to their day, it moves away from the rival in **9 Duels II duels (34 decisions)**: 5707,
  5860, 5964, 6022, 6023, 6040, 6048, 6085 and 6191. For example:
  - 5860: 172→181 on day 0, then 169→180;
  - 6022: 81→67 on day 10, four times in a row.
  - Four more flagged decisions were the intended first move to their day, and are left out of that count.
- **Probe:** a buyer with a 100 limit and 1.2 per day opens at 34 on day 10, then offers 28, 22, 17 and 12 while the
  rival concedes.
- **The simulator plays it differently:** its give is worth-neutral (`open_worth + 0 * C`, duel_sim_v2.py:229).
- **Fix (one policy for both paths):** play the give worth-neutral, as it was simulated, and keep the hold once we
  are on their day.
  ```python
  # policy.code_day
  if r.call == "give":
      return r.their_day, r.call, 0.0
  # policy.code_move
  if step < A.min_step(v, last, theirs) and not (call == "give" and last.days != day):
      return hold("code: small step")
  # agent.first_day (see the S3 first_day finding)
  extra = 0.0
  ```
  If you keep the strategist's premium of about C (prompt rule 3) instead, apply it in both paths, and only on the
  move to their day.
- **A second defect in the same policy (Duel Lab v2):** the single `OPENER_SHARE` 0.42 opens sellers far too low. The
  models' median seller opener is 0.73 × the limit, and the buyer median 0.37. Set it per role before any
  code-first use.

### S2. Hot-reload sets: a missing file goes silent, the loop can use the wrong baseline, and v2 breaks a prompt line
- **The missing file:**
  - `run/` is gitignored. A restart from another checkout or worktree, or a lost file, plays the code defaults with
    no warning: the guards on with `MONO_END_SHARE` 0.25, `LATE_SWITCH_LEFT` 4 and `MIN_STEP_P` 3.
  - The Duel Lab puts that "guarded baseline" about 0.037 a duel below the chosen set.
  - When the file exists, the overrides are printed at start (`params: K old -> new`). **Only a missing file is
    silent.**
  - **Fix:** make the chosen set the defaults in `agent.py` / `runner.py`. Failing that, have `run()` warn when
    `params.path` doesn't exist.
- **The wrong baseline:** `tools/duel_loop.py` evaluates "today" from the params file on the machine where it runs.
  - Run on a machine without the file, it reads `MIN_STEP_P` 3. The STEP UP gate then proposes 4, and `approve` on
    Aleks's machine, where the value is 5, would **lower** it.
  - When `base_overrides` differs, `approve` only warns (duel_loop.py:956).
  - **Fix:** refuse unless `--force`, and run the loop on the duelist's machine only.
- **The prompt at `LATE_SWITCH_LEFT` 0 (the v2 set):** `days_guide` (agent.py:454) then tells the strategist "with 0
  ticks left and the days still apart, it offers their day…". In code the switch is off (`ticks_left > 0` always).
  - The model may hold its day, waiting for a switch that never comes.
  - **Fix:** omit that sentence when `LATE_SWITCH_LEFT` is 0. Better still, don't state the number at all, which also
    helps with hot switches (see the switching section below).

### S3. Latency at 15-second ticks: about 30% of model decisions time out, and the failover never engages (main and branch)
- **Latency:** the Duels II records hold 411 model decisions: mean **9.3 s**, p90 12.4 s.
  - **125 (30%) took over 10 s**, 78 over 11 s and 51 over 12 s.
  - The strategist alone averages 6.9 s, and 62 of the 411 decisions made a second negotiator call.
  - At 15-second ticks the runner's budget is `max(8, tick − 5)` = **10 s** (runner.py:387).
- **What a timeout does:** it becomes `safe_move`, which never holds and is exempt from the worth floor.
- **What it costs:** the Duel Lab's v2 model puts this at about **−0.005 a duel at 31% fallbacks**, and −0.008 to
  −0.010 at 67% (Opus at 8-14 s). That is modelled [L], so it is a real but modest cost.
- **The failover can't help:** `Failover` keeps its default `timeout_s` of 20 s (failover.py:21; \_\_main\_\_.py:55
  passes 20 s only to the backup), so the backup model is never asked inside a 10 s budget.
  - The runner's cancellation is a `CancelledError`, which `except (LLMError, TimeoutError)` (l.38) doesn't count. So
    the trip and its cooldown never fire either.
  - During an Opus slowdown, every turn burns 10 s and falls back.
- **Fixes:**
  1. Count cancellations in `Failover`: `except asyncio.CancelledError: self.failures += 1; ...; raise`. Give it a
     budget below the decision's, for example `timeout_s=6`.
  2. Run with `--negotiator-model claude-haiku-4-5`: about 1.8 s against 2.4 s.
  3. Optionally, on a timeout, fall back to a code move that respects the holds instead of `safe_move`. This only
     comes after the S1 fix and per-role openers, since it routes about 30% of decisions through the code policy.
     The Duel Lab v2 simulated code-first steps with per-role openers at 0.388 (SAFE), against 0.381 for the models'
     steps.

### S3. The new settings would change, or hold back, the offers that 12 of 56 Duels II deals closed on
_This is the evidence risk, not a bug. It is measured at the earlier 0.5 file; the SAFE set holds the same and floors
harder, and v2 holds far more._ The replay put the models' real moves through the branch's `held()` and then
`guarded()`:
- **Mid-duel holds:** 52 of 271 model offers become holds. **7 of those 52 were the offers the deal closed on:** 5653,
  5796, 5822, 5823, 5946, 6040 and 6141.
- **The closing floor raises 5 more closing offers:** 5616 (105→111), 5800 (88→93), 5893 (92→95), 6101 (75→80) and
  6190 (88→87).
- **A 13th deal (6094)** has its closing offer turned into an accept at the same price, which is no worse for us. It
  is left out of the 12.
- **What rides on it:** those 12 deals were worth 293 P of result. The gain depends on the simulator's belief that
  those rivals would have accepted a later or higher offer.
- **The 6190 guard at 0.5 is almost inert:** the gap is measured against a rival offer that was outside our limit
  (worth −15), so 6190's own step is cut by only 1 P. This supports the Lab's v2 move to 0.25.
- **Mitigation:** run the 8-duel gate (deal rate below 0.75 → step back v2 → SAFE → today) on two waves.

### S3. In a days duel whose weight can't be read, the guards treat the day as free
- **The cause:** when `day_values` is None, `worth()` ignores the day.
  - The guards' first rule then accepts any offer that is better on price alone. Probe: our offer is 62 on day 0;
    their 58 on day 10 is accepted.
  - The code policy does the same from the opener on.
  - The runner already leaves such duels to the models (`by_code`), but `final()` runs `guarded()` on every path.
  - It is harmless while Duels III keeps Duels II's wording.
- **Fix:**
  - `guarded()`: return early when `self.view.has_days and self.view.day_values is None`. (`first_day` already does,
    through `day_read`.)
  - `respond_code`: use the model path for that duel.

### S3. Sellers can never offer below their nominal limit, even inside the limit on a bonus day (main and branch)
- **The cause:** `mentions_past_limit` checks amounts in the text on price only (guards.py:60), and `final()` blocks
  the whole move on it (agent.py:896).
  - Probe: a seller with limit 73 and 4.46 per day offers 70 on day 10, worth +41.6. It becomes "Let me think about
    that.", and the runner holds.
  - The same happens to the silent walk, the floor's price and the code policy's steps.
- **The cost:** silent-rival duels 5816 and 6006 froze for their last 3-4 ticks at 74 and 73 on day 10, and ended
  with no deal. This cost is soft, because those rivals never spoke.
- **Fix:** don't flag the move's own price once `past_limit` has passed it. For example, filter out
  `p.value == move.price` in `final()`.

### S3. `first_day` changes 12 of the 68 real openers, and its give isn't the one the simulator played
- **Menu calls:** on a menu call it forces our best day even when the model chose their day.
  - 10 of the 12 changes were menu calls. In 9 of those 10 the model had opened on their day.
  - **8 of the 10 deals settled on their day:** 5796 (40.6), 5822 (33.0), 5809 (28.8), and also 5653, 5827, 5893,
    6049 and 6176.
  - Whether later offers stay on our day is up to the strategist, not code. With v2, `LATE_SWITCH_LEFT` 0, no code
    switch would follow.
- **Give calls:** `first_day` adds a premium of C in worth (agent.py:880). The price moves by C plus the cost
  difference between the model's day and theirs: 22 P in 5622 (C ≈ 14). The simulator's give is worth-neutral.
- **Relevance under v2:** `OPEN_WAIT` 0 makes us open before the rival does, so `first_day` (which needs their offer)
  will rarely fire.
- **Fix:** `extra = 0.0`, as in S1. Consider leaving the model's day on a menu call.

### S4. Smaller issues
- **The floor's price can fall below 1 P.** On a costly day the floor goes to ≤ 0 (6095: −2 on day 10), and `final()`
  then turns it into `safe_move`.
  - Fix: as `held()` does, recompute on our last day when the price is below 1.
- **The first guard can accept a near-zero offer.** When the drafted move is itself past our limit, the first rule
  accepts any in-limit standing offer, even one worth about 0.
  - Fix: require `worth(move) >= 0` before converting.
- **The code policy's accept makes a text call it never sends.** `duel_accept` posts no text, and the call delays the
  accept by up to 3.5 s.
  - Fix: set the text to "Agreed." and skip `write()` for accepts.
- **The accept race (main too).** `POST /accept` takes the rival's offer as it stands at that moment.
  - Fix: compare the result's `price` with `move.price` and log any mismatch.
- **Restarts and the late switch.** `switched` isn't restored on a restart, and code doesn't stop a flip back to our
  day after the late switch (6190: 66 on day 10, then 122 on day 0).
- **NaN for an int key raises.** `validate()` raises `ValueError` on NaN for an int key instead of refusing it. The
  runner catches it and keeps the last good set, but `approve` crashes with a traceback (and writes nothing).

## Can the loop switch between 2-3 sets Aleks approves in advance, by a rule after each wave, with no human present?

**Not as built. The change that makes it safe is small, about 80 lines plus one line in the runner, and one prompt
line.** The Duel Lab's own plan is exactly this: three sets (v2, SAFE and today), stepping back after 8 duels when
the deal rate falls below 0.75.

**What a hot reload does to duels already in progress:** it applies to them at their next decision.
- How it works:
  - The runner re-reads `run/duel_params.json` on every new tick (keyed on the file's mtime and size) and sets the
    module globals.
  - Every rule reads those globals when it runs: holds, caps, the worth floor, the accept and deadline rules, the
    silent walk, the late switch, `OPEN_WAIT`.
  - Nothing is fixed per duel.
- Three side effects:
  1. **The prompts don't change.** The strategist's system prompt is written when the duel starts, and it states
     `LATE_SWITCH_LEFT` and `DAY_SAME_SIDE_P` (agent.py:446-454). A duel already running keeps the old numbers while
     code plays the new ones. The facts sent each turn (`MIN_STEP_P`, `MAX_STEP_SHARE`, `CLOSING_TICKS`) are current.
  2. **The records misattribute.** A duel's record stores `params` once, when the duel starts (runner.py `update`).
     A change in the middle of a duel shows only in the JSONL `params` event, so the wave loop scores that duel under
     the wrong set.
  3. **One decision can mix the old and new values.** A decision waiting on a model call can read the old values
     before the await and the new ones after it. This is harmless.
- **Safety holds whatever the set.** No tunable can push us past our limit: `final()` checks `past_limit`, a price of
  at least 1 P, the day 0-10 and the text's amounts, and none of those checks reads a param.

**Why it isn't ready to run without a human:**
- **Nothing applies on its own.** `run` and `watch` only propose, and `approve` is manual.
- **Calling `approve` from a cron would be unsafe:**
  - It **merges** the proposal into the file (`{**existing, **chosen}`), so a key from v2 that SAFE leaves out
    (`OPEN_WAIT` 0) would survive a step back to SAFE.
  - It accepts any value within the bounds, not just a list of approved sets.
  - On a changed baseline it only warns.
- **There is no quiet moment between waves.** In Duels II, starts rolled after the first two waves, never more than
  15 ticks apart, and each duel lasted 16. From tick 1239 to tick 1402 at least one of our duels was live on every
  tick. A wave counts as closed only once all its duels finish, and by then the next wave is already playing. A
  switch therefore always lands in the middle of some duels.
- **One wave is noise.** With 4 duels, a single no-deal reads 0.75. The gates wait for at least 8 duels with a rival
  that spoke.

**The smallest safe change:**
1. **A list of approved sets.** Add `duel_loop.py approve-sets --file run/duel_sets.json --by Aleks`, which Aleks runs
   once before 11:00.
   - The file holds `{"v2": {...}, "safe": {...}, "today": {...}}`.
   - **Every set lists the same keys:** `MIN_STEP_P`, `MAX_STEP_SHARE`, `LATE_SWITCH_LEFT`, `OPEN_WAIT` and
     `MONO_END_SHARE`. "today" is 3 / 0.25 / 4 / 2 / 0.25.
   - Each set is checked with `params.validate` and the CROSS rules, and the file is stamped with the approver.
   - Only allow keys that are safe to change mid-duel. Those five are safe once the prompt stops stating
     `LATE_SWITCH_LEFT` (see S2); `OPEN_WAIT` only affects a duel before its opener.
   - Keep `CLOSING_TICKS`, `DECIDE_LEFT`, `ACCEPT_BY` and `DAY_SAME_SIDE_P` identical across sets.
2. **A switch command.** Add `duel_loop.py switch --every 15`, run **on the duelist's machine**, where the records
   are local and fresh. On each newly closed wave it:
   - runs a fixed, cumulative rule: the 8-duel gate, stepping v2 → safe → today;
   - requires at least 8 duels since the last switch, only ever steps back (never forward without a human), and
     never switches more than once per two waves;
   - writes `run/duel_params.json` **as a full replacement** of exactly one named set, with `write_atomic` and a
     `_note` naming the set, wave, rule and evidence;
   - does nothing, with a warning, if the current file isn't one of the approved sets;
   - honours a kill switch (`run/duel_switch.off`, or `--dry`) and logs each switch to `intel/duel-loop.md`.
3. **Record the set on every decision.** Add `"params": self.params.overrides() if self.params else None` to the
   `decisions=[{...}]` record (runner.py:412), and label each duel by the set it played most of its ticks under.
   - True per-duel pinning would mean moving roughly 30 global reads into a per-agent snapshot: not a change for
     Sunday morning.
   - Applying a switch mid-duel is acceptable once it is recorded, because these keys only move thresholds.

**Without that change:** keep switching by a human. Pre-write each set as a proposal file like
`docs/duels3-start.json`, so a switch is one command: `approve --proposal docs/<set>.json --by Aleks`.
- **List the same five keys in every set.** `approve` merges, so it then overwrites every key and nothing from the
  old set remains.
- **Don't `revert` first:** the defaults could play for a tick in between.

## Offline replay (Duels II, 68 duels, 514 decisions, at the earlier 0.5 file's settings)

The records are at 16 ticks and 8% decay, not Sunday's 12 / 10%. Each decision is a one-step counterfactual on the
real history.

| Path | Result |
|---|---|
| Code policy (the runner's order: closing → switch → silent → `code_move` → `final`) | 225 steps, 126 small-step holds, 68 openers, 50 silent-walk steps, 31 accepts, 6 late switches, 7 blocked seller offers turned into holds (5816, 6006); **34 give retreats in 9 duels (S1)** |
| Guards on the models' real moves (`guarded` only) | 27 worth floors, 4 accept-instead (5618: their 46 on day 0, worth 4, beat our 23-24 on day 5, worth 2; today's main takes it at 2 ticks left, the guard at 3) |
| `held` + `guarded` | 193 unchanged, 52 holds, 12 floors, 11 caps, 3 accepts; 13 closing offers touched (12 excluding 6094; S3) |
