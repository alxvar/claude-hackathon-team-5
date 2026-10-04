# v10 matchmaker: page finishers and first copies

_Written by `tools/matchmaker.py` at 09:33 (tick 1502). Read-only. Holdings: the feed's copies (gifts, eggs and Workshop crafts included) plus the page arithmetic on the leaderboard's album_filled/pages_complete and minted supply (`tools/album.py`; 0 conflicts with intel/holdings-audit.md). ✓ = a proven gap, a bid since Saturday, or a want-list; "undecided" = the buyer may hold it. Giver: a true duplicate or a set it dumps (held back when its page is complete and under two copies are seen after its last craft); receiver: no copy, collects the set; both gain > 0 at the price (conservative multipliers). Want-lists: `intel/wants.md`. Never a page-closer for a rival or a team < 6 below us; a rival on either side gains <= 10 P at our price. Venue: a club deal (both sides in the club) alternates v10 / a member's market (least used, then lowest market score, never either side's own; page-closers on v10); every other deal on v10._

## Matches (best first)

| # | Buyer | Card | Seller | Venue | Price | Value created | Closer | Rival | Why |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Team 9 | RET-09 El Ángel Caído | Team 7 | v10 · club | ~76 | +155.1 (low +155.1) | **page 10/10** |  | page 9/10 · bid ✓ · gap proven · seller holds 2 · also t08 |
| 2 | Team 1 | MAL-11 La Sala Pentagrama | Team 10 | v10 | ~100 | +72 (low +72) |  | rival seller | bid ✓ · seller dumps MAL |
| 3 | Team 9 | MAL-10 Noche de Movida | Team 10 | v10 | ~45 | +35 (low +28) |  | rival seller | bid ✓ · gap proven · seller dumps MAL |
| 4 | Team 9 | MAL-09 La Heroína del Dos de Mayo | Team 10 | v10 | ~45 | +35 (low +28) |  | rival seller | bid ✓ · undecided · seller dumps MAL |
| 5 | Team 16 | RET-09 El Ángel Caído | Team 8 | v10 | ~70 | +24 (low +24) |  |  | bid ✓ · gap proven · seller dumps RET · also t07 |
| 6 | Team 9 | LAV-02 El Frutero de Argumosa | Team 16 | v10 | ~9 | +13 (low +11.2) |  |  | bid ✓ · undecided · seller holds 2 · also t04, t18 · spare unverified: 1 seen after its common craft at tick 730 |
| 7 | Team 13 | RET-08 Palacio de Velázquez | Team 7 | v10 | ~21 | +11.8 (low +11.8) |  | rival buyer | bid ✓ · gap proven · seller holds 2 |
| 8 | Team 16 | RET-06 La Rosaleda | Team 8 | v10 | ~24 | +8.6 (low +8.6) |  |  | bid ✓ · gap proven · seller dumps RET |
| 9 | Team 16 | RET-01 Barca del Estanque | Team 2 | v10 | ~9 | +7.7 (low +7.4) |  |  | bid ✓ · gap proven · seller holds 2 · also t09 |
| 10 | Team 8 | MAL-02 Plaza del Dos de Mayo | Team 14 | v10 | ~9 | +7.6 (low +7.6) |  |  | bid ✓ · undecided · seller dumps MAL · also t07, t16, t04 |
| 11 | Team 16 | RET-03 El Titiritero | Team 4 | v10 | ~9 | +7.1 (low +7.1) |  |  | bid ✓ · gap proven · seller holds 2 · also t08 |
| 12 | Team 7 | SAL-02 El Portero | Team 9 | v10 · club | ~9 | +6.4 (low +6.4) |  |  | bid ✓ · gap proven · seller holds 2 · also t02, t12 |
| 13 | Team 13 | RET-01 Barca del Estanque | Team 9 | v10 | ~8 | +5.1 (low +5.1) |  | rival buyer | bid ✓ · gap proven · seller holds 2 · also t02 |
| 14 | Team 3 | LAT-05 El Organillero | Team 2 | v10 | ~8 | +5 (low +4) |  | rival buyer | bid ✓ · undecided · seller dumps LAT · also t09 |
| 15 | Team 16 | RET-04 Paseo de Coches | Team 8 | v10 | ~9 | +3.4 (low +3.4) |  |  | bid ✓ · gap proven · seller dumps RET · also t03 |
| 16 | Team 13 | RET-03 El Titiritero | Team 8 | v10 | ~8 | +1.2 (low +1.2) |  | rival buyer | bid ✓ · gap proven · seller dumps RET · also t04 |
| 17 | Team 13 | RET-05 La Ardilla | Team 8 | v10 | ~8 | +1.2 (low +1.2) |  | rival buyer | bid ✓ · gap proven · seller dumps RET |
| 18 | Team 7 | SAL-01 Escaparate de Serrano | Team 4 | v10 | ~9 | +0.8 (low +0.8) |  |  | bid ✓ · gap proven · seller dumps SAL |

## Ready DMs

**1. RET-09 · Team 7 → Team 9 at ~76 P on v10 (Puesto de Team 5)**
- To Team 7: "Hi Team 7! Could you post your El Ángel Caído (RET-09) on v10 (Puesto de Team 5) as an ask addressed to Team 9, at ~76 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! Team 7 can post El Ángel Caído (RET-09) on v10 (Puesto de Team 5) as an ask addressed to Team 9, at ~76 P: accept it there once it's up. Thanks!"

**2. MAL-11 · Team 10 → Team 1 at ~100 P on v10 (Puesto de Team 5)**
- To Team 10: "Hi Team 10! Could you post your La Sala Pentagrama (MAL-11) on v10 (Puesto de Team 5) as an ask addressed to Team 1, at ~100 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 1: "Hi Team 1! Team 10 can post La Sala Pentagrama (MAL-11) on v10 (Puesto de Team 5) as an ask addressed to Team 1, at ~100 P: accept it there once it's up. Thanks!"

**3. MAL-10 · Team 10 → Team 9 at ~45 P on v10 (Puesto de Team 5)**
- To Team 10: "Hi Team 10! Could you post your Noche de Movida (MAL-10) on v10 (Puesto de Team 5) as an ask addressed to Team 9, at ~45 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! Team 10 can post Noche de Movida (MAL-10) on v10 (Puesto de Team 5) as an ask addressed to Team 9, at ~45 P: accept it there once it's up. Thanks!"

**4. MAL-09 · Team 10 → Team 9 at ~45 P on v10 (Puesto de Team 5)**
- To Team 10: "Hi Team 10! Could you post your La Heroína del Dos de Mayo (MAL-09) on v10 (Puesto de Team 5) as an ask addressed to Team 9, at ~45 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! Team 10 can post La Heroína del Dos de Mayo (MAL-09) on v10 (Puesto de Team 5) as an ask addressed to Team 9, at ~45 P: accept it there once it's up. Thanks!"

**5. RET-09 · Team 8 → Team 16 at ~70 P on v10 (Puesto de Team 5)**
- To Team 8: "Hi Team 8! Could you post your El Ángel Caído (RET-09) on v10 (Puesto de Team 5) as an ask addressed to Team 16, at ~70 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 8 can post El Ángel Caído (RET-09) on v10 (Puesto de Team 5) as an ask addressed to Team 16, at ~70 P: accept it there once it's up. Thanks!"

**6. LAV-02 · Team 16 → Team 9 at ~9 P on v10 (Puesto de Team 5)**
- To Team 16: "Hi Team 16! Could you post your El Frutero de Argumosa (LAV-02) on v10 (Puesto de Team 5) as an ask addressed to Team 9, at ~9 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! Team 16 can post El Frutero de Argumosa (LAV-02) on v10 (Puesto de Team 5) as an ask addressed to Team 9, at ~9 P: accept it there once it's up. Thanks!"

**7. RET-08 · Team 7 → Team 13 at ~21 P on v10 (Puesto de Team 5)**
- To Team 7: "Hi Team 7! Could you post your Palacio de Velázquez (RET-08) on v10 (Puesto de Team 5) as an ask addressed to Team 13, at ~21 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 13: "Hi Team 13! Team 7 can post Palacio de Velázquez (RET-08) on v10 (Puesto de Team 5) as an ask addressed to Team 13, at ~21 P: accept it there once it's up. Thanks!"

**8. RET-06 · Team 8 → Team 16 at ~24 P on v10 (Puesto de Team 5)**
- To Team 8: "Hi Team 8! Could you post your La Rosaleda (RET-06) on v10 (Puesto de Team 5) as an ask addressed to Team 16, at ~24 P? They're ready to take it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 16: "Hi Team 16! Team 8 can post La Rosaleda (RET-06) on v10 (Puesto de Team 5) as an ask addressed to Team 16, at ~24 P: accept it there once it's up. Thanks!"

## Teams one or two cards from a page

- Team 9 RET 9/10 · missing RET-09
- Team 6 LAV 9/10 · missing LAV-05 · rival · **may be complete** (server: 3 complete pages, feed sees 1)
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
| Team 1 | exact | 39/39 | 21 | 0 |
| Team 2 | partial | 30/34 | 8 | 22 |
| Team 3 | partial | 24/35 | 12 | 24 |
| Team 4 | partial | 39/40 | 10 | 11 |
| Team 6 | inconsistent | 0/40 | 0 | 0 |
| Team 7 | exact | 37/37 | 23 | 0 |
| Team 8 | partial | 28/33 | 11 | 21 |
| Team 9 | partial | 30/42 | 11 | 19 |
| Team 10 | partial | 32/37 | 18 | 10 |
| Team 11 | partial | 1/13 | 14 | 45 |
| Team 12 | exact | 40/40 | 20 | 0 |
| Team 13 | exact | 32/32 | 28 | 0 |
| Team 14 | repaired | 40/41 | 18 | 2 |
| Team 15 | exact | 42/42 | 18 | 0 |
| Team 16 | exact | 34/34 | 26 | 0 |
| Team 17 | exact | 37/37 | 23 | 0 |
| Team 18 | partial | 42/46 | 2 | 16 |

- run/known_holdings.json entry for Team 15 ignored: the feed shows MAL-09, MAL-10 held.
