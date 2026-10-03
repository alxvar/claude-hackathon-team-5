# Strategist (claude-opus-5-5, Sat 18:55)

## How the points really work
- **Negotiating (30)** = duels + ladder + team-trade value. Team trade = min(50, ΔV − price − taker fee) [V cap 50, n=2 commons]. Dealer deal = min(0, ΔV − price). The ladder scores best 3 deals per level, higher levels weigh more.
- Our ladder is spent for today [L: negotiating flat at 21.88 while ladder went 0.373 → 0.437]. Flags are spent too (≈3 scored per team). Today 1 neg_point ≈ 0.049 board (+40.4 → +1.99).
- **Market (30)**: bench efficiency + value created on our venue. The stall earns half; the mean of the top 3 earns full.
  - We sit at 7.5. The leaders sit at 9.15-12.5 [17:50], and no team is near 30.
  - Market is the field's weakest component and our biggest gap.
- **Judges (40)**: a 3-minute pitch, or 5 minutes for the top 3. It is the largest block, and the field has not yet competed on it.
- **Relative and per round** [V]: at a round start, `neg_points` and the ladder reset for everyone.
  - Round 3 runs from game hour 16.65 (Sun ≈11:34) to 20.08 (15:00), only 3.4 h, yet it carries 40% of the game.
  - Its benches at 17.0 and 19.0 (Sun ≈11:55, ≈13:55) are each a large share of round 3's bench score. Saturday spread its bench score over ~8 sessions.
- **Board now**: t14 31.8, us 31.7, t06 31.7, t10 29.7, t03 29.6. Our lead rests on the SAL close.
- **Pack drag is real money.** The silver pack fell 87.1 → 76.7 on the SAL close, cutting it from ~+50 to +40.4.

## Our winning strategy
**Own Round 3: the Chamberí page plus the Sunday benches.** Tonight, only cash and safety.
- **CHA is 1.6× for us, the top multiplier.** Nobody values CHA more than we do (some teams may tie).
  - Our values: CHA common 16, uncommon 40, rare 112, page bonus 106.
  - Dealer prices sit below these values. The data shows Abuela commons at 9, uncommons at 22-23, Picaros rare buys at a median of 57, and Chato rare finals at 86-87.
  - So every dealer buy builds the page at a zero loss and adds ladder points at a fresh round-3 ladder (we are level 5).
  - The closing team trade then books the bonus: up to +50.
- **Stop:**
  - ladder deals and flags today;
  - addressed page-closer bids (four bids, 0 fills);
  - the MAL and LAT pages;
  - the Workshop (scores 0);
  - any SAL, RET or LAV page card sale (all three pages are complete);
  - packs from dealers;
  - offers on rival venues;
  - any feed to t14, t06, t03 or t10.
- **Keep:**
  - the bargains daemon plus a hand-checked taker accept (maker read from the feed's `offer.listed`);
  - small maker asks above our value to non-rivals;
  - getting v10 trades to positive value created.

## Levers nobody is using yet
1. **Close CHA with an uncommon, not the cheapest common.**
   - If the cap is flat 50, the score is the same: min(50, 40 + 106 − p − fee) = 50 for p ≤ ~90.
   - If the cap is 5×book, it pays up to 146 − p (cap 125).
   - Every close in our data was a common or fell below the cap, so the form is untested.
2. **The sell-and-buy-back close (our verified LAV recipe, +50).**
   - Sell one CHA card to a non-rival team before the page is full, finish the rest via dealers, then buy that card back.
   - This makes sure a team holds the closer. CHA reaches teams only through packs; whether any team will hold the card we need is not in the data.
3. **A fresh ladder at levels 1-4 on Sunday.** It resets per round [V]. L3 paid ~3× L2 (Pilar +0.050). Reserve the inventory now:
   - LAT-03, LAT-04 and one LAV-02 spare for Picaros (L4, buys commons);
   - MAL-08 for Pilar (L3).
4. **Sunday 09:00-11:34 may still be round 2** (round 3 is scheduled at 16.65) [?]. If so, maker fills overnight and at the open still add to Saturday's round.

## Plan, anchored to the schedule
1. **Now (Operator).** Check 15513 (LAV-02 "for 0" to t01).
   - t01 collects LAV and sits 7.5 below us, so the feeding rule fails.
   - Keep it only if it is a swap gaining ≥3 for us and LAV-02 is not t01's closer; otherwise cancel.
2. **Now (Operator, trade.py).** Post maker asks at 9 on El Rastro or v15 to t07/t09 for the other LAV spares (LAV-02 ×1, LAV-03, LAV-04).
   - Keep the MAL commons asks.
   - Reprice after 10 min.
   - Expected ≈ +2 to +8 neg each, plus cash for CHA.
   - Cash 120 + the 150 grant = 270. The CHA build plus close costs ≈ 254-314 at the dealer finals above, so every P helps.
3. **Before 20:00 (game hour 11.0, bench).** Market lane confirms our venue is live. Dani lands one v10 pair from `v10-suggestions.md`: the buyer's multiplier above the seller's, no rival on either side. Expected mm 0 to +5 [L].
4. **20:39 (Duels II).** Aleks picks `--days-read`; the Duel Lab calls the day reading the biggest swing (right 0.47 vs backwards −0.18 per duel). Lucas and Dani draft the pitch during the duels.
5. **Tonight (Dani at the desk).** Ask two questions:
   - Is the cap flat 50 or 5×book?
   - Can a silver pack pull CHA after the release?
6. **22:00 (bench).** Supervise. Before the close, the Market lane replays bench recordings: board broker vs stall, including the hard bench.
7. **Sun 09:00.** Check `/api/clock` for the round and confirm `neg_points` has not reset (hypothesis B). Benches at 09:34 (hard) and 09:55 count for round 2.
8. **Sun 11:34 (CHA release, round 3; grant at 11:37).**
   - Open the silver pack before any CHA trade if it can pull CHA; if it can't, open it tonight to end the drag (after the Chief's OK).
   - Operator posts CHA bids at once.
   - Dealer buys at ≤ value with −2/−3 steps, never a first price: commons from Abuela, uncommons from Abuela/Chato, rares from Picaros/Chato.
   - Leave one card (an uncommon if the cap is 5×book) for a team-trade close. Expected +50 neg, or more if the cap is 5×book.
9. **Sun 11:34-12:30.** Ladder sales of the reserved items, only at ≥ our value:
   - Picaros: LAT-03, LAT-04, LAV-02 spare;
   - Pilar: MAL-08, only if she bids ≥17.5 after the fever breaks.
10. **Sun 11:55 and 13:55 (benches).** The venue must be live and supervised; downtime scores 0. Use the board broker only if replays show ≥ stall, else the stall.
11. **Sun 13:34 (Duels III, 10% decay, 12 ticks).** Close fast.
12. **15:00-16:00.** Pitch prep. Story: what we measured and how we used it: the cap, pack drag, below-list ladder, the flag cap, masked makers, 4-tick offer expiry.

## Hypotheses to test
- **A. Cap = flat 50 vs 5×book.** Cheapest test: the desk question; otherwise the CHA uncommon close. Metric: Δ`neg_points` > 50 means 5×book.
- **B. Sun 09:00-11:34 is still round 2.** Test: one maker fill at ~09:10. Metric: no `neg_points` reset before 16.65, and the board moves.
- **C. Silver pack pulls CHA after the release.** Test: the desk or the pack catalog. Metric: the contents' sets.
- **D. Picaros/Chato sell CHA rares below 112.** Test: open a thread at the release with a −2/−3 step protocol. Metric: the final price.
- **E. Round-3 ladder moves the board again.** Test: negotiating before and after the first L3/L4 deal.
- **F. Pilar after "the fever breaks" bids <17.5 for MAL-08.** Test: a probe thread on Sunday. Metric: her standing bid; walk if below value.
- **G. Board broker ≥ stall on the hard bench.** Test: Market lane replay of the recorded bench. Metric: efficiency vs the auto stall.
