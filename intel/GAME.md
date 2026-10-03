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
- **Addressed offers are NOT private** [V Sat 02:50]: an offer with `to` is hidden from public boards (the addressee sees it
  in `GET /api/me/offers`), but the public FEED's `offer.listed` event shows it in full: maker, `to`, give, want (35 such
  events on Friday). Anyone reading the feed sees what we bid for and whom we target: keep page-critical bids short-lived.
  Team 13's claim that only the addressee sees them is false. **Card-for-card swaps** exist (give assets, want
  cards). A venue's owner scores the value created between other teams on it: trading on a leader's venue feeds the leader
  (Team 13 lobbied every team on Sat 02:00 to trade and swap on its venue v03).
- **Clearing prices on El Rastro** [V]: common 9 (LAT 7.5), uncommon 24.5 (MAL 26, SAL 24.5, LAT 21.5), rare 70 (53-80).
  Only 5% of asks and 9% of bids filled; filled bids took a median 4 ticks.
- **Duels** [V, 30 practice duels; corrected Sat 09:48]: result = our surplus × (1 − decay)^rounds, rounds = min(our
  messages, theirs): **every duel message counts as a round, priced or not** (duel 277: 3 no-price messages each raised
  `rounds`; 278: restating the same price every tick cost 10 rounds). Silence is the only free hold; no deal = 0.
- **Round 2 (Sat)** [V]: fired at tick 160 (game hour ~2.7, not 4.0): `neg_points` 67.8 → 0 and `ladder_points` → 0 for
  every team; holdings carry over. Tick 165: grant = 150 P + a sobre_barrio pack for everyone (ours: RET-05, SAL-01,
  SAL-03). Saturday clock: game hour = wall hour (30 s ticks, 120 ticks/h).
- **Abuela on Saturday** [V, n=1]: our first deal of the day (RET-04 common) opened at 12 and closed negotiated at 9
  (worth 11): `neg_points` 0 → 0, `ladder_points` 0 → 0.014. No fixed welcome price today [L: the welcome price does not
  reset per day]. Menus Sat: Abuela common list 10, uncommon 25; Chato uncommon 26, rare 77, silver pack 150.
- **Dealer gains don't score** [V, n=2 clean windows, Sat 09:41-09:45]: Abuela RET-04 at 9 and RET-03 at 9 (worth 11
  each; collection value +22): `neg_points` 0 → 0 both times (predicted +2 each if gains counted). Dealer deals pay only
  through the ladder: Abuela commons +0.014, +0.018, +0.016 (3 deals, 12 → 9 each). The deck's Hint 1 "+4" is team trades.
- **Dealer losses score in full** [V, Sat 09:53]: RET-09 from Chato at 87 (worth 77): `neg_points` 0 → −10.0 exactly;
  ladder unchanged (4th Chato deal of ours that never moved it). His path: 97, 96, 95, 90, then FINAL 87 against our
  57 → 69 (+3 steps); Team 18 paid 86 for RET-09 at tick 206. RET-10 [V, 10:04]: first try his FINAL 91 came when our
  bid was 66 (walked, cap 88); retry: 97, 96, …, 89, FINAL 86 when our bid reached 69 → `neg_points` −10 → −19.0 (77 − 86).
  Pattern [L, n=3]: his rare final lands when our +3 steps reach ~69 (≈ 0.9 × list 77) → 86-87; at 66 it was 91.
- **Chato mirrors our step size** [V, Sat 10:07, RET-06 uncommon]: our 18 → 21 in +1 steps; his 33, 33, 32, FINAL 31
  after 4 rounds ("One peseta. That's your big move? … You moved one, I moved one. That's the last number I say").
  Friday's +1 → 28-29 protocol fails today; he finals after ~4-5 rounds whatever we do. RET uncommons go to Abuela.
- **Warm vs cold with Chato** [V, n=1 each, same card RET-06]: cold (open 18, +1, price-only text) → his 33, 33, 32, FINAL 31
  in 4 rounds, walked. Warm (open 20, +3, greeting/thanks/"for our Retiro page", Spanish mix) → his 33, 33, 33, 32, 31, then
  he ACCEPTED our 30 ("Done. 30 P.") in 5 rounds: `neg_points` −19 → −21.5 (27.5 − 30), ladder unchanged (Chato deal 5,
  still never moves the ladder). Abuela RET-08 at 22 (her 29 → 22): `neg_points` 0, ladder +0.003 (a 4th level-1 deal).
- **RET rares** [V, feed ticks 160-188]: no team pulled a RET rare from a grant pack (every sobre_barrio `best` = null);
  the only sources are Chato (rare list 77) and silver packs. Team 15 bids 59 and Team 2 9-12 for RET-09/10.

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
