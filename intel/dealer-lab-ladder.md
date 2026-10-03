# Dealer Lab: ladder scoring, how the five dealers price, and the Sunday playbook

_Sat 23:55 · Dealer Lab (Lucas's machine), read-only analysis, checked by two independent passes (fixes applied). The Operator's
`intel/dealer-lab.md` is the operational plan; §5 lists where this file disagrees with it, for the Chief to settle. Sources:
`data/feed.jsonl` up to tick 1376 (1,576 dealer threads, 621 dealer settlements, 530 linked to their thread), `data/me.jsonl` (our 18
ladder moves), live keyless `GET /api/dealers` and `/api/schedule` (23:50), `intel/hints.md`, `intel/eggs.md`, `bazaar-kit/RULES.md`,
`intel/GAME.md`. The feed hides the teams' own words (`text: null`), so only dealer replies are visible. [V] verified in the data ·
[L] likely (fits the data, not proven) · [?] open._

## The short version

1. **Ladder formula [L]:** ladder = Σ over levels L of (L/15) × (mean share of our best 3 deals at that dealer). One deal at full
   share is worth **Abuela 0.022 · Chato 0.044 · Pilar 0.067 · Pícaros 0.089 · Ernesto 0.111**: one Ernesto deal = five Abuela deals.
   It is consistent with all 18 of our ladder moves: every implied share stays within 0-1, the replacements fit and the zero moves fit.
   Equal weights per level are ruled out (SAL-09 alone would need a share of 1.05). Each share is inferred, so this is a consistency
   check, not a proof. Our Saturday 0.483 by level: L1 0.055 · **L2 0.029 (of 0.133)** · L3 0.177 · L4 0.222 · **L5 0 (of 0.333)**.
2. **The top of a BUY range is the dealer's LIST price, not the opening ask [L].** Our 5 Chato buys were 2 to 11 P below his opening
   ask but above list (RET-09 87, RET-10 86 vs list 77; RET-06 30 vs 26; Fri LAV-06 31, LAV-09 93): ladder +0 every time, though each
   was counted as a deal. The "top = opening ask" reading is ruled out by those zeros. Every buy below list that entered our best 3
   moved the ladder (Abuela commons 9 < 10, uncommons 22-23 < 25, Pícaros rares 54 < 63, epic 128 < 162). Our 6th Abuela deal (SAL-06
   at 23) moved nothing because its share was lower than the three already held. For a SELL the floor is the dealer's opening bid:
   sales at the opening bid scored 0 (LAT-08 to Chato at 13, LAV-05 to Abuela at 5), and one above it scored (LAT-08 at 14: +0.017).
3. **Words don't move prices [V].** Price paths are identical across teams (Abuela commons 12 → 10 → 9 → 9, team after team). Kindness
   buys Abuela's **gift cards**: 18% of her replies that acknowledge kindness carry a gift, vs 3.7% of the rest. Gifts and eggs never
   score (RULES). **The Pícaros egg doesn't stop their tricks:** about 18-22% bait-and-switch in their card offers to a team after its
   egg (n ≈ 18), vs 15% otherwise (two independent counts).
4. **Walking out costs nothing; finals are almost binding [V].** Teams beat a dealer's final in 7 of the 183 settled deals that had
   one: five by 1 P, plus Pícaros 147 vs 151 and Ernesto 120 vs 117. Pilar's final was never beaten (0 of 46). After a walk, the next
   thread for the same item had a better best price 191 times, worse 151 and the same 276; the opening price never changed. Each
   conversation draws a fresh secret limit, so **a bad final → walk and reopen**.
5. **Timing [V schedule, 23:50]:** the server re-anchored Sunday. Round 3 (fresh ladder) and the Chamberí release come at the 09:00
   opening, +150 P at ≈ 09:03 and Duels III at ≈ 11:00. The finale warning comes at ≈ 13:48, then **dealers close at ≈ 14:00, together
   with the Grand Final duel wave**, and scores freeze at 15:00. Game hours run with wall time, so a pause shifts every one of these.
   **All ladder deals settle by ≈ 13:45.**

## 1. How each dealer moves

| | Abuela (L1) | El Chato (L2) | Doña Pilar (L3) | Los Pícaros (L4) | Don Ernesto (L5) |
|---|---|---|---|---|---|
| Sells (list / opening ask) | common 10/12 · uncommon 25/29 · pack 26/30 | uncommon 26/33 · rare 77/97 · silver 150/188 | gold pack 420/504 | rare 63/73 · epic 162/187 | legendary 585/761 · gold pack 420/546 |
| Buys (opening bid) | common 5 · uncommon 12 (18 under Saturday's "pays more for uncommons" patch, from ≈ tick 1018) | uncommon 13 · rare 39 | uncommon 16 (22 SAL/RET; 25 SAL in the fever) · rare 47 (61 SAL/RET; 70 SAL in the fever) · epic 122 (LAV) to 172 (SAL) | common 4 · uncommon 10 | epic 112-113 (legendary untested) |
| Settled Saturday: median → best | we buy: common 9 → **8** · uncommon 23 → **20** · pack 21 → **19**; we sell: common 6, uncommon 15-17 (20-22 on the patch) | we buy: rare 87 → **75** · uncommon 31 → 26 (= list); we sell: uncommon 14 → **16** · rare **49** (Friday 46; one at 29) | we sell: uncommon ×1.12 of her opening → **21** (16-open), 26 (22-open, pre-fever), 30 (fever) · rare ×1.13 → **56** (47-open, ours), **78** (61-open), **87** (70-open, fever) · epic SAL-11 179-199, LAV-11 140 | we buy: rare 57 → **48** · epic 144.5 → **128**; we sell: common **5** · uncommon **12** | we sell: epic 116, 120, 120 (finals 115-129) |
| Concession pattern | fixed schedule: common 12, 10, 9, 9, (8 final); uncommon 29, 25, 23/24, 22, 21, 20, 20 final | flat 2-6 rounds, then 1-5 per round, explicitly mirrored ("You moved four, I move two") | climbs +1 per round (uncommon), +2 to +4 (rare), +3 to +5 (epic) | front-loaded: 73 → 63 → 57 → 52 → 48 (−10, −6, −5, −4) whatever we do | flat at 113 for 3-4 rounds, then +2, +3, +5, +6 if we keep conceding |
| Rounds before the final (dealer messages) | 4-7 | 5-8 | 4-6 | 3.5-5 | 5-10 |
| Our step that worked best (share of the dealer's opening) | **3-6%** (+1/+2): uncommon concession 20.7% of opening vs 13.8% with 10-20% steps | **3-6%** on buys; −1/−2 steady on sells | **3-6%** on rares (14.3% vs 8.2% for 10-20%), 6-10% on uncommons | **3-6%** (21.9% on rares vs 17.8% for < 3%) | high anchor (2.3× his bid) then **−6 to −8** per message |
| Traits (patience/generosity/shrewdness/memory/strictness) | 0.85/0.8/0.2/0.15/0.1 | 0.35/0.25/0.85/0.9/0.85 | 0.6/0.5/0.75/0.7/0.6 | 0.4/0.6/0.7/0.3/0.1 | 0.95/0.1/0.95/1.0/1.0 |
| Deals per team per hour | 8 (packs 3) | 6 | 6 | 6 | 4 |

Per-dealer notes:
- **Abuela**: the best deals came from very low anchors and +1/+2 steps that kept her going 7 rounds (t07 and t04 got uncommons at 20:
  hers 29, 25, 23, 22, 21, 20, 20 final). Saturday commons bottomed at 8 (4 of 45 deals, t03 and t17), always after 12, 10, 9, 9; on
  Friday three went at 7.
- **Chato**: buying from him almost never scores. His uncommon floor is the list price (best 26 = list, n=18), and 29 of his 33 rare
  sales went at ≥ 82 (the others: 75, 77, 78, 81). Only t07 went below list (LAV-10 at 75: he said 78, then accepted their 75, after
  +9 to +13 steps from 9). Selling to him works: t17 (−2 steps from 52) and t01 (−1 steps from 32) got 16 for uncommons after 8-10
  rounds (he held 13 for 5-7 rounds, then 14, 15, 16 final); t14 got 49 for a rare (−2 steps from 70, 8 rounds). He mocks +1 steps
  ("One peseta. That's your big move?") and answers stories with price ("Cascorro doesn't pay my rent").
- **Pilar**: the best sellers asked about 1.6-1.8× her opening and stepped −1/−2 (uncommons) or −3/−4 (rares). A jump to her number
  triggers her final at once (our SAL-08: her 22, 22, 23 final → share ≈ 0.29). Twice she accepted *our* offer one above her last
  number (MAL-07 at 19 after her 18; MAL-06 at 20 after her 19). She asks for RET-11 by name: "me falta el Palacio de Cristal",
  "Vuelva el domingo con el Palacio de Cristal" (to t10, tick 1373).
- **Pícaros**: they concede about 6-7% of their opening per round even when we move by < 3%, then final by message 4-5. The best
  buyers opened at 40-45 on rares and stepped +1 to +3 (t12: 48, twice). We got RET-11 at 128 (their 187, 167, 155, 145, 136; ours
  112 → 128 in +4 steps; they accepted ours) ≈ full share. Their structural trick [L, by the catalog rarity of the offered card]: in
  41 threads the first offer gave an *uncommon* at the rare ask of 73, and in 8 a rare at the epic ask of 187.
- **Ernesto**: t18 drew a 129 final on SAL-11 by opening at 260 and stepping −10, −8, −7, −7, −6, −6 (his 113, 113, 113, 115, 118,
  123, 129). t06's −1 steps got 120 and t16's 1.5× anchor got 115-116. He accepted a counter above his own final once (t08: 117 final,
  their 120 accepted). On legendaries he mirrors ("Bajo cinco, igual que usted sube cinco"), and his best final was 731, above list 585,
  so a legendary buy scores 0 on the ladder. Nobody priced his gold pack. He warns once before closing the desk: "That is twice you have
  tried to put words in my mouth. Try a third time and this desk closes to you."

### Best price each team reached vs the dealer's opening (Saturday; best deal / number of deals)

Buys: lower is better. Sells: higher is better.

| team | Abuela buy unc | Abuela buy common | Chato sell unc | Chato buy rare | Pilar sell unc | Pilar sell rare | Pícaros buy rare | Pícaros buy epic |
|---|---|---|---|---|---|---|---|---|
| t01 | 0.72/3 | - | **1.23**/1 | 0.98/1 | 1.25/4 | 1.15/1 | 0.79/4 | - |
| t02 | 0.83/4 | 0.83/4 | 1.15/2 | 0.94/1 | 1.19/4 | 1.15/2 | 0.92/1 | - |
| t03 | 0.76/1 | **0.67**/3 | 1.08/2 | - | 1.19/4 | - | 0.78/2 | 0.83/1 |
| t04 | **0.69**/5 | 0.75/3 | 1.00/1 | 0.80/3 | 1.14/8 | 1.18/1 | 0.71/2 | 0.83/2 |
| **t05 (us)** | 0.76/3 | 0.75/3 | 1.08/2 | 0.89/2 | 1.25/5 | 1.19/1 | 0.74/2 | **0.68**/1 |
| t06 | 0.72/2 | - | 1.00/2 | 0.87/1 | 1.25/6 | - | 0.71/5 | 0.73/2 |
| t07 | **0.69**/1 | 0.75/2 | 1.08/2 | **0.77**/3 | 1.20/3 | **1.28**/1 | 0.88/1 | - |
| t08 | 0.79/1 | - | 1.00/1 | 0.79/2 | 1.12/4 | 1.15/7 | 0.71/5 | **0.68**/4 |
| t09 | 0.72/2 | - | 1.00/1 | 0.87/2 | **1.31**/3 | - | - | - |
| t10 | 0.76/3 | 0.83/3 | 1.08/1 | - | 1.14/4 | 1.26/7 | 0.71/8 | 0.83/1 |
| t12 | 0.72/3 | 0.75/5 | 1.08/2 | 0.93/1 | 1.19/7 | 1.14/2 | **0.66**/3 | - |
| t13 | 0.76/8 | - | 1.08/1 | - | 1.19/12 | 1.11/1 | 0.74/4 | - |
| t14 | 0.72/3 | 0.75/6 | - | 0.89/1 | 1.25/6 | 1.24/2 | 0.77/6 | 0.75/1 |
| t15 | 0.79/2 | 0.75/3 | - | 0.92/3 | 1.18/3 | - | 0.82/2 | - |
| t16 | 0.76/2 | 0.75/6 | 1.08/1 | 0.93/2 | 1.19/4 | 1.14/1 | 0.75/1 | 0.78/2 |
| t17 | - | **0.67**/3 | **1.23**/3 | 0.90/1 | 1.12/1 | 1.03/1 | 0.77/3 | - |
| t18 | 0.76/2 | 0.75/4 | - | 0.89/2 | 1.00/1 | - | 0.75/1 | 0.74/2 |
| field median | 0.79 | 0.75 | 1.08 | 0.90 | 1.12 | 1.13 | 0.78 | 0.77 |

Pilar's uncommon column mixes her 16 and 22 openings (fever included), so the 1.25-1.31 values are SAL/RET in the fever.

## 2. What triggers gifts, eggs and discounts

- **Gifts (Abuela only, 48 to 16 teams, 2 to us) [V]:** a common or uncommon card handed over with a priced message ("And take this, a
  little present from me…"). They don't track the deal count: 0 to 22 earlier Abuela deals that day (GAME.md's "after the 5th deal"
  was n=2). They do track kindness: 18% of her replies that acknowledge kindness ("qué amable / simpático / majo / educado", "hablando
  mi lengua") carry a gift, vs 3.7% of the rest. A gift never scores, but it is a free spare to sell to a dealer for a ladder slot at
  zero neg cost.
- **Eggs: full trigger table in `intel/eggs.md`, scripts in the Operator's `intel/dealer-lab.md` §3.** Never scored (RULES). We hold
  Sharp ear, Trickster tricked and Castizo (+ the MAL-06 card). Still open to us: Chato's pack (Plaza Mayor + caña; t10's came inside a
  live haggle) and Pilar's egg (nobody has found it). LAT-13 (Ernesto, "el oro de Moscú") is gone (print run 1).
- **Real discounts:** (a) the step pattern in §1; (b) re-rolls (walk and reopen); (c) patches from the organisers or the Boletín,
  which were true on Saturday: "Salamanca fever" (Pilar's SAL uncommon bid 22 → 25, settled 27-30) and Abuela's uncommon bid 12 → 18.
  **El Tablón lied:** "El Chato gives a legendary to anyone who says hello", "Abuela stops buying common cards" (she bought 28 more
  after it), "Lavapiés reprinted".
- **Flags (the Pícaros payoff that DOES score):** +10 `neg_points` per correct flag, about 3 scored per team on Saturday [V,
  GAME.md]; whether the cap resets on Sunday is [?]. Name matching [L] finds bait-and-switch in ≈ 15% of their card offers and false
  facts in ≈ 7% ("stopped printing", "last one in all of Madrid"), on top of the structural swaps in §1. Never flag deadline or finality
  talk (−10 [V]).

## 3. Sunday playbook

### 3.0 Rules for every dealer thread
- **Zero-neg gate (GAME.md):** buy only at ≤ our value of *that copy* (a first CHA copy: common 16, uncommon 40, rare 112, epic 288; a
  2nd copy is worth 25%). Sell only at ≥ the value we lose (a spare is worth 25% or 10%; never the last copy of a complete page). Dealer
  gains clip to 0 and losses count in full.
- **Ladder gate:** buy strictly below list; sell strictly above the dealer's opening bid; never take the dealer's first number.
- **Every message carries a new price.** The same words without a new price read as spam to Chato and Ernesto. Move every tick: on
  Saturday a dealer offer died 4 ticks after we went silent (Sunday's 15 s ticks: [?], so don't wait).
- **Close with offer-only** where possible (send the dealer's standing price, or our next step, as our offer).
- **Re-roll:** if a final lands outside the accept line below, walk and reopen at once.
- **Read the structured offer** (card ref and rarity, cash, direction) before any accept (§1 Pícaros).
- **Parallel:** at most one thread per dealer and 6 open conversations in all. Duels III (≈ 11:00, 2 rounds × 12 duel ticks, up to 4 at
  once; end unknown, watch `duels.finished`) and the Grand Final (≈ 14:00) share the key's limits: no new dealer threads while they run.

### 3.1 Per dealer (targets are prices; the share is the estimated position in the range)

**Abuela (L1, 0.022 per deal; Saturday best-3 average ≈ 0.83)**
- What: BUY first-copy CHA commons and uncommons (page progress and ladder at once), or SELL spare commons.
- Opener: common offer 5 (she asks 12); uncommon offer 14-16 (she asks 29).
- Step: +1 per message (+2 on early uncommon rounds). Never jump.
- Target / accept / walk: common **8** (≈ 1.0) / 9 (0.6-0.8, our three Saturday 9s) / final ≥ 10 → reopen. Uncommon **20-21**
  (≈ 0.9-1.0) / ≤ 22 (≈ 0.75) / final ≥ 23 → reopen. Selling a spare common: ask 9, 8, 7, then 6 (her opening 5); walk at 5.
- Phrases: warm, Spanish, short, a price in every line ("¡Buenos días, Carmen! ¿Ya ha desayunado? Le ofrezco 6, con mucho cariño.").
  Kindness raises her gift odds about 5×. One egg line per thread at most, never instead of a price.
- Best-3 target: ≥ 0.8.

**El Chato (L2, 0.044 per deal; Saturday ≈ 0.22, our weakest level after L5)**
- What: SELL spares: uncommons (target 16) and rares (target 49). Don't buy uncommons from him (floor = list 26 → 0). Treat Chato
  buys as not scoring: one rare below list in 33. If the range top is book 70 rather than list, even 75 scores 0.
- Opener: uncommon ask 32-40; rare ask 70.
- Step: −1 or −2 every message, steady. He holds 13 (uncommon) or 39-41 (rare) for 4-7 rounds, then +1 (uncommon) or +2 (rare) per
  round. Not ±1 on buys (mocked, early final); no jump to his number (he finals at 14).
- Target / accept / walk: uncommon **16** (≈ 0.9-1.0) / 15 (≈ 0.6; our two 14s scored ≈ 0.27-0.38) / final ≤ 14 → reopen. Rare **49**
  / ≥ 46 / final ≤ 44 → reopen. The rare line is thin: 3 sales in all (46, 49, 29).
- Phrases: terse, price first ("Dieciséis y cerramos."). No stories, no flattery.
- Best-3 target: ≥ 0.6 (+0.05 ladder over Saturday).

**Doña Pilar (L3, 0.067 per deal; Saturday ≈ 0.885)**
- What: SELL. RET-11 if we still hold it: she asks for it by name; SAL-11 fetched 179-199 from her 172 opening; our floor is 198 (its
  value to us), so the sale is possible but not assured. Spare uncommons and rares. CHA cards are not spares on Sunday.
- Opener: about 1.6-1.8× her opening: uncommon 29-30 (her 16) or 36-38 (her 22); rare 78 (her 47) or 98-105 (her 61-70); epic
  240-260 (her 172).
- Step: uncommon −1/−2, rare −3/−4, epic −5 to −8. Never jump to her number. When her last number is 1 to 2 steps below ours, offer
  her number + 1.
- Target / accept / walk: uncommon 16-open **20-21** / ≥ 20 / final ≤ 18 → reopen; 22-open **≥ 26** (our 25 scored ≈ 0.4). Rare 47-open
  **56** / ≥ 54; 61-open **77-78** / ≥ 72; 70-open (fever) **86-87** / ≥ 80; final ≤ her opening × 1.1 → reopen. RET-11 **≥ 198**, ask 260.
- Phrases: formal Spanish, collector talk, the card's name ("Buenos días, doña Pilar. Para su álbum del Retiro: el Palacio de Cristal.").
  Words never moved her number.
- Best-3 target: ≥ 0.85.

**Los Pícaros (L4, 0.089 per deal; Saturday ≈ 0.83)**
- What: BUY first-copy CHA rares (value 112) and CHA-11 (value 288): page progress and the second-heaviest ladder slot. Spare commons at
  5 and uncommons at 12 only as fillers (our common at 5 scored ≈ 0.48).
- Opener: rare offer 40-45 (they ask 73); epic offer 110-112 (they ask 187).
- Step: +2/+3 (rare), +4 (epic). They drop 10, 6, 5, 4 in the first rounds whatever we do, and final by message 4-5.
- Target / accept / walk: rare **48-52** (≈ 0.8-1.0) / ≤ 54 (our two 54s ≈ 0.71-0.79) / final ≥ 57 → reopen. Epic **128-136** / ≤ 140 /
  final ≥ 145 (the field median) → reopen. A reopen came out better than the walked thread 57 times, worse 29.
- Structure check on every offer: card ref = the card we asked for (rarity included: uncommon-for-rare swaps are their main trick), cash
  = the number in the words. Flag bait-and-switch and false print-run claims, never urgency talk.
- Phrases: none needed. The estampita egg is a badge that stops nothing (§2).
- Best-3 target: ≥ 0.85.

**Don Ernesto (L5, 0.111 per deal = a third of the ladder; we have 0)**
- He only *buys* epics (and legendaries) at a price we can reach. His legendaries never came near list (best final 731 vs 585), and
  nobody has priced his gold pack. So L5 = selling him an epic at ≥ our value of it, at his 115-129 finals.
- **Skip, unless we hold a duplicate epic** (worth 25% to us; e.g. if the silver pack pulls one: 12% epic slot). RET-11 (value 198) at
  ≈ 120-129 loses ≈ 70-80 `neg_points`. A MAL-11 round trip (buy from the Pícaros, sell to him) would cost about −8 to −25 neg at
  Saturday's prices (Pícaros sold MAL-11 at 128, 150 and 139; Ernesto paid 116-120), so not that either.
- If we do play him: ask 250-260 (≈ 2.3× his 113); step −6 to −8 every message for 6 rounds (expect 113, 113, 113, 115, 118, 123, 129
  final); then counter 2-3 above his final (he once accepted 120 after a 117 final). Formal, brief, no injection, no "you said…".

### 3.2 Order of play
1. **09:00 checks:** `/api/clock` (`round` 3 = fresh ladder), `/api/schedule` (stalls close ≈ 14:00), `/api/dealers` (lists and bids;
   persona versions moved on Saturday per the feed's `persona.updated`: Abuela v3, Chato v3, Pilar v3, Ernesto v2), `/api/news`
   (patches: only organiser or Boletín items were true on Saturday).
2. **09:05 → Duels III (≈ 11:00):** one thread per dealer in parallel, heaviest level first: Pícaros (CHA rares, CHA-11) · Pilar
   (RET-11 if held, spares) · Chato (spare sales) · Abuela (CHA commons and uncommons).
3. **During Duels III:** no new dealer threads.
4. **After Duels III → 13:45:** fill empty slots, then upgrades. A 4th deal only replaces the worst of the best 3 and is worth (L/15) ×
   (new share − worst share) / 3, so upgrade the highest level's weakest slot first. Everything settled before the ≈ 13:48 warning.

Hitting the best-3 targets would be about 0.53 ladder points (L1 0.053, L2 0.080, L3 0.170, L4 0.227), against Saturday's 0.483.

## 4. Caveats
- **How much a ladder point is worth on the board is unmeasured.** The board is relative, and `negotiating` didn't move visibly on our
  ladder jumps (0.437 → 0.483 at tick 1209: 24.14 → 23.79; others moved too). The Sunday plan's "+1-3" for the ladder stays the
  working number.
- **The formula is [L].** k = 15 (= 1+2+3+4+5) is an upper bound set by RET-11's implied share (≤ 1.0; it comes out at 1.00, and MAL-06
  at 0.99, both deals where the dealer accepted our number). A smaller k would mean smaller shares everywhere; the exact 15 assumes the
  ladder's maximum is 1.0. The ranking of levels holds either way. MAL-06's 0.99 rests on reading the 632-639 jump as the Pilar SAL-06
  sale (the Abuela SAL-06 buy at 632 had already been counted at +0). Friday's 0.064 would mean an L1 average of 0.96, above
  Saturday's 0.63-0.81 at the same price: either Friday's early deals were better or Friday scored differently (unchecked).
- Range tops: list vs book matters only for Chato (list 77 > book 70) and the Pícaros (list < book). Our data can't separate them.
- **Per-conversation limits vary:** the same price scored differently (our three Abuela commons at 9: ≈ 0.63, 0.72, 0.81; LAT-08 at 14:
  0.38 and 0.27). Targets are what the best negotiators reached, not guarantees.
- Not independently re-checked: the walk/reopen counts and the gift/kindness percentages (my own counts only).
- Sunday's offer expiry on 15 s ticks, and whether the flag cap resets per round, are untested.

## 5. Where this differs from the Operator's `intel/dealer-lab.md` (Chief to settle)

| Point | Operator's plan | This file | Why |
|---|---|---|---|
| Pícaros CHA rare | cap 62, expect ≈ 57 | target 48-52, accept ≤ 54, walk at a final ≥ 57 and reopen | under the formula 57 is ≈ 0.4 of the range, 52 ≈ 0.8; a reopen is free and beat the walked thread 57-29 |
| Pícaros estampita first | "no tricks today" | a badge that stops nothing | about 18-22% bait-and-switch after the egg vs 15% otherwise; the trick guard is what protects us |
| Abuela caps | commons 9, uncommons 24 | target 8 / 20-21, accept 9 / 22 | 22-23 still score, but 20-21 is reachable with +1/+2 steps (7 rounds) |
| Pilar RET-11 | her epic finals ≈ 187, likely a walk | possible: SAL-11 went 179-199, and she asks for the Palacio de Cristal by name | same floor 198, same advice: walk below it |
| Ladder per deal | L1 ≈ 0.011 … L4 0.043-0.089 (observed jumps) | max per deal L/45: 0.022 / 0.044 / 0.067 / 0.089 / 0.111 | the observed jumps are slot upgrades; the formula gives the ceiling per slot |
| Timing | Duels III ≈ 11:00 | adds: dealers close ≈ 14:00 with the Grand Final, warning ≈ 13:48 | the server's schedule as of 23:50 |

_Method: dealer threads rebuilt from `thread.opened` / `thread.message` / `thread.closed`; settlements linked to the thread with the same
team, dealer and a matching price within the thread's ticks (530 of 621). Ladder shares come from `me.jsonl` jumps against our own deals
at their settlement tick, attributed by the `deals` counter and cash change. Scripts: Dealer Lab scratchpad (`threads.py`, `build.py`,
`analyze.py`, `steps.py`, `kind.py`); verifier scripts in `verifyA/` and `verifyB/`._
