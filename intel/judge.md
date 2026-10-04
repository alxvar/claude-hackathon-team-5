# Judge (claude-opus-5-5, Sun 09:05)

## Verdict
**Holding at #3 (30.5) after a frozen night, but stalled.** We trail Team 10 by 7.1 and Team 18 by 0.8, and lead Team 12 by only 0.1. `neg_points` has sat at 119.1 since tick 988, about 450 Saturday ticks with no scored deal, while Team 18 gained +0.8 and Team 12 +0.4 late Saturday (Dani's Δ).

## Our strategies: keep / kill / scale
- **t0 CHA chain (pid 22755): KEEP.** It is the day's biggest lever. CHA rares are worth 112 against a Pícaros cap of ≤ 62, so it carries no dealer losses. The page bonus is 106 (capped at +50 per team-trade closer). Case J fires at the first live tick.
- **Dealer bot: KEEP.**
  - LAV-04 to Pícaros: it walked at her opening price of 4, which is correct (RULES:35). `neg_points` was unchanged.
  - Ladder went 0.437 → 0.483 after 19:04. The source of that rise is not in the data, and per the Chief at 17:45 the ladder no longer moves the board.
- **Trading loop: KEEP, but verify it is alive now.**
  - Its last scored accepts were Saturday: tick 669 (+6.2) and tick 904 (+15.5 window).
  - Since then it has logged only errors (`no card sobre_bienvenida` every minute, then DNS failures 22:55-23:24). Its last line was 00:36, with nothing logged since doors opened.
  - The Mac slept 08:28-09:00.
- **Our bids and listings: SCALE.**
  - We have 0 open offers. The plan's maker book target is 20-30.
  - Our last own team trade, SAL-06 at 28, scored +40.4.
  - We hold 392 cash, and the Sunday GUARDRAIL says cash goes to 0 by 14:00.
- **Flags: KILLED.** Three scored (+10 each), one cost −10, and flag 8 scored 0 after an hour. The cap does not reset.
- **Club routing on v10 (our venue), 50/50: KEEP per the 08:05 directive.** The current `mm_points` value is not in the data.
- **Duelist: KEEP.** Duel score is 35.39. Session 3's last 10 duels gave 8 deals and 2 no-deals. C+ was confirmed by the Duel Lab at 07:38.

## Check the scout
- **Holds:**
  - Pícaros tiers 57/60/62 and closers on El Rastro, addressed with the fee added (07:25).
  - RET-11 goes to Pilar only at ≥ 198 (01:40).
  - Ladder 0.373 → 0.437 with `negotiating` flat at 21.88.
  - The Team 12, 18 and 6 trade figures.
  - Teams 17 and 1 fail the ≥ 10 feeding rule (4.7 and 4.9 below us).
- **Wrong: "Team 10 holds the club venue at v10, each club trade feeds it."** v10 is OUR venue (GAME.md: v10 trades moved our `mm_points`). Club deals on v10 feed us, not Team 10.
- **Wrong: Team 10 "bought RET-03 at 8."** The trade was t10→t06, so Team 10 sold it.
- **Wrong: "Team 8's bid for RET-02 is 5."** The bid is for RET-01.
- **Weak: the spare-sale evidence.** LAV-02 at 10 and LAT-04 at 9 are rival asks, which shows supply, not demand. No bid exists for these cards, and no buyer passes the feeding rule.
- **Inaccurate: LAT-03 and LAT-04 called "spares".** We hold one copy of each, so they are not spares.
- **Stale: "08:45 t0 chain".** Case J moved t0 to the first live tick.

## The 3 changes with the highest expected gain
1. **Keep the Mac awake until 15:00 (a human runs `caffeinate`/pmset), then confirm live PIDs and one instance each.** The processes to check are t0 22755, window.sh 58604, the trader and the book.
   - Effect: protects the whole CHA chain (up to +50 per closer, plus value − price on each CHA buy) and the trader's accepts. The 08:28 sleep already delayed t0's 08:35 step to 08:45.
   - Risk: a double instance on restart. Use the PID lock.
2. **At C, open sobre_plata first, then rebuild a maker book of ≥ 20 offers via `trade.py`.**
   - Bids: CHA bids inside the 54/22/9 public limits, and below-value team buys under the 12:00 cash-sink order.
   - Asks: spares at about 9-10, to buyers that pass the feeding rule only.
   - Reprice anything unfilled for 10 minutes.
   - Effect: restarts scored team trades after 450 flat ticks and turns 392 non-scoring cash into points.
   - Risk: overspending before the CHA rares fill. Respect the 110 floor until 13:30.
3. **Fix the trader's `sobre_bienvenida` error before it masks real failures, and drop that card from the loop's config.**
   - Effect: restores clean monitoring. A silent loop failure on Saturday would have hidden the +15.5-type accepts.
   - Risk: a mid-window restart. Do it before Duels III at about 11:00.
