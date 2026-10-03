# Judge (claude-opus-5-5, Sat 22:49)

## Verdict
Falling behind: #4 at 30.49 (−0.2 in 15 min, −0.7 in 60 min). Team 10 leads at 37.7, 7.2 ahead. Team 18 passed us (+1.3 in 60 min). `neg_points` has been flat at 119.1 since tick 988, about 430 ticks with no scoring deal.

## Our strategies: keep / kill / scale
- **Trading loop: fix.** It has had no accept since 17:46 (5 h). From 22:41 it logs `unknown_card sobre_bienvenida` every minute, so its card list is broken. Fix that before Sunday 09:00.
- **Dealer bot: keep it parked.** The last priced thread (Pícaros LAV-04, 19:04) walked correctly at a final of 4 against our floor, with neg and ladder unchanged. Ladder and flags are spent: `negotiating` stayed flat across ladder 0.373 → 0.437. Use dealers only for the CHA page at ≤ our value.
- **Egg threads: done.** Abuela gave MAL-06 plus a badge. The other four dealers gave nothing, and the round-2 retry gave nothing. Stop.
- **SAL-11 bid (115 → t04): keep.** It has been unfilled since about 21:45. Our value is 162 (first copy), so 162 − 115 = 47, under the cap, before pack drag. The overnight re-post (job bz665n6tg) is correct.
- **Ask 19980 (MAL-03 → t09 at 9) and 19982 (MAL-08 → t01 at 20): kill both.** Both are single copies on the MAL page, which now needs only MAL-07/09/10 (page bonus 66.25 × 0.7 ≈ 46). Each sale gains +2 to +2.5 and breaks the Sunday MAL close. They also break the club rule "duplicates only".
- **Ask 19979 (LAV-03 → t04 at 6) and 19981 (LAV-04 → t01 at 6): keep only after a feeding check.** These are true spares (3.2 each). But t04 and t01 both collect LAV and sit only 5.3 and 4.7 below us, not the ≥ 10 the feeding rule requires. Pull them if either card could close a LAV page for the buyer.
- **Maker book size: scale.** We have 5 live offers against the plan's 20-30. The spares that qualify are LAV-02 ×2 (1.3 each), LAV-03 and LAV-04 (one extra copy each).
- **In-room trades / v10 desk: no measurable result.** Market is 7.5, the stall level, so real trades are scoring 0 so far. The RET-09 t08 → t09 match (21:40) does not appear in the trade list. Club Castizo starts Sunday.
- **Duelist: keep.** Duel points went 33.19 (22:23) → 35.39. Apply the Duel Lab's Duels III parameters (+1.85 pts simulated over 68 duels) only after Aleks reviews them.

## Check the scout
- **Holds:**
  - SAL-11 math (162 value, ≤ 125 cap, floor 260).
  - Our score is slipping and neg is flat.
  - Team 1 gained +3.0 in 60 min.
  - t10 bids 210 for LAV-11.
  - Never route trades to v07.
  - Don't sell RET-11 to t16 at 99 (it is worth 198 to us).
- **Fails:**
  - Offer IDs 19656/19657/19658 are stale; the live ones are 19979-19982.
  - It says t12 bought SAL-09 from t09 and t01 bought LAT-10. The trade list shows the reverse: t12 sold SAL-09 to t09, and t01 sold LAT-10 to t12.
  - "A RET-09 ask at 84" does not exist. There is no RET-09 ask; 84 was RET-10 sold t06 → t04.
  - "t18 is not a dealer buyer" is wrong: t18 has 23 dealer trades.
  - It calls t12 #5; it is #3.
  - It talks about "t09's live asks", but t09 only has bids.
- **Missed:**
  - The asks it endorses sell MAL page cards.
  - The top four has changed: t18 is now #2 and t06 dropped to #6 (−2.4 in 15 min). Dani's feeding list (22:35) is stale; add t18 to never-feed.

## The 3 changes with the highest expected gain
1. **Cancel 19980 and 19982 now; re-list only true duplicates (LAV-02, LAV-03, LAV-04) to teams ≥ 10 below us.** Teams that qualify now: t15, t02, t09, t16, t07.
   - Effect: protects the Sunday MAL close (up to +50 on a fresh round's neg) for a cost of about 4.5 neg points tonight.
   - Risk: none material.
2. **Sunday 09:00, in this order:**
   - Fix the loop's `sobre_bienvenida` bug.
   - Open the grant pack before any trade, to avoid pack drag.
   - Start the CHA page. CHA values are above dealer prices: rares are worth 112 to us.
   - Effect: per the Analyst (§3g), +3.2 to +5.6 final, the largest lever left.
   - Risk: CHA rares are scarce and contested. Buy rares first, from teams.
3. **SAL-11: if t04 hasn't filled by about 09:15 Sunday, counter at 125 (the guardrail cap).**
   - Effect: +37 to +47 neg in round 3, minus pack drag (SAL-06 lost about 8 to drag). Cash 392 − 125 = 267 stays above the 260 floor, and the +150 grant brings it to 417 against CHA's ~330.
   - Risk: t04 sells SAL-11 elsewhere first. Cap the time spent chasing at 30 minutes, then put the cash into CHA.
