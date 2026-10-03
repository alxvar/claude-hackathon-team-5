# Judge (claude-opus-5-5, Sat 18:29)

## Verdict
Holding #3 at 30.0, but losing ground at the top: +0.6/60 min vs t06 +4.3 (gap 1.7) and t14 +0.4 (gap 1.5). t03 is 0.4 behind and gained +0.4 in 15 min. neg_points have been flat at 78.7 since tick 904.

## Our strategies: keep / kill / scale
- **Dealer bot: KILL (confirm it is stopped).** The ladder is capped (negotiating flat across ladder 0.373 → 0.437). Its last log is still a Chato MAL-08 sell thread at 17:40, stepping 24 → 19 against his 14; the 17:45 directive cancelled it. L5 Ernesto is unreachable at our cash.
- **Trading loop: KEEP.** Its only two accepts today were swaps worth +6.2 (15:48) and +15.5 (17:46). No bad fills.
- **SAL-06 bids: KEEP, RETARGET.** Four addressed bids in 28 min (35 → t02, 42 → t02, 50 → t13, 50 → t17) and 0 fills. 14889 expires at tick 993, about 5 min from now.
- **MAL/LAV common asks (14534, 14696, 14698, 14733): KEEP only if the feeding check passes.**
  - Each gains only ≈ +2 to +2.8.
  - t15 collects MAL and sits 5.9 below us, not ≥ 10 below. If MAL-02 or MAL-05 closes its page, t15 books up to +50 against our +2.
  - Teams.md agrees: "no buyer passes the feeding rule above value + 3".
- **v10 ad job (every 15 min): UNPROVEN.** No v10 fill or mm_points change is in the data since tick 398 (−5.2).
- **Dani in-room (t02 SAL-06): KEEP.** t02 dumps SAL, so it likely holds a spare. Its 120 is an anchor.

## Check the scout
- **Holds:**
  - SAL-06 close ≈ +32 at 50 and +22 at 60.
  - Keep the pack unopened (Chief 18:20).
  - Don't take t16's 5 P RET or 12 P LAV-06 bids.
  - t14's RET-03 buy at 7 (tick 946) and its SAL-04 ↔ MAL-05 swap (939).
  - t03's commons at 6 and 3 (ticks 904, 929).
  - t10 +0.7/15 min, L5 unlocked.
- **Wrong:**
  - t10 did not sell MAL-10: it bought it from t03 at 74.
  - t06 bought the RET commons at ticks 861 and 905 from t12; it did not sell them.
  - "t03's negotiating is the highest" is stale (tick 850); current value not in data.
  - "Fastest climber t10" holds over 15 min only; over 60 min it is t06 (+4.3).
  - Action 3 is flawed. We hold no rare or uncommon spares: all RET/LAV are single page cards, and SAL is reserved. Our own sales on v10 are not "value created between other teams", and the ad job pairs other teams, never our cards.
- **Missed:**
  - t17 closed its SAL page Friday with our SAL-06. Selling it now breaks its page, so the t17 fallback is likely futile.
  - The unopened pack drags the close by ≈ 2.4 (SAL-06 at tick 632: −2.7 vs −0.5). Expect ≈ +30, not +32.

## The 3 changes with the highest expected gain
1. **SAL-06 from t02 (≈ +22 to +30 neg, ≈ +1.0 to +1.5 board [L]).**
   - Let 14889 → t17 lapse.
   - Dani gets t02 to post the ask itself: one SAL-06, ≤ 60, on v15 or El Rastro. The watcher auto-accepts under the 85-floor guardrail.
   - If t02 prefers our bid: one maker bid → t02 on v15 at 50, asking 2× the ticks (server halves them).
   - Main risk: t02 holds at > 60 and we end with 0. Never go past the 60 ceiling, and never close at a dealer.
2. **Duels II: ship the `--days-read auto|flip|unsure` switch before the 19:30 freeze (Aleks's call).**
   - Day reading is the largest swing left: +0.47/duel right vs −0.18 backwards (red team). Duel points are live while neg and ladder are flat.
   - Risk: flipping on a wrong read. Default to auto, and flip only on a confirmed misread in the first duels.
3. **Make v10 value created measurable, then push it in person.**
   - Log mm_points after each ad slot. If there is no positive-VC fill by 19:00, Dani pitches the top non-rival pair from `intel/v10-suggestions.md` face to face (t09 or t15 buyers, sellers holding 2 copies).
   - Expected: 0 to +5 mm per trade, ≈ +3 board at the cap [L].
   - Risk: a negative-VC fill (tick 398: −5.2, #3 → #7). Run the rival and VC test on every pair, and never involve t03, t06, t10 or t14.
