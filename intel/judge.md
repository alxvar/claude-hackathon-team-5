# Judge (claude-opus-5-5, Sat 10:13)

## Verdict
**Falling behind.** We are #7 at 18.9: −1.1 over 60 min and +3.6 over 15 min. Team 18 is at 28.0 (+8.8 / 60 min) and Team 2 at 23.4 (+16.5 / 60 min), so we are 9.1 behind #1. Our `neg_points` are −19.0, all from two Chato rares (RET-09 at 87, RET-10 at 86). Nothing positive has scored yet today. The RET page, if it closes by a team trade, is the only lever in sight that recovers this: about +50 [L].

## Our strategies: keep / kill / scale
- **Abuela bot (RET commons/uncommons): keep, but ladder only.** Ladder went 0 → 0.048 over 3 deals (+0.014/+0.018/+0.016), and `neg_points` did not move.
  - The ladder counts the best 3 deals per level, and level 1 now has 3. RET-07/08 add ladder only if they beat the weakest share (12 → 9 = 25% of range).
  - Value from here is page progress and cash saved, not ladder.
- **Chato rares: done, never repeat.** They cost −10 and −9, and the ladder did not move on any of our 4 Chato deals. Those −19 are sunk unless the page closes.
- **Chato RET-06 (directive 10:10, cap 31, warm, +2/+3): keep, as decided.** It is the only ladder lever left (level-3 early start). The cold +1 run walked at his final of 31.
- **Maker book (6 spares at 9 + SAL-08 at 33): reprice or route.**
  - 0 fills in 12+ min after the 09:59 reprice, and 0 in the 17 min before it.
  - Rivals list LAV-04 at 9-10 and LAV-03 at 9, so we are not cheaper.
  - Addresses t07/t09/t15/t16 are now only 6.3-8.6 below us, which fails the feeding rule's ≥ 10 for any page-closer.
- **Trading loop: unverified.** Its action log shows no Saturday line at all; the last entry is Fri 23:23. Fills attributable to it: 0.
- **Swaps 3245/3246: killed correctly** (0 fills in 25 min).
- **Team bid RET-10 at 70: killed correctly** (no holder).
- **v10 at 0% fee (since tick 230): keep** (zero cost). No v10 settlement yet. Market is 5.61, up from 4.8 at the 10:00 bench (source not in the data).
- **In-room trades: none in the data.** Dani's table reads "no buyer passes the feeding rule".

## Check the scout
- **Holds:**
  - The RET-08 thread (29 → 25, ours 19, bid 3904 to tick 248). Abuela's log since shows 24.
  - Abuela uncommon median 22 over 7 deals.
  - Team 2 sold RET-07 to t15 at 24, and bids 18/16 for RET-10/09.
  - Team 18 paid 49 for RET-02.
  - Chato finalled 31 on RET-06.
  - Team 12's market comes from one 7 P trade.
  - Our spare asks are idle.
- **Does not hold:**
  - "Each Abuela deal moves the ladder": the best-3 rule says otherwise, and level 1 already has 3.
  - "Cancel the stale swaps": already done at 10:10.
  - "Team 15 bids 59 for RET-09/10": the board has no t15 bid now (stale GAME.md line).
  - "RET-06 from Abuela, Chato only if Abuela stalls": contradicts Lucas's 10:10 directive (RET-06 from Chato, cap 31). Rejected.

## The 3 changes with the highest expected gain
1. **Secure a team source for RET-01 now, so the page closes by a team trade.**
   - Who holds RET-01 is not in the data. t13 bids 2 for it, so t13 lacks it.
   - Lucas or Dani asks in the room or WhatsApp for a holder, preferring non-top-4 teams. The operator posts the addressed bid at ~20 only once RET-06/07/08 are held. Keep it short-lived, because the feed shows addressed offers.
   - Do not buy RET-01 from Abuela: the page bonus is believed to score only via a team trade [L].
   - Effect: ~+50 `neg_points` [L, cap form open], about +8 board at 0.16/pt [L]. This reverses the −19.
   - Risk: no holder sells, the page stays open and the −19 stays sunk.
2. **Run the RET uncommon purchases to a hard cash budget.**
   - Cash is 202 and the floor is 100, so 102 is spendable. RET-06 ≤ 31, RET-07 ≤ 24, RET-08 ≤ 24 and RET-01 ≤ 20 + 2 fee total 101.
   - Accept Abuela's final ≤ 24 (her 24 is at cap). Each P under 24 is floor slack.
   - Re-read `/api/me` cash before each buy. If RET-06 lands at 31 and the others at 24, RET-01 must be ≤ 19 + fee.
   - Risk: one overshoot leaves no cash for the page-closing card.
3. **Fix the maker book in one pass.**
   - Confirm `loop.py` is alive: its log has no Saturday events.
   - Pull the spare asks addressed to t07/t09/t15/t16 whose card could close a LAV/SAL page for them; they fail the ≥ 10-below rule. Re-address only to teams that don't collect that set.
   - Ask Lucas whether Dani may point a named buyer at a live offer (§6b). This is unclear after the 10:06 "no in-person pitching" line, which was about v10.
   - Effect: about +6 `neg_points` per fill (9 − value 1.2-3.2 − 0 fee as maker).
   - Risk: selling a page-closer to a rival 6-9 points below us lets it pass us. Friday's SAL-06 to t17 did exactly that.
