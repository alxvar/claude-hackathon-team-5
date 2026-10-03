# Judge (claude-opus-5-5, Sat 22:33)

## Verdict
Falling behind the leader and barely holding #3. Team 10 is at 38.0 (+2.7 in 60 min) and we are at 30.7 (−0.9), so the gap is now 7.3. Team 12 sits only 0.3 below us. Our neg_points have been flat at 119.1 since tick 988, about 400 ticks with no scored gain.

## Our strategies: keep / kill / scale
- **Dealer bot: kill for score.** The last priced thread (19:01, Pícaros LAV-04) walked with neg and ladder unchanged. Ladder 0.373 → 0.483 never moved the board. The 21:45 directive says no dealer threads.
- **Egg threads: stop after the Chato pack.** They brought MAL-06 (17.5) and badges, with score effect not in the data. Gifts never score, though MAL-06 helps the MAL page.
- **Trading loop: keep, but check it is alive.** Its last accept was 17:46 (+15.5, the 2nd scored accept today). The log has no line after 20:15 "closed", although the 21:45 directive turned bots back on.
- **SAL-11 bid to t04: keep and scale to the cap.** Bid 18605 lapsed unfilled, 18977 lapsed, and 19620 sits at 115. t04 ignored the bids and its bot answers no chat.
- **Spare-sell offers (19655-19658): split.**
  - Keep LAV-03 at 6 and LAV-04 at 6: about +2.8 each as maker, from 2nd and 3rd copies.
  - **Kill MAL-03 at 9 and MAL-08 at 20.** Holdings show a single copy of each, so selling one breaks the MAL page (01-06 + 08 held; Sunday close per 21:00/21:20). The gain is only +2.0 and +2.5.
- **RET-11 hold: keep.** Sell only at ≥ 198, per the 21:20 directive. t12 paid 216 at tick 1245.
- **v10 swap desk, ads and rebate: keep, with a deadline.** Real trades are the biggest open lever (22.5). The ads posted (21:46, 21:56, 22:06), but no team trade has settled anywhere since tick 1332. Bot pings got no replies.
- **DENY/FLIP reactor: keep it gated.** The DENY refusal at 21:39 was correct (stale target). No current bid qualifies for a FLIP:
  - MAL-11: our value 126 is below Pícaros' list of 162.
  - MAL-09/10: Pícaros at about 57 against our value of 49 is about −5 net.
- **Duels: keep.** We are at 34.13 duel points, and 8 of the last 10 closed in a deal. Duel Lab's Duels III params are worth about +1.85 duel pts over 68 duels. The board conversion is not in the data. This is Aleks's call, on branch `duelist-loop`.

## Check the scout
- **Holds:**
  - SAL-11 at ≤ 125 is within the guardrail, our value is 162, and cash 392 covers it above the 260 floor.
  - RET-11 hold at ≥ 198; t12 paid 216.
  - The ranks #4-#6 are close behind us (0.3-0.7).
  - Team 10, Team 4 and Team 1 hourly rates match the metrics within 0.2.
- **Wrong:**
  - The offers expire at tick 1420, not 1385.
  - Team 18 is +0.0/15 min and −0.1/60 min, not "+1.9 in 30 ticks".
  - Rare book value is 70, not 77 (77 is our RET value).
  - Team 10 *bought* MAL-11 at 195 from t08; it did not sell it.
  - Our own sales do not count for the v10 rebate or desk goals. Only trades between other teams count.
  - "Market bid for uncommons ≈ 24" is a single SAL-06 bid; there is no MAL uncommon bid.
- **Missed:** MAL-03 and MAL-08 are not spares, so the scout's "confirm first" should have been "cancel".

## The 3 changes with the highest expected gain
1. **Raise the SAL-11 bid from 115 to 125, addressed to t04 on v15, requesting 240 ticks** (the server halves to 120).
   - Operator via `trade.py`.
   - Expected: about +35 neg_points (minus about 2 of pack drag), roughly +1.6-2.3 board. That protects our 0.3 lead over Team 12.
   - Risk: t04's bot never fills addressed bids (2 lapses so far). If so, the 125 P stays reserved for CHA and nothing is lost.
2. **Cancel offers 19656 (MAL-03) and 19658 (MAL-08) now, or let them expire at 1420 and never re-post.**
   - Expected: keeps Sunday's MAL close alive. It is worth up to the +50 cap in a fresh round, versus +4.5 forgone tonight.
   - Risk: none if MAL stays in the plan. If Lucas drops MAL for CHA budget, we lose +4.5.
3. **Lucas and Dani close the RET-09 t08 → t09 match at ~100 on v10 in person before 23:00, since bots ignore chat.**
   - Expected: VC ≈ +134 per the matchmaker, enough for the full real-trades mark (≈ +5 board under the 5.0 × min(1, VC/top-3) reading [L]).
   - Both parties are below us: t09 at 23.6 gains a page, but stays 7 behind.
   - Risk: the 21:40 match has no settlement yet. If nothing settles on v10 by 23:00, stop the ads and move the desk effort to the 09:00 Sunday grant window.
