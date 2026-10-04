# v10 matchmaker: page finishers and first copies

_Written by `tools/matchmaker.py` at 12:44 (tick 2262). Read-only. Holdings: the feed's copies (gifts, eggs and Workshop crafts included) plus the page arithmetic on the leaderboard's album_filled/pages_complete and minted supply (`tools/album.py`; 0 conflicts with intel/holdings-audit.md). ✓ = a proven gap, a bid since Saturday, or a want-list; "undecided" = the buyer may hold it. Giver: a true duplicate or a set it dumps (held back when its page is complete and under two copies are seen after its last craft); receiver: no copy, collects the set; both gain > 0 at the price (conservative multipliers). Want-lists: `intel/wants.md`. Never a page-closer for a rival or a team < 6 below us; a rival on either side gains <= 10 P at our price. Venue: a club deal (both sides in the club) alternates v10 / a member's market (least used, then lowest market score, never either side's own; page-closers on v10); every other deal on v10._

## Matches (best first)

| # | Buyer | Card | Seller | Venue | Price | Value created | Closer | Rival | Why |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Team 7 | CHA-08 El Instituto | Team 1 | v10 | ~24 | +20.6 (low +20.6) |  |  | bid ✓ · undecided · seller holds 2 |
| 2 | Team 8 | MAL-06 Tienda de Discos | Team 7 | v10 · club | ~26 | +13.9 (low +13.9) |  |  | bid · **ask first** · seller dumps MAL · ask first: t08 sold a MAL-06 at tick 510, it may keep another |
| 3 | Team 17 | RET-06 La Rosaleda | Team 8 | v10 | ~24 | +9.4 (low +9.4) |  | rival buyer | bid ✓ · undecided · seller dumps RET |
| 4 | Team 16 | RET-04 Paseo de Coches | Team 1 | v10 | ~8 | +7 (low +7) |  |  | bid ✓ · gap proven · seller holds 2 · also t08 |
| 5 | Team 8 | MAL-02 Plaza del Dos de Mayo | Team 14 | v10 | ~9 | +6.3 (low +6.3) |  |  | bid · **ask first** · seller dumps MAL · also t06, t16, t02 · ask first: t08 sold a MAL-02 at tick 171, it may keep another |
| 6 | Team 3 | LAT-05 El Organillero | Team 2 | v10 | ~8 | +5 (low +4) |  | rival buyer | bid ✓ · undecided · seller dumps LAT · also t09 |
| 7 | Team 17 | RET-05 La Ardilla | Team 8 | v10 | ~9 | +3.7 (low +3.7) |  | rival buyer | bid ✓ · undecided · seller dumps RET |
| 8 | Team 16 | RET-01 Barca del Estanque | Team 8 | v10 | ~8 | +2.4 (low +2.4) |  |  | bid ✓ · gap proven · seller dumps RET |
| 9 | Team 16 | RET-03 El Titiritero | Team 8 | v10 | ~8 | +2.4 (low +2.4) |  |  | bid ✓ · gap proven · seller dumps RET · also t04 |

## Ready DMs

**1. CHA-08 · Team 1 → Team 7 at ~24 P on v10**
- To Team 1: "Hi Team 1! Could you post your El Instituto (CHA-08) on v10 as an ask addressed to Team 7, at ~24 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 7: "Hi Team 7! Team 1 can post El Instituto (CHA-08) on v10 as an ask addressed to Team 7, at ~24 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**2. MAL-06 · Team 7 → Team 8 at ~26 P on v10**
- To Team 7: "Hi Team 7! Could you post your Tienda de Discos (MAL-06) on v10 as an ask addressed to Team 8, at ~26 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 8: "Hi Team 8! Team 7 can post Tienda de Discos (MAL-06) on v10 as an ask addressed to Team 8, at ~26 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**3. RET-06 · Team 8 → Team 17 at ~24 P on v10**
- To Team 8: "Hi Team 8! Could you post your La Rosaleda (RET-06) on v10 as an ask addressed to Team 17, at ~24 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 17: "Hi Team 17! Team 8 can post La Rosaleda (RET-06) on v10 as an ask addressed to Team 17, at ~24 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**4. RET-04 · Team 1 → Team 16 at ~8 P on v10**
- To Team 1: "Hi Team 1! Could you post your Paseo de Coches (RET-04) on v10 as an ask addressed to Team 16, at ~8 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 1 can post Paseo de Coches (RET-04) on v10 as an ask addressed to Team 16, at ~8 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**5. MAL-02 · Team 14 → Team 8 at ~9 P on v10**
- To Team 14: "Hi Team 14! Could you post your Plaza del Dos de Mayo (MAL-02) on v10 as an ask addressed to Team 8, at ~9 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 8: "Hi Team 8! Team 14 can post Plaza del Dos de Mayo (MAL-02) on v10 as an ask addressed to Team 8, at ~9 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**6. LAT-05 · Team 2 → Team 3 at ~8 P on v10**
- To Team 2: "Hi Team 2! Could you post your El Organillero (LAT-05) on v10 as an ask addressed to Team 3, at ~8 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 3: "Hi Team 3! Team 2 can post El Organillero (LAT-05) on v10 as an ask addressed to Team 3, at ~8 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**7. RET-05 · Team 8 → Team 17 at ~9 P on v10**
- To Team 8: "Hi Team 8! Could you post your La Ardilla (RET-05) on v10 as an ask addressed to Team 17, at ~9 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 17: "Hi Team 17! Team 8 can post La Ardilla (RET-05) on v10 as an ask addressed to Team 17, at ~9 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**8. RET-01 · Team 8 → Team 16 at ~8 P on v10**
- To Team 8: "Hi Team 8! Could you post your Barca del Estanque (RET-01) on v10 as an ask addressed to Team 16, at ~8 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 8 can post Barca del Estanque (RET-01) on v10 as an ask addressed to Team 16, at ~8 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

## Teams one or two cards from a page

- Team 3 LAV 8/10 · missing LAV-02 (undecided), LAV-04 (undecided) · rival · **may be complete**

## Held back (never suggested)

- MAL-02 for Team 8: seller safety: Team 17's MAL page is complete and only 0 copies of it seen after its last common craft (tick 929)
- MAL-02 for Team 8: seller safety: Team 10's MAL page is complete and only 0 copies of it seen after its last common craft (tick 1718)
- RET-01 for Team 13: seller safety: Team 1's RET page is complete and only 1 copy of it seen after its last common craft (tick 1333)
- RET-01 for Team 16: seller safety: Team 18's RET page is complete and only 1 copy of it seen after its last common craft (tick 2216)
- RET-01 for Team 16: seller safety: Team 12's RET page is complete and only 1 copy of it seen after its last common craft (tick 1114)
- RET-01 for Team 16: seller safety: Team 1's RET page is complete and only 1 copy of it seen after its last common craft (tick 1333)
- RET-04 for Team 16: seller safety: Team 18's RET page is complete and only 0 copies of it seen after its last common craft (tick 2216)

## Holdings (page arithmetic)

| Team | Status | Held | Proven gaps | Undecided |
|---|---|---|---|---|
| Team 1 | exact | 49/49 | 11 | 0 |
| Team 2 | partial | 36/41 | 2 | 22 |
| Team 3 | partial | 30/40 | 8 | 22 |
| Team 4 | exact | 43/43 | 17 | 0 |
| Team 6 | repaired | 40/48 | 11 | 9 |
| Team 7 | partial | 40/41 | 7 | 13 |
| Team 8 | partial | 39/44 | 3 | 18 |
| Team 9 | partial | 42/46 | 10 | 8 |
| Team 10 | exact | 41/41 | 19 | 0 |
| Team 11 | partial | 1/13 | 12 | 47 |
| Team 12 | exact | 45/45 | 15 | 0 |
| Team 13 | inconsistent | 0/32 | 0 | 0 |
| Team 14 | partial | 42/43 | 8 | 10 |
| Team 15 | exact | 43/43 | 17 | 0 |
| Team 16 | exact | 44/44 | 16 | 0 |
| Team 17 | partial | 39/40 | 9 | 12 |
| Team 18 | exact | 47/47 | 13 | 0 |

- run/known_holdings.json entry for Team 5 ignored: the feed shows MAL-07, MAL-10 held.

- run/known_holdings.json entry for Team 15 ignored: the feed shows MAL-09, MAL-10 held.
