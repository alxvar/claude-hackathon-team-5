# Ops audit: who shares the team key on Sunday (independent auditor, Sun 01:30)

Read-only audit of the code (main + `origin/duelist-loop` 3a0f6f3 + the Operator's scratchpad scripts), Saturday's logs
and a token-bucket simulation. No game call was made. Tags: [V] verified in code, logs or the organisers' deck ·
[L] likely (model or inference) · [?] open.

## 0. Bottom line

1. **The duel accept cannot lose the market's accept to the trader or a dealer bot, and duels don't use up our 6
   conversations** [V, §1]. Two of the feared collisions don't exist.
2. **The real shared resource is 5 requests/s per key (bursts of 20).** With everything on at 15 s ticks, the key runs
   at **73-92 % of capacity** during Duels III. The trader alone takes ≈ 1.6 req/s, 32 % of the key (≈ 24 requests per tick, 18 of them venue boards).
   Every daemon fires in the first 0-4 s after the tick, the same seconds as the duelist's moves. Model: **30-700
   429s per hour** (≈ 300 at 0.15 s latency), **8-180 of them on the duelist** [L, §3].
3. **Damage to duels is small, not zero.** The SDK's 3 quick retries (1.5 s) absorb almost every 429. In the model,
   0-2 duel moves an hour slip a full tick, and no deadline accept is lost. The duelist logged 0 `rate_limited`
   send errors in 136 recorded duels (34 Friday practice, 102 Saturday) [V]. The insurance is cheap, though: on Saturday the trader took **2 accepts all
   day** [V], so pausing it, swaps and opps for the waves costs ≈ nothing. With them off: **0-1 429s an hour at every
   latency tested** [L].
4. **Nothing gives the duelist priority** [V]. The arbiter only gates accepts and is off (`ARBITER_HOLDS` unset,
   correctly). The only lever is the Operator stopping daemons, as on Saturday (job by05m2zep).
5. **Policy, §6:** the Operator runs `tools/daemons.sh stop trader swaps opps` at T−5 min before Duels III and before
   the Final. There are no dealer threads, no `run/book.json` edits and no restarts inside a window. Resume when
   `duels.finished` appears, one daemon per tick, **with the floors spelled out** (daemons.sh defaults to
   `CASH_FLOOR=100`). Aleks starts the duelist at 10:30, not 08:30. Its idle polling is ≈ 9 % of the key during the CHA rush.

## 1. Settled facts

| Question | Answer | Evidence |
|---|---|---|
| Does a duel accept use the team's 1 accept/tick? | **No** [V] | Organisers' Duels deck (Downloads/The Bazaar - Duels.pdf, p.3): "Duel messages and accepts have their own limits: they never block your trading." Also organisers Sat 16:55 (runner.py docstring, directives 16:55). |
| Do duels count in the 6 open conversations? | **No** [V] | Sat 22:20:55-22:21:02 (`logs/egg-madrid.log`): 5 dealer threads opened (2099-2104: chato, abuela, picaros, pilar, banco) at tick 1367. At that tick 6 of our duels were live (6085, 6101, 6182, 6177, 6007, 6190; `docs/duels/*.json` first/last ticks) and 4 more were ending. Desk Q6 can close. |
| Does the 5 req/s cover duel requests? | **Yes, assume so** [L] | Same key, same server (deck p.2). "Their own limits" refers to the per-tick message and accept limits. RULES: "5 requests per second per key (bursts of 20)". |
| Market limits in force | 1 accept, 1 message/side/tick, 6 threads, 30 open offers, 12 new listings per tick [V] | `/api/clock` limits as recorded in the repo |
| A spent accept returns | `wait_for_tick` (429), not `accept_taken` [V] | team/aleks.md Sat 10:40 |
| Keyless reads | 60/s per address, separate from the key [V] | 97 "at most 60 requests per second" lines Sat 11:59-16:34 (bargains, news, opps, radar, recorder). They hit our intel tools, never the key. |
| Saturday's key 429s | 6 events [V] | opps 09:39, 10:41, 21:34:59 · status 10:41, 15:29 · duelmon 21:35 (the trader 21:50 and autoflip 21:54 lines are Friday's). The **21:34-21:35 cluster is the mid-Duels-II restart burst** (team/lucas.md 21:37). |

## 2. Each process on the key (15 s ticks; code-derived)

"Keyed/tick" counts only requests that carry `X-Team-Key`. The SDK sends the key on **every** call of a keyed
`Bazaar`, public routes included, so the trader's 18 board reads count.

| Process (machine) | Keyed req/tick (req/s) | When in the tick | Writes / accepts / threads | On a 429 or refused accept |
|---|---|---|---|---|
| **duelist** (Aleks; `--poll 2`) | idle 6.5 (0.43): clock + duels every 5 s, plus 4/min sweep. Active ≈ 15 (1.0) | polls all tick. Moves at t+1..t+6 s (code decides, Haiku words) | ≤ 1 msg per live duel per tick (4 at once). Accepts and messages: own limits | SDK 3 retries (0.25/0.5/0.75 s). Then the move is **pending → next tick** (`RETRY_CODES` + any 429). Deadline accept at 2 ticks left, with the last tick spare. A failed poll means 4 s blind. **No priority over anyone** |
| **trader** (`loop.py`) | ≈ 24 (1.6): 2 clock, me, my_offers, **18 boards**, 0-3 values, feed/duels sometimes | t+0.2 → ≈ t+11 s, paced 0.3 s | ≤ 1 accept/tick (Sat: 2 all day); no offers | SDK 3 retries. A refused accept (`wait_for_tick`/`rate_limited`/`http_429`) is always retried next tick; a failed board is skipped |
| **book.py** | ≈ 7 (0.47) steady. CHA merge: 13 posts + 13 value reads over 3 ticks (6 new/tick) | **unpaced burst** at t+0.2-1.5 s (≈ 6 req/s) | maker only. Keeps our open offers ≤ 25 (30 − OPEN_RESERVE). ≤ 6 new/tick | retries=1. A failed post is retried next tick. A refresh whose cancel worked but post failed leaves the bid **off the board ≥ 1 tick** |
| **swaps.py** | ≈ 5 (0.32): 2 clocks/tick, 6-9 reads every other tick | t+0.2 burst | ≤ 2 posts/run, ≤ 4 live | retries=1; error → run skipped, sleep 5 s |
| **opportunities.py** (opps) | 3 + V value reads + posts per run, every 2-3 ticks (0.2-0.33) | from t+0.2, paced 1/s | ≤ 3 live, ≤ 2 posts/run | **retries=0**: a 429 on me/my_offers aborts that run; a failed post ends the run |
| collector | ≈ 4.4 (0.29): feed(1000), me, leaderboard, rastro board every ≈ 16 s, plus 6 reads every 2 min | drifts | none | SDK default; logs, continues |
| duel_monitor | 2-3 (0.15-0.21). It reads `duels(done)` **every tick while no duel is live** | t+7.5 s, paced 1.05 s | none | retries=1; error → 15 s pause |
| reactor | 0.05, rising to ≈ 0.5 in a listing wave (CHA release); value lookups ≤ 1/s, plus me + my_offers per minute | on events | none | a failed value read → that listing is **never evaluated** (a BUY line silently missed) |
| status | 11 unpaced every 5 min (0.04) | a 2 s burst | none | logs |
| watch.py (Operator Monitor) | 6 unpaced every 30 s (0.2) | burst | none | logs |
| scout / judge | 4 per 15 / 30 min | burst | none | logs |
| bargains (DOWN since Sat) | keyed value reads + board sweep every 2 min | | none | retries=0; keep it down (the reactor covers it keylessly) |
| archiver | 2 at the round change (fires at R3 t+0) | t+0 | none | logs |
| recorder | broker key, 2 Hz during benches (≈ 09:21, 11:21, 13:21 [L]) | | none | separate key [L; ? whether broker keys share the team's 5/s] |
| Dani's dashboard | ≈ 2.3 (0.16): me + duels per tick, duels(done) every 3rd | t+1..t+4 s | none | logs |
| `simple_buy.py` (Operator) | ≈ 0.15 req/s per thread (thread() every 12 s + say) | drifts | 1 thread per run; `--offer-only` = **no accept of ours** | retries=1; thread/say errors caught. **`open_thread`, the walk's `close_thread` and `me()` are unguarded**: a 429 there crashes the run, and a crash on the walk branch leaves the thread open |
| `rbuy.py` / `deny.py` (Operator) | 5-6 unpaced per shot | when fired | **1 accept** | rate: 3 retries. Accept already spent this tick (`wait_for_tick`): **exits, no retry** |
| `abuela_bot.py` | plan(): **≈ 50 value reads at 4/s (≈ 12 s)** before its first thread; then ≈ 4/tick | | thread + accept unless `--offer-only` | `wait_on_tick=False`; tick-waits on say/accept and retries; an exception closes the thread |
| `chato_steady.py`, `dealer_sell.py` | ≈ 4/tick | | thread + accept unless `--offer-only` | **`wait_on_tick` left at the SDK default (True)**: a refused say/accept sleeps to the next tick and is re-sent blind ≤ 3 times. No try around say/accept: after that the process dies **with the thread open** |
| keyless (hub.collect, news, radar, hints, matchmaker, reactor stream) | 0 on the key | | | per-address 60/s (§1) |

Market accepts on Sunday come only from the trader, rbuy/deny, any "we accept" last-card deal, and chato_steady,
abuela_bot or dealer_sell run without `--offer-only`. Book, opps and swaps are makers: the counterparty spends its own
accept.

## 3. Simulation (scratchpad `contention_sim.py`, not in the repo)

**Model.** One token bucket (20 tokens, 5/s refill). Each process is replayed as its code issues requests (order,
pacing, `wait_tick` phase, SDK retry rule). Board and feed payloads get 1.4-3× latency. Latency is lognormal around
0.08 / 0.15 / 0.3 s. 8-12 runs each. Duels III: 17 waves × (12 + 1) ticks, 4 duels each. A duel moves with p = 0.55 per
tick from tick 2, with a deadline accept at 2 ticks left. Duel moves go out 0.8-4 s after the poll sees the tick. [L:
the server's limiter may be stricter than a plain bucket.]

| Scenario | Keyed req/s | 429 hits | Duelist hits | Duel moves pushed a tick | Lost deadline accepts |
|---|---|---|---|---|---|
| **R3 t+0 → 90 min, all on** (trader, book + CHA merge, swaps, opps, reactor wave, 5 Operator dealer threads, idle duelist, …) | 3.3-4.1 | 14-380 / 90 min (157 @0.15) | 2-41 | n/a | n/a |
| R3, same without swaps | 3.8 | 18 / 90 min @0.15 | 2 | n/a | n/a |
| R3 first 3 ticks only | | book loses **0.1-2.3 CHA bid posts** (re-posted a tick later); trader 0.4-6 hits; reactor 0.3-2.6 | | | |
| **Duels III, all on** | 3.7-4.6 | **32-700 / h (304 @0.15)** | 8-177 | 0-2 / h (≤ 0.6 %) | 0 |
| Duels III, all on + 2 dealer threads + an abuela_bot plan() | 4.6 | 356 / h @0.15 | 86 | 0.4 / h | 0 |
| Duels III, trader + book + reactor + watch kept; swaps, opps, dealer threads off (≈ red-team §H) | 3.1-4.1 | 0-64 / h | 0-16 | 0 | 0 |
| **Duels III, policy §6** (book, collector, duelmon, status, watch, reactor, analysts, dashboard, rbuy; **no trader / swaps / opps / dealer threads**) | 2.3-2.5 | **0-1 / h** | 0 | 0 | 0 |
| CHA release *inside* Duels III, policy on (book merge + 2 dealer threads + reactor wave) | | 0-6 / h | 0-1.6 | 0 | 0 |
| same, trader + swaps + opps on | | 35-658 / h | 8-159 | 0.1-1 / h | 0; book fails 1-15 posts |

**One tick, all on, Duels III (0.15 s, seed 3)**, requests per second into the tick: +0 s 13 ok (book 5, trader 2,
swaps 2, duelist 3, reactor 1) · +1 s 11 (status burst 6) · +2 s 9 → **bucket 0** · +3 s 4 ok, **4 refused** (dashboard
2, opps, trader) · +4 s and +5 s: **the duelist's moves refused** · then the trader alone refills slowly until ≈ +12 s.
With the policy, the same tick peaks at 12 requests in the first second and the bucket never drops below 11.

Why it bunches: trader, book, swaps and opps all `wait_tick()` and fire 0.15 s after the boundary, the dashboard
fires at +1 s, and the duelist's poll sees the new tick within 2 s. At 15 s ticks the quiet tail is half of
Saturday's, so the bucket has less time to refill.

## 4. Collisions, ranked

1. **Tick-start 429s on the key during duel waves** (trader ≈ 32 % of the key, then the book, swaps and opps bursts).
   It costs duel moves 0.25-1.5 s, now and then a whole tick, and the monitors their reads. The worst case,
   a deadline accept refused twice = no deal, is ≈ 0 in the model but not impossible under a stricter limiter.
2. **Restart bursts.** Sat 21:34-21:35: restarting opps, bargains, trader, book and swaps mid-Duels II gave the 429s on
   opps and duelmon [V]. Each start fires its first sweep at once (book: clock then step, no wait).
3. **CHA t+0 rush (09:00).** book merge (13 bids, unpaced), trader restart, swaps, opps, the reactor's listing wave,
   the archiver's round snapshot, the idle duelist and the Operator's Pícaros/Abuela threads all land together. Result:
   1-2 CHA bids land a tick late. The Pícaros `open_thread` at t+0 wins only if it fires first, and if it is refused
   simple_buy crashes (unguarded).
4. **Market accept, trader vs Operator.** If the trader spent the tick's accept (late in its sweep, ≈ t+8-11 s),
   `rbuy.py`, `deny.py` or a "we accept" last card gets `wait_for_tick` and exits without retry. Rare: 2 trader accepts
   on Saturday. But the last-card deals (CHA, MAL-07: +50 each) are the most valuable accepts of the day.
5. **Leaked conversations.** chato_steady and dealer_sell die with the thread open after repeated refusals, and so does
   simple_buy on a failed walk-close. That blocks "one per dealer" (the next Pícaros or Abuela run is refused) and
   holds 1 of 6. Our planned peak is ≈ 4 threads, so the cap only bites through leaks.
6. **New listings and offers.** The merge tick can reach book 6 + opps 2 + swaps 2 = 10, so 3 manual posts in that tick
   push it past 12, and the last one gets `wait_for_tick`. Open offers ≈ 24-26 of 30 in R3: book entries ≈ 17, opps ≤ 3, swaps ≤ 4. book stops at 25
   total by design, but opps and swaps can push past 30 and get refused (harmless).
7. **The duelist's own idle polling** (0.43 req/s from whenever it starts) is ≈ 9 % of the key during the CHA rush.

## 5. 429 and accept handling: verdict

- Nobody hot-loops on a 429 [V]. Retries are bounded everywhere (SDK: 3 × 0.25-0.75 s; then next tick or next run).
- **Duelist:** handles it well (pending → next tick; the last tick is spare), but **has no priority**. Every other
  process competes equally.
- **Gaps to fix, or at least avoid running, on Sunday:**
  (a) chato_steady and dealer_sell: `wait_on_tick` default plus no try/close, so they can die holding a thread. Use
  simple_buy or abuela_bot with `--offer-only` instead.
  (b) simple_buy: guard `open_thread`, `close_thread` and `me()`, or fire it before the book merge.
  (c) rbuy/deny: no retry on a spent accept. Re-run next tick, or pause the trader for that tick.
  (d) reactor: a value read refused by a 429 drops that listing for good.
  (e) opps `retries=0`: a run lost per 429 (cheap).
  (f) book refresh = cancel then post, and a refused post leaves the CHA bid off the board for a tick.

## 6. Policy: the duel window (Operator on Lucas's Mac runs every command; daemons live there)

**Times** [L: re-read `/api/schedule` at 08:55 and 10:30; game hour = wall hour]: Duels III ≈ 11:00-11:51 (68 duels,
17 waves × 12 ticks), Final ≈ 14:00-14:27. Saturday's Duels II protocol (stop at 20:25) is the template. What went wrong was the mid-session restart at 21:34 (429s on opps and duelmon).

| When | Who | Exactly |
|---|---|---|
| 08:30 | Aleks | `duelist_sunday.sh --check` only (tests + params, no start). **Start the duelist at 10:30** (the plan's "live by 10:30"), so its idle polling stays out of the CHA rush |
| R3 t+0 (09:00 if the clock jumps) | Operator | Order: (1) the Pícaros CHA-09 thread first, while the bucket is full; (2) merge `book_cha_entries.json` (book posts 6/tick by itself); put the LAT-06/07/08 fodder bids into run/book.json, not by hand (12 listings/tick); (3) `CASH_FLOOR=464 tools/daemons.sh restart trader` at **t+2 min**, not t+0 |
| R3 t−2 min → t+5 min | Operator | `tools/daemons.sh stop swaps opps`, then at t+5 min `CASH_FLOOR=<opps floor> tools/daemons.sh start opps`, 15 s later `tools/daemons.sh start swaps`. Model: 157 → 18 429s over 90 min without swaps |
| ≤ T−15 min (≈ 10:45, ≈ 13:45) | Operator | Last dealer deals settle; **no new dealer threads** until the window ends (dealers close 14:00 anyway) |
| **T−5 min (≈ 10:55)** | Operator | `tools/daemons.sh stop trader swaps opps`, then the `pgrep` check in the block below must print nothing (swaps runs under `uv run`: no orphan python may survive the `pkill -P`). `bargains` stays down |
| inside the window | everyone | **Running:** book (CHA bids stay live; fills need no accept of ours), collector, status, duelmon, reactor, watch, scout/judge, archiver, recorder, Dani's dashboard, keyless tools. **Allowed:** rbuy/deny one-shots on reactor lines, and last cards as maker posts (they accept). **Not allowed:** run/book.json edits (each = cancel + post bursts), any `daemons.sh start/restart`, abuela_bot (plan() = 50 reads at 4/s), chato_steady, dealer_sell, simple_buy, ad-hoc loops on the key |
| end: `duels.finished` for "Duels III" in the feed (`wait_duels_end.py`, block below), else 12:30 | Operator | `CASH_FLOOR=<trader floor in force> tools/daemons.sh start trader`; 15 s later `CASH_FLOOR=<opps floor> tools/daemons.sh start opps` (+ `OPPS_BUILD=…` if set); 15 s later `tools/daemons.sh start swaps`. **Always pass the floors**: daemons.sh defaults trader, opps and book to `CASH_FLOOR=100` |
| 13:55 → `duels.finished` "Final" (fallback 14:35) | Operator | Same stop, same staggered restart. The market closes 15:00 |
| any window | Aleks | Announce "wave live / Duels III done" in the team chat; one duelist only. If a duel shows a refused move, tell the Operator, who checks `tools/daemons.sh status` |

Copy-paste block for the Operator (repo root on Lucas's Mac; fill the floors in force from team/lucas.md):

```bash
# T-5 min
tools/daemons.sh stop trader swaps opps
pgrep -fl "agents/trader/loop.py|agents/trader/swaps.py|tools/opportunities.py"   # must print nothing
# plain | on purpose: macOS pgrep reads an extended regex; "\|" matches nothing (false all-clear, tested Sun 01:40)

# end of the window: wait for duels.finished (script in the Operator session's scratchpad, not in the repo)
python3 /private/tmp/claude-501/-Users-lucaswiese-Documents-claude-hackathon-team-5/b5f4f4ed-eee9-4f01-988e-7d30f8b0148b/scratchpad/wait_duels_end.py "Duels III" --until 1230
CASH_FLOOR=<trader floor> tools/daemons.sh start trader; sleep 15
CASH_FLOOR=<opps floor> tools/daemons.sh start opps; sleep 15    # add OPPS_BUILD=... if one is in force
tools/daemons.sh start swaps
tools/daemons.sh status
```

If the clock **resumes** instead of jumping, the CHA release can fall inside a duel window. Run the CHA fast start with
the trader, swaps and opps still off (book merge + Pícaros thread fit: 0-6 429s an hour in the model).

**A priority rule, if anyone wants code later (not for Sunday):** a `run/duel_window` file that trader, swaps and opps
check before each sweep. This is the arbiter idea applied to request rate instead of accepts. Today `daemons.sh stop`
does the same with no code change.

## 7. Limits of this audit

- The limiter is modelled as a plain 20-token bucket. If the server counts a rolling 1 s window, bursts hurt more and the
  policy matters more [?].
- Venue count is taken as 18 boards for the trader (hub.collect reads 19 boards) [L]. With 12, the trader drops to 1.2 req/s and the
  all-on 429s fall by about a third.
- Whether broker-key reads (recorder, broker) share the team's 5/s is untested [?]. If they do, a bench at ≈ 11:21
  inside Duels III adds 2 req/s, and `tools/daemons.sh stop recorder` belongs on the T−5 list.
- The idle-duelist, Dani-dashboard and Operator-Monitor rates assume they run as coded. Ad-hoc Claude Code reads
  are not modelled.
