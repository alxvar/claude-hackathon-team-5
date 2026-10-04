# Judge (claude-opus-5-5, Sun 04:47)

## Verdict
**Holding at #3, stalled since tick 988.** Score 30.5, 7.1 behind Team 10 (37.6) and 0.8 behind Team 18 (31.3). Team 12 is 0.1 behind us (30.4). Our neg_points have stayed at 119.1 since the SAL close at tick 988 (+40.4), with no scoring deal in about 450 ticks. The game is closed until 09:00.

## Our strategies: keep / kill / scale
- **Dealer bot: keep, for fodder and CHA only.**
  - Dealer deals scored 0 or less all of Saturday.
  - Ladder went 0.437 → 0.483, but the board stayed flat on ladder gains ([L], Chief 17:45).
  - The last Pícaros sell (LAV-04) correctly walked at her opening of 4.
  - The 8 threads at ticks 1367-1370 carried no price from us. They were egg probes and scored nothing.
- **Trading loop: keep, but fix it first.**
  - Its last scoring accepts were 15:48 (+6.2) and 17:46 (+15.5).
  - Since then its log shows only errors. `unknown_card sobre_bienvenida` repeats every minute (22:41-22:45), which points to a bad entry in its book. There are also DNS failures from 22:55 to 23:24.
- **Our bids and listings: change how we post.** We had 414 listings and now 2 open offers, both addressed (LAV-03 → t04 and LAV-04 → t01, at 6). The measured fill rate is 0.3% for addressed offers against 3.5% for open ones (directive 00:37). Unless a buyer agreed on WhatsApp, post open.
- **In-room and team trades: scale.** Every point we gained Saturday afternoon came from team trades: the t07 swap (+15.5) and the SAL-06 page close from t08 (+40.4). Flags and ladder are spent.
- **Duels (Aleks): keep the code-first setup.** Session 3 finished 8 deals and 2 no-deals in the last 10. Duel score is 35.39.

## Check the scout
- **Holds:**
  - The CHA rares from the Pícaros at the first tick with `--offer-only` match directive 00:55.
  - The +50 cap is [V], and the SAL-06 close scored +40.4.
  - RET-09 t07 → t09 is approved. t09 is 7.2 below us, which passes the ≥ 6 rule.
  - The open bids (t09: SAL-06 at 20, SAL-10 at 68; t16: LAV-10 at 28) are all far below our values of 82.1, 122.6 and 177.1.
  - Team 6 fell 2.4.
- **Wrong: "+1 neg_point at most" for the LAV asks.** Each sale at 6 against our value of 3.2 is +2.8 as maker, so +5.6 if both fill.
- **Unchecked: the feeding rule on those asks.** t04 is 5.4 below us and t01 is 4.7, so both fail the ≥ 6 rule if either card closes a page for them. teams.md lists t04 as a LAV buyer.
- **Wrong: the flag probe date.** It was Sat 17:43, around tick 905, not tick ~1055.
- **Over-claimed: "flags spent".** The cap may reset on Sunday; directive 00:55 (5) says check.
- **Wrong: Team 18's LAT-10 at 72 was "under our 1× benchmark".** Rare book is 70, so 72 is above it.
- **Gap on cash:** "392 vs the 464 floor" misses the real constraint. After CHA we keep 392 − 242/250/282 = 150/142/110 P. The MAL close is GO only at ≥ 150 P (directive 01:40), so it is GO in case A only.
- **Gap on the round reset:** the scout ignores it. Round 2 reset neg_points and ladder to 0 ([V]). If round 3 does the same, 119.1 means nothing on Sunday and the first moves matter most.

## The 3 changes with the highest expected gain
1. **CHA at the round-3 event, in this order.**
   - Read `neg_points` and `ladder` right after the event to see whether they reset.
   - Start the Pícaros CHA-09/10 threads (`--offer-only`, check card and rarity) together with the capped public bids.
   - Open the silver pack (71.6) right after the release.
   - Effect: up to +50 for the page close (cap [V]), plus value − price on every below-value CHA buy.
   - Risk: Pícaros bait and switch, and CHA rares running out of print. The operator checks every accept by hand.
2. **Raise cash so the MAL close passes the ≥ 150 P gate.**
   - Before 10:30, post OPEN asks on a non-rival member venue:
     - LAT-03 and LAT-04 at 9, the LAT clearing level (others ask 9; our value is 5).
     - The 3 LAV-02 spares (1.3 each) at 6-10, in line with the others' LAV-02 ask at 10.
     - Re-post LAV-03 and LAV-04 open at 6, unless t04/t01 agreed by WhatsApp and the card is not their page closer.
   - Effect: case B goes from 142 to ≥ 150 P, which unlocks the MAL close (+30 np past our cap per directive 01:40), plus about +3 np per spare sold.
   - Risk: low fill rate. Reprice anything unfilled after 10 minutes, never below our value + 3.
3. **Fix the trader before its 09:00 restart, then fire v10 row #1.**
   - Remove the `sobre_bienvenida` entry from its book.
   - Restart with `CASH_FLOOR=464` (directive 00:40).
   - Fire RET-09 t07 → t09 on v10 first (+67.6 value created; probably reaches the full real-trades score alone).
   - Risk: t07 or t09 does not confirm in the room. Fall back to list rows #2 and #3 at 08:30.
   - Stop the trader, swaps and opps daemons at T−5 before Duels III.
