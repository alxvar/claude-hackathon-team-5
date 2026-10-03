# Scout (claude-sonnet-5-5, Sat 19:13)

## Top 3 actions now

1. **Sell MAL-08 → t01 at 24 (offer 16001, v15, live to tick 1109). Operator keeps it live and lets it fill; do not reprice.**
   - Evidence: the card is worth 17.5 to us, so a fill gains +6.5 P cash. Team trade scores are positive and we are the maker, so no fee. t01 is #12 at 24.1, well below us at 31.7. t01 collects MAL and has 4 MAL buys.
   - Effect: small positive neg_points, at most about +6.5 if the gain counts at ΔV (the exact amount is not in the data). The ladder is capped, so no ladder effect.
   - Confidence: med.

2. **Push the v10 value-created trades for the market gap. The Operator keeps 15872 (MAL-03 → t09 at 9) and 15991 (LAV-03 → t09 at 6) live. Dani asks t09 in person to accept.**
   - Evidence: the 17:40 directive names v10 value created as the only lever for the market gap. The 15872 and 15991 offers go to t09, which is #17 at 20.1 and not a rival. t09 has 3 MAL buys and 1 LAV buy.
   - Effect: positive market-making only if the buyer's value exceeds the seller's. This is not in the data for t09's MAL-03 and LAV-03. 15872 is not on v10 per the data; the venue for either offer is not shown, so Dani must check it first.
   - Confidence: low-med.

3. **Honour the DENY rule: the Chief or Analyst watches the top-3 rivals (t06, t10, t14). If the Chief posts a "DENY <card> <offer id>" line, the Operator runs deny.py (cap 35 P incl. fee, cash ≥ 85, team seller only).**
   - Evidence: the GUARDRAIL at 19:05 allows this. We are #1 at 31.7 with Team 6 at 31.6 and Team 10 at 31.6, a gap of 0.1, so one rival page close (≈ +2.4 board) would pass us.
   - Effect: it protects the lead. The cost is about −1 board at 30 P.
   - Confidence: med. No DENY line exists yet.

## What the climbing teams are doing
- **Team 10** (+3.9 in 60 min, 12 team trades) buys RET-03 from t06 at 12 (tick 1033). It collects LAV/RET and holds Level 5 via 5 Pilar deals. It is allied with t01, so watch t01 ↔ t10 trades on t01's venue.
- **Team 18** (+2.4 in 60 min, +0.9 in 15 min) collects RET/SAL and has only 36 deals. Its gains come from a few well-chosen cards, not volume.
- **Team 12** (+1.6 in 15 min, 57 deals) is buying RET/MAL. It paid 84 for RET-09 from t06 at tick 895.
- **Team 16** is consolidating RET. It bought RET-08, RET-05 and RET-07 from t15 at 13, 5 and 13 (ticks 1022-1023). It also bid for RET-06 at 13 and RET-01/02/03 at 4. It is #7 at 27.4, so it is not a rival, but it may soak up our RET spares.

## Threats
- **Lead is 0.1.** t06 and t10 are tied at 31.6 and t14 is at 31.3. We are flat at +0.0 over 15 min, while t18 (+0.9) and t12 (+1.6) are climbing. The ladder is capped and flags are spent, so only team trades, v10 and Duels II remain.
- **t07 bids 38 P for RET-09 (offer 16030).** We hold RET-09 at 149.9 and RET-10 at 149.9, so we do not sell. It signals demand for RET rares. Pilar buys rares at 79 and Pícaros at 56, so no dealer sale of a rare passes our value.
- **Level 5 (Don Ernesto, sobre_oro 546) is open to rivals** (t08, t10, t14, t15, t16 all unlocked). Never buy a pack. Packs drag the unopened-pack value, and Team 8's silver pack cost −5.65 board.
