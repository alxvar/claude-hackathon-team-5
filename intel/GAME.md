# The Bazaar: what every agent must know (stable; edit only when the rules or a measured fact change)

## Scoring (RULES.md)
- Score = Negotiating 30 + Market-making 30 + Judges 40. Each day is a round; Friday counts half; rounds are averaged. Scores are relative to the field (ours drops when others rise).
- Negotiating = duels (share of each deal's pie) + dealer ladder (share of each dealer's price range; best 3 deals per level; higher levels weigh more; a missing deal counts 0) + **value gained in trades with other teams, at our private values**.
- Market-making = Market Test efficiency (bench, every ~2 h from Saturday) + value created between other teams on our venue. Fees never count.
- Never counts: number of trades, fees earned, pack luck, gifts.

## Measured facts (operator-maintained; verified Sat 00:00-01:15 by independent agents; [V] verified, [L] likely, [?] open)
- **Team trade** [V]: score = Δ(our whole collection value, incl. page bonus and unopened packs) − price − fee if WE accept.
  `parties` = [maker, taker]; only the taker pays the fee, ceil(5% × price) + 1 P per card. Being the maker saves the fee
  and the team's single accept per tick.
- **Dealer deal**: score = min(0, ΔV − price). Losses count in full [V: MAL-07 at 29 (worth 17.5) −11.8; LAV-05 sold at 5
  (worth 13) −8.0; LAV-09 at 93 (worth 91) −2.0]. Gains are clipped to 0 [L]. A dealer deal never adds `neg_points`.
- **Per-trade cap** [L, n=1]: our page-completing buy (value 99.1, paid 8 + 2) scored exactly +50.0, not 89.1. Forms that
  still fit: flat 50 · gain ≤ 5×book · gain ≤ 5×(price+fee) · value ≤ 6×book. Test: plan §4B.
- **Page bonus** [V]: 25% of the page's book (265) × our multiplier = 66.25 × m (LAV 86.1, RET 72.9, CHA 106), priced into the
  last missing card (LAV-09 read 177.1 when it was the only one missing). It scores only when a TEAM trade completes the
  page [L: Team 17 +6.25 board via a team trade; Team 10 +2.1, Team 7 +1.1, Team 12 +1.0 via Chato].
- **Unopened packs drag** [L]: each new card lowers an unopened pack's expected value, shifting a trade's score by ~1-4
  points (explains SAL-08 +1.9, SAL-06 +6.0, LAV-06 −2.3). Open packs before trading.
- **Relative score** [V]: the leader sits at the top of the scale; idle teams fall 0.07-1.7 per snapshot when others gain.
  1 `neg_point` ≈ 0.16 board points (Friday's marginal rate; [L] for Saturday).
- **El Chato** (level 2, 6 deals/team/hour) [V]:
  - Sells uncommons from 33; +1 per round → final 28-29 (Team 3); bigger early bids end at 31-32.
  - Sells rares from 97; constant +2 to +4 per round, bid just under his standing offer → 82-90 [L: one sale at 82, the
    other seven 89-93]; +1 steps give an early final at 91-93; big jumps earn ~1.
  - Buys uncommons at 13; if you open ≥ 39 and step down 2-3 he goes to a 15-16 final. Buys rares (paid 46 for LAT-09).
  - Silver pack: opens 188 (Team 8 paid 181, board −5.65). Never buy packs.
- **Abuela** (level 1, 8 deals/team/hour, 3 packs/hour) [V]: opens common 12, uncommon 29, pack 30; more rounds = lower
  (common 9-10, uncommon 21-24 after 5-7 rounds, pack 19 after 8). Each team's first deal was a fixed welcome price (17
  pack/uncommon, 7 common) [V; whether it resets each day: ?].
- **Ladder** [?]: Abuela deals moved ours (0.054 → 0.064); our 3 Chato deals did not, and no variable explains which Chato
  deals count. A deal at the dealer's opening price never counts [V, RULES]. Level 2 opened early to teams with 3
  negotiated Abuela deals [V].
- **Venues** [V]: 4 team venues exist (v01 Team 6 0.5%→0%, v02 Team 12 0%, v03 Team 13 1%, v04 Team 2 0% auto), all with 0
  trades on Friday. All 46 team trades went through El Rastro.
- **Addressed offers are private** [V Sat 02:30]: an offer with `to` doesn't appear on public boards; the addressee sees it
  in `GET /api/me/offers`. Our addressed bids don't reveal our needs. **Card-for-card swaps** exist (give assets, want
  cards). A venue's owner scores the value created between other teams on it: trading on a leader's venue feeds the leader
  (Team 13 lobbied every team on Sat 02:00 to trade and swap on its venue v03).
- **Clearing prices on El Rastro** [V]: common 9 (LAT 7.5), uncommon 24.5 (MAL 26, SAL 24.5, LAT 21.5), rare 70 (53-80).
  Only 5% of asks and 9% of bids filled; filled bids took a median 4 ticks.
- **Duels** [V, 30 practice duels]: result = our surplus × (1 − decay)^rounds, rounds = min(our priced offers, theirs);
  silence costs no decay; no deal = 0.

## Our private values (`/api/me` → affinity; every team has the same six numbers, shuffled)
Chamberí (CHA) 1.6 (released Sunday) · Lavapiés (LAV) 1.3 · El Retiro (RET) 1.1 (released Saturday) · Salamanca (SAL) 0.9 · Malasaña (MAL) 0.7 · La Latina (LAT) 0.5.
Book values: common 10, uncommon 25, rare 70, epic 180, legendary 450. Our value = book × multiplier; a 2nd copy is worth 25%, a 3rd 10%. A complete page (commons + uncommons + rares of a set) adds a 25% bonus.

## What we can do (the executors)
- El Rastro: list a card for cash, bid cash for any copy of a card, accept others' offers (1 accept per team per tick), offers addressed to one team (`to`).
- `agents/trader/loop.py`: auto-accepts El Rastro offers that gain ≥3 (buys) / ≥6 (sells into bids).
- Autoflip (archived in `archive/fri/autoflip.py`): DEAD, dealer buys above value subtract. Never restart it.
- `agents/trader/trade.py`: manual list / bid / accept. `agents/dealers/abuela_bot.py`: dealer negotiation (`--dealer`, `--ladder`).
- Duels: Aleks's `agents/duelist/` (not ours to run).
- Humans in the room (Lucas, Dani) can find card holders and agree trades; card owners are anonymous in the API.
