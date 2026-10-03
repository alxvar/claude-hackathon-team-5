# Sunday: the Chamberí (CHA) page (Builder, Sat 11:40; team bids 12:10; reviews 12:30, 13:30, 13:55, fixes applied)

**Goal:** complete the CHA page Sunday morning, **buying from teams first** (Chief 12:05, from intel/rivals.md play 1).
A dealer buy below our value scores 0 (gains clipped, GAME.md). A team buy scores value − price (cap 50). As maker at
clearing (9 / 24.5 / 70) that is **+7 / +15.5 / +42** per common / uncommon / rare. Dealers are a per-card timed
fallback at ≤ list. The last card always comes from a team (+50, capped). CHA carries our highest multiplier (1.6).

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
that card is worth its value + 106 to us: common 122, uncommon 146, rare 218. A team trade scores at most 50, so the
last card is worth bidding up to **value − 50: 72 / 96 / 168**. No CHA card is minted yet (`minted: 0`). 18 teams [V].

## When [check at 09:00]

- Saturday closes at hour 16.161 (23:00). **Sunday opens at the same hour, at 09:00, with 15 s ticks** [V].
- On the schedule after the open: **CHA released and round 3 at 16.65; the Sunday allowance (+150 P each) at 16.7**
  [V]. If game time keeps pace with the wall clock on Sunday, as it did on Saturday, that is **≈ 09:29 and ≈ 09:32**
  [L]. The catalog says CHA `"release": "sun+0h"`, which reads as 09:00: **[?] 09:00 or ≈ 09:29.** Read `/api/catalog`
  `released` at 09:00 and every few minutes after.
- **Duels III at 18.65 (≈ 11:29)**, 4 at once, until ≈ 12:20 [L]; final duels at 21.65 (≈ 14:29), when all dealers
  close too. Doors close at 22.161 (15:00) [V schedule; wall times L]. Directive 12:50 superseded 10:35: **duels don't
  share our trading limits**, so the trader and dealer threads may run during duels. The plan still aims to finish
  the dealer buys by ~11:20 (Chief 12:05), as a target, not a hard stop.

## Sources and expected prices

| Cards | **First: teams** (our bids, as maker) | Gain | **Fallback: dealers at ≤ list** [V menus] | Dealer score |
|---|---|---|---|---|
| CHA-09, 10 | bid 70 → up to 90 | +42 → +22 each | ~10:00 · Chato, list 77 (finals 82-93 Saturday: bid at list first) | 0, or a loss above 112 |
| CHA-06, 07 | bid 24 → up to 30 | +16 → +10 each | ~10:30 · Abuela, list 25 (ends 21-24) | 0 |
| CHA-01..04 | bid 9 → up to 12 | +7 → +4 each | ~10:30 · Abuela, list 10 (ends 9-10 after 5-7 rounds) | 0 |
| CHA-08, CHA-05 (the pair) | bid flat 24 / 9, below their peers, so they fill last | +16 / +7 | 12:30 · CHA-08 from Abuela ≤ 25 if both are still missing | 0 |
| **The last card**, whichever it is | its bid jumps to **value − 50** (72 / 96 / 168), cash permitting (`last_card`) | **+50** (cap) | never from a dealer: the bonus scores only in a team trade (both dealer bots refuse it) | — |

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

- Now (Sat 13:30, tick 630): **184 P**. Sunday allowance: **+150 P** at ≈ 09:32, a few minutes after the release.
- **Saturday close target (Chief 12:40): ≥ 200 P, stretch 230** (with the allowance: 350 / 380). The 13:15 GUARDRAIL
  allows one Operator bargain buy ≤ 100 that may take cash to 60 for that trade; the tier below is picked from the
  real C, whatever happened.
- **Peak need by ~11:20 ≈ 260-321 P:** the 8 cards other than the pair (244 if all at dealer lists, 288 if all at our
  bid floors, 224 if teams fill at the start bids) plus the pair's flat bids (24 + 9 = 33).
- **Total by ~12:30 ≈ 321-385 P:** add CHA-08 from Abuela (~25) and the last card at value − 50 (72 for CHA-05),
  less the 33 the pair already held. Rares are counted at 90 (team floor); two Chato deals at the `--cap 100` retry add
  up to 20.
- **The book clamps a bid to the cash it has** (227140e): a bid cash can't cover goes out at what cash allows (never
  dropped) and moves up when cash frees. Cash for a bid = `/api/me` cash − our other open bids − the floor. **[?]** If the
  server already holds cash behind an open bid, that counts it twice: at the first bid, read `/api/me` cash just before
  and after, and tell the Builder.
- **abuela_bot and chato_steady don't count open bids:** pass `--cash-floor` = the cash in our open CHA bids, so a
  dealer deal never spends the cash behind a team bid. The trader does count them (227140e).
- Before the allowance, cash won't cover all 10 start bids (257): the book funds them in file order (rares first, the
  pair last) and clamps or skips the rest, retrying every tick.

### Degrade path: cash C at the allowance (Saturday close + 150)

The rares never degrade: 70 → 90 from teams, then Chato at ≤ 77 and ≤ 100. They are worth 112 each and the most from a
team (+42 → +22). What gives first is the pair (Chief 12:40): it already bids flat and last, and the last card takes
whatever cash is left, because any price up to value − 50 scores the same capped +50.

| C (close) | Apply | Peak by 11:20 (worst) | Left for the last card (worst) |
|---|---|---|---|
| ≥ 385 (≥ 235) | the plan as written | 321 | 72 |
| 340-385 (190-235; the 200 target = 350) | nothing to change: the book's cash clamp gives the last card what's left | 321 | C − 313: 37 at 350, 67 at 380 |
| 310-340 (160-190) | **B** | 303 | C − 295: 15-45 |
| < 310 (< 160) | **B + C**, and tell the Chief | ≤ 303 | < 15: a team may not sell the last card that cheap |

Worst cases count rares at 90; the Chato `--cap 100` retry can add up to 20. The table assumes CHA-05 closes (72). If the
last card is CHA-08 (96) or a rare (168), it needs more; the book still bids what cash is left, but a team is unlikely
to sell an uncommon or a rare that cheap.

- **B · commons and uncommons at list.** Floors 10 (CHA-01..04) and 25 (CHA-06/07) instead of 12 / 30. A team fill at 10
  still scores +6; the dealer fallback costs the same.
- **C · rares first.** Add the CHA-01..04 entries only after both rares are in (filled or bought). If the rares aren't
  in at 10:30, the Abuela run for commons waits until they are.

## Order

0. **Pick the degrade tier** from C = Saturday close + 150 before the release; re-read `/api/me` cash after the
   allowance (≈ 09:32) and adjust if it differs. Tell the Chief which tier.
1. **At the release** (catalog `released`; not before, since refused posts retry every tick on the shared 5 req/s),
   right after opening pack 755 (checklist step 3), **add** the CHA bids below to run/book.json for the cards still
   missing, **keeping the asks already there**.
   - All on **El Rastro** (`page_closer: true`): any of them can turn out to be the card that closes the page, and page
     closers stay off team venues (directives 10:18, 10:30). `life: 20` (directive 09:46).
   - `book.py` caps each bid at value − 3 (13 / 37 / 109). Unfilled 20 ticks (5 min at 15 s) at one price, it steps up
     ¼ of the gap to the entry's floor (12 / 30 / 90), if cash allows: rares reach ~85 by 10:00, commons 12 in ~15 min.
   - `last_card: true` (2a465dc): every 10 ticks the book re-reads our value; once a card is the page's last missing
     one, its bid jumps to value − 50 (72 / 96 / 168), cash permitting. **No Operator edit is needed for the closer.**
   - The book cancels a bid by itself once that card reaches us another way (a dealer, the trader, the pack: a005145).
     opps never bids for a card the book bids for (45ce829); run it with `OPPS_BUILD=RET` all morning anyway, so it
     can't bid CHA when an entry is removed for a dealer buy.
**Before any dealer run (steps 2-4): never send the page's last missing card to a dealer.** Count the CHA cards still
missing; the last one keeps its book entry. If a dealer bot refuses a card for "page bonus" (chato_steady exits
"refused: page bonus"; abuela_bot logs `skip_buy` / `cards_not_buyable` "page bonus"), that card has become the last
one: **put its entry back** in run/book.json with `last_card: true`, in one write; it posts straight at value − 50.
This is the one allowed remove-and-re-add.

2. **~10:00 · rares.** For a CHA rare not filled from a team: **remove its entry** from run/book.json (the book cancels
   the bid within a tick), check `/api/me/offers` shows no bid for it, then buy it from Chato with the steady protocol
   (ORCHESTRATOR: rares at a constant +2 to +4): `chato_steady.py CHA-09 --cap 77 --open 57 --step 3 --cash-floor <F>`.
   If he walks with a final above 77, run it again 10 ticks later with `--cap 100` (below 112, so a dealer loss is
   impossible). chato_steady refuses a page's last card, before opening and before every accept (227140e). Never a team
   bid and a Chato thread for the same rare at once: a second copy is worth 28.
3. **~10:30 · the rest.** For CHA-01..04 and CHA-06/07 still missing: remove their entries, check `/api/me/offers`, then
   Abuela per rarity at ≤ list: `--cards <commons> --max-buy 10`, **then** (after it ends: one Abuela run at a time)
   `--cards <uncommons> --max-buy 25`. Aim to be done by ~11:20.
4. **The pair stays as team bids.** Whichever card is last, its bid jumps by itself (step 1). **12:30, after Duels III:**
   if CHA-05 and CHA-08 are both still missing, remove the CHA-08 entry and buy it from Abuela (`--cards CHA-08
   --max-buy 25 --deals 1`): CHA-05 becomes the last card and bids 72 (or what cash allows). CHA-05 is the closer
   because commons print 300 vs 90, so a team is likelier to hold a spare. More than two missing at 12:30: buy all but
   one common the same way. If no team ever sells the last card, the bonus is lost: never close the page through a
   dealer (both dealer bots refuse to).
5. Never a pack unless the Chief directs one (unopened packs drag trade scores [L]). The one exception so far: asset 755
   (silver pack), opened at the release before the CHA bids (checklist step 3).

## run/book.json at the release (add to the asks already there; all on El Rastro)

```json
  {"card": "CHA-09", "side": "buy", "price": 70, "floor": 90, "page_closer": true, "last_card": true, "life": 20},
  {"card": "CHA-10", "side": "buy", "price": 70, "floor": 90, "page_closer": true, "last_card": true, "life": 20},
  {"card": "CHA-06", "side": "buy", "price": 24, "floor": 30, "page_closer": true, "last_card": true, "life": 20},
  {"card": "CHA-07", "side": "buy", "price": 24, "floor": 30, "page_closer": true, "last_card": true, "life": 20},
  {"card": "CHA-01", "side": "buy", "price": 9, "floor": 12, "page_closer": true, "last_card": true, "life": 20},
  {"card": "CHA-02", "side": "buy", "price": 9, "floor": 12, "page_closer": true, "last_card": true, "life": 20},
  {"card": "CHA-03", "side": "buy", "price": 9, "floor": 12, "page_closer": true, "last_card": true, "life": 20},
  {"card": "CHA-04", "side": "buy", "price": 9, "floor": 12, "page_closer": true, "last_card": true, "life": 20},
  {"card": "CHA-08", "side": "buy", "price": 24, "floor": 24, "page_closer": true, "last_card": true, "life": 20},
  {"card": "CHA-05", "side": "buy", "price": 9, "floor": 9, "page_closer": true, "last_card": true, "life": 20}
```

Tier B: CHA-01..04 floor 10, CHA-06/07 floor 25. Tier C: leave CHA-01..04 out until both rares are in.

- **Edit the file in one write** (open, change, save). Never remove an entry and add it back to change a field: the
  removal cancels the bid and the re-add posts it at the file price again, losing its climb (5 asks reset this way at
  Sat 13:11). The one exception: a card a dealer bot refused as the page's last (Order, before step 2).
- A `last_card` entry's `floor` must stay below its value − 50 (72 / 96 / 168), as all the floors above do: a higher
  floor would keep the last card's bid at min(floor, value − 3), which scores less than +50.
- A filled bid is marked done; its entry can stay. **Removing an entry cancels its live bid** (45ce829). A missing or
  half-written file, or one without an `offers` list, changes nothing (227140e).
- **Editing an entry's `price` moves the live bid within a tick**, clamped to the floor, value − 3 and cash; a bid held
  below its file price is re-checked every 10 ticks and moves up once it can (227140e).
- [?] Whether the server accepts a bid before CHA is released: that is why the bids go in at the release.
- The buy-fill path has never run live (no bid of the book has filled yet): watch logs/book.jsonl for `filled` on the
  first team fill.

## 15 s ticks [?]

- **Offer life.** On Saturday, real life = asked × tick_seconds / 60 (asked 120, lived 60). If that ratio holds on
  Sunday, offers live ¼ of what is asked. `opps` and `book.py` already scale by 60 / tick_seconds. **Check the first
  post's `expires_tick − created_tick`** and tell the Builder if it isn't what was asked.
- **Dealer deals.** 5-7 rounds; the dealer bots wait for each reply, so expect ~2.5-4 min per deal at 15 s, plus 10
  ticks (2.5 min) between two conversations with the same dealer. Six open conversations per team: Abuela and Chato
  can run in parallel (one run per dealer at a time).
- **A dealer's offer expires after 4 ticks** [V, threads 805 and 832]. When it expires and nobody moves, both dealer
  bots log `no_live_offer` each tick and walk on the 4th (e875b82). To keep talking to **Chato** at a new cap: Ctrl-C the
  running chato_steady (the thread stays open), then `chato_steady.py <card> --resume <thread> --cap <new> ...`.
  Abuela runs are never resumed (their cap is already her list); abuela_bot has no `--resume` (it is `--resume-cap`,
  and abbreviations are refused since 001c203).

## Operator checklist, Sunday 09:00-12:30

Commands run from the repo root with the key loaded: `set -a; . ./.env; set +a; uv run python agents/dealers/...`.

1. **09:00** · `GET /api/clock` (open? `tick_seconds` 15?), `/api/schedule` (release and allowance hours),
   `/api/catalog` (CHA `released`?), `/api/news`, `/api/me` (cash), `/api/me/value?card=CHA-01` (16), `CHA-06` (40),
   `CHA-09` (112).
2. **09:01** · `tools/daemons.sh status`. Book with floor 0 (its only bids are the CHA page's):
   `CASH_FLOOR=0 MIN_GAIN_SELL=2 tools/daemons.sh restart book`. Opps at 100 without CHA:
   `CASH_FLOOR=100 OPPS_BUILD=RET tools/daemons.sh restart opps`. The trader may run (directive 12:50) at its floor
   100 and counts our open bids against it (227140e): `tools/daemons.sh restart trader` (no CASH_FLOOR prefix).
3. **At the release** · first **open asset 755** (sobre_plata, value 91.1 Sat 12:45) alone in its measurement window:
   `tools/daemons.sh stop book opps trader` (the book's live asks stay up), open it, read `/api/me`, then start them
   again with the step 2 commands
   (Operator 12:50, the Chief's decision: kept unopened until then; luck never scores). Fallback: if the desk or the
   feed shows pack contents are fixed at grant time, open it Saturday evening instead. Then add the CHA bids to
   run/book.json for the cards still missing (a CHA card from the pack: leave its entry out; keep the asks), with the
   floors of the degrade tier, in one write.
   **≈ 09:32** · read `/api/me` cash = C after the allowance; adjust the tier if it differs from the expected and tell
   the Chief. Tier C: add CHA-01..04 only once both rares are in.
4. **First bid out** · `/api/me` cash before and after (does the server hold bid cash?); `expires_tick − created_tick`
   (×4?); it sits on El Rastro.
5. **~10:00** · rares not filled (never the page's last missing card; a refused card goes back in the book: the rule
   before Order step 2): remove the entry, check `/api/me/offers`, then
   `chato_steady.py CHA-09 --cap 77 --open 57 --step 3 --cash-floor <open CHA bid cash>` (and CHA-10); `--cap 100` on
   a second try.
6. **~10:30** · CHA-01..04 / CHA-06/07 still missing, except the page's last missing card: remove the entries, check
   `/api/me/offers`, then
   `abuela_bot.py --dealer abuela --cards <commons> --max-buy 10 --deals <n> --cash-floor <open CHA bid cash>`; when it
   ends, the same with `--cards <uncommons> --max-buy 25`.
7. **By ~11:20** (target) · dealer threads done. Log `neg_points` before and after each deal: expect value − price on
   team buys, 0 on dealer buys.
8. **Any time** · when one CHA card is left, logs/book.jsonl shows its `recheck` to value − 50 within 10 ticks; check
   it. **12:30** · CHA-05 and CHA-08 both missing: remove CHA-08, then `abuela_bot.py --dealer abuela --cards CHA-08
   --max-buy 25 --deals 1 --cash-floor <CHA-05 bid>`; CHA-05's bid jumps to 72 by itself. Expect **+50** on the closing
   team trade.
