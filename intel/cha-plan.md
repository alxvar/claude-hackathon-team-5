# Sunday: the Chamberí (CHA) page (Builder, Sat 11:40; live API facts at 11:13; independently verified)

**Goal:** complete the CHA page on Sunday morning. Eight cards come from dealers at ≤ our value (each scores 0 and loses
nothing). The last two come from teams; the one that closes the page scores +50 (the per-trade cap). CHA carries our highest multiplier (1.6), so
dealer prices sit well below our values.

**Decision needed from Lucas (GUARDRAIL):** the Sunday-morning cash floor. The plan spends ≈ 264 P by ~11:20, out of ≈ 264-320 P. Today's floor is 100. The 02:20 GUARDRAIL only says "0 by Sunday 14:00". Proposed: **floor 0 from 09:00 Sunday for the CHA page buys only.**

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

| Cards | Source | Menu [V, /api/dealers] | Expected price [GAME.md, Saturday] | Score |
|---|---|---|---|---|
| CHA-01..05 | Abuela | commons of released sets, list 10; 8 deals/team/hour | opens ~12, ends **9-10** after 5-7 rounds | 0 each (price < 16) |
| CHA-06..08 | Abuela (Chato as backup) | uncommons, list 25 (Chato 26); Chato 6 deals/team/hour | Abuela opens ~29, ends **21-24**; Chato finals ~31 | 0 each (< 40) |
| CHA-09, 10 | Chato | rares of released sets, list 77 | opens 97, +2-4 per round; finals **82-93**, seven of eight at **89-93** | 0 each (< 112) |
| The last card | a team | a page-closer bid on El Rastro | see "Order" | **+50** (cap) |

[?] Unknown: whether Abuela and Chato have CHA stock at release, and how much (rares print 30 for 18 teams). Teams
may also pull CHA from packs; which sets a pack draws from isn't in the catalog. **Doña Pilar** sells no CHA singles:
she buys uncommons, rares and epics, and sells gold packs at list 420 (whether they carry CHA [?]; never bought).

## Cash [V now; L ahead]

- Now (11:13): **114 P**. Sunday allowance: **+150 P** at ≈ 09:32, a few minutes after the release.
- **Need by ~11:20 (dealer part):** rares 2 × ~90 = 180, CHA-06/07 2 × ~23 = 46, CHA-01..04 4 × ~9.5 = 38, **≈ 264 P**.
- **Need later:** CHA-05 and CHA-08 from teams (one at ≤ 13 or 37, the closer at 40-96): **total ≈ 315-365 P**.
- **Hold cash on Saturday evening: ≥ ~170 P at the 23:00 close** (with the 150 allowance: ~320).
  - Saturday income still to come: the maker book on v07.
  - SAL-08 to Doña Pilar in her "Salamanca fever": 25% over book ≈ 31 P (worth 22.5 to us, so it scores 0). The schedule
    puts the fever at hour 9.15-11.15 (≈ 15:58-17:58 [L]), but its own note says "until 17:30": **sell before 17:30.**
  - She buys no commons. Pilar opens to all teams at hour 5.51 (≈ 12:20 [L]).
- If cash is short at release, buy the two rares first and the commons and uncommons after the allowance (≈ 09:32).

## Order

1. **Rares first** (print 30, scarcest), from Chato at release: CHA-09, then CHA-10, cap 100 each (value 112; never
   above value, since dealer losses count in full).
2. **Uncommons CHA-06 and CHA-07, then commons CHA-01..04**, from Abuela; caps at value − 3 (37 / 13).
3. **Keep CHA-05 (a common) and CHA-08 (an uncommon) missing** after the dealer runs, and bid for both from teams on
   El Rastro (book.json below):
   - While both are missing, neither closes the page. `book.py` caps each bid at our value − 3 (CHA-05 13, CHA-08
     37), so a team fill of either is an ordinary buy.
   - **The other one is then the last card.** Its value jumps by 106 (CHA-08 to 146, CHA-05 to 122) and `book.py`
     re-reads values every 10 ticks, so its cap rises to the entry's floor.
   - The closing team trade scores the full **+50** as maker at any price ≤ 96 (CHA-08) or ≤ 72 (CHA-05), if the cap is
     a flat 50. **CHA-08 closing at ≤ ~90 also tests flat-50 against 5×book (125)**, GAME.md's open question; above ~90
     both read 50 and pack drag (±1-4 [L]) blurs it. CHA-05 closing gives no test (5×10 = 50).
4. **12:30, after Duels III: if neither has filled, buy one from Abuela** so the other is last. Prefer
   `--cards CHA-05`, so the uncommon CHA-08 closes and runs the cap test. `abuela_bot` refuses a card that would close
   the page from a dealer, so it can't buy the last one by mistake. If the last card never comes from a team, the page
   bonus is lost: never close the page through a dealer.
5. Rares as team bids: **only if Chato has no CHA rares**, and then sequentially. Never post them while a Chato
   conversation can still sell one: a team filling a bid after Chato has sold us the card buys a 2nd copy worth 28 at
   ~100 (about −70). `book.py` doesn't cancel a bid when the card arrives from elsewhere.
6. Never a pack unless the Chief directs one (unopened packs drag trade scores [L]).

## run/book.json from ~11:20 (after the dealer runs)

```json
{"offers": [
  {"card": "CHA-08", "side": "buy", "price": 30, "floor": 90, "page_closer": true, "life": 20},
  {"card": "CHA-05", "side": "buy", "price": 10, "floor": 72, "page_closer": true, "life": 20}
]}
```

- `page_closer: true` puts both on El Rastro: one of them will close the page (directives 10:18, 10:30). `life: 20`
  keeps each ≤ 20 real ticks (directive 09:46).
- `book.py` (eb36ec8) caps every bid at our value − 3 and re-reads our values every 10 ticks (e07a8c4). While both
  cards are missing the caps are 37 and 13. When one arrives, the other's value jumps and its floor binds (90 / 72);
  the book steps the bid up every 20 ticks.
- Remove the filled card's entry (the book marks it done).

## 15 s ticks [?]

- **Offer life.** On Saturday, real life = asked × tick_seconds / 60 (asked 120, lived 60). If that ratio holds on
  Sunday, offers live ¼ of what is asked. `opps` and `book.py` already scale by 60 / tick_seconds. **Check the first
  post's `expires_tick − created_tick`** and tell the Builder if it isn't what was asked.
- **Dealer deals.** 5-7 rounds; `abuela_bot` waits for each reply, so expect ~2.5-4 min per deal at 15 s, plus 10 ticks
  (2.5 min) between two conversations with the same dealer. Six open conversations per team: run Abuela and Chato in
  parallel. Eight deals ≈ 35-45 min, which fits 09:29 → ~10:15 for Abuela.

## Operator checklist, Sunday 09:00-09:35

1. **09:00** · `GET /api/clock` (open? `tick_seconds` 15?), `/api/schedule` (release and allowance hours),
   `/api/catalog` (CHA `released`?), `/api/news`, `/api/me` (cash; our CHA values 16/40/112).
2. **09:01** · `tools/daemons.sh status`. Restart `book` (`MIN_GAIN_SELL=2`, with the Sunday `CASH_FLOOR` set by
   GUARDRAIL) and `opps`. **Keep the trader stopped until Duels III ends** (directive 10:35).
3. **09:02** · Cancel Saturday asks that hold cash or cards we need. Expect cash ≈ Saturday close; +150 at ≈ 09:32.
4. **At release**, two runs in parallel (both under `uv run`, so the narrator works):
   - **Chato:** `uv run python agents/dealers/abuela_bot.py --dealer chato --cards CHA-09,CHA-10 --deals 2 --cash-floor <GUARDRAIL floor>`
   - **Abuela:** `uv run python agents/dealers/abuela_bot.py --dealer abuela --cards CHA-06,CHA-07,CHA-01,CHA-02,CHA-03,CHA-04 --deals 6 --cash-floor <GUARDRAIL floor>`
5. **First offer posted** · check `expires_tick − created_tick` (×4?).
6. **By ~11:20** · all dealer threads closed before Duels III (≈ 11:29). Log `neg_points` before and after each deal in
   team/lucas.md: expect 0 on every dealer buy.
7. **~11:20** · load the CHA-05 / CHA-08 bids into run/book.json (El Rastro, life 20).
8. **12:30** (Duels III over) · if neither has filled, buy CHA-05 from Abuela (`--cards CHA-05 --deals 1`) so CHA-08
   closes. `bargains` pages Lucas if an ask is worth ≥ 20 to us after the fee; expect **+50** on the closing team trade.
