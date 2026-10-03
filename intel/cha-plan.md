# Sunday: the Chamberí (CHA) page (Builder, Sat 11:40; reworked 12:10 for team bids; verified 12:30, fixes applied)

**Goal:** complete the CHA page Sunday morning, **buying from teams first** (Chief 12:05, from intel/rivals.md play 1).
A dealer buy below our value scores 0 (gains clipped, GAME.md). A team buy scores value − price (cap 50). As maker at
clearing (9 / 24.5 / 70) that is **+7 / +15.5 / +42** per common / uncommon / rare. Dealers are a per-card timed
fallback at ≤ list. The closing card still comes from a team (+50, capped). CHA carries our highest multiplier (1.6).

**Cash floor (GUARDRAIL 11:35, Lucas "ok"):** 0 from doors-open **for the CHA page buys only** (the book's CHA bids and
the dealer fallback below); every other bot keeps 100 until the 02:20 rule (0 by Sunday 14:00).

## The set [V, /api/catalog + /api/me/value]

| Cards | Rarity | Book | Print run | Our value | On the page |
|---|---|---|---|---|---|
| CHA-01..05 | common | 10 | 300 | **16** each | yes |
| CHA-06..08 | uncommon | 25 | 90 | **40** each | yes |
| CHA-09, 10 | rare | 70 | 30 | **112** each | yes |
| CHA-11 | epic | 180 | 9 | 288 | no |
| CHA-12 | legendary | 450 | 3 | 720 | no |

Page bonus = 25% × 265 (page book) × 1.6 = **106** [V, GAME.md]. It is priced into whichever card is missing last, so
that card is worth its value + 106 to us: common 122, uncommon 146, rare 218. No CHA card is minted yet (`minted: 0`).
There are 18 teams [V, leaderboard].

## When [check at 09:00]

- Saturday closes at hour 16.161 (23:00). **Sunday opens at the same hour, at 09:00, with 15 s ticks** [V].
- On the schedule after the open: **CHA released and round 3 at 16.65; the Sunday allowance (+150 P each) at 16.7**
  [V]. If game time keeps pace with the wall clock on Sunday, as it did on Saturday, that is **≈ 09:29 and ≈ 09:32**
  [L]. The catalog says CHA `"release": "sun+0h"`, which reads as 09:00: **[?] 09:00 or ≈ 09:29.** Read `/api/catalog`
  `released` at 09:00 and every few minutes after.
- **Duels III at 18.65 (≈ 11:29)**: 4 at once, 12-tick duels, two round-robins, so it runs until ≈ 12:20 [L]. Directive 10:35
  says no taker accepts during scored duels: **stop the trader and every dealer thread for Duels III** and for the final
  duels at 21.65 (≈ 14:29), when all dealers close too. Doors close at 22.161 (15:00) [V schedule; wall times L].
  **All dealer buying must end by ~11:20.**

## Sources and expected prices

| Cards | **First: teams** (our bids, as maker) | Gain | **Fallback: dealers at ≤ list** [V menus] | Dealer score |
|---|---|---|---|---|
| CHA-01..04 | bid 9 → up to 12 | +7 → +4 each | ~10:30 · Abuela, list 10 (ends 9-10 after 5-7 rounds) | 0 |
| CHA-06, 07 | bid 24 → up to 30 | +16 → +10 each | ~10:30 · Abuela, list 25 (ends 21-24) | 0 |
| CHA-09, 10 | bid 70 → up to 90 | +42 → +22 each | ~10:00 · Chato, list 77 (finals 82-93 Saturday: bid at list first) | 0, or a loss above 112 |
| CHA-08 | bid 24, up to 37 while not the last card | +16 → +3 | 12:30 · Abuela ≤ 25, only if CHA-05 is still missing | 0 |
| CHA-05 (the closer) | bid 9 → 13; **72** once it is the last card | +7; **+50** (cap) as the closer | never from a dealer (the page bonus scores only in a team trade) | — |

- Who sells [?]: teams that pulled CHA from packs or bought from dealers and value CHA low. No team's CHA multiplier is
  known (intel/multipliers.json has only ours), so the bids are **public** (no `to`). One bound [L]: t06's LAV and SAL
  both read ~1.45, so they hold 1.6 and 1.3 and t06's CHA is ≤ 1.1. A top-4 team can fill one of our bids and gain
  price − its value; at near-clearing prices that is small [L].
- [?] Unknown: whether Abuela and Chato have CHA stock at release, and how much (rares print 30 for 18 teams).
  **Doña Pilar** sells no CHA singles: she buys uncommons, rares and epics, and sells gold packs at list 420 (whether
  they carry CHA [?]; never bought).
- Ladder [?]: a negotiated dealer deal counts for the level ladder, one at the dealer's opening price never does
  (RULES.md:35). Whether "at or below list" is the rule is unproven (n = 1, intel/rivals.md §1).

## Cash [V now; L ahead]

- Now (12:40): **123 P**. Sunday allowance: **+150 P** at ≈ 09:32, a few minutes after the release.
- **Peak need by ~11:20 ≈ 295-340 P:** the 8 cards bought by then (244 if all at dealer lists, 288 if all at our bid
  floors, 224 if teams fill at the start bids) plus the CHA-05 and CHA-08 bids standing all morning (13 + 37 = 50).
- **Total by ~12:30 ≈ 340-385 P:** add CHA-08 from Abuela (~23) and CHA-05 as the closer (72), less the 50 those two
  bids already held. Rares are counted at 90 (team floor; Chato's Saturday finals were 82-93): two Chato deals at the
  `--cap 100` retry would add up to 20.
- **Saturday close target (Chief 12:40): ≥ 200 P, stretch 230** (with the 150 allowance: 350 / 380). Projected
  ~200-215: Pilar buys MAL-06/07 (~36), SAL-08 in her fever (~31), the book's asks. No new spend today beyond the
  verified epic exception (≤ 80). Below the full plan's 385, the degrade path below applies.
  - Saturday income still to come: the maker book's asks.
  - SAL-08 to Doña Pilar in her "Salamanca fever": 25% over book ≈ 31 P (worth 22.5 to us, so it scores 0). The schedule
    puts the fever at hour 9.15-11.15 (≈ 15:58-17:58 [L]), but its own note says "until 17:30": **sell before 17:30.**
  - She buys no commons. Pilar opens to all teams at hour 5.51 (≈ 12:20 [L]).
- **[?] Whether the server holds cash behind an open bid.** Our bots subtract open bids from cash themselves (book.py,
  opps). At the first bid, read `/api/me` cash just before and after: if it drops by the bid, the server holds it too and
  the book counts it twice (it would stop bidding early). Tell the Builder either way.
- **abuela_bot and chato_steady don't count open bids:** pass `--cash-floor` = the cash in our open CHA bids (≥ 50 for
  the CHA-05/08 pair), so a dealer deal never spends the cash behind a team bid.
- Before the allowance (≈ 09:32), cash won't cover all 10 start bids (257). The book posts in file order and skips what
  doesn't fit, retrying every tick: the rares are listed first, CHA-08 and CHA-05 last.

### Degrade path: cash C at the allowance (Saturday close + 150), read at ≈ 09:32

The rares never degrade: 70 → 90 from teams, then Chato at ≤ 77 and ≤ 100. They are worth 112 each and the most from a
team (+42 → +22). What gives first is the CHA-05/08 pair, because the last card scores the same capped **+50 at any
price ≤ 72 / 96**: a lower closer bid costs fill chance, not points.

| C (close) | Apply | Peak by 11:20 (worst) | Left for the closer (worst) |
|---|---|---|---|
| ≥ 385 (≥ 235) | the full plan | 338 | 72 |
| 340-385 (190-235; the 200 target = 350) | **A** | 321 | C − 313: 37 at 350, 67 at 380 |
| 310-340 (160-190) | **A + B** | 303 | C − 295: 15-45 |
| < 310 (< 160) | **A + B + C**, and tell the Chief | ≤ 303 | < 15: a team may not sell the last card that cheap |

- **A · the pair waits.** CHA-08 and CHA-05 bid flat until one of them is the last card:
  `{"card": "CHA-08", "side": "buy", "price": 24, "floor": 24, ...}` and `{"card": "CHA-05", "side": "buy", "price": 9,
  "floor": 9, ...}` (last in the file). When one fills, or after CHA-08 is bought from Abuela at 12:30, set the other's
  **`price` and `floor`** to min(72 for CHA-05 / 90 for CHA-08, free cash), where free cash = `/api/me` cash − our other open
  bids. The move clamps to the floor, so both fields must change.
- **B · commons and uncommons at list.** Floors 10 (CHA-01..04) and 25 (CHA-06/07) instead of 12 / 30. A team fill at 10
  still scores +6; the dealer fallback costs the same.
- **C · rares first.** Post the CHA-01..04 bids only after both rares are in (filled or bought); the uncommons and the
  pair stay as above.

## Order

0. **At ≈ 09:32** · read `/api/me` cash = C and pick the degrade tier (Cash section). Tell the Chief which.
1. **At the release** (catalog `released`; not before, since refused posts retry every tick on the shared 5 req/s),
   **add** the 10 CHA bids below to run/book.json, **keeping the asks already there**: an entry removed from the file is
   cancelled within a tick (45ce829).
   - All on **El Rastro** (`page_closer: true`): any of them can turn out to be the card that closes the page, and page
     closers stay off team venues (directives 10:18, 10:30).
   - `life: 20` (directive 09:46).
   - `book.py` caps each bid at value − 3 (13 / 37 / 109). Unfilled 20 ticks (5 min at 15 s) at one price, it steps up
     ¼ of the gap to the entry's floor (12 / 30 / 90), if cash allows: rares reach ~85 by 10:00, commons 12 in ~15 min.
   - The book cancels a bid by itself once that card reaches us another way (a dealer, the trader: a005145), and opps
     never bids for a card the book bids for (45ce829).
2. **~10:00 · rares.** For a CHA rare not filled from a team: **remove its entry** from run/book.json, check
   `/api/me/offers` shows no bid for it, then buy it from Chato with the steady protocol (ORCHESTRATOR: rares at a
   constant +2 to +4): `chato_steady.py CHA-09 --cap 77 --open 57 --step 3 --cash-floor <F>`. If he walks with a final
   above 77, run it again 10 ticks later with `--cap 100` (below 112, so a dealer loss is impossible). chato_steady has
   no page-bonus block: it is safe here only because CHA-05 and CHA-08 are still missing, so a rare can't be the last
   card. Never a team bid and a Chato thread for the same rare at once: a second copy is worth 28.
3. **~10:30 · the rest.** For CHA-01..04 and CHA-06/07 still missing: remove their entries, check `/api/me/offers`, then
   Abuela per rarity at ≤ list: `--cards <commons> --max-buy 10` and `--cards <uncommons> --max-buy 25`. Done by
   **~11:20**, before Duels III (≈ 11:29): no dealer threads during scored duels (directive 10:35).
4. **CHA-05 and CHA-08 stay as team bids.** The moment one fills, the other is the last card (value +106): **set its
   `price` to its floor (72 / 90) in run/book.json** (degrade tier A: `price` and `floor` to min(72 / 90, free cash)). The book re-reads our value and moves the bid within a tick, for
   **+50** as maker (any price ≤ 72 / 96 scores the same capped +50, so waiting only costs fill chance). Left alone, it
   climbs ¼ of the gap every 20 ticks: about an hour to the floor.
   **12:30, after Duels III:** if neither has filled, remove the CHA-08 entry and buy it from Abuela (`--cards CHA-08
   --max-buy 25 --deals 1`), then set CHA-05's `price` to 72. CHA-05 is the closer because commons print 300 vs 90,
   so a team is likelier to hold a spare. If no team ever sells the last card, the bonus is lost: never close the page
   through a dealer (abuela_bot refuses to).
5. Never a pack unless the Chief directs one (unopened packs drag trade scores [L]).

## run/book.json at the release (add to the asks already there; all on El Rastro)

```json
  {"card": "CHA-09", "side": "buy", "price": 70, "floor": 90, "page_closer": true, "life": 20},
  {"card": "CHA-10", "side": "buy", "price": 70, "floor": 90, "page_closer": true, "life": 20},
  {"card": "CHA-06", "side": "buy", "price": 24, "floor": 30, "page_closer": true, "life": 20},
  {"card": "CHA-07", "side": "buy", "price": 24, "floor": 30, "page_closer": true, "life": 20},
  {"card": "CHA-01", "side": "buy", "price": 9, "floor": 12, "page_closer": true, "life": 20},
  {"card": "CHA-02", "side": "buy", "price": 9, "floor": 12, "page_closer": true, "life": 20},
  {"card": "CHA-03", "side": "buy", "price": 9, "floor": 12, "page_closer": true, "life": 20},
  {"card": "CHA-04", "side": "buy", "price": 9, "floor": 12, "page_closer": true, "life": 20},
  {"card": "CHA-08", "side": "buy", "price": 24, "floor": 90, "page_closer": true, "life": 20},
  {"card": "CHA-05", "side": "buy", "price": 9, "floor": 72, "page_closer": true, "life": 20}
```

The full plan (C ≥ 385). Below that, change the floors per the degrade path: A sets CHA-08 to floor 24 and CHA-05 to
floor 9; B sets CHA-01..04 to floor 10 and CHA-06/07 to 25.

- CHA-05 and CHA-08 carry their closing floors (72 / 90). The value − 3 cap holds them at 13 / 37 until one of them
  is the last card; then the cap is 119 / 143 and the floor binds.
- A filled bid is marked done; its entry can stay. **Removing an entry cancels its live bid** (45ce829); a missing or
  half-written file changes nothing.
- **Editing an entry's `price` moves the live bid within a tick** (clamped to the floor and to value − 3; 45ce829).
- [?] Whether the server accepts a bid before CHA is released: that is why the bids go in at the release.
- The buy-fill path has never run live (no bid of the book has filled yet): watch logs/book.jsonl for `filled` on the
  first team fill.

## 15 s ticks [?]

- **Offer life.** On Saturday, real life = asked × tick_seconds / 60 (asked 120, lived 60). If that ratio holds on
  Sunday, offers live ¼ of what is asked. `opps` and `book.py` already scale by 60 / tick_seconds. **Check the first
  post's `expires_tick − created_tick`** and tell the Builder if it isn't what was asked.
- **Dealer deals.** 5-7 rounds; the dealer bots wait for each reply, so expect ~2.5-4 min per deal at 15 s, plus 10
  ticks (2.5 min) between two conversations with the same dealer. Six open conversations per team: run Abuela and Chato
  in parallel.

## Operator checklist, Sunday 09:00-12:30

Commands run from the repo root with the key loaded: `set -a; . ./.env; set +a; uv run python agents/dealers/...`.

1. **09:00** · `GET /api/clock` (open? `tick_seconds` 15?), `/api/schedule` (release and allowance hours),
   `/api/catalog` (CHA `released`?), `/api/news`, `/api/me` (cash), `/api/me/value?card=CHA-01` (16), `CHA-06` (40),
   `CHA-09` (112).
2. **09:01** · `tools/daemons.sh status`. Book with floor 0 (its only bids are the CHA page's):
   `CASH_FLOOR=0 MIN_GAIN_SELL=2 tools/daemons.sh restart book`. Opps separately at 100:
   `CASH_FLOOR=100 tools/daemons.sh restart opps`. **Trader stays stopped until Duels III ends** (directive 10:35).
3. **At the release** · add the 10 CHA bids to run/book.json (keep the asks).
4. **First bid out** · `/api/me` cash before and after (does the server hold bid cash?); `expires_tick − created_tick`
   (×4?); it sits on El Rastro.
5. **~10:00** · rares not filled: remove the entry, check `/api/me/offers`, then
   `chato_steady.py CHA-09 --cap 77 --open 57 --step 3 --cash-floor <open CHA bid cash>` (and CHA-10); `--cap 100` on
   a second try.
6. **~10:30** · CHA-01..04 / CHA-06/07 still missing: remove the entries, check `/api/me/offers`, then
   `abuela_bot.py --dealer abuela --cards <commons> --max-buy 10 --deals <n> --cash-floor <open CHA bid cash>`, and the
   same with `--cards <uncommons> --max-buy 25`.
7. **By ~11:20** · every dealer thread closed (Duels III ≈ 11:29). Log `neg_points` before and after each deal:
   expect value − price on team buys, 0 on dealer buys.
8. **When CHA-05 or CHA-08 fills** · set the other's `price` to its floor (72 / 90). **12:30** · if neither filled:
   remove CHA-08, `abuela_bot.py --dealer abuela --cards CHA-08 --max-buy 25 --deals 1 --cash-floor <CHA-05 bid>`,
   then CHA-05's `price` to 72. Expect **+50** on the closing team trade.
