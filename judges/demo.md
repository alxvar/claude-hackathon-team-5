# Demo skeleton: Team 5 for the judges

> PLAN.md calls this file `docs/demo.md`. It lives in `judges/` (Dani's folder). Drafted Sat ~10:20.
> The judging format and criteria are still unknown (desk question Q7 is pending). RULES.md only says "Judges 40: your ideas and your craft".
> Numbers move during the day: refresh every figure from its source before presenting. The decision log behind this deck is `DECISIONS.md`.

---

## Slide 1: Three humans, many agents, one shared brain

**Message:** we play a four-part game with three people and a set of AI agents, and git keeps all of them in sync.

- The game: 18 teams (ranks run to #18, team/dani.md 09:43). Score = Negotiating 30 + Market-making 30 + Judges 40. Friday counts 20%, Saturday 40%, Sunday 40%, and every score is relative to the field (saturday-plan.md §1 [V]).
- One key per team, with shared limits: 5 requests/s, 1 accept per tick, 6 open conversations, 30 open offers (CLAUDE.md).
- Roles: Aleks runs the duel agent and the shared data hub. Lucas runs 4 Claude Code sessions (Chief of staff, Operator, Builder, Market), plus the trading bots and analysts. Dani covers the organisers' desk, the room, a read-only rival dashboard and the judges (intel/saturday-sessions.md; PLAN.md).
- Git is the shared brain. Each person writes only `team/<name>.md`. A hook pulls on every prompt and tells each Claude session what teammates pushed, then commits and pushes at the end of each turn (tools/team_sync.sh).
- 332 commits by Sat ~10:17: Lucas 245, Aleks 65, Dani 21, Claude 1; most were automatic (git log).

**On screen:** the GitHub repo → `STATUS.md` (it rewrites itself every 5 min from the server, tools/status.py), then the `team/` folder.
**Speaker note:** "No shared chat history: everything that matters is a file, so any human or agent can pick up where another left off."

---

## Slide 2: Architecture: facts → advice → decisions → actions

**Message:** code collects the facts, LLMs advise, a single Operator acts, and humans only set the limits.

```
 [code]  PUBLIC GAME DATA (keyless reads: feed, leaderboard, board, schedule)
            |                         |                          |
 [code]  tools/collector.py      hub collectors (Neon,       dashboard (Dani's laptop)
         every ~15 s             2 machines) + demand model  -> intel/teams.md every 10 min
            |                    hub/demand.py (Aleks)
 [code]  tools/metrics.py -> intel/metrics.md (every 2 min)
            |
 [agent] ANALYSTS, advisory only: scout (Sonnet, 5 min), judge (Opus, 15 min), strategist (Opus, 45 min)
            |
 [agent] CHIEF OF STAFF session -> intel/directives.md  <--  [human] LUCAS: GUARDRAIL lines, venue/cash calls
            |
 [agent] OPERATOR session (the only game writer for trades and dealers)
            |-> loop.py (taker) + book.py (maker book), abuela_bot / chato_steady (dealers)
            |-> opportunities.py -> ntfy alert -> [human] DANI points a team at a live offer in the room
            v
          GAME  <-- accept arbiter (1 accept per tick) -->  [agent+code] DUELIST (Aleks's code; on Sunday it runs on Lucas's Mac, branch duelist-loop @ f57a002)
                                                            code-first policy + Haiku negotiator + code guards
 [agent] MARKET session: recorder, broker simulations, our venue v10
 [agent] BUILDER session: tools, tests, fixes
 Everything logs to git: team/*.md, intel/*.md, docs/duels/
```

- The facts layer has no LLM: the collector runs every ~15 s and metrics every 2 min (tools/collector.py, tools/metrics.py).
- The analysts only advise. The Operator applies what passes the hard limits and logs what it skipped and why (intel/ORCHESTRATOR.md).
- There is one writer per job. The Operator holds `run/operator.lock`, and only one duelist can run per machine (intel/saturday-sessions.md; docs/duelist-runbook.md).
- The team's single accept per tick goes to a duel only when a scored duel needs it (tools/arbiter.py).
- Humans: Lucas changes limits only through GUARDRAIL lines. Dani never invents a price and only points teams at offers that are already live (saturday-plan.md §6b).

**On screen:** this diagram, then `intel/directives.md` (newest block on top) beside `team/lucas.md`.
**Speaker note:** "The LLM talks, the engine decides" (research/02-offense.md). No model can spend past a written limit.

---

## Slide 3: The learning loop: a measured mistake → a rule → code

**Message:** every loss we measured became a rule, and most rules became code with a test.

- **Autoflip.** It bought MAL-07 from a dealer at 29, a card worth 17.5 to us: `neg_points` −11.8 (LOG.md F13). New rule: never buy from a dealer above our value. Autoflip is dead, and the ladder mode never pays above value (intel/GAME.md; team/lucas.md Fri 22:01).
- **Feeding a rival.** We sold SAL-06 to Team 17 at 26; they went 15.5 → 23.7 and passed us (team/dani.md Fri 22:35). New rule: page-closing cards only to teams ≥ 10 points below us, never to the top 4. It is coded in the `tools/opportunities.py` SELL filter and the dashboard's sell table (PLAN.md rule 5; team/dani.md 09:43).
- **The git incident.** A pull loop discarded sessions' work 13 times between 09:44 and 09:52. Fix 5b22cc1 added 7 new tests, and the rule is now "code edits in a worktree" (team/lucas.md 09:57).
- **Predict, then measure.** RET-09 from El Chato was predicted at −10.0 and measured at −10.0 exactly (team/lucas.md 09:55). Dealer gains were predicted at +2 each if they counted; they measured 0 [V, n=2] (intel/GAME.md).
- Process rules: one deal per measurement window; independent verification before any directive that moves > 20 P; stale premises are dropped (saturday-plan.md §7).

**On screen:** LOG.md "Findings history", where several findings are marked WRONG and superseded, then `intel/GAME.md` with its [V]/[L] labels, then `intel/metrics.md` → "What each of our deals did to neg_points".
**Speaker note:** show the wrong findings first; the corrections are the story.

---

## Slide 4: Duels: Clock-Standing, and why silence is the only free move

**Message:** our duel agent is two models inside code guards, and the practice taught us to talk less.

- Clock-Standing: a strategist (Opus) knows our limit and sets a price band. A negotiator (Sonnet) writes the message and never sees the limit. Code blocks any price past the limit (docs/how-the-leading-model-works.md; docs/duelist-runbook.md "Safety rails").
- Score = surplus × (1 − decay)^rounds, where rounds = min(our messages, theirs), priced or not (intel/GAME.md [V]).
- Practice (unscored): 19 deals out of 34 duels (56%), 15% of deal value lost to decay, decisions in 5.3 s on average and 14.2 s at most. Silent rivals: 12 duels, 0 deals (intel/duel-review.md 09:37).
- Duel 181: the rival's offer was inside our limit, but no deal closed: ≈10.6 P lost. Code now accepts any in-limit offer by 2 ticks left (intel/duel-review.md; docs/duelist-runbook.md).
- Duel 278: we answered a repeated price every tick, which made 10 rounds and scored 2.7 instead of 4.7. Now a hold sends nothing (team/aleks.md 09:48, 09:55).
- Duels I ≈ 11:59 and Duels II ≈ 18:29 (team/aleks.md Now). Results: TBD.

**On screen:** the duel monitor page (`python -m agents.duelist monitor`, http://127.0.0.1:8766), the dashboard's Duels tab (transcripts, price path vs our limit), and `docs/duels/README.md`.
**Speaker note:** cost per decision is about $0.005-0.007 (team/aleks.md Fri 21:25, 22:07). TBD: add the Duels I numbers after ~13:30.

---

## Slide 5: Market-making and pages: where the cash went

**Message:** we didn't pay for a venue we couldn't make better than the free stall. We set the stall to 0% fee and put the cash into the El Retiro page.

- Market-making = Market Test efficiency + value created between other teams on our venue. Matching as well as the free stall earns half the points (RULES.md:82).
- Opening a board venue costs 270 P: a 250 P refundable bond plus 20 P (RULES.md:70).
- Market Test 3.0: our stall scored 0.899 efficiency and 4.8 market, the same as every stall team. No board venue beat the stall (t06 3.66, t13 2.13) (intel/market-log.md 10:00 [V]). In simulation our broker v1 is −1.2 pp vs the stall, so it fails our gate of ≥ stall + 2 pp (market-log 10:03 [L, model]).
- One 7 P trade on Team 12's 0% venue gave it about +3.2 market points. We moved our stall v10 from 3% to 0% from tick 230 (directives 10:06 [V]).
- RET page, complete at 10:27: rares first from El Chato (RET-09 at 87, RET-10 at 86: −19.0), uncommons from Abuela, and the last card (RET-01) from Team 10 at 20 through a team trade: **+50.0 exactly**. Net +28.5 on the set today, inside the +24 to +45 we planned at 09:55 (team/lucas.md 10:27; directives 09:55).
- The same trade was our cap test: 50 measured where 63.9 was uncapped, so the per-trade cap is a flat 50 or 5×book [V, n=2] (intel/GAME.md).

**On screen:** the dashboard's Market tab, `intel/market-log.md`, and the leaderboard's market column.
**Speaker note:** "Evidence first: a broken broker scores 0, and a copy of the stall earns the same as the stall."

---

## Slide 6: Next: Sunday, and what we'd do differently

**Message:** Sunday weighs as much as Saturday (40%) but lasts 6 hours at 15 s ticks, so we prepare now.

- Chamberí is our best set (1.6×). Page bonus ~106; values: common 16, uncommon 40, rare 112, above El Chato's ~90, so dealer buys carry no losses (saturday-plan.md §4B; intel/GAME.md).
- Cash goes to 0 by Sunday 14:00, into buys at or below our value, Chamberí first (GUARDRAIL, directives 02:20).
- 15 s ticks: with the LLM deciding, replies averaged 9.2 s (29 % over 10 s), so Sunday's duelist is code-first: code decides price and day, Claude Haiku 4.5 writes the words (≈ 2 s), with an 8 s failover (docs/duelist-sunday-summary.md).
- Sunday Market Tests: 3 (hours 17, 19, 21) per Dani's audit, newer than the plan's 2. The venue gate deadline is Sun 09:30 (team/dani.md 10:16; directives 09:55).
- What we'd change: one rule, one check (the feeding rule and the cash floor exist in several versions); code edits only in worktrees; test a lever by hand before automating it (DECISIONS.md, entries 3, 7, 12, 16).

**On screen:** the "Open decisions" section of `DECISIONS.md`, then the stage table in saturday-plan.md §2b.
**Speaker note:** TBD after Q7: adjust the length to the judging format.

---

## What we measured

| Fact | Value | How measured | Label |
|---|---|---|---|
| Team trade score | Δ(our whole collection value) − price − fee if we accept | our trades vs `neg_points` (intel/GAME.md) | [V] |
| Taker fee | ceil(5% × price) + 1 P per card; only the taker pays | settlements (intel/GAME.md) | [V] |
| Dealer losses | count in full: MAL-07 −11.8, LAV-05 −8.0, LAV-09 −2.0, RET-09 −10.0, RET-10 −9.0 | `neg_points` before/after each deal (intel/GAME.md) | [V] |
| Dealer gains | don't score: RET-04, RET-03 at 9, worth 11, `neg_points` 0 → 0 | 2 clean windows, Sat 09:41-09:45 (intel/GAME.md) | [V, n=2] |
| Page bonus | 66.25 × multiplier (LAV 86.1, RET 72.9, CHA 106) | `/api/me/value?card=` before/after (intel/GAME.md) | [V] |
| Page bonus route | scores only when a team trade completes the page | Team 17 vs Teams 10, 7, 12 (intel/GAME.md) | [L] |
| Per-trade cap | +50.0 twice: LAV page (Fri, ~89 implied) and RET page (Sat 10:27, 63.9 uncapped); flat 50 or 5×book | our two page-closing team trades (intel/GAME.md) | [V, n=2] |
| Unopened pack drag | ~1-4 points per trade | three gaps fitted (intel/GAME.md) | [L] |
| Relative score | idle teams fall 0.07-1.7 per snapshot | leaderboard snapshots (intel/GAME.md) | [V] |
| 1 `neg_point` | ≈ 0.16 board points | ticks 110-155, Friday (saturday-plan.md §1) | [V] Fri, [L] Sat |
| Duel result | surplus × (1 − decay)^rounds; rounds = min(our messages, theirs) | 30 practice duels; duels 277, 278 (intel/GAME.md) | [V] |
| Round reset | `neg_points` 67.8 → 0 and ladder → 0 at tick 160; holdings carry over | `/api/me` (intel/GAME.md) | [V] |
| Saturday clock | game hour = wall hour (30 s ticks, 120 per hour) | ticks 159 → 173 (directives 09:37) | [V] |
| El Chato, rares | final 86-87 when our +3 steps reach ~69 | 3 deals (intel/GAME.md) | [L, n=3] |
| El Chato, steps | mirrors our step size; finals after ~4-5 rounds | RET-06, Sat 10:07 (intel/GAME.md) | [V] |
| Abuela | opens 12 / 29 / 30 (common / uncommon / pack); after 5-7 rounds: uncommon 21-24, common 9-10 | public feed, all teams (intel/GAME.md) | [V] |
| El Rastro clearing | common 9, uncommon 24.5, rare 70; 5% of asks and 9% of bids filled | Friday feed (intel/GAME.md) | [V] |
| Addressed offers | not private: the public feed shows them | feed `offer.listed` (intel/GAME.md) | [V] |
| Market Test 3.0 | our stall 0.899; every stall team 4.8 market; no board venue beat the stall | snapshot 220 (intel/market-log.md) | [V] |
| Value created on a venue | one 7 P trade ≈ +3.2 market for the owner | Team 12, snapshots 200-220 (intel/market-log.md) | [L] |
| Duel practice | 19 deals / 34 (56%); 15% of value lost to decay | duel monitor (intel/duel-review.md 09:37) | not labelled |

## Cost ledger

| Who / process | Model | Spend | Source |
|---|---|---|---|
| Whole team, Friday | all | ~$2 in total | intel/saturday-sessions.md |
| Lucas: analysts (scout / judge / strategist) | Sonnet 5.5 / Opus 5.5 / Opus 5.5 | TBD. The key had a $1 cap on Friday, hit at 21:59 and raised at 22:19 | saturday-plan.md §5; team/lucas.md Fri 22:12, 22:19 |
| Lucas: dealer narrator (new) | Sonnet 5.5 | ~$0.0007 per message | team/lucas.md 10:35 (Builder) |
| Claude Code sessions (Chief, Operator, Builder, Market) | Opus 5.5 / Fable 5.1 | personal plans, not API credits | CLAUDE.md; intel/saturday-sessions.md |
| Aleks: duelist | Opus strategist + Sonnet negotiator | ~$0.005-0.007 per turn; $0.16 to replay 6 practice duels | team/aleks.md Fri 21:25, 22:07; Sat 09:48 |
| Aleks: hub and demand model | no LLM | API $0; hosting TBD | hub/README.md |
| Dani: Claude Code billed to Dani's API key by mistake | — | $17.65 spent, $82.36 left (the team's Sunday reserve) | team/dani.md 10:12 |
| Dani: dashboard | no LLM | API $0 | dashboard/README.md |
| Saturday and Sunday totals | | TBD | |

## Round-close snapshots

| Moment | Rank, score | `neg_points` / market | Cash | Screenshot | Source |
|---|---|---|---|---|---|
| Fri close (round 1) | #6, 19.99 (frozen at tick 160; #5, 20.03 at 22:55) | 67.8 / — | 252 | TBD | data/leaderboard.jsonl ticks 155, 160 |
| Sat 10:05 (reference only) | #7, 19.20 | −19.0 (10:09) / 5.23 | 202 | — | STATUS.md; intel/metrics.md |
| Sat round 2 close | TBD | TBD | TBD | TBD | |
| Sat close (23:00) | TBD | TBD | TBD | TBD | |
| Sun close | TBD | TBD | TBD | TBD | |

Note: round 2 is Saturday's round (intel/GAME.md). If the desk confirms that the leftover `day_closes` at ~10:49 does nothing, "Sat round 2 close" and "Sat close" become one row.
