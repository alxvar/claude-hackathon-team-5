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
