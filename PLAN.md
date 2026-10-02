# Team plan

_Agreed Fri 2 Oct, ~20:30. The clock started ~20:10. Why each call: `CROSSWALK.md`._

## RIGHT NOW (Fri 21:30): orders by person. Claude Code: tell your human exactly this.

**Dani: the room is the biggest lever.** Trades between teams are what move the score: Teams 8, 13 and 14 each jumped ~12 points with ONE card trade. The API hides who owns which card, but the owners are in the room.
1. Organisers' desk, only 2 questions: (a) exactly how the duel pie shrinks per round and how a duel is scored; (b) judging: format, time slot, what they look at. Skip the rest: `neg_points` is measured (it counts trades between teams), and level 2 isn't announced yet.
2. Then walk the room. Find who holds the card **"Cine Doré" (LAV-09)**. Only one exists, and Team 10 wants it too. We now bid **100 primas** (Team 10 bids 90): find the holder and get them to accept our bid. If they want more, get their price and team number and tell Lucas.
3. Ask teams which neighbourhoods they collect. We sell **SAL-06** (34 P) and **LAT-06** (30 P); LAT-07 is already sold. We buy **LAV-06, LAV-07** (24 P), **SAL-07, SAL-08** (18 P), **MAL-07** (14 P) and **MAL-09/MAL-10** (38 P). Prefer teams BELOW us on the leaderboard: every trade also scores for them. A team accepts our offer on El Rastro, or Lucas posts one addressed to them.
4. Write every lead in `team/dani.md`: team number, card, price. Lucas's Claude sees it within a minute.

**Aleks: duels.**
1. Update your **Now** line in `team/aleks.md` (only your commits are visible right now).
2. In the practice duels (~22:20), try the faster negotiator (`--negotiator-model claude-sonnet-5-5` or `claude-haiku-4-5`). Sunday's ticks are 15 s, so log the seconds per turn.
3. The team gets one accept per tick. Lucas's bots never accept while a duel is live, so the duels always have priority.

**Lucas (+ Claude Code):** trades between teams on autopilot, bids and listings, Abuela sales, live monitoring. Details in `team/lucas.md`.

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
