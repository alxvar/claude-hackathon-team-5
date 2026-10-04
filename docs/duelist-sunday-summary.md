# Duelist for Sunday: what changed, how it was tested, what to run (for Aleks)

_Chief, Sun 09:45. One page; links go to the full evidence. Branch `origin/duelist-loop` @ **29aa1be** (22 commits on top of main, 17 files, +3,258 lines). main is untouched and is the rollback._

## 1. What changed (vs main)
1. **Hot-reloaded params** (`run/duel_params.json`, 27 bounded tunables) plus a **params registry**. Tuning applies at the next decision without a restart.
2. **Code-first policy** (`--policy code`). Code decides accept / hold / step / day; the LLM only writes the message text (Haiku ≈ 2 s per decision, vs 9.2 s mean and 29% > 10 s with the LLM deciding).
3. **Guards on every offer.** Accept instead of offering something worse, worth-monotonic concessions, the day call enforced on the first offer, a floor price ≥ 1 P, NaN refused, and no accept-instead from a past-limit draft. `{"GUARDS": 0}` turns them off live.
4. **Audit fixes** (`a412b67`, `7a0d516`):
   - a "give" day call no longer re-adds the day premium on every step. That bug made the bot back away from the rival in 9 Duels II replays; it now does 0 times.
   - per-role openers: **seller 0.42 (price distance), buyer 0.37** (`29aa1be`, the Duel Lab's ruling: seller 0.73 opened ≈ 1.0 × limit in worth);
   - a missing params file plays set A and says so LOUDLY;
   - failover: the primary's budget is 8 s (`--failover-s`) and a timeout counts as a failure, so the trip fires within a 15 s tick;
   - an unreadable day weight is handed to the models.
5. **Param sets** in `docs/duel_sets.json`: C (Sunday), A (safer), today.
   - `tools/duel_loop.py use SET` writes the whole file.
   - `switch` is a one-way **C → A** rule: ≥ 12 closed duels with rivals that spoke and a deal rate < 0.60. Kill switch: `run/duel_switch.off`.
   - `approve` refuses a changed baseline unless `--force`.
6. **`tools/duelist_sunday.sh`**, a one-command start:
   - runs in its own worktree (no merge into your checkout);
   - full suite, abort on red;
   - refuses if a duelist is running, BEFORE touching params;
   - `--check`, `--status`, `--stop`, `--rollback` (to main's duelist).

## 2. How it was tested
- **Suite: 579 passed** on 29aa1be (from 547 at the first review).
- **Independent audit #1** (`intel/duelist-audit.md`, no-context agent): GO with `--policy llm` only. It found the give-retreat bug, the missing-params issue, the 30% LLM timeouts at 15 s ticks and unsafe set switching. All four were fixed.
- **Independent re-audit** (`intel/duelist-reaudit.md`): GO-WITH-CHANGES on a99f641. Its patch was applied.
- **Delta audit** of 29aa1be (same file, last section): **GO**.
  - R1 rollback, R2 refuse-first, R3 opener, R5, R6 and R9 verified.
  - Sandbox: start refuses at step 1, `--stop` and `--rollback` behave.
  - **Duels II replays: no wrong actions.**
- **Two independent simulators agree** (`intel/duel-lab.md` SUNDAY v2 + `intel/duel-crosscheck.md`, built from scratch without reading the Lab): **C > A > today** in every opponent world (past rivals, a Team-10-style fast closer, silent rivals, mirrors). Per-opponent profiles were tested and are not worth it (+0.0014/duel).
- **Contrarian review** (`intel/contra-duels.md`): keep code policy + C, add **C+**. The Duel Lab confirmed C+ on its sim with the trader ON: +0.028/duel, no world worse.

## 3. Expected effect [modelled]
Code-first C+ ≈ 0.43 points/duel vs ≈ 0.34 for Saturday's LLM setup with ~30% timeouts. That's ≈ +6 raw duel points in Duels III and ≈ +3 in the Final (≈ +1.5-2 Sunday round points). C+ alone adds ≈ +0.45 Sunday points.

## 4. What to run (PLAN.md #32, zsh, keep the braces)
```
SHA=29aa1bed66962959ce633492d84bbc321385c7e7
bash <(git show "${SHA}:tools/duelist_sunday.sh") --status
COMMIT=$SHA bash <(git show "${SHA}:tools/duelist_sunday.sh") --stop     # only if Saturday's duelist is up
COMMIT=$SHA bash <(git show "${SHA}:tools/duelist_sunday.sh") --check    # expect "steps 1-4 passed"
COMMIT=$SHA AUTOSWITCH=1 bash <(git show "${SHA}:tools/duelist_sunday.sh")
# then C+ (hot), in the worktree $WT the script prints:
printf '{"wave": "C+ Duel Lab", "params": {"MIN_STEP_P": 15, "ACCEPT_BY": 1}}\n' > "$WT/run/c_plus.json"
(cd "$WT" && python3 tools/duel_loop.py approve --proposal run/c_plus.json --by Aleks)
```
- Never pipe the script's output (it hangs). Never re-run start/`--check` while it's live (a restart reinstalls plain C; re-apply C+).
- **Times today:** Duels III ≈ 11:00, the Final ≈ 14:00 (re-read `/api/schedule`).
- **First-wave check** (≈ 3 min in):
  1. `grep -E "direction unknown|CAN'T READ|refused"` on the newest `$WT/logs/duelist/supervise-*.log` prints nothing;
  2. the first deal's pred = points in `uv run python -m agents.duelist review`;
  3. no `refused:` lines;
  4. ≥ 1 of the first 4 rivals that spoke reached a deal.
- **Escape ladder:**
  1. `python3 tools/duel_loop.py use A`;
  2. the same sha with `POLICY=llm`;
  3. `--rollback` (Saturday's duelist on main).
  - If an accept shows a send error: approve `{"ACCEPT_BY": 2}`.

## 5. Residual risks
- Rivals may have changed their bots overnight; AUTOSWITCH C → A is the insurance.
- `--rollback` costs ≈ 0.09/duel vs C.
- The market negotiator (`agents/negotiator/`) stays OFF today (PLAN #33): only the Operator trades on the shared key.
