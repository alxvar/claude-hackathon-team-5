# Scout (claude-sonnet-5-5, Sat 09:51)

## Top 3 actions now
1. **Sell SAL-08 to a buyer other than t02, and re-check the other addressed asks (Operator, trader.py).**
   - Offer 3053 (SAL-08 → t02 at 33) is aimed at a team that collects RET/LAT and has 3 team trades. Its stated prices are "c 6 u 55 r 12", so it is not a SAL buyer.
   - The profile table lists Team 16 (#17, 10.5 below us) as the SAL buyer. Our SAL-08 is worth 22.5 to us, so a sale at 33 gains about +10.5 (+12 if t16 accepts as taker, who pays the fee).
   - Re-address offer 3053 to t16 at 33, or hold it for a SAL page-completer. Do this only after checking that t16 is not one card from a SAL page.
   - Effect: roughly +10 `neg_points`, about 1.6 board points at 0.16 each. Confidence: low-med.
2. **Fix the two 0 P offers, 3245 (SAL-03+SAL-05 → t16) and 3246 (MAL-02+MAL-04 → t07) (Operator).**
   - Both ask 0 P for cards we value at 9+9 (SAL) and 7+7 (MAL), so a fill loses about 18 and 14.
   - Cancel them, or re-post at ≥ our value plus 1: SAL at 10 each, MAL at 8 each.
   - Evidence: the clearing prices are common 9 (MAL 26 uncommon), t16 is at #17 and t07 at #16. A 0 P price looks like a typo or a bundle-parsing bug.
   - Effect: avoids −14 to −18 `neg_points`. Confidence: high that it is a loss risk, med that it is a bug.
3. **Bid for RET commons from teams at ≤ 9 (Operator, `trade.py`).**
   - Cards: RET-01, RET-02, RET-06 and RET-07, which we do not hold. RET-03, RET-04 and RET-05 we have.
   - Evidence: Abuela's last RET-02 deal closed at 10 against our 9, and RET-08 sat at 29 against our 14. Team 2 bids only 3-7 for RET commons, so the market sits at 2-7 and sellers are cheap.
   - Make each bid short-lived (≤ 20 ticks) and address it to the holder. Open the bid at 6. The RET common is worth 11 to us, so a fill at 6-9 gains 2-5 each.
   - Effect: a cheaper RET page than the Abuela route, plus a position for the last-card cap test. Confidence: med.

## What the climbing teams are doing
- **Team 2 (+6.3 in 15 min, the only climber).** It sold SAL-10 (rare) to t01 for 72 at tick 163 and LAV-07 to t14 for 55 at tick 161. It buys RET and LAT commons cheap (RET-04 at 7, RET-02 at 6). It sells high-value rares and uncommons, then re-bids low.
- **Teams 13 and 12 (leaders, both falling about 4-5).** Team 13 shows 30 deals and 5 MAL buys. Both are still on top on volume, so we cannot beat them by volume alone.
- **Rare trades at 70-80 are where the points are.** Examples: t16 bids 78 for SAL-10, and t02→t01 SAL-10 at 72. Smaller commons at 3-9 move the score by almost nothing.

## Threats
- **Team 2 is bidding on RET-09/10 at 11-13 and RET commons at 3-7.** Team 15 also bids 5 on RET-05. They compete for the same RET cards we need, at lower prices than Abuela charges. Team 2 is also the target of our SAL-08 ask.
- **Our ladder is only 0.032, and the 15-minute change is −4.6.** Everyone fell, so we stay #6 on relative position, but idle time costs us. Our maker book has gone unfilled for ~5 min.
- **Cash is 384 against a 370 floor.** The RET page needs about 280 P and the venue bond 270 P. Both do not fit, so the cap test and the venue decision compete for the same cash.
