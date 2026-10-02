# Team plan

_Agreed Fri 2 Oct, ~20:30. The clock started ~20:10. Why each call: `CROSSWALK.md`._

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

**Dani: the desk, the page-gap desk, the judges' story.**
1. **09:00, organisers' desk**: the 8 questions in plan §3, answers in `team/dani.md` at once.
2. **From ~10:00, page-gap desk** (plan §6b): `intel/sellable.md` lists, one line each, which team lacks a card we have
   spare (and what to say), and which team holds a card we need (and our live bid). Only point teams at offers already
   live; never name a price that isn't in the file. Lucas will also tell you in person when a big one appears.
3. **Judges (40%)**: the judging format by 09:30; `docs/demo.md` skeleton; screenshot the big screen at each round close;
   draft the pitch with Lucas during Duels I.

**Lucas (+ 3 Claude Code sessions: operator, strategy, builder)**: decides, is the human channel, owns the story. Only the
operator writes to the game. Never buy from a dealer above our value; never feed teams within 10 points of us.

## How the clock works

A **tick** is when the game settles: every 60 s tonight, every 30 s on Saturday, every 15 s on Sunday. The organisers can move it anywhere between 5 and 60 s.

Per tick, the **team** can:
- send **one message per conversation**, with up to 6 conversations open at once;
- **accept one offer**. This one limit is shared by the whole team, duels and dealers included;
- post up to 12 listings.

Reads (prices, offers, clock) are not tied to ticks: up to 5 requests per second.

**Every script waits for the server's tick (`b.wait_tick()`) and never sleeps for a fixed 60 s.**

## Who owns what

| Owner | Job | Writes with the team key? |
|---|---|---|
| **Aleks** | Duels: the live duel agent | Yes, duel endpoints only |
| **Lucas** (+ Claude Code) | Dealers (Abuela and the ones after her), our own market (broker), analysis | Yes, dealer and market endpoints only |
| **Dani** | Judges (40%): the story, the demo, the decisions log. Organiser questions. Watching other teams | No |

## Today (Friday counts half; doors close at 23:00)

**The one event tonight: the practice duels, around 22:10.** They don't score, but they are our first real games against other teams.

**Aleks**
- Connect Clock-Standing to the duel API (`duels()`, `duel_say(text, price)`, `duel_accept()`), on Claude, with full logs. Target: the practice duels.
- If it isn't ready by 22:00, a simple script plays instead. It's practice; the logs are what we need.
- Push the bench code tonight, so decay can go in tomorrow.

**Lucas**
- An Abuela bot built from the starter, with two changes:
  - **It counters before it accepts.** Her first offer was 17 P and the starter took it as-is, so that deal probably doesn't count as negotiated. Three negotiated deals give us early access to level 2, and level 2 lets us open our own market (30% of the score).
  - **It never takes cash below 270 P**, the bond for that market.
- The bot never accepts while a duel is live, since the team gets one accept per tick.
- A read-only monitor: clock, cash, deals, duel results. In the practice duels, measure how fast the pie shrinks.

**Dani**
- Take these four questions to the organiser desk now:
  1. How exactly does the duel pie shrink per round, and how is a duel scored?
  2. Does a deal at a dealer's first offer count as negotiated?
  3. When does level 2 open?
  4. How do the judges evaluate, and what do they want to see?
- Start `DECISIONS.md`: one line per decision, with the reason. It becomes our story for the judges. It can be edited on the GitHub website.
- Watch the big screen during the practice duels and note what other teams do.

## Tomorrow

- **Aleks:** two-issue duels (price + delivery day) before Duels II (~18:00). Decay in the bench.
- **Lucas:** the broker for the Market Test (30%), simulated offline first.
- **Dani:** the story and demo for the judges.

## Team rules

1. **One script per job, one owner.** Say in the team chat when a script starts and when it stops.
2. **Each job has its own folder:** `agents/duels/`, `agents/dealers/`, `broker/`, `tools/`. Work on `main`, pull before you push.
3. **Keys stay in `.env`, never in GitHub.** Each person spends their own $100 on their own job. Dani's $100 is the reserve for Sunday.
4. **Sync for 10 minutes at schedule events, not clock times** (the clock already slipped): before the practice duels, at Friday's close, before Duels I, before Duels II.
