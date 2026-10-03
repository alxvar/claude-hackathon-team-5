# Judge (claude-opus-5-5, Sat 17:24)

## Verdict
**Holding #2, at risk of losing it.** We are at 29.38, 1.0 behind Team 14 (30.4). Over 60 min we gained +0.9 against Team 14's +0.5, but over the last 15 min we lost 0.4. `neg_points` has been flat at 63.2 since tick 774. Team 3 is 0.2 behind us and climbing (+1.0 / 15 min, +3.1 / 60 min).

## Our strategies: keep / kill / scale
- **Dealer bot, ladder (Pilar / Pícaros): KEEP.** Ladder went 0.181 → 0.373 at 0 neg. MAL-06 to Pilar at 20 with −2 steps gave +0.040. The two L4 SAL buys gave +0.070 and +0.063, but the field joined (Chief: SAL-10 netted ~+0.36 board). Keep to free sales only, as directed.
- **Pícaros flags: KILL (already paused).** Results were +30, then −10, then three 0s (7225, 7344, 7356), which looks capped.
- **Fever resale SAL-09/10 → Pilar at ≥85: QUESTION it.** It scores 0 neg because dealer gains clip, so it only buys cash. It also conflicts with the SAL page (change 1).
- **Trading loop: KEEP, low yield.** One accept since 15:29 (swap SAL-04 → RET-04 on t07's v11, +6.2). No losses.
- **Our maker book: SCALE.** Only 5 offers are live against the plan's 20-30. Our last team-trade gain was tick 760 (+2.5). Since then, team trades have been our only remaining source of `neg_points`.
- **Asks 12480 / 12654 (SAL-02, SAL-01 at 11 to t16): KILL.** These are our only copies, worth 9 each, so the gain is +2. Team 16 collects SAL, and these may be its page-closers (it is 3.3 below us, under PAGE_CLOSER_GAP 6). They are also our own SAL page cards.
- **Team 15 approval and commission (in-room): KEEP.** It costs at most 3 P and is low risk, per the 17:15 directive.

## Check the scout
- **Wrong:** "we 29.73, #1 by a hair". Metrics have us #2 at 29.38, with Team 14 at 30.4.
- **Wrong:** "Team 3 now #6, 7 offers addressed to it". Team 3 is #3 at 29.2, and we have 0 open offers to t03. The 17:25 directive forbids new ones.
- **Wrong:** "Team 1 #3, +2.5/60". Team 1 is #4 at 28.8, +1.3/60.
- **Wrong:** "Sell RET-04 to t07". RET-04 is our only copy, worth 83.9 as a page card.
- **Wrong:** "LAT-04 has 2 copies". We hold one.
- **Unsupported:** the 9.5 sale prices to t07 come from teams.md at tick 631, and t07 has no live bids.
- **Wrong:** "0 P LAV-02 offers are errors". The operator says they are LAV-02→LAT swaps (+3.7 each), and the offer IDs the scout cites are stale.
- **Holds:** flags are capped; the L4 buys have diminishing returns; Team 6 bought SAL-09 at 68 (tick 781); Team 16 reached L4 at tick 761; Team 6 is within ~2 of us (now 2.1 below, so a rival under the 17:25 rule).
- **Weak:** "Pilar rare median 70" rests on n=1.

## The 3 changes with the highest expected gain
1. **Chief puts the SAL page to Lucas before the 18:06 fever job runs.**
   - We hold SAL-01..05, 08, 09 and 10. Only the uncommons SAL-06 and SAL-07 are missing.
   - Page bonus = 66.25 × 0.9 ≈ 59.6. Bought from a team at ~25 as maker, the last card scores the +50 cap (≈ +4.7 board per the 15:55 directive).
   - The fever resale scores 0 neg.
   - **Needs Lucas's GUARDRAIL:**
     - Cancel the SAL-09/10 fever job and asks 12480 / 12654.
     - Allow ~50 P of buys below the 100 floor.
     - Buy SAL-06 from Abuela at ≤23 (≈ −0.5, plus pack drag of about −2.4).
     - Buy SAL-07 last, from a team, as maker.
   - **Risks:**
     - No SAL uncommon is offered (Pícaros hold SAL-06/08, but cards from them are dealer buys and score no gain).
     - Our bids are visible on the feed.
     - Less Sunday CHA cash (fever cash is ~+170 if we sell instead).
2. **Operator fills the maker book with true spares to safe teams (t09, t07, t08, t15) at 8.**
   - Cards: 2nd and 3rd LAV-02 (worth 1.3 each), 2nd LAV-03 and LAV-04 (3.2 each), and MAL commons at ≥9 if MAL is not being paged.
   - Expected gain is +4.8 to +6.7 per fill. Reprice after 10 min.
   - **Risk:** few fills (5% of asks filled on Friday). Never list LAV spares to t03, which is collecting LAV (it got LAV-10 at tick 844).
3. **Enforce the rival filter on every live offer each 15 min:**
   - Top 6, or within 3.0 board of us: today t14, t03, t01, t12, t10, t06, t18.
   - Add any team that gains >1.0 in 15 min.
   - Team 3's +3.1/60 is the one threat that takes #2 from us.
   - **Risk:** cancelling offers costs a few small fills; that is cheaper than one +50 page-closer handed to a rival.
