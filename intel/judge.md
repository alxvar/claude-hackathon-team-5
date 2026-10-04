# Judge (claude-opus-5-5, Sun 10:08)

## Verdict
**Holding at #4, not gaining.** We are at 30.2, behind t10 by 2.5, t12 by 1.6 and t18 by 0.8, and ahead of t03 by 2.2. The CHA close lifted us +1.1 over 15 min, but we are −0.3 over 60 min. We have lost the #3 slot the 09:28 directive told us to defend, to t18. t10 is falling (−4.9 over 60 min), so #1 is still in reach.

## Our strategies: keep / kill / scale
- **Dealer bot: keep until the 14:00 cut.**
  - Six Abuela CHA buys at 8/9/8/9/22/21, all below value, cost 0 neg.
  - The Pilar sale of the LAV-07 spare at 17 moved the ladder 0.115 → 0.148.
  - The ladder is at 0.172 now. No losses today.
- **Addressed closer bids on El Rastro: scale.** CHA-05 from t02 at 72 scored neg 0 → 50.0, exactly the cap. The whole CHA page cost 196 P. This is the only method that has paid today.
- **RET-11 asks: keep, but act fast.**
  - The asks to t13 at 248 and 235 both lapsed unfilled.
  - The ask to t02 at 240 (offer 21583) expires at tick 1653. The board shows tick 1647, so about 6 ticks are left.
- **Trading loop: keep, but verify it is alive.**
  - Its last accept was Sat 17:46 (+15.5).
  - The action log shows no event after 00:36. The 09:55 restart in Lucas's log does not appear in it.
  - It has made no Sunday fills.
- **LAT-06/07/08 bids at 9: keep.** These are uncommons worth 12.5 each, so a fill is +3.5. They cost nothing while unfilled, and LAT-08 denies t12 one of its gaps.
- **Duelist: keep, one instance only.**
  - 136 duels finished. The last 10 gave 8 deals and 2 no-deals.
  - Metrics show duel 0.0 this round, so Duels III and the Final are still unscored upside.
- **Flags: dead.** The Saturday probe confirmed the cap. Spend no more effort here.
- **v10 / market-making:** no current numbers in the metrics. Not in data.

## Check the scout
- **Holds:**
  - RET-11 to t02 at 240 is right: 198 → +42, inside the per-trade cap.
  - Do not sell CHA cards. The 146/218 values include the page bonus.
- **Wrong: "neg sits at the 50 cap, the gain is capped."** The cap is per trade [V]. On Saturday our total reached 119.1. Whether our trade part has capped against the field is the Analyst's M5; that is not in the data.
- **Wrong: "expires 40 ticks from now."** It expires at tick 1653 against tick 1647 on the board, about 6 ticks.
- **Wrong: cancel the LAT bids.**
  - The scout cites dead offer IDs (20331, 20332). The live ones are 20680, 21657 and 21658.
  - It values LAT-06/07/08 at 5 as commons. They are uncommons worth 12.5, so the bids are +3.5 each, not a loss.
- **Wrong: "ladder capped near 0.15."** We are at 0.172, and the Pilar LAV-07 sale moved it +0.033 today.
- **Workshop:** the +11.8 is collection value only. GAME.md [V] shows neg and ladder unchanged, so it does not score. Low priority.
- **Stale rival numbers:**
  - The scout says t12 is +1.3/15; metrics show −0.7/15 and +1.4/60.
  - It says t18 is 0.6 above us; it is now 0.8 above us and 0.8 behind t12.
  - It says t08 is +1.3; metrics show +0.7.

## The 3 changes with the highest expected gain
1. **RET-11 to t02, before tick 1653.**
   - Dani confirms in person now.
   - Re-post at 240 the moment it lapses. Request double the expiry ticks and read back the `expires` the server returns; Sunday's tick scaling is not in the data.
   - Fallback is 230, per Lucas's log.
   - Effect: +42 neg.
   - Risk: t02 buys t10's copy instead, which gives the leader +98. Speed is the whole play.
2. **MAL page: put the numbers to the Chief now, not at 12:00.**
   - Dealers close at 14:00, so a 12:00 call leaves too little time.
   - We hold MAL-01..06 and MAL-08. We are missing MAL-07, MAL-09 and MAL-10.
   - Rares cost ≤ 62 at the Pícaros against a value of 49, so −13 each and −26 at worst.
   - The closer is MAL-07, worth about 64 with the page bonus. A team just sold one at 9, at tick 1647. Bought through an addressed El Rastro bid with the fee added, it scores +50 (cap).
   - Net about +24 to +34 neg. Cash needed is about 150, inside the 197 left above the 176 floor.
   - Order: rares first, closer last.
   - Risk: a rare unavailable at ≤ 62 leaves −13 sunk with no closer. Stop after the first rare if the second has no live path. Never trade MAL with t12.
3. **Duels III readiness (≈ 11:00) and trader liveness.**
   - Confirm exactly one duelist on Lucas's Mac (sha 29aa1be).
   - At T−5, stop swaps, opps and the recorder (directives 01:30 and 07:25(9)).
   - Run the first-wave check after wave 1.
   - Confirm `loop.py` is running with floor 176. Its log has nothing for Sunday.
   - Effect: secures the only part still at 0 this round. Size is not in the data.
   - Risk: two duelist processes on one key, or a silent dead trader missing below-value asks.
