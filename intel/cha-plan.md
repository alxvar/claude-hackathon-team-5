# Sunday: the Chamberí (CHA) page (Builder, Sat 11:20; facts from the live API at 11:13)

**Goal:** complete the CHA page Sunday morning: 9 cards from dealers at ≤ our value (each scores 0, loses nothing), the
last card from a team (+50, the per-trade cap). Our multiplier on CHA is the highest of our six (1.6), so dealer list
prices sit well below our values and no dealer buy here should lose points.

## The set [V, /api/catalog + /api/me/value]

| Cards | Rarity | Book | Print run | Our value | On the page |
|---|---|---|---|---|---|
| CHA-01..05 | common | 10 | 300 | **16** each | yes |
| CHA-06..08 | uncommon | 25 | 90 | **40** each | yes |
| CHA-09, 10 | rare | 70 | 30 | **112** each | yes |
| CHA-11 | epic | 180 | 9 | 288 | no |
| CHA-12 | legendary | 450 | 3 | 720 | no |

Page bonus = 25% × 265 (page book) × 1.6 = **106** [V, GAME.md], priced into whichever card is last missing: that
card is worth its value + 106 to us (common 122, uncommon 146, rare 218). None is minted yet (`minted: 0`).

## When [mixed: check at 09:00]

- Saturday closes at hour 16.161 (23:00). **Sunday opens at the same hour 16.161 at 09:00, 15 s ticks** [V, /api/clock + /api/schedule].
- On the schedule, after the open: **CHA released at 16.65, round 3 starts at 16.65, the Sunday allowance (+150 P for
  everyone) at 16.7** [V]. If the game hour keeps pace with the wall clock on Sunday (as on Saturday, 30 s of game per
  30 s tick) that is **≈ 09:29 for the release, ≈ 09:32 for the grant** [L]. The catalog says CHA `"release": "sun+0h"`,
  which reads as 09:00: **[?] 09:00 or ≈ 09:29: read /api/catalog `released` at 09:00 and every few minutes after.**
- Later on Sunday: Duels III at 18.65 (≈ 11:29), **all dealers close at 21.65 (≈ 14:29)**, the final duels at 21.65,
  doors close 22.161 (15:00) [V schedule; wall times L]. All dealer buying must be done well before ~14:29.

## Sources and expected prices

| Cards | Source | Menu [V, /api/dealers] | Expected price [from Saturday, GAME.md] | Score |
|---|---|---|---|---|
| CHA-01..05 | Abuela | commons of released sets, list 10; 8 deals/team/hour | opens ~12, ends **9-10** after 5-8 rounds | 0 each (price < 16) |
| CHA-06..08 | Abuela (or Chato) | uncommons, list 25 (Chato 26); Chato 6 deals/team/hour | Abuela opens ~29, ends **21-24**; Chato finals ~31 | 0 each (< 40) |
| CHA-09, 10 | Chato | rares of released sets, list 77; 6 deals/team/hour | opens 97, +2-4 per round, finals **82-91** | 0 each (< 112) |
| The last card | a team | bids on v07 / El Rastro, addressed if we know a holder | any price up to value + 106 − 50 still scores the full +50 | **+50** (cap) |

[?] Whether Abuela and Chato have CHA stock at release, and how many copies (rares print 30 across 18 teams), is
unknown. Teams may also pull CHA from packs [?: which sets a pack draws from isn't in the catalog].
**Doña Pilar** buys uncommons/rares/epics only (also of released sets) and sells gold packs (list 420): no CHA source.

## Cash [V now; L ahead]

- Now (11:13): **114 P**. Sunday grant: **+150 P** at ≈ 09:32. Saturday income still to come: the maker book (asks on
  v07) and SAL-08 to Doña Pilar in her "Salamanca fever" (25% over book, hour 9.15-11.15 ≈ 15:58-17:58 today [L]):
  ~31 P for SAL-08 (worth 22.5 to us: scores 0). She buys no commons.
- **Page cost at Saturday's dealer prices:** commons 5 × ~9.5 = 48 · uncommons 3 × ~23 = 69 · rares 2 × ~87 = 174 ·
  **≈ 290 P**, minus the dealer price of the card we leave for a team, plus what that team asks (common ~15-30 P,
  uncommon ~40-60 P [L]).
- So we need **≈ 300 P by ~10:30 Sunday**: 114 + 150 = 264 is short by ~40 P. **Hold cash on Saturday evening**:
  every P spent after now must leave ≥ ~150 P at the close, or the rares wait for team sales. Cash floor: 100 today,
  **0 by Sunday 14:00** (GUARDRAIL 02:20).

## Order

1. **Rares first** (scarcest, print 30): CHA-09 and CHA-10 from Chato at release, cap 100 each (value 112; never above
   value: dealer losses count in full).
2. Uncommons, then commons, from Abuela (Chato for uncommons if Abuela has none), caps at value − 3 (37 / 13).
3. **The last card from a team.** Which one to leave:
   - **an uncommon** (worth 146 as the last card): if the cap is flat 50, any price ≤ 96 scores +50; if the cap is 5×book (125), it
     scores more. Closing on an uncommon is the test that **separates flat-50 from 5×book** [GAME.md open question].
     Harder to source: uncommons print 90.
   - **a common** (worth 122 last): easier (print 300, more teams pull them), but 5×book = 50 = flat 50: no test.
   - Recommendation [L]: leave **CHA-08** (an uncommon) last; if no team offers one by ~12:30, buy it from Abuela and
     leave a common last instead (bid up to 72 for it: still +50).
4. Never a pack (packs drag the score until opened) unless the Chief directs one.

## run/book.json at 09:00

[?] Whether the server accepts a bid for an unreleased card is unknown: try one at 09:00, else load at release.

```json
{"offers": [
  {"card": "CHA-08", "side": "buy", "price": 40, "floor": 96, "venue": "v07"},
  {"card": "CHA-09", "side": "buy", "price": 70, "floor": 109, "venue": "v07"},
  {"card": "CHA-10", "side": "buy", "price": 70, "floor": 109, "venue": "v07"}
]}
```

`book.py` caps every bid at our value − 3: CHA-08 bids 37 while other CHA cards are missing; once it is the last one
its value reads 146, so the cap is 143 and the book's own floor 96 binds. `book.py` re-reads our values every 10 ticks
(e07a8c4) so the cap follows. Rares as team bids are a fallback to Chato, not a replacement.

## 15 s ticks [?]

- Offer life: on Saturday the server counted `expires_in_ticks` in 60 s units (asked 120 → 60 real ticks). On Sunday
  that would be ×4. `opps` and `book.py` already scale by 60 / tick_seconds: **check the first post's
  `expires_tick − created_tick`** and tell the Builder if it isn't what was asked.
- Dealer rounds: 5-8 rounds per deal at 15 s ≈ 1.5-2 min; `abuela_bot` waits 10 ticks (2.5 min) between conversations
  with the same dealer. Six open conversations per team: run Abuela and Chato in parallel.

## Operator checklist, Sunday 09:00-09:15

1. 09:00 · `GET /api/clock` (open? `tick_seconds` 15?), `/api/schedule` (CHA release and grant hours), `/api/catalog`
   (CHA `released`?), `/api/news` (any CHA rumour), `/api/me` (cash, our CHA values: 16/40/112).
2. 09:01 · Restart `book`, `opps`, `trader` if the night stopped them (`tools/daemons.sh status`); `MIN_GAIN_SELL=2` for book.
3. 09:02 · Cancel Saturday's stale asks that hold cash or cards we need; confirm cash ≥ ~260 after the grant (≈ 09:32).
4. 09:03 · Post the first `book.json` bid (or wait for the release); check `expires_tick − created_tick` on it (×4?).
5. At release · Chato: CHA-09, then CHA-10 (the Operator's `chato_steady.py`, cap 100). Abuela in parallel:
   CHA-01..05, CHA-06, CHA-07 (`uv run python agents/dealers/abuela_bot.py`, narrator on; caps 13 / 37).
6. Keep CHA-08 for a team: bid on v07 + El Rastro; `bargains` pages Lucas if anyone asks ≤ value − 20.
7. Before 11:29 (Duels III): the arbiter yields our accept to scored duels; schedule dealer accepts around duel waves.
8. Log each deal's `neg_points` before/after (expect 0 for every dealer buy, +50 on the last team trade) in team/lucas.md.
