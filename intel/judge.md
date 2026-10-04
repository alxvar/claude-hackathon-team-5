# Judge (claude-opus-5-5, Sun 15:21)

## Verdict
**We finished first.** Team 5 is #1 at 37.73, ahead of t10 at 35.76 (+1.97) and t12 at 34.51. The final hour was slipping: t10 gained +1.0 over the last 60 min while we gained +0.6, so the lead held only because the clock stopped.

## Our strategies: keep / kill / scale
- **Team-trade page closers: SCALE.** They were our engine. `neg_points` went 0 → 104.8 on Sunday, and 100 of that came from two +50 closers: CHA-05 at 72 from t02 and CHA-11 at 190 from t10.
- **In-room deal with a rival (CHA-11 from t10): KEEP, with a caveat.** We gained +50, but t10 gained about +1.47 board points, the same as us (directive 13:12). The gap did not move. Treat rival values as unknown, never as "small".
- **Dealer bot and ladder: KILL earlier next time.** The ladder stayed flat at 0.364 from midday. The LAT-05 sale to the Pícaros at 5 (12:05) left both neg (50 → 50) and ladder (0.364 → 0.364) unchanged. Late dealer threads were pure time cost.
- **Trading loop (`loop.py`): KILL in this form.**
  - Its last accept was Sat 17:46 (+15.5).
  - On Sunday it logged only clock, closed and network-error events.
  - No Sunday fills are attributable to it in the logs.
- **Final-push addressed bids: KILL.** RET-11, SAL-11 and MAL-11 were bid at value −15, then value −5. They got 0 fills and were all cancelled at 14:57.
- **MAL-09 bids: KILL.**
  - Three addressed bids at 75 (to t01, t09, t15) lapsed.
  - The Pícaros thread ended at 56 against our 44.
  - The MAL page stayed at 9/10, so it never scored.
- **Flags: DONE.** Net +20 from 3 scored flags; later flags scored 0.
- **v10 market: KEEP, it worked but did not beat the stall.**
  - mm_points 14.0, market 13.08, second to t09's 13.34.
  - Every bench scored at the stall's 0.5, so the broker added nothing on benches.
  - v10 had 8 trades, 10 traders and VC 248.7.
- **Duels: KEEP.** Duel points rose 34.65 → 35.84 in the final wave (27 deals, 7 no-deals).

## Check the scout
- **Holds:**
  - Game over; lead 1.97; 0 open offers.
  - t10 sold RET-11 to t09 at 216 (tick 2757) and CHA-11 to t01 at 160 (tick 2498).
  - t04 has 99 deals and −0.2/−0.2; its 2 P commons are confirmed at ticks 2774-2778.
  - Final duels 27/7; VC 248.7.
  - "Re-normalisation effect not in the data" is correct.
- **Wrong:**
  - "t02 bought SAL-11 at 222" is false. The feed reads SAL-11 t02→t03, so **t02 sold it**.
  - t02's +1.5 includes that sale plus buying CHA-11 from t17 at 140; the scout's causal story is unproven.
- **Unsupported:**
  - "t09 resold CHA-01": the feed only shows t09 selling it at 9.
  - "Selling epics at book-level prices gained t10 0.5 per 15 min" is a correlation, not a measured attribution.

## The 3 changes with the highest expected gain (judges = 40%; the game score is frozen)
1. **Submit by 15:30 (Lucas/Dani).**
   - Paste `judges/pitch/sunday/submit-story.md` into /submit and fill the Q4 slots.
   - Strike any claim built on the scout's t02 misreading.
   - Lead with verified numbers: #1 at 37.73, the two +50 closers, v10's 8 trades and VC 248.7.
   - Gain: protects the 40% block. Risk: missing the deadline.
2. **Fix the record before judges read the repo (Builder).**
   - `metrics.md` attributes "tick 1466: −119.1 · picaros buy RET-11 at 128". That is the round reset, not a deal.
   - The tick 904 and tick 2169 windows each bundle many deals into one change, against plan §7.1.
   - Relabel these in LOG.md and the metrics. A judge seeing a −119 dealer loss would misjudge our discipline.
   - Whether judges read the repo is not in the data (desk Q7 was unanswered). Risk: editing logs after the freeze looks like tampering, so add notes rather than rewriting lines.
3. **Prepare the v10 bounty answer (Lucas).**
   - The Chief flagged a fair-play risk in the 10:50 and 11:25 directives.
   - State the facts: the reward was announced in the v10 ad; buys were capped at ≤ value (≥ 0 deals); every reward trade was off v10.
   - Name which payouts actually settled; that is not in the data, so pull it from the feed before Q&A.
   - Risk: an unprepared answer reads as score-farming.
