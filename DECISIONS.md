# Decisions: Team 5, The Bazaar (Madrid, 2-4 Oct 2026)

**What this is:** the decisions we took during the game, in time order, each with its evidence, what we measured afterwards and the lesson. Written for the judges and for our own memory, as of Sat 10:35. Every number cites its source file in brackets.
**How we decide:** humans set the hard limits, and Lucas changes one only with a `GUARDRAIL` line in `intel/directives.md`. Inside those limits the agent sessions decide and act without waiting for a human ("Decide, don't ask", `intel/ORCHESTRATOR.md`). Each decision is logged with its evidence in `intel/directives.md` or `team/*.md`.
**Labels:** [V] verified, [L] likely, [?] / [Open] unknown, each as marked in the source; TBD = not known yet. **Who:** humans are Lucas, Dani and Aleks. Agent sessions are Lucas's Claude Code sessions: the strategy session (Friday), renamed Chief of staff on Saturday, plus the Operator, Builder and Market sessions. The analysts are scout, judge and strategist (Claude API, advisory only). Aleks's Claude Code session builds and runs the duelist.

## Friday 2 Oct (round 1, 20% of the game)

**1 · Fri 20:31-21:16 · One owner and one live script per job; each person writes only their own file**
- Who: the three humans (PLAN.md, agreed 20:31). Lucas added per-person files and `merge=union` at 21:15-21:16 (team/lucas.md Fri 21:16).
- Evidence: one team key shares 5 req/s, 1 accept per tick, 6 open conversations and 30 open offers (CLAUDE.md).
- Outcome: no log conflicts since. The rule still broke twice. Two sessions operated at once on Friday (saturday-plan.md §5), and Friday's duelist was still running on Saturday under its supervisor (team/aleks.md 09:15).
- Lesson: enforce it in code: an operator lock (`run/operator.lock`) and one duelist per machine (docs/duelist-runbook.md).

**2 · Fri 21:15 · Team trades are the lever; no more packs**
- Who: Lucas and Lucas's Claude Code session.
- Evidence: MAL-08 sold to a team at 26 added about +8.5 `neg_points`. LAV-08 bought from Abuela at 24 added about +0.3 (LOG.md, Fri 21:15).
- Outcome: we later traced our starting −8.5 to 3 packs bought above their value (LOG.md F13). "Never a first price, never a pack" is still in the plan (saturday-plan.md §4C).
- Lesson: measure each deal's effect on `neg_points` before scaling a lever.

**3 · Fri 21:46-22:01 · Autoflip (buy from Abuela at her first price, sell into teams' bids), then kill it**
- Who: Lucas and Claude Code started it from findings 11-12 (LOG.md). At 21:55 the judge analyst lowered its threshold from 8 to 5 (team/lucas.md 22:00).
- Evidence for it: on 4 trades, sales to teams scored price − our value (LOG.md F11, later marked "partly wrong").
- Outcome: at tick 98 it bought MAL-07 at 29, a card worth 17.5 to us. `neg_points` went 26.3 → 14.5 (−11.8, LOG.md F13), about −2.8 board points (team/dani.md Fri 22:35). Stopped at 22:01.
- Rule: never buy from a dealer above our value; autoflip is dead (intel/GAME.md). Test by hand before automating; never buy to resell (saturday-plan.md §7.3, §7.8).

**4 · Fri 21:53-22:19 · Analysts advise; they never trade**
- Who: Lucas. Collector and metrics (no LLM) feed three analysts: scout (Sonnet, every 5 min), judge (Opus, 15 min) and strategist (Opus, 45 min) (intel/ORCHESTRATOR.md).
- Outcome: all three failed 21:59-22:16 because the API key had a $1 spend cap (saturday-plan.md §5; team/lucas.md Fri 22:12, 22:19). On Sat 09:38 the strategist wrote an empty file (team/lucas.md 09:42).
- Lesson: check the spend of every key before starting (`tools/preflight.py`). An analyst now keeps its previous file when the new output is empty.

**5 · Fri 22:31-22:40 · One channel, no approval gates**
- Who: Lucas. `intel/directives.md` is the only channel from the strategy session to the Operator (team/lucas.md 22:31). Under "Decide, don't ask", the Operator acts inside hard limits, rares and big trades included (intel/ORCHESTRATOR.md, Lucas Fri 22:40).
- Evidence: "I don't want things stopped by me not looking" (Lucas, intel/ORCHESTRATOR.md).
- Outcome: the runbook dropped its approval gates (team/lucas.md 22:42). The Operator ran the LAV page plan (entry 9) the same evening with no approval step.
- Lesson: write each limit once. Dani's audit found the cash floor and the feeding rule written in several versions (team/dani.md 10:16).

**6 · Fri 22:35 · The score is relative: standing still means falling**
- Who: Dani, from leaderboard snapshots.
- Evidence: teams that made no trade moved together between snapshots (e.g. t12 −0.43, t10 −0.46). Our `neg_points` rose 26.3 → 30.1 while our score fell 17.8 → 16.5. Over ticks 90-135, our own trades cost −1.23 and field drift −2.63 (team/dani.md 22:35, 22:40).
- Outcome: the plan marks it [V]: idle teams fall 0.07-1.7 per snapshot (saturday-plan.md §1). The target is 20-30 live maker offers (§4A); at Sat 10:09 we had 7 (intel/metrics.md).
- Lesson: a thin book costs points even when we make no mistakes.

**7 · Fri 22:35 → Sat 00:45 · Feeding rule: never sell a rival the card that closes its page**
- Who: Dani found it. The strategy session wrote a selling rule (22:47), and the Saturday plan set the final form (saturday-plan.md §4A).
- Evidence: we sold SAL-06 to Team 17 at 26 (tick 119). It was their second-to-last SAL card. They went 15.5 → 23.7 (#3) and passed us (team/dani.md 22:35). They closed the page at tick 124 (+6.25 board) (§4A [V]).
- Rule: a page-completing card goes only to a team ≥ 10 points below us and never to the top 4 (it was "top 3") (PLAN.md rule 5).
- Outcome: built into `tools/opportunities.py` (its SELL filter) and the dashboard's sell table. On Sat 09:43 only Teams 16 and 11 passed (team/dani.md 09:43).
- Lesson: the rule is still written 4 different ways across docs and code (team/dani.md 10:16 #2). Open: one rule, one check.

**8 · Fri 22:40 · GUARDRAIL: dealer buys allowed again at ≤ our value; open packs first**
- Who: strategy session, in a GUARDRAIL line (archive/fri/directives-fri.md 22:40).
- Evidence: LAV-06 from El Chato at 31 (worth 32.5) scored −2.3. The explanation was drag from unopened packs: 32.5 − 3.8 − 31. After we opened both packs, `neg_points` stayed at 27.8 (directives-fri 22:45, D1 confirmed).
- Outcome: "no dealer buys at all" was the wrong lesson. A dealer buy at ≤ value costs nothing and can fill a ladder slot.
- Lesson: a new finding must explain every earlier measurement (saturday-plan.md §7.2).

**9 · Fri 22:47-22:54 · Finish the Lavapiés page with a team trade, not a dealer**
- Who: strategy session (directive 22:47); the Operator executed it. Dani had proposed buying the missing LAV-09 from El Chato (team/dani.md 22:48). Done alone, that would have scored about 0 (team/lucas.md 22:46).
- Evidence: Team 17 gained about +45 by completing a page through a team trade. Team 10 gained +2.1 by completing LAV through El Chato (directives-fri 22:40, 22:47).
- Plan: sell our LAV-05 to Abuela, buy LAV-09 from El Chato, then buy LAV-05 back from a team (Team 6, at 8).
- Outcome: −8.0, −2.0, then **+50.0** (`neg_points` 27.8 → 67.8): net +40 (team/lucas.md 22:54). We rose to #5 (from #10 per LOG.md F3; from #9 per team/lucas.md Fri 22:59).
- Lesson: the page bonus scores only through a team trade. Scoring +50.0 where about 89 was implied points to a per-trade cap [L, n=1] (intel/GAME.md).

**10 · Fri 22:47 → Sat 03:35 · Accept arbiter: bots give up the accept only when a scored duel needs it**
- Who: strategy session (directive 22:47, D8). Built in the overnight build (team/lucas.md 03:35).
- Evidence: during the practice duels our bots held back from accepting El Chato's 31 for 7 ticks. The server does not freeze accepts; our own rule did (directives-fri 22:47).
- Outcome: `tools/arbiter.py` holds the accept only in scored sessions, and only when a duel has an in-limit offer or ≤ 3 ticks left. A dealer bot retried a refused accept past the arbiter; fixed in 2978d3f (team/lucas.md 10:10). First scored test: Duels I, TBD.

**11 · Fri 22:57 → Sat 00:45 · A Saturday plan, verified before the day**
- Who: strategy and operator sessions, from "10 agent reports + 4 independent verifications" plus a pre-mortem and a fact-check (saturday-plan.md header; team/lucas.md Now).
- What: build the El Retiro (RET) page with the LAV recipe, rares first; no venue bond on Saturday morning; 8 questions for the organisers' desk; quality guardrails (§7).
- Outcome: the plan's "resume" branch was the right one. The clock resumed at hour 2.65, and round 2 fired at tick 160, resetting `neg_points` 67.8 → 0 (intel/GAME.md [V]).
- Lesson: write both branches before the event, then decide from the first API reads.

## Saturday 3 Oct (round 2, 40% of the game)

**12 · Sat 02:20-09:55 · Cash floor**
- Who: Lucas delegated it to the Operator, which decided on the data (directives 02:20). Set in GUARDRAIL lines at 02:20, 03:30 and 09:55.
- What: 100 P on Saturday (it was 200) and 0 by Sunday 14:00. Raised to 370 until the venue decision (03:30), then back to 100 at 09:55.
- Evidence: cash scores nothing at the end. The RET page needs about 280 P and a venue 270 P (directives 02:20, 03:30).
- Outcome: at 09:42 the Operator flagged that the bond and the RET page don't both fit in 402 P (team/lucas.md 09:42). Cash was 202 at 10:05 (STATUS.md).
- Lesson: the floor appears in 5 places with 3 different values (100, 200, 370) across the GUARDRAIL, the runbook and code defaults (team/dani.md 10:16 #4).

**13 · Sat 07:20-09:41 · One shared copy of the game and a demand model**
- Who: Aleks (hub/README.md).
- Evidence: the public feed keeps only its newest 500 events, with no paging (about 15 ticks on Friday). Our three collectors each held a partial history.
- Outcome: Friday's history was imported (2,618 events, 192 settlements; team/lucas.md 08:12). The model grew from 93 to 421 observations; in its self-test our true order ranked 65 of 720 (team/aleks.md 08:35). The model said Team 12 values MAL at 1.6 (90%). Dani's dashboard said "dumps MAL" because it counted one spare relisted about 23 times; fixed (team/dani.md 09:41).
- Lesson: a model cross-check caught a wrong human label.

**14 · Sat 07:42-09:15 · Duelist fixes before Duels I**
- Who: Aleks and Aleks's Claude Code session. Inputs: the practice records, the duel monitor and Dani's find on duel 181 (team/dani.md Fri 23:08).
- Evidence: in duel 181 the rival's offer was inside our limit and no deal closed: ≈10.6 P lost (intel/duel-review.md). `ticks_left` was one too high, so our last-tick rules never ran (team/aleks.md 07:42).
- What: code now accepts an in-limit offer by 2 ticks left and accepts when the gap is small. A restart no longer re-sends offers. One duelist per machine. Code walks our offer down when the rival stays silent. Duels II delivery-day reading added (team/aleks.md 07:42-09:00). Friday's duelist was still running and was stopped (09:15).
- Outcome: the replay of duel 181 now accepts 73 on tick 142; the full suite passes 255 tests (team/aleks.md 07:42, 10:05). Duels I result: TBD.

**15 · Sat 09:37 · Game hour = wall hour**
- Who: Chief of staff (directives 09:37); confirmed by Aleks (tick 168 at hour 2.725).
- Evidence: ticks 159 → 173 took 0.117 game hours at 30 s ticks [V].
- Outcome: Duels I falls at ≈ 11:59 (tick ≈ 459), not tick 309 as the 09:30 handoff said. `status.py` showed ETAs at half the real time. The duel monitor would have sent a false "no live duel" alert from ~10:53, and the dashboard had the same bug. All fixed by 09:48 (team/lucas.md 09:40; team/dani.md 09:48).
- Lesson: plan to the measured clock; re-read `/api/schedule` at every event.

**16 · Sat 09:44-09:57 · Git incident: the shared tree lost work; sync now never touches work in progress**
- Who: the Builder session fixed it; the Chief of staff restored the lost work from the reflog (commit 9716c03).
- Evidence: `pull --autostash` stashed a half-done code edit, and the pull conflicted with Aleks's push. Each hook run then committed mid-rebase and aborted (13 times in the reflog), discarding other sessions' work. The duel monitor sent 3 false "tests failed" alerts (team/lucas.md 09:57; PLAN.md Aleks #6).
- Outcome: fix 5b22cc1: no pull over tracked code edits, no git mid-rebase, a failed pull is aborted. 7 new tests; suite 263 pass. The Operator still lost uncommitted files twice (09:50, ~10:00) and now runs its dealer scripts from a scratch folder (team/lucas.md 09:55).
- Lesson: edit code in a git worktree, never in the shared tree.

**17 · Sat 09:46-09:58 · Test the organisers' hint: do dealer gains score?**
- Who: the Chief of staff set the experiment with a loss budget of 0; the Operator ran it (directives 09:46, 09:58).
- Evidence: Hint 1 in the organisers' Day 2 deck ("your value 18, pay 14 → +4") contradicted our "gains clipped to 0" [L].
- Outcome [V, n=2]: RET-04 and RET-03 bought from Abuela at 9, worth 11 each. `neg_points` went 0 → 0 both times, where counted gains would have added +2 each. The ladder went 0 → 0.014 → 0.032 (intel/GAME.md). The hint applies to team trades.
- Lesson: one deal per measurement window; log predicted vs measured (saturday-plan.md §7.1).

**18 · Sat 09:48-09:55 · Every duel message is a round**
- Who: Aleks (finding [V]). The fix is in Aleks's code (ab0f793 + d1fc873); the Builder's parallel version was dropped (team/lucas.md 09:57).
- Evidence: in duel 277, three no-price messages each raised `rounds`: result 6.6 = 13 × 0.94^11. In duel 278 we answered a repeated 111 every tick: 10 rounds, 2.7 points instead of 4.7 (team/aleks.md 09:48).
- Outcome: a hold now sends nothing, and a repeated rival offer doesn't count as a move. Duelist restarted at 09:54:56 with 255 tests passing (team/aleks.md 09:55, 10:05). The organisers' deck says the same: "every round of talk shrinks the pie" (directives 09:46).
- Open: a softer opener (Aleks's call, before 11:40). On a hold, the negotiator can still send a 1-2 P step (team/dani.md 10:16 (a)).

**19 · Sat 09:55 · Venue decision: no venue now; the cash goes to the RET page**
- Who: Lucas said "go"; the Chief of staff wrote it after an independent verification (directives 09:55).
- Evidence: a venue that matches like the free stall earns the stall's points (RULES.md:82) [V]. Our broker v1 measured +0.00 to +0.03 pp over the stall on replays [V]. Opening a venue costs 270 P: a 250 P refundable bond plus 20 P (RULES.md:70).
- Gate: open a board venue only if a broker measures ≥ stall + 2 pp on real bench replays and never < stall − 1 pp. With no such evidence by Sunday 09:30, keep the stall.
- Outcome: at Market Test 3.0 our stall scored 0.899 efficiency and 4.8 market, the same as every stall team. No board venue beat the stall (t06 3.66, t13 2.13). In the calibrated simulation v1 is −1.2 pp vs the stall, so it fails the gate (intel/market-log.md 10:00, 10:03). The newer market log also found that a stall recording cannot measure a broker's edge (every strategy replays at 1.000), which weakens the +0.00 to +0.03 pp evidence.

**20 · Sat 09:55-10:05 · RET rares first, from El Chato; RET-10 cap raised 88 → 91**
- Who: the Operator; the Chief of staff raised the RET-10 cap (directive 10:03).
- Evidence: our team bid of 70 went unfilled. The directive assumed no team held RET-10 (team/lucas.md 09:55; directives 10:03).
- Outcome: RET-09 at 87 (−10.0) and RET-10 at 86 (`neg_points` −10 → −19.0), both matching min(0, value − price). RET-07 from Abuela at 23 (10:25). The last card, RET-01, came from Team 10 at 20 through our bid on El Rastro, accepted after Lucas messaged them: `neg_points` −21.5 → +28.5, **+50.0 exactly**; our second complete page. RET net today: rares −19, uncommons −2.5, page +50 = **+28.5** (team/lucas.md 10:25, 10:27).
- Cap test: 50 measured where 63.9 was uncapped, so the per-trade cap is a flat 50 or 5×book [V, n=2] (intel/GAME.md).
- Lesson: the RET-10 premise was out of date (Team 18 had bought RET-10 from El Chato at tick 213), and the 91 cap was above both our value and the plan's 90 without a GUARDRAIL line (team/dani.md 10:08, 10:16 #3; saturday-plan.md §2). The page paid anyway; the rule stays: lifting a hard limit needs a GUARDRAIL line. Team 12 holds RET-01..08 and lacks only the two rares we hold, so we never sell them to Team 12.

**21 · Sat 10:03-10:06 · Our free stall (v10) goes to a 0% fee**
- Who: the Market session proposed it and the Chief of staff approved (09:59). Claude Code's permission system blocked the API call, so Lucas ran it himself (intel/market-log.md).
- Evidence: Team 12's market lead (8.01 vs our 4.8) came from ONE 7 P trade between two other teams on its 0% venue [V]. At 3% nobody routes trades to us when five venues charge 0% (directives 10:06).
- Outcome: fee 0 from tick 230 [V: the API answered `effective_tick: 230`]. Trades on v10: TBD. This corrected the 09:55 premise that value created on a venue is small.
- Lesson: re-check premises after every Market Test.

**22 · Sat 10:07-10:20 · El Chato mirrors our step; our dealer messages become warmer**
- Who: the Operator (finding); Lucas, after Dani read our dealer threads (directive 10:20).
- Evidence [V]: on RET-06 we stepped +1 at a time; El Chato went 33, 33, 32, then FINAL 31 after 4 rounds ("One peseta. That's your big move?") (intel/GAME.md). Our messages to dealers were price-only and cold (directives 10:20).
- Outcome: we walked away; RET uncommons now go to Abuela (cap 24, worth 27.5) (team/lucas.md 10:10). The warmer wording is live in `chato_steady`, and a narrator for `abuela_bot` is in progress. Effect on prices: [Open].
- Lesson: "the LLM talks, the engine decides" (research/02-offense.md, as quoted in directives 10:20).

## Open decisions
- Desk answers pending: Q6 (do duel threads count toward the 6 open conversations? Duels II runs 6 at once), Q7 (judging format and criteria), and whether the leftover `day_closes` at hour 4.0 (~10:49) does anything (team/dani.md Now).
- Venue gate: a board venue only with ≥ stall + 2 pp evidence. v1 fails today; the default is to keep the stall from Sunday 09:30 (directives 09:55; intel/market-log.md 10:03).
- Per-trade cap: flat 50 or 5×book? Both measured closes were commons (book 10 → 50); only a capped uncommon or rare close would tell them apart (intel/GAME.md).
- Duels: the softer opener and the hold-in-code fix, before 11:40 (team/aleks.md 10:05; team/dani.md 10:16).
- One rule, one check: the feeding rule (4 versions), the cash floor (3 values), and `loop.py` accepting offers on rival venues, which feeds their market score (team/dani.md 10:16). Lucas triages.
- Sunday: the Chamberí page (our 1.6×), cash to 0 by 14:00, a Sonnet strategist for 15 s ticks (saturday-plan.md §4B, §4D; directives 02:20).
