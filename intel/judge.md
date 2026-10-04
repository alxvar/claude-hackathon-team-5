# Judge (claude-opus-5-5, Sun 02:43)

## Verdict
**Holding, not gaining.** We are #3 at 30.5, 7.1 behind Team 10 (37.6), 0.8 behind Team 18 (31.3) and 0.1 ahead of Team 12 (30.4). `neg_points` has sat at 119.1 since tick 988, which is 457 ticks with no scored trade gain. Ladder rose 0.437 → 0.483, but the board did not move on ladder after 17:45 [L].

## Our strategies: keep / kill / scale
- **In-room / swap team trades: SCALE.** They are our only scored gains since noon: the t07 swap +15.5 (tick 904) and the t08 SAL-06 page close +40.4 (tick 988).
- **Dealer bot: KEEP, only for GUARDRAIL fodder.** The last thread (LAV-04 to the Pícaros) walked correctly at her final of 4 against our floor, at zero cost. Dealer gains are clipped to 0, so it only feeds the ladder.
- **Trading loop: KEEP, fix first.** It made 2 accepts all Saturday (+6.2, +15.5). Since 22:41 its log shows an `unknown_card sobre_bienvenida` error every minute plus DNS errors. These must be fixed before 09:00.
- **Our listings: KILL addressed asks that have no agreed buyer.** We posted 414 listings for 17 team trades. Offers 19979 and 19981 are addressed asks with no WhatsApp agreement in the logs, and they expire at tick 1455. Addressed asks fill at 0.3%, open asks at 3.5% (directive 00:37).
- **Flags: DONE.** Net +20, and the cap is spent (probe at 17:43 scored 0).
- **Duels: KEEP the current setup.** Duel score is 35.39, and 8 of the last 10 session-3 duels ended in a deal.

## Check the scout
- **Holds:**
  - Cash 392, CHA cash A 242 / B 250 / C 282, and the per-trade cap of 50.
  - t01 (25.8) and t04 (25.1) are both ≥ 10 below us and outside the top 4.
  - LAV-03 and LAV-04 copies are worth 3.2 each.
  - RET-11 is worth 198, and the ≥ 198 floor matches directive 01:40.
  - The t12 purchases (RET-11 at 216, LAT-10 at 86) and the Team 18 LAT-10 buy at 72 are correct.
- **Wrong: "v10 = Team 10's venue … feed its venue."** v10 is OUR venue (free stall; directive 00:35). The VC directives feed our own market score, not Team 10.
- **Wrong: "Team 10 sells MAL-11 … to t10 at 195."** The feed shows t08 → t10, so Team 10 bought it. It sold SAL-11 to t17.
- **Wrong: RET-11 "gain unmeasured, capped at 50."** At 216 the gain is +18, which is below the cap.
- **Wrong: selling RET-11 "via Pilar."** A dealer sale scores 0 `neg_points`. Only a team sale counts.
- **Self-contradictory: LAV spares.** Selling both spares and keeping them as Workshop fodder conflict:
  - We have 4 spare LAV commons (LAV-02 ×2, LAV-03, LAV-04).
  - Selling LAV-03 and LAV-04 leaves 2, and the Workshop needs 3.
  - Dani's table also shows no buyer clearing value + 3 (6 − 3.2 = 2.8).
- **Missing: the MAL gate.** Cash 392 minus the CHA cost leaves 150 in case A, 142 in B and 110 in C. The ≥ 150 MAL gate (directive 01:40) fails in B and C.
- **Missing: the trader floor.** The trader floor of 464 is built on CHA case B = 288, while the 00:46 log says B = 250. One of the two numbers is stale.

## The 3 changes with the highest expected gain
1. **CHA fast start at round 3's first tick, with the cash numbers reconciled first.**
   - Operator recomputes `CASH_FLOOR` = actual CHA case + 126 (MAL) only if ≥ 150 is left; otherwise the CHA case alone.
   - Pícaros CHA rares run `--offer-only` with the trick guard; public capped bids go up in parallel.
   - Effect: CHA page close up to +50, plus below-value CHA buys (value 16 / 40 / 112).
   - Risk: Pícaros print runs run out (SAL-11 9/9), and a wrong floor blocks the trader.
2. **Fund the MAL close with a team sale of RET-11 at ≥ 198.**
   - Dani asks a RET collector ≥ 10 below us and outside the top 4 (t13, t16, t02, t09, t15, t07).
   - We sell as maker with an addressed ask after a WhatsApp agreement.
   - Effect: up to +18 `neg_points` on the sale, and it unlocks the MAL close (+30 `neg_points` past our cap per 01:40).
   - Risk: no buyer has shown 198 in cash (not in the data). Pilar's ~140 never qualifies.
3. **At 09:00, fix the trader and move spares to open asks.**
   - Fix `sobre_bienvenida` in `loop.py` (bad card id) before the restart.
   - Cancel 19979 and 19981 if they are still live.
   - Workshop 3 LAV spares → 1 uncommon, and sell it to Pilar above 16 (ladder fodder).
   - List the 4th spare OPEN at 9 on a non-rival member's venue.
   - Execute the approved v10 row #1 (RET-09 t07 → t09, +67.6 VC).
   - Effect: a few `neg_points` from the spare sales; v10 VC toward the 40-50 target.
   - Risk: low. Each of these deals is small, and the uncommon the Workshop yields is outside our control.
