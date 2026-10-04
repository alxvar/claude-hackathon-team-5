# v10 matchmaker: page finishers and first copies

_Written by `tools/matchmaker.py` at 12:14 (tick 2142). Read-only. Holdings: the feed's copies (gifts, eggs and Workshop crafts included) plus the page arithmetic on the leaderboard's album_filled/pages_complete and minted supply (`tools/album.py`; 0 conflicts with intel/holdings-audit.md). ✓ = a proven gap, a bid since Saturday, or a want-list; "undecided" = the buyer may hold it. Giver: a true duplicate or a set it dumps (held back when its page is complete and under two copies are seen after its last craft); receiver: no copy, collects the set; both gain > 0 at the price (conservative multipliers). Want-lists: `intel/wants.md`. Never a page-closer for a rival or a team < 6 below us; a rival on either side gains <= 10 P at our price. Venue: a club deal (both sides in the club) alternates v10 / a member's market (least used, then lowest market score, never either side's own; page-closers on v10); every other deal on v10._

## Matches (best first)

| # | Buyer | Card | Seller | Venue | Price | Value created | Closer | Rival | Why |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Team 3 | SAL-11 La Puerta de Alcalá | Team 2 | v10 | ~259 | +45.9 (low +45.9) |  | rival buyer | bid ✓ · seller dumps SAL |
| 2 | Team 4 | LAV-06 La Tabacalera | Team 16 | v10 | ~24 | +15 (low +10) |  | rival buyer | page 8/10 ✓ · gap proven · seller dumps LAV |
| 3 | Team 8 | MAL-06 Tienda de Discos | Team 7 | v10 · club | ~26 | +13.2 (low +13.2) |  |  | bid · **ask first** · seller dumps MAL · ask first: t08 sold a MAL-06 at tick 510, it may keep another |
| 4 | Team 9 | LAV-02 El Frutero de Argumosa | Team 16 | v10 | ~9 | +13 (low +11.2) |  |  | bid · **ask first** · seller holds 2 · also t04, t18 · spare unverified: 1 seen after its common craft at tick 730; ask first: t09 sold a LAV-02 at tick 369, it may keep another |
| 5 | Team 4 | LAV-05 Bici de Reparto | Team 8 | v10 | ~9 | +10.5 (low +9.5) |  | rival buyer | page 8/10 ✓ · gap proven · seller holds 2 · also t16 · spare unverified: 1 seen after its common craft at tick 1404 |
| 6 | Team 16 | RET-01 Barca del Estanque | Team 1 | v10 | ~8 | +7.1 (low +7.1) |  |  | bid ✓ · undecided · seller holds 2 · also t08 · spare unverified: 1 seen after its common craft at tick 1333 |
| 7 | Team 8 | MAL-02 Plaza del Dos de Mayo | Team 6 | v10 | ~9 | +6.3 (low +6.3) |  |  | bid · **ask first** · seller dumps MAL · also t16, t14, t03 · ask first: t08 sold a MAL-02 at tick 171, it may keep another |
| 8 | Team 16 | RET-06 La Rosaleda | Team 8 | v10 | ~22 | +5.4 (low +5.4) |  |  | bid · **ask first** · seller dumps RET · ask first: t16 sold a RET-06 at tick 1011, it may keep another |
| 9 | Team 3 | LAT-05 El Organillero | Team 2 | v10 | ~8 | +5 (low +4) |  | rival buyer | bid ✓ · undecided · seller dumps LAT · also t09, t06 |
| 10 | Team 1 | RET-03 El Titiritero | Team 4 | v10 | ~7 | +4 (low +4) |  | rival seller | bid ✓ · gap proven · seller holds 2 |
| 11 | Team 2 | MAL-04 El Tatuador | Team 8 | v21 · club | ~4 | +3.1 (low +2.1) |  |  | bid ✓ · undecided · seller holds 2 · spare unverified: 0 seen after its common craft at tick 1404, its MAL page may be complete |
| 12 | Team 16 | RET-03 El Titiritero | Team 8 | v10 | ~8 | +2.1 (low +2.1) |  |  | bid ✓ · undecided · seller dumps RET · also t04 |
| 13 | Team 16 | RET-04 Paseo de Coches | Team 8 | v10 | ~8 | +2.1 (low +2.1) |  |  | bid ✓ · undecided · seller dumps RET · also t18 |
| 14 | Team 13 | RET-01 Barca del Estanque | Team 8 | v10 | ~8 | +1.3 (low +1.3) |  | rival buyer | bid ✓ · gap proven · seller dumps RET · also t01 |
| 15 | Team 13 | RET-05 La Ardilla | Team 8 | v10 | ~8 | +1.3 (low +1.3) |  | rival buyer | bid ✓ · gap proven · seller dumps RET |

## Ready DMs

**1. SAL-11 · Team 2 → Team 3 at ~259 P on v10**
- To Team 2: "Hi Team 2! Could you post your La Puerta de Alcalá (SAL-11) on v10 as an ask addressed to Team 3, at ~259 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 3: "Hi Team 3! Team 2 can post La Puerta de Alcalá (SAL-11) on v10 as an ask addressed to Team 3, at ~259 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**2. LAV-06 · Team 16 → Team 4 at ~24 P on v10**
- To Team 16: "Hi Team 16! Could you post your La Tabacalera (LAV-06) on v10 as an ask addressed to Team 4, at ~24 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 4: "Hi Team 4! Team 16 can post La Tabacalera (LAV-06) on v10 as an ask addressed to Team 4, at ~24 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**3. MAL-06 · Team 7 → Team 8 at ~26 P on v10**
- To Team 7: "Hi Team 7! Could you post your Tienda de Discos (MAL-06) on v10 as an ask addressed to Team 8, at ~26 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 8: "Hi Team 8! Team 7 can post Tienda de Discos (MAL-06) on v10 as an ask addressed to Team 8, at ~26 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**4. LAV-02 · Team 16 → Team 9 at ~9 P on v10**
- To Team 16: "Hi Team 16! Could you post your El Frutero de Argumosa (LAV-02) on v10 as an ask addressed to Team 9, at ~9 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! Team 16 can post El Frutero de Argumosa (LAV-02) on v10 as an ask addressed to Team 9, at ~9 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**5. LAV-05 · Team 8 → Team 4 at ~9 P on v10**
- To Team 8: "Hi Team 8! Could you post your Bici de Reparto (LAV-05) on v10 as an ask addressed to Team 4, at ~9 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 4: "Hi Team 4! Team 8 can post Bici de Reparto (LAV-05) on v10 as an ask addressed to Team 4, at ~9 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**6. RET-01 · Team 1 → Team 16 at ~8 P on v10**
- To Team 1: "Hi Team 1! Could you post your Barca del Estanque (RET-01) on v10 as an ask addressed to Team 16, at ~8 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 1 can post Barca del Estanque (RET-01) on v10 as an ask addressed to Team 16, at ~8 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**7. MAL-02 · Team 6 → Team 8 at ~9 P on v10**
- To Team 6: "Hi Team 6! Could you post your Plaza del Dos de Mayo (MAL-02) on v10 as an ask addressed to Team 8, at ~9 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 8: "Hi Team 8! Team 6 can post Plaza del Dos de Mayo (MAL-02) on v10 as an ask addressed to Team 8, at ~9 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

**8. RET-06 · Team 8 → Team 16 at ~22 P on v10**
- To Team 8: "Hi Team 8! Could you post your La Rosaleda (RET-06) on v10 as an ask addressed to Team 16, at ~22 P? Only there, please: they're ready to take it on v10. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 8 can post La Rosaleda (RET-06) on v10 as an ask addressed to Team 16, at ~22 P: please accept it there, on v10, once it's up, and don't bid for it elsewhere meanwhile. Thanks!"

## Teams one or two cards from a page

- Team 4 LAV 8/10 · missing LAV-05, LAV-06 · rival

## Held back (never suggested)

- LAV-06 for Team 4: seller safety: Team 1's LAV page is complete and only 0 copies of it seen after its last uncommon craft (tick 1361)
- MAL-02 for Team 8: seller safety: Team 17's MAL page is complete and only 0 copies of it seen after its last common craft (tick 929)
- MAL-02 for Team 8: seller safety: Team 10's MAL page is complete and only 0 copies of it seen after its last common craft (tick 1718)
- MAL-04 for Team 2: seller safety: Team 1's MAL page is complete and only 0 copies of it seen after its last common craft (tick 1333)
- MAL-04 for Team 2: seller safety: Team 12's MAL page is complete and only 0 copies of it seen after its last common craft (tick 1114)
- RET-01 for Team 16: seller safety: Team 18's RET page is complete and only 1 copy of it seen after its last common craft (tick 723)
- RET-01 for Team 16: seller safety: Team 12's RET page is complete and only 1 copy of it seen after its last common craft (tick 1114)

## Holdings (page arithmetic)

| Team | Status | Held | Proven gaps | Undecided |
|---|---|---|---|---|
| Team 1 | exact | 47/47 | 13 | 0 |
| Team 2 | partial | 36/41 | 2 | 22 |
| Team 3 | partial | 32/38 | 8 | 20 |
| Team 4 | exact | 41/41 | 19 | 0 |
| Team 6 | repaired | 40/48 | 11 | 9 |
| Team 7 | repaired | 30/43 | 16 | 14 |
| Team 8 | partial | 38/43 | 3 | 19 |
| Team 9 | partial | 42/46 | 10 | 8 |
| Team 10 | exact | 41/41 | 19 | 0 |
| Team 11 | partial | 1/13 | 12 | 47 |
| Team 12 | repaired | 40/44 | 15 | 5 |
| Team 13 | repaired | 30/32 | 27 | 3 |
| Team 14 | partial | 42/43 | 8 | 10 |
| Team 15 | exact | 43/43 | 17 | 0 |
| Team 16 | partial | 37/38 | 8 | 15 |
| Team 17 | exact | 38/38 | 22 | 0 |
| Team 18 | exact | 47/47 | 13 | 0 |

- run/known_holdings.json entry for Team 5 ignored: the feed shows MAL-10 held.

- run/known_holdings.json entry for Team 15 ignored: the feed shows MAL-09, MAL-10 held.
