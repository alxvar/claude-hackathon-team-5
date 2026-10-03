# Scout (claude-sonnet-5-5, Sun 00:23)

## Top 3 actions now

1. **Cancel SAL-11 bid 20252 (115 → t04) at the first tick, as the 00:50 GUARDRAIL says. Executor: operator via `trade.py`.**
   - Evidence: it is worth about +0.2 pts per 115 P versus about 0.7 per 100 P for MAL. t04 is #11 (25.1), so it is not a leader we would feed. It expires at tick 1565 anyway.
   - Effect: frees 115 P of our 392 cash for CHA and MAL. SAL-11 would have been our first copy, valued 162, and is skipped on purpose.
   - Confidence: high.

2. **Take t09's MAL-09 and MAL-10 bids, 56 P each (offers 20251 and 19719), only if we hold the card. Check holdings first.**
   - Evidence: metrics list t09 bidding 56 P for each; MAL-09 and MAL-10 are not in our holdings. Our MAL value is 0.7× (rare ≈ 49), so selling at 56 is above value if we do own them. The Chief's directive keeps MAL-08 as never-sell.
   - Do not sell MAL cards we need for the MAL close.
   - Effect: team trade gain ≈ +7 each if we have them, otherwise nothing. t09 is #16 (23.3), so we are not feeding a leader.
   - Confidence: low, because ownership is unconfirmed and the MAL close may need them.

3. **At 09:00 run the Sunday CHA order from intel/dealer-lab.md §FAST-START. Executor: operator with `abuela_bot.py --dealer`.**
   - Evidence: the 00:25 Sunday settings are Pícaros CHA rare target 48-52 and accept ≤ 54 (62 only for the last card), and cash is 392 against a CHA need of 242-384 P by case.
   - Effect: CHA page at 1.6× is worth +3.2-5.6 final [L]. Per-card dealer buys score 0 at or below our value.
   - Confidence: med.

## What the climbing teams are doing

- **Team 18 (#2, 31.3, +1.2 over 60 min).** It collects RET/LAT. It bought LAT-10 from t13 at 72 (tick 1332), the only real mover in the top 3 and it is feeding off cheap rares. It is a top-4 team, so we never feed it.
- **Team 12 (#4, 30.4).** It has 70 deals and 29 team trades. It bought RET-11 at 216 from t06 (tick 1245), LAT-10 at 86 from t01 and LAV-08 at 14 from t08. It is paying above book for epics and rares, so an epic sale to it must clear that price.
- **Team 10 (#1, 37.6, −0.3).** It is flat to falling and has 467 listings. It still takes MAL-11 at 195 and sells SAL-11 at 207. Its sales to t17 and t09 suggest a leader dumping lower-multiplier cards.
- **Team 6 (#6, −2.7 over 60 min).** It is selling RET rares to t04 at 84 and RET-06 to t07 at 30, which drains its own score.

## Threats

- **Team 18 is closing on us.** It is +1.2 over 60 min against our −0.4, with 31.3 against our 30.5. Falling to #4 costs rank, so a CHA finish matters.
- **Team 12 is at 30.4, about 0.1 behind us.** It is a top-4 team and is buying RET and LAT rares.
- **Dealers close about 14:00, and dealer prices may move against us.** RET-11 sale to Pilar needs ≥ 198 and round 3 only; Sunday ticks run at 15 s. Do not sell RET-11 below 198.
