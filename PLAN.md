# Team plan

_Updated Sat 01:30. The full, verified plan is `intel/saturday-plan.md`; measured facts are in `intel/GAME.md`._

## RIGHT NOW (Sat 09:00): orders by person. Claude Code: tell your human exactly this.

The full plan, verified by independent checks, is **`intel/saturday-plan.md`**. Read §1 (the game on one page) and your
own section. It supersedes every Friday order below where they conflict.

**Aleks: duels (Duels I at 11:30 if the clock jumps to hour 4.0 at 09:00, ~12:51 if it resumes at 2.65).**
1. Before Duels I, in `agents/duelist/` (plan §4D), each with a regression test on `docs/duels/`:
   - deadline trigger: decide at `ticks_left ≤ 3`; at ≤ 2 accept any standing offer inside our limit, in code
     (duel 181 must accept 73 by tick 143);
   - from `ticks_left ≤ 4`, close by sending the rival's own standing price (they spend their accept, not ours);
   - decay-aware accept: accept an in-limit offer when the gap ≤ max(2 P, 2d/(1−d) × our surplus);
   - hold breaker: both sides still 3 ticks with ≥ 3 left → force a decision (duels 103/104);
   - silent rival: concede on a code schedule toward a floor (keep ≥ 30% of anchor-to-limit); silence costs no decay;
   - prompt fix: decay is per exchange, not per tick (`agent.py:148,178`); read session parameters from the payload.
2. Before Duels II (18:00 / ~19:21): `days` payload shapes (number / list / dict) tested offline; day value computed in
   code; full packages; ≤ 3 exchanges at 8% decay.
3. Sunday: Sonnet as strategist (15 s ticks; Opus peaked at 14.2 s).
4. Laptop on mains + `caffeinate`; check your API key's spend limit before 11:00 (Lucas's was $1 on Friday).
5. Write `team/aleks.md` Now line; review the accept arbiter (plan §5) with Lucas's builder session.
6. Repo fixes in your files (found by Friday night's audit): the decay text also in `agents/duelist/prompts/negotiator.md:11`,
   `prompts/strategist.md:26-28` and `docs/duelist-runbook.md` ("per tick" → per exchange; l.30 vs l.67 contradict);
   `docs/duels/README.md` labels the practice as "Duels I" (fix in `records.py` `summary()`); `.env.template` duplicates
   `.env.example` without `export` (delete it, point the runbook to `.env.example`); add a "pre-rules history" banner to
   `docs/how-the-leading-model-works.md`, `what-we-tried-so-far.md`, `plan-clock-standing-on-bazaar.md`.

**Dani: the desk, the page-gap desk, the judges' story.**
1. **09:00, organisers' desk**: the 8 questions in plan §3, answers in `team/dani.md` at once.
2. **From ~10:00, page-gap desk** (plan §6b): `intel/sellable.md` lists, one line each, which team lacks a card we have
   spare (and what to say), and which team holds a card we need (and our live bid). Only point teams at offers already
   live; never name a price that isn't in the file. Lucas will also tell you in person when a big one appears.
3. **Judges (40%)**: the judging format by 09:30; `docs/demo.md` skeleton; screenshot the big screen at each round close;
   draft the pitch with Lucas during Duels I.
4. Repo fixes in your files: `dashboard/server.py` (l.816, 874) writes "never the top 3" into `intel/teams.md`; the rule is
   now top 4, plus page-completing cards only to teams ≥ 10 points below us. Move `judges/team-messages.md` (Friday chat
   drafts, incl. "buy LAV-09 from Chato") to `archive/fri/`. Your "Touches" line: the dashboard also writes `intel/teams.md`.

**Lucas (+ 3 Claude Code sessions: operator, strategy, builder)**: decides, is the human channel, owns the story. Only the
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
| **Lucas** (+ 3 Claude Code sessions) | Operator (the only writer to the game: trades, dealers, venue), strategy, builder | Yes, operator session only |
| **Dani** | Organisers' desk, page-gap desk (`intel/sellable.md`), judges' story (40%) | No |

## Team rules

1. **One script per job, one owner.** Say in the team chat when a script starts and when it stops.
2. **Each job has its own folder:** `agents/duelist/`, `agents/dealers/`, `agents/trader/`, `broker/`, `tools/`, `dashboard/`. Work on `main`, pull before you push.
3. **Keys stay in `.env`, never in GitHub.** Each person spends their own $100 on their own job. Dani's $100 is the reserve for Sunday.
4. **Sync for 10 minutes at schedule events, not clock times** (the clock already slipped): at 09:00 after the clock check, before Duels I, before Duels II, at each round close.
5. **Feeding rule:** a page-completing card goes only to a team ≥ 10 points below us and never to the top 4 (plan §4A).
