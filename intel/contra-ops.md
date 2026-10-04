# Contrarian ops review of intel/sunday-final.md (Sun 06:55, independent, no prior context)

Scope: timing, operations and single points of failure (SPOFs) of `intel/sunday-final.md`, plus the files it leans on (ops-contention,
dealer-lab §FAST-START + §4, chief-handoff, directives, daemons.sh, duelist_sunday.sh @ origin/duelist-loop 29aa1be, GAME.md,
score-model §4.7, PLAN.md, RULES.md, cha_book/mal_book, live-tuning). Read-only. No game calls: `BAZAAR_URL` is unset in this
environment, so the keyless clock/schedule reads were skipped. Local checks only: process command lines, `run/` files, one local
`uv` signal test. Tags: **[V]** verified here (file, code or process) · **[L]** likely · **[?]** open.

## 0. Bottom line

1. **The case call at 08:55 cannot work.** At 06:45 the clock read `round 2, paused, doors closed, t 13.367` [V `run/archiver.json`], and it will read the same at 08:55.
   Decide at the **first live tick**. Fire CHA on the **catalog `released` flag**, and take duel times from **`/api/schedule`,
   recomputed at every event**. That gives three signals and three triggers; today's plan rolls them into one read.
2. **The money-critical t+0 depends on things that fail.** It needs a Claude Code session that may be waiting on a permission
   prompt, scripts that live only in `/private/tmp`, and Lucas, who is booked at the organisers' desk at 09:00. Arm one
   deterministic background job at 08:45 instead.
3. **Several daemons are still running Saturday's settings** [V `ps`]. `opps` runs `--build RET,CHA` at floor 350, so it would
   post CHA bids up to book (70 for a rare) against the 54 cap. `book` runs `--cash-floor 350`, which blocks the rare bids until
   the +150 lands and caps all CHA bids at 192 P after that. The documented fix (`OPPS_BUILD=RET`) has a side effect: opps would
   then **sell our only CHA copies**, because CHA is not in `run/reserved.json` [V code].
4. **The duelist start is pinned to 10:30 wall time, and the files give three different Duels III times** (10:00 PLAN #31,
   11:00 sunday-final, 11:29 Aleks's Now and cha-plan). Start it at R+5 min (idle polling ≈ 9 % of the key) and stop guessing.
5. **The CHA dealer timers run into Duels III** (Abuela t+440/t+480 ticks = 10:50/11:00 at 15 s ticks) [V cha_book]. Chain the
   Pícaros rares (CHA → MAL) at t+0. Finish Abuela by D3−20.

## 1. Issues ranked by impact (expected loss × probability)

### #1 HIGH: t+0 has no reliable trigger, and its decision rule reads a value that cannot change before 09:00
- **Break (a).** sunday-final says "The Operator decides at 08:55 on `/api/clock` `round`". The clock is closed and paused
  until the doors open, so 08:55 shows round 2 in **both** cases [V archiver.json 06:45: `"round": 2, "paused": true,
  "doors": "closed"`]. A literal reading calls case A and skips the CHA race. A careful reading stalls until someone notices. On
  Saturday the first tick came about 29 min late ("late open"; ticks 630→632 took 2 h 05) [V GAME.md, redteam §1.1], so any
  "09:00" in the plan is really "R".
- **Break (resume then jump; CHA after round 3).** The decision mixes three questions:
  - Which round do our deals count in? That is `round` at the first tick.
  - When do duels and the dealers' close happen? That is `/api/schedule` `at_hours − t_hours`, which moves on every re-anchor
    (the "hybrid" case puts Duels III at 14:17).
  - Can we buy CHA? That is the catalog's `released` flag.
  If the clock resumes and then jumps at, say, 09:40, or if CHA is released after round 3 starts, a plan keyed to 08:55 or
  09:00 fires early or late. Specific failure modes:
  - The silver pack is opened before CHA exists, so it cannot pull CHA.
  - The Pícaros CHA thread fails on an unreleased card. `simple_buy`'s `open_thread` is unguarded [V ops-contention §5b], so it
    crashes.
  - The book posts bids for unreleased cards every tick.
- **Break (who presses the button).** Today the t+0 steps are typed by the Operator session:
  - That session has been alive since Sat 09:34 [V run/operator.lock], about 21 h of compacted context.
  - It wakes from a 600 s sleep loop at about **08:44** [V process 11431: `while [ $(date +%H%M) -lt 0840 ] … sleep 600`]. It
    then has about 15 min for a 9-item checklist plus the case call.
  - Its scripts (`simple_buy.py`, `rbuy.py`, `deny.py`, `wait_duels_end.py`) exist only in
    `/private/tmp/…/b5f4f4ed…/scratchpad` [V]. A reboot deletes them, and no other machine has them.
  - Any permission prompt at 09:00 waits for Lucas, whom sunday-final sends to the desk at 09:00 (stage 6).
- **Fix.**
  1. **Builder, by 08:20:** copy the Operator scripts into `tools/sunday/` and commit them. They read keys from the
     environment [V], but `simple_buy.py` hard-codes Lucas's repo path in `sys.path` [V]. Also copy
     `run/{cha_book,mal_book,book_cha_entries,reserved}.json` there.
  2. **Builder, by 08:20:** write `tools/sunday/t0.sh` (sketch in §3) and dry-run it against keyless reads.
  3. **Operator, 08:45:** start `t0.sh` in the background (one approval) and leave it alone.
  4. **Chief, now:** SendMessage the Operator to wake at **08:15**, not 08:44, so the checklist runs while the game is closed.
  5. **The rule:** the case = `round` at the first tick with `doors == "open"`, `paused == false` and `tick > 1445`. A round-2
     reading at 08:55 means nothing.

### #2 HIGH: the live daemons contradict the directives [V `ps` 06:50]
| Process | Running now | Problem | Fix (08:35, game closed, zero contention) |
|---|---|---|---|
| `opps` (since Sat 21:39) | `--build RET,CHA`, CASH_FLOOR 350 [L lucas.md 21:37] | Posts **addressed CHA bids at book** (rare 70, up to value − 3 = 109) [V opportunities.py:15] against directive 00:35 (CHA/MAL only via the books) and the 54/22/9 anti-flip caps. It also risks a double buy with the book and the Pícaros | `tools/daemons.sh stop opps` now. Start it at R+10 with `OPPS_BUILD=RET CASH_FLOOR=464` (case J only) |
| `opps` with `OPPS_BUILD=RET` (the documented fix) | — | CHA drops out of `protected` = build ∪ complete ∪ LAV [V :388], so a **single CHA copy counts as "spare"** [V :404-409] and opps offers it for sale. CHA is not in `run/reserved.json` [V] | **Add CHA-01..CHA-10 to `run/reserved.json`** (atomic write) before R. That also covers swaps. The trader already keeps CHA through `--build` [V loop.py:52, 283] |
| `book` (since Sat 21:34) | `--cash-floor 350 --min-gain-sell 2` | room = cash − open bids − 350 [V book.py:374]. Before the +150: 42 P, so the rare bids at 48 are skipped. After it: 192 P, against 219 P of CHA bids at caps, so some bids are skipped | `CASH_FLOOR=0 MIN_GAIN_SELL=2 tools/daemons.sh restart book` at 08:35 (book.json then holds only the 2 LAV asks). Check that `pgrep -fl agents/trader/book.py` shows exactly 1 |
| `intel/live-tuning.md` §2 | — | Its "hard limit" for team bids is **rares 90, uncommons 30, commons 12**, so the Operator may raise the public CHA bids past the 54/22/9 caps on an Analyst line | Chief: one-line fix to that limit: public CHA bids ≤ 54/22/9; anything higher addressed, pre-agreed, non-rival only |
| `reactor` BUY lines + `rbuy.py` (standing rule Sat 21:31) | — | A CHA ask at 80 is a valid BUY line (112 − 80 − fee ≥ 15), which breaks "CHA/MAL only via the books" | Operator ignores BUY lines on CHA-*/MAL-*. Builder: a one-line filter if there is time |

### #3 HIGH impact, low-to-moderate probability: the duelist start is a fixed wall time while Duels III is uncertain
- **Break (c).** Duels III appears as ≈ 10:00 (PLAN #31: "live and tested by 09:55"), ≈ 11:00 (sunday-final, ops-contention: start
  at 10:30) and ≈ 11:29 (team/aleks.md Now, cha-plan). PLAN.md stops at #31 [V], so Aleks has no #32 with the sha or the
  corrected time. Any re-anchor moves D3. If D3 falls before Aleks's start, whole waves get **no reply, which scores 0**. That is
  ≈ 0.1 Sunday pts per duel, 4 duels per wave.
- **Second-order effect.** If the Saturday duelist (f92fe34) is still up on Aleks's Mac, `--check` and the start both die at step 1
  ("already running") [V duelist_sunday.sh]. If nobody stops it, Saturday's code plays Duels III.
- **Fix.**
  - Aleks runs `--status`, then `--stop` if a duelist is up, then `--check` at 08:30, and **starts at R+5 min** in every case.
    Idle cost: 0.43 req/s ≈ 9 % of the key, after the 3-tick t+0 burst [ops-contention §2].
  - Chief: write PLAN #32 now (sha 29aa1be, start at R+5, D3 from `/api/schedule`, the exact commands in §3).
  - If the Final would end after 14:58, the 15:00 close can cut it. Duels then score 0 [?]. Aleks watches the schedule at 13:30.

### #4 MED: the CHA/MAL dealer timetable runs into Duels III
- **Break (c, e).** The cha_book `after_ticks` values for Abuela are 240/300/360/400/440/480 and 840 [V]. At 15 s ticks that is
  10:00, 10:15, 10:30, 10:40, **10:50, 11:00** and 12:30. The 01:30 policy forbids new dealer threads after D3−15 (10:45).
- MAL is gated "after CHA", and CHA isn't finished until CHA-08 at 12:30. So MAL-09/10, fodder sales and RET-11 → Pilar all
  crowd into the **11:52-13:45** window (Pícaros 6 deals per team per hour; rare stock per hour [?]).
- **Fix.**
  - MAL fits by construction: 542 − worst-case CHA 282 = 260 ≥ 150 [V dealer-lab: "the full MAL runs in every case now"]. So
    **chain the four Pícaros rares in one background job: CHA-09 → CHA-10 → MAL-09 → MAL-10**. The dealer allows one thread
    at a time anyway. `simple_buy` exits on "already hold" [V], so the chain is idempotent.
  - Abuela fallbacks run from **C+60 (10:00) to D3−20 (10:40)**, one thread at a time (6 deals fit the 8 per hour).
  - Whatever is still missing at D3−20 waits for `duels.finished`. CHA-08/05 stay the "last card" pair, from teams.

### #5 MED (low probability, catastrophic): one Mac, auto-pulls, and state that exists only there
- **Break (d).**
  - Lucas's Mac runs the Operator, every daemon, the analysts and all of `run/`, which is gitignored [V].
  - The network outage at 22:50-23:24 showed up only afterwards: book, swaps, duelmon and news still show DNS errors as their
    last log lines [V `daemons.sh status`].
  - `team_sync.sh` runs `git pull --rebase --autostash` **on every prompt in every session** [V]. Any code pushed to main
    (Builder, Aleks's auto-sync) lands under the running daemons and goes live at the next supervised crash-restart or at the
    11:52 restart.
  - Memory note: autostash has already leaked conflict markers into the tree once.
  - Already fine [V]: `caffeinate -dimsu` is running and the Mac is on AC. caffeinate does not stop lid-close sleep [L]:
    **keep the lid open**.
- **Fix.**
  - Code freeze on main 08:40-15:00: the Builder pushes to branches only. The Operator writes `git rev-parse HEAD` to
    `run/ops_sha` at 08:35, and before any restart `git diff --stat $(cat run/ops_sha) HEAD -- agents tools engine` must be
    empty.
  - Hotspot drill at 08:30 (2 min): join, `curl` the clock, rejoin.
  - Close every Claude Code session except Chief, Operator and Market by 08:45. That means fewer prompts, fewer pulls and
    fewer permission waits.
  - Lucas pre-allows the exact run-sheet command prefixes in his settings if he wants zero prompts. Only Lucas can change
    permissions.
  - Backup Operator is Aleks's Mac: the scripts and books are now in git (#1). It needs only the `.env` it already has.

### #6 MED: duel-window triggers are manual, with fixed fallbacks and blank floors
- **Break (c).**
  - Who stops at T−5? The Operator, by hand.
  - The restart fallback is `--until 1230`, a fixed time [V ops-contention §6]. If D3 slips to 11:45, the bots come back
    mid-wave.
  - The restart commands carry `<trader floor>` / `<opps floor>` placeholders. A bare `daemons.sh start` falls back to
    **CASH_FLOOR=100 and OPPS_BUILD=RET,CHA** [V daemons.sh].
  - Opps' floor is never specified anywhere.
  - `uv` forwards SIGTERM, so `stop` leaves no orphan book or swaps [V local test: the grandchild python died]. The pgrep check
    stays as a cheap guard.
- **Fix.**
  - Keep the floors in **`run/floors.env`** (`TRADER_FLOOR=`, `OPPS_FLOOR=`). Every start sources it, and the Operator edits
    only that file.
  - Arm a `window.sh` job: every 60 s it reads keyless `/api/schedule` + `/api/clock`. At D−5 it runs
    `stop trader swaps opps recorder` and the pgrep check. On `duels.finished`, or **D + 65 min** (not 12:30), it restarts
    trader, then opps, then swaps, 15 s apart, from `floors.env`.
  - Add `recorder` to the stop list: the broker key's share of 5/s is [?], and the 11:21 bench falls inside Duels III.

### #7 MED-LOW: the silver pack races the Pícaros at t+0
- **Break (b).** FAST-START puts the Pícaros CHA-09 thread (offer-only, so the dealer can accept any tick) at t+0, and the pack at
  "right after CHA's release". If the pack pulls CHA-09 or CHA-10 while that offer stands, we buy a second rare at ≈ 50, worth
  28 to us: **−22 to −26 np** (dealer losses count in full [V GAME.md]).
- **Fix:** **pack first (1 request), then the Pícaros chain, then the book merge 2 ticks later.** Every CHA card is missing at C,
  so the ≥ 2-missing gate holds. A pulled rare also saves ≈ 50 P.
- Residual, accepted: the public rare bid and the Pícaros can settle in the same tick. Book cancels a bid only one tick after the
  card arrives [V book.py:24]. No team holds a CHA rare at C [redteam §1.2], so this is rare.

### #8 MED-LOW: the end of the day strands cash and cards (e)
- **Break.**
  - The trader floor is 464 = CHA 288 + MAL 126 + 50, "lowered as the books fill", but nobody owns lowering it. As CHA is
    spent, cash falls below 464 and the trader and opps stop buying for the rest of the day.
  - Expected idle cash at 15:00: 542 − (242..282) − 126 − fodder ≤ 60 ≈ **74-174 P, worth 0** ("only deals score").
  - Dealers close ≈ 14:00 (warning 13:48) and the Final window starts at F−5. In practice that means **the last dealer thread
    at 13:45**.
  - Fodder bought after ≈ 13:15 can't be resold to Pilar/Chato.
  - A last-card team deal accepted in the final tick may never settle [?].
- **Fix (floor schedule in `run/floors.env`, every buy still at gain ≥ 3):**
  - after the Pícaros chain: floor = remaining planned spend + 50 (≈ 300);
  - at 13:00: 100;
  - after the Final, or at 14:30: **0**.
  - Remove the fodder bids from book.json at 13:15.
  - At 13:30, if two or more CHA cards are still missing, buy all but one from dealers before 13:45, so the last one can close by
    team trade.
  - Settle CHA's last card and MAL-07 (Team 15, v26) **by 14:45**.

### #9 MED: human load and double-booking (f)
- **Break.**
  - At 09:00 sunday-final puts Lucas at the desk (stage 6) and also in charge of every Operator approval and the case relay.
  - The 08:30 WhatsApps are all on Lucas: RET-09 and SAL-02 pairs, Team 16 rows after the rival check, Team 15 MAL-07.
  - The CHA last card must be "pre-agreed" with a non-rival holder, but **no team holds a CHA card before C**, so it can't be
    agreed at 08:30.
  - Aleks is idle until D3; Dani is the natural sender.
- **Fix.**
  - **Aleks asks the desk question at 08:40** (before the doors) and records the answer.
  - **Dani sends every pair text at 08:30.** Sellers post now; **buyers accept only on our "GO" after R** (see #11).
  - Lucas sits at the Mac 08:45 → R+20, then hunts the CHA last-card holder with Dani from R+15. The reactor and feed show who
    pulls CHA-05/08.
  - The morning then needs about 3 human actions each.

### #10 MED: six files give six different instructions for the same 30 minutes
- **Break.**
  - Trader: 09:00 (sunday-final) vs t+2 min (ops-contention) vs 08:45 (dealer-lab §4 #3).
  - Duelist: "up before 09:00" (sunday-plan) vs 09:55 (PLAN #31) vs 10:30.
  - "09:00 Pícaros estampita thread" (dealer-lab §4 #7, sunday-plan) occupies the one-per-dealer slot that CHA-09 needs at C, and
    the egg is already earned (badge 'Trickster tricked') [V GAME.md].
  - The §4 #5 cancels are already done [V lucas.md 01:33, Sat 23:43].
- **Fix:** Chief adds one banner to sunday-plan, dealer-lab §4 and ops-contention §6: "superseded for 08:30-11:00 by
  intel/contra-ops.md §3". Drop the 09:00 estampita and Abuela-cocido text threads: the egg line rides inside the priced CHA-09
  message.

### #11 LOW-MED [?]: overnight v10 pairs settling on the boundary tick
- If a buyer accepts while closed, it settles at the first tick, which is also when round 3 fires. Whether that settlement counts
  in round 2 (closed day) or round 3 is unknown. The 7.5 real-trades target needs RET-09 on **Sunday**.
- **Fix:** sellers post early, buyers accept on "GO" (R plus 1 tick). The cost is one minute.

### #12 LOW-MED: Aleks's Mac, and running two duelists on a takeover
- `duelist_sunday.sh`'s single-instance check is a **local** `pgrep` [V]. If Aleks's Mac drops off the network and Lucas starts a
  backup, two duelists run on one key once it reconnects. That means double messages and double decay.
- **Fix.**
  - Aleks: `caffeinate -dimsu &`, power plugged in, lid open, hotspot ready.
  - Takeover only after Aleks runs `--stop`, or his Mac is powered off. Then on Lucas's Mac:
    `COMMIT=$SHA AUTOSWITCH=1 bash <(git show "${SHA}:tools/duelist_sunday.sh")`.

### #13 LOW: Anthropic API outage
- Duelist: with `--policy code`, code decides, and a failed text call falls back to plain text (`move.text = text or plain(…)`),
  then `safe_move` [V policy.py:157-167, agent.py:7]. It degrades and doesn't stop.
- The analysts are advisory.
- Claude Code sessions stop: then **Lucas runs §3 from a terminal**. That is why §3 is commands, not prose.

## 2. Direct answers

- **(a)** The `round` rule is right for *which day scores*, but it must be read at the first live tick, never at 08:55 (#1).
  Duel times come from `/api/schedule`, recomputed each event. CHA actions fire on the catalog's `released` flag.
  - Resume, then a later jump: the t0 job just keeps waiting for C.
  - CHA released after round 3: the R rows run, and the C rows wait.
  - CHA released while still round 2: page the Chief. Default [L]: run only the Pícaros rare chain (print-run race; 0 np either
    way); hold the book, Abuela and the last card until round 3 (Saturday's ladder and trade part are capped).
- **(b)** Order in §3:
  - C: pack, then Pícaros CHA-09 (on a full token bucket).
  - C+2 ticks: book merge, by atomic `mv`.
  - R+5: duelist.
  - R+10: trader, then opps (`OPPS_BUILD=RET`), then swaps, 15 s apart.
  - The +150 lands about 3 min after the open (CHA bids fit within 392 P with book floor 0).
  - Only one Pícaros thread exists, so no race on the dealer slot.
- **(c)** D3 ≈ 11:00-11:51 and F ≈ 14:00-14:27 only if the clock jumps at 09:00. Triggers come from the schedule:
  - no new dealer thread from D−20;
  - open threads closed by D−5;
  - stop at D−5 (by `window.sh`, not by hand);
  - restart on `duels.finished`, or D+65.
  - Early D3: the duelist is already live from R+5.
  - Late D3: the stop just moves with it.
- **(d)** #1, #5, #12, #13.
- **(e)** #8.
- **(f)** #9.

## 3. Run sheet 08:30 → 11:00

**Anchors.**
- **R** = first tick with doors open, not paused, tick > 1445.
- **C** = CHA `released` in the keyless `/api/catalog`.
- **D3** = Duels III start = `now + (at_hours − t_hours)` from `/api/schedule`, recomputed at R, C+1 min, 10:30 and every event.

Wall times assume case J with R = C = 09:00 and D3 = 11:00. If R slips, shift every R/C row; D3 rows follow D3.
`SHA=29aa1bed66962959ce633492d84bbc321385c7e7`. Floors live in `run/floors.env`.

| Time | Who | Action (exact) | Done when |
|---|---|---|---|
| 08:15 | Chief | SendMessage the Operator: wake now, run dealer-lab §4 while the game is closed. Write PLAN #32 (sha, start R+5, this sheet) | Operator acknowledges |
| 08:15-08:30 | Builder | `cp <op-scratchpad>/{simple_buy,rbuy,deny,wait_duels_end,fast_start_dry,dealer_sell}.py tools/sunday/`, plus the four run/*.json books. Write `t0.sh` and `window.sh` (below). Dry-run them keylessly, commit, push. **Then no code pushes to main until 15:00** | `git log -1 tools/sunday` |
| 08:30 | Aleks | `caffeinate -dimsu &` · power · `COMMIT=$SHA bash <(git show "${SHA}:tools/duelist_sunday.sh") --status` → if a duelist is up: `… --stop` → `… --check` | "steps 1-4 passed" |
| 08:30 | Lucas | Hotspot drill (2 min). Close every Claude Code session except Chief, Operator and Market (Builder after 08:30) | 3 sessions |
| 08:30 | Dani | Pair texts (market-sunday §0.5): RET-09 t07→t09, SAL-02 t09→t07, Team 15 MAL-07 on v26. "Sellers post now; **buyers accept when we say GO**" | sellers confirm |
| 08:35 | Operator | `git pull` (clean tree, no stash) → `git rev-parse HEAD > run/ops_sha` | sha logged |
| 08:36 | Operator | Add CHA-01..10 to `run/reserved.json` (write to a tmp file, then `mv`) · `tools/daemons.sh stop opps swaps recorder` · `pgrep -fl "tools/opportunities.py|agents/trader/swaps.py"` prints nothing (plain `|`: macOS pgrep reads an extended regex, so `\|` matches nothing and gives a false all-clear, per ops-contention §6) | reserved has 28 refs |
| 08:38 | Operator | `CASH_FLOOR=0 MIN_GAIN_SELL=2 tools/daemons.sh restart book` · `pgrep -fl agents/trader/book.py` → exactly 1. **Trader stays at 9999** | book log "closed" |
| 08:40 | Operator | Stage `run/book.sunday.json` = book.json + `book_cha_entries.json` + LAT-06/07/08 buys ≤ 12 on v15. Check with `python3 -c 'import json;json.load(open(...))'`. **Do not move it into place** | file valid |
| 08:40 | Aleks | At the organisers' desk: the Market Test question (sunday-final #6) → team/aleks.md + Chief | answer logged |
| 08:42 | Operator | One keyed read of our open threads → close any dealer thread (none expected; one per dealer) | 0 dealer threads |
| 08:45 | Operator | `printf 'TRADER_FLOOR=464\nOPPS_FLOOR=464\n' > run/floors.env` · start **`t0.sh`** and **`window.sh`** in the background (one approval each) · heartbeat | both logging "waiting" |
| 08:50 | Lucas | At the Mac until R+20. Lid open | — |
| 08:55 | Operator | Keyless clock + schedule read. **Expect "closed, round 2": this is not the case call.** List each event's `at_hours`. Team chat: "armed" | posted |
| 08:59 | everyone | No hand-typed keyed commands until R+2 | — |
| **R** (09:00:00-15) | t0.sh | Logs `round`, `t_hours`. **round 3 → J** (continue). **round 2 → A** (branch below) | log line |
| R+0 | Operator → Dani | Team chat "R3 live, GO" → Dani tells the pair buyers to accept | buyers ack |
| **C** (same tick in J) | t0.sh | (1) open silver pack 1013 (1 req). (2) background **Pícaros chain** (below). Book untouched | chain log shows `open_thread` ok |
| C+30 s | t0.sh | `mv run/book.sunday.json run/book.json` (atomic). book.py posts ≤ 6/tick over 3 ticks | book log: posts |
| C+1 min | Operator | One `/api/me`: cash (has the +150 landed?), pack pulls, CHA held. Recompute D3, F and dealer close → team/lucas.md Now + chat | times posted |
| C+1 → C+10 | t0.sh chain | CHA-09 (open 42, +2, cap 54; walk on final ≥ 57 → reopen once at cap 57) → CHA-10 (same) → MAL-09 → MAL-10 (open 40, +2, cap 49, reopen once). Operator watches for `TRICK` / `walk` / `closed_reason` | 4 rares or a logged reason |
| R+5 (09:05) | Aleks | `COMMIT=$SHA AUTOSWITCH=1 bash <(git show "${SHA}:tools/duelist_sunday.sh")` → `--status`: 1 process, set C | idle polling |
| R+10 (09:10) | Operator | `set -a; . run/floors.env; set +a` · `CASH_FLOOR=$TRADER_FLOOR tools/daemons.sh restart trader` · wait 15 s · `OPPS_BUILD=RET CASH_FLOOR=$OPPS_FLOOR tools/daemons.sh start opps` · wait 15 s · `tools/daemons.sh start swaps` · `tools/daemons.sh status` | all running |
| 09:15 | Lucas + Dani | CHA last-card hunt: which **non-rival** team pulled CHA-05/08 (feed, reactor) → agree one addressed post, ≤ 72 for a common, ≤ 96 for an uncommon | holder named |
| 09:15 | Analyst | First live-tuning line (bands per the corrected §2 caps) | file updated |
| 09:20 | Lucas | Leaves the Mac. The Operator is autonomous | — |
| 09:21 | — | Bench (stall): nothing | — |
| ≈ 09:30 | Operator | Chain done → `floors.env` TRADER/OPPS = remaining planned spend + 50 (≈ 300) → restart trader, then opps, 15 s apart | floors logged |
| 09:45 | Dani | Second-wave pairs (Team 16 rows after the rival check) | — |
| 10:00 (C+60) | Operator | **Abuela chain**, one thread at a time, only cards still missing (caps per cha_book): CHA-06 → CHA-07 → CHA-01..04. Guard: no new thread after D3−20. Fodder, if LAT has landed: Pilar thread (> 16) in parallel | threads close |
| 10:00 | Operator | If the chain hit `persona_quota`/`sold_out`: rerun the rest of the Pícaros chain now (new hour) | — |
| 10:30 | Operator + Aleks | Re-read the schedule and confirm D3 · `window.sh` shows the stop time · Aleks `--status` | D3 confirmed |
| **D3−20 (10:40)** | Operator | Last new dealer thread. Remaining CHA/fodder deals → after `duels.finished` | — |
| D3−10 (10:50) | Operator | Open dealer threads close by D3−5 (walk if needed) · `tools/daemons.sh status` | 0 dealer threads |
| **D3−5 (10:55)** | window.sh | `tools/daemons.sh stop trader swaps opps recorder` + pgrep check. No book.json edits, no restarts, no dealer threads | pgrep prints nothing |
| D3 (11:00) | Aleks | Wave 1 at the screen. Announce in chat. AUTOSWITCH runs | — |

**Case A branch (R shows round 2).**
- Dani sends GO for the v10 pairs (Saturday points).
- Trader stays at 9999. **Opps stays stopped** (no cash team trades in the tail).
- Swaps start at R+10 (0-cash swaps are fine). No dealer threads (Saturday ladder is capped).
- Aleks still starts at R+5.
- `t0.sh` keeps waiting. When round 3 and C arrive, run the sheet from the **C** row.
- `window.sh` follows the schedule.

**CHA later than round 3.** Run the R rows. C rows fire at C. If C falls inside D3−20 … `duels.finished`, still run the pack, the
Pícaros chain and the book merge (ops-contention §6: 0-6 429s an hour with trader, swaps and opps off). Abuela waits.

**After 11:00 (for #8).**
- `duels.finished` or D3+65 → `window.sh` restarts from `floors.env`.
- 11:52-13:45: CHA-08 (Abuela, if CHA-08 and CHA-05 are both missing), leftover CHA/MAL, fodder → Pilar > 16 then Chato > 13,
  RET-11 → Pilar ≥ 198.
- 13:00: floors 100. 13:15: fodder bids out of book.json. 13:30: all-but-one CHA in hand. 13:45: last dealer thread.
- F−5: `window.sh` stop. After the Final, or at 14:30: floors 0.
- Last-card and MAL-07 deals settled by 14:45. 15:00: doors close.

**`t0.sh` sketch (Builder; deterministic, keyless polling, about 30 lines).**
```bash
#!/usr/bin/env bash
# Waits for R, then C; fires pack → Pícaros chain → book merge. Never retries a buy blindly; logs everything.
R=/Users/lucaswiese/Documents/claude-hackathon-team-5; set -a; . "$R/.env"; set +a; O="$R/tools/sunday"; L="$R/logs/t0.log"
j() { curl -s --max-time 5 "$BAZAAR_URL$1"; }
until j /api/clock | python3 -c 'import sys,json;c=json.load(sys.stdin);sys.exit(0 if c["tick"]>1445 and c.get("doors")=="open" and not c.get("paused") else 1)'; do sleep 2; done
echo "$(date +%T) R $(j /api/clock | python3 -c 'import sys,json;c=json.load(sys.stdin);print(c["tick"],c["round"],c["t_hours"])')" >> "$L"
until j /api/catalog | python3 -c '<exit 0 iff the CHA set is released>'; do sleep 3; done   # Builder: match the catalog's field
echo "$(date +%T) C" >> "$L"
<open silver pack 1013 (Operator's call)> >> "$L" 2>&1
EGG='Conozco el timo de la estampita, como Lazarillo y Rinconete. Sin trucos, ¿eh? {p} P por la carta.'
B() { python3 "$O/simple_buy.py" "$1" --dealer picaros --open "$2" --step 2 --cap "$3" --floor-cash 0 --offer-only --first-text "$EGG"; }
cutoff() { [ "$(date +%H%M)" -lt "${STOP_HHMM:-1040}" ]; }   # D3−20; the Operator exports STOP_HHMM if D3 moves
( for c in CHA-09 CHA-10; do cutoff && { B $c 42 54 || B $c 42 57; }; done
  for c in MAL-09 MAL-10; do cutoff && { B $c 40 49 || B $c 40 49; }; done ) >> "$R/logs/picaros_chain.log" 2>&1 &
sleep 30; python3 -c 'import json;json.load(open("'"$R"'/run/book.sunday.json"))' && mv "$R/run/book.sunday.json" "$R/run/book.json"
```
`window.sh` follows the same pattern: a 60 s loop on the keyless schedule and clock. At D−5 it runs `daemons.sh stop trader swaps
opps recorder` plus the pgrep check, then waits for `wait_duels_end.py "<session>" --until <D+65>`, then starts trader, opps and
swaps 15 s apart from `run/floors.env` (with `OPPS_BUILD=RET`).

## 4. Limits of this review
- No live clock or schedule read (no `BAZAAR_URL` here). D3/F come from the files ([L] wall times).
- The catalog's `released` field name, the pack-open call and the Pícaros hourly rare stock are not checked [?].
- The ranking is my judgment (impact × probability), not a simulation. The 429 numbers are ops-contention's.
