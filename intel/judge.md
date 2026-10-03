# Judge (claude-opus-5-5, Sun 00:25)

## Verdict
Holding #3 at 30.49 (0/15 min, −0.4/60 min), 7.1 behind Team 10 (37.6, −0.3/60). Team 18 is gaining on us: 31.3, +1.2/60 min, 0.8 ahead. Team 12 is 0.1 behind at 30.4. `neg_points` has been flat at 119.1 since tick 988. The game is closed until Sun 09:00.

## Our strategies: keep / kill / scale
- **Dealer bot: KEEP, buys only.** The last thread (Pícaros LAV-04 sell, final 4 under floor 4/value 3.2) walked correctly, so 0 neg was lost. Ladder 0.483 looks spent: `negotiating` stayed flat across 0.373 → 0.437 [L]. Use it only for CHA buys at ≤ value. Ernesto: no neg-safe deal (00:40 log).
- **Trading loop: KEEP, RESTART.** Its last real fills were the swaps at 15:48 (+6.2) and 17:46 (+15.5). Since then the log shows only errors: `unknown_card sobre_bienvenida` ×5, then network failures. The fix (918f823) loads only at the next restart.
- **Maker asks 19979 / 19981 (LAV-03 → t04 at 6, LAV-04 → t01 at 6): KEEP.**
  - Each is about +2.8 over our value of 3.2, with no fee because we are the maker.
  - Both expire at tick 1455, 10 ticks after the open.
  - Of 414 listings, few filled, and the sell table is empty: no buyer passes the feeding rule.
- **SAL-11 bid 20252 (115 → t04): KILL** at the first tick (00:50 GUARDRAIL).
- **In-room / page-closing team trades: SCALE.**
  - SAL-06 from t08 at 28 gave +40.4, our biggest single gain on Saturday.
  - The t07 swap gave +15.5 and moved the board +0.74 (≈ 0.05 per neg point).
- **v10 market: SCALE.**
  - Saturday ended at 7.5, the stall number, and nobody beat the stall.
  - Real trades are worth 22.5 and remain the largest open lever.
- **Duels: not ours to run.** Session 3 shows 8 of the last 10 duels as deals; duel score is 35.39.

## Check the scout
- **#1 Cancel 20252: HOLDS.** It matches the GUARDRAIL and the expiry at tick 1565.
- **#2 Sell into t09's 56 bids for MAL-09/10: VOID.**
  - We hold neither card; holdings show MAL-01..06 and MAL-08 only.
  - Even if we held them, the "MAL close stays" directive would forbid the sale.
  - Read it the other way: t09 is competing with us for the MAL rares we need.
- **#3 CHA FAST-START at 09:00: HOLDS.** Cash 392 covers the 242-384 P need, and the +3.2-5.6 [L] estimate comes from the 21:20 directive. Caveat: in the 384 case, nothing is left for MAL.
- **Team 18 +1.2/60 and the LAT-10 buy at 72: HOLD.** Team 12 at 30.4: holds.
- **Team 10 MAL-11 at 195 and SAL-11 at 207: HOLD.** Team 6 −2.7/60: holds; that sales cause it is inferred.
- **"Dealer prices may move against us": NOT IN THE DATA.**
- **Missed:** the two LAV asks expire at tick 1455, and MAL-08 is never-sell (00:50).

## The 3 changes with the highest expected gain
1. **At 09:00:**
   - Read `/api/clock` `round`.
   - Cancel 20252.
   - Run the CHA FAST-START with these limits: Pícaros rares 48-52, accept ≤ 54; Abuela commons ≤ 9, uncommons ≤ 22.
   - Buy the last CHA card from a team; a page-closer is worth at most 50 + price.

   Expected: +3.2-5.6 final [L].
   Risk: Pícaros bait and switch, so the trick guard checks every offer. A dealer buy above value loses in full.
2. **MAL close via a team trade, only if ≥ 150 P is left after CHA.**
   - Get the MAL rares from the Pícaros at ≤ 49, which is our value and fills the empty L4 slot.
   - Buy the closer from a team, e.g. t15's spare MAL-07.

   Expected: up to +50 neg (bonus 46.4 + card value, capped) ≈ +2.5 board at the measured 0.05/pt.
   Risk: t09's 56 bids outbid us for MAL-09/10. Cash could run out if CHA lands in the 384 case.
3. **Before 09:00, restart `loop.py` with 918f823; Lucas and Dani broker v10 club pairs.**
   - Start with RET-09 t08 → t09: +68 value created, a page-finisher.
   - Both sides are ≥ 10 below us and outside the top 4.

   Expected: about 3.9-4.8 of the 5 real-trades points (Market sim [L]).
   Risk:
   - Club pairs leaking to the top 4 (t10, t18, t12, t03).
   - Another network outage like the 22:50-23:24 one; the operator alerts on a quiet `team/lucas.md`.
