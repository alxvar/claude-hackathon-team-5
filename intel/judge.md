# Judge (claude-opus-5-5, Sat 21:28)

## Verdict
**Falling behind the leader, holding the podium.** #3 at 31.6: 0.0 over 60 min against Team 10's +1.3. The gap to #1 is now 3.7, and we are 0.6 behind #2 (Team 6, −0.5). Team 12 is closing at +1.2/60 min and sits 2.1 back. We were #2 at 31.93 at tick 1230. `neg_points` has been flat at 119.1 since tick 988, about 270 ticks with no scored deal.

## Our strategies: keep / kill / scale
- **Dealer bot: KILL, except the RET-11 → Pilar job.**
  - The RET-11 buy at 128 moved ladder 0.437 → 0.483, but the board fell 31.93 → 31.63. The Chief has measured the ladder as flat for the board.
  - The last thread (Pícaros LAV-04) correctly walked at an opening 4.
- **Trading loop: KEEP running, but it is idle.**
  - Last accept was 17:46 (SAL-07↔LAT-01, +15.5), and it has logged nothing since the 20:15 pause.
  - No ask or bid on El Rastro now beats our value. RET and SAL bids would break complete pages, and LAT asks at 8 sit above our value of 5.
- **Our bids and listings: SCALE a little.**
  - We have 0 open offers.
  - Our true spares are LAV-02 (×2 beyond the page, 1.3 each), LAV-03 and LAV-04 seconds (3.2), and LAT-03/LAT-04 (5).
  - Gains are about +3 each as maker. That is small (≈ +0.15 board each at the 0.05/point rate) but non-zero tonight.
- **In-room trades (SAL close): KEEP the method.**
  - SAL-06 from t08 at 28 scored +40.4, our last real gain.
- **v10 swap desk and pair-ads: KEEP, but unproven.**
  - Ads have run since 21:11/21:24. The number of v10 settlements since then is not in the data, and our current mm_points are not in the data either.
- **Duels II: FIX NOW.**
  - Of the session-3 duels finished so far, 3 of 4 ended no_deal (5618, 5619, 5622), and no_deal scores 0.
  - 6 duels are live.

## Check the scout
- **Holds:**
  - t12 paid 216 for RET-11 (tick 1245).
  - Pícaros epic median is 142.
  - t13 sold MAL-10 → t02 at 30.
  - t09 bought MAL-06 from t10 at 20, and t12 sold SAL-09 → t09 at 70.
  - t17 bids 150 for MAL-11, and t10 bids 205 for LAV-11.
  - Cash 392 against floor 350 leaves 42 P of slack.
- **Wrong:**
  - "t10's gains come from its venue v10": **v10 is our venue.** t10's venue is v07 (19:40 directive). Any ad or DM built on that line must be corrected.
  - "t08 asks RET-10 84": no such ask exists. The 84 was t06 → t04 (tick 1257). So the t08-holds-RET-09 premise rests on the matchmaker alone.
  - "t10 bids 112 for SAL-11": not in the data. The only SAL-11 offer is an ask at 245.
  - "t15 bids 56 on MAL-09/10": the 55-56 bids are from t09 and t04.
- **Missing:** the rebate tally (cap 80) exceeds tonight's 42 P of slack. Settle it at Sunday 09:05, after the +150 grant, as the 21:30 directive allows.

## The 3 changes with the highest expected gain
1. **Duels II: Aleks enforces the code-side deadline rules now (§4D items 1 and 6).**
   - The rules: accept any in-limit standing offer at `ticks_left ≤ 2`, and send the rival's own standing price and days from ≤ 4.
   - Compute days cost from `your_days_weight` in code.
   - Effect: turns 0-point no_deals into positive surplus across the 6 live duels and the rest of the session.
   - Risk: a days miscalculation lands outside the limit, which scores negative. Unit-check one live payload first.
2. **v10: get the matchmaker #1 trade (RET-09 t08 → t09, ~100) settled on v10 by people, not ads.**
   - Lucas or Dani first confirms in person that t08 holds RET-09, because the scout's evidence for it is wrong.
   - Effect: VC ≈ +134, which the 21:40 directive treats as enough for the full real-trades mark (22.5 scale, at +5.0 so far).
   - Then count v10 settlements at 21:50. If there are 0 after three ads, drop the ads and broker only in the room.
   - Risk: both teams are non-rivals (24.6 and 22.1), so the only cost is a rebate of ≤ 10 P.
3. **RET-11: ask Lucas for a GUARDRAIL to allow a team buyer above 198 alongside the Pilar job.**
   - A Pilar sale scores 0. A team sale at price p scores p − 198 in `neg_points`, capped at 50, and still counts for Saturday's round.
   - t12's print at 216 shows team demand exists. RET collectors below us include t02, t16, t07 and t09.
   - Never sell to t18 (#5) or t12 (#7, climbing; now holds a copy).
   - Risk: the extra value goes to a low team and the round closes before a fill. If no team bid arrives by 22:35, fall back to the existing Pilar job.
