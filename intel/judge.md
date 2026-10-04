# Judge (claude-opus-5-5, Sun 12:46)

## Verdict
Gaining: we are #1 at 35.39 (+1.8 over 15 min, +2.6 over 60 min). t10 is at 34.2 (+0.1/60) and t12 at 34.1 (−0.5/60), so our lead is 1.2.

## Our strategies: keep / kill / scale
- **MAL closer: keep.**
  - MAL-07 filled through the public bid at 15: neg 52.2 → 54.8.
  - MAL-09 is now the last card (value-when-last 95.4). Bid 26022 at 60 to t08 is worth +35.4 if it fills; it expires at tick 2308.
  - 60 is above the 12:22 limit of ≤ 49. The Chief approved it at 12:43, and it is still ≥ 0.
- **CHA-11 epic bid: keep.** 25784 at 240 vs value 288 is +48. It expires at tick 2303 (about 26 ticks).
- **Dealer spare sales (Pícaros/Abuela/Pilar): kill.**
  - The tick-2169 batch and LAT-05 at 5: neg 50.0 → 50.0, ladder 0.364 flat. Zero gain, accepts and attention spent.
  - LAT-05 and LAT-01 were sold to dealers at 5 and 6. Bounty bid 25997 now buys them back at 10, which is pure churn.
  - Pícaros MAL-09 threads walked twice (58, 56). A dealer last card scores 0 by rule anyway.
- **Spare sales to non-rival teams: keep, small.** RET-03 → t01 at 5 (worth 2.8) gave +2.2.
- **LAT book bids (31 / 12 / 4): keep, low value.**
  - None has filled since posting.
  - LAT-09/10 are worth 35, so the max gain is +4 each. Never raise above 35, even though t01 paid t06 44.
- **v10 bounty/reward: keep (Lucas's GUARDRAIL).**
  - The 3rd settlement took v10 value created to 114.4 and mm_points 0.9 → 5.9.
  - Paying in kind at value costs 0 np.
  - Risk: the fair-play review the Chief flagged.
- **Trading loop: verify it is running.**
  - Its log has no Sunday entry (the last line is "closed" at 00:36), yet the 12:22 directive says ON.
  - Low stakes right now: no current ask is ≥ our value + 3 + fee.
- **teams.md "Who to sell" table: kill its rows.** It suggests selling MAL-10, MAL-06 and MAL-08 to t17. Those are MAL page cards, and selling any one destroys the +35-50 closer.
- **Duels: no change.** The Duel Lab Final check says NO CHANGE; duel score is 24.68.

## Check the scout (12:30 notes)
- **Holds:**
  - t18 bids 25 for MAL-09/10.
  - LAT-09/10 are worth about 35 and our 31 bids are likely unfilled.
  - t15 sold CHA-09/10 to t16 at 65, and t13 sold CHA-01 to t16 at 40.
  - t12 sold SAL-12 to t16 at 380.
  - t03's trend is +1.8/60.
- **Stale:**
  - "t12 #1, leads us by 0.6": we are now #1, 1.3 above t12.
  - "t03 1.3 behind": it is now 3.1 behind.
  - "MAL-07 last from t15": MAL-07 filled from t07, so MAL-09 is last.
  - "bid 25451 at 48" has been replaced by 26022 at 60.
  - "CHA-11 25638 at 220" has been replaced by 25784 at 240.
- **Wrong:**
  - "t04 +4.5 in 60 min": the metrics show +1.7.
  - "t10 bids only 100 for CHA-11": the Chief has t10 at 210, and t10 sold CHA-11 to t06 at 184 (tick 2228).
  - "t12 collects LAT": teams.md says RET/MAL/LAV, though the metrics show LAT×8 buys, so this is mixed.
  - "SAL-11 t04→t02 at 220 (tick 1858)": not in the data.

## The 3 changes with the highest expected gain
1. **Land CHA-11 before tick 2303 (+48).**
   - Dani confirms in the room that t08 will accept 25784 at 240.
   - On expiry, make one move to t16 (#11, non-rival) at ≤ 238 (value − 50). Never t10 or t06 (Chief's rival list).
   - Risk: t08 sells elsewhere first.
2. **Land MAL-09 before tick 2308 (+35.4 at 60; +50 at ≤ 45).**
   - Dani confirms in the room that t08 holds MAL-09. Holders are anonymous in the API.
   - If t08 doesn't hold it, mal09_bid.py's single move to t13 stands.
   - Keep it a team trade on El Rastro. Never buy the last card from the Pícaros (scores 0).
   - Risk: t18 (top 4) outbids us. Its bid is 25 now, so the risk is low.
3. **After 1-2 resolve, use spare cash for one epic closer-style bid: LAV-11 at ≤ 184.**
   - Value 234 = 180 × 1.3, [L] by analogy with CHA-11 = 288. That makes it a +50 team trade.
   - Address one El Rastro bid to a non-rival holder that Dani finds in the room. The holder is not in the data.
   - t17's 112 is the only LAV-11 bid on the board.
   - Risk: the holder is a top-4 rival (then don't bid) or won't sell under the Pícaros' epic price (~149).
   - Cash 647 − 416 in bids leaves room, and leftover cash doesn't score.
