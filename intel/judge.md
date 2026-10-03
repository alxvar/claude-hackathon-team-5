# Judge (claude-opus-5-5, Sat 18:12)

## Verdict
**We are falling behind.** Over 60 min we gained +0.2 (30.0, #3). Team 6 gained +3.9 (31.7), Team 14 +1.9 (31.6) and Team 3 +1.2 (29.2, 0.8 behind us). Our `neg_points` stayed at 78.7 for the last 15 min.

## Our strategies: keep / kill / scale
- **Dealer bot (ladder deals): kill**, except the Chief's single defensive L5 deal.
  - Ladder 0.373 → 0.437 left `negotiating` flat at 21.88.
  - The MAL-08 → Chato thread fell 24 → 19 in −1 steps while his bid only went 13 → 14 (he mirrors step size). No deal.
- **Trading loop: keep.** Two accepts today, both positive: +6.2 (15:48) and +15.5 (17:46). The second moved the board 29.24 → 29.98. It costs nothing while idle.
- **SAL-06 page-close bid: scale. It is our biggest live lever.**
  - Value 82.1, so 50 P gives +32 and 60 P gives +22.
  - Only 14557 (50 → t13, expires 973) is live. Team 2's bid 14268 is gone from our open offers.
  - The auto-accept watcher only matches a **t02** ask.
- **Small maker asks (MAL-02/05 → t15 at 9, MAL-03 → t09 at 9, LAV-03 → t09 at 6): hold to expiry.**
  - Each would gain +2 to +2.8 if filled; all are still unfilled. Don't reprice; they are not worth accepts or attention.
- **14397 (LAV-02 at 0 → t09): kill.** It is −1.3 `neg_points` and earns no market points, because our own sale is not value created between other teams.
- **In-room trades (Dani): scale.**
  - SAL-06 talks with t02: anchor 120, counter 50, ceiling 60.
  - v10 room plan (t02 → t08/t07, t07 → t09): no settlement on v10 is visible. The venue is not in the trade feed (not in the data).
  - t02's RET-03 went to t14 (top 2) at 7 (tick 946) instead of t07 as planned.

## Check the scout
- **Holds:** the GUARDRAIL terms (≤ 60, floor 85, fee ≤ 4), the 1.6 gap to Team 14, the t14 swap with t16 and its RET-03 buy at 7, t03 selling MAL-02 to t17 at 3, and t06's 540 listings.
- **Fails: "14268 is live, 42 → t02."** At 18:11 the only SAL-06 bid is 14557, 50 → t13. Its step plan 42 → 46 → 50 is already overtaken.
- **Fails: the cap math.** The +50 cap binds only at price ≤ 32.1. At 35 the gain is +47.1, at 42 it is +40.1. The Operator's "at 35 hits the cap" is wrong too.
- **Fails: action 2.** Our own asks to t09 do not score market-making; only trades between other teams on our venue do.
- **Fails, and goes against the 17:58 directive: action 3** (sell SAL-09/10 to Pilar at ≥ 85 after the close).
  - After SAL-06 lands they read ~122 each, so a sale at 85 is about −37 each, counted.
  - It also undoes the page we just paid for. This is a stale premise from 17:45.
- **Fails: "Team 6 sold RET-02/03 to t06".** The trades were t12 → t06; Team 6 bought them.
- **Unsupported: "listing volume is Team 6's engine".** Team 8 has 1,034 listings and sits at #14.
- **Data conflict:** `teams.md` (18:08) has Team 1 at #5 with 28.2, but the 18:11 top 10 does not list it. Re-check before any rival test that names Team 1.

## The 3 changes with the highest expected gain
1. **Close SAL-06 with exactly one copy.**
   - Dani asks t02 to post an ask ≤ 60 addressed to t05 on v15 (0 fee). The watcher accepts it.
   - Keep 14557 to t13 as the single bid. Patch the watcher to cancel 14557 and re-read holdings before it accepts.
   - Expected: +22 to +32 `neg_points`, about +1.1 to +1.6 board at 0.05 per point.
   - Main risk: two fills in the same tick. A second copy is worth 5.6, so paying 50-60 for it costs about −45 to −55.
2. **Get one or two v10 trades between other teams settled.**
   - Use the room plan: t02 SAL-03 → t08, t07 RET-01 → t09, at ~9. Buyers must collect the set and not already hold the card, so value created stays positive.
   - Read our `market` after each settlement.
   - Expected: about +3 board [L, Chief], the only lever sized to close the 1.6-1.7 gap.
   - Main risks: value created turning negative (as with SAL-07 → t15 at −5.2), and any trade that gives t10, t03, t14 or t06 a gain.
3. **Rebuild cash for Sunday's CHA page with non-page spares, sold as maker.**
   - Spares: MAL-08 (17.5), LAT-03/04 (5), LAV-02 ×2, LAV-03 and LAV-04 extras (1.3-3.2).
   - Sell to non-rival teams at ≥ value + 3, on v15 or El Rastro.
   - Never sell SAL or other page cards. Leave SAL-09/10 alone.
   - Why: after SAL-06 at 50-60, cash drops to 91-101, which is below the 120 that the L5 buy needs and thin for CHA. CHA team buys below value score uncapped.
   - Expected: small `neg_points` now, and Sunday room to buy.
   - Main risk: a spare closes a page for a top-6 team. Check the buyer's progress in that set first.
