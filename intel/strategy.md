# Strategist (claude-opus-5-5, Sat 17:18)

## How the points really work
- **Final** = 60 × (0.5·Fri + Sat + Sun)/2.5 + judges 40. Sat and Sun are 24 game points each. Judges (40) is the largest single block: 3 min of pitch, 5 min for the top 3.
- **Negotiating 30**, relative to the leader.
  - Team trades: one trade scores at most +50, ≈ +4.7 board. This is the biggest per-action payout we have measured.
  - Dealer deals: ≤ 0 neg. They pay only through the ladder.
  - Flags: +10 each, but the last 3 scored 0, so they look capped [L].
  - Ours now: neg 63.2, ladder 0.373, duel 13.93.
- **Ladder**: best 3 deals per level. L3 pays ≈ 3× L2.
  - L4 slot 1 paid +0.070 and slot 2 +0.063. Once 5 teams joined L4 (ticks 761-802), slot 2 netted only ~+0.36 board.
  - So ladder points are cheap only during a head start.
- **Market-making 30** = bench (the stall earns half, full = mean of the top 3) + NET value created on our venue.
  - One good trade on v10 moved our market 7.5 → 12.5. One dump (t15 buying SAL) took it to −5.2.
  - t14's lead was one value-created trade on its stall (+3.10 board).
  - t10 sits at the cap; what the cap is: not in the data.
  - Per trade, this is our highest-leverage component and it is two-sided.
  - Our current mm and bench_efficiency: not in the data. The Market session must report them after the 17:54 bench.
- **Round boundaries (schedule)**: round 3 fires Sun 11:34 (hour 16.65).
  - Sun 09:00-11:34, including the hard bench at 09:34 and the 09:55 bench, still feeds round 2 [L].
  - Round 3 benches: 11:55 and 13:55. The 21.0 bench falls after the 20.078 close.
  - So each Sunday bench ≈ half of round 3's bench score.
- **Where the field is weak**:
  - Value created on team venues: Friday had 0 team-venue trades; current counts are not in the data.
  - Level head starts.
  - Round 3 neg: everyone starts from 0 at 11:34.
- **Standing**: #1 29.73 vs t14 29.7. t01, t03 and t16 are climbing at +3.7 to +4.7/h.

## Our winning strategy
1. **Close the Salamanca page today. This is new, and it is the biggest move left in round 2.**
   - We hold SAL-01..05, SAL-08, SAL-09 and SAL-10. Missing: SAL-06 and SAL-07.
   - Bonus = 66.25 × 0.9 = 59.6. The last card bought from a team is worth 22.5 + 59.6 = 82.1, so it scores the +50 cap at p ≤ 32 as maker (≤ 29 as taker).
   - The fever resale scores 0 neg; this scores ≈ +4.7 board, more than t14's whole +3.10 stall edge.
   - Cash: MAL-09 → Pilar ≥ 55 (17:30) takes us to ≥ 147. SAL-06 ≤ 23 plus SAL-07 ≤ 30 leaves ≈ 94. With the 150 grant that is ≈ 244, matching the Sunday target of ~245.
   - **Needs Lucas**: a GUARDRAIL for floor ~94 (now 100), plus holding SAL-09/10 instead of the 16:43 fever plan.
   - Fallback keeps that plan: if SAL-07 is not secured by 19:30, the fever job runs 19:30-20:03.
2. **Curate value-created trades onto v10.** Pair a seller that dumps set X with a buyer that collects X; both outside the top 5.
   - The t15 approvals run until 18:30.
   - Never route a buyer that dumps the set (the SAL-07 → t15 lesson, −10.2).
3. **Sunday**:
   - Round-2 benches at 09:34 (hard) and 09:55.
   - CHA page in round 3: our 1.6× values, with a team-bought page closer at +50.
   - Benches at 11:55 and 13:55 supervised.
4. **Judges**: the pitch is our measured-formula science (cap, page recipe, flags, step rules) plus the guardrails. Aim to stay top 3 for the 5-minute slot.
- **STOP**:
  - L4 buys and flags beyond one probe.
  - 0-P "sales": 12725 and 12759 give LAV-02 to t07/t09 at −1.3 each and look like feeding.
  - Chato buys above list.
  - Any sale of a page card. RET-04 is now worth 83.9, not a spare.

## Levers nobody is using yet
- **SAL page with 8/10 already held.**
  - Field SAL rare buys from Pícaros (median 59) are resale plays; nobody can close a SAL page as cheaply as we can.
  - Sources: SAL-07 last went t10 → t15 (tick 398); t15 dumps SAL. SAL-06: Abuela (paid 23 earlier) or a team at ≤ 22.5.
  - Keep the bids addressed and short-lived, because the feed shows them.
- **Curated collector trades on our venue.** Same-set pairs from the profiles:
  - LAV: t15, t08 or t06 → t07, t09 or t04.
  - RET: t13 → t07, t09 or t02.
  - MAL: t08, t06 or t09 → t02.
  - Evidence: 133 team trades, yet one stall trade was worth +3.10 board to t14.
  - Dani pitches only offers that already exist; we can't trade on v10 ourselves.
- **Sunday 09:00-11:34 is still round 2 [L].** Morning trades and two benches count where our neg is already 63+. Most teams will treat Sunday as round 3.
- **L5 head start.**
  - Unlock pattern: L3 "3 Chato deals", L4 "2-3 Pilar deals". We have 2 Pícaros deals.
  - The 17:35 spare-common sale is the 3rd: it fills L4 slot 3 and may unlock L5 early.
  - L5's status in /api/levels: not in the data (output truncated).
- **The cap rewards one high-value buy.** Any team buy with value − price ≥ 50 scores 50.
  - A CHA epic is worth 288 to us, so it scores +50 at ≤ 238 (LAT-11 traded at 160).
  - LAV-11 is worth ≥ 234 to us, so it scores +50 at ≤ 184. Its holders: not in the data. Pilar holds one.

## Plan, anchored to the schedule
1. **Now**:
   - Operator: cancel 12725 and 12759 (`trade.py`).
   - Chief → Lucas: SAL-page GUARDRAIL decision. The fever job holds SAL-09/10 until that decision.
   - Dani: in the room, find SAL-07 and SAL-06 holders (start with t15).
2. **17:30** Operator: MAL-09 → Pilar ≥ 55 (directive).
3. **17:35-17:40** Operator:
   - Sell a spare LAV-02 to Pícaros: offer-only, steps of −2/−3, not at their opening bid (L4 slot 3 / L5 probe).
   - One flag, structured mismatch only.
4. **If approved** Operator:
   - First: SAL-06 from a team at ≤ 22 or from Abuela at ≤ 23.
   - Last: SAL-07 from a team at ≤ 29-32, as maker if possible. Expected +50.
5. **17:54 bench** Market session: bench_efficiency vs stall, plus our mm. Decide whether broker work for Sunday is worth it.
6. **18:04** Operator: SAL-04 spare (2.2) → Pilar in the fever, cash only.
7. **18:00-18:30** Dani: curated v10 pairs inside the t15 approvals.
8. **19:30** SAL fallback decision. **20:39** Duels II (Aleks): days logic; all duel accepts can go in the same tick.
9. **Evening** Operator: sell non-page singles as maker to collectors outside the top 5, at ≥ value + 2. These are MAL-01..05 (7), MAL-08 (17.5), LAT-01/03/04 (5) and the LAV/SAL spares.
10. **During Duels II** Lucas + Dani: draft and rehearse the 3/5-minute pitch.
11. **Sun 09:00** Operator: re-read /api/schedule. **09:34 / 09:55** Market session: benches, supervised.
12. **11:34 CHA + round 3** Operator:
    - Open the pack, then build CHA at ≤ value. Chato rares at ≤ 112 score 0 neg.
    - Leave the cheapest common for a team buy: 16 + 106 = 122, so +50 at p ≤ 72.
13. **11:55 / 13:55** benches. **13:34** Duels III (Aleks). **15:00-16:00** pitch prep.

## Hypotheses to test
- **Flag cap resets** (per hour or per dealer opening). Test: one structured-mismatch flag after 17:40. Decided by neg_points +10 vs 0.
- **Cap form (flat 50 vs 5×book)**. Test: the SAL-07 (uncommon) close at p ≈ 20. Uncapped it is 62 minus pack drag. Decided by `neg_points` delta: 50 vs ≈ 59-62.
- **L5 early unlock = 3rd Pícaros deal**. Test: the 17:35 spare sale. Decided by a `level.unlocked` event for t05.
- **Value created on v10 = buyer value − seller value**. Test: log each curated trade's predicted sign. Decided by mm delta per settlement.
- **Sunday-morning benches count in round 2**. Test: Dani asks the desk at 17:30. Decided by the desk answer.
- **An epic adds to a complete page**. Test: GET /api/me/value?card=LAV-11 (read-only). Decided by value > 234.
- **Pilar's fever bid holds under the field dump**. Test: the SAL-04 spare at 18:04. Decided by her final vs 12.5 (25% over book).
