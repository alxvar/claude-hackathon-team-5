# v10 matchmaker: page finishers and first copies

_Written by `tools/matchmaker.py` at 22:55 (tick 1420). Read-only. Holdings are a feed lower bound (~80% recall on our own album): a missing card may already be held unless the team bid for it or put it on a want-list (✓). Giver: a true duplicate or a set it dumps; receiver: no copy, collects the set; both gain > 0 at the price (conservative multipliers). Want-lists: `intel/wants.md`. Never a page-closer for a rival or a team < 6 below us; a rival on either side gains <= 10 P at our price._

## Matches (best first)

| # | Buyer | Card | Seller | Price | Value created | Closer | Rival | Why |
|---|---|---|---|---|---|---|---|---|
| 1 | Team 9 | RET-09 El Ángel Caído | Team 7 | ~70 | +118.8 (low +118.8) | **page 10/10** |  | page 9/10 · bid ✓ · seller holds 2 · also t08 |
| 2 | Team 1 | MAL-11 La Sala Pentagrama | Team 10 | ~100 | +72 (low +72) |  | rival seller | bid ✓ · seller dumps MAL |
| 3 | Team 15 | MAL-09 La Heroína del Dos de Mayo | Team 10 | ~45 | +35 (low +35) |  | rival seller | page 8/10 · known want ✓ · seller dumps MAL |
| 4 | Team 15 | MAL-10 Noche de Movida | Team 10 | ~45 | +35 (low +35) |  | rival seller | page 8/10 · known want ✓ · seller dumps MAL |
| 5 | Team 1 | RET-08 Palacio de Velázquez | Team 7 | ~24 | +18.8 (low +18.8) |  |  | bid ✓ · seller holds 2 |
| 6 | Team 9 | LAV-02 El Frutero de Argumosa | Team 16 | ~9 | +13 (low +11.2) |  |  | bid ✓ · seller holds 2 · also t04, t07, t18 |
| 7 | Team 1 | SAL-04 Café en Goya | Team 8 | ~9 | +12.5 (low +10) |  |  | page 8/10 · seller holds 4 · also t07, t15, t14 |
| 8 | Team 3 | LAV-04 Mural de la Esquina | Team 8 | ~9 | +12.5 (low +10) |  | rival buyer | page 8/10 · seller holds 4 · also t01, t16 |
| 9 | Team 14 | LAV-08 Teatro Valle-Inclán | Team 7 | ~26 | +11.2 (low +7.5) |  | rival buyer | page 8/10 · seller dumps LAV |
| 10 | Team 3 | LAV-02 El Frutero de Argumosa | Team 4 | ~9 | +10.5 (low +7.8) |  | rival buyer | page 8/10 · seller holds 2 · also t16 |
| 11 | Team 17 | LAV-06 La Tabacalera | Team 16 | ~24 | +10 (low +7.5) |  | rival buyer | bid ✓ · seller dumps LAV |
| 12 | Team 7 | SAL-05 Taxi Blanco | Team 8 | ~9 | +9 (low +9) |  |  | bid ✓ · seller holds 4 · also t16 |
| 13 | Team 1 | SAL-06 La Galería | Team 2 | ~26 | +8.8 (low +2.5) |  |  | page 8/10 · seller dumps SAL |
| 14 | Team 8 | MAL-02 Plaza del Dos de Mayo | Team 10 | ~9 | +8.8 (low +8.8) |  | rival seller | bid ✓ · seller holds 2 · also t17, t03 |
| 15 | Team 8 | SAL-03 Perrito con Abrigo | Team 1 | ~9 | +8.7 (low +8.4) |  |  | bid ✓ · seller holds 3 · also t15 |
| 16 | Team 7 | SAL-01 Escaparate de Serrano | Team 1 | ~9 | +8.7 (low +8.4) |  |  | bid ✓ · seller holds 3 |
| 17 | Team 3 | SAL-03 Perrito con Abrigo | Team 1 | ~9 | +8.7 (low +8.4) |  | rival buyer | page 8/10 · seller holds 3 · also t15 |
| 18 | Team 14 | LAV-01 La Corrala | Team 16 | ~9 | +8.5 (low +6) |  | rival buyer | page 8/10 · bid ✓ · seller dumps LAV · also t07 |
| 19 | Team 7 | RET-03 El Titiritero | Team 4 | ~9 | +7.5 (low +7.5) |  |  | page 8/10 · seller holds 2 |
| 20 | Team 7 | SAL-02 El Portero | Team 2 | ~9 | +7.5 (low +7.5) |  |  | bid ✓ · seller holds 2 · also t09, t01 |

## Ready DMs

**1. RET-09 · Team 7 → Team 9 at ~70 P**
- To Team 7: "Hi Team 7! Could you post your El Ángel Caído (RET-09) on v10 as an open ask at ~70 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! El Ángel Caído (RET-09) can be on v10 soon: post an open bid there at ~70 P and it crosses. Thanks!"

**2. MAL-11 · Team 10 → Team 1 at ~100 P**
- To Team 10: "Hi Team 10! Could you post your La Sala Pentagrama (MAL-11) on v10 as an open ask at ~100 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 1: "Hi Team 1! La Sala Pentagrama (MAL-11) can be on v10 soon: post an open bid there at ~100 P and it crosses. Thanks!"

**3. MAL-09 · Team 10 → Team 15 at ~45 P**
- To Team 10: "Hi Team 10! Could you post your La Heroína del Dos de Mayo (MAL-09) on v10 as an open ask at ~45 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 15: "Hi Team 15! La Heroína del Dos de Mayo (MAL-09) can be on v10 soon: post an open bid there at ~45 P and it crosses. Thanks!"

**4. MAL-10 · Team 10 → Team 15 at ~45 P**
- To Team 10: "Hi Team 10! Could you post your Noche de Movida (MAL-10) on v10 as an open ask at ~45 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 15: "Hi Team 15! Noche de Movida (MAL-10) can be on v10 soon: post an open bid there at ~45 P and it crosses. Thanks!"

**5. RET-08 · Team 7 → Team 1 at ~24 P**
- To Team 7: "Hi Team 7! Could you post your Palacio de Velázquez (RET-08) on v10 as an open ask at ~24 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 1: "Hi Team 1! Palacio de Velázquez (RET-08) can be on v10 soon: post an open bid there at ~24 P and it crosses. Thanks!"

**6. LAV-02 · Team 16 → Team 9 at ~9 P**
- To Team 16: "Hi Team 16! Could you post your El Frutero de Argumosa (LAV-02) on v10 as an open ask at ~9 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! El Frutero de Argumosa (LAV-02) can be on v10 soon: post an open bid there at ~9 P and it crosses. Thanks!"

**7. SAL-04 · Team 8 → Team 1 at ~9 P**
- To Team 8: "Hi Team 8! Could you post your Café en Goya (SAL-04) on v10 as an open ask at ~9 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 1: "Hi Team 1! Café en Goya (SAL-04) can be on v10 soon: post an open bid there at ~9 P and it crosses. Thanks!"

**8. LAV-04 · Team 8 → Team 3 at ~9 P**
- To Team 8: "Hi Team 8! Could you post your Mural de la Esquina (LAV-04) on v10 as an open ask at ~9 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 3: "Hi Team 3! Mural de la Esquina (LAV-04) can be on v10 soon: post an open bid there at ~9 P and it crosses. Thanks!"

## Teams one or two cards from a page (feed lower bound)

- Team 18 RET 9/10 · missing RET-07 · rival
- Team 16 SAL 9/10 · missing SAL-07
- Team 16 LAT 9/10 · missing LAT-08
- Team 12 LAT 9/10 · missing LAT-08 · rival
- Team 10 RET 9/10 · missing RET-02 · rival
- Team 9 RET 9/10 · missing RET-09
- Team 7 LAV 9/10 · missing LAV-04
- Team 6 LAV 9/10 · missing LAV-05 · rival
- Team 4 LAT 9/10 · missing LAT-02
- Team 15 MAL 8/10 · missing MAL-09, MAL-10
- Team 14 LAV 8/10 · missing LAV-01, LAV-08 · rival
- Team 14 LAT 8/10 · missing LAT-06, LAT-07 · rival
- Team 12 MAL 8/10 · missing MAL-03, MAL-08 · rival
- Team 7 RET 8/10 · missing RET-03, RET-07
- Team 3 SAL 8/10 · missing SAL-03, SAL-10 · rival
- Team 3 LAV 8/10 · missing LAV-02, LAV-04 · rival
- Team 1 SAL 8/10 · missing SAL-04, SAL-06

## Held back (never suggested)

- LAT-08 for Team 12: page-closer for a rival
- RET-07 for Team 18: page-closer for a rival
- RET-02 for Team 10: page-closer for a rival
