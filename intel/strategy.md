# Strategist (claude-opus-5-5, Sat 20:30)

## How the points really work
- **Weights.** Board = Neg 30 + MM 30 + Judges 40, all relative to the field. Rounds weigh Fri 0.5, Sat 1, Sun 1, so **Sunday is 40% of the game**.
  - Round 2 resets were [V] for neg_points (67.8 → 0) and the ladder. Holdings carried over.
  - Round 3 starts at game hour 16.65, after Sunday opens at 13.857. So Sunday 13.857-16.65, including the hard bench at 14.65 and the bench at 15.0, is still round 2 [L, schedule].
- **Neg (our 119.1, flat since tick 988).**
  - Team trades score ΔV − price − taker fee, capped at 50 per trade.
  - Dealer deals score min(0, ·).
  - The ladder is capped for us: board flat across 0.373 → 0.437.
  - Flags are capped at ≈3 scored per team: net +20, and the 4th clean flag scored 0.
  - On Saturday, **every neg lever except team trades is spent**.
- **MM.**
  - Bench: we sit at the stall level (market 7.5). Leaders are at 9.15-12.5.
  - Value created (VC) on v10 is NET. One positive trade took us 7.5 → 12.5 (+5). One negative trade (t15 dumping SAL) took us to −5.2.
  - The +5 cap is [L, 2 trades].
  - **VC is the cheapest board point left today**: gap to #1 t10 is 2.4, and one good v10 trade is ≈ +5.
- **Duels.** 13.93 so far. Score is surplus × (1 − decay)^rounds, and every message counts as a round. Duels III decay is 10% over 12 ticks.
- **Judges, 40.** Untouched by the board. Our measured-fact discipline (GAME.md [V]/[L], predicted vs measured) is the story.

## Our winning strategy
1. **Tonight: win MM, not Neg.**
   - Get 1-2 positive-VC v10 trades between non-rivals, then defend against negative ones.
   - Settle the rebate as a ≥0 trade.
   - Run Duels II.
2. **Sunday: own Chamberí.** CHA is 1.6× for us, the field max. Every other team values it at 0.5-1.3, so we outbid everyone and still gain.
   - Team buys at Friday clearing prices: common 9 vs 16 (+7), uncommon 24.5 vs 40 (+15), rare 70 vs 112 (+42).
   - Last common via team trade: worth ≈122 with the 106 bonus, so it books the +50 cap.
   - Full page ≈ 35 + 45 + 84 + cap. Cost ≈ 260 P against 120 + 150 grant = 270.
   - Dealer CHA buys at ≤ value score 0 and fill gaps.
3. **Sunday: rebuild the ladder from zero** (assuming the round 2 reset repeats). We are level 5. Use L4 Picaros and L5 Banco (heaviest), 3 deals each, only sells ≥ value or buys ≤ value.
4. **Stop:**
   - Dealer deals tonight.
   - Egg hunting.
   - 40-P fantasy asks (MAL-02 → t08: t08's uncommon median is 22.5).
   - Selling any LAV/RET/SAL page card: it books the bonus as a loss.
   - Feeding t10, t06, t03, t14, t18.

## Levers nobody is using yet
- **CHA at 1.6 is uncontested.** It isn't released yet, and multipliers are shuffled, so nobody else has 1.6. Post bids for all 10 CHA cards at release, as maker, before packs get opened elsewhere.
- **Open sobre_plata at the CHA release, before the first CHA trade.** Pack drag measured −2.4 per card. Ten CHA trades with it unopened lose ≈ −24, and opening it may pull CHA cards for free (luck never counts).
- **Our duplicates are Sunday ladder fodder.**
  - LAV-02 ×2 spares are worth 1.3 each. Picaros bought a common at 4 tonight (4 > 1.3), so a sale is 0 neg plus a ladder share.
  - Keep them for round 3 instead of selling at 6 tonight.
- **Flags may reset with round 3** [?]. The cap held within round 2. If it resets, that is up to ≈ +30 neg, the size of one page close, for free.
- **Round 2 runs into Sunday morning** [L]. Trades at 13.857-16.65 likely count for Saturday's round. Use that window for positive spare sales and v10 VC, never losses.

## Plan, anchored to the schedule
| When | Who | Move | Impact |
|---|---|---|---|
| Resume → 11.65 | Dani + Market | Pair 1-2 v10 trades: seller dumps the set, buyer collects it and lacks the card (t13 → t07/t09/t16). No t10/t06/t03/t14/t18. Market reads mm_points after each fill. | ≈ +5 board [L] |
| Resume | Operator | Cancel 17650 (MAL-02 → t08 at 40). Keep LAV-03/04 at 6, MAL-03 at 9, MAL-08 at 20 → t01. Re-address MAL-08 to t17 or t13 at 20 if unfilled. | +2 to +8 neg |
| 11.65 Duels II | Aleks | Days in code. Full packages. Close by sending the rival's own price at ≤4 ticks left. | duel share |
| 13.0 bench | Market | v10 open and supervised. Record bench_offers. | bench ≥ stall |
| 22:45 | Operator | Rebate (≤30 P): buy on v15 (fee 0) a card we lack worth ≥ the owed amount, Dani confirms holder. Else cap the price at our value. | ≈0 instead of −15 |
| Sun 13.857 | Operator | Read /api/clock and neg_points (round-2 carry test). Bench 14.65 hard + 15.0 supervised. | round-2 MM |
| 16.649 CHA release | Operator | Open sobre_plata. Then post maker bids for all CHA cards at 9/24/70, on El Rastro or v15. Dani pitches pack-openers. | sets up +160ish |
| 16.65 round 3 | Operator | Ladder: 3 deals each at L5/L4/L3/L2/L1, below list, stepping −2/−3, never the opening price, ≤/≥ value only. | fresh ladder |
| 16.65+ | Operator | One clean bait-and-switch flag (flag-reset test). | +10 or 0 |
| 17, 19 benches | Market | Supervised venue. Pair 1-2 positive-VC v10 trades again (round 3 VC). | ≈ +5 board [L] |
| 18.65 Duels III | Aleks | ≤2 exchanges at 10% decay. | duel share |
| Before 21.65 | Operator | Last CHA common via team trade (cap 50). Cash → 0 into non-negative buys by the directive's 14:00 limit. | +50 |
| All Sunday | Lucas + Dani | Pitch for the 40 judge points: measured-fact table, decision timeline, VC story. | judges |

## Hypotheses to test
1. **Neg, ladder and flag cap reset at round 3.** Test: one flag after 16.65. Metric: neg_points +10 within 90 s.
2. **Sunday pre-16.65 trades count in round 2.** Test: read neg_points at 13.857 and after the first maker fill. Metric: it continues from 119.1 rather than restarting at 0.
3. **VC cap is +5 per round and NET.** Test: mm_points after each v10 fill tonight. Metric: whether the second fill adds anything.
4. **Cap is 5×book, not flat 50.** Test: the first CHA uncommon or rare bought from a team > 50 below value. Metric: whether the score exceeds 50. If yes, make the page-closer an uncommon (cap 125) instead of a common.
5. **Dealer packs carry CHA after release.** Test: open sobre_plata at 16.649 and check the album. Metric: CHA cards pulled. Also /api/me/value of sobre_barrio vs Abuela's price; buy only if value ≥ price (0 neg).
6. **A board broker beats auto on the hard bench.** Test: replay recorded bench_offers, matching all crossing pairs per tick. Metric: efficiency ≥ stall + 2 pp before switching mechanism.
7. **"Payday, tips"** changes something. Test: Chief reads the announcement. Metric: Market re-scores v10 within 10 min (18:40 contingency).
