# Judge (claude-opus-5-5, Sat 10:29)

## Verdict
Falling behind the top 3, holding the pack: #6 at 19.3 (−0.7/60 min) vs T18 29.3 (+10.1), T2 26.0 (+19.1), T12 27.1. The gap to #4 (T14 22.9) is 3.6. The board shows +0.4/15 min; whether that includes the tick-276 +50 is not in the data.

## Our strategies: keep / kill / scale
- **Abuela bot (warm narrator): keep, needed cards only.** 5 below-list deals today. `neg_points` 0 each, ladder +0.014/+0.018/+0.016/+0.003/+0.004. Gains are shrinking (best 3 per level), so it is not worth running for the ladder alone.
- **Chato buys: kill.** RET-09 −10, RET-10 −9, RET-06 −2.5 = −21.5. None moved the ladder and none unlocked Pilar.
- **Trading loop (`loop.py`): idle or dead.** No event since Fri 23:23 (DNS errors), so no Saturday accepts. Confirm it is running.
- **Maker book (11 addressed asks on v07): fix.** 0 fills Saturday, and 4 earlier asks expired unfilled. No bids exist for these cards on El Rastro. The asks are priced fine; the missing piece is buyers who know about them.
- **RET page: done, keep the recipe.** Net +28.5 (rares −19, uncommons −2.5, close +50.0). The cap test is resolved: flat 50 or 5×book.
- **In-room push: scale.** RET-01 filled only after Lucas messaged Team 10 (+50.0). It is our only Saturday team-trade fill.
- **v07 reciprocity: no data yet.** Zero fills our side, so there is nothing to audit.

## Check the scout
- Holds:
  - Do not sell RET-09/10 into t02's 21/19 bids.
  - T18 bought RET-02 at 49; T2 sold RET-07 at 24 and bids 21/19.
  - T14 bought LAT-03 at 8.
  - T13 unlocked Pilar and fell 7.2/h.
  - Chato deals lose points and don't move the ladder.
- Stale: #1 (RET-01 bid, escalate to 25/30). It filled at 20 on tick 276; the guardrail is spent and the floor is back to 100.
- Wrong: "sell spare RET cards after the page closes". We hold one copy of each RET card. Any sale breaks the page and gives up the 72.9 bonus.
- Wrong: "the Sat sell at 9 earned +7.7". That was Friday, tick 106. Saturday's only team trade is the RET-01 buy.
- Unsupported: "t13 holds RET". A 2 P bid shows want, not holdings.

## The 3 changes with the highest expected gain
1. **Get the 11 live asks filled: Dani/Lucas message each addressee, as with Team 10.**
   - Targets: t07, t09, t16, t15, t01.
   - Add LAT-08 at 21.5 (worth 12.5) and MAL-02/04 at 9 (worth 7).
   - Repost before ticks 320/325 with 2× the expiry ticks you want.
   - Effect: if all fill at listed prices as maker (no fee), +60 `neg_points` (LAV spares +17.4, SAL spares +13.6, LAT-04 +11.6, MAL-06/07 +13, others +4.5). LAT-08 adds +9.
   - Risk: a spare may close the buyer's page (they gain up to +50). All addressees are outside the top 4; never re-address to T18/T12/T2/T14.
2. **No dealer buy above our value. Pilar after ~12:20 only for leftovers teams won't take.**
   - Candidate: SAL-08 (worth 22.5; she pays over book for SAL), sold at ≥ our value and beating her list.
   - Effect: 0 neg loss plus level-3 ladder (amount not in data). Each avoided Chato deal saves 2.5-10.
   - Risk: the "below/beyond list counts" rule is only [L], so the ladder gain may be 0.
3. **Restart and verify `loop.py` before Duels I ends, under the accept arbiter.**
   - Effect: catches any ask below value − 3 − fee at no cost. This matters most on Sunday for CHA cards (worth 16/40/112).
   - Risk: the shared key's 5 req/s limit (Friday 429s). Run reads keyless, and keep it from taking an accept during an in-limit duel tick.
