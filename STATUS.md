# Team 5 — live status

_Auto-updated by `tools/status.py` (read-only). Last update **Fri 21:50** · tick 90 (60 s/tick) · game hour 1.50 · running · today closes 23:00._

## Team: now and latest

_From `team/<name>.md`; each person writes only their own file._

**Aleks** — Duels: Clock-Standing on the duel API (`duels`, `duel_say`, `duel_accept`), on Claude, for the practice duels (~22:20). _Aleks: replace this line with what you are actually doing._

**Dani** — Reading RULES.md (duels, ladder, scoring) so I can ask the organisers' desk sharp questions; going to the desk before the practice duels (~22:20).
  - Fri 21:45 · read the public feed (no key) · **Team 10 outbid us on LAV-09: 90 P (offer #1114, tick 76) vs our 85 (#910).** Also: the feed's `offer.listed` events carry the real maker team id, so 65 of the 77 "anonymous" El Rastro offers can be matched to a team (feed → offer id → actor) · next: Lucas decides on LAV-09; I'm building a read-only dashboard on this
  - Fri 21:25 · checked the 5 questions against RULES.md · Q2 already answered (a deal at the dealer's opening price doesn't count, line 35); the other 4 sharpened (duel pie decay formula, early-unlock count, level 2 timing, judging format, whether pack prices count in neg_points) · next: organisers' desk

**Lucas** — `autoflip.py` live: fills other teams' bids with cards bought from Abuela at her first price when the sale scores ≥8. `loop.py` sells our cards into good bids and buys underpriced listings. LAV-09 bid 100. Listings repriced to market (LAT-06 22, SAL-06 30). Watcher live
  - Fri 21:46 · LAT-06 sold at 22 within ~3 min of repricing it to the market (was unsold at 30 for 15 min) · `neg_points` 16.6 → 26.3 · lesson: price at the market's bid level, it fills fast
  - Fri 21:50 · stopped the LAT flip before buying (collectors bid 16, not 27); Team 8's 35 bid for MAL-07 vanished while we haggled · autoflip live: takes Abuela's first price and sells into the bid in ~2 ticks · Dani's script for the room is in PLAN.md
  - Fri 21:43 · Dani spotted Team 10 bidding 90 for LAV-09 · raised ours to 100 (worth 91 now; the page bonus scores if LAV-06/07 come last from teams; also blocks Team 10's page) · LAT flip restarted with caps 25/10 (Abuela stops at ~24)

## Score

| Total | Rank | Negotiating | Market | Duel pts | Ladder pts | Bench eff. | Deals | Level | Cash | Album |
|---|---|---|---|---|---|---|---|---|---|---|
| 17.80 | 8 | 17.80 | 0.00 | 0.00 | 0.06 | — | 15 | 1 | 380 | 16/40 |

Leaderboard (snapshot at tick 90; refreshes every few minutes):

| # | Team | Score | Negotiating | Market | Deals |
|---|---|---|---|---|---|
| 1 | Team 13 | 27.83 | 27.83 | 0.00 | 13 |
| 2 | Team 18 | 25.11 | 25.11 | 0.00 | 9 |
| 3 | Team 8 | 24.99 | 24.99 | 0.00 | 8 |
| 4 | Team 10 | 23.97 | 23.97 | 0.00 | 13 |
| 5 | Team 12 | 21.16 | 21.16 | 0.00 | 12 |
| 8 | Team 5 | 17.80 | 17.80 | 0.00 | 15 |

## Next on the schedule

_ETA assumes the current tick length and no pause._

| Game hour | ETA | Action | Note |
|---|---|---|---|
| 2.00 | ~30 min | duels | Practice duels (not scored): learn the protocol |
| 3.00 | ~90 min (after today's close) | bench | The Market Test: every venue gets the same synthetic book |
| 4.00 | ~150 min (after today's close) | round | Round 2 starts (holdings carry over) |
| 4.00 | ~150 min (after today's close) | set_release | El Retiro released |
| 4.00 | ~150 min (after today's close) | day_closes | Closed until Saturday 09:00 |
| 4.00 | ~150 min (after today's close) | day_opens | Saturday opens |
| 4.05 | ~153 min (after today's close) | grant_all | El Retiro has arrived: a pack and the Saturday allowance (150 primas) for everyone |
| 5.00 | ~210 min (after today's close) | bench | The Market Test: every venue gets the same synthetic book |

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
| 147 | abuela | buy | LAT-08 | 29 | 16 | — | — | 8 | closed |  |
| 160 | abuela | buy | MAL-07 | 29 | 16 | — | — | 4 | closed |  |

## Abuela benchmark: every team's deals with her (public feed)

| Item | Side | All deals | Median | Min | Max | Ours | Our avg |
|---|---|---|---|---|---|---|---|
| common card | team buys | 20 | 9.50 | 7 | 12 | 2 | 9 |
| common card | team sells | 18 | 9.50 | 5 | 23 | 4 | 5.50 |
| sobre_barrio | team buys | 25 | 22 | 17 | 30 | 3 | 20.33 |
| uncommon card | team buys | 24 | 22.00 | 17 | 25 | 1 | 24 |
| uncommon card | team sells | 4 | 14.00 | 13 | 16 | 0 | — |

## Duels

Live: 0 · finished: 0


## Dealers

| Dealer | Status | Level | Open to us | Sells | Buys | Deals/hour |
|---|---|---|---|---|---|---|
| abuela | active | 1 | True | sobre_barrio (26 P), common (10 P), uncommon (25 P) | common, uncommon | 8 |
| chato | announced | — | False |  |  | — |

## Levels

- El Chato: None — 
