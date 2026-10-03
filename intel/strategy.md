# Strategist (claude-opus-5-5, Sat 13:16)

## How the points really work
- **Board formula.** Board = Neg 30 + MM 30 + Judges 40. The game part is (0.5·Fri + Sat + Sun)/2.5, so Saturday and Sunday each weigh 40%. The live board is (0.5·Fri + Sat)/1.5 [V]. Scores are relative, so standing still means falling.
- **Neg rates** (12:13 directive). 1 neg_point ≈ 0.094 board. +0.01 ladder ≈ +0.33 board. Duels are 40% of Saturday Neg.
  - Team trades are capped at 50 per trade [V].
  - Dealer deals only subtract from neg [V] and pay only through the ladder.
- **Our ladder: 0.181.**
  - L1 (Abuela, 5 deals): 0.055.
  - L2 (Chato): 0.017 from LAT-08 sold at 14. **2 of 3 slots are empty.**
  - L3 (Pilar): 0.050 + 0.040 + **0.019** (weak slot).
  - Measured routes into the ladder:
    - Dealer buys below the menu list (Abuela).
    - Dealer sells above the dealer's opening bid (Chato at 14, Pilar at 19).
    - Chato buys above list never counted (6 of 6), and he refused a buy at list 26 at 13:08.
- **MM rules.**
  - Market Test: the stall earns half; full points go to the top-3 mean. 12:58 decision: no board venue.
  - Value created on our venue: board contribution capped at +5.0 and floored at 0 [V].
  - Ours sits at **mm −5.2** (SAL-07 dump to t15), so it currently contributes 0 on the board.
- **Where the field is weak.**
  - Venues had 0 trades Friday; nearly all 97 team trades go through El Rastro.
  - t14's measured edge is **+3.10 from one trade on its stall**. That is more than our whole gap to #1: 30.4 − 29.0 = 1.4.
  - Ladder L2 slots: every Chato buy fails to count.
- **Our neg_points have been flat at 35.2 since tick 404.** The team-trade engine is idle.

## Our winning strategy
1. **Claim the value-created component (+5 board cap) before anyone copies t14.**
   - Route collector←dumper trades between other teams onto v10.
   - Since we are below the board floor, further negative trades on v10 cost no board points now [L, floor].
   - One rare moving from a 0.5 holder to a 1.3 holder creates roughly 50 of value. That should cover our −5.2 and reach the cap [L: mm-to-board ratio not in data].
2. **Fill the ladder with cash-neutral cycles.**
   - L2: buy LAT uncommons from teams at ≤12 (worth 12.5 to us), then sell them to Chato at 14, offer-only. This adds neg and cash and fills 2 slots (≈ +1.1 board).
   - L3: in the Salamanca fever, sell a SAL uncommon bought from Abuela at ≤22 to Pilar at ~30. This costs 0 neg and replaces the 0.019 slot.
3. **Sunday is 40% of the game and everything resets.**
   - Chamberí at 1.6×: every CHA card bought from a team below value scores. Rare 112 vs ~75 from teams is about +37 each.
   - Close the page with a team buy for +50.
   - Redo the 3×3 ladder early with pre-stocked LAT/MAL uncommons.
- **Stop:**
  - All Chato buys, including the L2-at-list attempt.
  - Epic chases.
  - Any board venue.
  - 4-6 P asks on cards that might be someone's page-closer.
  - SAL-01 → t06 (t06 is only 4.9 below us; cancel 8776 unless Dani confirms it isn't t06's closer).

## Levers nobody is using yet
- **Routing other teams' trades onto v10.**
  - Evidence nobody does it: venues had 0 trades Friday; t14 got +3.10 from a single trade.
  - Pitch (Dani/Lucas): "Post it on v10: same price." Add "no El Rastro 5% + 1 P fee" only if v10's fee is 0; our stall's fee is not in the data, so check first.
  - Targets come from the rival profiles, with no top-4 party:
    - SAL rares → t06, t08, t17.
    - LAV → t07, t04.
    - RET → t02, t09, t15, from dumpers t13, t17, t06, t08.
- **L2 through dealer sells of low-multiplier uncommons we buy cheap.**
  - Evidence: LAT-08 at 14 gave +0.017 at 0 neg.
  - Chato's uncommon buy final is 14; Abuela also buys uncommons at 13. Dumpers' outside option is about 13, so a 12-13 maker bid is plausible. Fill rate is not in the data.
- **Salamanca fever cycle.** Pilar pays 25% over book on SAL (uncommon ≈ 31).
  - Abuela's SAL-06 thread is already at 25 vs our 22.
  - Buy ≤22 (0 neg, below list, so L1 may also tick), sell to Pilar at ≥28 with −2 steps (+6 cash or more).
- **Pre-stocked Sunday ladder inventory.**
  - Buy LAT/MAL uncommons Saturday evening below value. This is positive Saturday neg.
  - Sell them to Chato/Pilar on Sunday as the first deals of the reset round.
  - Whether others pre-stock: not in data.
- **LAV spares as page-closers.** If t07 or t09 lacks LAV-02/03/04, sell at 30-40 instead of 6. That is +26.8 neg vs +2.8 per fill.
- **Flags.** "A correct flag scores." Nobody's usage is in the data, and neither is the size of the reward.

## Plan, anchored to the schedule
Wall times assume 120 ticks per game hour; Saturday checks out (hour 16.152 = 23:00).
- **Now (Operator):**
  - Close Abuela SAL-06 at ≤22 (thread 8787) and hold it for the fever. A second SAL uncommon at ≤22 only if Abuela offers it.
- **Now (Operator, trade.py):**
  - Addressed maker bids at 12 for LAT-06/07/08 to t17, t01, t13 and t09. Never public, because t14 and t18 collect LAT.
  - On the first fill: Chato sell, offer-only at 14, alone in its window. Continue only if Δladder > 0. Max 2 slots; walk above 14.
- **Now (Dani):**
  - Ask t07 and t09 whether LAV-02/03/04 closes their page. If yes, the Operator re-lists at 35 addressed, as maker.
- **Now and all afternoon (Lucas/Dani in the room):** pitch v10 routing for collector←dumper rare and uncommon trades.
  - Builder's radar pages each v10 fill; log Δmm_points per trade.
- **13:48 bench (hour 7.0):** stall only; no action.
- **15:30 (Aleks):** Duels II. Integrative days, ≤3 rounds (per directive).
- **15:57-17:30 (Operator), Salamanca fever:**
  - Pilar sell of the SAL uncommon. Open high, step −2, let her climb, then offer her standing bid.
  - Second sale only if the first beat 0.019.
  - Pilar buys no commons; never sell RET/LAV page cards.
- **18:27 (Aleks):** Duels II, 68 duels.
- **Evening (Operator):**
  - Carry 2 LAT uncommons at ≤12 into Sunday for Chato.
  - Keep cash ≥170 at close (11:35 directive). Projection: 184 + fever margin − ~25 inventory.
- **Sunday 09:00 (Operator):**
  - Re-read /api/clock and /api/schedule. If game hour = 120 ticks, events fall at:
    - CHA release ≈ 09:15.
    - Duels III ≈ 10:15.
    - **Abuela closes ≈ 11:45** [L].
  - Then, in order:
    1. Open sobre_plata after the CHA release (already planned).
    2. Ladder sells first, for cash and the reset round.
    3. CHA buys from teams below value.
    4. CHA rares from teams ≤100 or Chato ~86-90 (0 neg).
    5. Abuela CHA commons/uncommons below list.
    6. Last card: a CHA common from a team → +50.
- **Sunday (Lucas/Dani):** keep routing to v10 and give the judges' pitch.
  - Story: measured fact store, the cap discovery, the ladder model, value-created routing.

## Hypotheses to test
- **v10 value created converts to board at the cap.** Test: one routed positive rare trade. Decides: mm_points and the board MM column.
- **Negatives below the floor are free.** Test: next v10 dump. Decides: whether board MM stays flat.
- **Chato L2 sell of a team-bought LAT uncommon at 14 counts.** Test: one cycle. Decides: Δladder ≈ +0.017.
- **A Pilar fever sale beats the 0.019 slot.** Test: one SAL sale with small steps. Decides: Δladder > 0.
- **Abuela SAL buy at 22 (below list 25) lifts L1.** Test: the open SAL-06 thread. Decides: Δladder.
- **Pack contents are drawn when opened.** Test: open sobre_plata after the CHA release. Decides: `pack.opened` shows CHA cards.
- **Abuela gifts recur Sunday after a day's 5th deal.** Test: count Sunday Abuela deals. Decides: a `gift.given` event.
- **A correct flag scores.** Test: flag one dealer message only where a logged "last number"/final was contradicted in the same thread. Decides: Δneg_points; skip if no verbatim case.
