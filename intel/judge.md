# Judge (claude-opus-5-5, Sun 09:37)

## Verdict
**Slipping.** We are #4 at 30.15 (−0.3 in 15 min). t12 is +1.0 to 31.5, and t18 passed us at 31.1, so the #3 spot that the 09:28 directive told us to defend is lost. t10 still leads at 33.7 but fell 3.9. Our `neg_points` this round are 0.0 with 0 team trades. t18's jump came from one team trade, CHA-01 bought from t13 at 72, which closed its CHA page (likely the +50 cap).

## Our strategies: keep / kill / scale
- **Abuela CHA commons: keep, but only as page building.**
  - CHA-01 to CHA-04 cost 8, 9, 8, 9 against a value of 16, with `neg_points` flat at 0 (dealer gains are clipped).
  - Level 1 is full: the best 3 deals are 8, 9, 8, so CHA-04 at 9 and the open CHA-06 thread add no ladder.
  - Rule: never buy the page's last card from a dealer. The closer scores only through a team trade.
- **Pilar fodder: keep, one slot left.** Ladder went 0.075 → 0.115 → 0.148 → 0.168 (LAT-06 at 18, LAV-07 at 17), with no neg cost. Level 3 has 2 of 3 deals filled. The board effect of the ladder is [L] only (Chief's 17:45 note).
- **Pícaros: done, keep the result.** CHA-09 at 55 against a value of 112 cost 0 neg. LAV-04 was walked correctly (their final 4 was below our floor of 5).
- **Public CHA bids (CHA-08/06 at 22, CHA-05 at 9): keep, but they are not working.** 0 fills. No team has a CHA ask on the boards.
- **LAT-06/07/08 bids at 9: kill unless they feed level 3's last slot.**
  - 0 fills, and the only asks for these cards sit at 30.
  - Worth at most about +3.5 each (LAT uncommon value 12.5), and nothing as a score once level 3 is full.
- **RET-11 to t13 at 248 (offer 20815): scale it, it is our only live +50.** Value 198, not a page card, and t13 is #7 at 24.6. Keep the planned single re-post at 235.
- **Trading loop: unproven this round.**
  - Its log has no Sunday entry after the 00:36 "closed" event, and there are 0 accepts since the R+10 restart.
  - Saturday's last two accepts gained +6.2 and +15.5.
  - Check that it is actually alive (see change 3).
- **In-room trades: none this round.** t18's +50 came exactly from one of these. This is the gap.

## Check the scout
- **Holds:**
  - Abuela commons close at ≤ 9 (confirmed four times).
  - Pilar fodder gives about +0.02 ladder per deal (+0.022 and +0.033 measured).
  - The CHA bids are unfilled because no seller exists.
  - t12 is the main rival.
  - Never sell SAL-09/10 below 122.6.
- **Stale or wrong:**
  - "We're #3 (+0.3)" is false: we are #4 at −0.3, and t18 is above us.
  - t12 shows "+2.0"; the metrics show +1.0.
  - Thread 2258 was CHA-01, not CHA-02.
  - Bid 20536 has been replaced by 20793.
  - LAV-07 is already sold (at 17, ladder 0.148), so action 3 is already done.
  - t03's SAL-10 bid is gone: t03 bought SAL-10 from t13 at 108.
- **Risky:** action 1 includes CHA-05 from Abuela. That is harmless only if a team-bought card ends up last. The Chief's plan, with CHA-05 last from a team, is the right one.

## The 3 changes with the highest expected gain
1. **Close CHA with a team trade now, copying t18 (expected +50 neg, the largest single lever).**
   - Finish CHA-06/08 at Abuela at ≤ 40 (`cha_close.sh` already does this).
   - Meanwhile Dani asks the room who holds a spare CHA-05, CHA-06 or CHA-08. t13 sold CHA-01, so it likely holds CHA spares.
   - Make whichever card a non-rival holds the last one. Post it on El Rastro, addressed, at value-when-last − 50 with the seller's fee added (07:25 directive).
   - Risk: the Chief's 72 bid targets t13, which is on `policy.rivals`, and 07:05 (3) says bids above the public limit must go to non-rival teams. Have the Chief confirm in writing, or prefer a non-rival holder. If nobody holds the card, the page stalls at 9/10.
2. **Sell surplus to teams at our value + 50 for capped trades (+50 each).**
   - RET-11 is live. If t13 lets offer 20815 expire at tick 1552, re-post once at 235 to a non-top-4 RET collector (t02, t07, t16).
   - Never sell to t10, t12, t18 or t03.
   - Risk: a fill at a lower price still scores 50 only if the price is ≥ 248 (198 + 50). Below that, we get price − 198. Do not drop below 198 (01:40 directive).
3. **Confirm the trader and opps processes are running and logging on HEAD 46dc399.**
   - A dead loop means missed maker fills, which are the only other source of neg this round.
   - Cost: one `daemons.sh` status check.
   - Risk: none. If they are down, restart them with the floors (110).
