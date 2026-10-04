# Judge (claude-opus-5-5, Sun 07:53)

## Verdict
**Holding.** We are #3 at 30.49. Team 10 leads by 7.1 and Team 18 leads us by 0.8. Team 12 is 0.1 behind us. `neg_points` has been flat at 119.1 since tick 988, and nobody has moved in 60 min because the game is closed (tick 1445).

## Our strategies: keep / kill / scale
- **Team trades (maker and swaps): SCALE.** Every positive `neg_points` move came from one: +4.7, +2.0, +2.0, +2.5, +6.2, +15.5 (swap) and +40.4 (SAL close). We have 0 open offers now.
- **Dealer bot: KEEP, but only for CHA buys at or below value.** Dealer gains clip to 0, so the bot earns nothing beyond the ladder. Its last thread (LAV-04 to Pícaros, 10→7 in −1 steps, her final 4 = her opening) was a correct walk: `neg_points` and ladder were unchanged. The playbook says step −2/−3, not −1.
- **Ladder chasing: KILL.** The board stayed flat across 0.373 → 0.437 (Chief 17:45).
- **Flags: KILL.** The cap is reached (flag 8 scored 0). Net +20.
- **Trading loop: KEEP, but FIX it before 09:00.**
  - It hit `unknown_card sobre_bienvenida` every minute from 22:41 to 22:45.
  - It hit DNS errors on /api/clock and /api/me from 22:55 to 23:24.
  - Its only accepts on Saturday were +6.2 and +15.5.
- **v10 club / venue: KEEP per directive.** Our `mm_points` are not in the metrics, so there is no evidence of their current effect.
- **Workshop: KEEP, but do not count on it.** It changes collection value only and is not scored.
- **Duels: KEEP (Aleks).** In the last 10, 8 reached a deal. C+ was confirmed by the Duel Lab at 07:38.
- **Cash: SPEND per GUARDRAIL.** We hold 392 and cash never scores. The target is 0 by 14:00.

## Check the scout
- **Holds:**
  - The game is closed, we have 0 offers, cash is 392 and the ladder is 0.483.
  - Flags are spent, and the t0 chain is armed (pid 22755).
  - The CHA numbers are right: value 112, page bonus 106, cap 50.
  - Team 12's buys (RET-11 at 216, LAT-10 at 86) and Team 10's epics (MAL-11 at 195 in, SAL-11 at 207 out) match the feed.
  - The rivals are t18, t12 and t03.
- **Weak:** "Pícaros rare median 55" rests on n=1.
- **Partly wrong:** "Team 6 dumps RET rares at 77-84" only partly holds. RET-10 went at 84 and 77, but RET-06 at 30 is an uncommon.
- **Wrong:** "CHA rares at ≤ 62 are a gain of ~50 each" is false for Pícaros. A dealer deal scores min(0, ΔV − p), so these buys score 0. Only the team-trade closer scores (≤ 50).
- **Unverified:** "Team 10 holds the venue lead" is not in the data.

## The 3 changes with the highest expected gain
1. **Open `sobre_plata` (71.6) before any CHA buy, and confirm the t0 chain's "pack →" step runs first.**
   - Effect: the CHA closer scores nearer +50. The SAL closer scored +40.4 instead of +50 because of pack drag, and SAL-06 scored −2.7 instead of −0.5.
   - Risk: none on score, since the pack opens either way.
2. **Have Dani source CHA cards from non-rival teams by addressed trade (executor posts, pre-agreed per the 07:05 limits).**
   - Watch `pack.opened` and listings from R.
   - At value 112, any team-bought rare at ≤ 62 scores +50 (at the cap); the same card from Pícaros scores 0. Commons (16) and uncommons (40) score value − price.
   - Effect: up to +50 per rare, but supply is unknown. No RET rare came from a grant pack on Saturday.
   - Risks: the feed exposes addressed bids, and the seller may be t10/t01, whose bids get cancelled per the directive.
3. **Fix the loop errors and add a network retry and alert, then verify `trade.py` lists before R+10.**
   - Effect: keeps the only scoring engine (team trades) live from minute one.
   - Risk: a restart collides with t0; keep exactly one process per role.
