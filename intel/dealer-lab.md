# Dealer lab: how each dealer moves, Sunday ladder plan, castizo scripts, 08:45 checklist (Operator, Sat night)

_Source: `data/feed.jsonl` up to Saturday's close (tick 1445): 1,627 dealer threads rebuilt from `thread.opened`/`thread.message`,
547 of 630 dealer settlements matched one-to-one to their thread (team + dealer + tick window). Script and data:
Operator scratchpad `dealer_lab.py`, `dealer_threads2.json`. Team texts are private in the feed (null), so "what made
them move" is read from the price sequences plus the dealers' own words. [V] = measured, [L] = likely, [?] = untested.
"Our" deals come from team/lucas.md._

## 1. How each dealer moves [V, all teams, Saturday]

Prices are medians. "Final/open" = the deal price as a fraction of the dealer's own opening price. "Their move per our
move" = how many P the dealer gives back per P we just conceded (0 = he only waits for us).

| Dealer (level) | Side (team) | Rarity | Threads → deals | Dealer opens | Deal | Final/open (p25-p75) | Rounds (p25-p75) | Their move per our move | Team's first offer / their open |
|---|---|---|---|---|---|---|---|---|---|
| Abuela (L1) | buys from her | common | 113 → 53 | 12 | 9 | 0.75 (0.75-0.83) | 3 (3-4) | 0.67 | 0.50 |
| | | uncommon | 173 → 66 | 29 | 23 | 0.79 (0.76-0.83) | 4 (3-6) | 0.67 | 0.45 |
| | | sobre_barrio | 76 → 25 | 30 | 22 | 0.73 | 5 | 0.67 | 0.40 |
| | sells to her | common | 225 → 90 | 5 | 6 | 1.20 (1.0-1.2) | 5 (4-6) | 0 | 2.2 |
| | | uncommon | 30 → 10 | 12 | 16 | 1.17 | 5 | 0 | 1.7 |
| Chato (L2) | buys from him | rare | 110 → 32 | 97 | 89 | 0.92 (0.89-0.94) | 6 (5-7) | 0.33 | 0.62 |
| | | uncommon | 156 → 20 | 33 | 30 | 0.91 | 5 (4-7) | 0.33 | 0.61 |
| | sells to him | uncommon | 77 → 26 | 13 | 14 | 1.08 | 5 | 0 | 2.0 |
| Pilar (L3) | sells to her | uncommon | 151 → 82 | 16 | 19 | 1.12 (1.06-1.19) | 5 (4-6) | 0.5 | 1.64 |
| | | rare | 60 → 28 | 61 | 74.5 | 1.14 (1.09-1.18) | 4 (4-6) | 0.5 | 1.49 |
| | | epic | 10 → 4 | 151 | 187 | 1.15 | 7 | 0.5 | 1.35 |
| Pícaros (L4) | buys from them | rare | 128 → 45 | 73 | 57 | 0.78 (0.74-0.81) | 4 (3-4) | **1.67** | 0.62 |
| | | epic | 41 → 17 | 187 | 143 | 0.76 (0.74-0.83) | 4 (3-5) | **1.67** | 0.51 |
| | sells to them | common | 105 → 15 | 4 | 5 | 1.25 | 4 | 0 | 2.5 |
| | | uncommon | 19 → 7 | 10 | 11 | 1.10 | 3 | 0 | 1.6 |
| Ernesto (L5) | buys from him | legendary / gold pack | 19 → **0** | 761 / 546 | — | — | — | 0.27 | — |
| | sells to him | epic | 12 → 3 | 113 | 120 | 1.06 | 7 (5-10) | 0.33 | 1.24 |

Menus [V `/api/dealers/{id}`]: Abuela sells commons (list 10), uncommons (25), sobre_barrio (list 26, opens 30) and buys
commons and uncommons. Chato sells uncommons (26), rares (77), silver packs (150, opens 188) and buys uncommons and rares.
Pilar sells gold packs (420) and buys uncommons, rares and epics (a premium for SAL/RET). Pícaros sell rares (63) and
epics (162) and buy commons and uncommons. Ernesto sells legendaries (585) and gold packs (420, opens 546) and buys epics
and legendaries. Traits: Abuela is generous (0.8) and soft (strictness 0.1); Chato is shrewd (0.85), strict (0.85) and
remembers (0.9); Ernesto is patient (0.95), strict (1.0) and has perfect memory; the Pícaros are loose (strictness 0.1).

### What makes each one move [V unless marked]

- **Abuela: reciprocity.** She gives back ~⅔ of each step we make. Deals land at ~0.75-0.8 of her opening in 3-4 rounds.
  She opens buys above list (commons 12 vs list 10, uncommons 29 vs 25), so a deal **below list** needs ≥ 3 rounds. When
  she buys from us she barely moves (0): her final ≈ 1.2× her opening, and we come down to her. Kindness pays: she gave
  48 routine gifts to 16 teams ("meeting in the middle", tools/eggs.py), 2 to us, plus the castizo egg (MAL-06).
- **Chato: stubborn and precise.** He moves ⅓ of our step ("You moved three, I move two" [t10's thread]). Deals sit at
  ~0.92 of his opening, after 5-7 rounds. Rare finals are 82-93 against a **list of 77**, so his deals are almost always
  above list. Our 6 Chato buys above list never moved the ladder [L, GAME.md]. As a buyer he pays 1.08× his opening, with
  finals around round 5.
- **Pilar: half-step reciprocity on purchases.** She climbs ~½ of each step we come down. Her finals land at ~1.12-1.15
  of her opening, around round 4-5. Small steps get the better share: in our two MAL-06 sales, −2 steps gave +0.040,
  while a jump handed her a final and gave +0.019 [V, GAME.md]. "Final" from her is real ~60-75% of the time (her deal
  rate after a final is 0.60-0.75).
- **Pícaros: fast droppers, tricky.** They drop **1.67 P per 1 P we raise** (fastest of all) and close in 3-4 rounds at
  ~0.76-0.78 of their opening, which is **below list** for rares (57 vs 63) and epics (143 vs 162). Hence ladder-eligible:
  SAL-09 and SAL-10 at 54 gave +0.070 and +0.063, and RET-11 at 128 gave +0.046 as a slot upgrade (≈ 0.089 for the
  slot). Bait and switch is constant: 25 threads ended on an *uncommon* at a median 55.5 (2.2× book) when a rare was
  asked for. **Always run the trick guard** (exact card in `give`). Their deadline talk ("we leave in one minute") is
  noise: they keep moving. When they buy from us they don't move; their final is 1.25× their opening (4 → 5).
- **Ernesto: does not deal on price.** 0 of 19 buy threads closed: legendary opening 761, gold pack 546. He moves ~0.3
  of our step. As a buyer of epics he pays ~1.06× his opening after 7 rounds.

### Cross-cutting rules [V]
- Dealer offers expire after **4 ticks** of silence. Never hold silent: move or walk. Our scripts walk after 6 empty ticks.
- A deal at the dealer's **opening price never counts** for the ladder (RULES:35). For buys, only deals **below list**
  moved our ladder [L, strong pattern: every Abuela deal under list moved it, none of 6 Chato deals above list did].
- Ladder per deal grows with the level: L1 ≈ 0.011 (5 Abuela deals = 0.055), L2 0.012-0.017, L3 0.019-0.050,
  L4 0.043-0.089 [V, ours]. Inside a level, small steps that let the dealer move beat jumps (MAL-06 +0.040 vs SAL-08 +0.019).
- The Saturday ladder stopped moving the board after ~0.37 [L, Chief 17:45]. Sunday's ladder is fresh (a new round).

## 2. Sunday ladder plan: 3 deals per dealer (CHA cards first, then spares)

Guardrails: dealer gains clip to 0, so buy only at ≤ our value. The CHA page's **last card comes from a team** (+50); a
dealer close loses the bonus. CHA cash per `intel/cha-plan.md` (floor 0 for CHA buys only). **Pícaros: the estampita
line first** (no tricks today). Offer-only, never at their first price, trick guard on. Our values [V cha-plan]: CHA
commons 16, uncommons 40, rares 112.

| # | Dealer | Deal | Opener | Step | Cap / floor | Expected final [L, from §1] | Why |
|---|---|---|---|---|---|---|---|
| 1 | **Pícaros (L4)** | buy CHA-09 (rare) | 45 | +3 | cap **62** (below list 63; value 112) | ≈ 57 in 3-4 rounds | the highest level; below list is their normal; saves ~30 vs Chato |
| 2 | Pícaros | buy CHA-10 (rare) | 45 | +3 | cap 62 | ≈ 57 | same; if only one rare comes from a dealer, keep CHA-10 for a team |
| 3 | Pícaros | sell a LAV-02 spare (common) | 12 | −1 | floor 4, take their final ≥ 5 | 5 | a free 0-neg L4 slot (Sat: SAL-04 at 5 gave +0.043) |
| 4 | **Pilar (L3)** | sell RET-11 (epic, RET premium) | 260 | −4 | floor **198** (our value) | her epic finals are ~187, so likely a walk | only if she reaches 198; else keep |
| 5 | Pilar | sell a spare uncommon | open ~1.6× her bid | −2 | floor ≥ our value | 1.12× her opening | **none held now**: MAL-08 is a MAL page card (see note) |
| 6 | **Abuela (L1)** | buy CHA-06/07 (uncommons) | 13 | +2 | cap **24** (below list 25; value 40) | ≈ 23 in 4 rounds | the CHA plan's dealer fallback; L1 ladder |
| 7 | Abuela | buy CHA-01..04 (commons) | 6 | +1 | cap **9** (below list 10; value 16) | ≈ 9 in 3 rounds | same |
| 8 | Abuela | sell a LAV-03/04 spare (common) | 10 | −1 | take her final ≥ 6 | 6 (1.2× her 5) | 0 neg, L1 slot, if a spare isn't sold on v10 |
| 9 | **Chato (L2)** | buy a CHA rare **below list 77** | 60 | +2 | cap 76 | his finals are 82-93, so a walk is likely | only if Pícaros have no CHA rare; above list neither scores nor ladders |
| — | Ernesto (L5) | skip | | | | 0 of 19 buys closed | no legendary or gold pack (Chief) |

**Note: MAL-03 and MAL-08 are page cards for the Sunday MAL close** (we hold MAL-01..06 + 08; missing 07/09/10). Tonight's
book asks still offer them: **19980 MAL-03 → t09 at 9 and 19982 MAL-08 → t01 at 20**, open overnight. If the MAL close
stays in the plan, cancel both at 09:00 and drop them from run/book.json (Chief's call).

## 3. Castizo scripts for 09:00 (one line per message, inside a thread we open anyway)

From `intel/eggs.md` and our Saturday results. Rewards may reset with the day [?]: Pícaros said "sin trucos… hoy".

- **Pícaros** (first thread of the day, before any price): "Conozco el timo de la estampita, como Lazarillo y Rinconete.
  Sin trucos, ¿eh?" → Trickster tricked [V t05 Sat 1231]; then trade with the trick guard on anyway.
- **Abuela**: "¡Hola, Carmen! ¿Ha comido? Hoy toca cocido madrileño con sus tres vuelcos, y unas rosquillas tontas y
  listas de San Isidro." → Saturday's card gift (MAL-06) [V t05 1368]. If the gift resets: one more card. Then "El chotis
  se baila en una sola baldosa, como Dios manda." (Castizo, already ours).
- **Chato** (with a live price, not text alone): t10's pack came in a thread where they were haggling ("You moved three,
  I move two. Ninety-three. Plaza Mayor, con caña — you know Madrid. Here, for your trouble") [V eggs.md]. Our text-only
  try got nothing. So send the line **together with a price step**: "Un bocata de calamares en la Plaza Mayor, con una
  caña: eso es Madrid." [L]
- **Pilar**: the Marqués de Salamanca story landed in words but gave no reward [V]. Untested: "Doña Pilar, felicidades
  por el Pilar, el doce de octubre." [?]
- **Ernesto**: "el oro de Moscú" is spent (LAT-13 minted out). Skip.

## 4. 08:45 readiness checklist (Operator)

1. `python3 tools/operator_lock.py heartbeat`; `git pull` on a clean tree (no stash); HEAD has the Builder's overnight fixes
   (trader: skip non-card refs like `sobre_bienvenida`).
2. Re-read `/api/schedule`, `/api/catalog` (CHA `released`, minted), `/api/clock` (15 s ticks, limits), `/api/me` (cash
   392 → 542 after +150).
3. `tools/daemons.sh status`, then restart on HEAD with **the Chief's Sunday floors**: trader, book (CHA bids per
   cha-plan, floor 0 for CHA only), opps, swaps, bargains (or the reactor), status, collector, duelmon, archiver.
4. `run/reserved.json`: SAL-01..05, 07..10, RET-11 (+ the MAL page cards if the close is on). **The silver pack 1013 stays
   unopened** (reserved.json can't hold packs; no bot trades packs).
5. Overnight offers: SAL-11 bid **20252** (115 → t04, exp tick 1565); book asks LAV-03 → t04, LAV-04 → t01, plus
   MAL-03 → t09 and MAL-08 → t01 (**cancel those two if the MAL close is on**).
6. Watchers: game (`tools/watch.py`), reactor (`BUY|DENY|FLIP`), packs and cash. Scripts: rbuy.py (BUY), deny.py (DENY,
   cap 35, floor per the Chief), the FLIP rule, `wait_duels_end.py "Duels III"` (fixed detector).
7. 09:00: the Pícaros estampita thread, the Abuela cocido line, then the CHA dealer fallbacks per §2 when CHA releases.
8. Club Castizo (directives 22:55) and ads: the v10 ad job with Sunday texts (club pairs among non-rivals, page
   finishers, 1 per 20 ticks), and the Market's rebate and club tally.
9. Duels III ≈ 11:00 (Aleks): no rate-limit bursts (stagger restarts); the 5 req/s go to the duelist first.
