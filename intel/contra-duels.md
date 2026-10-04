# Contra-duels: trying to break stage 2 of `intel/sunday-final.md` (Sun ≈ 08:00)

_Contrarian review, read-only. No game calls, no keys, nothing started, nothing on the branch changed._
- _**Read:** sunday-final, duel-lab (SUNDAY v2 + morning check), duel-crosscheck, duelist-reaudit (incl. Delta audit
  29aa1be), duelist-audit, `docs/duelist-loop.md` and `docs/duel_sets.json` at origin/duelist-loop, RULES.md,
  audit-why-we-lost, ops-contention, the code at 29aa1be, and our 136 duel records._
- _**Re-ran both simulators read-only:** the Lab's `v2/sim3.py` and the cross-check's `robust.py` / `labpol.py`. The
  drivers and outputs are in this session's scratchpad `contra/`, which is temporary:
  - drivers: `overnight.py`, `mirror.py`, `fallbacks.py`, `pols_contra.json`;
  - outputs: `overnight_H1.out`, `overnight_H2.out`, `mirror.out`, `fallbacks.out`, `xcheck_share.out`,
    `xcheck_paired.out`, `pols_contra_robust.pkl`._
- _**Checked:** an independent verifier pass audited this file against its sources: 1 major and 11 minor flags, all
  fixed below._
- _**Labels:** [V] measured on records or code, [L] modelled, [?] unknown._
- _**Units:** the Lab's "+5.4 / +2.7" are raw duel points (share × 0.9^rounds, summed over duels). The Analyst's
  Duels III +4.7 and Final +2.3 Sunday points, at ≈ 0.42 a duel, imply **1 raw duel point ≈ 0.16 Sunday points ≈
  0.07 final** [L]. Saturday's 6.9 of 12 at 35.4 raw implies 0.2._

## Verdict: CHANGE five things, KEEP the core

| # | Issue | Expected Sunday points at stake | Fix | Verdict |
|---|---|---|---|---|
| 1 | Set C stops at the corner of the Lab's own grid. Both simulators prefer accepting one tick later. The Lab's also prefers holding longer; in the cross-check's, holding alone is a wash | **+0.5 to +0.7** [L] | **C+** = C plus `MIN_STEP_P` 15 and `ACCEPT_BY` 1. Two hot params, no code, no restart. Only with the trader, swaps and opps off in the duel window | **CHANGE** |
| 2 | No first-wave check. The switch can't fix a misread or a new issue, and its SWITCH line hides one | EV **+0.15 to +0.5** [L, on a [?] 3-5% chance], tail −4 to −11 | A four-line check on the first wave of each session, and a SWITCH line read as an alarm | **CHANGE** (add) |
| 3 | The only real escape is `--rollback` to main, ≈ −0.09 a duel against C | ≈ +0.1 EV [L], but **−1.5 to −2** if pulled at the start | Three tiers: hot `use A`, the same sha with `POLICY=llm`, then rollback (with faster flags) | **CHANGE** |
| 4 | Ops: three different start commands, the pipe hang, stale briefs for Aleks | +0.05 to +0.15 [L] | One zsh-safe block, run in a plain Terminal tab | **CHANGE** |
| 5 | Units: the plan prices the duel delta about 5× too high. The duel window also blocks dealer threads, which cost duels nothing | duel-side ≈ 0; market-side [?] | Restate: C over today's setup ≈ +1.5 Sunday points. Allow the Operator's dealer threads in the window; keep the trader, swaps and opps off | **CHANGE** (wording and the window rule) |
| 6 | The C → A switch: timing and carry-over | ≈ 0 (≤ 0.03) | None: carry A into the Final as the Lab says | KEEP |
| 7 | Code vs LLM policy at 15 s ticks; Haiku down or slow | 0 | None | KEEP code |
| 8 | Free offers under rounds = min(ours, theirs) once we're ahead in the count | ≈ +0.1 [L, rough] | A count-aware walk: a code change | KEEP for today |

**The six questions in one line each:**
- **(a)** Yes, C is robust to the overnight changes I could model. It beats A in every world but one, where all sets tie.
  The real risk is a format or wording change, which no set fixes (issue 2).
- **(b)** The switch rule's speed doesn't matter, because the switch is worth ≈ 0. A carries into the Final
  automatically unless someone re-runs the script.
- **(c)** Code policy is immune to a slow or dead Haiku: only the words change.
- **(d)** Yes, there is a cheap hedge: C+.
- **(e)** Fix the command, the terminal and the fallback ladder.
- **(f)** The plan doesn't exploit that waiting and accepting are free. C+ does, in part.

## 1. C+ : hold to the bound, accept on the last tick (questions d, f)

**The gap.** The Lab picked C, but by its own note, "C sits on the grid's corner, so more extreme values were not
tested". The cross-check's optimum (XC: hold, then one big final) lies further along the same axis. Two hot params move
C that way within their bounds (`params.py` SPEC):
- `MIN_STEP_P` (bounds 0-15): **15**;
- `ACCEPT_BY` (bounds 1-4): **1**.

**Both models, paired, against C** (12 ticks at 10%, code-first, openers 0.42 / 0.37) [L]:

| vs C, per duel | Lab sim3, past rivals (R1-R5 + fast, 36k duels, H1) | Lab, worst of 5 "overnight" worlds | Cross-check, base (share, 95% over 17 teams) | Cross-check, worst of 8 variants |
|---|---|---|---|---|
| `MIN_STEP_P` 15 | +0.018 ± 0.002 | −0.003 ± 0.003 (tough to the end) | +0.010 ± 0.013 | −0.003 (no deadline accepts) |
| `ACCEPT_BY` 1 | +0.011 ± 0.001 | +0.005 (harder anchors) | +0.032 ± 0.010 | +0.014 ± 0.006 |
| **Both (C+)** | **+0.029 ± 0.002** | **+0.007 ± 0.003** | **+0.042 ± 0.014** | **+0.014 ± 0.008** |
| Set A, for scale | −0.027 | — | −0.009 | — |

- **H2 agrees:** +0.027 for C+ against past rivals.
- **The two models split on `MIN_STEP_P` 15 alone:** clear in the Lab's (+0.018 ± 0.002), a wash in the cross-check's
  (+0.010 ± 0.013, from −0.003 to +0.012 across its variants). `ACCEPT_BY` 1 and the combination are clearly positive
  in both, in every variant (`xcheck_paired.out`).
- **C+ doesn't lower the deal rate:** 0.895 vs 0.889 in the Lab's model; 0.84 vs 0.84 in the cross-check's.
- **Mirrors** (`mirror.out`): sim3's mirror engine plays both sides with the models' drawn openers, not 0.42 / 0.37.
  Our C+ beats our C by +0.025 to +0.117 against all five opponents: today, A and C on the LLM policy, and C and C+ on
  code.
  - `ACCEPT_BY` 1 alone loses to the A opponent (−0.020).
  - The combination doesn't, though its deal rate there drops from 1.00 to 0.92.

**Why it fits the scoring.** Rounds = min(our priced offers, theirs), and accepts add no round. A hold sends nothing,
and waiting one more tick to accept costs no round by itself.
- **Mid-duel:** at 15, a step goes out only when 12% of the gap is at least 15 P, so the gap must be at least 125 P in
  worth (67 at 8).
- **The close:** the guard's minimum step becomes min(15, gap), so the close concedes up to 50% of gaps up to 30 P.
- **The result is XC's shape** (hold, then a larger final), reached with params. C's closing ticks and silent walk stay.

**The risk the models don't see: `ACCEPT_BY` 1 has no spare tick.** An accept refused on the last tick is not retried.

**The records say the risk is small [V]:**
- our two accepts sent at ticks_left 1 (2506, 6095) both settled on the deadline tick;
- 13 deals in sessions 1-3 closed on the deadline tick;
- none of our accepts was ever refused. The send errors in 136 records are 3 `wait_for_tick`, all on offers, and 2
  `bad_price`.

**ops-contention's model [L]:** with the trader, swaps and opps off and 2 dealer threads open during Duels III, it gives
0-6 key 429s an hour, 0-1.6 of them on the duelist, and 0 moves pushed a tick. The SDK's three retries absorb a
429 within 1.5 s.
- **Caveat:** that model's "0 lost deadline accepts" assumed `ACCEPT_BY` 2, so a spare tick. Under C+, a move pushed a
  tick at ticks_left 1 is a lost deal.

**Under that window, the expected loss is ≈ 0.001 a duel against a gain of 0.011-0.032 [L].**
- **With the trader on,** the model gives 0-16 duelist hits an hour and still 0 pushed.
- **With swaps and opps on as well,** it gives 0.1-2 pushed an hour.
- **So C+'s `ACCEPT_BY` 1 is conditional:** use it only while the trader, swaps and opps stay off in the duel window
  (§5). If they run, keep `ACCEPT_BY` 2 and take `MIN_STEP_P` 15 alone (+0.018 Lab, +0.010 cross-check).

**Stake:** +0.029 to +0.042 a duel × 102 duels = +3.0 to +4.3 raw ≈ **+0.5 to +0.7 Sunday points** (≈ +0.2-0.3 final).
That is more than C's whole edge over A.

**Fix: apply it after the start.** Not before: the start's `use C` would overwrite it.
```bash
WT=../team5-duelist-sunday
printf '{"wave": "C+ contra-duels", "params": {"MIN_STEP_P": 15, "ACCEPT_BY": 1}}\n' > "$WT/run/c_plus.json"
(cd "$WT" && python3 tools/duel_loop.py approve --proposal run/c_plus.json --by Aleks)
```
- **What you should see:** `MIN_STEP_P: 8.0 → 15` (`use` stores the float) and `ACCEPT_BY: default 2 → 1`. At the
  next tick the supervise log shows the `params:` change lines.
- **Why it's safe [L]:**
  - `approve` merges, so `_set` stays "C" and the auto-switch still works. A switch writes A whole, which puts
    `ACCEPT_BY` back to 2.
  - The limit checks in `final()` read no param, so no value of these two keys can push an offer past our limit.
- **Not run:** I read this in `duel_loop.py` (`approve`, `load_proposal`) but my session was refused permission to run
  it, even on a scratch params file. The Builder should dry-run it with `--params /tmp/x.json` first.
- **Undo:** `use C` (one tick).
- **Any script re-run reinstalls plain C:** re-apply the block above.
- **If any accept shows a `send_error`,** set `ACCEPT_BY` back to 2 the same way.
- **Not XC itself:** that is a code change, and the Lab's simulator says XC loses. C+ is the part of XC that both
  models favour.

## 2. No first-wave check, and the switch hides what it can't fix (questions a, b)

**The precedent.** The biggest duel loss on record is a reading failure:
- **Duels II wave 1** read every day weight as "direction unknown" and opened at day 5: 2 deals of 6 (team/aleks.md
  21:31).
- **The red team** measured: read right 0.47 a duel, direction unknown 0.23, unreadable 0.15, backwards −0.18.

**Why it is worse now.** Under the code policy, no model reads the words. `days.direction()` parses the game's English
("adds" / "costs").
- New wording gives `sure=False`, so our best day becomes 5: Saturday's wave 1 again.
- Flipped semantics give negative deals.
- A new issue gets every priced send refused with `missing_<x>`. The runner only repairs `missing_days`.

**Why the switch doesn't help.** On a collapse, the switch writes A: same reading, same code, same adapter. It can't fix
any of these, and then it is spent. A "SWITCHED C → A" line reads like the insurance worked.

**Stake.**
- **Probability:** ≈ 3-5% [?]. The 06:45 schedule shows unchanged settings.
- **Unnoticed through both sessions:** −0.24 to −0.65 a duel × 102 ≈ **−4 to −11 Sunday points**.
- **Caught after one wave:** ≈ −0.2 to −0.5.

**Fix: four checks** on the first new-duel lines and the first closed deal of Duels III (≈ 3 min in), and again at the
Final:
1. Every days duel's day line names a direction ("each day after day 0 costs you …", "… a bonus from day 0"). This
   prints nothing: `grep -E "direction unknown|CAN'T READ|refused" <newest $WT/logs/duelist/supervise-*.log>`.
2. For the first deal, `pred` = `points` in `uv run python -m agents.duelist review`. Run it from the checkout, where
   the live records are; `records.py` is identical on main and 29aa1be.
3. No `refused:` lines (a new issue).
4. At least one of the first four rivals that spoke reached a deal.

**If check 1 or 2 fails because the reading is reversed**, restart with the flip:
```bash
bash <(git show "${SHA}:tools/duelist_sunday.sh") --stop
COMMIT=$SHA SET=C AUTOSWITCH=1 FLAGS="--model claude-opus-5-5 --effort low --negotiator-model claude-haiku-4-5 --failover-s 8 --days-read flip" bash <(git show "${SHA}:tools/duelist_sunday.sh")
```
Then re-apply C+.
- **"Direction unknown" needs a code fix:** the `--days-read` modes are only auto, flip and unsure. On Saturday b7d91f3
  took about 10 min.
- **A SWITCH line in `$WT/logs/duelist/switch-*.log`** means: run the four checks before believing it.

## 3. The way back costs about 0.1 a duel; add the cheaper tiers (question e)

**What `--rollback` starts:** main's duelist on the LLM policy, at 15 s ticks:
- Saturday's flags: Opus medium strategist, Sonnet negotiator;
- main's Failover: 20 s, and cancellations don't count;
- no 6190 guards, no `MONO_END_SHARE`.

**What each option scores** (sim3, the same worlds) [L]:

| Option | Points per duel |
|---|---|
| C+ | 0.459 |
| C | 0.430 |
| A, code (hot `use A`) | 0.403 |
| A, LLM on the same sha (10% timeouts) | 0.377 |
| Main, LLM (31% timeouts) | 0.339 |
| Main, LLM (60% timeouts) | 0.336 |

- **The rollback costs** −0.09 a duel against C and −0.12 against C+. Pulled at the start of Duels III, that's
  **−1.5 to −2 Sunday points** over both sessions.
- **The swap itself** leaves 2-3 ticks with no moves (stop ≤ 10 s, tests, start). Any duel in its last ticks then can
  lose its deadline accept.

**Fix: pick the tier by symptom.** Time any restart just after a burst of deadline accepts, when one wave has ended and
the next has just started.

| Symptom | Action | Downtime | Cost vs C [L] |
|---|---|---|---|
| Deal rate low, rounds and prices sane, no errors (the set is too stiff) | `(cd "$WT" && python3 tools/duel_loop.py use A --by Aleks)` | none: next tick | −0.027 |
| The code policy misbehaves (odd prices, errors from `respond`) | `--stop`, then `COMMIT=$SHA SET=A POLICY=llm FLAGS="--model claude-opus-5-5 --effort low --negotiator-model claude-haiku-4-5 --failover-s 6"` with the start line | ≈ 30 s | −0.053 |
| The branch is broken (supervise crash loop, an offer past our limit) | `OLD_FLAGS="--effort low --negotiator-model claude-haiku-4-5"` before the `--rollback` line. Main takes Haiku [V]; Opus medium overruns the 10 s budget. `--status` then shows these flags, not Saturday's | ≈ 30 s | ≈ −0.09 |
| A day misread | Issue 2's restart | ≈ 30 s | — |

## 4. Ops: one block, a plain terminal, fresh briefs (question e)

**Three different start commands are in circulation:**
1. **The Delta audit's block:** `git show "${SHA}:tools/…"` with `AUTOSWITCH=1`. This one is correct.
2. **The Lab's morning check:** `AUTOSWITCH=1 COMMIT=29aa1be bash <(git show origin/duelist-loop:tools/…)`. The script
   comes from a moving ref.
3. **`docs/duelist-loop.md`:** `origin/duelist-loop` with `#` comments. In zsh the start line passes `#` as `$1`, so
   the script prints its usage and exits 2 (Delta audit [V]). It also never sets `AUTOSWITCH`, and the script's default
   is 0.

**Aleks's own docs are stale.**
- `intel/brief-aleks.md` says "Sunday: Sonnet as strategist".
- `team/aleks.md`'s Now line gives set A's values (cap 0.18, `MIN_STEP_P` 5, `LATE_SWITCH_LEFT` 2) as "Duel Lab picks
  for Duels III".

**The pipe hang.**
- **Cause:** `start_in` leaves a bash subshell that holds the script's stdout as the supervisor's parent. A pipe never
  closes: `| tee`, or a Claude Code Bash call, which captures output through one.
- **Through Claude Code** the call hangs until its timeout. Whether the harness then kills the process tree, and the
  duelist with it, is [?].
- **Rule:** start, stop and roll back only in a plain Terminal tab. If the script is ever touched again, the code fix
  is `exec nohup …` in both background subshells.

**The Lab's live check reads the records next to the script.** Run `tools/duel_gates.py` from the checkout:
- From `$WT` it reads the 29aa1be snapshot and says "fewer than 12" forever.
- Under C+, if the rule fires, it prints "live params are not set C: no switch". That tool only advises; the real
  switch keys on `_set` and would switch.

**The switch can stay silent (unlikely).** It acts only when the session's settings read (12 ticks, 10%) [V code].
- **Where it reads them:** from `docs/duels/feed.jsonl` (the sweep keeps the last 200 feed events a minute) or from
  each record's `session` object. The runner fills that object with a 500-event feed read as soon as it sees a duel of
  an unknown session.
- **If both miss `duels.scheduled`,** posted when a session starts (ticks 120, 459, 1239), the switch reads 16 ticks,
  never evaluates, and prints nothing [L: unlikely].
- **Check:** after the first closed wave, `$WT/logs/duelist/switch-*.log` shows a "switch rule HOLD" line.

**What Aleks keeps on screen:**
- `tail -f` of the supervise log and of the switch log;
- `--status` every ≈ 10 min;
- the monitor page, started from the checkout: `uv run python -m agents.duelist monitor`.

Under C+, expect more "hold, nothing sent" lines, more accepts at ticks_left 1, and ≈ 1.3-2 rounds per deal. The Lab's
"2-3" was for C.

**Stake:** an unnoticed misstart costs ≈ 0.3 Sunday points per wave; the wrong set (A) ≈ −0.45 Sunday points.

**Fix:** stage 2 carries exactly this block, and Aleks updates his Now line.
- The `approve` line is still unrun (§1): the Builder should dry-run it first.
- If it errors, it writes nothing and plain C plays.
```bash
git fetch origin
SHA=29aa1bed66962959ce633492d84bbc321385c7e7
COMMIT=$SHA bash <(git show "${SHA}:tools/duelist_sunday.sh") --check
COMMIT=$SHA AUTOSWITCH=1 bash <(git show "${SHA}:tools/duelist_sunday.sh")
WT=../team5-duelist-sunday
printf '{"wave": "C+ contra-duels", "params": {"MIN_STEP_P": 15, "ACCEPT_BY": 1}}\n' > "$WT/run/c_plus.json"
(cd "$WT" && python3 tools/duel_loop.py approve --proposal run/c_plus.json --by Aleks)
bash <(git show "${SHA}:tools/duelist_sunday.sh") --status
```

## 5. The plan's units, and a duel window that over-protects (question e)

**The units.** Stage 2 reads "≈ +7 with set C (+5.4 / +2.7 over today's setup)".
- **+7** is the duel part's level, in Sunday points (Analyst §4).
- **+5.4 / +2.7** are raw duel points.
- **C over today's setup** is ≈ +0.087 × 102 ≈ 8.9 raw ≈ **+1.4 to +1.8 Sunday points** (≈ +0.6 final), not +8.
- **So every set question is worth less than 1 Sunday point:** C vs A, the switch, XC, C+.

**The window rule.** At T−5 it stops the trader, swaps and opps, opens no new dealer threads and allows no restarts.

**What the dealer-thread ban buys: nothing measurable** (ops-contention, Duels III rows [L]):
- policy §6 alone: 0-1 key 429s an hour;
- policy §6 plus 2 dealer threads and a reactor wave (the CHA-release row): 0-6 429s an hour, 0-1.6 on the duelist,
  0 moves pushed a tick.

**What it costs:** ≈ 80 min of window [L] with no new dealer threads.
- That includes any CHA step still open at 10:55 (stage 1, +7).
- It also includes the dealers' last minutes before they close (warning 13:48, close ≈ 14:00).

**Fix.**
- **Allow the Operator's dealer threads in the window.** A stage-1 action never waits for a duel window.
- **Keep the trader, swaps and opps off, and freeze restarts.** With swaps and opps on, the model pushes 0.1-2 moves an
  hour a tick. Under C+, a push on the last tick loses the deal.
- **The trader alone** (0-16 duelist hits an hour, 0 pushed) took 2 accepts all Saturday. It isn't worth `ACCEPT_BY`
  1's margin.

## 6. The switch rule: harmless, nearly worthless (question b): KEEP

**Timing.** 12 rivals that spoke ≈ wave 4: 13-16 min into Duels III's ≈ 55, about halfway through the Final's ≈ 27.

| True deal rate with rivals that spoke | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.89 (C's expected) |
|---|---|---|---|---|---|---|
| P(the rule fires at the first look) | 0.94 | 0.81 | 0.56 | 0.28 | 0.07 | 0.007 |

**Speed doesn't matter.** The Lab puts the switch's whole value at ≤ 0.2 raw a session (≈ 0.03 Sunday points). A faster
rule (8 duels) misfires: the cross-check gives 12% at a true rate of 0.84.

**A is never the better set in the overnight worlds I modelled** (sim3, code-first) [L]:

| World | C | A |
|---|---|---|
| More silent rivals (20%) | 0.378 | 0.353 |
| Faster closers (40%) | 0.409 | 0.386 |
| Harder anchors | 0.381 | 0.337 |
| Holders (35%) | 0.395 | 0.373 |
| Tough to the end | 0.265 | 0.264 (a tie) |

**Into the Final.**
- **No restart:** A carries over by itself. The params file and the switch state persist, and `_switch` has no A entry.
- **After a switch,** any restart must pass `SET=A`. A plain re-run brings C back with the rule spent
  (`run/duel_switch_state.json` keeps `switched_from`).
- **Either way,** the value is ≈ 0.

## 7. Code vs LLM at 15 s; Haiku down or slow (question c): KEEP code

**The code policy [V code]:**
- Decisions are code, at ≈ 0.6-0.8 s.
- One Haiku call writes the words, capped at 3.5 s (`TEXT_TIMEOUT_S`). The client is async, so a hang stalls nothing
  else.
- If Haiku is down or slow, the call times out or raises `LLMError`, and code's plain words go out instead ("I can do
  57 P, delivery on day 10."). The numbers don't change.
- Two slow calls in a row trip Failover to Sonnet for 120 s, still under the same cap.
- An API outage or a spent credit limit changes only the words.

**The LLM policy:**
- Opus low plus Haiku must fit a 10 s budget. Failover at 8 s leaves the backup ≈ 2 s.
- Every overrun becomes `safe_move`, which never holds and skips the worth floor.
- sim3: A on the LLM policy with 10% timeouts scores 0.377, against 0.403 for A on code.

**Residuals:**
- An exception outside `LLMError` / `TimeoutError` in the text call turns that decision into `safe_move`.
  - In 903 recorded decisions there were 0 `error:` fallbacks [V].
  - But all 903 were Saturday's LLM-policy decisions. The code path's text call has never run live.
  - Leave it, and watch for `FALLBACK(error` in the supervise log.
- R5 (an unreadable weight) goes to the models. Issue 2 covers it.
- If the organisers cut the tick below 10 s, approve `TEXT_TIMEOUT_S` 1.5. It is hot, with bounds 0.5-8.

## 8. What rounds = min(ours, theirs) still leaves on the table (question f): KEEP for today

**C+ uses one part:** silence costs no round, and accepts add no round.

**Not used: free offers once we're ahead in the count.** When we have sent more priced offers than the rival, further
offers from us are free until they speak again.
- One-shot and sparse rivals (cross-check O, Q, E: 1-2 messages a duel, deal rates 0.62, 0.67, 1.0) go quiet after one
  offer.
- C and C+ still treat each of our steps as a round and hold until the last 3 ticks.
- A walk like the silent walk, started after their single offer, would cost no decay.
- **Stake:** ≈ +0.5 raw ≈ +0.1 Sunday points [L, rough]. It is a code change: not today.
