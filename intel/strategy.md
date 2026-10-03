# Strategist (claude-opus-5-5, Sat 09:42)

## How the points really work
- **Weights.** Game = Neg 30 + Market 30, averaged (0.5·Fri + Sat + Sun)/2.5. Saturday is 40% and Sunday is 40%. Judges are 40.
- **Everything is relative.** The leader sits at the top of each scale (Team 13 held exactly 30.0 Neg on Friday).
- **Round 2 reset the field to zero** [V tick 160: our `neg_points` 67.8 → 0, ladder 0.054 → 0].
  - Every team fell 0.1-3.1 in the last 15 min (T12 −3.1, us −2.2), so nobody has scored much yet.
  - Whoever books first sets the top of round 2's Negotiating scale. Speed now is worth more than at any later hour.
- **Team trades: min(cap, ΔV − p − taker fee).**
  - The cap is ~50 per trade [L, n=1].
  - Page completion is the only way to hit the cap. Our LAV close gave +50, worth ≈ 8 board points at 0.16/pt [L].
  - Maker spares give +4 to +8 each [V: +7.7, +6.0].
- **Dealers only subtract** [V: −11.8, −8.0, −2.0].
  - Abuela deals move the ladder; our Chato deals did not.
  - The ladder is now 0 for everyone and counts the best 3 deals per level, so 6 negotiated deals fill levels 1-2.
  - Board points per ladder point: not in the data.
- **Market = bench efficiency + value created between other teams on our venue.**
  - **Value created: 0 for the whole field.** All 46 of Friday's team trades went through El Rastro; v01-v04 had 0 trades.
  - Rules say team venues trade from +3 h, i.e. hour 3.0 ≈ 09:50 [L]. That component opens today, unclaimed.
  - Bench: the stall earns half, the top-3 mean earns full. If every venue matches like the stall, how the scale behaves is not in the data.
- **Field weaknesses, cheapest first:**
  1. Value created on a venue (0 everywhere).
  2. Round-2 ladder (0 everywhere).
  3. Round-2 page closes (none yet).
  4. Swaps (all 53 feed trades are card-for-cash).

## Our winning strategy
Two things: **be the first round-2 page-closer (RET), funded by selling every low-multiplier card as maker**, and **be the venue where the bottom teams trade.**
- **Why not copy the leaders.**
  - Leaders spend 70-80 P on SAL rares (T13, T17, T18, T1). At their multipliers that scores little.
  - Our RET rare is worth 77 and Team 15's standing bid is 59. Bidding 60-66 as maker books +11 to +17 per rare, before the page bonus.
- **Sale stock (none of it has a page in reach for us):**
  - MAL-06/07 (17.5 each, clear 25-26).
  - SAL-08 (22.5, ~33 to T02).
  - MAL-02/04, SAL-03/05, LAT-03.
  - Spares: LAV-02/03/04, SAL-01/02, LAT-04×2 (1.2-3.2 each).
  - Clearing prices total ≈ 190 P and ≈ +80 `neg_points` (derived from the GAME.md clearing prices).
- **Cash.**
  - With the bond paid we have 402 − 270 = 132, so 32 spendable above the 100 floor.
  - The RET page needs ~250. Sales plus swaps close the gap.
  - If a RET rare is still missing at 15:00, stop (plan §4B) and hold the cash for CHA.
- **Sunday:** CHA at 1.6× (rares worth 112, above Chato's ~90, so no dealer loss). Bring cash to 0 by 14:00 (GUARDRAIL).
- **STOP:**
  - Chato deals for the ladder alone.
  - Packs and first prices.
  - Any LAV first copy. The page is complete: a sale loses 99-177 against a 50 cap on any re-close.
  - Sales to the top 4 or Team 14 (0.1 below us, collects LAV).
  - Taker accepts, except a page-closer or an ask below value − 3 − fee.
  - Trading on v03 (T13) or v02 (T12).

## Levers nobody is using yet
1. **Card-for-card swaps for RET cards.**
   - Evidence: zero swaps in 53 feed trades. Every team opened a grant pack today (ours gave RET-05), so non-RET teams hold RET cards worth little to them.
   - Exploit: offer MAL-06 (17.5 to us) for a RET uncommon (27.5 to us), addressed to non-collectors (not T02/T15). This saves the cash the venue bond takes.
2. **Value created on our own venue or stall.**
   - Evidence: 0 team-venue trades all of Friday; T13 is lobbying for v03, so the lever is real.
   - Exploit:
     - Ask the desk now whether other teams can trade on our free stall. If yes, Dani pitches the bottom 8 teams to trade there.
     - If not, use our board venue once the directive opens it.
   - Unlike v03, every fill there scores for us, not a leader.
3. **Page-closers sold to the bottom teams.**
   - Evidence: the last common of a page is worth ~76×m to the buyer, and our spares are worth ≤ 3.2 to us.
   - Exploit: when T07, T09 or T16 bids for a LAV, SAL or LAT card we hold spare, reprice from 10 to 35-45, addressed to them. Apply the feeding rule (≥ 10 below us, never top 4).
4. **Abuela's welcome price for a RET uncommon.**
   - Evidence: the first deal was a fixed 17 [V]; whether it resets is open.
   - Exploit: our first Abuela deal today is a RET uncommon. If 17, that is 10.5 below value and inside the 32 spendable.

## Plan, anchored to the schedule
Times are wall clock = game hour (directive 09:37).

| When | Who | Move | Expected |
|---|---|---|---|
| 09:40-09:50 | Operator | Abuela RET uncommon (welcome-price test). Swap offers MAL-06 / MAL-07 / SAL-08 for any RET-06/07/08, addressed to non-RET teams (≤ 30 offer limit). | Card at ≤ value; ladder deal 1 |
| 09:40 | Dani | Desk: can other teams trade on our stall? Does the leftover hour-4.0 `day_closes fri` do anything? Q6 (do duels count in the 6 conversations)? | Decides lever 2 |
| ~09:50 bench 3.0 | Market session | Recorder on; venue decision per directive 02:20; read every team's `market` | Floor 370 → 100 |
| 09:55-11:55 | Operator + trader | Maker book 20-30: sale stock at clearing to teams ≥ 10 below us; reprice after 10 min. RET-09/10 bids at 60-66, short-lived (the feed exposes addressed bids). | ≈ +80 `neg_points`; rares +11 to +17 each |
| 09:55-11:55 | abuela_bot `--ladder` | RET uncommons at 21-24 and commons at 9-10, negotiated, ≤ value | 3 ladder deals |
| 10:00-12:00 | Dani | Points bottom teams at our live addressed offers (opportunities.md); holders of RET rares from `pack.opened` | Rare sourcing |
| 11:50 bench 5.0 | Market session | Venue live and supervised | Bench + venue base |
| 11:59-~13:35 Duels I | Aleks | Duelist (§4D fixes); arbiter holds accepts only on duel-critical ticks; bots maker-only | Duel points |
| 11:59-13:35 | Lucas + Dani | Judges pitch: "measured facts" table, decision timeline, reset/cap findings | Judges 40% |
| 13:50-18:20 | Operator | Finish RET: rares from teams (Chato ≤ 90 only if needed and cash allows); last card = a RET common from a team at ~20 (cap test) | +24 to +45 net (plan §4B) |
| 18:29 Duels II | Aleks | `days` logic; no dealer threads if Q6 says duels count in the 6 conversations | — |
| 19:50, 21:29 hard, 21:50 | Market session | Broker supervised through the hard bench | Bench |
| 21:00-23:00 | Operator | Sell leftover spares; keep cash for CHA | Sunday funds |
| Sun open | Chief | Re-read `/api/schedule` (round 3 at 23:29 falls after the close, so expect a re-anchor). CHA page from teams below value; dealers ≤ value; cash → 0 by 14:00 | Second +50 close |

## Hypotheses to test
- **Cap form** (flat 50 · 5×book · 5×(p+f) · value ≤ 6×book).
  - Experiment: the RET finish, a common from a team at ~20.
  - Decides: the measured score. 50 = flat or 5×book; ≈ 62 = 5×(p+f); ≈ 38 = value ≤ 6×book.
- **Other teams can trade on our free stall, and value created counts there.**
  - Experiment: desk question, plus `/api/venues` after hour 3.0.
  - Decides: our `market` component moves after a third-party fill.
- **Which dealer deals count for the ladder.**
  - Experiment: (a) the Abuela welcome deal; (b) one negotiated Chato RET uncommon at 28 (−0.5).
  - Decides: `ladder_points` before and after each, one deal per window.
- **Abuela's welcome price resets each day.**
  - Experiment: the first Abuela RET uncommon today.
  - Decides: a price of 17 vs 29.
- **Swaps fill.**
  - Experiment: three swap offers for RET uncommons, addressed to non-RET teams.
  - Decides: any fill within 20 min (vs 5% of asks filled on Friday).
- **Bench scale when everyone matches like the stall.**
  - Experiment: read all teams' `market` after bench 3.0.
  - Decides: the stall teams' share. Half means a better broker pays; full means the venue only pays through value created.
