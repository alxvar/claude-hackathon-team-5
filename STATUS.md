# Team 5 — live status

_Auto-updated by `tools/status.py` (read-only). Last update **Fri 21:15** · tick 55 (60 s/tick) · game hour 0.92 · running · today closes 23:00._

## Team: now and latest

_From `team/<name>.md`; each person writes only their own file._

**Aleks** — Duels: Clock-Standing on the duel API (`duels`, `duel_say`, `duel_accept`), on Claude, for the practice duels (~22:20). _Aleks: replace this line with what you are actually doing._

**Dani** — Five questions to the organisers' desk (the four in `PLAN.md`, plus: what is `neg_points`?). _Dani: replace this line with what you are actually doing._

**Lucas** — E3 team trades live (`agents/trader/trade.py`): 3 sells listed, bids for LAV-09 (70 P) and LAV-06 (24 P). E2 bot selling spares to Abuela (`--no-buy`). Watching the leaderboard and our score live (`tools/watch.py`). Next: Market Test broker.
  - Fri 21:18 · per-person files under `team/` + `merge=union` on logs: two people can no longer conflict on the same file · everyone writes only in their own `team/<name>.md`

## Score

| Total | Rank | Negotiating | Market | Duel pts | Ladder pts | Bench eff. | Deals | Level | Cash | Album |
|---|---|---|---|---|---|---|---|---|---|---|
| 13.21 | 5 | 13.21 | 0.00 | 0.00 | 0.06 | — | 8 | 1 | 327 | 17/40 |

Leaderboard (snapshot at tick 55; refreshes every few minutes):

| # | Team | Score | Negotiating | Market | Deals |
|---|---|---|---|---|---|
| 1 | Team 13 | 28.15 | 28.15 | 0.00 | 10 |
| 2 | Team 10 | 28.10 | 28.10 | 0.00 | 9 |
| 3 | Team 14 | 23.68 | 23.68 | 0.00 | 6 |
| 4 | Team 8 | 23.23 | 23.23 | 0.00 | 4 |
| 5 | Team 5 | 13.21 | 13.21 | 0.00 | 8 |

## Next on the schedule

_ETA assumes the current tick length and no pause._

| Game hour | ETA | Action | Note |
|---|---|---|---|
| 2.00 | ~65 min | duels | Practice duels (not scored): learn the protocol |
| 3.00 | ~125 min (after today's close) | bench | The Market Test: every venue gets the same synthetic book |
| 4.00 | ~185 min (after today's close) | round | Round 2 starts (holdings carry over) |
| 4.00 | ~185 min (after today's close) | set_release | El Retiro released |
| 4.00 | ~185 min (after today's close) | day_closes | Closed until Saturday 09:00 |
| 4.00 | ~185 min (after today's close) | day_opens | Saturday opens |
| 4.05 | ~188 min (after today's close) | grant_all | El Retiro has arrived: a pack and the Saturday allowance (150 primas) for everyone |
| 5.00 | ~245 min (after today's close) | bench | The Market Test: every venue gets the same synthetic book |

## Our dealer deals

_Her first = her first price in the conversation. A deal at her first price probably doesn't count as negotiated._

| Thread | Dealer | Side | Item | Her first | Our first | Deal | vs her first | Msgs | Status | Closed |
|---|---|---|---|---|---|---|---|---|---|---|
| 10 | abuela | buy | sobre_barrio | 17 | — | 17 | +0% | 1 | deal |  |
| 29 | abuela | buy | sobre_barrio | 30 | 16 | 22 | -27% | 7 | deal |  |
| 36 | abuela | buy | sobre_barrio | 30 | 16 | 22 | -27% | 9 | deal |  |
| 40 | abuela | buy | LAV-05 | 12 | 7 | 9 | -25% | 5 | deal |  |
| 45 | abuela | buy | LAV-02 | 12 | 7 | 9 | -25% | 7 | deal |  |
| 82 | abuela | buy | LAV-08 | 29 | 16 | 24 | -17% | 11 | deal |  |
| 95 | abuela | buy | LAV-07 | 29 | 16 | — | — | 2 | closed |  |
| 97 | abuela | sell | 1 card(s) | 5 | 9 | — | — | 2 | open |  |

## Abuela benchmark: every team's deals with her (public feed)

| Item | Side | All deals | Median | Min | Max | Ours | Our avg |
|---|---|---|---|---|---|---|---|
| common card | team buys | 15 | 10 | 7 | 12 | 2 | 9 |
| common card | team sells | 9 | 13 | 5 | 23 | 0 | — |
| sobre_barrio | team buys | 18 | 20.00 | 17 | 24 | 3 | 20.33 |
| uncommon card | team buys | 16 | 22.50 | 17 | 25 | 1 | 24 |
| uncommon card | team sells | 3 | 13 | 13 | 16 | 0 | — |

## Duels

Live: 0 · finished: 0


## Dealers

| Dealer | Status | Level | Open to us | Sells | Buys | Deals/hour |
|---|---|---|---|---|---|---|
| abuela | active | 1 | True | sobre_barrio (26 P), common (10 P), uncommon (25 P) | common, uncommon | 8 |

## Levels

_None announced yet._
