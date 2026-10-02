# Judge (claude-opus-5-5, Fri 21:51)

## Verdict
We cannot tell whether we are gaining on the leaders, because the leaderboard is not in the data. Our own `neg_points` rose 16.6 → 26.3 (+9.7) between 21:32 and 21:46, and we are in 3 of the 22 trades between teams.

## Our strategies: keep / kill / scale
- **Selling to teams at the market's bid level: SCALE.** LAT-07 sold at 21 (tick 68) and LAT-06 at 22 (tick 86, +9.7). LAT-06 sat unsold at 30 for 15 min, then filled ~3 min after the reprice.
- **Autoflip (LAT): KEEP, uncommons only.** At our LAT value of 0.5, a common is worth 5 to us. The last LAT common fills were 6–9 P, so a common scores at most +4, which is below the ≥8 trigger. An uncommon at 21–22 scores +8.5–9.5. No autoflip results appear in the actions log yet.
- **Dealer bot haggling to buy flip stock: KILL.** Thread 160 (MAL-07) spent 2+ ticks haggling 16 → 19 against her 27, and Team 8's 35 bid vanished meanwhile. The flip cost is only cash, so speed matters more than price. Use the bot for ladder deals only.
- **Dealer bot `--ladder` for El Chato: KEEP.** He is a level-2 dealer and has not opened yet. A missing deal counts 0.
- **`loop.py`: KEEP, but it is producing nothing.** It made 0 actions in the last 25 entries, and El Rastro shows no bids or asks to accept.
- **Our bids: VERIFY NOW.** Metrics show "Our open offers: 0", yet the log says 10 bids (21:20) plus LAV-09 at 100 (21:43). Only MAL-06 at 12 filled. Either the bids are gone or the metrics feed is broken.
- **LAV-09 bid at 100: CUT to 91.** Lucas's own figure is 91 (70 × 1.3). A fill at 100 scores −9 unless LAV-06/07 also arrive from teams, and we have no evidence they are lined up. A bid of 91 still beats Team 10's 90 and keeps the block.
- **In-room trades (Dani): no logged result yet.** The script is in PLAN.md.

## Check the scout
- scout.md is not available, so there is nothing to check.
- Lucas's claims, checked against the metrics:
  - MAL-06 at 12 (tick 66), LAT-07 at 21 (tick 68) and LAT-06 at 22 (tick 86) all match the trade list.
  - "Abuela stops at ~24" for uncommons is consistent with the 23 median buy price.
  - "Collectors bid 16" cannot be verified: the bid book is empty in the metrics.

## The 3 changes with the highest expected gain
1. **Sell Team 15 the LAT cards it lacks; Dani confirms the list in the room.**
   - Team 15 bought 5 LAT cards from teams (01, 02, 05, 06, 07). A 2nd copy is worth only 25% to them, so stop offering those numbers.
   - Offer LAT-03, -04 and -08 or higher, uncommons at 21–22.
   - If we hold a LAT rare, sell it to them: it is worth 35 to us, and rare sales between teams went for 53–80, which would score +18 to +45.
   - Whether we hold any LAT rare is not in the data. Lucas checks `/api/me`.
   - Risk: Team 15's standing is not in the data. If they lead, every sale also scores for them. Check the leaderboard first, and stop if their gain exceeds ours.
2. **Do El Chato's 3 ladder deals the moment he opens** (`abuela_bot.py --ladder`). Higher levels weigh more, and a missing deal counts 0.
   - The expected effect is ladder share only; the point size is not in the data.
   - Risk: it uses the 8 deals/hour budget we share with the flips. Give Chato's deals priority.
3. **Repost the bids, and cap LAV-09 at 91** with `trade.py`.
   - First confirm the 10 bids still exist, given the empty book. Repost any that are missing at gain ≥3.
   - Effect: avoids a −9 fill on LAV-09 and restores our fill pipeline. MAL-06 gave +5.2 from a single bid.
   - Risk: Team 10 raises above 91 and takes the LAV page. That only matters if Team 10 is a leader, which is not in the data.
