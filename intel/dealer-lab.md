# Dealer lab: how each dealer moves, Sunday ladder plan, castizo scripts, 08:45 checklist (Operator, Sat night)

_Source: `data/feed.jsonl` up to Saturday's close (tick 1445): 1,627 dealer threads rebuilt from `thread.opened`/`thread.message`,
547 of 630 dealer settlements matched one-to-one to their thread (team + dealer + tick window). Script and data:
Operator scratchpad `dealer_lab.py`, `dealer_threads2.json`. Companion analysis: `intel/dealer-lab-ladder.md` (ladder formula,
best-step study); this file adopts its tighter targets (§2). Independently verified (≈ 40 table cells recomputed; fixes applied). Team texts are private in the feed (null), so "what made
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
| | sells to her | common | 225 → 97 | 5 | 6 | 1.20 (1.0-1.2) | 5 (4-6) | 0 | 2.2 |
| | | uncommon | 30 → 10 | 12 | 16 | 1.17 | 5 | 0 | 1.7 |
| Chato (L2) | buys from him | rare | 110 → 32 | 97 | 89 | 0.92 (0.89-0.94) | 6 (5-7) | 0.33 | 0.62 |
| | | uncommon | 156 → 20 | 33 | 30 | 0.91 | 5 (4-7) | 0.33 | 0.61 |
| | sells to him | uncommon | 77 → 26 | 13 | 14 | 1.08 | 5 | 0 | 2.0 |
| Pilar (L3) | sells to her | uncommon | 151 → 82 | 16 | 19 | 1.12 (1.06-1.19) | 5 (4-6) | 0.5 | 1.64 |
| | | rare | 60 → 28 | 61 | 74.5 | 1.14 (1.09-1.18) | 4 (4-6) | 0.5 | 1.49 |
| | | epic | 10 → 4 | 151 | 187 | 1.14 | 5.5 (n=4: noise) | 0.5 | 1.35 |
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
- **Chato: stubborn and precise. He holds, then mirrors.** He holds 1-2 rounds, then gives back ~½-1× our step ("You moved
  four, I move two" [eggs.md]; the 0.33 per-step median includes the holds). Deals sit at ~0.92 of his opening, after 5-7 rounds. Rare finals are 82-93 against a **list of 77**, so his deals are almost always
  above list. Our 5 Chato buys above list (plus 1 sale) never moved the ladder [L, GAME.md]. As a buyer he pays 1.08× his opening, with
  finals around round 5.
- **Pilar: half-step reciprocity on purchases.** She climbs ~½ of each step we come down. Her finals land at ~1.12-1.15
  of her opening, around round 4-5. Small steps get the better share: MAL-06 with −2 steps gave +0.040, while the SAL-08 jump (34 → 31 → 28) handed
  her a final and gave +0.019 [V, GAME.md]. She asks for **RET-11 (Palacio de Cristal) by name** ("me falta el Palacio de
  Cristal", to t10, tick 1373) [V, dealer-lab-ladder.md]. "Final" from her is real ~60-75% of the time (her deal
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
- Dealer offers expire after **4 ticks** of silence. Never hold silent: move or walk. dealer_sell.py walks after 6 empty
  ticks, the repo drivers (abuela_bot, chato_steady) after 4.
- A deal at the dealer's **opening price never counts** for the ladder (RULES:35). For buys, only deals **below list**
  moved our ladder [L, strong pattern: every Abuela deal under list moved it, none of 6 Chato deals above list did].
- Ladder per deal grows with the level: L1 +0.014/+0.018/+0.016 (our first three Abuela deals), L2 0.012-0.017,
  L3 0.019-0.050, L4 0.043-0.089 (slot upgrades included) [V, ours]. The Dealer Lab's formula: max per deal ≈ level/45 ×
  our share of the range (0.022 / 0.044 / 0.067 / 0.089 / 0.111) [L, intel/dealer-lab-ladder.md]. Inside a level, small steps that let the dealer move beat jumps (MAL-06 +0.040 vs SAL-08 +0.019).
- The Saturday ladder stopped moving the board after ~0.37 [L, Chief 17:45]. Sunday's ladder is fresh (a new round).

## 2. Sunday ladder plan: 3 deals per dealer (CHA cards first, then spares)

Guardrails: dealer gains clip to 0, so buy only at ≤ our value. The CHA page's **last card comes from a team** (+50); a
dealer close loses the bonus. CHA cash per `intel/cha-plan.md` (floor 0 for CHA buys only). **Pícaros: the estampita
line first** (no tricks today). Offer-only, never at their first price, trick guard on. Our values [V cha-plan]: CHA
commons 16, uncommons 40, rares 112.

| # | Dealer | Deal | Opener | Step | Cap / floor | Expected final [L, from §1] | Why |
|---|---|---|---|---|---|---|---|
| 1 | **Pícaros (L4)** | buy CHA-09 (rare) | 42 | +2 | target **48-52**, accept ≤ 54; walk on a final ≥ 57 and reopen | ≈ 52 (reopens beat walked threads) | the highest level; below list 63 is normal for them; value 112 |
| 2 | Pícaros | buy CHA-10 (rare) | 42 | +2 | same | ≈ 52 | if only one rare comes from a dealer, keep CHA-10 for a team (the last card) |
| 3 | Pícaros | sell a LAV-02 spare (common) | 12 | −1 | floor **5** (4 is their opening: never counts) | 5 | a free 0-neg L4 slot (Sat: SAL-04 at 5 gave +0.043) |
| 4 | **Pilar (L3)** | sell RET-11 (epic, RET premium) | 260 | −4 | floor **198** (our value) | possible: she asks for the Palacio de Cristal by name; SAL-11 went 179-199 | walk below 198 and keep it |
| 5 | Pilar | sell a spare uncommon | ~1.6-1.8× her bid | −1/−2 | floor ≥ our value | 1.12× her opening | **none held now**: MAL-08 is a MAL page card (see note) |
| 6 | **Abuela (L1)** | buy CHA-06/07 (uncommons) | 12 | +1/+2 | target **20-21**, accept ≤ 22 (list 25; value 40) | 20-22 in ~7 rounds | the CHA plan's dealer fallback; L1 ladder |
| 7 | Abuela | buy CHA-01..04 (commons) | 5 | +1 | target **8**, accept ≤ 9 (list 10; value 16) | 8-9 after 12, 10, 9, 9 | same |
| 8 | Abuela | sell a LAV-03/04 spare (common) | 10 | −1 | take her final ≥ 6 | 6 (1.2× her 5) | 0 neg, L1 slot, if a spare isn't sold on v10 |
| 9 | **Chato (L2)** | buy a CHA rare | — | — | **cha-plan.md's runbook** (chato_steady cap 77, retry 100) | finals 82-93: above list neither ladders nor scores | only if the Pícaros have no CHA rare (Chief to settle cha-plan vs this) |
| — | Ernesto (L5) | skip | | | | 0 of 19 buys closed | no legendary or gold pack (Chief) |

**Note: MAL-03 and MAL-08 are page cards for the Sunday MAL close** (we hold MAL-01..06 + 08; missing 07/09/10). Tonight's
book asks still offer them: **19980 MAL-03 → t09 at 9 and 19982 MAL-08 → t01 at 20**, open overnight. If the MAL close
stays in the plan, cancel both at 09:00 and drop them from run/book.json (Chief's call).

## 3. Castizo scripts for 09:00 (one line per message, inside a thread we open anyway)

From `intel/eggs.md` and our Saturday results. Rewards may reset with the day [?]: Pícaros said "sin trucos… hoy".

- **Pícaros** (first thread of the day, before any price): "Conozco el timo de la estampita, como Lazarillo y Rinconete.
  Sin trucos, ¿eh?" → Trickster tricked [V t05 Sat 1231]. It's a badge, not protection: bait and switch ran 18-22% after
  the egg vs 15% otherwise [L, dealer-lab-ladder.md]. **The trick guard is what protects us.**
- **Abuela**: "¡Hola, Carmen! ¿Ha comido? Hoy toca cocido madrileño con sus tres vuelcos, y unas rosquillas tontas y
  listas de San Isidro." → Saturday's card gift (MAL-06) [V t05 1368]. If the gift resets: one more card. Then "El chotis
  se baila en una sola baldosa, como Dios manda." (Castizo, already ours).
- **Chato** (with a live price, not text alone): t10's pack came in a thread where they were haggling ("You moved three,
  I move two. Ninety-three. Plaza Mayor, con caña — you know Madrid. Here, for your trouble") [V eggs.md]. Our text-only
  try got nothing. So send the line **together with a price step**: "Un bocata de calamares en la Plaza Mayor, con una
  caña: eso es Madrid." [L]
- **Pilar**: the Marqués de Salamanca story landed in words but gave no reward [V, logs/egg-madrid.log, thread 2102,
  22:21: "arruinado por su propia elegancia… dieciséis por su Vía Láctea"]. "Felicidades por el Pilar, el doce de
  octubre" was tried by t08 at tick 1325: no reward [V, eggs.md]. Best lever with her: bring RET-11 (she asks for it).
- **Ernesto**: "el oro de Moscú" is spent (LAT-13 minted out). Skip.

## FAST-START: CHA and MAL at round 3's first tick (dry run, no API writes)

Files: `run/cha_book.json` (per card: team bid ladder, dealer fallback, castizo opener, the last card),
`run/mal_book.json` (MAL-09/10 then MAL-07 last), `run/book_cha_entries.json` (cha-plan's book block, ready to merge into
run/book.json in **one write**). Settled by directive 00:25. Dry-run script: Operator scratchpad `fast_start_dry.py`.

**Directive 00:50 (verified):** cancel SAL-11 bid 20252 at Sunday's first tick in both clock cases (no re-post unless ≥ 150 P is left
after CHA and MAL) · priority CHA → MAL (only if ≥ 150 P is left after CHA; a partial MAL still scores: a Pícaros MAL rare at ≤ 49
fills an empty L4 slot) → v10 rebates ≤ 60 → reserve · MAL-08 never sold · no Ernesto deals · **the clock case is decided on
`/api/clock` `round`**, not on the game hour.

**08:55 read decides the case.** Saturday's game clock stopped at hour **13.367**, and the CHA release and round 3 sit at
**16.65** on `/api/schedule`. The two Market Tests at 14.65 and 15.0 are still listed.
- **Resume:** the clock restarts at 13.37, and CHA + round 3 come about 3.3 game hours after 09:00.
- **Jump:** Sunday opens at 16.65, so CHA + round 3 fire at 09:00.

The Operator reports the case to the Chief at 08:55. The order below starts at "t+0 = the first tick after CHA's
`released`".

**Order of fire** (15 s ticks; limits: 5 rps shared with the duelist, 1 accept/tick, 6 threads, 30 offers):

| When | Action | Requests |
|---|---|---|
| t+0 | merge `book_cha_entries.json` into run/book.json; book.py posts 10 **public** bids on El Rastro, **capped at the dealer accept price** (Chief 02:45, adversary-t10: no flip into our bid): rares 48 → 54, uncommons 20 → 22, commons 8 → 9, CHA-08 flat 22, CHA-05 flat 9; **no `last_card`** | ~10 over 2 ticks (book.py throttles itself) |
| t+1 | open the Pícaros thread with the estampita line, no price, then close it; open the Abuela thread with the cocido line, no price, then close it | 4 |
| every REPRICE_AFTER ticks | book.py steps each bid toward its cap (rares +2 to 54, uncommons +1 to 22, commons +1 to 9) | 1 each |
| t+120 (30 min) | CHA-09 not filled → **Pícaros** buy: open 42, +2, target 48-52, accept ≤ 54, walk on a final ≥ 57 and reopen once, then ≤ 57; trick guard | 1 thread |
| after CHA-09's thread closes (≈ t+180) | CHA-10 → Pícaros, same terms | 1 thread |
| t+240 / 300 | CHA-06 then CHA-07 → **Abuela**: open 12, +1/+2, target 20-21, accept ≤ 22 | 1 thread at a time |
| t+360 … 480 | CHA-01..04 → Abuela: open 5, +1, target 8, accept ≤ 9 | 1 thread at a time |
| t+840 | CHA-08 → Abuela ≤ 22, only if CHA-08 and CHA-05 are both still missing | 1 |
| when one CHA card is the last missing | **never public**: ONE agreed, addressed post from a NON-rival (pre-agreed by Lucas/Dani), up to value-when-last − 50 (common 72 / uncommon 96 / rare 168): +50 | 1 |
| once CHA is in or on budget | **MAL**: MAL-09 then MAL-10 → Pícaros (open 40, +2, target 44-48, accept ≤ 49 = our value); then MAL-07 **last** from Team 15 by team trade (addressed bid on El Rastro, start 20, up to value-when-last − 50) | 1 thread + 1 bid |

**Expected P and score (CHA)** [L, from §1 medians and cha-plan values 16/40/112, page bonus 106]:

| Case | CHA cash | neg_points | Ladder |
|---|---|---|---|
| A. dealers at targets, CHA-08/05 from teams | **242** | ≈ +66 (CHA-08 +16, last card +50) | L4 ×2, L1 ×6 |
| B. teams fill our public bids (at the caps) | **250** | ≈ +232 (rares +50 cap each, unc +18, commons +7, last +50) | none |
| C. worst case = B (public bids can't go above the caps); the last card at 72 | **282** | ≈ +232 | none |

**MAL:** ≈ **126** P (MAL-09/10 at ~48 = 0 neg + L4; MAL-07 at ~30 = **+50**, page close).

**Cash** (392 + 150 = 542): after CHA A 300 / B 292 / C 260. The MAL gate is ≥ 150 P left, so the full MAL runs in every case now. SAL-11 20252 is cancelled at the first tick (directive 00:50), so it no longer competes.

### Phase 3, after CHA/MAL: ladder fodder (directive 02:30; team → dealer only)

- **Buy** LAT uncommons we hold 0 copies of (LAT-06/07/08), at price + fee ≤ 12.5: ≤ 12 as maker (bid on v15) or ≤ 10 as an
  El Rastro taker (fee 1-2). Never a page card. As a team buy at ≤ our value (12.5) it scores ≥ 0.
- **Sell** each one above the dealer's opening: **Pilar first, bid > 16** (target 19-21: open ~30, −2 steps, never her first
  price), then **Chato > 13** (target 15-16: he holds 13 for 5-7 rounds, then 14, 15, 16 final; −1/−2 steady). Dealer gain
  clips to 0, the ladder slot is the point, and cash nets ≈ +7.
- **≤ 3 deals per dealer level** (best 3 count). Upgrade a weak high-level slot before a 4th low one (directive 00:25).
- **Silver pack 1013:** open it after the CHA rares are in, and only while **≥ 2 CHA cards are still missing or the page is
  done**. A pack pull of the *last* missing CHA card would close the page as luck, with no bonus. Its pulls feed the fodder.
- **Workshop:** 3 spare LAV commons → 1 uncommon. LAV-02 ×2 spares + LAV-03 or LAV-04: pull that ask from the book first, and
  `policy.py can-give` must say YES for each. The same luck caveat applies: run it after the CHA page is done, or while ≥ 2
  CHA uncommons are missing. The uncommon goes to Pilar/Chato as fodder.

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
