# Judge (claude-opus-5-5, Sat 20:39)

## Verdict
**Falling behind the top two.** We are #3 at 31.6 with 0.0 over 60 min. T10 is at 34.0 (+1.9) and T6 at 32.6 (+1.1). At tick 1100 the gaps were 1.42 to T10 and 0.42 to T6; now they are 2.4 and 1.0. `neg_points` has sat at 119.1 since tick 988 (213 ticks). Our lead over #4 T3 is 1.6.

## Our strategies: keep / kill / scale
- **In-room team trades: SCALE.** SAL close +40.4 (tick 988), swaps +6.2 and +15.5. These are the only sizeable positive `neg` moves since the flags.
- **Trading loop: KEEP; restart once hold-writes clears.** Last fills were 15:48 and 17:46; there have been none since. It costs nothing while idle.
- **Maker asks: RETARGET.**
  - 5 asks are live and none has filled since 19:29. MAL-08 → t01 has gone unfilled for over an hour (24 → 20).
  - MAL-02 → t08 at 40 for a card worth 7 to us will not fill: t08 *dumps* MAL.
  - The best case is about +3 `neg` per spare.
  - LAV-04 → t01 (LAV collector, 7.9 below us) breaks the plan's ≥10-below feeding rule if it closes t01's page.
- **Dealer bot on spares: KILL.** LAV-04 → Pícaros walked at the final of 4, with 0 `neg` and 0 ladder. The ladder is capped for us (17:45).
- **Flags: KILLED.** Net +20; the 17:43 probe scored 0.
- **Egg hunt: stays stopped.** 3 tries, 0 events.
- **v10 market-making + rebate: KEEP.** Our current mm score is not in the data. The past record is +4.99, then −5.2 from a single t10 trade. T10's +1.9/h is consistent with market, but that is [L].
- **DENY line: KEEP dormant.** No trigger has fired.

## Check the scout
- **Holds:**
  - Pause and hold-writes are set (tick 1201).
  - The 18:40 contingency applies to Payday.
  - Recent RET-rare prices are right (t04 → t07 at 66, t06 → t07 at 77).
  - Don't sell LAV-06/07 into t13's 15 bids (they are worth 118.6 to us).
  - T2 is +2.6 over 15 min.
  - T7's volume is not lifting its score (21.2).
- **Does not hold:**
  - "LAV-02 ×3 priced at about 6": none of our open offers is LAV-02. Only LAV-03 and LAV-04 are listed at 6.
  - "T3 holds top Negotiating 24.49": that figure is from tick 850 and is stale.
  - "T10 relies on market-making": inference, not in the metrics.
- **Misses:**
  - Payday put our cash at **520** (floor 100). This is the main new lever and the scout ignores it.
  - The widening gap to T10 and T6.
  - The announcement is truncated ("Only deals sc…"). Its scoring condition is not in the data.

## The 3 changes with the highest expected gain
1. **Close the MAL page via team trades tonight.**
   - Situation: we hold 6/10. Missing are MAL-06 and MAL-07 (worth 17.5 each) and MAL-09 and MAL-10 (worth 49 each). The page bonus of 46.4 lands on the last card.
   - Buy from non-top-4 MAL dumpers (t13, t04, t12, t14), as a maker bid on v15, addressed to the seller.
   - Ceilings: uncommon ≤ 20 (Pilar's outside price), rare ≤ 56. Buy the cheapest card last.
   - Recent comparables: MAL-10 at 30 (t13 → t02), MAL-08 at 14 (t12 → t04).
   - Effect [L]: about +40–55 `neg` after roughly 10 of pack drag, ≈ +2–2.7 board. Cost ≈ 130 P, leaving ~290 P for CHA on Sunday.
   - Risks:
     - t09 is bidding 20 for MAL-06.
     - An overpaid rare is a −7 loss if the page never closes, so cap the total buy at the four cards and stop if a rare isn't secured by ~22:00.
   - Needs verifier sign-off (it moves >20 P).
2. **Swap spares for MAL cards with t04 (Dani, in person).**
   - t04 collects LAV and dumps MAL, sits 8.0 below us and is not a rival. Offer our LAV-02/03/04 spares (1.3–3.2 to us) for their MAL-06/07.
   - Effect: saves cash and gives ≈ +15 each against 1–3 given up. Both sides gain.
   - Risk: a LAV spare closes t04's LAV page. That adds roughly +2.5 board to a team 8 below us, and it does not pass us.
3. **Before any spend, get the full Payday text and re-score.**
   - Dani reads it at the front; the Market and the Analyst re-score per the 18:40 contingency.
   - Until then, skip the "vault and epics": dealer gains score 0, our ladder is capped and packs are never bought.
   - Cancel MAL-02 → t08. Move the remaining asks to the ≥10-below buyers (t09, t07, t16).
   - Risk: a scoring change the announcement implies is not in the data, so hold until it is known.
