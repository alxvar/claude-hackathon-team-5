# Judge (claude-opus-5-5, Sat 13:32)

## Verdict
Mixed. Over 60 min we closed on #1 (we +1.8, t14 +1.1; gap 3.35 → 2.65). Over 15 min we lost 1.1 to t14 (we −0.8, t14 +0.3). neg_points has been flat at 35.2 since tick 404 and the ladder flat at 0.181 since 12:45, so we score nothing new while t10 (+4.1) and t6 (+4.6) climb.

## Our strategies: keep / kill / scale
- **Pilar L3 sells (dealer bot):** **scale**. Ladder went 0.122 → 0.181 at 0 neg cost (MAL-07 +0.050, MAL-06 +0.040, SAL-08 +0.019). The +0.019 slot is the one to replace.
- **Chato L2 buy at list 26:** **kill**. He held 33 → 32 against our 26 (thread 805), and our 6 Chato buys above list never moved the ladder. A buy at his 30-31 final costs about −5 to −8.5 neg for 0 ladder.
- **Abuela SAL-06 at cap 25:** **change the cap**. Three threads (her 29 → 25) produced nothing. At 25 we pay −2.5 neg (value 22.5), and L1 is saturated: the 4th Abuela deal added only +0.003. Cap at 22.
- **Trading loop (`loop.py`):** **keep; it costs nothing**. It has made 0 accepts all Saturday, and the El Rastro asks hold nothing near our value + 3.
- **Spare-ask book (9 asks, 5-11 P):** **keep, but re-address**. No fill since tick 404 (~1.9 h), and commons now clear at 5 (ticks 595-610). Most addressees fail the feeding rule (≥ 10 below us): t04 is 4.8 below and collects LAV, t03 7.6, t09 6.4, t06 4.2, t15 6.2, t16 5.7. Only t07 (#17, 10.8 below) passes.
- **Earlier team trades:** these scored best. RET-01 from t10 at 20 gave +50 (cap), SAL-01 to t03 at 7 gave +4.7, MAL-03 from t04 at 5 gave +2.0.
- **v10 venue (Lucas plan B):** **keep, positive-only**. It has measured +4.99 and then −5.2 (SAL-07 t10→t15), so it is net negative so far.
- **Lunch bargain watch:** **keep**. No ask qualifies: the best is LAT-08 at 24-25, worth 12.5 to us.

## Check the scout
- **Holds:**
  - sobre_plata is unopened (92.9).
  - RET and LAV pages are complete.
  - No bargain target exists.
  - Pilar paid 140 for LAV-11.
  - The t15↔t07 0 P swaps happened (ticks 607/613/616).
  - t14 sold RET commons at 9 (591-598).
  - t4 bids 26/27 for RET-06/08.
  - We have no ask to t07.
- **Stale:**
  - The gaps. It says "t14 leads by 2.2, t18/t10 at 29.2"; the metrics show 2.65, with t18 at 28.8 and t10 at 28.9.
  - "t12 +1.3/15 min": the metrics show −0.3/15 and −2.6/60.
  - "t15 17 team trades": teams.md shows 22.
  - "Pilar median 18 over 6": the metrics show 5 deals.
- **Wrong:**
  - "Team 6 is buying SAL": it sold SAL-03 to t14 (tick 600).
  - "Sell any spare uncommon to Pilar": we hold no spare uncommon. Every uncommon is a page card worth 100-118, so this applies only to what the pack yields.

## The 3 changes with the highest expected gain
1. **Open sobre_plata now, then route its contents to the empty ladder slots (Operator, offer-only).**
   - Selling to Chato above his opening bid at ≥ our value refilled an L2 slot before: LAT-08 at 14 gave +0.017 at 0 neg, and our L2 slots are empty.
   - Uncommons go to Pilar with −2/−3 steps to replace the +0.019 slot.
   - It also removes the 1-4 point pack drag [L].
   - Effect: up to ~+1.2 board per filled L2 slot (directive A estimate). Risk: the contents are not in the data, and a MAL uncommon (17.5) is below Chato's 14-16 bid, so it goes to Pilar only.
2. **SAL-06 from Abuela at ≤ 22, then to Pilar at ≥ 23 in small steps (16:00-18:00 per plan A).**
   - 0 neg on both legs. It replaces the SAL-08 slot (+0.019) with a +0.040-0.050-type deal, ≈ +0.7-1.0 board.
   - Risk: Abuela may not go below 25. Then walk, never pay 25.
3. **Re-address the spares (Operator).**
   - LAV-02/03/04 and LAT-04 go to t07 at 7-8, the only buyer that collects LAV/LAT and passes the ≥ 10 rule.
   - Hold MAL-02/04, SAL-01 and LAT-03 at value + 2. Drop any ask below our value.
   - Effect: ~+2 to +4 neg per fill (≈ 0.2-0.4 board each), and it removes the risk of handing t04, t03 or t09 a +50 page close (≈ +4.7 board, enough to put t04 level with us).
   - Risk: t07 may not buy. Then the asks expire, which is still better than feeding a team close behind us.
