# Strategist (claude-opus-5-5, Sat 09:59)

## How the points really work
- **Negotiating 30** has three parts, and each is relative to the field (the leader sits at the top).
  - Team trades score ΔV − p − fee (taker only), with a cap of ~50 per trade [L].
  - Dealer deals score min(0, ΔV − p) [V]. A dealer can only cost us `neg_points`. Its upside is the ladder, plus cards that set up a page we finish with a team trade.
  - Ladder: best 3 deals per level, a missing deal counts 0, higher levels weigh more. Level 1 is full (0.014/0.018/0.016 = 0.048). Level 2 (Chato) is **0 after 4 deals** → 3 empty slots at a heavier weight.
  - Duels: surplus × (1−d)^messages; no deal = 0. Duels I (hour 5.15) is the first scored session, so **every team is at 0**.
- **Round 2 reset at tick 160.** The field restarted from 0. We sit at −10.0 (RET-09 at 87 from Chato) and drift −2.5 per 15 min while Team 12 adds +7.4. 1 `neg_point` ≈ 0.16 board [L].
- **Market-making 30**:
  - Bench: matching the free stall earns half; the top-3 mean earns full. Venue value: 0 trades on any team venue all Friday, so nobody scores it.
  - Gated by GUARDRAIL 09:55: no venue now.
- **Judges 40**: the largest block. Our measured-rules record is the material for it: dealer gains = 0, every duel message = a round, the 50 cap, addressed offers leak in the feed.
- **Cheapest points now (field ≈ 0)**:
  1. Duel close-rate: fewer than half of Friday's practice duels ended in a deal.
  2. Level-2 ladder slots: Chato rare buys show a median 86, above his list 77.
  3. CHA at 1.6 on Sunday.

## Our winning strategy
**Be the top-multiplier collector who never pays a dealer above list, plus the duel closer.**
1. **Saturday: finish RET.**
   - Net ≈ −10 (RET-09) − ~10 (RET-10) + 50 (last common from a team) ≈ **+30 `neg_points` ≈ +4.8 board** [L, cap n=1].
   - Uncommons must cost ≤ 27.5 (0 loss). Buy them from Chato **below his list 26**, so they also feed the empty level-2 ladder slots and the level-3 early start.
2. **Duels: maximise closed deals, not anchors.**
   - Field close-rate <50%, and every message costs 6/8/10%. One closed duel at ~45% of the pie beats any team that lets half its duels die.
3. **Sunday: be the CHA buyer.**
   - Our 1.6 is the highest of the six values, so we can outbid every holder below 1.6 and still gain.
   - Team buys below 112/40/16 score in full: a rare at Rastro's clearing 70 = +42.
   - Dealer CHA singles at ≤ value cost 0 (RET rares cost −10 each).
   - The last CHA common comes from a team: +50.
   - Arrive with cash.
- **Stop**:
  - Chato rares beyond RET-10.
  - Any dealer deal above its list "for the ladder" (4 such deals scored 0).
  - Human time on maker asks for 1-3-point commons (leave them to the trader/repricer).
  - Venue work outside the Market session's gate.
  - Any sale to t12/t13/t14/t17/t04.

## Levers nobody is using yet
- **Ladder = price better than the dealer's list** [hypothesis, fits all data]:
  - Abuela commons at 9 vs list 10 counted.
  - Chato at 93 and 87 (rare list 77) and 31 (uncommons) counted 0. LAT-08 sold at his buy price 13 = opening, which never counts.
  - Chato uncommons cleared at a median 26 over the last 60 ticks, so ≤ 25 is reachable. Nobody shows a Chato rare below list (median 86).
  - Exploit: the 3 RET uncommons from Chato at ≤ 25.
- **Duel closing**:
  - The organisers say "open with an offer the other side can take"; Aleks found that each message costs a round.
  - Exploit: open inside a plausible zone. From `ticks_left ≤ 4`, send the rival's own standing price so they accept (and spend their accept).
- **Flags**: "a correct flag scores, a wrong one costs" (RULES). No flag activity appears in our data. Exploit only a structural contradiction, e.g. text says "final" but the offer lacks `final: true`.
- **Reading the feed for gaps**: addressed bids leak in `offer.listed`. They tell us what t12/t13 lack (never fill it) and which teams ≥10 below us lack a card we hold as a spare.
- **Swaps for RET uncommons**: 3245 (SAL-03+05 → RET-07, t16) and 3246 (MAL-02+04 → RET-08, t07) are live per the operator log. They save cash and both sides gain.

## Plan, anchored to the schedule (wall ≈ game hour + 6:50; re-read `/api/schedule` each round)
1. **Now → bench 5.0 (~11:50), Operator: RET page.**
   - Verify 3245/3246 want RET cards, not 0 P. Metrics show "for 0"; if that is the real price, cancel.
   - RET-10 via `chato_steady`, cap 88.
   - RET-06/07/08: Chato steady +1 steps, target ≤ 25, cap 28. One thread at a time, read `ladder_points` after each deal. Abuela ≤ 24 only after the 3 Chato deals.
   - Cash: 288 − 88 − 78 − 22 = 100. It fits the 100 floor with 0 margin; one maker fill or swap fill restores slack.
2. **After RET-06..10 are held, Operator: RET-01 last.**
   - Bid ~20 addressed to a holder outside the top 4 (t06 sold RET-02 at tick 205), ≤ 20 ticks.
   - Expect +50 (cap test: 50 / 62 / 38) → log it in GAME.md.
3. **Before Duels I (5.15, ~12:00), Aleks:**
   - The §4D fixes, plus the close rule.
   - Bots run maker-only via the arbiter.
4. **Duels I (~12:00-13:40):** Lucas + Dani draft the judges' pitch around the measured-rules table.
5. **Benches 5/7/9/11 (~11:50, 13:50, 15:50, 17:50), Market session:** replay recorded `bench_offers` against the gate (stall + 2 pp). No venue unless it passes.
6. **When level 3 activates (watch `/api/levels`), Operator:** if we have 3 below-list Chato deals, use the early start for the best 3 deals at ≤ value.
7. **Afternoon, Operator + Dani:** sell MAL/LAT/SAL spares and the SAL-08 ask (3536, t16 at 33) to collectors ≥ 10 below us. Purpose: Sunday cash.
8. **Duels II (11.65, ~18:30), Aleks:**
   - Send full price+days packages; give days on the side we weight less.
   - No dealer threads if desk Q6 says duels fill the 6 conversations.
9. **Close (23:00), Operator:** cash ≥ 250 target (100 floor + spare sales); never sell LAV page cards.
10. **Sunday open, Operator:**
    - CHA from dealers at ≤ value: 0 score, page progress.
    - CHA from teams below 112/40/16: positive score.
    - Last common from a team: +50.
    - Cash → 0 by 14:00 (GUARDRAIL).
11. **Duels III (18.65), Aleks:** 10% decay; close within ≤ 2 messages.

## Hypotheses to test
| Hypothesis | Cheapest experiment | Deciding metric |
|---|---|---|
| Ladder credits only the price below the list | Next Chato RET uncommon at ≤ 25 vs list 26 (0 loss: worth 27.5) | `ladder_points` rises (vs 0 for 4 above-list deals) |
| Cap form | RET-01 from a team at ~20 | +50 flat/5×book · ~62 5×(p+f) · ~38 6×book |
| L3 early start needs "good" (ladder-counting) Chato deals | Same deals as row 1; watch L3 activation | `level.unlocked` for t05 before "open to all" |
| Stall earns half even if no board venue beats it | Read every team's `market` after bench 5.0 (read-only) | Stall teams equal vs below board-venue teams |
| A correct flag scores | Flag one structural contradiction (text "final", no `final: true`) | Score component change; cost of a wrong flag: not in the data |
| Sunday packs carry CHA | Read rivals' `pack.opened` `best` after CHA release, before buying any pack | Share of CHA pulls |
| Duels count in the 6 conversations | Desk Q6; else a refused 6th thread during Duels II | Error code on thread open |
