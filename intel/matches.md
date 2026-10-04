# v10 matchmaker: page finishers and first copies

_Written by `tools/matchmaker.py` at 07:44 (tick 1440). Read-only. Holdings: the feed's copies (gifts, eggs and Workshop crafts included) plus the page arithmetic on the leaderboard's album_filled/pages_complete and minted supply (`tools/album.py`; 0 conflicts with intel/holdings-audit.md). ✓ = a proven gap, a bid since Saturday, or a want-list; "undecided" = the buyer may hold it. Giver: a true duplicate or a set it dumps (held back when its page is complete and under two copies are seen after its last craft); receiver: no copy, collects the set; both gain > 0 at the price (conservative multipliers). Want-lists: `intel/wants.md`. Never a page-closer for a rival or a team < 6 below us; a rival on either side gains <= 10 P at our price._

## Matches (best first)

| # | Buyer | Card | Seller | Price | Value created | Closer | Rival | Why |
|---|---|---|---|---|---|---|---|---|
| 1 | Team 9 | RET-09 El Ángel Caído | Team 7 | ~76 | +156.2 (low +156.2) | **page 10/10** |  | page 9/10 · bid ✓ · gap proven · seller holds 2 · also t08 |
| 2 | Team 1 | MAL-11 La Sala Pentagrama | Team 10 | ~100 | +72 (low +72) |  | rival seller | bid ✓ · seller dumps MAL |
| 3 | Team 9 | MAL-10 Noche de Movida | Team 10 | ~45 | +35 (low +28) |  | rival seller | bid ✓ · gap proven · seller dumps MAL |
| 4 | Team 9 | MAL-09 La Heroína del Dos de Mayo | Team 10 | ~45 | +35 (low +28) |  | rival seller | bid ✓ · undecided · seller dumps MAL |
| 5 | Team 16 | RET-09 El Ángel Caído | Team 8 | ~70 | +23.7 (low +23.7) |  |  | bid ✓ · gap proven · seller dumps RET · also t07 |
| 6 | Team 13 | RET-08 Palacio de Velázquez | Team 7 | ~22 | +13.4 (low +13.4) |  | rival buyer | bid ✓ · gap proven · seller holds 2 |
| 7 | Team 9 | LAV-02 El Frutero de Argumosa | Team 16 | ~9 | +13 (low +11.2) |  |  | bid ✓ · undecided · seller holds 2 · also t04, t18 · spare unverified: 1 seen after its common craft at tick 730 |
| 8 | Team 3 | LAT-05 El Organillero | Team 2 | ~8 | +8.8 (low +7.8) |  | rival buyer | bid ✓ · undecided · seller holds 2 · also t09 · spare unverified: 1 seen after its common craft at tick 1349 |
| 9 | Team 16 | RET-06 La Rosaleda | Team 8 | ~24 | +8.5 (low +8.5) |  |  | bid ✓ · gap proven · seller dumps RET |
| 10 | Team 16 | RET-01 Barca del Estanque | Team 2 | ~9 | +7.7 (low +7.4) |  |  | bid ✓ · gap proven · seller holds 2 · also t09 |
| 11 | Team 8 | MAL-02 Plaza del Dos de Mayo | Team 7 | ~9 | +7.2 (low +7.2) |  |  | bid ✓ · undecided · seller dumps MAL · also t16, t04, t10 |
| 12 | Team 16 | RET-03 El Titiritero | Team 4 | ~9 | +7.1 (low +7.1) |  |  | bid ✓ · gap proven · seller holds 2 · also t08 |
| 13 | Team 7 | SAL-02 El Portero | Team 9 | ~9 | +6.5 (low +6.5) |  |  | bid ✓ · gap proven · seller holds 2 · also t02, t12 |
| 14 | Team 13 | RET-01 Barca del Estanque | Team 9 | ~9 | +5.7 (low +5.7) |  | rival buyer | bid ✓ · gap proven · seller holds 2 · also t02 |
| 15 | Team 16 | RET-04 Paseo de Coches | Team 8 | ~9 | +3.4 (low +3.4) |  |  | bid ✓ · gap proven · seller dumps RET |
| 16 | Team 1 | RET-03 El Titiritero | Team 8 | ~9 | +1.9 (low +1.9) |  |  | bid ✓ · gap proven · seller dumps RET · also t04 |
| 17 | Team 1 | RET-05 La Ardilla | Team 8 | ~9 | +1.9 (low +1.9) |  |  | bid ✓ · gap proven · seller dumps RET |
| 18 | Team 7 | SAL-01 Escaparate de Serrano | Team 4 | ~9 | +1.2 (low +1.2) |  |  | bid ✓ · gap proven · seller dumps SAL |

## Ready DMs

**1. RET-09 · Team 7 → Team 9 at ~76 P**
- To Team 7: "Hi Team 7! Could you post your El Ángel Caído (RET-09) on v10 as an ask addressed to Team 9, at ~76 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! Team 7 can post El Ángel Caído (RET-09) on v10 as an ask addressed to Team 9, at ~76 P: accept it there once it's up. Thanks!"

**2. MAL-11 · Team 10 → Team 1 at ~100 P**
- To Team 10: "Hi Team 10! Could you post your La Sala Pentagrama (MAL-11) on v10 as an ask addressed to Team 1, at ~100 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 1: "Hi Team 1! Team 10 can post La Sala Pentagrama (MAL-11) on v10 as an ask addressed to Team 1, at ~100 P: accept it there once it's up. Thanks!"

**3. MAL-10 · Team 10 → Team 9 at ~45 P**
- To Team 10: "Hi Team 10! Could you post your Noche de Movida (MAL-10) on v10 as an ask addressed to Team 9, at ~45 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! Team 10 can post Noche de Movida (MAL-10) on v10 as an ask addressed to Team 9, at ~45 P: accept it there once it's up. Thanks!"

**4. MAL-09 · Team 10 → Team 9 at ~45 P**
- To Team 10: "Hi Team 10! Could you post your La Heroína del Dos de Mayo (MAL-09) on v10 as an ask addressed to Team 9, at ~45 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! Team 10 can post La Heroína del Dos de Mayo (MAL-09) on v10 as an ask addressed to Team 9, at ~45 P: accept it there once it's up. Thanks!"

**5. RET-09 · Team 8 → Team 16 at ~70 P**
- To Team 8: "Hi Team 8! Could you post your El Ángel Caído (RET-09) on v10 as an ask addressed to Team 16, at ~70 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 8 can post El Ángel Caído (RET-09) on v10 as an ask addressed to Team 16, at ~70 P: accept it there once it's up. Thanks!"

**6. RET-08 · Team 7 → Team 13 at ~22 P**
- To Team 7: "Hi Team 7! Could you post your Palacio de Velázquez (RET-08) on v10 as an ask addressed to Team 13, at ~22 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 13: "Hi Team 13! Team 7 can post Palacio de Velázquez (RET-08) on v10 as an ask addressed to Team 13, at ~22 P: accept it there once it's up. Thanks!"

**7. LAV-02 · Team 16 → Team 9 at ~9 P**
- To Team 16: "Hi Team 16! Could you post your El Frutero de Argumosa (LAV-02) on v10 as an ask addressed to Team 9, at ~9 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! Team 16 can post El Frutero de Argumosa (LAV-02) on v10 as an ask addressed to Team 9, at ~9 P: accept it there once it's up. Thanks!"

**8. LAT-05 · Team 2 → Team 3 at ~8 P**
- To Team 2: "Hi Team 2! Could you post your El Organillero (LAT-05) on v10 as an ask addressed to Team 3, at ~8 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 3: "Hi Team 3! Team 2 can post El Organillero (LAT-05) on v10 as an ask addressed to Team 3, at ~8 P: accept it there once it's up. Thanks!"

## Teams one or two cards from a page

- Team 9 RET 9/10 · missing RET-09
- Team 3 SAL 8/10 · missing SAL-03 (undecided), SAL-10 (undecided) · rival · **may be complete**
- Team 3 LAV 8/10 · missing LAV-02 (undecided), LAV-04 (undecided) · rival · **may be complete**

## Held back (never suggested)

- MAL-02 for Team 8: seller safety: Team 17's MAL page is complete and only 0 copies of it seen after its last common craft (tick 929)
- SAL-02 for Team 7: seller safety: Team 1's SAL page is complete and only 0 copies of it seen after its last common craft (tick 1333)
- SAL-01 for Team 7: seller safety: Team 1's SAL page is complete and only 0 copies of it seen after its last common craft (tick 1333)
- LAV-02 for Team 9: seller safety: Team 14's LAV page is complete and only 0 copies of it seen after its last common craft (tick 1090)
- MAL-04 for Team 2: seller safety: Team 1's MAL page is complete and only 0 copies of it seen after its last common craft (tick 1333)
- MAL-04 for Team 2: seller safety: Team 12's MAL page is complete and only 0 copies of it seen after its last common craft (tick 1114)

## Holdings (page arithmetic)

| Team | Status | Held | Proven gaps | Undecided |
|---|---|---|---|---|
| Team 1 | exact | 37/37 | 13 | 0 |
| Team 2 | partial | 26/31 | 2 | 22 |
| Team 3 | partial | 23/30 | 3 | 24 |
| Team 4 | partial | 39/40 | 1 | 10 |
| Team 6 | repaired | 30/40 | 9 | 11 |
| Team 7 | exact | 37/37 | 13 | 0 |
| Team 8 | partial | 28/33 | 2 | 20 |
| Team 9 | partial | 29/41 | 2 | 19 |
| Team 10 | partial | 32/37 | 8 | 10 |
| Team 11 | partial | 1/13 | 5 | 44 |
| Team 12 | exact | 40/40 | 10 | 0 |
| Team 13 | exact | 32/32 | 18 | 0 |
| Team 14 | repaired | 40/41 | 8 | 2 |
| Team 15 | exact | 42/42 | 8 | 0 |
| Team 16 | exact | 34/34 | 16 | 0 |
| Team 17 | exact | 37/37 | 13 | 0 |
| Team 18 | exact | 37/37 | 13 | 0 |

- run/known_holdings.json entry for Team 15 ignored: the feed shows MAL-09, MAL-10 held.
