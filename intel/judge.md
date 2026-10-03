# Judge (claude-opus-5-5, Sat 16:35)

## Verdict
**Holding against the leaders but falling in rank.**
- We are at 28.43 (+0.3 in 60 min), 1.5 behind #1. The gap was 1.94 at snapshot 680, and it narrowed because t14 lost 0.9.
- We dropped #5 → #6 when t1 (+3.6/60) passed us. t16 (+4.5) is 1.5 below us and t03 (+5.6) is 2.3 below.
- Since tick 632: neg_points 32.5 → 40.7, ladder 0.181 → 0.200.

## Our strategies: keep / kill / scale
- **Dealer sells (offer-only, price ≥ value): KEEP.**
  - LAT-08 → Chato at 14 lifted the ladder 0.188 → 0.200 at 0 neg cost.
  - The ladder kept rising past the ~0.15 "cap", so that [L] is wrong.
- **Buying from a dealer to resell to Pilar: KILL.**
  - SAL-06 bought from Abuela at 23 cost −2.7 neg (≈ −0.25 board).
  - The resale to Pilar at 25 left the ladder at only 0.181 → 0.188 (≈ +0.23 board): break-even, with risk.
- **Trading loop: KEEP.**
  - One accept since 15:29: the t08 swap, predicted +6.2, measured +6.2.
  - The errors in its log are from Friday night.
- **Public bids at ≤ value (SAL-07 20, MAL-08 15, LAT-02 3): KEEP.**
  - Their sibling bid (MAL-01 at 5) filled for +2.0 as maker.
  - How long they sat unfilled is not in the data.
- **Addressed spare asks (7 live): PRUNE.**
  - None of these asks has filled; the last spare sale was SAL-01 at tick 351 (+4.7).
  - MAL-02 and MAL-05 sit with t15, which has no cash (operator 16:31).
  - LAT-03 → t03 expires at tick 761.
- **Workshop: KEEP, but only when the output gets sold.** It added +11.8 collection value and 0 neg. MAL-06 has to sell at ≥ 17.5 to bank anything.
- **In-room MAL-09: KEEP refusing t10** (#3, it would close their page). The t15 reservation is dead: they have no cash.
- **Duels: KEEP.** Score 13.93; the last 10 show 9 deals and 1 no_deal (2523, buyer, limit 196).

## Check the scout
- **Holds:**
  - The can-give results (LAV-02 YES, LAV-04 NO).
  - #1-#6 within 1.5.
  - Ignore t04's RET-10 bid at 25.
  - The ladder is past 0.15.
- **Wrong, t16's LAT-09 trade:** the feed shows **t16 → t03**. t16 sold it and t03 bought it at 88, not the reverse.
- **Wrong, the +6.2 credited to Pilar's SAL-06 at 25:** that +6.2 is the t08 swap. Dealer gains clip to 0.
- **Wrong, "fill t16's bids with spares":**
  - t16 bids LAV-03 at 3 (value 3.2) and MAL-03 at 1 (value 7), and we hold no spare RET-07 or LAV-06. Every fill would lose.
  - The "+2.0 MAL-01" it cites as a past sale was a buy, not a sale.
- **Stale:**
  - Ask "10716" is now 11426.
  - Pilar's uncommon median is 19 over 7, not 18 over 6.
  - Dani's table still lists 2 copies of LAT-04 and RET-04 (the Workshop and the swap changed both).
  - t07's 9.5 is an estimate, not a bid.
- **Unverified:** t03's bid of 69 for LAV-10 (offer 11295) is not in the metrics bid list.

## The 3 changes with the highest expected gain
1. **Re-run the feeding check on every live ask to t16 and t03 now, and cancel what fails.**
   - Asks at risk: SAL-01 and SAL-02 → t16; LAT-03 and LAV-04 → t03.
   - Both teams were "safe" at 15:55, but they are now within 6 of us (1.5 and 2.3) and both collect SAL/LAT. One closer hands them up to +50 (≈ +4.7 board) for our +2.
   - Readdress to t09/t08/t07, or use public El Rastro, after `policy.py can-give`.
   - Risk: we give up about +2 per card.
2. **MAL-09 (worth 49): Dani asks t02 and t04 in the room whether it closes their MAL page.**
   - If it doesn't: post a maker ask at ~65 addressed to them. Expect ≈ +16 neg ≈ +1.5 board, the largest gain on our books.
   - If no team takes it: sell to Pilar with the floor raised from 55 to ~65. Her rare median is 69 over 3, and a higher price means more ladder share.
   - Risk: t02 and t04 are only ~5 below us, so a closer is barred under the gap-6 rule.
3. **Salamanca fever (18:03-20:03): sell only what we hold.**
   - Cards: reserved SAL-08 and SAL-03/04/05, plus SAL-07 if bid 10569 fills at 20.
   - Sell to Pilar at ≥ value with −2/−3 steps, offer-only, one thread per window, and no dealer buy-to-resell.
   - Expected: ladder +0.007 to +0.04 where a sale beats our weakest L3 slot, at 0 neg cost.
   - Risk: L3's best-3 slots may be full (the last SAL resale added only +0.007). Stop after one sale that doesn't move the ladder.
