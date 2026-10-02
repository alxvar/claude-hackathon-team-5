# The Bazaar: what every agent must know (stable; edit only when the rules or a measured fact change)

## Scoring (RULES.md)
- Score = Negotiating 30 + Market-making 30 + Judges 40. Each day is a round; Friday counts half; rounds are averaged. Scores are relative to the field (ours drops when others rise).
- Negotiating = duels (share of each deal's pie) + dealer ladder (share of each dealer's price range; best 3 deals per level; higher levels weigh more; a missing deal counts 0) + **value gained in trades with other teams, at our private values**.
- Market-making = Market Test efficiency (bench, every ~2 h from Saturday) + value created between other teams on our venue. Fees never count.
- Never counts: number of trades, fees earned, pack luck, gifts.

## Measured facts (kept current by the operator from metrics.md → "What each of our deals did to neg_points")
- **`neg_points` counts trades between teams at OUR private values, net of fees: selling a card scores `price − our value of that copy` (minus the fee, 5% + 1 P, when WE accept).**
- **CORRECTED 22:00: dealer purchases ABOVE our value SUBTRACT.** Measured: MAL-07 bought from Abuela at 29 (worth 17.5 to us) → `neg_points` 26.3 → 14.5 (−11.8). The −8.5 we started with came from packs bought above their value. A dealer purchase BELOW our value showed no clear gain (LAV-08 at 24, worth 32.5: ~+0.3). **Rule: never buy from a dealer above our private value, ladder deals included. Flipping dealer cards into team bids is dead (−11.5 on the buy, +5 to +8 on the sale).**
- Measured on our deals (22:00-22:20): buying from a team scores about value − price − fee (SAL-08 at 18, worth 22.5, we accepted, fee 2: +1.9); selling scores price − the copy's value when they accept (LAV-04 3rd copy at 9, worth 1.3: +7.7). One sale scored more than that: SAL-06 at 26, worth 22.5 → +6.0 instead of +3.5 (unexplained; watch the next SAL sale).
- **El Chato (level 2, 6 deals/team/hour; we had early access, open to all at hour 2.63):** sells LAV uncommons from 33, down to 31-32 after ~5 rounds (our value 32.5, so ≈0 `neg_points`; ladder only). Bids 13 for a MAL uncommon (worth 17.5) and doesn't move. Silver pack: list 150, opens 188. Rares list 77. No value-positive Chato deal found yet. **22:32: bought LAV-06 from Chato at 31 (BELOW our value 32.5) → `neg_points` 30.1 → 27.8 (−2.3) and `ladder_points` unchanged (0.064).** So dealer buys never add `neg_points`, even below value (LAV-08 at 24 → +0.3, LAV-06 at 31 → −2.3, MAL-07 at 29 → −11.8), and a Chato deal reached by proposing his own price gave no visible ladder. **Rule: no dealer buys at all unless Lucas directs one.**
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
- `agents/trader/autoflip.py`: STOPPED 22:00 (flipping loses points, see the correction above).
- `agents/trader/trade.py`: manual list / bid / accept. `agents/dealers/abuela_bot.py`: dealer negotiation (`--dealer`, `--ladder`).
- Duels: Aleks's `agents/duelist/` (not ours to run).
- Humans in the room (Lucas, Dani) can find card holders and agree trades; card owners are anonymous in the API.
