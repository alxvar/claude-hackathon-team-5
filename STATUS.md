# Team 5 — live status

_Auto-updated by `tools/status.py` (read-only). Last update **Fri 21:41** · tick 81 (60 s/tick) · game hour 1.35 · running · today closes 23:00._

## Team: now and latest

_From `team/<name>.md`; each person writes only their own file._

**Aleks** — Duels: Clock-Standing on the duel API (`duels`, `duel_say`, `duel_accept`), on Claude, for the practice duels (~22:20). _Aleks: replace this line with what you are actually doing._

**Dani** — Reading RULES.md (duels, ladder, scoring) so I can ask the organisers' desk sharp questions; going to the desk before the practice duels (~22:20).
  - Fri 21:25 · checked the 5 questions against RULES.md · Q2 already answered (a deal at the dealer's opening price doesn't count, line 35); the other 4 sharpened (duel pie decay formula, early-unlock count, level 2 timing, judging format, whether pack prices count in neg_points) · next: organisers' desk

**Lucas** — FLIP (`agents/trader/flip.py`): buying La Latina cards from Abuela (we value them least) and listing them for LAT collectors at 26 (uncommons) / 11 (commons). E3 autopilot + 19 offers up. Spares now listed for teams at 10, no longer sold to Abuela. Watcher live
  - Fri 21:38 · found the scoring lever (LOG finding 11): sales to teams score price − our value, dealer buys cost only cash · stopped selling spares to Abuela (0 points) and listed them for teams; started flipping LAT cards (buy from Abuela, list at 26/11) · next: measure the first flip's points
  - Fri 21:34 · El Chato (level 2) announced; dealer bot gained `--ladder` (cheapest menu items, packs included) for when he opens · our multipliers found in `/api/me`: CHA 1.6 (Sunday), LAV 1.3, RET 1.1 (Saturday) · next: Chato's 3 deals the moment he opens
  - Fri 21:32 · MAL-06 bought at 12 (+5.2) and LAT-07 sold at 21 (+8.7): `neg_points` 16.6 · repriced sells toward the buyer's value (finding 7), raised SAL/MAL bids, added MAL rare bids · next: watch fills, reprice every ~10 min

## Score

| Total | Rank | Negotiating | Market | Duel pts | Ladder pts | Bench eff. | Deals | Level | Cash | Album |
|---|---|---|---|---|---|---|---|---|---|---|
| 16.15 | 8 | 16.15 | 0.00 | 0.00 | 0.06 | — | 14 | 1 | 358 | 17/40 |

Leaderboard (snapshot at tick 80; refreshes every few minutes):

| # | Team | Score | Negotiating | Market | Deals |
|---|---|---|---|---|---|
| 1 | Team 13 | 26.89 | 26.89 | 0.00 | 12 |
| 2 | Team 18 | 25.66 | 25.66 | 0.00 | 8 |
| 3 | Team 8 | 24.99 | 24.99 | 0.00 | 8 |
| 4 | Team 10 | 24.65 | 24.65 | 0.00 | 12 |
| 5 | Team 12 | 21.40 | 21.40 | 0.00 | 11 |
| 8 | Team 5 | 16.15 | 16.15 | 0.00 | 14 |

## Next on the schedule

_ETA assumes the current tick length and no pause._

| Game hour | ETA | Action | Note |
|---|---|---|---|
| 2.00 | ~39 min | duels | Practice duels (not scored): learn the protocol |
| 3.00 | ~99 min (after today's close) | bench | The Market Test: every venue gets the same synthetic book |
| 4.00 | ~159 min (after today's close) | round | Round 2 starts (holdings carry over) |
| 4.00 | ~159 min (after today's close) | set_release | El Retiro released |
| 4.00 | ~159 min (after today's close) | day_closes | Closed until Saturday 09:00 |
| 4.00 | ~159 min (after today's close) | day_opens | Saturday opens |
| 4.05 | ~162 min (after today's close) | grant_all | El Retiro has arrived: a pack and the Saturday allowance (150 primas) for everyone |
| 5.00 | ~219 min (after today's close) | bench | The Market Test: every venue gets the same synthetic book |

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
| 97 | abuela | sell | 1 card(s) | 5 | 9 | 6 | +20% | 9 | deal |  |
| 104 | abuela | sell | 1 card(s) | 5 | 9 | 6 | +20% | 7 | deal |  |
| 114 | abuela | sell | 1 card(s) | 5 | 9 | 5 | +0% | 9 | deal |  |
| 124 | abuela | sell | 1 card(s) | 5 | 9 | 5 | +0% | 9 | deal |  |
| 136 | abuela | sell | 1 card(s) | — | — | — | — | 0 | closed |  |
| 138 | abuela | buy | LAT-08 | 29 | 16 | — | — | 7 | closed |  |
| 145 | abuela | buy | LAT-07 | — | — | — | — | 0 | closed |  |
| 147 | abuela | buy | LAT-08 | 29 | 16 | — | — | 2 | open |  |

## Abuela benchmark: every team's deals with her (public feed)

| Item | Side | All deals | Median | Min | Max | Ours | Our avg |
|---|---|---|---|---|---|---|---|
| common card | team buys | 20 | 9.50 | 7 | 12 | 2 | 9 |
| common card | team sells | 18 | 9.50 | 5 | 23 | 4 | 5.50 |
| sobre_barrio | team buys | 24 | 21.50 | 17 | 30 | 3 | 20.33 |
| uncommon card | team buys | 22 | 22.50 | 17 | 25 | 1 | 24 |
| uncommon card | team sells | 3 | 13 | 13 | 16 | 0 | — |

## Duels

Live: 0 · finished: 0


## Dealers

| Dealer | Status | Level | Open to us | Sells | Buys | Deals/hour |
|---|---|---|---|---|---|---|
| abuela | active | 1 | True | sobre_barrio (26 P), common (10 P), uncommon (25 P) | common, uncommon | 8 |
| chato | announced | — | False |  |  | — |

## Levels

- El Chato: None — 
