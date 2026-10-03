# How Team 13 and Team 18 score, and what to copy (Builder, Sat 11:55)

_Sources: `data/feed.jsonl` (settlements de-duplicated by id; Friday = ticks < 159, Saturday after), `/api/dealers`
menus, the leaderboard (tick 420), our `/api/me` (11:50) and the hub's demand model (`hub.team_mult`, run 124:
**estimated** multipliers [L], ours exact). "Gain" = book × the team's multiplier − price for a buy, price − that for
a sale (fees and page bonuses left out) [L]. Opening prices exist only where the feed kept the thread messages
(mostly after tick ~70)._

## The board now [V, leaderboard tick 420]

| Team | Score | Negotiating | Market | Deals |
|---|---|---|---|---|
| t13 | 27.72 | **24.39** | 3.33 | 45 |
| t18 | 26.66 | 19.16 | 7.5 | 28 |
| us (t05) | 22.66 | 15.16 | 7.5 | 35 |

Our parts [V, /api/me]: neg_points 35.2, ladder 0.055, duels 0, bench 0.5, **mm_points −5.2** (value destroyed by
trades on our v10 stall).
Estimated multipliers [L, hub]: **t13** MAL 1.35, SAL 1.35 (both most likely 1.6), LAV 1.07, RET 0.91, LAT 0.59.
**t18** RET 1.51 (most likely 1.6), LAT 1.21, SAL 1.17, LAV 0.70, MAL 0.67. **Ours** CHA 1.6, LAV 1.3, RET 1.1,
SAL 0.9, MAL 0.7, LAT 0.5.

## 1. Dealer deals [V counts and prices; list prices from /api/dealers now]

| | Friday | Saturday | vs list (buys) | Unlocks |
|---|---|---|---|---|
| **t13** | 15: 7 Abuela buys, 6 Abuela sells, 2 Chato sells | 15: 3 Abuela buys (packs), 8 Abuela sells, 2 Chato buys, 1 Chato sell, 1 Pilar sell | **never above list**: Abuela 8 below (5 of them packs), 2 at; Chato 2 **at** list (LAV-06/07 at 26) | Chato t98 ("6 deals with abuela"); **Pilar t262 ("3 deals with chato")** |
| **t18** | 8: 6 Abuela buys, 1 Chato buy, 1 Chato sell | 8: 6 Abuela buys, 2 Chato buys | Abuela 10 below, 2 at; Chato 3 **above** (LAT-08 32, RET-09/10 86) | Chato t98 ("3 deals with abuela"); no Pilar |
| **us** | 15: 7 Abuela buys, 5 Abuela sells, 2 Chato buys, 1 Chato sell | 8: 5 Abuela buys, 3 Chato buys | Abuela 11 below, 1 above (MAL-07 29); **every Chato buy above list** (31, 93, 87, 86, 30) | Chato t98 ("6 deals with abuela"); no Pilar |

- **t13 sells its spare commons to Abuela.** 14 sales at 5-6 P: it opens at 22 and she bids 5, ending after 6-7 rounds.
  Spare copies are worth little (a 2nd copy counts 25%, values rules), so a sale at ≥ that value scores 0. It probably
  feeds the ladder [?].
- **The early unlock counts deals at list, not only below it** [L]. t13 unlocked Pilar when her level activated (tick
  262), with 4 Chato deals before then: 2 buys at exactly list (26) and 2 sales negotiated up from his opening bid (LAT-09
  39 → 46, MAL-06 13 → 15). We had 0 such deals: 5 Chato buys above list, and 1 sale at his opening bid (13, which never
  counts, RULES).
  - This refines GAME.md's "only below-list deals count" [L] to **at or below list**.
  - The reason says 3, not 4: which deal didn't count is [?].
  - Level 2 [?]: t18's "3" matches its 3 card buys before tick 98 with its 2 packs left out, and t13's "6" matches its 5
    card buys plus 1 sale. Our "6" doesn't fit the same rule cleanly (3 card buys and 4 sales, 2 of them at her
    opening bid).

## 2. Team trades [V prices; gains L at hub multipliers]

| | Friday | Saturday | Pattern |
|---|---|---|---|
| **t13** | 9 (6 buys, 3 sells), est. **+122** | 6 (2 buys, 4 sells), est. +22 | **Buys its high sets** (MAL/SAL ≈ 1.35) at clearing: SAL-09 at 74 (+20), SAL-10 at 70 (+24), MAL-10 at 65 (+30, t331), MAL commons at 6 (+7.5 each). **Sells its low set** (LAT 0.59): LAT-09 at 65 (+24), LAT-01+07 at 40 (+19). All on El Rastro except two small sales on t12's v02. |
| **t18** | 9 (2 buys, 7 sells), est. −2 | 3, est. −31 | Sells commons at ~9 for roughly nothing; bought RET-02 at **49** from t02 (−34 at book × 1.51; with RET's page bonus it was likely its page close). It scores on pages: RET from Chato (RET-09/10 at 86) plus Abuela. |
| **us** | 9 (3 buys, 6 sells), est. +40 + the LAV page (+50) | 3, est. −9 + the RET page (+50) | Pages first. Small sales into bids. |

**What t13 does that we don't:** multiplier arbitrage, trade by trade. It buys cards of a set it values ~1.35-1.6×
at clearing, and sells cards of a set it values ~0.6× at clearing: +7 to +30 per trade. Its +122 on Friday came from
nine trades. It never pays a dealer above list.

## 3. Venues and value created [V]

- t13 opened **v03** (board, 1% fee) at tick 129: **0 trades** on it in the feed. t18 has its **v18** stall (3%,
  auto): 0 trades. Market: t13 3.33, t18 7.5.
- Our **v10** (0% since tick 230): 2 trades by other teams. t10 → t01 MAL-07 at 14 (+5.0 value created, est.) and
  t10 → t15 SAL-07 at 26 (−2.8 est.). Our mm_points −5.2 [V] says value created on our stall is negative overall.
- **Neither leader scores on venues.** t13 leads on negotiating alone; the market leaders are t10 (12.5) and t12 (11.74).

## 4. The 3 highest-value plays we're not making

1. **Sunday: buy CHA from teams, not dealers** [L].
   - Why: a dealer buy below our value scores 0 (gains clipped). A team buy scores value − price (cap 50). At
     clearing, each CHA card from a team is worth **+6 (common), +15 (uncommon), +42 (rare)**, against 0 from Abuela or
     Chato. This is t13's engine applied to our 1.6×.
   - Expected: **+60 to +160 neg_points** (≈ +10-25 board at ~0.16/pt [L]) if teams sell, on top of the +50 page close.
   - Cost: the same cash as the dealer route.
   - Risk: supply (minted 0; teams pull CHA from packs or buy from dealers first).
   - **Changes intel/cha-plan.md:** post team bids at ~clearing (common 9-10, uncommon 24-25, rare 70-80) on El Rastro
     and v07 from the release, and use Abuela and Chato only as a timed fallback (rares at ~10:00, the rest by ~11:00).
2. **Sell our low-multiplier cards at clearing, to non-top-4 collectors** [L].
   - We hold LAT (0.5), MAL (0.7) and spare SAL/LAT copies. At clearing (common 9, uncommon 24.5) that is **≈ +67
     neg_points (≈ +10 board)** for the lot, 0 cash.
   - Today's book prices several **below clearing**: LAT-04 ×2 at 4, SAL-02 at 4, LAV-03 at 5, against ~9. Raising
     those to 8-9 adds ≈ +15.
   - The trader (taker) needs **min-gain-sell 6**. A collector's bid of 9 for a spare LAT-04 (worth 1.2) nets
     9 − 2 fee − 1.2 = 5.8, so it is refused: a bar of 3 for low-multiplier spares would take it.
   - Constraint: fills (5-9% of asks fill [V Friday]), and the collectors rule (cde494b).
3. **Never pay a dealer above list; buy at list** [L, n=1 for Pilar].
   - t13 got Pilar early with at-list Chato buys. Every one of our Chato buys was above list (31, 93, 87, 86, 30) and
     earned no ladder or unlock.
   - Expected: small. Ladder 0.055 so far; Pilar opens to all at ≈ 12:20 anyway.
   - Cost: 0, and it saves the above-list premium (our 5 Chato buys paid 44 P over list in all, and 0 ladder).
   - Apply it to Sunday's CHA rares: bid Chato **at 77** (list) before paying more.

**Not available today:** epics and legendaries. None has traded, been pulled as a pack's best card, or been listed
in the feed; the only sign is a 88 P bid by t12 for SAL-11 (tick 105). `bargains` pages Lucas if one shows up below
value − 20 (after the fee).
