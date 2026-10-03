# Strategist (claude-opus-5-5, Sat 12:28)

## How the points really work
- **Day weights:** the board now = (0.5·Fri + Sat)/1.5 [V]. The final = (0.5·Fri + Sat + Sun)/2.5, so a Sunday point equals a Saturday point (40% each).
- **Round resets:** a new round reset `neg_points` and ladder for every team [V, tick 160]. Whether value created resets is [?].
- **Negotiating 30, relative to the leader:**
  - Duels are 40% of Saturday Negotiating [12:13].
  - Ladder: +0.01 ≈ +0.33 board; best 3 deals per level; a missing deal counts 0.
  - Team trades: 1 neg ≈ 0.094 board, capped at 50 per trade [V].
  - Dealer gains clip to 0; dealer losses count in full.
- **Market 30:**
  - Bench: our stall scored 0.933 efficiency; market 7.5 is the number every stall team gets.
  - Value created on our venue: NET, capped at +5.0 board, floored at 0 [V].
  - One t10→t01 collector-buy on v10 moved market 7.5 → 12.5 (#7 → #3). One wrong-way trade (t10→t15) erased it.
- **Board price list:**

| Move | Board points |
|---|---|
| Net-positive value created on v10 | up to +5.0 (≈ 53 neg_points) |
| One ladder deal (LAT-08: +0.017) | ≈ +0.56 |
| A capped page close (+50) | ≈ +4.7 |
| A +3 maker sale | ≈ +0.28 |

- **Field weak spots:**
  - Value created: stall teams all sit at 7.5. Team 13 lobbies for any trade on v03 with no direction rule.
  - Ladder L3: Pilar opened to all at tick 502; only t13 had an early head start (tick 262).
  - Sunday: everything resets, CHA is our 1.6×, and dealer CHA buys cost us 0.
- **Our standing:** 26.4, #5, 5.8 behind t12. Gaps: v10 net is negative (mm −5.2); ladder 0.072 with L2 at 1/3 deals and L3 at 0/3.

## Our winning strategy
1. **Own value created on v10 (curated collector-buys).** A seller that dumps the set posts an ask on v10 addressed to a buyer that collects it; the buyer accepts.
   - Pairs from teams.md, all well below us: t08→t07 (LAV/LAT), t06→t15 (MAL/LAT), t03→t15 (MAL), t16→t07 (LAV).
   - Never a top-4 team (t12/t14/t13/t18), never a pair close to us (t17, t01, t10, t04, t02), never a wrong-way direction.
2. **Ladder at zero neg cost.** L3 = MAL-07 and MAL-06 to Pilar at ≥ 18 (our value 17.5), plus SAL-08 in her fever.
   - L2 stays at 1/3: no Chato card clears his final 14 at or above our value.
3. **Duels II (68 duels, days issue)** is the largest Negotiating block left today. Aleks ships the days logic.
4. **Sunday CHA 1.6×.** Every dealer CHA buy is below our value (16 / 40 / 112), so it costs 0 neg.
   - Shape each one as a negotiated close (never the opening price) so it also builds round 3's ladder.
   - Close the page with a team trade (+50).
5. **Stop:**
   - Chato sells below value.
   - Maker sales to climbers: pull 7042 (LAV-02 → t09).
   - Any trade on top-4 venues.
   - Active epic hunting: no epic ask exists in the data.

## Levers nobody is using yet
- **Direction-controlled venue value.**
  - Evidence: v10's only two trades went +4.99 and then net −5.2. Nobody else conditions venue trades on the sign.
  - Exploit: Dani pitches the pairs above. Market logs mm_points after each trade; add a buffer trade late in the day.
- **Silver pack timing.**
  - Evidence: our Saturday grant pack, opened just after the RET release, gave RET-05 [V]. So packs likely draw from newly released sets [L].
  - Our unopened sobre_plata (86.8) opened after the CHA release could pull 1.6× cards and save Sunday cash. Pulls never score; the cash saved does.
  - Cost: 1-4 points of drag per Saturday team trade, and few are planned.
- **Dealer flags.** RULES: "Some lie; a correct flag scores". There is no flag in our logs.
  - Flag only a clear text-versus-structure contradiction inside one thread. The cost of a wrong flag is not in the data.
- **Card-for-card swaps for CHA.** All 86 trades in the feed are for cash.
  - Sunday cash binds, so swap LAT/MAL/SAL spares for CHA cards held by teams whose `pack.opened` shows a CHA pull.

## Plan, anchored to the schedule (Saturday wall time = 12:23 + (game h − 5.56))
1. **Now, during Duels I · Operator · MAL-07 → Pilar.**
   - Re-post 7508 (expires at tick 511) with 2× the ticks wanted; offer-only, floor 18, alone in its window.
   - If Δladder ≥ 0.01, do MAL-06 the same way; stop on a zero reading. Impact ≈ +0.5 board each.
2. **Now · Operator · re-address 7042 (LAV-02) to t07 at 6.** Repost asks to t15/t03/t06/t16 only for non-closer cards.
3. **12:30-13:45 · Lucas + Dani in the room · 2-3 curated pairs on v10.** Target: net positive before bench 7.0 at 13:49. Impact up to +5.0 board.
4. **Benches at 13:49, 15:49, 17:49, 19:49, hard 21:28 and 21:49 · Market · record `bench_offers` and replay broker vs stall.**
   - A board venue opens only through the plan's §4E gate.
   - Bond + fee (270) vs cash 123 and the CHA close target: Lucas rules.
5. **~16:00-17:58, Pilar's SAL fever · Operator · cancel 7238, then SAL-08 → Pilar, offer-only.**
   - Ask from 31 (25% over the uncommon book of 25), floor 23. This is the third L3 deal.
6. **18:28 Duels II · Aleks.** Zero dealer threads (directive). Lucas and Dani rehearse the pitch.
7. **20:00-22:50 · Operator · sell spares as maker to non-feeding buyers.**
   - Cash ≥ 170 (directive), or ≥ 230 if the Chief adopts cha-plan a4327c6. The silver pack stays unopened.
8. **22:30 · Dani · one buffer collector-buy on v10** if net slipped.
9. **Sun 09:00 · Operator · reset check.** Read `/api/clock` and `/api/me` (neg, ladder, mm) and the silver pack's value.
10. **CHA release (game h 16.65) · Operator · re-read the pack value.** Open it if the value rose; run intel/cha-plan.md. Cheapest common last, from a team: +50.
11. **Bench 17.0 · Market · stall live.** Dani lands one curated v10 pair early in round 3.
12. **Duels III (18.65) · Aleks.** All dealer buys done before the finale (21.65); cash → 0 into non-negative buys.

## Hypotheses to test
- **H1. Value created = buyer value − seller value, and raw net can exceed the cap (a buffer works).**
  - Test: the next curated v10 trade.
  - Decides: venue_value_created and mm_points in data/me.jsonl against book × multiplier.
- **H2. L3 sells move the ladder more than L2 sells.**
  - Test: MAL-07 → Pilar.
  - Decides: Δladder vs LAT-08's +0.017.
- **H3. Value created resets each round.**
  - Test: read mm_points at round 3's start.
  - Decides: 0 vs carry-over.
- **H4. A pack draws from sets released at open time.**
  - Test: the sobre_plata value at Saturday close vs after the CHA release.
  - Decides: value rises → open it Sunday; otherwise open it at Sunday 09:00 before any trade.
- **H5. A Chato buy at ≤ his menu list counts for the ladder** (t13 bought LAV-06/07 at 26).
  - Test: the first CHA uncommon from Chato, warm, +3 steps toward 26.
  - Decides: Δladder. Buy anyway up to value 40 (0 neg).
- **H6. A correct dealer flag scores.**
  - Test: one flag on a clear contradiction.
  - Decides: score change in that window.
- **H7. The hard bench degrades the auto stall.**
  - Test: replay the 21:28 `bench_offers` through broker v1.
  - Decides: broker − stall ≥ 2 pp → evidence for a Sunday board venue.
