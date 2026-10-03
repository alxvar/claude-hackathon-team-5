# Judge (claude-opus-5-5, Sat 11:19)

## Verdict
Gaining: #3 at 29.5 (+10.4 in 60 min). The leaders are t13 at 30.4 (+7.0) and t18 at 30.2 (+1.6), so the gap to #1 is 0.9.

## Our strategies: keep / kill / scale
- **Chato buys: kill.** RET-09 cost −10.0, RET-10 −9.0 and RET-06 −2.5. All 6 of our Chato deals were above list and none moved the ladder. The RET page is complete, so no Chato need remains.
- **Abuela via abuela_bot: kill unless a card is needed.** Below-list deals moved the ladder: +0.014 to +0.018 per common, and RET-07 only +0.004 as the 5th deal at level 1. Dealer gains never score.
- **Trading loop (loop.py): no measured value.** Its log shows only errors and an open at tick 285, with no accept or fill attributed since. Keep it stopped from 11:50 per the directive.
- **Addressed maker asks on v07: keep, but they don't fill by themselves.** There was 1 fill in ~95 ticks with 12-14 live offers: SAL-01 at 7, +4.7 (predicted +4.8). That fill came after Lucas's DM and t03's counter.
- **In-room deals (Lucas DMs): scale.** They produced RET-01 from t10 (+50.0, page closed) and SAL-01 to t03 (+4.7). These are our only two positive `neg_points` events since round 2.
- **Public bids 5590 (SAL-04 at 7, worth 9) and 5591 (MAL-03 at 5, worth 7): keep.** As maker the gain is +2 each, and cash stays at 102, above the floor.
- **Reciprocal venues (v10/v07): keep.** One v10 trade moved our market score 7.3 → 12.5 (+4.99).
- **Duels:** 34 practice duels all ended in a deal, and duel points are 0.0. Scored performance is not in the data yet; Duels I starts at 11:30.

## Check the scout
- **Holds:**
  - The gain arithmetic on every ask: LAT-08 +12.5, SAL-08 +2.5, LAV-02/03 at 3.2 each.
  - t01 is ~7.0 below us, so it fails the ≥10 rule.
  - No open bid exists for any spare (t02 bids 3 for LAT-03, which we value at 5).
  - t10 is +4.5 in 15 min.
- **Weak:**
  - "Raise to 28 for t03" rests on an estimate built from 1 team trade.
  - t03 countered our SAL-01 ask of 10 down to 7, so it bargains down, not up. Its cash is not in the data.
  - LAV-03 at 8 would still undercut the public LAV-03 asks at 9 (×2), so that raise is the more plausible of the two.
- **Wrong:**
  - "t13 +8.5 in 15 min, #2": the metrics show +1.6 and #1. t18 is #2 at 30.2, not #1 at 30.6.
  - "t02 bids 64 for SAL-09": the bid is 61.
  - "t17 is top 4": it is #10.
  - "Reposts must happen before 11:50": per directive 10:35, book.py keeps posting as maker during duels. Only accepts freeze.
- **Missed:**
  - t01 already bought MAL-07 at tick 311, so our offer 5440 (MAL-07 → t01) is a 2nd copy for them and is dead weight.
  - MAL-02 at 9 → t17 is undercut by public MAL-02 asks at 6-7 (×4), so it won't fill.

## The 3 changes with the highest expected gain
1. **Dani/Lucas walk every live addressed ask to its addressee before 11:30, and keep going during Duels I.**
   - Use only the file prices: t03 for LAT-08 at 25, SAL-08 at 25 and LAT-03 at 7; t17, t15, t07, t09, t06 and t16 for theirs.
   - Fills use their accept, not ours, so the duel freeze doesn't block them.
   - Effect: up to +37.2 `neg_points` if all 12 fill (LAT-08 alone +12.5), plus ~165 P cash toward Sunday's CHA page.
   - Risk: an addressee's lacks are unknown. All addressees are ≥10 below us except t01; fix that per change 2.
2. **Re-address MAL-07 (5440) from t01 to t15 at 20.** t15 collects MAL and is #12, 14.4 below us. Reprice MAL-02 (4988) to 6 or swap its addressee.
   - Effect: +2.5 on MAL-07, and turns a dead offer into a live one. At 6, MAL-02 would score −1 (its value is 7), so a new addressee at 9 is the only positive option.
   - Risk: none material; t15 is far below and not top 4.
3. **After Duels I, if LAT-08, MAL-06, MAL-07 or SAL-08 are still unsold, sell up to 3 of them to Pilar at ≥ our copy value.**
   - Pilar buys uncommons only, never commons. Level 3 currently holds 0 deals for us, and the ladder counts the best 3 per level.
   - Effect: 0 `neg_points` (dealer sale), plus cash and ladder at a higher-weight level.
   - Risk: whether Pilar sells move the ladder is not in the data (only "beat her list" [L]). A team sale scores +2.5 to +12.5 more, so Pilar is the fallback only.
