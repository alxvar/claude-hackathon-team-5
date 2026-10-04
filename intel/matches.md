# v10 matchmaker: page finishers and first copies

_Written by `tools/matchmaker.py` at 09:58 (tick 1602). Read-only. Holdings: the feed's copies (gifts, eggs and Workshop crafts included) plus the page arithmetic on the leaderboard's album_filled/pages_complete and minted supply (`tools/album.py`; 0 conflicts with intel/holdings-audit.md). ✓ = a proven gap, a bid since Saturday, or a want-list; "undecided" = the buyer may hold it. Giver: a true duplicate or a set it dumps (held back when its page is complete and under two copies are seen after its last craft); receiver: no copy, collects the set; both gain > 0 at the price (conservative multipliers). Want-lists: `intel/wants.md`. Never a page-closer for a rival or a team < 6 below us; a rival on either side gains <= 10 P at our price. Venue: a club deal (both sides in the club) alternates v10 / a member's market (least used, then lowest market score, never either side's own; page-closers on v10); every other deal on v10._

## Matches (best first)

| # | Buyer | Card | Seller | Venue | Price | Value created | Closer | Rival | Why |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Team 9 | RET-09 El Ángel Caído | Team 7 | v10 · club | ~76 | +158.8 (low +158.8) | **page 10/10** |  | page 9/10 · bid ✓ · gap proven · seller holds 2 · also t08 |
| 2 | Team 16 | SAL-12 La Dama de Serrano | Team 12 | v10 | ~322 | +227.5 (low +182.5) |  | rival seller | bid ✓ · seller dumps SAL |
| 3 | Team 1 | MAL-11 La Sala Pentagrama | Team 10 | v10 | ~100 | +72 (low +72) |  | rival seller | bid ✓ · seller dumps MAL |
| 4 | Team 16 | SAL-11 La Puerta de Alcalá | Team 4 | v10 | ~174 | +65.3 (low +47.3) |  |  | bid ✓ · seller dumps SAL |
| 5 | Team 9 | MAL-10 Noche de Movida | Team 10 | v10 | ~45 | +35 (low +28) |  | rival seller | bid ✓ · gap proven · seller dumps MAL |
| 6 | Team 9 | MAL-09 La Heroína del Dos de Mayo | Team 10 | v10 | ~45 | +35 (low +28) |  | rival seller | bid ✓ · undecided · seller dumps MAL |
| 7 | Team 16 | RET-09 El Ángel Caído | Team 8 | v10 | ~68 | +24.5 (low +24.5) |  |  | bid ✓ · gap proven · seller dumps RET · also t07 |
| 8 | Team 9 | LAV-02 El Frutero de Argumosa | Team 16 | v10 | ~9 | +13 (low +11.2) |  |  | bid ✓ · undecided · seller holds 2 · also t04, t15, t18 · spare unverified: 1 seen after its common craft at tick 730 |
| 9 | Team 13 | RET-08 Palacio de Velázquez | Team 7 | v10 | ~21 | +11.8 (low +11.8) |  | rival buyer | bid ✓ · gap proven · seller holds 2 |
| 10 | Team 16 | RET-06 La Rosaleda | Team 8 | v10 | ~24 | +8.7 (low +8.7) |  |  | bid ✓ · gap proven · seller dumps RET |
| 11 | Team 16 | RET-01 Barca del Estanque | Team 2 | v10 | ~9 | +6.8 (low +6.6) |  |  | bid ✓ · gap proven · seller holds 2 · also t09, t12 |
| 12 | Team 7 | SAL-02 El Portero | Team 2 | v15 · club | ~9 | +6.4 (low +6.4) |  |  | bid ✓ · gap proven · seller holds 2 · also t12 · spare unverified: 0 seen after its common craft at tick 1349, its SAL page may be complete |
| 13 | Team 16 | RET-03 El Titiritero | Team 4 | v10 | ~9 | +6.3 (low +6.3) |  |  | bid ✓ · gap proven · seller holds 2 · also t08 |
| 14 | Team 13 | RET-01 Barca del Estanque | Team 9 | v10 | ~8 | +5 (low +5) |  | rival buyer | bid ✓ · gap proven · seller holds 2 · also t02 |
| 15 | Team 16 | RET-04 Paseo de Coches | Team 8 | v10 | ~9 | +3.5 (low +3.5) |  |  | bid ✓ · gap proven · seller dumps RET |
| 16 | Team 13 | RET-03 El Titiritero | Team 8 | v10 | ~8 | +2.1 (low +2.1) |  | rival buyer | bid ✓ · gap proven · seller dumps RET · also t04 |
| 17 | Team 13 | RET-05 La Ardilla | Team 8 | v10 | ~8 | +2.1 (low +2.1) |  | rival buyer | bid ✓ · gap proven · seller dumps RET |
| 18 | Team 7 | SAL-01 Escaparate de Serrano | Team 4 | v10 | ~9 | +1 (low +1) |  |  | bid ✓ · gap proven · seller dumps SAL |

## Ready DMs

**1. RET-09 · Team 7 → Team 9 at ~76 P on v10 (Puesto de Team 5)**
- To Team 7: "Hi Team 7! Could you post your El Ángel Caído (RET-09) on v10 (Puesto de Team 5) as an ask addressed to Team 9, at ~76 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! Team 7 can post El Ángel Caído (RET-09) on v10 (Puesto de Team 5) as an ask addressed to Team 9, at ~76 P: accept it there once it's up. Thanks!"

**2. SAL-12 · Team 12 → Team 16 at ~322 P on v10 (Puesto de Team 5)**
- To Team 12: "Hi Team 12! Could you post your La Dama de Serrano (SAL-12) on v10 (Puesto de Team 5) as an ask addressed to Team 16, at ~322 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 12 can post La Dama de Serrano (SAL-12) on v10 (Puesto de Team 5) as an ask addressed to Team 16, at ~322 P: accept it there once it's up. Thanks!"

**3. MAL-11 · Team 10 → Team 1 at ~100 P on v10 (Puesto de Team 5)**
- To Team 10: "Hi Team 10! Could you post your La Sala Pentagrama (MAL-11) on v10 (Puesto de Team 5) as an ask addressed to Team 1, at ~100 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 1: "Hi Team 1! Team 10 can post La Sala Pentagrama (MAL-11) on v10 (Puesto de Team 5) as an ask addressed to Team 1, at ~100 P: accept it there once it's up. Thanks!"

**4. SAL-11 · Team 4 → Team 16 at ~174 P on v10 (Puesto de Team 5)**
- To Team 4: "Hi Team 4! Could you post your La Puerta de Alcalá (SAL-11) on v10 (Puesto de Team 5) as an ask addressed to Team 16, at ~174 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 4 can post La Puerta de Alcalá (SAL-11) on v10 (Puesto de Team 5) as an ask addressed to Team 16, at ~174 P: accept it there once it's up. Thanks!"

**5. MAL-10 · Team 10 → Team 9 at ~45 P on v10 (Puesto de Team 5)**
- To Team 10: "Hi Team 10! Could you post your Noche de Movida (MAL-10) on v10 (Puesto de Team 5) as an ask addressed to Team 9, at ~45 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! Team 10 can post Noche de Movida (MAL-10) on v10 (Puesto de Team 5) as an ask addressed to Team 9, at ~45 P: accept it there once it's up. Thanks!"

**6. MAL-09 · Team 10 → Team 9 at ~45 P on v10 (Puesto de Team 5)**
- To Team 10: "Hi Team 10! Could you post your La Heroína del Dos de Mayo (MAL-09) on v10 (Puesto de Team 5) as an ask addressed to Team 9, at ~45 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! Team 10 can post La Heroína del Dos de Mayo (MAL-09) on v10 (Puesto de Team 5) as an ask addressed to Team 9, at ~45 P: accept it there once it's up. Thanks!"

**7. RET-09 · Team 8 → Team 16 at ~68 P on v10 (Puesto de Team 5)**
- To Team 8: "Hi Team 8! Could you post your El Ángel Caído (RET-09) on v10 (Puesto de Team 5) as an ask addressed to Team 16, at ~68 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 8 can post El Ángel Caído (RET-09) on v10 (Puesto de Team 5) as an ask addressed to Team 16, at ~68 P: accept it there once it's up. Thanks!"

**8. LAV-02 · Team 16 → Team 9 at ~9 P on v10 (Puesto de Team 5)**
- To Team 16: "Hi Team 16! Could you post your El Frutero de Argumosa (LAV-02) on v10 (Puesto de Team 5) as an ask addressed to Team 9, at ~9 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! Team 16 can post El Frutero de Argumosa (LAV-02) on v10 (Puesto de Team 5) as an ask addressed to Team 9, at ~9 P: accept it there once it's up. Thanks!"

## Teams one or two cards from a page

- Team 15 LAV 9/10 · missing LAV-05 · **may be complete** (server: 4 complete pages, feed sees 2)
- Team 12 LAV 9/10 · missing LAV-07 (undecided) · rival · **may be complete**
- Team 12 LAT 9/10 · missing LAT-08 (undecided) · rival · **may be complete**
- Team 9 RET 9/10 · missing RET-09
- Team 15 LAT 8/10 · missing LAT-04, LAT-09 · **may be complete** (server: 4 complete pages, feed sees 2)

## Held back (never suggested)

- SAL-02 for Team 7: seller safety: Team 1's SAL page is complete and only 0 copies of it seen after its last common craft (tick 1333)
- SAL-01 for Team 7: seller safety: Team 1's SAL page is complete and only 0 copies of it seen after its last common craft (tick 1333)
- LAV-02 for Team 9: seller safety: Team 14's LAV page is complete and only 0 copies of it seen after its last common craft (tick 1090)
- MAL-04 for Team 2: seller safety: Team 1's MAL page is complete and only 0 copies of it seen after its last common craft (tick 1333)
- MAL-04 for Team 2: seller safety: Team 8's MAL page is complete and only 0 copies of it seen after its last common craft (tick 1404)

## Holdings (page arithmetic)

| Team | Status | Held | Proven gaps | Undecided |
|---|---|---|---|---|
| Team 1 | exact | 41/41 | 19 | 0 |
| Team 2 | partial | 33/38 | 5 | 22 |
| Team 3 | partial | 32/36 | 11 | 17 |
| Team 4 | partial | 39/41 | 9 | 12 |
| Team 6 | repaired | 40/50 | 9 | 11 |
| Team 7 | exact | 37/37 | 23 | 0 |
| Team 8 | exact | 38/38 | 22 | 0 |
| Team 9 | partial | 31/43 | 10 | 19 |
| Team 10 | partial | 31/39 | 9 | 20 |
| Team 11 | partial | 1/13 | 13 | 46 |
| Team 12 | partial | 35/43 | 8 | 17 |
| Team 13 | exact | 32/32 | 28 | 0 |
| Team 14 | exact | 42/42 | 18 | 0 |
| Team 15 | inconsistent | 0/42 | 0 | 0 |
| Team 16 | exact | 34/34 | 26 | 0 |
| Team 17 | exact | 37/37 | 23 | 0 |
| Team 18 | exact | 48/48 | 12 | 0 |

- run/known_holdings.json entry for Team 15 ignored: the feed shows MAL-09, MAL-10 held.
