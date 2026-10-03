# Judge (claude-opus-5-5, Sat 22:01)

## Verdict
**Falling behind.** We are #4 at 30.6, down 1.0 in 60 min, while t10 gained +4.5 to 38.5 (7.9 ahead) and t12 gained +2.5 and passed us. `neg_points` has sat at 119.1 since tick 988 (333 ticks with no scored deal); only duels are moving (13.93 at 21:17 → 25.75 now).

## Our strategies: keep / kill / scale
- **Duelist (Duels II): keep.** It is our only rising component (+11.8 duel points in ~40 min; wave 2 closed 5/5 or 6/6 deals). Give it priority on accepts and rate limit.
- **Dealer bot: keep off.**
  - Last thread (19:01, LAV-04 at Pícaros) walked at 4 vs our floor 4. `neg_points` and ladder unchanged.
  - Dealer gains clip to 0, and the ladder is flat for the board (Chief 17:45).
  - The one good dealer deal was the RET-11 buy at 128 (value 198, 0 neg, L4).
- **Trading loop (`loop.py`): keep, but it is idle.**
  - Last accepts were 15:48 (+6.2) and 17:46 (+15.5); nothing in 4+ h.
  - It hit rate limits at 21:50 on the shared 5 req/s.
- **Our bids and listings: fix.**
  - SAL-11 bid 18605 expired unfilled; it is re-posted as 18977.
  - The four sells are small (+2 to +3 each).
  - Two of them, MAL-03 (18963) and MAL-08 (18965), sell our **only copies**: MAL-01..05 + 08 are page progress for Sunday's MAL option (21:20, priority 3). Others ask MAL-01/03 at 12, so rebuying costs more than the 9 we would get.
- **Bot-to-bot team chat pings: kill.** 0 of 4 replied (t09, t08, t04, t01); two closed the thread.
- **v10 swap desk / matchmaking: scale, in person.**
  - No v10 trade between other teams is visible since the 21:30 rebate.
  - The big-screen ads have no measured fill yet.
  - `mm_points` / real-trades value is not in the data.
- **DENY reactor: keep with the `pages_complete` filter.** The 21:39 RET-02 target was stale and correctly not bought.

## Check the scout
- **Holds:**
  - SAL-11 at ≤125 with t04 counters auto-accepted (log 21:45/21:53).
  - Team 3 is ~0.6-0.7 behind us; t12 passed us (+1.1/15 min).
  - RET-09 t08 → t09 is the matchmaker's #1 match, with no `neg_points` effect for us.
- **Wrong:** "probably capped" for SAL-11. At 115 the gain is 162 − 115 = 47, under the 50 cap. That is ≈ +2.3 board at 0.05/point, minus some pack drag (sobre_plata, size not in the data).
- **Missing risk on SAL-11:** Pilar paid ~140 for an epic (GAME.md). A 115-125 bid likely loses to the dealer.
- **Wrong: "spare duplicates".** MAL-03 and MAL-08 are single copies. Only LAV-03 and LAV-04 (2 copies each) are true spares.
- **Wrong: our sells "on v10" add venue value.** Venue value is created *between other teams*; our own fills score only as `neg_points`.
- **Wrong: "don't route to t10's venue; one sale there wiped ours".** The wipe was t10's SAL-07 sale on **our** v10 (tick 398, t10 → t15). The routing lesson came from our SAL-01 on t10's v07.
- **Not in the data:** Team 8 "+1.8/h" (Dani shows Δ +0.1).
- **Minor:** t10's LAV-11 bid is now offer 19081, not 18361.

## The 3 changes with the highest expected gain
1. **Broker the RET-09 t08 → t09 match face to face (Lucas or Dani).**
   - Bot chat is dead (0/4 replies). Walk to both teams, point them at v10, and quote the 10 P rebate.
   - Effect: matchmaker VC ≈ +134, which it says reaches the full real-trades mark (up to 5.0 on that component per the 21:20 model).
   - Neither team is in the top 4: t09 #15, t08 #10.
   - Risk: t08 sells to Pilar or to a top-4 RET collector (t10, t12) instead.
2. **Cancel 18963 (MAL-03) and 18965 (MAL-08); list true spares instead.**
   - List the 2nd LAV-02 (1.3), 3rd LAV-02 (1.3), 2nd LAV-03 and 2nd LAV-04 to non-rival LAV collectors (t01, t04, t17) at 5-6.
   - Effect: protects the Sunday MAL page (the +50 counts in full in a fresh round) and costs ≤ +4.5 of forgone gain.
   - Risk: none on score; cash stays ≥ 350.
3. **SAL-11: keep 18977 to expiry (tick 1371) and look for other holders now.**
   - Have the reactor/radar scan the feed for other SAL-11 holders. Bid ≤125 addressed to any non-rival holder.
   - t17 just paid 207 and is a collector: skip it. Do not exceed the guardrail.
   - Effect: +37 to +47 `neg_points` ≈ +1.9-2.3 board if filled.
   - Risk: dealers outbid us (~140), so expect no fill. Free the 260 floor exception back to 350 at expiry.
