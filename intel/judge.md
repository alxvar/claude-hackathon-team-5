# Judge (claude-opus-5-5, Fri 22:17)

## Verdict
**Falling behind.** We are 16.4 (#8, −1.3/15 min). The gap to #1 Team 13 (27.8, flat) widened 10.1 → 11.4. Team 12 is +4.5, which fits its SAL-09 rare sale at 75 (tick 109). Teams 17 and 6 below us are +2.3 and +2.8, now 1.6 and 1.8 behind us.

## Our strategies: keep / kill / scale
- **Autoflip: kill (done).** LOG measured −11.8 on the MAL-07 buy against +5 to +8 on the sale. Discrepancy: metrics show `neg_points` 26.3 → 24.1 over 15 min, not → 14.5. The 14.5 reading is not reconciled with the metrics; operator should recheck.
- **Dealer bot (Chato): keep, change the mission.** Thread 214 offered asset 119 at 21, Chato held 13, and we walked. Walking was correct (13 is below MAL-07's 17.5 if 119 is MAL-07). But ladder is 0.064 and we have no Chato deals. Point it at buys at or below our value, not sales.
- **Trading loop: keep, verify it is alive.** Its only log line is a rate_limited error at 21:50. No accepts are logged since. Whether it took SAL-08 at 18 (tick 102) is not in the data.
- **Our bids: none open.** All 10 earlier bids are filled or gone. SAL-08 came from Team 12 (#2). Our gain there was about +4.5 before fee; Team 12's gain is not in the data.
- **LAV-04 listing at 9: kill.** One copy already sold at 9 (tick 106). If this is our last copy, its value is 13, so the sale scores −4. Other asks for LAV-04 sit at 10 unsold.
- **In-room trades: scale.** The LAV-09 holder search is moot: our bid was cancelled at 22:00, and an ask at 110 is now visible.

## Check the scout
- **Holds:** Team 13 leads at 27.8. Team 15 is a heavy LAT buyer (LAT×10) and sits below us. Team 17 bids 78 for MAL-09 (still live). Selling LAV commons at 9-10 scores negative.
- **Stale:**
  - Team 10's 110 bid for LAV-09 is no longer in the bids; a LAV-09 ask at 110 exists instead.
  - "Keep LAV-09 bid at 91" no longer applies; that bid is cancelled.
  - The MAL-10 bids (78/75) are gone, and SAL-10 filled t10→t13 at 70 (tick 98).
  - Team 17's 26 bids for MAL-07/08 were filled by t15 (tick 98).
  - Team 8 is no longer at 25.0; it is 22.7 (−2.3).
- **Unverifiable:** "prefer t9/t3". They appear in no trade or bid data.

## The 3 changes with the highest expected gain
1. **Close 3 Chato deals at or below our value (`abuela_bot.py --dealer chato --ladder`).**
   - Targets: LAV-06/07 at ≤29 each (worth 32.5). LAV-09 at ≤77 if he sells it (worth 91); this also blocks Team 10's LAV page.
   - Haggle down: ladder scores our share of his price range, not the list price.
   - Effect: fills level-2 ladder slots that count 0 today. `neg_points` effect is about 0 (LOG: below-value dealer buys gave about +0.3).
   - Risk: Chato's floors are not in the data. Never pay above value.
2. **Check `/api/me` inventory for rares that are bid above our value.**
   - MAL-09: Team 17 bids 78 (#9, below us), our value 49 → about +29.
   - LAT-09/10: Team 18 bids 55, our value 35 → +20. But Team 18 is #4, above us. Address offers to t17-tier teams first, and sell to Team 18 only if no other buyer appears.
   - Do NOT sell SAL-09 into Team 8's 55 (our value 63) or LAV-10 into Team 4's 85 (our value 91).
   - Risk: we may hold none (not in the data).
3. **Sell LAT spares (our lowest value, 0.5) and MAL spares (0.7) via `trade.py` with `to` set.**
   - LAT goes to t15. MAL-07 goes to t17 at about 21: MAL-06 traded at 21 at tick 103, while MAL-06 asks at 25 sit unsold.
   - Per card: LAT commons at 9-10 ≈ +4-5, LAT uncommons ≈ +8 (LAT-07 at 21 scored +8.7), MAL-07 at 21 = +3.5.
   - Cancel the LAV-04 listing at 9 in the same pass.
   - Risk: small per trade. Avoid filling for Teams 13 and 12.
