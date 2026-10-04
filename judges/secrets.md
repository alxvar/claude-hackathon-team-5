# Secrets desk (auto, Sun 11:36, tick 2007)

_Public data only (feed, news, catalog, levels); `dashboard/secrets.py`. Eggs, badges, gifts and Workshop pulls never score (RULES.md); the cards and packs they bring can be traded. Only Lucas's Operator talks to dealers._

## Hidden cards (catalog `hidden: true`)

- **LAT-13 La Chulapa Dorada** (legendary, print run 1, minted 1): "Only one was ever printed. Don Ernesto knows where." → given to **Team 2** by Don Ernesto at tick 1021

## Easter eggs: the trigger behind each

| Egg | Dealer | Trigger (from the dealer's reply) | Prize | Teams | Us |
|---|---|---|---|---|---|
| Sharp ear | Abuela Carmen | ask Abuela about 'la chulapa dorada' | Sharp ear | 12: Team 1, Team 10, Team 13, Team 16, Team 18, Team 2, Team 3, Team 4, Team 5, Team 6, Team 8, Team 9 | yes |
| gift | Don Ernesto | ask Don Ernesto about 'el oro de Moscú' | LAT-13 | 1: Team 2 | **no** |
| Trickster tricked | Los Pícaros | tell Los Pícaros you know the 'timo de la estampita' (Lazarillo, Rinconete) | Trickster tricked | 9: Team 1, Team 10, Team 13, Team 16, Team 18, Team 2, Team 5, Team 6, Team 8 | yes |
| Castizo | Abuela Carmen | tell Abuela the chotis is danced on one baldosa (verbena de la Paloma) | Castizo | 7: Team 10, Team 13, Team 16, Team 18, Team 2, Team 5, Team 8 | yes |
| gift | El Chato | tell El Chato 'Plaza Mayor, bocadillo de calamares, caña bien tirada' | sobre_barrio | 5: Team 10, Team 12, Team 16, Team 2, Team 8 | **no** |
| gift | Abuela Carmen | tell Abuela about 'cocido madrileño con sus tres vuelcos' (rosquillas) | LAT-06, LAV-08, MAL-06, RET-07, SAL-06 | 8: Team 10, Team 12, Team 16, Team 18, Team 2, Team 5, Team 8, Team 9 | yes |

**Ours:** Abuela Carmen (Castizo), Abuela Carmen (Sharp ear), Abuela Carmen (gift), Los Pícaros (Trickster tricked)
**Missing:** Don Ernesto (gift), El Chato (gift)

## Radio Rastro: which source tells the truth

| Source | TRUE | FALSE | OPEN | FLAVOUR |
|---|---|---|---|---|
| Boletín del Bazar | 1 | 0 | 0 | 1 |
| Radio Rastro | 2 | 0 | 1 | 4 |
| El Tablón | 0 | 4 | 1 | 2 |

| Tick | Source | Headline | Verdict | Evidence |
|---|---|---|---|---|
| 283 | Boletín del Bazar | Radio Rastro is on the air | **FLAVOUR** | Madrid colour (weather, football, metro, churros) |
| 331 | Radio Rastro | Atleti win 2-1 and Madrid goes out to celebrate | **FLAVOUR** | Madrid colour (weather, football, metro, churros) |
| 403 | Radio Rastro | El Chato is looking for rare Malasaña cards | **OPEN** | too few chato rare buys to tell (before 0, after 0) |
| 499 | El Tablón | El Chato gives a legendary to anyone who says hello! | **FALSE** | 0 legendary handed out by chato in the egg log |
| 583 | Radio Rastro | Metro line 5 is closed between Ópera and Callao | **FLAVOUR** | Madrid colour (weather, football, metro, churros) |
| 643 | Boletín del Bazar | Abuela Carmen gives out packs for her saint's day | **TRUE** | 8 gift(s) from abuela within two hours |
| 763 | El Tablón | Abuela stops buying common cards from today | **FALSE** | abuela bought 43 common card(s) afterwards |
| 835 | Radio Rastro | Half-hour queue at the San Ginés churro shop | **FLAVOUR** | Madrid colour (weather, football, metro, churros) |
| 943 | Radio Rastro | Abuela pays more for uncommon cards until teatime | **TRUE** | abuela paid median 15 before (n=3) vs 19.5 after (n=4) |
| 1027 | Radio Rastro | Sun and 24 degrees; a storm after ten | **FLAVOUR** | Madrid colour (weather, football, metro, churros) |
| 1123 | El Tablón | All of Lavapiés will be reprinted tonight | **FALSE** | print runs are fixed (RULES.md: commons 300 … legendaries 3) |
| 1464 | El Tablón | Someone lost a red umbrella next to Abuela's stall | **FLAVOUR** | Madrid colour (weather, football, metro, churros) |
| 1470 | El Tablón | Tomorrow common cards will be worth double | **FALSE** | catalog book for common still 10 |
| 1482 | Radio Rastro | Bonus pay: the Bazaar gives everyone 60 primas in one hour | **TRUE** | our cash +60 at tick 1722 |
| 1494 | El Tablón | El Rastro closes at midnight for roadworks | **OPEN** | a market claim this desk can't test yet |
| 1506 | El Tablón | Anyone want to swap a Cine Doré for two roast chestnuts? | **FLAVOUR** | Madrid colour (weather, football, metro, churros) |

## The Workshop: three spares → one surprise

37 crafts so far; output by set: MAL 11, RET 8, LAT 6, SAL 6, LAV 5, CHA 1. The output is a random card of the next rarity from any released set (inputs from one set come out in another), so a craft is a lottery ticket for the set we build.

- tick 1090 Team 14: common → **SAL-06** La Galería
- tick 1114 Team 12: common → **LAT-08** Las Vistillas
- tick 1202 Team 13: common → **LAT-07** Vermut del Domingo
- tick 1326 Team 1: common → **RET-08** Palacio de Velázquez
- tick 1327 Team 1: common → **MAL-07** Mercado de San Ildefonso
- tick 1333 Team 1: common → **LAV-06** La Tabacalera
- tick 1349 Team 2: common → **MAL-08** La Vía Láctea
- tick 1361 Team 1: uncommon → **LAT-09** San Isidro
- tick 1404 Team 8: common → **RET-06** La Rosaleda
- tick 1466 Team 5: common → **LAV-07** Samosas de la Plaza
- tick 1718 Team 10: common → **CHA-07** Club de Jazz
- tick 1819 Team 2: common → **MAL-08** La Vía Láctea

- **The Workshop**: ««Three spares. One surprise.»» POST /api/taller {"assets": [a, b, c]}: three spare copies of one rarity (you keep at least one of each card) become one card of the next rarity. The pull is luck, shown and never scored.
- **Radio Rastro**: ««At El Rastro you hear everything. Some of it is true.»» News on air: GET /api/news (newest first; also news.posted on the live stream). Three sources: the Boletín del Bazar (the Bazaar bulletin), Radio Rastro and El Tablón, the notice board. Some items are true and the market moves as they say; some are rumours that never happen; some are just Madrid. Nothing tells you which is which.
