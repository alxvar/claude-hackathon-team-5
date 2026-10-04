# v10 matchmaker: page finishers and first copies

_Written by `tools/matchmaker.py` at 11:10 (tick 1902). Read-only. Holdings: the feed's copies (gifts, eggs and Workshop crafts included) plus the page arithmetic on the leaderboard's album_filled/pages_complete and minted supply (`tools/album.py`; 0 conflicts with intel/holdings-audit.md). ✓ = a proven gap, a bid since Saturday, or a want-list; "undecided" = the buyer may hold it. Giver: a true duplicate or a set it dumps (held back when its page is complete and under two copies are seen after its last craft); receiver: no copy, collects the set; both gain > 0 at the price (conservative multipliers). Want-lists: `intel/wants.md`. Never a page-closer for a rival or a team < 6 below us; a rival on either side gains <= 10 P at our price. Venue: a club deal (both sides in the club) alternates v10 / a member's market (least used, then lowest market score, never either side's own; page-closers on v10); every other deal on v10._

## Matches (best first)

| # | Buyer | Card | Seller | Venue | Price | Value created | Closer | Rival | Why |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Team 9 | LAV-02 El Frutero de Argumosa | Team 16 | v10 | ~9 | +13 (low +11.2) |  |  | bid ✓ · undecided · seller holds 2 · also t04, t18 · spare unverified: 1 seen after its common craft at tick 730 |
| 2 | Team 8 | MAL-06 Tienda de Discos | Team 4 | v10 · club | ~26 | +10.1 (low +10.1) |  |  | bid ✓ · undecided · seller dumps MAL |
| 3 | Team 16 | RET-06 La Rosaleda | Team 8 | v10 | ~22 | +6.7 (low +6.7) |  |  | bid ✓ · undecided · seller dumps RET |
| 4 | Team 8 | MAL-02 Plaza del Dos de Mayo | Team 16 | v10 | ~9 | +6.3 (low +6.3) |  |  | bid ✓ · undecided · seller dumps MAL · also t14, t04, t03 |
| 5 | Team 16 | RET-03 El Titiritero | Team 4 | v10 | ~8 | +5.4 (low +5.4) |  |  | bid ✓ · undecided · seller holds 2 · also t08 |
| 6 | Team 7 | SAL-02 El Portero | Team 2 | v15 · club | ~8 | +5.3 (low +5.3) |  |  | bid ✓ · gap proven · seller holds 2 · also t12 · spare unverified: 0 seen after its common craft at tick 1819, its SAL page may be complete |
| 7 | Team 2 | MAL-04 El Tatuador | Team 8 | v21 · club | ~4 | +3.1 (low +2.1) |  |  | bid ✓ · undecided · seller holds 2 · spare unverified: 0 seen after its common craft at tick 1404, its MAL page may be complete |
| 8 | Team 16 | RET-04 Paseo de Coches | Team 8 | v10 | ~8 | +2.7 (low +2.7) |  |  | bid ✓ · undecided · seller dumps RET |

## Ready DMs

**1. LAV-02 · Team 16 → Team 9 at ~9 P on v10**
- To Team 16: "Hi Team 16! Could you post your El Frutero de Argumosa (LAV-02) on v10 as an ask addressed to Team 9, at ~9 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! Team 16 can post El Frutero de Argumosa (LAV-02) on v10 as an ask addressed to Team 9, at ~9 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**2. MAL-06 · Team 4 → Team 8 at ~26 P on v10**
- To Team 4: "Hi Team 4! Could you post your Tienda de Discos (MAL-06) on v10 as an ask addressed to Team 8, at ~26 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 8: "Hi Team 8! Team 4 can post Tienda de Discos (MAL-06) on v10 as an ask addressed to Team 8, at ~26 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**3. RET-06 · Team 8 → Team 16 at ~22 P on v10**
- To Team 8: "Hi Team 8! Could you post your La Rosaleda (RET-06) on v10 as an ask addressed to Team 16, at ~22 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 8 can post La Rosaleda (RET-06) on v10 as an ask addressed to Team 16, at ~22 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**4. MAL-02 · Team 16 → Team 8 at ~9 P on v10**
- To Team 16: "Hi Team 16! Could you post your Plaza del Dos de Mayo (MAL-02) on v10 as an ask addressed to Team 8, at ~9 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 8: "Hi Team 8! Team 16 can post Plaza del Dos de Mayo (MAL-02) on v10 as an ask addressed to Team 8, at ~9 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**5. RET-03 · Team 4 → Team 16 at ~8 P on v10**
- To Team 4: "Hi Team 4! Could you post your El Titiritero (RET-03) on v10 as an ask addressed to Team 16, at ~8 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 4 can post El Titiritero (RET-03) on v10 as an ask addressed to Team 16, at ~8 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**6. SAL-02 · Team 2 → Team 7 at ~8 P on v15 (Team 15's market)**
- To Team 2: "Hi Team 2! Could you post your El Portero (SAL-02) on v15 (Team 15's market) as an ask addressed to Team 7, at ~8 P? Only there, please: they're ready to take it on v15. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 7: "Hi Team 7! Team 2 can post El Portero (SAL-02) on v15 (Team 15's market) as an ask addressed to Team 7, at ~8 P: please accept it there, on v15, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**7. MAL-04 · Team 8 → Team 2 at ~4 P on v21 (Team 9's market)**
- To Team 8: "Hi Team 8! Could you post your El Tatuador (MAL-04) on v21 (Team 9's market) as an ask addressed to Team 2, at ~4 P? Only there, please: they're ready to take it on v21. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 2: "Hi Team 2! Team 8 can post El Tatuador (MAL-04) on v21 (Team 9's market) as an ask addressed to Team 2, at ~4 P: please accept it there, on v21, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**8. RET-04 · Team 8 → Team 16 at ~8 P on v10**
- To Team 8: "Hi Team 8! Could you post your Paseo de Coches (RET-04) on v10 as an ask addressed to Team 16, at ~8 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 8 can post Paseo de Coches (RET-04) on v10 as an ask addressed to Team 16, at ~8 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

## Teams one or two cards from a page

- Team 2 CHA 8/10 · missing CHA-09, CHA-10

## Held back (never suggested)

- MAL-02 for Team 8: seller safety: Team 17's MAL page is complete and only 0 copies of it seen after its last common craft (tick 929)
- MAL-02 for Team 8: seller safety: Team 10's MAL page is complete and only 0 copies of it seen after its last common craft (tick 1718)
- SAL-02 for Team 7: seller safety: Team 1's SAL page is complete and only 0 copies of it seen after its last common craft (tick 1333)
- SAL-01 for Team 7: seller safety: Team 1's SAL page is complete and only 0 copies of it seen after its last common craft (tick 1333)
- RET-01 for Team 13: seller safety: Team 2's RET page is complete and only 1 copy of it seen after its last common craft (tick 1819)
- LAV-02 for Team 9: seller safety: Team 14's LAV page is complete and only 0 copies of it seen after its last common craft (tick 1090)
- MAL-04 for Team 2: seller safety: Team 1's MAL page is complete and only 0 copies of it seen after its last common craft (tick 1333)
- MAL-04 for Team 2: seller safety: Team 12's MAL page is complete and only 0 copies of it seen after its last common craft (tick 1114)
- RET-01 for Team 16: seller safety: Team 2's RET page is complete and only 1 copy of it seen after its last common craft (tick 1819)
- RET-01 for Team 16: seller safety: Team 12's RET page is complete and only 1 copy of it seen after its last common craft (tick 1114)

## Holdings (page arithmetic)

| Team | Status | Held | Proven gaps | Undecided |
|---|---|---|---|---|
| Team 1 | exact | 48/48 | 12 | 0 |
| Team 2 | partial | 34/39 | 4 | 22 |
| Team 3 | partial | 33/37 | 10 | 17 |
| Team 4 | partial | 40/41 | 8 | 12 |
| Team 6 | repaired | 40/48 | 11 | 9 |
| Team 7 | exact | 38/38 | 22 | 0 |
| Team 8 | partial | 37/42 | 3 | 20 |
| Team 9 | partial | 32/44 | 8 | 20 |
| Team 10 | exact | 41/41 | 19 | 0 |
| Team 11 | partial | 1/13 | 12 | 47 |
| Team 12 | exact | 44/44 | 16 | 0 |
| Team 13 | exact | 32/32 | 28 | 0 |
| Team 14 | partial | 42/43 | 8 | 10 |
| Team 15 | exact | 44/44 | 16 | 0 |
| Team 16 | partial | 35/36 | 10 | 15 |
| Team 17 | exact | 37/37 | 23 | 0 |
| Team 18 | exact | 47/47 | 13 | 0 |

- run/known_holdings.json entry for Team 5 ignored: the feed shows MAL-10 held.

- run/known_holdings.json entry for Team 15 ignored: the feed shows MAL-09, MAL-10 held.
