# Strategist (claude-opus-5-5, Sat 16:30)

## How the points really work
- **Board = (0.5·Fri + Sat)/1.5 for now** [V]. Sunday's round counts in full once its day ends.
- **Negotiating 30** is scaled to the field's leader. Three parts:
  - **Duels**: 40% of Saturday Negotiating [V]. Our duel score is 13.93; its board conversion is not in the data.
  - **Dealer ladder**: +0.01 ≈ +0.33 board [V 12:13]. Ours is 0.200 ≈ 6.6 board, and the ~0.15 "cap" is refuted. Best 3 deals per level count; L3 ≈ 3× L2.
  - **Team-trade value**: 1 `neg_point` ≈ 0.094 board [V], capped at 50 per trade (≈ +4.7 board).
- **Market-making 30**:
  - Bench: the stall gets half, the top-3 mean gets full. Every board venue scored below the stall today, and Team 3 got 0 [directive 12:58].
  - Value created on our venue: capped at +5.0 board, floored at 0 [V]. `mm_points` itself is net and can go negative (−5.2 at 11:30).
  - Our current `mm_points` and `bench_efficiency` are not in the data.
- **Judges 40**: the largest share, and nothing scores it automatically. Criteria are not in the data beyond "ideas and craft".
- **Where the field is weak**: value created. Team 14's whole lead over us was one stall trade (+3.10 board [L]). The cap is +5, and other teams' values are not in the data. This is the single largest component still open to us.
- **The schedule is the hidden scoring rule**:
  - Round 2 runs until Sun 11:34 (hour 16.65), so the hard Market Test (09:34) and the 09:55 bench fall in round 2.
  - Round 3 (CHA) runs only 11:34-15:00, about 3.4 h, with the same weight as Saturday's ~14 h [plan: Sat 40%, Sun 40%]. Points per hour there are about 4× today's.
  - At the round event, `neg_points` and the ladder reset to 0 [V at round 2]. Every empty ladder slot is then a full-value point again.
- **Board now**: t12 29.9, t14 29.9, t10 28.9, t18 28.9, t1 28.6, us 28.4 (#6). The gap to #1 is 1.5, which is less than one capped trade (4.7).

## Our winning strategy
1. **Today: close a third page.** MAL is the cheapest.
   - We hold MAL-01..06 and MAL-09. Missing: MAL-07, MAL-08 (uncommons) and MAL-10 (rare). The bonus is 66.25 × 0.7 = 46.4.
   - Buy MAL-10 and MAL-07 first; leave an uncommon for last. A last uncommon bought at ≤ 13 scores the full +50 (17.5 + 46.4 − p).
   - Go only if MAL-10 comes from a safe team at ≤ 60. Then net ≥ +39 (≈ +3.7 board), which beats selling MAL-09 to Team 15 at 70 (+21).
   - Never buy MAL-10 from Chato (~87 → −38).
2. **Become the venue that hosts page-closers between other teams (v10).** One closer trade between two teams ≥ 6 below us can approach the +5 board cap, as Team 14 did.
3. **Treat Sunday 11:34-15:00 as the main event.** Stage cash, ladder stock and the CHA bids tonight.
   - CHA is our 1.6×: common 16, uncommon 40, rare 112.
   - Every CHA card bought from a low-multiplier team below value scores. A rare at ≤ 62 hits the cap.
   - The last card of the CHA page comes from a team: +50.
4. **Stop doing these:**
   - Dealer buy-to-resell outside the fever (≈ 0 net).
   - Chato buys above list (never counted, always lost).
   - Uncommon bids with < 5 margin: pack drag ate 2.4 on SAL-06.
   - Asks addressed to teams that are now within 6 of us.

## Levers nobody is using yet
- **Brokered page-closers on our venue.**
  - Evidence it is unused: every Friday team trade was on El Rastro. Only Team 13 lobbies for its own venue (v03). Team 14's +3.10 came from a single trade.
  - How: Dani pairs a dumper with a collector from `teams.md` (e.g. t15/t09/t07 collect RET or LAV). The seller lists on v10 addressed to the collector.
  - Both teams must be ≥ 6 below us; never t13 or t17.
- **The Workshop as a ladder-stock factory.**
  - It activated at tick 706 (Sat 16:15); other teams' use is not in the data.
  - Our LAV-02/03/04 spares are worth 3.2 each. Three of them give one uncommon (last time MAL-06, worth 17.5).
  - That uncommon sells to Pilar at ≥ 19 (L3) or Chato at 14 (L2 slot 3, still empty) at 0 `neg` cost.
- **The round-3 ladder reset.**
  - Before 11:34 a deal only replaces a slot: our weakest L3 deal is +0.019, so a new one adds only its excess.
  - After 11:34 every slot starts from 0, and 9 slots (3 per level) are open.
  - Hold 3 sellable uncommons and rares for Pilar, plus 3 for Chato, and execute from 11:34.
  - Evidence nobody pre-stages: not in the data. We would be first by design.
- **Round 2's Sunday tail.** Fill round 2's empty L2 slot and any page close in the 09:00-11:34 window, then switch to round 3 for everything else.

## Plan, anchored to the schedule
1. **Now (16:30), Operator:**
   - Re-run `can-give` and the closer check on asks to t03 (26.1) and t16 (25.7). Both are within 3 of us and climbing: cancel 10651, 10793, 10653 and 10885 unless can-give says YES and the card is not a closer.
   - Read `mm_points` and `bench_efficiency` into metrics.
2. **Now, Operator:** lower the MAL-08 bid 10570 to 13, keep it public, and add a MAL-07 bid at 15. Impact: ≤ +50 if MAL-10 lands.
3. **Now → 20:00, Lucas and Dani:**
   - In the room, find MAL-10 at ≤ 60 from a safe team (t15, t08, t03-if-still-low, t09, t07; not t10).
   - Ask Team 15 for its answer on MAL-09.
   - If no MAL-10 by 20:00: sell MAL-09 to t15 at 70 (+21), else to Pilar at ≥ 49.
4. **Now, Operator:** MAL-06 → Pilar, stepping −2/−3 from ~30, offer-only, alone in its window. Floor 19. Impact: +0.021 ladder ≈ +0.7.
5. **Now → 22:00, Dani:** broker 1-2 closer trades onto v10 between teams ≥ 6 below us. Impact: up to +5 board, minus what we hold now.
6. **18:03-20:03, Operator:** SAL-08 → Pilar only if it beats the new third L3 slot. The Chief first lifts SAL-08's reservation.
7. **20:33 Duels II, Aleks:** Duel Lab #1 (concede 15% of the gap, cap 18%), trade cheap days for price, ≤ 3 rounds. The trader keeps running.
8. **22:00-23:00, Operator:** Workshop LAV-02/03/04 spares if still unsold (cancel 10716 first). Keep the output as round-3 stock. Cash ≥ 100.
9. **Sun 09:00, Operator:** re-read `/api/schedule` and `neg_points`. Fill the empty L2 slot for round 2: Chato sale at ≥ value. The stall is live for 09:34 and 09:55.
10. **Sun 11:34-11:37 (round 3, CHA, +150 P), Operator:**
    - Run the 9 staged ladder deals; Abuela buys at or below list.
    - Bid CHA rares at ≤ 62 and uncommons at ≤ 30, addressed to low-ranked teams.
    - CHA page, rares first, last common from a team.
    - Cash → 0 by 14:00.
11. **Sun 13:34 Duels III, Aleks:** 4 concurrent duels, decay 10%, close fast.
12. **Judges, Lucas and Dani during Duels II:** the story is that we reverse-engineered the scoring (cap 50, pack drag, ladder-share stepping, the Workshop, round timing), backed by the predicted-vs-measured table.

## Hypotheses to test
- **H1: Sunday 09:00-11:34 deals count in round 2.**
  - Test: read `neg_points` at 09:00 (40.7+ means round 2 is still live) and again after the 11:34 event (0 means reset).
  - Decides whether round-2 stock is spent before 11:34.
- **H2: A page-closer trade between two teams on v10 moves our market score toward the +5 cap.**
  - Test: one brokered trade, with `mm_points` and the board's market part read before and after.
- **H3: The fever widens Pilar's range, so a SAL sale earns a larger ladder share.**
  - Test: SAL-08 in the fever with the same steps as MAL-06; compare against +0.040.
- **H4: Workshop output is random in set.**
  - Test: the next LAV-spare Workshop. Metric: the output card and its `your_value` (a LAV/RET duplicate is worth only 25%).
- **H5: Cap form (flat 50 vs 5 × book).**
  - Test: a CHA uncommon bought from a team at ≤ 15 (value 40; 5 × book = 125). A measured +25 is uncapped either way; only a gain above 50 separates the forms, which a rare can do.
  - Metric: `neg_points` delta.
- **H6: Our held silver pack yields CHA after release.**
  - Test: read its EV in `/api/me` at 11:34. If it does not rise, open it at once (it costs ~2.4 drag per buy).
