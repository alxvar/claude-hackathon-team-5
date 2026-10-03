# Judge (claude-opus-5-5, Sat 22:17)

## Verdict
Holding #3 (30.9) but falling behind the leader. Team 10 is at 38.3 and gained +3.7 in 60 min, while we lost −1.1. Team 6 (31.7), Team 12 (30.7) and Team 18 (30.1) sit within 1.2 of us. Our `neg_points` have been flat at 119.1 since tick 988, about 6 h of game time.

## Our strategies: keep / kill / scale
- **Dealer bot**: keep it off, as the directive says.
  - Last thread: LAV-04 at Pícaros (her 4, final) → walked, neg/ladder unchanged.
  - Ladder 0.483 no longer moves the board (Chief 17:45).
- **FLIP rule (22:13)**: keep the rule, but nothing qualifies now.
  - MAL-11: t17 bids 150, but our value is 126, below the Pícaros epic list of 162.
  - LAV-11: t10 bids 205, and t10 is excluded.
  - MAL-09/10: t09 bids 56 against our value of 49 → est. score below +20.
- **Trading loop**: keep running, but it is idle. The last accept was 17:46 (+15.5); since then the log shows only errors (a rate limit at 21:50).
- **Maker book**: kill two offers, keep two.
  - Only 5 offers are live; the plan calls for 20-30.
  - MAL-03 (19328) is our only copy and MAL-08 (19331) our only MAL uncommon. Selling them for +2/+2.5 works against "MAL page → Sunday" (directive 21:00).
  - LAV-03 and LAV-04 at 6 are true spares: keep.
- **SAL-11 bid**: scale it.
  - 18605 expired unfilled; 18977 (115 → t04) is unfilled, and t04 ignored the pings.
  - The GUARDRAIL allows 125.
- **Team-bot chat pings**: kill. t09, t08, t04 and t01 gave no reply or closed the thread; bots don't take chat.
- **Reactor BUY/DENY**: keep. DENY 18669 was correctly refused (t10's RET page was already closed), and no bad buy went through.
- **v10 ads / rebate / pair ads**: keep, but they are unmeasured.
  - No v10 settlement and no `mm_points` appear in the data since 21:30.
  - The 15-min change (+0.2) shows no market lift.
- **Duels**: keep. Duel points are 31.57 with Duels II live (6 live, wave 2 at 5/5 deals per directive).
- **RET-11 hold** (bought at 128 from Pícaros, value 198): keep per directive (Pilar only at ≥ 198).

## Check the scout
- **Holds**:
  - SAL-11 went t10 → t17 at 207.
  - t10 bids 205 for LAV-11.
  - t13 bids 42 for RET rares and 4 for RET commons.
  - "Don't sell RET-09/10" is right: both are single copies on a complete page.
  - t04 bids 5 for LAV-02.
  - t12 bought LAT-10 at 86 from t01, and t10 bought MAL-11 at 195.
- **Does not hold**:
  - "SAL-11 ask at 245": not in the asks list.
  - "RET-10 ask 84": only RET-09 has an 84 ask.
- **Score changes are wrong**:
  - Team 12 is −0.1/+2.5, not +1.7/+3.1.
  - Team 1 is +0.8/+2.0, not +2.8/+2.2.
  - Team 10 is +3.7/60 min, not +4.7.
- **SAL-09 t12 → t09 at 70** was a t12 sale, not a buy.
- **"Selling to Team 1 passes the feeding rule"**: false. Team 1 is 5.2 points below us, and the rule needs ≥ 10.
- **"Spare commons" includes MAL-03**: it is a single copy, so not a spare. MAL-08 is not a spare either.

## The 3 changes with the highest expected gain
1. **Lucas/Dani close the RET-09 t08 → t09 match on v10 in person tonight**, the directive's top match, at about 100.
   - Bots ignore chat, so humans are the only channel.
   - The Builder adds our `mm_points`/market to metrics.md so the result is measured.
   - Effect: VC ≈ +134, "enough for the full real-trades mark" of the 22.5 [L].
   - Risk: t08 sells elsewhere first, or the trade lands off v10. Both teams are non-rivals, so no leader is fed.
2. **Re-post the SAL-11 bid at 125 (the GUARDRAIL max), maker on v15, 240 ticks requested, and Dani asks t04's humans in the room.**
   - Effect: up to +37 `neg_points` (162 − 125, minus pack drag) ≈ +1.8 board at the measured 0.05/pt.
   - Risk: t04 may not hold or sell at that price; 0 if unfilled. The cash floor of 260 still holds (392 − 125 = 267).
3. **Cancel 19328 (MAL-03) and 19331 (MAL-08). Replace them with true-spare maker asks addressed to non-top-4 teams that hold live bids:**
   - LAV-02 at 5 → t04, against t04's bid of 5 (value 1.3, +3.7).
   - Re-post LAV-03 and LAV-04 at 6 when they lapse (tick 1385).
   - Effect: keeps Sunday's MAL page intact; the swap costs about −4.5 forgone `neg_points` and earns +3.7 back.
   - Risk: negligible; these are small gains.
