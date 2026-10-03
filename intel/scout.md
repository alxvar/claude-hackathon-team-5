# Scout (claude-sonnet-5-5, Sat 23:57)

## Top 3 actions now

1. **Keep SAL-11 bid 20252 (115 → t04, v15, exp tick 1565); raise only at Sunday's open, never above 125.**
   - Evidence: t04 dumps SAL, and our SAL-11 value is 162 (first copy). The directive allows ≤ 125 with a 260 floor for this buy only. Cash is 392, and CHA needs ≈ 330.
   - Ask 245 on the board (t10 sold SAL-11 to t17 at 207, tick 1296) is the wrong route.
   - Effect: about +37 to +47 neg_points if filled at 115-125 (162 − price − fee). Confidence: med. Operator does it at 09:00 via trade.py.

2. **Swap-desk match RET-09 t07 → t09 on v10 (Lucas/Dani brokers it; the matchmaker has it as the +68 VC trade).**
   - Evidence: the market-day closeout shows club pairs at +89 VC, 68 of it from this one page-finishing trade. t09 collects RET (9/10 per the directive) and also bids MAL-09/10 at 56. Market scores "real trades" (22.5 of the 30).
   - Effect: a market-making lever (no neg_points). The sim says +89 on v10 is worth ≈ 3.9-4.8 of 5. Confidence: med. This is a human job (Lucas DMs both sides at 09:00).

3. **Sunday CHA rares from the Pícaros at ≤ 54 (target 48-52), with the last CHA card bought from a team.**
   - Evidence: the Chief decision at 23:43 and dealer-lab.md say Pícaros rare accept ≤ 54. The Pícaros rare median is 55 over 1 deal. Our CHA rare value is 112 (book 70 × 1.6), so each buy at ≤ 54 sits far below value, and dealer gains clip to 0.
   - Effect: it builds toward the page (bonus 106 on CHA, scored only via a team trade finishing it, which is why the last card comes from a team, capped at +50). Ladder: Pícaros is L4, max 0.089 per deal. Confidence: med. Operator does it, ≥ 09:00 on round 3.

## What the climbing teams are doing

- **Team 18 (#2, +1.2 in 60 min)** collects RET/LAT, with 40 deals. It bought LAT-10 from Team 13 at 72 (tick 1332) and dumps LAV/MAL. Its gain comes from steady buys of its own sets, not from big trades.
- **Team 12 (#4)** is buying epics and rares: RET-11 from t06 at 216 (tick 1245), LAT-10 from t01 at 86 and from t13 at 72, and SAL-09 from t12 to t09 at 70. It has 70 deals and 29 team trades, the most among the top teams.
- **Team 6 (−2.7 in 60 min)** is selling off: RET-10 to t04 at 84, RET-03 to t10 and RET-06 to t07. It looks like a faller, not a threat.

## Threats

- **Team 10 (#1, 37.6)** leads us by 7.1. It holds v07 and is a RET/LAV collector. Any trade routed to its venue feeds it, so keep everything on v10, v15 or El Rastro.
- **Team 12 (#4, 30.4)** is 0.1 behind us and is buying RET: RET-11 at 216, plus RET-02/03 interest. It competes for RET cards and for CHA when round 3 opens.
- **Pícaros/Chato rare prices** for CHA are not in the data beyond Pícaros 55 and Chato 97. If a team bids above 54 first, the Pícaros route closes. Check the price before committing cash.
