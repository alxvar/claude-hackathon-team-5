# Judge (claude-opus-5-5, Sat 11:35)

## Verdict
**Falling behind.** We dropped from #3 (27.9, teams.md 11:02) to #7 (22.35). The gap to #1 grew from 0.9 to 5.3, and we lost 7.1 in 15 min. `neg_points` rose 33.2 → 35.2, but `mm_points` went +4.99 → −5.2 after the tick-398 trade on v10 and erased that gain.

## Our strategies: keep / kill / scale
- **Chato buys: KILL.** Three Chato deals today cost −10 (RET-09), −9 (RET-10) and −2.5 (RET-06), −21.5 in total. All were above list, and the ladder moved 0 every time.
- **Abuela dealer bot: KEEP, needed cards only.** Its returns are shrinking: the commons added +0.014-0.018 each, RET-08 +0.003, RET-07 +0.004 (ladder 0.051 → 0.055). Stop at 11:40 per directive.
- **loop.py: KILL after Duels I unless it shows a fill.** Since its 10:32 restart the log has no accept, only open/close events and errors.
- **book.py maker asks: KEEP, re-check addressees.** It has one fill (SAL-01 to t03, +4.7). Asks to t07 at 9 sat unfilled for 50 min. The 11:32 snapshot shows 0 open offers after the v07 cancel.
- **Public bids on v07: KILL (done 11:37).** MAL-03 filled at 5 for +2.0, but v07 is t10's venue and t10 is now #4, so every trade there feeds a top-4 team's market score.
- **v10 deal with Team 10: SCALE only collector-buys.** Its two trades netted about −10 mm in total (+4.99, then −10.2). The 11:31 rule stands.
- **In-room page closers: KEEP.** RET-01 from t10 at 20 gave +50.0, our best trade of the day. The next one is the CHA close on Sunday.
- **Epic GUARDRAIL buy: hold.** No epic or legendary asks on any of the 19 boards; the bargains daemon is watching.

## Check the scout
- **#1 (no accepts from 11:50): action holds, evidence wrong.** The 34 "finished" duels in the metrics are session-1 duels (277/278 are practice in GAME.md), and the duel score is 0.0. Duels I has not started. "40% of the duel part" is not in the data.
- **#2 (MAL-06/07 to t17 at 26): REJECT.**
  - 26 is t17's median uncommon price, not a bid.
  - Offer 6112 is not in our logs.
  - At 22.35, t17 (17.5 at 11:02) is about 5 below us. MAL lacks are unknown, so they count as closing, and t17 fails the ≥10 rule.
  - Same problem for live 5813 (MAL-07 → t15 at 21): t15 (15.1) is about 7 below us.
- **#3 (LAV spares at 9-10): partly holds.**
  - t09 did buy LAV-04 at 9 at tick 353.
  - But 4 LAV-04 asks at 10 and 2 LAV-03 asks at 9 are sitting unfilled, and ours at 9 to t07 never filled. Raising the price won't fill.
  - The 11:02 public-LAV condition ("no top-4 team collects LAV") now fails: t10 is #4 and collects LAV.
- **Climbers section: factually wrong.**
  - t01 SOLD SAL-10 (to t06 at 76) and LAT-09 (to t16 at 68); it did not buy rares.
  - t16 SOLD LAV-10 at 82 and BOUGHT LAT-09.
  - "Cash 114" and "RET-10 bid 36" are stale or wrong: metrics show cash 109 and a bid of 38.
- **teams.md "Who to sell to": stale.** Its gaps assume we are at 27.9. Now only t09 (~12), t07 (~10.5) and t11 (inactive) are ≥10 below us, and that needs a live check.

## The 3 changes with the highest expected gain
1. **Protect Duels I (34 duels; the duel score is 0.0 now).**
   - Operator: abuela_bot threads down at 11:40, loop.py stopped at 11:50, book.py maker-only.
   - Lucas: confirm in person that Aleks's duelist is running. Standby only if Aleks's process is dead.
   - Effect: a missed duel deal scores 0, and duels are worth far more than the trader's +2 to +5 fills.
   - Risk: the duelist is down or the accepts collide.
2. **Recover market-making with collector-buys on v10 (10 mm points swung in 2 trades).**
   - Dani and Lucas pitch non-top-4 pairs to trade on v10, addressed: t09 bids MAL-06 at 17 and SAL-06 at 20, and t06 bids SAL-09 at 68.
   - Sellers to target are teams that dump that set: t16, t03 and t14 dump MAL; t15 dumps SAL. Never a top-4 seller.
   - Team 10 posts on v10 only addressed to collectors (11:31 rule).
   - Effect: each collector-buy is positive value created for us, and the first one gave +4.99 market.
   - Risk: the holders are unknown, and the sign of each trade only shows after it settles. Market logs every trade.
3. **Re-run the feeding check on every live ask against the live leaderboard, now.**
   - Pull or re-address 5813 (MAL-07 → t15) and LAT-08 → t03 (t03 is about 6 below us and collects LAT).
   - Post no public LAV asks while t10 sits in the top 4.
   - Post MAL-06 to t09 at 20-21 (a known lack, +2.5 to +3.5 for us), but only if t09 is ≥10 below us.
   - Effect: avoids handing a +50 closer to a team near us; the cost is a few small fills.
   - Risk: the pool of eligible buyers shrinks to 2-3 teams, which slows cash toward the CHA target of 170. If we recover rank, re-widen the list.
