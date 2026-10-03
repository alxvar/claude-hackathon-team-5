# Scout (claude-sonnet-5-5, Sun 01:39)

## Top 3 actions now

1. **Check the Sunday 09:00 clock, schedule and reset before any trade (Operator, with Dani at the desk).**
   - Evidence: the game is closed until Sunday 09:00 (tick 1445). Our open offers 19979 (LAV-03 → t04 at 6) and 19981 (LAV-04 → t01 at 6) expire at tick 1455. Our spare LAV-03/04 are worth 3.2 each, so 6 is a gain.
   - Effect: this is the Sunday checklist (`intel/dealer-lab.md` §4). The reset check matters because Saturday's round-2 reset zeroed `neg_points` (67.8 → 0). We hold 119.1 now.
   - Confidence: high.

2. **Execute the CHA fast start at the first tick of round 3 (Operator: `run/cha_book.json`, Pícaros threads with `--offer-only`).**
   - CHA is worth 1.6× to us, so CHA rares are worth 112 against dealer prices of about 55-90. Directive 00:55: the Pícaros rares in parallel with capped public bids (SAL-09 29/30 and SAL-11 9/9 print runs are running out).
   - Public bids stay capped at the dealer accept price (rares ≤ 54, uncommons ≤ 22, commons ≤ 9). Open the silver pack right after the CHA release.
   - Evidence: the last card of a page is worth at most 50 + price; the Saturday SAL close was +40.4 at 28 P from t08.
   - Effect: the CHA page is the biggest remaining lever; neg_points per card are value − price at ≤ our value. Cash is 392, and the plan sets a 464 floor (CHA 288 + MAL 126 + reserve), so the trader is sells-only until 09:00.
   - Confidence: med.

3. **Sell spares OPEN on a non-rival member's venue, and list the fodder (Operator via `trade.py`).**
   - Evidence: open asks fill about 10× more than addressed ones (3.5% vs 0.3%). Current El Rastro asks and bids:
     - t16 bids 18 for RET-06 (we hold three at 100.4, so no sale).
     - t08 bids 5 for LAT-08.
     - t08 bids 5 for RET-02 (our value is 83.9, so no sale).
   - Spares worth selling (value, 1.3-7, to sell ≥ 6): LAV-02 (three at 1.3), LAV-03/04 (3.2), MAL commons (7), LAT-03/04 (5). Keep MAL-01..05 until the MAL page decision.
   - Effect: small, about +1-3 neg_points. Fodder buys stay on the directive's price limits only.
   - Confidence: low-med.

## What the climbing teams are doing

- **Team 18 (#2, +0.8 per 30 ticks)** collects RET/LAT. It bought LAT-10 from t13 at 72 (tick 1332). That is a rare bought below the ~86 other teams paid for the same card, so it is buying scarce cards under market.
- **Team 12 (#4 on the board, Δ +0.4)** is the heaviest LAT/RET buyer: LAT×8 in the trades table, LAT-10 at 86 (tick 1304), LAT-06 at 20, RET-11 at 216 (tick 1245), and LAV-08 at 14 from t08 (tick 1420). It is also a collector at epic prices.
- **Team 10 (#1, 37.6)** has 62 deals and 467 listings. It sells epics at 195-207 (MAL-11 to t10 at 195, SAL-11 to t17 at 207) and moves commons at 8-10 (RET-03 at 8 to t06, tick 1392). It is a volume maker, and we should not feed it.

## Threats

- **Team 10's lead is 7.1 points** (37.6 vs our 30.5), and its venue earns on trades between other teams. Do not route club or fodder trades through v10 beyond the directive's 2-of-3 split.
- **Team 18 (31.3) and Team 12 (30.4)** are within 1 point of us. Any page closer we sell them is a feed; the RET-09 t07 → t09 closer is not ours to sell.
- **RET epic and rare prices are moving up:** RET-11 sold at 216, RET-10 at 84. Our RET-11 is worth 198 to us, so per the directive sell only at ≥ 198 to Pilar; the 216 clearing price suggests Pilar's price may exceed that, but this is not in the data.
