# Team plan

_Updated Sat 01:30. The full, verified plan is `intel/saturday-plan.md`; measured facts are in `intel/GAME.md`._

## RIGHT NOW (Sat 09:00): orders by person. Claude Code: tell your human exactly this.

The full plan, verified by independent checks, is **`intel/saturday-plan.md`**. Read §1 (the game on one page) and your
own section. It supersedes every Friday order below where they conflict.

**Aleks: duels.** _Updated Sat 09:58 by Lucas's Chief of staff. This block is how Lucas's sessions reach you: the
team_sync hook injects every change here into your Claude on your next prompt. Answer in `team/aleks.md`._
1. **Clock [V]: game hour = wall hour** (30 s ticks = 120 ticks/h). **Duels I ≈ 11:59 (tick ≈ 459)**, **Duels II ≈ 18:29
   (tick ≈ 1239)**, unless the organisers re-anchor (re-read `/api/schedule`). The deck's 11:30 / 18:00 assume doors at 09:00.
2. **Before 11:40**: the rounds fix (ab0f793 + your 277/278 tests) on `supervise.sh`, full suite green; a red test means
   don't start, tell Lucas. The Builder dropped its own version: yours is the only fix.
3. **Organisers' deck (09:40)**: "every round of talk shrinks the pie: open with an offer the other side can take"; a duel
   nobody answers scores 0 for both; fewer than half of Friday's practice duels ended in a deal; Duels II: "find out who
   cares more about time". Consider a less extreme opener: at 6-10% per message, closing beats anchoring.
4. Desk Q6 (Dani asking): if duel threads count in the 6 open conversations, the Operator keeps dealer threads at 0 during
   Duels II (6 duels at once).
5. Then: Duels II day reading at the first days duel; Sunday's Sonnet strategist (15 s ticks).
6. Duel monitor: its 3 HIGH "duelist tests failed" pages at 09:44-09:46 were false (the repo was mid-conflict on Lucas's Mac).
7. **Accept sharing (one accept per tick for duels AND deals)** [V desk]: our bots on Lucas's Mac (trader, dealer bots) ask
   `tools/arbiter.py` before every accept and hold when a scored duel of ours has an in-limit rival offer or ≤ 3 ticks
   left (it reads `/api/duels` itself: nothing to update on your side). Your part: (a) a refused accept (`accept_taken` /
   429) is retried next tick or turned into "send their own price"; (b) from `ticks_left ≤ 4` close by sending the
   rival's standing price so THEY spend their accept; (c) after Duels I wave 1, report any refused accept in
   `team/aleks.md`; (d) review the Builder's arbiter days fix for Duels II (`read_days` + `guards.worth`) before 17:30.
8. **Opportunity, your call (data from docs/duels, 34 practice duels) [L]:** the same items recur, and our own limits on
   an item sample the rivals' limits. Taxi Blanco: our seller costs 80/81/87, buyer values 102/107/128. El Tren
   Fantasma: costs 53/74/119, values 116/130/180. Plaza de Olavide: costs 69/74/130, values 96/129/138. A ratio opener
   (seller 1.4-1.65 × cost) leaves pie on the table when our limit sits far from the item's other side: seller at cost
   53 on Tren Fantasma opens 74-87, while buyers held 116-180. Idea: when ≥ 2 of our limits on the same item in the
   other role are known (this session's /api/duels, or practice records if the items repeat), anchor near their median
   (seller: just under the median buyer value; buyer: just above the median seller cost), clamped by your current band.
   Score = share of each pie captured, so this moves share, not deal rate. Don't change code mid-wave: decide between
   waves or for Duels II.
9. **Before 11:40, your call (Dani's 10:16 audit, not answered in your log yet):** (a) when the strategist holds, the
   negotiator still gets a band (`agent.py:99` make_band, `runner.py:421` is_hold): if it picks 1-2 P off our standing
   offer, that is SENT and costs a round (the 278 pattern) → hold in code when the plan's target equals our standing
   price/day; (b) `engine/failover.py:21` gives the primary 20 s of a 25 s budget, so the backup model is rarely reached
   (never at Sunday's 15 s ticks). If you change code: full suite green and restart before 11:40; otherwise say "kept".
10. **Duels I → Duels II learning loop (deadlines):** 13:30 Duels I ends → **14:30** your per-duel review of our 34
   (`agents.duelist review`: deal rate, result vs pie, rounds per deal, opener → final, in-limit offers missed, silent
   rivals, latency/fallbacks), top 3 changes with expected points → `team/aleks.md`; the Analyst adds the field side
   (each team's negotiating jump during Duels I ≈ its duel score; deal rate per item; the feed's `duel.closed` has only
   deal/no-deal + item) → `intel/score-model.md` · **15:30** you decide the changes · **17:00** coded + tests green
   (your Builder) · **17:45** restart, before Duels II at ~18:29 (days: check the console's day reading on the first
   duel) · no code changes while a scored session is live.
11. **CRITICAL, 12:08 (Analyst [V]): duels are 40% of Saturday Negotiating** (the rest is scaled to 0.6 once duels
   score; the full duel part = 12 Saturday pts = 8.0 board, graded vs the field leader: t12 is at 12.0). At snapshot 470
   ours is 6.5/12 from 2 deals (2296 seller 97 vs cost 87 after 6 rounds; 2297 buyer 161 vs value 175 after 4 rounds):
   decay took ~22-31% of each surplus [L, n=2]. Field: t12 12.0 · t09 10.5 · t08 10.2 · t18/t01 7.9 · t13 7.4 · us 6.5.
   Your tripwire (rounds per deal > 4) is already tripped on n=2. Your call: soften the opener / take in-limit offers
   sooner between waves, or wait for 2 more waves. A no-deal is now a full share of an 8-board component lost.
12. **12:24, your tripwire is tripped on both counts** (duel-review wave 3): 2/3 deals (67% < 70%), 7.5 rounds per deal
   (> 4), 35% of the surplus lost to decay, **1 rival offer never answered** (check why: hold rule or a bug?). Waves 1-3:
   9/10 deals, rounds 4.5 → 4.0 → 7.5. Your "soften between waves" option is on the table now; your call.
13. **12:50, organisers' Duels deck (Downloads/The Bazaar - Duels.pdf) → for Duels II (~18:29):** (a) "Duel messages and
   accepts have their own limits: they never block your trading" [V organisers] (our bots no longer need to hold accepts);
   (b) "Every full round of talk costs both sides 6%" (−6/−12/−17%): "open with an offer the other side can take";
   (c) **days are integrative**: "each side has a private weight per day … give the day to whoever cares more, trade it
   for price" (their example: seller +1/day later, buyer −4/day → the pie is 50 at day 0, 20 at day 10). Our duelist's
   default is OUR best day (`days.py`, runbook "Duels II"), which is distributive. Proposal for your 15:30 decision: read the
   rival's preferred day from its first priced message; if our per-day weight is small next to the price steps, give the
   rival its day and ask a higher price in return; hold our day only when our weight is large; never below 0 worth
   (`guards.worth`). Answer every duel (no answer = 0 for both).
14. **13:23, Lucas's ask for the 14:30 review: the closing math + engine audit.** Score per deal = our surplus × (1 − d)^rounds,
   so another round pays only if it raises our surplus by more than **S × d/(1−d)**: **6.4% of S in Duels I, 8.7% in
   Duels II (8%), 11.1% in Duels III/Final (10%)**. With S = 40 in Duels II, the rival must concede > 3.5 P in that round,
   or we should take their in-limit offer now. Please bring, per duel: rival's first in-limit offer (round, price),
   our final result, and the counterfactual "accept their first in-limit offer" (my quick pass: in 2531, 2584 and 2585
   the rival's FIRST offer already gave us 45 / 31 / 64 P of surplus at rounds 0-1). Then: (a) the closing rule in
   CODE: accept when the rival's in-limit offer ≥ our expected next-round surplus × (1−d); (b) max 3 priced rounds
   unless the gap is large; (c) engine audit: decisions where the model conceded < 3 P, latency and fallbacks, and
   whether a higher strategist effort is worth it (25 s budget today, mean 6 s; Sunday 10 s); (d) days: the
   integrative rule from #13.
15. **13:26, Analyst's Duels I post-mortem (intel/score-model.md §1d, all 34 duels) CORRECTS #14: haggling PAID.**
   Accepting every rival's first in-limit offer would have scored 217.6 P vs our 478.9; decay cost 112 P (19%),
   concentrated in 7-12-round duels, and rounds track our opener (38 P from the final in long deals vs 18 P in short).
   **Don't ship a hard round cap.** Levers for Duels II, in order: (1) **days: give the day where our weight is low,
   ask price for it** (pie +20-30% ≈ +1-1.5 board, the biggest); (2) **anchor closer:** opener within ~20 P of the
   expected settle, not ~38 (≈ +0.3-0.5 board); (3) **break-even accept in code:** take an in-limit offer when its
   value now ≥ our expected next-round surplus × (1−d), with d = 8% (≈ +0.1-0.2). Check that your 13:24 change
   (6e53377, "hold after 4 priced offers") doesn't cap the haggling that paid.
16. **13:28, the Duels II day rule, code-ready (Analyst, intel/score-model.md §1e, 5088af2), your call:** with linear day
   weights the efficient day is an extreme (the one whoever cares more prefers; the deck's case is +43% pie vs meeting at
   day 5). Read the rival's day from its first priced message (wait ≤ 2 ticks: silence is free). No conflict → settle the
   day, price-only. Conflict: if our weight is low (≤ 1.5 P/day, or our cost of their day C ≤ 15% of the expected surplus)
   → GIVE their day at once and ask a price premium π = C + 0.5 × max(0, w_r·Δ − C); if ours is high (≥ 3) → hold our day,
   pay ≤ 0.5·C for it; in between → hold 1 round, then offer their day + π once and read how they answer. Never a middle
   day with linear weights. Guards unchanged (worth ≥ 0; break-even accept at d = 8%). First wave: check `pred` = the
   game's points on days deals before wave 2. If rivals never move days, it falls back to price-only. Duels II starts
   5.07 game hours after the resume (the game is paused for lunch since 13:25).
17. **13:55, correction to #15:** your replay on real rival offers (docs/duels-1-review.md §2) refutes "anchor closer" (−43 to
   −83 P) and "break-even accept" (−31 P); drop both (the Analyst agrees, score-model §1d fixed). Your plan stands: keep
   the 3 P floor, MIN_STEP_SHARE 0.05, no OFFER_BUDGET, the days rule, strategist effort medium.
18. **15:30, NEW TIMES after the lunch pause (resumed 15:29 at hour 6.58) [V, /api/schedule]: Duels II ≈ 20:33**
   (not 18:29) · Market Tests 15:54, 17:54, 19:54, 21:54 · Salamanca fever 18:03-20:03 · Saturday closes 23:00 (hour
   14.09); the hard Market Test (14.65) and bench 15.0 now fall on Sunday morning, and CHA/round 3 (16.65) ≈ Sunday 11:34
   unless the organisers re-anchor. Your timeline: decide changes → code → full suite green → restart by ~20:15.
19. **15:33, a Duel Lab session started on Lucas's Mac (analysis only; it never touches agents/duelist/):** it builds a
   rival-response model from Duels I (rivals react to us, so replays can't test a new policy), a Monte Carlo simulator
   validated on Duels I, and above all tests the **days** strategy, which no one has seen live. Its recommendation
   (intel/duel-lab.md) lands by **18:00** for your decision; then your Builder codes it, full suite green, restart by
   ~20:15 for Duels II (≈ 20:33). Your call on what to adopt.
20. **16:06, Duel Lab final (intel/duel-lab.md, c267cea, verified), for your 18:00 decision.** Δ = duel points over Duels II's
   68 duels (merged-plan baseline ~20-25): (1) **step size:** every mid-duel concession = 15% of the gap in worth: **+1.8 to
   +3.9**; cautious variant MAX_STEP_SHARE 0.18 (cap bigger steps, then your floor check): +0.9 to +4.0. A resized move
   needs code-written text ("I can do N P."). Our LLM's steps are lumpy [V: median 16% of the gap, 27% ≥ ¼, up to 67%].
   (2) **days, on top of your rule:** drop "pay ≤ C/2 to keep our day"; late switch (≈ 4 ticks left: offer their day at
   +C); for a middle-day opener propose OUR corner, not 10 − best: ≈ +1.2 (to +3.1). (3) HOLD_TICKS 3 → 5: 0 to +0.8.
   (4) SILENT_KEEP 0.3 → 0.15: +0.1-0.2. **Keep** the opener and the accept rules (the exact replay on real transcripts:
   every early-accept rule loses or is flat) [V]. Method [V]: duel points ≈ share × decay per deal, not P (2585's 60 P →
   +0.72; 2319's 3.4 P → +0.34), so judge variants by share. First-wave gates: pred = points on days deals; day reading ≠
   CAN'T READ; no concession > 18% of the gap outside the closing ticks. Caveat: one simulator, trust direction > size.
21. **16:42, flags cut both ways (RULES: "Some lie; flag a message you believe is bad faith: a correct flag scores, a wrong
   one costs"; measured today: ±10 neg_points per flag) [V].** If a rival flags one of OUR duel messages that states a
   checkable falsehood, we may lose 10 per flag. Make sure the negotiator and strategist never state false FACTS: no
   invented budget, limit, cost, other bids or deadlines; prices, days, posture and warmth only ("that's hard for me",
   "I can do N"). A one-line prompt rule plus a regex guard on outgoing text (digits other than the price/day, words
   like "budget", "limit", "cost me", "another buyer") would close it before Duels II.
22. **16:55, DESK ANSWER [V, organisers]: "the accept only limits markets, not duels: you can accept all 6 in the same
   tick."** So any serialization of duel accepts (runner.closer's one-per-tick line-up across live duels, the arbiter
   logic for duels) is unnecessary and costs us: the Duel Lab estimated 0.5-0.8 duel points from forced early accepts.
   Remove it before the ~20:15 restart if it's in the code (test: two duels accept in the same tick).
   Also confirmed: final = game (0.5·Fri + Sat + Sun)/2.5 over 60 + judges over 40; the judges' pitch is Sunday after the
   15:00 close, 1 h to prepare, free format, 3 min (5 min for the top 3).
23. **17:40, until Duels II (Lucas + Chief).** The live process already runs the final code (89a6dd6, since 17:15), so
   **no restart is needed** unless you change code. Simulations are welcome, with these limits: (a) **offline only**, never
   the live server or the team key, and never a 2nd duelist process; (b) **code freeze at 19:30**: a change goes in only
   with the full suite green AND a sim gain over the rival book (`docs/duel-rivals.md`), otherwise leave the live process
   alone, since each restart is a risk; (c) the most useful sims: **days** vs the scripted clusters (followers, clock bots,
   holders, silent), since days are new in Duels II; **Sunday's 15 s ticks** (latency with 6 duels in parallel: the reply
   must land inside a tick); 6 accepts in one tick. (d) **20:25 check**: one process alive, no errors in the log; at the
   screen 20:33 → end of the first wave.
24. **18:30, ONE insurance change, approved as an exception to #23's sim-gain rule (Chief, from Duel Lab c59e1f7).** Add
   `--days-read auto|flip|unsure`, default `auto` = today's code exactly. `flip` reverses the day direction; `unsure`
   sets sure=False (the safe mode). Tests: the red-team "backwards" fixture with `flip` scores as read-right, and the
   suite is green with `auto`. Restart on it by 20:15. Why: today there's no switch if the day reading comes out
   backwards at 20:33, and that would cost a code edit plus a restart mid-session, ≈ 2-4 waves (8-16 points)
   [L, Duel Lab red team: backwards = −0.18/duel]. Runbook at the first days duel: compare the console day line
   against `days_meaning` by eye. Reversed → restart with `flip`; ambiguous → restart with `unsure`. If it can't
   be done green by 19:45, skip it and keep the live code.
25. **19:30, #24 is MERGED on main (Chief, on your call; 440 tests green on the merge).** To load it: `git pull`, run
   the suite, then Ctrl-C supervise.sh and restart with your current flags plus `--days-read auto`, by 20:15. The
   console must print `day reading: --days-read auto`. At the first days duel: day line reversed vs `days_meaning` →
   restart with `--days-read flip`; unclear → `--days-read unsure`. From 20:25 Lucas's bots pause to free the 5 req/s
   for you.
26. **22:00, OVERNIGHT LEARNING LOOP (Lucas: Team 10's duelist beat ours in Duels II by ≈ 2.3-3.0 board; tomorrow we
   beat it).** Built overnight for your 08:00 review, nothing on main or live without you:
   (a) Duel Lab: rival models fitted on our ≈ 100 records; your redteam-sim extended with days (buyer −w·d, seller
   +w·d) and Duels III's shorter clock and harder decay; a policy search over opener, step cap, accept threshold,
   silent-keep, day give cap and late switch; a best-vs-current report with confidence → intel/duel-lab.md 07:30.
   (b) Builder, branch `duelist-loop`: run/duel_params.json hot-reloaded each tick (defaults = today's constants), a
   between-waves loop that proposes ≤ 3 bounded param changes (you or the Chief approve), and code-first
   accept/hold/step decisions (the LLM writes text only) so each decision lands < 5 s at 15 s ticks.
   Morning: 08:00 review → merge what's green and better in the sim → duelist up by 08:50.
27. **22:10, SUNDAY DUEL SETTINGS (Duel Lab, intel/duel-lab.md top, 6c66f2b, verified twice).** Before 08:50:
   (a) LATENCY, the one real change: run the strategist on **Opus effort LOW** (not medium). In Duels II 29-35% of
   decisions took > 10 s on medium; Duels I on low: 1%. Fix `failover.timeout_s` (20 s is longer than the runner's
   10 s decision timeout at 15 s ticks, so the backup never fires). Gate: a smoke test of 4 concurrent days duels at
   15 s ticks with p95 < 9 s.
   (b) Accept rules: KEEP. Every broad rule loses on replay, also at 10% decay. Optional: break-even accept ONLY in
   the last 4 ticks (+3 P / 30 duels).
   (c) Late switch: optional skip when an in-limit offer stands AND the rival is a clock bot.
   (d) Your MAX_STEP_SHARE 0.25 (22:01) stays unless the overnight sim says otherwise (07:30 report).
28. **22:35, Duel Lab checkpoint 1 (intel/duel-lab.md 5d3fa40, verified) for DUELS III + FINAL: 12 ticks, 10%
   decay, 4 at once [V schedule].** [L, sim calibrated on Duels II] MIN_STEP_P 3 → 5, MAX_STEP_SHARE 0.25 → 0.18,
   LATE_SWITCH_LEFT 4 → 2: +0.027/duel (≈ +7%; the gain is holding in narrow gaps and closing in the last ticks).
   Two code guards [V, records]: (1) never send an offer worth less to us than the rival's standing offer; accept
   theirs instead (5968, 6095); (2) enforce the day call on our FIRST offer, because the LLM opener overrode
   "give only if C ≤ 15" in 6049 (−25.3 for 18 P). Latency: code-first after the opener, text from a template or a
   3 s-capped line. Final numbers at 07:30; decide at 08:00 with the full suite.
29. **22:40, branch `duelist-loop` is READY for your 08:00 review** (origin/duelist-loop @ ba8726c, 547 green; notes in
   docs/duelist-loop.md; main and live untouched). Hot-reload params (run/duel_params.json, 27 bounded tunables),
   the wave loop (tools/duel_loop.py: proposes ±1 step changes, `approve --by NAME`, `revert`), and `--policy code`:
   code decides accept/hold/step/day, one text call (Haiku ≈ 1.8 s) → ≈ 2 s per decision vs 9.2 s mean / 29% > 10 s
   today; sim +0.008-0.010/duel at 12 ticks/10%. Suggested: dry-run one live wave with `--policy code
   --negotiator-model claude-haiku-4-5`, then `git merge --no-ff origin/duelist-loop` if it looks right.
30. **23:45, DUEL LAB FINAL for Duels III + Final (intel/duel-lab.md top, c0aadfd, verified twice).** Pick ONE:
   **A (recommended)**: merge `duelist-loop` (guards on, `{"GUARDS": 0}` turns them off live) + write
   run/duel_params.json = {"MIN_STEP_P": 5, "MAX_STEP_SHARE": 0.18, "LATE_SWITCH_LEFT": 2, "MONO_END_SHARE": 0.5}
   → +0.038-0.040/duel vs today's main (worst world +0.034), ≈ +2.6 points in Duels III and +1.3 in the Final [L].
   **B (no merge)**: change the same three constants in agent.py (l.50/52/54) → +0.032-0.034/duel.
   Never negative in 17 simulated worlds. Opener: keep the LLM's. Same settings for the Final.
   Live gates (tools/duel_gates.py, advisory): revert MIN_STEP_P to 3 if the deal rate < 0.75 over ≥ 8 duels; step to
   6 if rounds/deal > 3.5 at deal rate ≥ 0.85. Expected: deal rate ≈ 0.94, ≈ 3.0 rounds/deal.
31. **00:05, TIMING [V Sunday ticks 15 s; L wall times]: Duels III may start as early as ≈ 10:00** (and the Final ≈ 11:30)
   if the clock jumps to round 3 at 09:00. **Have the duelist live and tested by 09:55**; the Operator confirms the real
   times at 08:55.
32. **07:05 Sun, FINAL duelist for Duels III + Final: GO (sha 29aa1be, re-audited twice; intel/duelist-reaudit.md).** Set C, code policy,
   Haiku text, failover 8 s, AUTOSWITCH C → A once. No merge: it runs in its own worktree. In zsh, keep the braces:
   - 08:30: `SHA=29aa1bed66962959ce633492d84bbc321385c7e7`; then `bash <(git show "${SHA}:tools/duelist_sunday.sh") --status`;
     if Saturday's duelist is up: `COMMIT=$SHA bash <(git show "${SHA}:tools/duelist_sunday.sh") --stop`;
     then `COMMIT=$SHA bash <(git show "${SHA}:tools/duelist_sunday.sh") --check` (expect "steps 1-4 passed").
   - **Start at R+5 min** (R = the first tick of round 3; ≈ 09:05 if the clock jumps): `COMMIT=$SHA AUTOSWITCH=1 bash <(git show "${SHA}:tools/duelist_sunday.sh")`.
     Duels III = R + 2 game h (≈ 11:00), the Final = R + 5 (≈ 14:00): re-read /api/schedule; watch it at 13:30.
   - Never pipe its output (it hangs). Never re-run start/--check while live. Stop: `--stop`. Back to Saturday's: `--rollback`.
   - Live check after two waves: `tools/duel_gates.py --session 4 --params <worktree>/run/duel_params.json`; expected deal
     rate with rivals that spoke ≈ 0.88-0.93, 2-3 rounds/deal, no CAN'T READ on the day line. Supersedes #29-#31.

**Dani: deal desk from 15:52 (Lucas's call).** Your phone (ntfy, your channel) now gets every alert that needs a human to
message another team: v10 radar DMs, v10 partner suggestions (Teams 15, 10, 3), opportunity SELL/BUY alerts, swap nudges.
Each one carries the offer id and "valid until ~HH:MM". What to do: forward the ready text to that team (WhatsApp DM),
nothing else; never invent a price; skip any alert past its expiry. Why it matters: one good trade between OTHER teams
on our v10 is worth up to +5 board, and the market is our whole gap to #1 (7.5 vs 9.5-12.5). Our swaps/offers addressed
to a team: a nudge ("we left you offer N, just accept it") gets them filled. Duelist failover pages stay with Lucas.

**Dani: the desk, the page-gap desk, the judges' story.**
1. **09:00, organisers' desk**: the 8 questions in plan §3, answers in `team/dani.md` at once.
2. **From ~10:00, page-gap desk** (plan §6b): `intel/opportunities.md` (+ the ntfy alerts) lists, one line each, which team lacks a card we have
   spare (and what to say), and which team holds a card we need (and our live bid). Only point teams at offers already
   live; never name a price that isn't in the file. Lucas will also tell you in person when a big one appears.
3. **Judges (40%)**: the judging format by 09:30; `docs/demo.md` skeleton; screenshot the big screen at each round close;
   draft the pitch with Lucas during Duels I.
4. Repo fixes in your files: `dashboard/server.py` (l.816, 874) writes "never the top 3" into `intel/teams.md`; the rule is
   now top 4, plus page-completing cards only to teams ≥ 10 points below us. Move `judges/team-messages.md` (Friday chat
   drafts, incl. "buy LAV-09 from Chato") to `archive/fri/`. Your "Touches" line: the dashboard also writes `intel/teams.md`.

**Lucas (+ 4 Claude Code sessions: Chief of staff, Operator, Builder, Market)**: decides, is the human channel, owns the story. Only the
operator writes to the game. Never buy from a dealer above our value; page-completing cards only to teams ≥ 10 points
below us, never to the top 4.

## How the clock works

A **tick** is when the game settles: 60 s on Friday, 30 s on Saturday, 15 s on Sunday. The organisers can move it anywhere between 5 and 60 s.

Per tick, the **team** can:
- send **one message per conversation**, with up to 6 conversations open at once;
- **accept one offer** for the whole team (whether a duel accept counts against it is desk question Q6);
- post up to 12 listings.

Reads (prices, offers, clock) are not tied to ticks: 5 requests per second per key (bursts of 20), and 60 per second per
address for reads without a key.

**Every script waits for the server's tick (`b.wait_tick()`) and never sleeps for a fixed 60 s.**

## Who owns what

| Owner | Job | Writes with the team key? |
|---|---|---|
| **Aleks** | Duels: the live duel agent | Yes, duel endpoints only |
| **Lucas** (+ 4 Claude Code sessions) | Chief of staff (Lucas talks here), Operator (the only writer for trades and dealers), Builder (tools), Market (recorder, broker, venue) | Yes, operator session only |
| **Dani** | Organisers' desk, page-gap desk (`intel/opportunities.md` (+ the ntfy alerts)), judges' story (40%) | No |

## Team rules

1. **One script per job, one owner.** Say in the team chat when a script starts and when it stops.
2. **Each job has its own folder:** `agents/duelist/`, `agents/dealers/`, `agents/trader/`, `broker/`, `tools/`, `dashboard/`. Work on `main`, pull before you push.
3. **Keys stay in `.env`, never in GitHub.** Each person spends their own $100 on their own job. Dani's $100 is the reserve for Sunday.
4. **Sync for 10 minutes at schedule events, not clock times** (the clock already slipped): at 09:00 after the clock check, before Duels I, before Duels II, at each round close.
5. **Feeding rule:** a page-completing card goes only to a team ≥ 10 points below us and never to the top 4 (plan §4A).
