# Judge (claude-opus-5-5, Sat 11:52)

## Verdict
**Falling behind.** We are #9 at 22.66, down 4.7 in 15 min, 6.4 behind #1 Team 14 (which gained 7.2) and 2.1 behind #5 Team 10.
- **Cause:** the market part fell from 12.5 to 7.5 (`mm_points` +4.99 → −5.2, v10 trade at tick 398). Negotiating only gained +2.0 (`neg_points` 33.2 → 35.2).
- **Duels:** `duel` is 0.0 with 0 live duels at 11:49. Check the Duels I start time in `/api/schedule`. The start time is not in the data.

## Our strategies: keep / kill / scale
- **Dealer bot, Abuela: hold.**
  - Below-list deals moved the ladder: commons +0.014 to +0.018, RET-07/08 +0.003 to +0.004, at 0 `neg_points`.
  - RET and LAV are complete, so we need no card from her until CHA on Sunday.
- **Dealer bot, Chato: kill, except the one decided ladder test.**
  - Measured losses: −10.0, −9.0 and −2.5 (RET-06 at 30, worth 27.5).
  - None of 6 deals moved the ladder (0.055).
- **Trading loop (`loop.py`): kill.**
  - Its last 25 events are errors and open/close events, with no accept on Saturday.
  - The bargains daemon found 0 of 67 asks worth taking, so there is nothing for it to take.
- **Our addressed asks (book.py): keep, but tighten.**
  - Saturday fills: SAL-01 at 7 (+4.7) and MAL-03 bought at 5 (+2.0).
  - 13 asks are live. The Team 7 asks have been unfilled for 50+ min. Team 7 is 172 listings ahead of us in volume for 12 team trades.
- **In-room / page trades: scale.**
  - RET-01 from t10 at 20 hit the +50 cap and closed RET.
  - This is the only Saturday move worth more than 5 points.
- **Venue v10: keep the stall, police who trades on it.**
  - A collector buy gave +4.99 (MAL-07, t10 → t01).
  - A dumper buy gave −10.2 (SAL-07, t10 → t15).

## Check the scout
**Claims that hold:**
- Team 3 is 4.9 below us.
- LAT-08 at 21 would score +8.5 (value 12.5).
- SAL-08 at 25 would score +2.5.
- Team 1 sold SAL-10 for 76 and LAT-09 for 68.
- Team 4 sold us MAL-03 at 5.
- The RET page is complete (closed at tick 276, +50), so "not racing" is correct.
- Holding the Chato test until after Duels I matches the directive.

**Claims that do not hold:**
- "Team 13 bids for rares: t17 has MAL-09 at 85" mixes up teams. The 85 bid is Team 17's.
- Team 2's RET-10 bid is 44, not 42.
- "Team 1/4 do rare swaps": the feed shows cash sales only.
- Its suggestion to re-address LAV commons to Team 1 breaks our own rule. Team 1 is #7 at 23.1, above us, and collects LAV.

## The 3 changes with the highest expected gain
1. **Get positive-value trades onto v10 (Dani in the room, Market logs the sign of each trade).**
   - Pitch non-top-4 pairs where the seller dumps a set and the buyer collects it:
     - t08 (dumps LAV/LAT) → t07 (collects LAV/LAT)
     - t16 (dumps MAL) → t17 or t15 (collect MAL)
     - t15 (dumps LAV) → t04 or t09 (collect LAV)
   - Lucas asks Team 10 again to post on v10 only to collectors.
   - Effect: the one clean collector trade was worth +4.99 on the market part. That is more than our entire Saturday trade book has scored.
   - Risk: another dumper buy goes negative, or a top-4 buyer closes a page on our venue.
2. **Ladder program after Duels I, as decided.**
   - Run one Chato SAL-06/07 buy: open 24, +2 steps, accept ≤ 26, alone in its window. Then read `ladder_points`.
   - Pre-set the Pilar sales of SAL-08, LAT-08 and MAL-06/07, each at or above both her buy list and our value. That gives 0 `neg_points`, a level-3 ladder deal and Sunday cash (109 now vs ≥ 170 target).
   - Effect: this is the gap to Team 13 (negotiating 24.3 vs 14.9). The ladder weight is not in the data.
   - Risk: our 3 Chato uncommon runs all finalled at 30-31, so he may never reach 26. Walk; it costs 0.
3. **Fix ask hygiene today via `trade.py`.**
   - Cancel MAL-02 → t01 (6426), since Team 1 is above us.
   - Re-price MAL-06 → t17 (6223, at 20 for +2.5). Team 17 bids 85 for MAL-09, so it is chasing its MAL page and is only 2.0 below us. Either price it at page level or move it to Pilar.
   - Reprice any ask unfilled for 10 min, per plan §4A.
   - Effect: avoids handing a team near us up to +50 for our +2 to +2.5.
   - Risk: fewer fills, about −2 to −5 `neg_points` forgone.
