# Sunday: the Chamberí (CHA) page (Builder, Sat 11:40, reworked 12:10 for team bids; independently verified)

**Goal:** complete the CHA page Sunday morning, **buying from teams first** (Chief 12:05, from intel/rivals.md play 1).
A dealer buy below our value scores 0 (gains clipped, GAME.md). A team buy scores value − price (cap 50). As maker at
clearing (9 / 24.5 / 70) that is **+7 / +15.5 / +42** per common / uncommon / rare. Dealers are a per-card timed
fallback at ≤ list. The closing card still comes from a team (+50, capped). CHA carries our highest multiplier (1.6).

**Decision needed from Lucas (GUARDRAIL):** the Sunday-morning cash floor (proposed: 0 from 09:00 for the CHA page
buys only). Today's floor is 100; the 02:20 GUARDRAIL says "0 by Sunday 14:00".
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

| Cards | **First: teams** (our bids, as maker) | Gain vs dealer | **Fallback ~10:30: dealers at ≤ list** [V menus] | Dealer score |
|---|---|---|---|---|
| CHA-01..05 | bid 9 → up to 12 | +7 → +4 each | Abuela, list 10 (ends 9-10 after 5-7 rounds) | 0 |
| CHA-06..08 | bid 24 → up to 30 | +16 → +10 each | Abuela, list 25 (ends 21-24); Chato list 26 | 0 |
| CHA-09, 10 | bid 70 → up to 90 | +42 → +22 each | Chato, list 77 (finals 82-93 Saturday: bid at list first) | 0, or a loss above 112 |
| The last card | a team, on El Rastro | **+50** (cap) | never from a dealer (the page bonus scores only in a team trade) | — |

- Who sells [?]: teams that pulled CHA from packs or bought from dealers and value CHA low. No team's CHA multiplier is
  known yet (intel/multipliers.json has only ours; none can be deduced), so the bids are **public** (no `to`). A
  top-4 team can fill one and gain price − its value; at near-clearing prices that is small [L].
- [?] Unknown: whether Abuela and Chato have CHA stock at release, and how much (rares print 30 for 18 teams).
  **Doña Pilar** sells no CHA singles: she buys uncommons, rares and epics, and sells gold packs at list 420 (whether
  they carry CHA [?]; never bought).

## Cash [V now; L ahead]

- Now (11:13): **114 P**. Sunday allowance: **+150 P** at ≈ 09:32, a few minutes after the release.
- **Need by ~11:20:** about the same whether teams or dealers sell (≈ 264 P at near-list prices); team fills at
  clearing cost a little less. Open bids lock cash while they stand.
- **Need later:** CHA-05 and CHA-08 from teams (one at ≤ 13 or 37, the closer at 40-96): **total ≈ 315-365 P**.
- **Hold cash on Saturday evening: ≥ ~170 P at the 23:00 close** (with the 150 allowance: ~320).
  - Saturday income still to come: the maker book on v07.
  - SAL-08 to Doña Pilar in her "Salamanca fever": 25% over book ≈ 31 P (worth 22.5 to us, so it scores 0). The schedule
    puts the fever at hour 9.15-11.15 (≈ 15:58-17:58 [L]), but its own note says "until 17:30": **sell before 17:30.**
  - She buys no commons. Pilar opens to all teams at hour 5.51 (≈ 12:20 [L]).
- If cash is short at release, buy the two rares first and the commons and uncommons after the allowance (≈ 09:32).

## Order

1. **At doors-open (09:00) or the release**, pre-load team bids for **all 10 CHA cards** in run/book.json (below).
   - All on **El Rastro** (`page_closer: true`): any of them can turn out to be the card that closes the page, and page
     closers stay off team venues (directives 10:18, 10:30).
   - `life: 20` (directive 09:46).
   - Our bids lock cash: the start prices total 257 P, so they fit in ~264 (Saturday close ~114 + 150 allowance) only
     with the GUARDRAIL floor at 0.
   - `book.py` caps each bid at value − 3 (13 / 37 / 109), steps it up every 20 ticks to the entry's floor (12 / 30 /
     90), and re-reads our values every 10 ticks.
2. **~10:00 · rares.** If a CHA rare hasn't filled from a team, remove its bid and buy it from Chato at **list (77)**
   first (`abuela_bot --dealer chato --cards CHA-09` or `CHA-10`, cap 100). Never keep a team bid and a Chato thread
   for the same rare at once: a second copy is worth 28.
3. **~10:30 · the rest.** Remove the bids for the cards still missing **except CHA-05 and CHA-08**, and buy those from
   Abuela at ≤ list (`abuela_bot --dealer abuela --cards <those>`). Done by **~11:20**, before Duels III (≈ 11:29):
   no dealer threads during scored duels (directive 10:35).
4. **CHA-05 and CHA-08 stay as team bids.** Whichever fills second closes the page: its value jumps by 106, so its
   cap rises to its floor (72 / 90 in the closing entries below), for **+50** as maker.
   **12:30, after Duels III:** if neither has filled, buy CHA-05 from Abuela (`--cards CHA-05 --deals 1`) so CHA-08
   closes. If no team ever sells the last card, the bonus is lost: never close the page through a dealer.
5. Never a pack unless the Chief directs one (unopened packs drag trade scores [L]).

## run/book.json at doors-open (team bids, all on El Rastro)

```json
{"offers": [
  {"card": "CHA-09", "side": "buy", "price": 70, "floor": 90, "page_closer": true, "life": 20},
  {"card": "CHA-10", "side": "buy", "price": 70, "floor": 90, "page_closer": true, "life": 20},
  {"card": "CHA-06", "side": "buy", "price": 24, "floor": 30, "page_closer": true, "life": 20},
  {"card": "CHA-07", "side": "buy", "price": 24, "floor": 30, "page_closer": true, "life": 20},
  {"card": "CHA-08", "side": "buy", "price": 24, "floor": 90, "page_closer": true, "life": 20},
  {"card": "CHA-01", "side": "buy", "price": 9, "floor": 12, "page_closer": true, "life": 20},
  {"card": "CHA-02", "side": "buy", "price": 9, "floor": 12, "page_closer": true, "life": 20},
  {"card": "CHA-03", "side": "buy", "price": 9, "floor": 12, "page_closer": true, "life": 20},
  {"card": "CHA-04", "side": "buy", "price": 9, "floor": 12, "page_closer": true, "life": 20},
  {"card": "CHA-05", "side": "buy", "price": 9, "floor": 72, "page_closer": true, "life": 20}
]}
```

- CHA-05 and CHA-08 carry their closing floors (72 / 90). The value − 3 cap holds them at 13 / 37 until one of them
  is the last card; then the cap is 119 / 143 and the floor binds.
- Remove an entry when its card has filled (the book marks it done) or when its dealer fallback starts.
- [?] Whether the server accepts a bid before CHA is released: if refused at 09:00, the book retries every tick; it
  goes out at the release.
- To move a bid faster, raise its `price`: the book re-reads the file every tick and never passes the floor.

## 15 s ticks [?]

- **Offer life.** On Saturday, real life = asked × tick_seconds / 60 (asked 120, lived 60). If that ratio holds on
  Sunday, offers live ¼ of what is asked. `opps` and `book.py` already scale by 60 / tick_seconds. **Check the first
  post's `expires_tick − created_tick`** and tell the Builder if it isn't what was asked.
- **Dealer deals.** 5-7 rounds; `abuela_bot` waits for each reply, so expect ~2.5-4 min per deal at 15 s, plus 10 ticks
  (2.5 min) between two conversations with the same dealer. Six open conversations per team: run Abuela and Chato in
  parallel. Eight deals ≈ 35-45 min, which fits 09:29 → ~10:15 for Abuela.

## Operator checklist, Sunday 09:00-12:30

1. **09:00** · `GET /api/clock` (open? `tick_seconds` 15?), `/api/schedule` (release and allowance hours),
   `/api/catalog` (CHA `released`?), `/api/news`, `/api/me` (cash; our CHA values 16/40/112).
2. **09:01** · `tools/daemons.sh status`; restart `book` (`MIN_GAIN_SELL=2`, Sunday `CASH_FLOOR` per GUARDRAIL) and
   `opps`. **Trader stays stopped until Duels III ends** (directive 10:35).
3. **09:02** · Cancel Saturday asks that hold cash we need. Write the 10 CHA bids into run/book.json.
4. **First bid out** · check `expires_tick − created_tick` (×4?); check it sits on El Rastro.
5. **~10:00** · rares not filled: remove the bid, then `uv run python agents/dealers/abuela_bot.py --dealer chato --cards CHA-09 --deals 1 --cash-floor <floor>` (and CHA-10).
6. **~10:30** · cards still missing except CHA-05/08: remove the bids, then `uv run python agents/dealers/abuela_bot.py --dealer abuela --cards <them> --deals <n> --cash-floor <floor>`.
7. **By ~11:20** · every dealer thread closed (Duels III ≈ 11:29). Log `neg_points` before and after each deal:
   expect value − price on team buys, 0 on dealer buys.
8. **12:30** · CHA-05/08: if neither filled, `--cards CHA-05 --deals 1` with Abuela so CHA-08 closes. Expect
   **+50** on the closing team trade.
