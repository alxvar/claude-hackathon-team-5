# The Bazaar: what every agent must know (stable; edit only when the rules or a measured fact change)

## Scoring (RULES.md)
- Score = Negotiating 30 + Market-making 30 + Judges 40. Each day is a round; Friday counts half; rounds are averaged. Scores are relative to the field (ours drops when others rise).
- Negotiating = duels (share of each deal's pie) + dealer ladder (share of each dealer's price range; best 3 deals per level; higher levels weigh more; a missing deal counts 0) + **value gained in trades with other teams, at our private values**.
- Market-making = Market Test efficiency (bench, every ~2 h from Saturday) + value created between other teams on our venue. Fees never count.
- Never counts: number of trades, fees earned, pack luck, gifts.

## Measured facts (LOG.md findings, verified on our own trades)
- **`neg_points` = sum over trades between teams of (value received − value given) at OUR private values, net of fees.** Selling a card scores `price − our value of that copy` (minus the fee, 5% + 1 P, when WE accept). What we paid for the card never enters: a dealer purchase neither scores nor subtracts.
- Dealer deals barely move `neg_points`; they feed the ladder only.
- Every trade between teams also scores for the counterparty. Price sales near the BUYER's value; prefer counterparties below us.
- Big jumps on the leaderboard (+8 to +15) came from single rare trades between teams (65-80 P).
- Good bids get filled by other teams within minutes. Speed beats price on purchases.
- Abuela: opens commons ~12, uncommons ~29, packs 30 (sometimes low: 17 or 7, and then she doesn't move); ends ~73-75% of a high opening. Limits: 8 deals/team/hour, 3 packs/hour.

## Our private values (`/api/me` → affinity; every team has the same six numbers, shuffled)
Chamberí (CHA) 1.6 (released Sunday) · Lavapiés (LAV) 1.3 · El Retiro (RET) 1.1 (released Saturday) · Salamanca (SAL) 0.9 · Malasaña (MAL) 0.7 · La Latina (LAT) 0.5.
Book values: common 10, uncommon 25, rare 70, epic 180, legendary 450. Our value = book × multiplier; a 2nd copy is worth 25%, a 3rd 10%. A complete page (commons + uncommons + rares of a set) adds a 25% bonus.

## What we can do (the executors)
- El Rastro: list a card for cash, bid cash for any copy of a card, accept others' offers (1 accept per team per tick), offers addressed to one team (`to`).
- `agents/trader/loop.py`: auto-accepts El Rastro offers that gain ≥3 (buys) / ≥6 (sells into bids).
- `agents/trader/autoflip.py`: fills other teams' bids with cards bought from Abuela when the sale scores ≥8.
- `agents/trader/trade.py`: manual list / bid / accept. `agents/dealers/abuela_bot.py`: dealer negotiation (`--dealer`, `--ladder`).
- Duels: Aleks's `agents/duelist/` (not ours to run).
- Humans in the room (Lucas, Dani) can find card holders and agree trades; card owners are anonymous in the API.
