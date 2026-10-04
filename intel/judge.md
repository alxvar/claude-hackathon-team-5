# Judge (claude-opus-5-5, Sun 04:16)

## Verdict
**Holding at #3 overnight, in a near-tie.**
- Standings: 30.49, behind Team 10 at 37.6 (−7.1) and Team 18 at 31.3 (−0.8); Team 12 is 0.1 behind at 30.4.
- Nothing moved: all deltas are +0.0 because the game is closed until 09:00.
- `neg_points` has been flat at 119.1 since tick 988.

## Our strategies: keep / kill / scale
- **In-room team trades: SCALE.** They are our only big scorers.
  - t08 SAL-06 at 28: +40.4 (page close).
  - t07 SAL-07/LAT-01 swap: +15.5.
  - t08 SAL-04/RET-04 swap: +6.2.
- **Trading loop: KEEP, but fix it before 09:00.**
  - Saturday's output was 2 accepts (+6.2, +15.5).
  - The log shows an `unknown_card: sobre_bienvenida` error every minute (22:41-22:45) and DNS failures (22:55-23:24).
- **Dealer bot, CHA buys: KEEP.** Buy only at ≤ value. Every CHA value (16/40/112) sits above the capped bids (9/22/54).
- **Dealer bot, ladder sales: KEEP at low priority.**
  - Ladder rose 0.437 → 0.483.
  - But `negotiating` stayed 21.88 while the ladder went 0.373 → 0.437 [L].
  - The last thread (Pícaros LAV-04: her bid 4, final) correctly walked with 0 change.
- **Flags: KILL.** Capped at 3 scored. The probe at 17:43 scored 0.
- **Our listings: KEEP as is.**
  - 19979/19981 are LAV-03/04 at 6, worth 3.2 each, a gain of +2.8 each.
  - Buyers t04/t01 sit 5.4/4.9 below us and are not top-4.
  - Addressed offers fill at only 0.3%. Both expire at tick 1455, 10 ticks after the reopen.
- **Duels: KEEP the code-first set.** Our 136 duels give duel 35.39; the last 10 in session 3 were 8 deals and 2 no-deals.

## Check the scout
- **Holds:**
  - Gaps to Team 18 (+0.8) and Team 12 (−0.1).
  - The t12/t10/t18 trade prices (216, 86, 195, 72).
  - The CHA bid caps 54/22/9 and the +50 cap.
  - Page points come only via a team trade [L].
  - RET-09 t07 → t09: t09 is 23.3, ≈7.2 below us, which passes the ≥ 6 rule.
- **Does not hold: "the full MAL fits in every case."**
  - Cash 392 minus CHA A/B/C (242/250/282) leaves **150/142/110**.
  - The 01:40 gate needs ≥ 150, so the MAL close is a GO only in case A.
  - The trader floor note puts MAL at 126, so in case C MAL does not even fit.
- **Inconsistent: fodder.**
  - The scout cites the ladder as flat on the board, then expects +1-2 Sunday points from it.
  - The Saturday evidence supports the first claim, not the second.
- **Stale: "Team 18 +0.8 per 30 ticks."** That Δ is from 23:08. Now it is +0.0, because the game is closed.

## The 3 changes with the highest expected gain
1. **Close the CHA page with a team trade first; everything else waits.**
   - Run the Pícaros CHA-09/10 threads at round 3's first tick with `--offer-only`.
   - Buy the last card as one agreed, addressed post from a non-rival (not t10/t18/t12/t03).
   - Effect: up to +50 `neg_points`. Saturday's +40.4 SAL close is the template.
   - Risk: print runs run out, or t10 front-runs a public last-card bid. Keep it addressed and short-lived.
2. **Re-run the MAL gate on real cash, not the "fits in every case" premise.**
   - Decide after the CHA buys settle, on the actual cash left.
   - At < 150 P left, the 01:40 directive itself says no MAL close.
   - Raise cash only from non-page spares: LAV-02 ×3 at 1.3, LAT-03/04 at 5. Use addressed asks to teams ≥ 10 below us.
   - Do not post open LAV asks: Team 10 (#1) collects LAV, and a page-closer must not reach it.
   - Effect: avoids a stranded half-MAL buy. The +30 past our cap is worth something only if the page actually closes.
   - Risk: under-funding CHA if spares are sold too low.
3. **Fix and restart the trader before 09:00.**
   - Remove the `sobre_bienvenida` reference.
   - Confirm DNS and the API respond.
   - Start sells-only, then `CASH_FLOOR=464` with `--exclude 'CHA-*,MAL-*'`.
   - Stop it at T−5 before Duels III (directive 01:30).
   - Effect: the loop is our only automated maker. Its 2 Saturday fills were worth +21.7.
   - Risk: a misconfigured restart buys into CHA/MAL. Verify the exclude list on the first tick's log.
