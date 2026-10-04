# Judge (claude-opus-5-5, Sun 05:18)

## Verdict
Holding, not gaining: #3 at 30.5, 7.1 behind Team 10 (37.6), 0.8 behind Team 18 (31.3), only 0.1 ahead of Team 12 (30.4). The game has been closed since tick 1445, so the 60-min change is 0.0 for everyone.

## Our strategies: keep / kill / scale
- **Page closers via team trades: SCALE.** They are our whole Saturday gain. SAL-06 from t08 at 28 scored +40.4 (not 50; the unopened pack's drag cost it). RET-01 scored +50 at the cap.
- **Swaps with other teams (trader loop): KEEP.** Two accepts: SAL-07↔LAT-01 +15.5 and SAL-04↔RET-04 +6.2. Fix the config before restart: `unknown_card sobre_bienvenida` errored every minute 22:41-22:45.
- **Dealer bot: KEEP for CHA buys and fodder only (directive 00:44).** Dealer deals add nothing to `neg_points` (min 0). The last thread, Pícaros LAV-04, correctly walked at their opening 4. The ladder (0.483) did not move the board from 0.373 to 0.437 [L, Chief 17:45].
- **Addressed cheap asks (19979, 19981 LAV-03/04 at 6): KILL the addressed form.** They expire at tick 1455. Addressed offers fill 0.3% vs 3.5% for open asks (directive 00:37).
- **Flags: DONE.** Net +20; the 8th flag scored 0 after 62 min, so the cap did not reset.
- **Listings volume (414 listings, 17 team trades): no evidence that volume scores.** Keep only priced, open asks of spares.

## Check the scout
- **Holds:**
  - Game closed; asks expire at 1455.
  - Cash 392 vs CHA need 242-282.
  - Pícaros rare median 55 (n=1 in the data).
  - t12 is 0.1 behind.
  - t18 bought LAT-10 at 72 vs t12's 86.
  - VC from RET-09 t07→t09 counts only toward the 7.5 real-trades share.
  - t07's holding is unconfirmed (owners masked).
- **Wrong, size of the gain:** "+0.5 per spare" is too low. Selling LAV-03/04 at 6 as maker (worth 3.2) gives ≈ +2.8 each.
- **Wrong, where CHA rares score:** "rare worth 112 vs Pícaros 54" implies a gain. Dealer buys score 0 (gains clipped). CHA value only scores through team trades and the page closer, which is capped at 50.
- **Wrong, direction of t12's SAL-09 trade:** t12 SOLD SAL-09 to t09 at 70 (t12→t09), it did not buy it.
- **Wrong, RET-11 logic:** "RET-11 can be undercut by teams" is backwards. t12 paid 216 (> our 198 hold), so teams pay above it. Still never sell it to t12 (top 4).
- **Stale:** "Team 18 Δ +0.8" is from teams.md at 23:08. Metrics show +0.0 over 60 min.

## The 3 changes with the highest expected gain
1. **Close the CHA page through a TEAM trade and open the silver pack right after the CHA release (directive 00:55).**
   - Buy every card except the cheapest common at ≤ value (dealers score 0, teams score value − price).
   - Leave one CHA common as the agreed, addressed closer from a non-rival.
   - Before the closer, confirm the pack (71.6) is opened. Drag cost ≈ 9.6 on the SAL close (40.4 vs 50).
   - Expected: closer ≈ +50, plus value − price on each team-bought CHA card.
   - Risks: print runs run out (both rares from Pícaros at round 3's first tick), and Pícaros tricks. The Operator must restart the dealer bots so they load trick guard e461e3b, and keep `--offer-only` on.
2. **Turn our spares into CHA cards via swaps and open asks.**
   - Spares: LAV-02 ×2 (1.3), LAV-03 (3.2), LAV-04 (3.2), LAT-03/04 (5).
   - Post OPEN asks on a non-rival member's venue at 9 (the Rastro common clearing price) as maker (no fee).
   - Offer card-for-card swaps for CHA commons to teams that don't collect CHA, via Dani with the offer live first.
   - Expected: +3-6 per cash sale. A swap for a CHA common (worth 16 to us) is up to ≈ +11-15, the same scale as Saturday's +15.5 swap.
   - Risk: feeding a top-4 team. Check the feeding rule before any card that completes a page for the buyer.
3. **Duel windows exactly per directive 01:30.**
   - Pin duelist sha 29aa1be at 08:00.
   - `daemons.sh stop trader swaps opps` at T−5 before Duels III and the Final; restart at `duels.finished`.
   - Expected effect: not in the data. Duels are 35.39 of our score inputs, and 2 of the last 10 duels ended with no deal.
   - Risk: missing the CHA fast start before 10:55. Finish the CHA threads before the Duels III window.
