# v10 matchmaker: page finishers and first copies

_Written by `tools/matchmaker.py` at 22:22 (tick 1360). Read-only. Holdings are a feed lower bound (~80% recall on our own album): a missing card may already be held unless the team bid for it or put it on a want-list (✓). Giver: a true duplicate or a set it dumps; receiver: no copy, collects the set; both gain > 0 at the price (conservative multipliers). Want-lists: `intel/wants.md`. Never a page-closer for a rival or a team < 6 below us; a rival on either side gains <= 10 P at our price._

## Matches (best first)

| # | Buyer | Card | Seller | Price | Value created | Closer | Rival | Why |
|---|---|---|---|---|---|---|---|---|
| 1 | Team 9 | RET-09 El Ángel Caído | Team 7 | ~70 | +68.4 (low +68.4) |  |  | page 9/10 · bid ✓ · seller holds 2 · also t08 |
| 2 | Team 9 | SAL-10 Museo Lázaro Galdiano | Team 18 | ~30 | +60.5 (low +60.5) |  | rival seller | bid ✓ · seller holds 2 · also t14 |
| 3 | Team 15 | MAL-09 La Heroína del Dos de Mayo | Team 10 | ~45 | +42.4 (low +42.4) |  | rival seller | page 8/10 · known want ✓ · seller dumps MAL |
| 4 | Team 15 | MAL-10 Noche de Movida | Team 10 | ~45 | +42.4 (low +42.4) |  | rival seller | page 8/10 · known want ✓ · seller dumps MAL |
| 5 | Team 1 | RET-09 El Ángel Caído | Team 8 | ~65 | +14.9 (low +14.9) |  |  | bid ✓ · seller dumps RET · also t07 |
| 6 | Team 1 | RET-08 Palacio de Velázquez | Team 4 | ~23 | +14.4 (low +14.4) |  |  | bid ✓ · seller holds 2 · also t07 |
| 7 | Team 13 | RET-08 Palacio de Velázquez | Team 7 | ~22 | +13.7 (low +13.7) |  | rival buyer | bid ✓ · seller holds 2 · also t04 |
| 8 | Team 8 | SAL-03 Perrito con Abrigo | Team 1 | ~9 | +13.2 (low +12.9) |  |  | bid ✓ · seller holds 3 · also t15, t02, t12 |
| 9 | Team 9 | LAV-02 El Frutero de Argumosa | Team 16 | ~9 | +13 (low +11.2) |  |  | bid ✓ · seller holds 2 · also t18 |
| 10 | Team 17 | LAV-06 La Tabacalera | Team 16 | ~24 | +12 (low +9.5) |  | rival buyer | bid ✓ · seller dumps LAV |
| 11 | Team 14 | LAV-01 La Corrala | Team 16 | ~9 | +8.5 (low +6) |  | rival buyer | page 8/10 · bid ✓ · seller dumps LAV |
| 12 | Team 7 | SAL-01 Escaparate de Serrano | Team 1 | ~9 | +8.1 (low +7.8) |  |  | bid ✓ · seller holds 3 · also t04 |
| 13 | Team 16 | RET-01 Barca del Estanque | Team 2 | ~9 | +7.5 (low +7.3) |  |  | bid ✓ · seller holds 2 · also t09 |
| 14 | Team 6 | RET-03 El Titiritero | Team 4 | ~9 | +7.3 (low +7.3) |  | rival buyer | page 8/10 · bid ✓ · seller holds 2 · also t08 |
| 15 | Team 8 | MAL-02 Plaza del Dos de Mayo | Team 7 | ~9 | +7.2 (low +7.2) |  |  | bid ✓ · seller dumps MAL · also t16, t04, t10 |
| 16 | Team 7 | SAL-02 El Portero | Team 9 | ~9 | +6.5 (low +6.5) |  |  | bid ✓ · seller holds 2 · also t02, t01, t12 |
| 17 | Team 7 | SAL-05 Taxi Blanco | Team 16 | ~9 | +6.4 (low +6.2) |  |  | bid ✓ · seller holds 2 · also t08, t12 |
| 18 | Team 1 | RET-03 El Titiritero | Team 10 | ~9 | +6.4 (low +6.4) |  | rival seller | bid ✓ · seller holds 2 · also t04, t08 |
| 19 | Team 13 | RET-01 Barca del Estanque | Team 9 | ~9 | +5.7 (low +5.7) |  | rival buyer | bid ✓ · seller holds 2 · also t02 |
| 20 | Team 3 | LAT-05 El Organillero | Team 2 | ~8 | +5 (low +4) |  | rival buyer | bid ✓ · seller dumps LAT · also t09 |

## Ready DMs

**1. RET-09 · Team 7 → Team 9 at ~70 P**
- To Team 7: "Hi Team 7! Could you post your El Ángel Caído (RET-09) on v10 as an open ask at ~70 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! El Ángel Caído (RET-09) can be on v10 soon: post an open bid there at ~70 P and it crosses. Thanks!"

**2. SAL-10 · Team 18 → Team 9 at ~30 P**
- To Team 18: "Hi Team 18! Could you post your Museo Lázaro Galdiano (SAL-10) on v10 as an open ask at ~30 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 9: "Hi Team 9! Museo Lázaro Galdiano (SAL-10) can be on v10 soon: post an open bid there at ~30 P and it crosses. Thanks!"

**3. MAL-09 · Team 10 → Team 15 at ~45 P**
- To Team 10: "Hi Team 10! Could you post your La Heroína del Dos de Mayo (MAL-09) on v10 as an open ask at ~45 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 15: "Hi Team 15! La Heroína del Dos de Mayo (MAL-09) can be on v10 soon: post an open bid there at ~45 P and it crosses. Thanks!"

**4. MAL-10 · Team 10 → Team 15 at ~45 P**
- To Team 10: "Hi Team 10! Could you post your Noche de Movida (MAL-10) on v10 as an open ask at ~45 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 15: "Hi Team 15! Noche de Movida (MAL-10) can be on v10 soon: post an open bid there at ~45 P and it crosses. Thanks!"

**5. RET-09 · Team 8 → Team 1 at ~65 P**
- To Team 8: "Hi Team 8! Could you post your El Ángel Caído (RET-09) on v10 as an open ask at ~65 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 1: "Hi Team 1! El Ángel Caído (RET-09) can be on v10 soon: post an open bid there at ~65 P and it crosses. Thanks!"

**6. RET-08 · Team 4 → Team 1 at ~23 P**
- To Team 4: "Hi Team 4! Could you post your Palacio de Velázquez (RET-08) on v10 as an open ask at ~23 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 1: "Hi Team 1! Palacio de Velázquez (RET-08) can be on v10 soon: post an open bid there at ~23 P and it crosses. Thanks!"

**7. RET-08 · Team 7 → Team 13 at ~22 P**
- To Team 7: "Hi Team 7! Could you post your Palacio de Velázquez (RET-08) on v10 as an open ask at ~22 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 13: "Hi Team 13! Palacio de Velázquez (RET-08) can be on v10 soon: post an open bid there at ~22 P and it crosses. Thanks!"

**8. SAL-03 · Team 1 → Team 8 at ~9 P**
- To Team 1: "Hi Team 1! Could you post your Perrito con Abrigo (SAL-03) on v10 as an open ask at ~9 P? There's a buyer for it. Only if it's a spare for you, keep one copy. Thanks!"
- To Team 8: "Hi Team 8! Perrito con Abrigo (SAL-03) can be on v10 soon: post an open bid there at ~9 P and it crosses. Thanks!"

## Teams one or two cards from a page (feed lower bound)

- Team 18 RET 9/10 · missing RET-07 · rival · **may be complete** (server: 3 complete pages, feed sees 1)
- Team 16 SAL 9/10 · missing SAL-07 · **may be complete** (server: 2 complete pages, feed sees 0)
- Team 16 LAT 9/10 · missing LAT-08 · **may be complete** (server: 2 complete pages, feed sees 0)
- Team 14 SAL 9/10 · missing SAL-06 · rival · **may be complete** (server: 3 complete pages, feed sees 1)
- Team 12 LAT 9/10 · missing LAT-08 · rival · **may be complete** (server: 3 complete pages, feed sees 0)
- Team 10 RET 9/10 · missing RET-02 · rival · **may be complete** (server: 3 complete pages, feed sees 0)
- Team 9 RET 9/10 · missing RET-09 · **may be complete** (server: 1 complete pages, feed sees 0)
- Team 7 LAV 9/10 · missing LAV-04 · **may be complete** (server: 2 complete pages, feed sees 1)
- Team 6 LAV 9/10 · missing LAV-05 · rival · **may be complete** (server: 2 complete pages, feed sees 0)
- Team 4 LAT 9/10 · missing LAT-02 · **may be complete** (server: 3 complete pages, feed sees 1)
- Team 15 MAL 8/10 · missing MAL-09, MAL-10 · **may be complete** (server: 4 complete pages, feed sees 3)
- Team 14 LAV 8/10 · missing LAV-01, LAV-08 · rival · **may be complete** (server: 3 complete pages, feed sees 1)
- Team 14 LAT 8/10 · missing LAT-06, LAT-07 · rival · **may be complete** (server: 3 complete pages, feed sees 1)
- Team 12 MAL 8/10 · missing MAL-03, MAL-08 · rival · **may be complete** (server: 3 complete pages, feed sees 0)
- Team 6 RET 8/10 · missing RET-03, RET-05 · rival · **may be complete** (server: 2 complete pages, feed sees 0)
- Team 3 SAL 8/10 · missing SAL-03, SAL-10 · rival · **may be complete** (server: 2 complete pages, feed sees 0)
- Team 3 LAV 8/10 · missing LAV-02, LAV-04 · rival · **may be complete** (server: 2 complete pages, feed sees 0)
- Team 1 SAL 8/10 · missing SAL-04, SAL-06 · **may be complete** (server: 3 complete pages, feed sees 0)
