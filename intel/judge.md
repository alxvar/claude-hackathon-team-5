# Judge (claude-opus-5-5, Sat 09:37)

## Verdict
**Falling behind.** We are #7 at 17.8 (−2.2 in 15 min; leader Team 13 −1.8, Team 14 −0.1). The gap is 10.4 to #1 and 1.5 to #4. `neg_points` and ladder reset to 0 at tick 160. Since the unpause we have 0 open offers and no bot activity, while others settled 7 team trades (ticks 160-166).

## Our strategies: keep / kill / scale
- **Trading loop**: keep and restart now. It has logged no Saturday actions; its last lines are Friday errors (rate_limited, sobre_bienvenida, network). Friday maker sells scored +7.7 (LAV-04 at 9) and +6.0 (SAL-06 at 26).
- **Our bids/listings**: scale from 0 to the plan's 20-30. The leaders list far more (t17 59 listings, t12 47).
- **Dealer bot on Chato**: kill, except as the RET-rare fallback. Chato deals scored −2.3 (LAV-06), −2.0 (LAV-09) and −8.0 (LAT-08 + Abuela LAV-05 window), and none moved the ladder.
- **Dealer bot on Abuela**: keep for the ladder now that it is reset to 0. Buy only at ≤ our value (Friday's MAL-07 at 29 cost −11.8).
- **In-room page trades (Dani)**: keep. The LAV-05 team buy at 8 was +50.0, the largest single gain we have. There is no Saturday output in the data yet.
- **Duelist (Aleks)**: 4 live, 34 finished, duel 0.0. Whether session 1 is scored is not in the data. The arbiter must hold our accepts only if it is.
- **Market recorder**: its status is not in the data. The first Market Test (hour 3.0) is the next event, and the venue decision and cash floor depend on it.

## Check the scout
- The scout has not run on Saturday, so there are no claims to check. Dani's `intel/teams.md` (tick 164) is the only rival read, and it is stale:
  - **Holds**: Team 15 and Team 2 collect RET. The live bids confirm it: t02/t15 on RET-09/10 at 7-10.
  - **Holds**: Team 14 buys LAV. It paid 55 for LAV-07 at tick 161.
  - **Fails**: it shows us #6 at 20.0 (Δ +5.1). Metrics show #7 at 17.8, and the +5.1 is Friday's page trade.
  - **Fails**: its sell table names Team 7 (8.8 below us) and Team 1 (9.4 below) as best buyers. Both now fail the ≥10-below rule for page-completing sales. Team 2 (11.0 below) passes.
  - **Fails**: Team 14 is only 0.1 below us and collects LAV, so never sell it LAV spares as page-closers.

## The 3 changes with the highest expected gain
1. **Open sobre_barrio, then restart `loop.py` and post a maker book.**
   - Floor: `--cash-floor 370` until the venue decision.
   - Asks: LAV-02/03/04, SAL-02 and LAT-04 spares at 9 (common clearing price; rival LAV-04 asks sit at 8-10). MAL-06/07 and SAL-08 at 25.
   - Addressing: send them to collectors that pass the feeding rule (Team 2, Team 9, Team 3). Never to the top 4 or Team 14.
   - Never sell a first-copy LAV card: each is worth 99-177 to us.
   - Effect: about +4 to +8 `neg_points` per fill (Friday comparables).
   - Risk: only 5% of asks fill (reprice after 10 min), and the unopened pack drags every trade's score.
2. **Ladder while it is cheap: `abuela_bot --dealer abuela --ladder --cash-floor 370`** before Duels I.
   - Before RET: negotiated buys only at ≤ value, e.g. a missing SAL common at ≤9.
   - After RET's release: RET commons at 9-10 (worth 11) and uncommons at 21-24 (worth 27.5). These score 0 `neg_points` and count toward the page.
   - Effect: Friday moved ladder 0.054 → 0.064 (board points per ladder point: not in the data).
   - Risk: −1 per common at 10 when we value it at 9. Whether the welcome price resets, and whether it counts, is open.
3. **RET rares first, as soon as the venue decision lowers the floor to 100.**
   - Bid at ≤74 for RET-09/10, addressed to holders below us, short-lived because the feed exposes addressed bids.
   - Fallback: Chato's steady-step protocol, capped at 90.
   - Finish with a RET common bought from a team at ~20 to test the cap.
   - Effect: +24 to +45 (plan §4B) plus the cap measurement.
   - Risk: Team 15 and Team 2 compete for RET rares (30 copies each). Cash is only 32 P spendable until the venue decision.
