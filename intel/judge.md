# Judge (claude-opus-5-5, Sun 00:09)

## Verdict
**Holding, slightly slipping.** #3 at 30.49 (−0.4 over 60 min). Team 18 passed us (+1.2/60 min → 31.3). Team 12 sits 0.1 behind at 30.4. Leader Team 10 is +7.1 ahead at 37.6. `neg_points` has been flat at 119.1 since tick 988 (~450 ticks with no scored deal). Market stayed at 7.5, the stall number, all Saturday.

## Our strategies: keep / kill / scale
- **Dealer bot: keep for CHA buys at ≤ value only; kill ladder-only threads.** No neg or ladder movement since tick 904. Last thread (Pícaros LAV-04) walked at 4 with no change. Ladder 0.483 had no board effect after 0.373 ([L], Chief 17:45).
- **Trading loop: keep and restart on HEAD.** 2 accepts since 15:29 (+6.2, +15.5). It logged 5 `unknown_card sobre_bienvenida` errors (fixed in 918f823, which only takes effect after a restart) and a network outage from 22:55 to 23:24.
- **SAL-11 bid 20252 (115 → t04): keep, but expect low odds.** Unfilled since 21:45. The last epic trade was SAL-11 at 207 (t10 → t17, tick 1296), and a 245 ask is live.
- **Book asks LAV-03 → t04 and LAV-04 → t01 at 6: let them lapse at tick 1455.** Gain is 2.8 each. t01 (−4.9) and t04 (−5.4) both collect LAV and are not ≥ 10 below us. Whether either card closes a page for them is not in the data.
- **v10 swap desk / club: scale.** Real trades are 22.5 of Market's 30 (organisers' deck). Our market was stuck at 7.5, and six benches had nobody above the stall. The matched trades are not executed yet.
- **In-room trades: keep.** They produced our two biggest Saturday deals: +40.4 (SAL-06 from t08) and +15.5 (swap with t07).

## Check the scout
- **Holds:** the ≤125 GUARDRAIL, value 162, cash 392, the 260 floor, and ≈ +2.3 board (≈ 0.05/pt × 47). Also holds: t09 bids 56 for MAL-09/10 and 24 for SAL-06; Team 6's RET sales to t12 (216) and t04 (84); t09 at #16; Team 10's 46 dealer / 16 team trades.
- **Unverified:** "t04 asks 245 for SAL-11". Public boards mask makers; the metrics list SAL-11 at 245 with no team.
- **Overstated:** "+47 if filled" ignores pack drag. Our unopened sobre_plata (71.6) cut SAL-06's capped +50 to +40.4.
- **Conflict:** RET-09 seller.
  - The scout and the 21:40 directive say t08 → t09 with VC ≈ +134.
  - The Market log (23:35) says t07 → t09 with 68 VC.
  - Resolve this before Lucas DMs anyone.
- **Wrong wording:** "dealer buys score ≤ 0 unless below value". They score min(0, ΔV − p), so never above 0. Whether the Pícaros stock CHA cards at all is not in the data.
- **Missed:** Team 18 overtook us, and Team 12 is 0.1 behind.

## The 3 changes with the highest expected gain
1. **Execute the RET-09 → t09 page-closer on v10 at the 09:00 open, then 2-3 more vetted swap-desk pairs.**
   - Effect: one collector trade took our market 7.5 → 12.5 (+5 board, tick 311). This is the only lever above +2 on the board.
   - Risk: value created is net. Tick 398's sale to a lower-multiplier holder wiped +5 → −5.2. Approve only pairs where the buyer values the card more than the seller, and never a top-4 team or a rival venue.
2. **Sunday sequencing:**
   - Restart everything on HEAD.
   - Confirm the round-3 reset in `/api/me`.
   - Open sobre_plata immediately after the CHA release and before any buy (directive: the pack is kept for CHA).
   - Effect: removes ~2-10 pts of drag per trade (SAL-06 lost 9.6).
   - Risk: opening before the release wastes the pack's CHA chance. Also, SAL-11 may fill before the pack is opened, which is accepted (still positive).
3. **CHA page:**
   - Rares from the Pícaros at 48-52 (≤ 54, below their list of 63); last card from a team as maker (no fee, cap 50). Value 112 vs ~50 gives 0 neg loss, and below-list deals are what moved the ladder in a fresh round.
   - Effect: +3.2-5.6 final [L].
   - Risks:
     - Pícaros bait-and-switch: check the structured card ID against the words before every accept (trick guard on).
     - Cash floor 350 until CHA is done.
