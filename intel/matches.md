# v10 matchmaker: page finishers and first copies

_Written by `tools/matchmaker.py` at 21:30 (tick 1260). Read-only. Holdings are a feed lower bound (~80% recall on our own album): a missing card may already be held unless the team bid for it or put it on a want-list (✓). Giver: a true duplicate or a set it dumps; receiver: no copy, collects the set; both gain > 0 at the price (conservative multipliers). Want-lists: `intel/wants.md`. Never a page-closer for a rival or a team < 6 below us; a rival on either side gains <= 10 P at our price._

## Matches (best first)

| # | Buyer | Card | Seller | Price | Value created | Closer | Rival | Why |
|---|---|---|---|---|---|---|---|---|
| 1 | Team 9 | RET-09 El Ángel Caído | Team 8 | ~100 | +133.6 (low +133.6) | **page 10/10** |  | page 9/10 · bid ✓ · seller dumps RET |
| 2 | Team 9 | SAL-10 Museo Lázaro Galdiano | Team 18 | ~30 | +59.7 (low +59.7) |  | rival seller | bid ✓ · seller holds 2 |
| 3 | Team 15 | MAL-09 La Heroína del Dos de Mayo | Team 10 | ~45 | +42.4 (low +42.4) |  | rival seller | page 8/10 · known want ✓ · seller dumps MAL |
| 4 | Team 15 | MAL-10 Noche de Movida | Team 10 | ~45 | +42.4 (low +42.4) |  | rival seller | page 8/10 · known want ✓ · seller dumps MAL |
| 5 | Team 14 | LAT-06 La Chulapa | Team 9 | ~22 | +15.1 (low +12.6) |  | rival buyer | page 8/10 · seller dumps LAT |
| 6 | Team 1 | RET-08 Palacio de Velázquez | Team 4 | ~22 | +13.9 (low +13.9) |  |  | bid ✓ · seller holds 2 · also t07 |
| 7 | Team 12 | MAL-08 La Vía Láctea | Team 4 | ~26 | +13.6 (low +13.6) |  | rival buyer | page 8/10 · seller dumps MAL |
| 8 | Team 13 | RET-08 Palacio de Velázquez | Team 7 | ~22 | +13.4 (low +13.4) |  | rival buyer | bid ✓ · seller holds 2 · also t04 |
| 9 | Team 8 | SAL-03 Perrito con Abrigo | Team 1 | ~9 | +13.2 (low +13) |  |  | bid ✓ · seller holds 3 · also t02, t15, t12 |
| 10 | Team 9 | LAV-02 El Frutero de Argumosa | Team 16 | ~9 | +13 (low +11.2) |  |  | bid ✓ · seller holds 2 · also t18 |
| 11 | Team 17 | LAV-06 La Tabacalera | Team 16 | ~24 | +12.8 (low +10.3) |  | rival buyer | bid ✓ · seller dumps LAV |
| 12 | Team 3 | LAV-04 Mural de la Esquina | Team 8 | ~9 | +12.7 (low +10.2) |  | rival buyer | page 8/10 · seller holds 3 · also t01, t16 |
| 13 | Team 1 | SAL-04 Café en Goya | Team 8 | ~9 | +12 (low +9.5) |  |  | page 8/10 · seller holds 4 · also t07, t15, t04 |
| 14 | Team 12 | MAL-03 Cartel de Conciertos | Team 8 | ~9 | +11.2 (low +11.2) |  | rival buyer | page 8/10 · seller holds 2 · also t16, t04 |
| 15 | Team 14 | LAV-01 La Corrala | Team 16 | ~9 | +8.5 (low +6) |  | rival buyer | page 8/10 · bid ✓ · seller dumps LAV |
| 16 | Team 7 | SAL-01 Escaparate de Serrano | Team 1 | ~9 | +8.1 (low +7.8) |  |  | bid ✓ · seller holds 3 · also t04 |
| 17 | Team 6 | RET-03 El Titiritero | Team 4 | ~9 | +7.4 (low +7.4) |  | rival buyer | page 8/10 · bid ✓ · seller holds 2 · also t08 |
| 18 | Team 8 | MAL-02 Plaza del Dos de Mayo | Team 7 | ~9 | +7.2 (low +7.2) |  |  | bid ✓ · seller dumps MAL · also t16, t04, t10 |
| 19 | Team 16 | RET-01 Barca del Estanque | Team 9 | ~9 | +7.2 (low +7.2) |  |  | bid ✓ · seller holds 2 |
| 20 | Team 3 | SAL-09 El Marqués | Team 2 | ~91 | +6.6 (low +6.6) |  | rival buyer | bid ✓ · seller dumps SAL |

## Ready DMs

**1. RET-09 · Team 8 → Team 9 at ~100 P**
- To Team 8: "Hi Team 8! Could you post your El Ángel Caído (RET-09) on v10 as an open ask at ~100 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! El Ángel Caído (RET-09) can be on v10 soon: post an open bid there at ~100 P and it crosses. Thanks!"

**2. SAL-10 · Team 18 → Team 9 at ~30 P**
- To Team 18: "Hi Team 18! Could you post your Museo Lázaro Galdiano (SAL-10) on v10 as an open ask at ~30 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! Museo Lázaro Galdiano (SAL-10) can be on v10 soon: post an open bid there at ~30 P and it crosses. Thanks!"

**3. MAL-09 · Team 10 → Team 15 at ~45 P**
- To Team 10: "Hi Team 10! Could you post your La Heroína del Dos de Mayo (MAL-09) on v10 as an open ask at ~45 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 15: "Hi Team 15! La Heroína del Dos de Mayo (MAL-09) can be on v10 soon: post an open bid there at ~45 P and it crosses. Thanks!"

**4. MAL-10 · Team 10 → Team 15 at ~45 P**
- To Team 10: "Hi Team 10! Could you post your Noche de Movida (MAL-10) on v10 as an open ask at ~45 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 15: "Hi Team 15! Noche de Movida (MAL-10) can be on v10 soon: post an open bid there at ~45 P and it crosses. Thanks!"

**5. LAT-06 · Team 9 → Team 14 at ~22 P**
- To Team 9: "Hi Team 9! Could you post your La Chulapa (LAT-06) on v10 as an open ask at ~22 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 14: "Hi Team 14! La Chulapa (LAT-06) can be on v10 soon: post an open bid there at ~22 P and it crosses. Thanks!"

**6. RET-08 · Team 4 → Team 1 at ~22 P**
- To Team 4: "Hi Team 4! Could you post your Palacio de Velázquez (RET-08) on v10 as an open ask at ~22 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 1: "Hi Team 1! Palacio de Velázquez (RET-08) can be on v10 soon: post an open bid there at ~22 P and it crosses. Thanks!"

**7. MAL-08 · Team 4 → Team 12 at ~26 P**
- To Team 4: "Hi Team 4! Could you post your La Vía Láctea (MAL-08) on v10 as an open ask at ~26 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 12: "Hi Team 12! La Vía Láctea (MAL-08) can be on v10 soon: post an open bid there at ~26 P and it crosses. Thanks!"

**8. RET-08 · Team 7 → Team 13 at ~22 P**
- To Team 7: "Hi Team 7! Could you post your Palacio de Velázquez (RET-08) on v10 as an open ask at ~22 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 13: "Hi Team 13! Palacio de Velázquez (RET-08) can be on v10 soon: post an open bid there at ~22 P and it crosses. Thanks!"

## Teams one or two cards from a page (feed lower bound)

- Team 18 RET 9/10 · missing RET-07 · rival
- Team 18 LAT 9/10 · missing LAT-10 · rival
- Team 16 SAL 9/10 · missing SAL-07
- Team 16 LAT 9/10 · missing LAT-08
- Team 10 RET 9/10 · missing RET-02 · rival
- Team 9 RET 9/10 · missing RET-09
- Team 7 LAV 9/10 · missing LAV-04
- Team 6 LAV 9/10 · missing LAV-05 · rival
- Team 4 LAT 9/10 · missing LAT-02
- Team 15 MAL 8/10 · missing MAL-09, MAL-10
- Team 14 LAV 8/10 · missing LAV-01, LAV-08 · rival
- Team 14 LAT 8/10 · missing LAT-06, LAT-07 · rival
- Team 12 MAL 8/10 · missing MAL-03, MAL-08 · rival
- Team 6 RET 8/10 · missing RET-03, RET-05 · rival
- Team 3 LAV 8/10 · missing LAV-02, LAV-04 · rival
- Team 1 SAL 8/10 · missing SAL-04, SAL-06

## Held back (never suggested)

- LAT-10 for Team 18: page-closer for a rival
- RET-07 for Team 18: page-closer for a rival
- RET-02 for Team 10: page-closer for a rival
