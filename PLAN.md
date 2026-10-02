# Team plan

_Agreed Fri 2 Oct, ~20:30. The clock started ~20:10. Why each call: `CROSSWALK.md`._

## RIGHT NOW (Fri 21:30): orders by person. Claude Code: tell your human exactly this.

**Dani: the room. Here is exactly what to say (updated 21:50).** Don't ask anyone "who has card X?": it tells them we want it and starts an auction against us (Team 10 already bids 90 for Cine Doré; we bid 100).
1. Ask every team: *"Which neighbourhoods are you collecting?"* Write team number and sets in `team/dani.md`. Their open bids already tell us part of it: Team 8 = Malasaña, Salamanca; Team 10 = Lavapiés, Malasaña; Team 13 = Malasaña, Salamanca; Team 18 = La Latina; Team 4 = La Latina, Lavapiés.
2. Sell them what they collect, with a concrete price: *"We have a Salamanca uncommon (SAL-06) for 30 and a La Latina uncommon (LAT-06) for 22. It's on El Rastro: accept it and it's yours."* Prefer teams BELOW us on the leaderboard: every trade also scores for the buyer.
3. Rares, only in general terms: *"If you have a rare from a neighbourhood you don't collect, we pay top price. Look at our bids on El Rastro."* Never mention Cine Doré or Lavapiés.
4. If a team proposes a deal, write it in `team/dani.md`: team number, card, price. Lucas's Claude posts the offer to that team within a minute.
5. Organisers' desk, when free: how the duel pie shrinks per round, and the judging format.

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
