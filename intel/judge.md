# Judge (claude-opus-5-5, Sat 14:06)

## Verdict
Holding at #5 (28.1): +1.8/60 min vs leader t14's +1.1 (gap 2.7), but −0.8/15 min, and t10 (+4.1/h) and t18 (+2.2/h) have passed us. neg_points have been flat at 35.2 since tick 404 and ladder flat at 0.181 since 12:45, so the last ~90 min of gain came from duels (13.93), not trading.

## Our strategies: keep / kill / scale
- **Pilar sells (dealer bot, offer-only):** KEEP. They took L3 to +0.109 (+0.050, +0.040, +0.019) at 0 neg cost. Small steps beat jumps (0.040 vs 0.019).
- **SAL-06 buy (Abuela/Chato):** PAUSE.
  - Three threads, no fill: Chato 33→32, Abuela 29→25 held, and now Abuela 29→29 against our 21.
  - SAL-06 is worth 22.5 to us, so a close at cap 25 costs −2.5 neg, not "−0.33".
  - Plan A's Chato-at-list-26 has not been reachable today: his uncommon finals were 30-32.
- **Chato buys:** KILL (already stopped). Six buys, zero ladder, −10 and −9 neg on the rares.
- **Swaps 9172/9173:** SCALE.
  - 9172 gives LAT-04 (2nd, 1.2) + MAL-04 (7) for SAL-07 (22.5) = +14.3.
  - 9173 gives LAV-02 (2nd, 3.2) for MAL-01 (7) = +3.8.
  - No fee, no cash, and t15↔t07 proved the pattern three times.
- **Spare asks (9 live):** REWORK. Zero fills since tick 404 (~226 ticks, far past the 10-min reprice rule).
  - Our LAV-04 at 7 → t03 sits under others' LAV-04 asks at 10, so the problem is the addressee, not the price.
- **loop.py auto-accept:** KEEP (free). There is no Saturday accept in its log, only pause and error events.
- **In-room / bargain watch:** KEEP. RET-01 from t10 (+50) is still our best trade of the day; bargains.log has 0 hits.
- **Duels:** KEEP. 9 deals in the last 10 of session 2. Duels II framing is Aleks's 15:30 call (directive 12:50).
- **Unopened sobre_plata (92.9):** OPEN unless the Chief is holding it for a Sunday CHA pull (his reason is not in the data). GAME.md: each trade carries a 1-4 point drag while it stays unopened.

## Check the scout
- Swap gains +14.3 / +3.8: **hold**, recomputed from values.
  - The feeding rule is only strictly met by t07 (17.3, ≥10 below us); t15 is 6.2 below.
  - The "re-post if the pause expires them" worry is moot: ticks are frozen at 630.
- SAL-06 "costs up to −0.33 neg_points": **wrong unit**. It is about −2.5 neg (≈ −0.24 board at 0.094).
- "Pilar uncommon finals 18-23": **misleading for SAL**. 18-19 were MAL finals; a SAL resale must close ≥ 22.5 or it loses. SAL-08 went at 23, Team 4 got 25.
- Bargain "no candidate": **holds**. The only RET ask is RET-04 at 12, and a 2nd copy is worth 2.75 to us.
- "Team 10 lists on its own venue v10": **wrong**. v10 is OUR venue (GAME.md: t10→t01 on v10 moved our mm_points).
- "Team 14 and Team 12 feeding each other": **no evidence**. t14's last sells went to t04/t09/t15, and t12 is −2.6/h.
- "Team 6 climbs by selling rares (tick 504)": **weak**. That trade predates the 60-min window.

## The 3 changes with the highest expected gain
1. **Get SAL-07 through swap 9172 before buying SAL-06, then sell SAL-07 to Pilar.**
   - Leave 9172 live through the unpause; have Dani point t15 at it in the room.
   - If it fills, sell SAL-07 to Pilar offer-only, steps −2/−3, floor 23.
   - Expected: +14.3 neg (≈ +1.3 board), plus an L3 slot that replaces SAL-08's 0.019 (up to ≈ +0.7 board).
   - Resume the Abuela SAL-06 buy (cap 25) only if 9172 is rejected or lapses.
   - Risk: t15 ignores it. If LAT-04/MAL-04 closes a t15 page, they book more than we do, but t15 is #14, not a leader.
2. **One L2 test through a Chato SELL above his opening bid (the only L2 route measured to count).**
   - Offer-only, a common worth ≤ his price: LAT-03 (5) or a MAL common (7). Cancel its team ask first and run it alone in its window.
   - Experiment-lane budget 0 neg: walk if his price < our value or he holds his opening.
   - Expected: about +0.017 ladder (LAT-08 precedent) ≈ +0.6 board per slot, with 2 slots empty.
   - Risk: Chato's common bid is not in the data and may sit below 5; it also uses up one of his 6 deals/h.
3. **Re-address the 7 spare asks and post more swaps, targeting teams that actually bought the set** (feed tallies):
   - LAV → t07 (5 LAV buys) / t04.
   - LAT → t15 (6) / t04.
   - MAL → t13 (6) / t01 / t17.
   - SAL → t01 / t17 / t06.
   - Never t14/t12/t10/t18. Possible page-closers go only to t07.
   - Reprice every 10 min unfilled, down to clearing (common 9, LAT 7.5).
   - Mirror the t15↔t07 swap pattern: our 2nd copies for their dumped-set cards worth more to us.
   - Expected: +4-6 neg per fill (≈ +0.4-0.6 board each), about +3 board if 6-8 fill.
   - Risk: the book bot churns again, and unknown page-closers leak to mid-table teams.
