# Scout (claude-sonnet-5-5, Sat 16:25)

## Top 3 actions now
1. **Sell page-closer-free spares to Team 7 (#17 per rival profile, ~10 below us)** — Operator via `trade.py`/book, after `tools/policy.py can-give <REF>`. Candidates: LAV-02 (YES per can-give), MAL-06 (YES). Other spares (LAV-03/04, RET-04, SAL-01) are NO per policy. Price ~9.5 (Team 7's median is c 9.5, an estimate). Evidence: the rival table shows +4.3 for LAV-02 against our value 3.2. Caveat: Team 7 collects RET/LAV/LAT, so LAV-02 could close its page. Check progress first, and sell only if it is not a closer or the gap is ≥ 6. Effect: about +4 neg_points each. Confidence: low-med.
2. **Keep the Team 10 bids and addressed asks alive, and answer t15 and t16 asks** — Operator. Bids 10569 (SAL-07 20), 10570 (MAL-08 15) and 10572 (LAT-02 3) expire at tick 772. Asks 10959 and 11046 (MAL-02/05 at 9 to t15) and 10653 and 10885 (SAL at 11 to t16) are live. t16 shows bids RET-07/08 at 14, but we hold RET-06/07/08 at 100.4 each, so do not sell them. The recent fills (MAL-01 at 5: +2.0; SAL-04/RET-04 at 0 from t08: +6.2) show small team trades pay. Effect: +2 to +6 neg_points per fill. Confidence: med.
3. **Place a dealer sale at level 3 (Pilar) while she pays above our value** — Operator via `abuela_bot.py --dealer pilar`. Sell MAL-09 (value 49) only if she pays ≥ 49. Her rare median is 69 over 3 sales. Her uncommon median is 18, so MAL-06 (17.5) at ≥ 18 costs nothing. Evidence: the last 3 Pilar sells moved the ladder 0.072 → 0.181 → 0.200. Step −2/−3 and let her climb. Expected: +0.01 to +0.04 ladder (≈ +0.33 board per 0.01). Confidence: med for MAL-06, low for MAL-09 (Lucas is already offering it to Team 15 at 70 P: check the reservation first).

## What the climbing teams are doing
- **Team 1 (+3.3/15 min, #5) and Team 16 (+3.3, #10):** no specific trades of theirs in the metrics explain it. Team 16 bought LAT-09 for 88 P (t16→t03, tick 724) and RET-06 at 14 (t12→t16). Team 3 (+2.9) received LAT-09 at 88 from t16. The cause is not in the data.
- **Team 12 (#1, 43 deals) and Team 14 (#2):** Team 12 has 26 dealer trades and Team 14 has few trades. Team 14's +3.10 from one value-created trade on its stall (directives 12:58) is the lever the leaders use.
- **Team 4 and Team 6 trade RET-06 (28 and 26 P, ticks 683/686):** they are the field's RET-uncommon market, while ours sit at value 100.4.

## Threats
- **Leaders are within 2 of us:** Team 12 29.9, Team 14 29.9, Team 10 28.9, Team 18 28.9, Team 1 28.6, us 28.4. Team 1 (+3.6/h) is closing on us. No gain-sharing trades with the top 5 unless our gain ≥ 3× theirs.
- **Team 13's buy-back and lending offers:** the 2 P bids for our RET commons are ~20% of value (RET-01 sells at 20). Directive says no.
- **Salamanca fever 18:03-20:03:** SAL-08 (22.5) has a Pilar resale window. Do not dump SAL to teams before it.
