# v10 matchmaker: page finishers and first copies

_Written by `tools/matchmaker.py` at 10:49 (tick 1822). Read-only. Holdings: the feed's copies (gifts, eggs and Workshop crafts included) plus the page arithmetic on the leaderboard's album_filled/pages_complete and minted supply (`tools/album.py`; 0 conflicts with intel/holdings-audit.md). ✓ = a proven gap, a bid since Saturday, or a want-list; "undecided" = the buyer may hold it. Giver: a true duplicate or a set it dumps (held back when its page is complete and under two copies are seen after its last craft); receiver: no copy, collects the set; both gain > 0 at the price (conservative multipliers). Want-lists: `intel/wants.md`. Never a page-closer for a rival or a team < 6 below us; a rival on either side gains <= 10 P at our price. Venue: a club deal (both sides in the club) alternates v10 / a member's market (least used, then lowest market score, never either side's own; page-closers on v10); every other deal on v10._

## Matches (best first)

| # | Buyer | Card | Seller | Venue | Price | Value created | Closer | Rival | Why |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Team 6 | SAL-12 La Dama de Serrano | Team 12 | v10 | ~322 | +340.3 (low +272.8) |  | rival seller | bid ✓ · seller dumps SAL |
| 2 | Team 6 | SAL-11 La Puerta de Alcalá | Team 4 | v10 | ~193 | +108.3 (low +81.3) |  |  | bid ✓ · seller dumps SAL |
| 3 | Team 13 | RET-07 Fuente de la Alcachofa | Team 2 | v10 | ~21 | +13.6 (low +12.9) |  | rival buyer | bid ✓ · gap proven · seller holds 2 |
| 4 | Team 9 | LAV-02 El Frutero de Argumosa | Team 16 | v10 | ~9 | +13 (low +11.2) |  |  | bid ✓ · undecided · seller holds 2 · also t04, t18 · spare unverified: 1 seen after its common craft at tick 730 |
| 5 | Team 13 | RET-08 Palacio de Velázquez | Team 7 | v10 | ~21 | +11.7 (low +11.7) |  | rival buyer | bid ✓ · gap proven · seller holds 2 |
| 6 | Team 8 | MAL-06 Tienda de Discos | Team 4 | v10 · club | ~26 | +10.1 (low +10.1) |  |  | bid ✓ · undecided · seller dumps MAL |
| 7 | Team 16 | RET-06 La Rosaleda | Team 8 | v10 | ~22 | +6.7 (low +6.7) |  |  | bid ✓ · undecided · seller dumps RET |
| 8 | Team 8 | MAL-02 Plaza del Dos de Mayo | Team 16 | v10 | ~9 | +6.3 (low +6.3) |  |  | bid ✓ · undecided · seller dumps MAL · also t06, t14, t04 |
| 9 | Team 7 | SAL-02 El Portero | Team 2 | v15 · club | ~9 | +6.2 (low +6.2) |  |  | bid ✓ · gap proven · seller holds 2 · also t12 · spare unverified: 0 seen after its common craft at tick 1819, its SAL page may be complete |
| 10 | Team 16 | RET-03 El Titiritero | Team 4 | v10 | ~8 | +5.4 (low +5.4) |  |  | bid ✓ · undecided · seller holds 2 · also t08 |
| 11 | Team 2 | MAL-04 El Tatuador | Team 8 | v21 · club | ~4 | +3.1 (low +2.1) |  |  | bid ✓ · undecided · seller holds 2 · spare unverified: 0 seen after its common craft at tick 1404, its MAL page may be complete |
| 12 | Team 16 | RET-04 Paseo de Coches | Team 8 | v10 | ~8 | +2.7 (low +2.7) |  |  | bid ✓ · undecided · seller dumps RET |
| 13 | Team 13 | RET-03 El Titiritero | Team 8 | v10 | ~8 | +2.1 (low +2.1) |  | rival buyer | bid ✓ · gap proven · seller dumps RET · also t04 |
| 14 | Team 13 | RET-05 La Ardilla | Team 8 | v10 | ~8 | +2.1 (low +2.1) |  | rival buyer | bid ✓ · gap proven · seller dumps RET |
| 15 | Team 7 | SAL-01 Escaparate de Serrano | Team 4 | v10 | ~9 | +0.7 (low +0.7) |  |  | bid ✓ · gap proven · seller dumps SAL |

## Ready DMs

**1. SAL-12 · Team 12 → Team 6 at ~322 P on v10**
- To Team 12: "Hi Team 12! Could you post your La Dama de Serrano (SAL-12) on v10 as an ask addressed to Team 6, at ~322 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 6: "Hi Team 6! Team 12 can post La Dama de Serrano (SAL-12) on v10 as an ask addressed to Team 6, at ~322 P: accept it there once it's up. Thanks!"

**2. SAL-11 · Team 4 → Team 6 at ~193 P on v10**
- To Team 4: "Hi Team 4! Could you post your La Puerta de Alcalá (SAL-11) on v10 as an ask addressed to Team 6, at ~193 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 6: "Hi Team 6! Team 4 can post La Puerta de Alcalá (SAL-11) on v10 as an ask addressed to Team 6, at ~193 P: accept it there once it's up. Thanks!"

**3. RET-07 · Team 2 → Team 13 at ~21 P on v10**
- To Team 2: "Hi Team 2! Could you post your Fuente de la Alcachofa (RET-07) on v10 as an ask addressed to Team 13, at ~21 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 13: "Hi Team 13! Team 2 can post Fuente de la Alcachofa (RET-07) on v10 as an ask addressed to Team 13, at ~21 P: accept it there once it's up. Thanks!"

**4. LAV-02 · Team 16 → Team 9 at ~9 P on v10**
- To Team 16: "Hi Team 16! Could you post your El Frutero de Argumosa (LAV-02) on v10 as an ask addressed to Team 9, at ~9 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! Team 16 can post El Frutero de Argumosa (LAV-02) on v10 as an ask addressed to Team 9, at ~9 P: accept it there once it's up. Thanks!"

**5. RET-08 · Team 7 → Team 13 at ~21 P on v10**
- To Team 7: "Hi Team 7! Could you post your Palacio de Velázquez (RET-08) on v10 as an ask addressed to Team 13, at ~21 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 13: "Hi Team 13! Team 7 can post Palacio de Velázquez (RET-08) on v10 as an ask addressed to Team 13, at ~21 P: accept it there once it's up. Thanks!"

**6. MAL-06 · Team 4 → Team 8 at ~26 P on v10**
- To Team 4: "Hi Team 4! Could you post your Tienda de Discos (MAL-06) on v10 as an ask addressed to Team 8, at ~26 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 8: "Hi Team 8! Team 4 can post Tienda de Discos (MAL-06) on v10 as an ask addressed to Team 8, at ~26 P: accept it there once it's up. Thanks!"

**7. RET-06 · Team 8 → Team 16 at ~22 P on v10**
- To Team 8: "Hi Team 8! Could you post your La Rosaleda (RET-06) on v10 as an ask addressed to Team 16, at ~22 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 8 can post La Rosaleda (RET-06) on v10 as an ask addressed to Team 16, at ~22 P: accept it there once it's up. Thanks!"

**8. MAL-02 · Team 16 → Team 8 at ~9 P on v10**
- To Team 16: "Hi Team 16! Could you post your Plaza del Dos de Mayo (MAL-02) on v10 as an ask addressed to Team 8, at ~9 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 8: "Hi Team 8! Team 16 can post Plaza del Dos de Mayo (MAL-02) on v10 as an ask addressed to Team 8, at ~9 P: accept it there once it's up. Thanks!"

## Teams one or two cards from a page

- Team 2 CHA 8/10 · missing CHA-09, CHA-10

## Held back (never suggested)

- MAL-02 for Team 8: seller safety: Team 17's MAL page is complete and only 0 copies of it seen after its last common craft (tick 929)
- MAL-02 for Team 8: seller safety: Team 10's MAL page is complete and only 0 copies of it seen after its last common craft (tick 1718)
- SAL-02 for Team 7: seller safety: Team 1's SAL page is complete and only 0 copies of it seen after its last common craft (tick 1333)
- SAL-01 for Team 7: seller safety: Team 1's SAL page is complete and only 0 copies of it seen after its last common craft (tick 1333)
- RET-01 for Team 13: seller safety: Team 2's RET page is complete and only 0 copies of it seen after its last common craft (tick 1819)
- LAV-02 for Team 9: seller safety: Team 14's LAV page is complete and only 0 copies of it seen after its last common craft (tick 1090)
- MAL-04 for Team 2: seller safety: Team 1's MAL page is complete and only 0 copies of it seen after its last common craft (tick 1333)
- MAL-04 for Team 2: seller safety: Team 12's MAL page is complete and only 0 copies of it seen after its last common craft (tick 1114)
- RET-01 for Team 16: seller safety: Team 2's RET page is complete and only 0 copies of it seen after its last common craft (tick 1819)
- RET-01 for Team 16: seller safety: Team 12's RET page is complete and only 1 copy of it seen after its last common craft (tick 1114)

## Holdings (page arithmetic)

| Team | Status | Held | Proven gaps | Undecided |
|---|---|---|---|---|
| Team 1 | exact | 43/43 | 17 | 0 |
| Team 2 | partial | 34/39 | 4 | 22 |
| Team 3 | partial | 33/37 | 11 | 16 |
| Team 4 | partial | 40/41 | 9 | 11 |
| Team 6 | repaired | 40/50 | 9 | 11 |
| Team 7 | exact | 35/35 | 25 | 0 |
| Team 8 | partial | 37/42 | 3 | 20 |
| Team 9 | partial | 32/44 | 9 | 19 |
| Team 10 | exact | 42/42 | 18 | 0 |
| Team 11 | partial | 1/13 | 13 | 46 |
| Team 12 | exact | 44/44 | 16 | 0 |
| Team 13 | exact | 32/32 | 28 | 0 |
| Team 14 | exact | 42/42 | 18 | 0 |
| Team 15 | exact | 44/44 | 16 | 0 |
| Team 16 | partial | 35/36 | 11 | 14 |
| Team 17 | exact | 37/37 | 23 | 0 |
| Team 18 | exact | 47/47 | 13 | 0 |

- run/known_holdings.json entry for Team 5 ignored: the feed shows MAL-10 held.

- run/known_holdings.json entry for Team 15 ignored: the feed shows MAL-09, MAL-10 held.
