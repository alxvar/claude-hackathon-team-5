# Duelist re-audit: `origin/duelist-loop` at a99f641 (and 3a0f6f3) before Duels III and the Final

_Independent re-audit, Sun 00:50-01:20, for Aleks and Lucas. It checks the fixes for `intel/duelist-audit.md`._
- _**Scope:** offline only. Nothing touched the live server, no key was read or printed, and nothing changed on main
  or the branch. The work ran in temporary worktrees of 3a0f6f3, a99f641 and origin/main and in a throwaway clone;
  all of them were removed afterwards._
- _**`--check`, `--stop` and `--rollback`** ran with `git fetch` and `curl` stubbed, and with dummy processes standing
  in for a live duelist. No real duelist was started._
- _**Sources:** the session scratchpad's `reaudit/` folder holds the replay, probe, fuzz and script-test files and
  their `.out` outputs. Every number below is copied from those outputs._
- _**Labels:** [V] measured on the code or the records, [L] modelled (the Duel Lab's `sim3`)._

## Verdict: GO-WITH-CHANGES

**The duelist code is safe to start from a99f641. Run it as it is if the fix commit below can't land and be
re-checked by about 10:30; until then, follow the operating rules.**
- **The code:**
  - The full suite is green.
  - The 514 Duels II decisions were replayed through the code policy under sets C, A and today, both as recorded
    and rescaled to 12 ticks at 10%. None accepted below our limit, offered past it, named a wrong day or stepped
    backward.
  - 6,000 random duels per set with readable day weights raised no flag. (Unreadable weights are a separate,
    low-probability residual: R5.)
  - The switch now stops at A, and `--stop` stops everything and starts nothing.
- **What still needs the fix:** two defects in `tools/duelist_sunday.sh` and one value defect.
  1. `--rollback` crash-loops. The Lab's SUNDAY v2 names it "the tested way back", so this matters.
  2. A re-run while the duelist is live rewrites the live params file before it refuses.
  3. The seller opener: −0.022 a duel, modelled.

  A 6-file patch fixes all three, plus three smaller items: the params-file sentinel (R6), fetch tolerance (R9), and
  handing unreadable-weight duels to the models (R5, a partial mitigation). On a99f641 it passes the suite (576), the
  set C replays and the script tests. It is in the appendix.

**Aleks's command.** Paste the lines exactly as they are. They carry no `#` comments, because interactive zsh
doesn't treat `#` as a comment unless `interactivecomments` is set. The braces in `"${SHA}:tools/…"` matter: in zsh,
`$SHA:t` is a modifier and breaks the path.

```bash
git fetch origin
SHA=a99f6417b644922c7ccefdf03f33f0bdcd9762a2
COMMIT=$SHA bash <(git show "${SHA}:tools/duelist_sunday.sh") --check
COMMIT=$SHA AUTOSWITCH=1 bash <(git show "${SHA}:tools/duelist_sunday.sh")
```

- **Where:** your normal checkout.
- **`--check`:** it must print "steps 1-4 passed". Then run the second line.
- **The start:** `SET=C` and `POLICY=code` are the defaults. `AUTOSWITCH=1` is the Lab's recommendation, and safe
  now that the switch stops at A.
- **If the fix commit lands:** use the same lines with its sha. First check that `git diff --stat a99f641 <sha>`
  shows only the six patched files, and that `--check` passes (it runs the full suite).
- **Moving a running a99f641 duelist onto the fix commit:**
  1. Run `--stop` first. The patched `--check` refuses while a duelist runs.
  2. Start with the new sha and `SET=<the set now live>`.
- **Never use `origin/duelist-loop` in place of the sha,** in either spot: it is a moving ref.

**Operating rules on a99f641 as it is:**
- **Start once.** While the duelist runs, use only `--status` and `--stop`. Never re-run start or `--check`: before it
  refuses, it checks code out in the live worktree and rewrites the live params file (R2).
- **After a `--stop`, restart with `SET=<the set now live>`.** Check it in `--status`. After a switch, a plain re-run
  would put C back with the rule already spent.
- **Don't use `--rollback`** (R1). Roll back by hand from your checkout, one line at a time:
  ```bash
  SHA=a99f6417b644922c7ccefdf03f33f0bdcd9762a2
  bash <(git show "${SHA}:tools/duelist_sunday.sh") --stop
  pgrep -fl "agents.duelist run|duelist/supervise.sh|duel_loop.py switch"
  git checkout main
  git status --short agents engine
  mkdir -p logs/duelist && (set -a; . ./.env; set +a; nohup agents/duelist/supervise.sh --negotiator-model claude-sonnet-5-5 --effort medium --negotiator-effort low > logs/duelist/supervise-rollback.log 2>&1 < /dev/null &)
  ```
  - **`pgrep` must print nothing.** If it prints a process, the stop didn't happen. Kill that process before starting
    main's duelist, or two duelists end up on the team key: the lock is per checkout.
  - **`git status` must print nothing,** too.
  - **The start line** uses Saturday's flags, which main's `run` accepts (checked offline).
- **For the Final:** if a switch happened in Duels III, start with `SET=A` (Lab: start on the set Duels III ended on).

## Tests

| Commit | `uv run python -m pytest -q tests` |
|---|---|
| 3a0f6f3 | **574 passed** |
| a99f641 | **576 passed** (+2: the switch stops at A; `--stop` starts nothing) |
| a99f641 + the appendix patch | **576 passed** |

On origin/main (950ac89), `tests/test_duelist.py` gives **77 passed**, and that is the test `--rollback` runs
(`main_test_duelist.out`). `git diff a99f641...950ac89` touches only `agents/dealers` and two of their tests: nothing
in `agents/duelist` or `engine`. `agents/` and `engine/` are identical at 3a0f6f3 and a99f641 (`main_drift.out`).

## The audit's items, one by one

| Audit item | Status | Evidence |
|---|---|---|
| **S1: the give retreat** (code policy) | **Fixed** [V] | `policy.code_day` returns a premium of 0 on a give, and the small-step hold stays on once we are on their day. Replay: 0 backward moves; the 9 duels and 34 decisions the audit flagged are clean. Probe (buyer, limit 100, 1.2 a day): opens at 51 on day 10, then holds. It used to go 34 → 28 → 22 → 17 → 12 |
| **Per-role openers** | **Done, but against the Lab** [V/L] | Sellers open at 0.74 × the limit in price, median, which is **1.00 × the limit in worth**. The models opened at 0.63 in price and 0.73 in worth, and the Lab simulated 0.42 in price (≈ 0.69 in worth). The Lab's SUNDAY v2 retracted the per-role item as its own units error (R3) |
| **Missing params file** | **Fixed mid-run, not at start** [V] | `Params._stamp` starts at `None`, which is also a missing file's stamp. On a fresh process `reload()` returns `{}`: the code defaults ("today") play silently with no warning (`probe_missing.out`). The test hides this by forcing `_stamp = "?"`. The script always writes the file first, so this bites only on another start path. Fix: a one-line sentinel (appendix) |
| **Failover at 8 s; a cancellation counts as a failure** | **Fixed** [V] | `failover.py:21` defaults to 8, and `:47-49` counts `CancelledError` and re-raises it. 3 tests cover `Failover` itself; the `--failover-s` pass-through was read in the code, not tested. Probe: two runner cancellations trip the primary, and the next call goes to the backup |
| **Prompt at `LATE_SWITCH_LEFT` 0** | **Fixed** [V] | `late_switch_line()` drops the line at 0 and never states a tick count (test at `tests/test_duelist.py:877`). The only number the prompt still states is `DAY_SAME_SIDE_P`, which no set changes |
| **Whole-file sets** (`use`) | **Fixed** [V] | Writes `_set`, `_note` and every key, atomically. Refuses an unknown set or a broken sets file. The sets match `intel/duel-sets/{C,A,today}.json` exactly. Works under python3 3.9.6 and 3.14.4 (`use_pythons.out`) |
| **`approve` on a changed baseline** | **Fixed** [V] | Refuses unless `--force` (`duel_loop.py:958-961`) |
| **The one-way switch and its kill switch** | **Fixed in a99f641** [V] | On 3a0f6f3 the switch cascaded: 12 duels at 0.50 gave C → A, and 4 more at 0.75 (session 0.56) gave **A → today on the next wave**. On a99f641, `_switch` is `{"C": "A"}`, and the same probe ends on A: "the last step of the switch: nothing written". The kill-switch file (`run/duel_switch.off`) has a test. `--dry` and once-per-set (`switched_from`) were read in the code, not tested |
| **The set recorded on every decision** | **Fixed** [V] | `runner.py:410-415` writes `params_set` and the overrides into the log and the record. Probe confirmed; there is no unit test |
| **Mid-duel switch** | **Works** [V] | Same duel, same state: C holds at 160 (a step of 6 < 8). After `use A`, the next decision steps to 154, and the record says A |
| **A seller below its nominal limit** | **Fixed** [V] | `said_past_limit`: an offer of 70 on day 10 against a limit of 73 (worth +41.6) now goes out |
| **`first_day` give premium** | **Fixed** [V] | `extra = 0`. Duel 5622 moves 8 P (worth-neutral) instead of 22. A menu call still forces our best day (optional; only the LLM path uses it) |
| **An unreadable day weight** | **Partly fixed** [V] | `guarded()` now skips. `respond_code` still plays the duel, though, with the day as free: our 60 on day 0 against their 58 on day 10 → **accept**. The fuzz ran 6,000 duels with unreadable weights, taking the true cost as linear in the curve's scale (an assumption, so the counts are illustrative). Under C: 485 offers past the true limit, 5 accepts below it, 7 backward moves; under A: 494 / 5 / 7. The patch hands these duels to the models. It only mitigates: when the models fail, `safe_move` still treats the day as free, and the patched probe with failing models still accepts the 58 (`a99_patched_probe_unreadable.out`) |
| **S4 items** | **Mostly fixed** [V] | Fixed: the floor never goes below 1 P, a near-zero accept is blocked, accepts make no text call (0 calls), and NaN is refused. Not done: logging an accept-price mismatch, and restoring `switched` after a restart (moot under C) |

## Duels II replays on the new code (task 3)

The 514 Duels II decisions went through the code policy in the runner's order: closing, switch, silent, then
`respond` (`respond_code` → text call fails offline → plain words → `final`). The models' real offers also went
through `held` + `final`. Sets come from `docs/duel_sets.json` via `Params.reload`.

| Set | Setting | Code path: accept below limit / offer past limit / wrong day / backward > 1 P | Rounding-up ≤ 0.9 P |
|---|---|---|---|
| C | as recorded (16 ticks, 8%) | **0 / 0 / 0 / 0** | 0 |
| C | rescaled to 12 ticks, 10% | **0 / 0 / 0 / 0** | 0 |
| A | both | **0 / 0 / 0 / 0** | 6 (late switch) |
| today | both | **0 / 0 / 0 / 0** | 27 / 41 (late switch) |

- **Set C, code path, as recorded:**
  - holds: 224 small-step, 1 same-offer;
  - steps: 104 code steps, 68 openers, 57 silent-walk steps;
  - 29 worth floors;
  - accepts: 20 deadline, 11 small-gap.
- **Where each replay ran:**
  - C (as recorded and rescaled) and A rescaled ran on a99f641.
  - A as recorded, and today in both settings, ran on 3a0f6f3. `agents/` and `engine/` are identical between the two
    commits.
  - On the patched code only C was re-run: 0 flags, and the seller opener at 0.43 in price / 0.69 in worth.
- **Fuzz** (6,000 random duels a set, both roles, readable weights): no flags under C or under A. For unreadable
  weights, see the table above (R5).
- **The LLM path (only matters with `POLICY=llm`):** the guards still pass the models' own moves.
  - 10 backward moves on a day change. Some are the strategist's give premium. Others are late flips back to our
    day: 5813, 58 on day 10 → 92 on day 0 with 3 ticks left.
  - Middle-day openers (day 5 at `OPEN_WAIT` 0): `first_day` acts only once the rival has offered.
  - The audit listed both: the flip back as S4 (6190), the `first_day` gap under `OPEN_WAIT` 0 in S3. Both are still
    open.

## `tools/duelist_sunday.sh`, line by line (task 4)

| Check | Result |
|---|---|
| **Worktree isolation** | **Good** [V]. A detached worktree at the sha, outside your checkout. Start mode never touches the checkout's branch. `run/`, `logs/` and `.venv` are ignored, so the dirty check still allows a re-run |
| **Abort on red tests** | **Works** [V]. With a red test added: "1 failed, 574 passed … ABORT: tests red: not starting" |
| **Refusing a second duelist** | **The refusal works, but it comes too late** [V]. It is step 4 of 6. Steps 1-3 first check out the sha in the live worktree and rewrite the live params file. Test: a dummy duelist was running and the params were on A; `--check` wrote C, then aborted. The check is also only local: other machines aren't seen, and the lock file is per checkout (`logs/duelist`) |
| **`--stop`** (a99f641) | **Works** [V]. It killed a dummy supervisor, duelist and switch. 6 s later: no process and no new log. It made no git writes (only `--status`'s read-only `git log`) and never touched `.env` |
| **`--rollback`** | **Broken** [V]. Details below |
| **No key leakage** | **Good** [V]. `.env` is sourced only inside the start subshell (`set -a`), never echoed, and there is no `set -x`. `--status` prints command lines (no key in them) and GETs `/api/clock` without a key. The switch process gets no key |
| **`git fetch` fails** | **Aborts at step 1** [V], even when the pinned sha is already local. That's safe, but it blocks a restart on bad Wi-Fi. The patch continues with the local copy when `COMMIT` is a sha |
| **Minor** | (1) "started in …" prints even when sourcing `.env` fails; the status 10 s later shows no process. (2) `bash <(git show origin/duelist-loop:…)` runs whatever the local ref holds: pin the sha in both places. (3) In zsh, `$SHA:tools` breaks: use `"${SHA}:tools"` |

**`--rollback` is broken in three ways:**
1. **Main's `run` has no `--records`.** Only `monitor` has it, but the script always appends it. argparse then exits
   with code 2, and `supervise.sh` restarts every 5 s, forever. `--status` shows a live supervisor, so it looks fine.
   Checked offline on origin/main: "unrecognized arguments: --records …". Without the flag, it parses.
2. **It stops every duelist first,** then fetches, checks out, pulls and runs the tests. If any of those fails, no
   duelist is left running.
3. **`pull --rebase` refuses a checkout with modified tracked files.** That is likely mid-session, because the live
   duelist writes `docs/duels` in that checkout.

## Defaults against the Duel Lab's SUNDAY v2 (task 5)

| Setting | Script | Lab SUNDAY v2 | Verdict |
|---|---|---|---|
| `SET` | C | C, if the prompt no longer states `LATE_SWITCH_LEFT` (it doesn't) | ✓ Same values as `intel/duel-sets/C.json` |
| `POLICY` | code | code, if the S1 fix passes its replay check (it does: 0 retreats) | ✓ |
| Negotiator | Haiku 4.5 | Haiku 4.5 | ✓ |
| Strategist | Opus 5.5, effort low | Opus, effort low (for the LLM fallback) | ✓ Unused under `POLICY=code` |
| `--failover-s` | 8 | 8 (the Run row) | ✓ Under code the text call is capped at 3.5 s, so 8 doesn't bind. Under `POLICY=llm`, 8 leaves the backup about 2 s of the 10 s decision budget; the audit had suggested about 6 |
| `AUTOSWITCH` | 0 (default) | **1**, with only C → A (needs a99f641's `_switch`) | ✓ Pass `AUTOSWITCH=1`, as in the command above. It is safe on a99f641; the restart rule handles R2 |
| The way back | `--rollback` | "the tested way back is `--rollback`" | **✗ Broken on a99f641 (R1).** Use the manual rollback until the patch lands |
| Code opener | seller 0.73, buyer 0.37 (price) | **0.42 in price** ("fine"; per-role retracted) | **✗ R3** |

**What the opener costs, in the Lab's own simulator** [L]: `sim3`, code-first, 12 ticks at 10%, 4,000 duels per world
in 6 worlds, paired seeds. The baseline lands on 0.423, against the Lab's 0.421 at 10,000 duels per world.

| Set | Opener 0.42 (Lab) | Branch (0.73 / 0.37) | Δ | Seller Δ | Buyer Δ |
|---|---|---|---|---|---|
| C | 0.423 | 0.401 | **−0.022** | −0.057 | +0.014 |
| A | 0.397 | 0.378 | −0.020 | −0.050 | +0.011 |

- **Over Duels III (68 duels):** −0.022 a duel ≈ −1.5 points; ≈ −0.75 in the Final (34 duels), using the Lab's own
  conversion (0.080 a duel ≈ 5.4 points).
- **The patch's mix, seller 0.42 and buyer 0.37:** ≈ 0.430 under C, from the same runs.
- **Even unfixed, code-first C (0.401) still beats** the alternative, LLM C with 30% timeouts (0.387).

## Remaining risks, ranked

1. **R1: `--rollback` crash-loops and stops the duelist before its checks.** It only matters in an emergency, but then
   no duels get played. The patch fixes it.
   - **Tested:** the checks-first order, in a throwaway clone. Main's `run` parses Saturday's flags without
     `--records`.
   - **Not run end to end:** the patched start itself.
   - **Until it lands:** roll back by hand (above).
2. **R2: a re-run of start or `--check` while live rewrites the live params file and checks out code before it
   refuses.** With `AUTOSWITCH=1`, this also resets A → C for good. Fixed by the patch (the duelist check moves to
   step 1); until then, follow the rule.
3. **R3: the seller opener at 0.73,** about −0.022 a duel [L], so about −1.5 points in Duels III and −0.75 in the
   Final. Fixed by the patch.
4. **C's holds (evidence risk, unchanged from the audit).** Mid-duel, C concedes only when the gap is at least 66.7
   P in worth (0.12 × gap ≥ 8). Otherwise it waits for the last 3 ticks and the deadline accept. That is what the Lab
   simulated. In Duels II it would have held or raised 12 closing offers, and C holds more. Watch the deal rate; the
   switch rule is the insurance.
5. **An unreadable day weight under code** (low probability, high cost). Code treats the day as free and can accept
   past the true limit. The patch hands such a duel to the models. When the models fail, `safe_move` still treats the
   day as free.
6. **A missing params file at start plays "today" silently.** Only on a start that bypasses the script. Fixed by the
   patch.
7. **The LLM-path residuals (only with `POLICY=llm`).** Late day flips and the give premium pass the guards, and
   failover 8 is above the Lab's 6.
8. **The one-duelist check is local only,** and the lock is per checkout. Confirm in the team chat that nothing else
   runs on the team key.
9. **A failed `git fetch` blocks a restart.** Fixed by the patch for a pinned sha.
10. **Small:** an accept-price mismatch isn't logged; `switched` isn't restored after a restart (moot under C); and
    `docs/duelist-loop.md` still describes the old `--rollback`.

## Appendix: the fix patch on a99f641 (6 files, +30 −24; 576 passed; replay C: 0 flags, seller opener 0.43 in price / 0.69 in worth)

What it changes:
- **`tools/duelist_sunday.sh`:**
  - the one-duelist check comes first;
  - a failed fetch is tolerated for a pinned sha;
  - `start_in` passes `--records` only when given, and refuses without `.env`;
  - `--rollback` checks everything first (no agents/engine edits, on main, the duelist identical to origin/main, the
    tests, `.env`), then stops, then starts without `--records`. It no longer pulls.
- **Code:**
  - seller opener 0.42;
  - the `Params` stamp sentinel;
  - code policy hands an unreadable-weight days duel to the models;
  - three test lines.
- **Tested:**
  - `--check`: clean, it passes. With a dummy duelist running, it aborts at step 1 and the params stay on A. With the
    fetch failing on a pinned sha, it continues.
  - `--rollback`, in a throwaway clone: with a code edit, it aborts with both dummies still alive. With no `.env`, it
    aborts before stopping anything.

<details><summary>the diff</summary>

```diff
diff --git a/agents/duelist/agent.py b/agents/duelist/agent.py
index 3545b7c..5d044ab 100644
--- a/agents/duelist/agent.py
+++ b/agents/duelist/agent.py
@@ -762,7 +762,7 @@ class DuelAgent:
         return Move("offer", text, price=price, days=days, meta={"repaired": True, **meta})
 
     async def respond(self, obs: Observation) -> Move:
-        if self.policy == "code":
+        if self.policy == "code" and not (self.view.has_days and self.view.day_values is None):
             return await self.respond_code(obs)
         self.calls = []
         try:
diff --git a/agents/duelist/params.py b/agents/duelist/params.py
index 832e96e..22d5c81 100644
--- a/agents/duelist/params.py
+++ b/agents/duelist/params.py
@@ -153,7 +153,7 @@ class Params:
         self.modules, self.path, self.sets_path = modules, Path(path or PATH), Path(sets or SETS)
         self.defaults = {k: getattr(modules[s.module], k) for k, s in SPEC.items() if s.module in modules}
         self.current = dict(self.defaults)
-        self._stamp: Any = None
+        self._stamp: Any = object()            # never equal to a stamp: the first reload always reads
         self.last_error: list[str] = []
         self.missing = False                           # the file is missing: the fallback set plays (loudly)
         self.set_name = "code defaults"                # what plays: a set's name, "custom", or the code defaults
diff --git a/agents/duelist/policy.py b/agents/duelist/policy.py
index 288655b..c5895a0 100644
--- a/agents/duelist/policy.py
+++ b/agents/duelist/policy.py
@@ -45,7 +45,7 @@ from .prices import money
 if TYPE_CHECKING:
     from .agent import DuelAgent, Move
 
-OPENER_SHARE_SELLER = 0.73   # a seller's opener: this share of the limit above it (the models' Duels II median, audit)
+OPENER_SHARE_SELLER = 0.42   # a seller's opener, in PRICE on our best day (Duel Lab SUNDAY v2: the day bonus takes it to ~0.70 in worth)
 OPENER_SHARE_BUYER = 0.37    # a buyer's: this share below it (one share for both opened sellers far too low)
 CODE_STEP_SHARE = 0.12   # a mid-duel concession: this share of the gap (simulated vs today's 25% cap, below)
 END_STEP_SHARE = 0.5     # in the last CLOSING_TICKS ticks: this share (the simulator's end_alpha)
diff --git a/tests/test_duelist_params.py b/tests/test_duelist_params.py
index 8e01fc2..5633fc7 100644
--- a/tests/test_duelist_params.py
+++ b/tests/test_duelist_params.py
@@ -106,7 +106,6 @@ def test_a_missing_file_plays_the_default_set_loudly_never_the_code_constants(tm
     sets.write_text(json.dumps({"_default": "A", "A": {"MIN_STEP_P": 5, "MAX_STEP_SHARE": 0.18}}))
     p = Params(modules(), tmp_path / "duel_params.json", sets=sets)
     try:
-        p._stamp = "?"                                                # force the first read
         r = p.reload()
         assert r["missing"] and A.MIN_STEP_P == 5 and A.MAX_STEP_SHARE == 0.18 and p.set_name.startswith("A ")
         put(p, {"_set": "C", "MIN_STEP_P": 8})                      # the file arrives: it wins, named
@@ -115,7 +114,6 @@ def test_a_missing_file_plays_the_default_set_loudly_never_the_code_constants(tm
         logs = tmp_path / "logs"
         runner = DuelRunner(None, None, None, dry_run=True, log=Log(logs), decay=None, duel_ticks=None, poll_s=0.1,
                             params=Params(modules(), tmp_path / "gone.json", sets=sets))
-        runner.params._stamp = "?"
         assert runner.reload_params()["missing"]
         assert any(json.loads(x)["event"] == "params_missing" for x in runner.log.path.read_text().splitlines())
     finally:
diff --git a/tests/test_duelist_policy.py b/tests/test_duelist_policy.py
index db88e86..accb113 100644
--- a/tests/test_duelist_policy.py
+++ b/tests/test_duelist_policy.py
@@ -44,7 +44,7 @@ def agent(view=SELLER, model=None):
 
 def test_the_opener_sits_opener_share_of_the_limit_away_rounded_toward_us():
     a, _ = agent()
-    assert P.code_move(a, obs(SELLER)).price == 70          # a seller: 40 + 0.73 x 40 = 69.2, up (per role, audit)
+    assert P.code_move(a, obs(SELLER)).price == 57          # a seller: 40 + 0.42 x 40 = 56.8, up (Duel Lab SUNDAY v2)
     b, _ = agent(BUYER)
     assert P.code_move(b, obs(BUYER)).price == 37           # a buyer: 60 - 0.37 x 60 = 37.8, down
 
@@ -132,7 +132,7 @@ def test_a_days_seller_opens_on_price_not_on_a_worth_that_carries_the_day_bonus(
     # Duel 6094 replay: worth-based, the opener came out at -2 P (day 10 adds 51.1 to a seller's worth)
     a, _ = agent(DAYS_SELLER)
     m = P.code_move(a, obs(DAYS_SELLER))
-    assert m.days == 10 and m.price == 59                   # 34 + 0.73 x 34 = 58.8, up
+    assert m.days == 10 and m.price == 49                   # 34 + 0.42 x 34 = 48.28, up
 
 
 def test_prices_never_go_below_the_floor_and_the_accept_ratio_is_tunable(monkeypatch):
diff --git a/tools/duelist_sunday.sh b/tools/duelist_sunday.sh
index b2db270..643ee9e 100755
--- a/tools/duelist_sunday.sh
+++ b/tools/duelist_sunday.sh
@@ -4,7 +4,7 @@
 #   bash <(git show origin/duelist-loop:tools/duelist_sunday.sh) --rollback   # back to Saturday's duelist on main
 #   bash <(git show origin/duelist-loop:tools/duelist_sunday.sh) --stop       # stop every duelist, start nothing
 #   bash <(git show origin/duelist-loop:tools/duelist_sunday.sh) --status     # one screen
-#   bash <(git show origin/duelist-loop:tools/duelist_sunday.sh) --check      # steps 1-4 only: never starts
+#   bash <(git show origin/duelist-loop:tools/duelist_sunday.sh) --check      # steps 1-4 only: never starts (refuses while a duelist runs)
 # The approved code runs from its own worktree ($WT), never from your checkout: your checkout's auto-sync pushes
 # HEAD to main, so a detached branch there would merge it unreviewed. Its duel records still go to your checkout's
 # docs/duels (--records), which your auto-sync pushes as before. Never writes to the game itself.
@@ -45,34 +45,45 @@ stop_all() {
   die "a duelist process is still running: $(procs | tr '\n' ' ')"
 }
 
-start_in() {   # dir, records, flags...
+start_in() {   # dir, records ("" = none: main's `run` has no --records), flags...
   local dir="$1" rec="$2"; shift 2
+  [ -f "$MAIN/.env" ] || die "no $MAIN/.env: not starting"
+  local extra=(); [ -n "$rec" ] && extra=(--records "$rec")
   mkdir -p "$dir/logs/duelist"
   local log="$dir/logs/duelist/supervise-$(date +%Y%m%d-%H%M%S).log"
   (cd "$dir" && set -a && . "$MAIN/.env" && set +a && \
-    nohup agents/duelist/supervise.sh "$@" --records "$rec" >"$log" 2>&1 </dev/null &)
-  say "started in $dir: supervise.sh $* --records $rec (log $log)"
+    nohup agents/duelist/supervise.sh "$@" ${extra[@]+"${extra[@]}"} >"$log" 2>&1 </dev/null &)
+  say "started in $dir: supervise.sh $* ${extra[*]:-} (log $log)"
 }
 
 case "${1:-start}" in
   --status) status; exit 0 ;;
   --stop) say "STOP: stopping every duelist and the switch on this machine; starting nothing"; stop_all; status; exit 0 ;;
   --rollback)
-    say "ROLLBACK: stopping every duelist on this machine"; stop_all
+    say "ROLLBACK: check main first, then stop and start (nothing is stopped if a check fails)"
     git -C "$MAIN" diff --quiet HEAD -- agents engine || die "uncommitted code in $MAIN: commit or stash it by hand first"
-    git -C "$MAIN" fetch -q origin && git -C "$MAIN" checkout -q main && git -C "$MAIN" pull -q --rebase origin main \
-      || die "could not bring $MAIN to origin/main"
+    [ "$(git -C "$MAIN" rev-parse --abbrev-ref HEAD)" = main ] || die "$MAIN is not on main: check out main by hand first"
+    git -C "$MAIN" fetch -q origin || say "   git fetch failed: comparing with the last fetched origin/main"
+    git -C "$MAIN" diff --quiet origin/main -- agents/duelist engine || die "$MAIN's duelist differs from origin/main: pull by hand"
     (cd "$MAIN" && "$UV" run python -m pytest -q tests/test_duelist.py >/dev/null 2>&1) || die "duelist tests red on main"
-    # main has no params file support: Saturday's constants, Saturday's flags (docs/duelist-runbook.md)
-    start_in "$MAIN" "$MAIN/docs/duels" $OLD_FLAGS
+    [ -f "$MAIN/.env" ] || die "no $MAIN/.env: not stopping anything"
+    say "   main is ready: stopping every duelist on this machine"; stop_all
+    # main has no params file support and no --records: Saturday's constants, Saturday's flags (docs/duelist-runbook.md)
+    start_in "$MAIN" "" $OLD_FLAGS
     sleep 8; status; exit 0 ;;
   start|""|--check) ;;
   *) echo "usage: duelist_sunday.sh [--status | --check | --stop | --rollback]"; exit 2 ;;
 esac
 
-say "1/6 fetch and check out $COMMIT in $WT"
-git -C "$MAIN" fetch -q origin || die "git fetch failed"
-sha="$(git -C "$MAIN" rev-parse --verify -q "$COMMIT^{commit}")" || die "no commit $COMMIT"
+say "1/6 one duelist per machine (before anything is touched: a live duelist reads $WT and its params file)"
+if procs >/dev/null; then die "a duelist is already running here: $(procs | tr '\n' ' '). Stop it, or use --rollback"; fi
+
+say "2/6 fetch and check out $COMMIT in $WT"
+if ! git -C "$MAIN" fetch -q origin; then
+  [[ "$COMMIT" =~ ^[0-9a-f]{7,40}$ ]] || die "git fetch failed (and $COMMIT is not a pinned sha)"
+  say "   git fetch failed: using the local copy of the pinned $COMMIT"
+fi
+sha="$(git -C "$MAIN" rev-parse --verify -q "$COMMIT^{commit}")" || die "no commit $COMMIT (fetch it first)"
 if [ -d "$WT/.git" ] || [ -f "$WT/.git" ]; then
   git -C "$WT" diff --quiet HEAD || die "$WT has local changes: remove the worktree or commit them"
   git -C "$WT" checkout -q --detach "$sha" || die "checkout failed in $WT"
@@ -81,17 +92,14 @@ else
 fi
 say "   $WT at $(git -C "$WT" log --oneline -1)"
 
-say "2/6 the full test suite"
+say "3/6 the full test suite"
 out="$(cd "$WT" && "$UV" run --project "$WT" python -m pytest -q tests 2>&1)"; code=$?
 echo "$out" | tail -1
 [ $code -eq 0 ] || { echo "$out" | grep -E '^(FAILED|ERROR)' | head; die "tests red: not starting"; }
 
-say "3/6 install the approved set $SET as the whole params file"
+say "4/6 install the approved set $SET as the whole params file"
 (cd "$WT" && python3 tools/duel_loop.py use "$SET" --by "$BY") || die "set $SET refused"
 
-say "4/6 one duelist per machine"
-if procs >/dev/null; then die "a duelist is already running here: $(procs | tr '\n' ' '). Stop it, or use --rollback"; fi
-
 if [ "${1:-}" = "--check" ]; then say "--check: steps 1-4 passed; not starting"; status; exit 0; fi
 
 say "5/6 start: --policy $POLICY $FLAGS"
```

To apply it: save the block as `fixes.patch`, then run `git apply fixes.patch` on a checkout of a99f641, commit and re-pin.

</details>
