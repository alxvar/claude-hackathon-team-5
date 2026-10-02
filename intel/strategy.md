# Strategist (claude-opus-5-5, Fri 21:56)

## How the points really work
- **Weights.** Friday counts 0.5 and Saturday and Sunday 1 each, so 80% of the weight is still ahead. Friday has about 66 ticks left (tick 94, closes 23:00), and every move tonight counts half. Saturday is the decisive round: 14 h, 8 Market Tests and both scored duel sessions.
- **Negotiating (30).**
  - Team trades: price − our value, net of fees, relative to the field. The gap to #1 is 10 points (17.8 vs 27.8), about one rare trade between teams (observed jumps +8 to +15).
  - Ladder: capped at our best 3 deals per level. Abuela is already at her floor (0.064), so more Abuela deals add almost nothing, while Chato (level 2) weighs more.
  - Duels: 0.0 for us. The practice session doesn't score, so every team is at 0 until Duels I (hour 6.5).
- **Market-making (30).** Every team is at 0: no venues yet, and the first Market Test lands Saturday morning (finding 6).
  - The free auto stall earns half the bench points for everyone, so that half gives no edge.
  - The edge is only above it: matching better than auto, toward the top-3 mean.
  - "Value created on our venue" is a second, uncontested line. Fees never count, so a 0-fee venue costs us nothing.
- **Judges (40).** The biggest share, not in the API. Our multi-agent daemon setup (collector, metrics, scout, judge, strategist) is craft we have to show.
- **Weakest field components: Market-making and duels.** These are the cheapest points.

## Our winning strategy
1. **Saturday: own Market-making.**
   - Unlock Chato.
   - Open a `board` venue with our own broker, built to beat the auto stall on the bench.
   - Set the fee at 0 (if accepted), so it undercuts El Rastro's 5% + 1 and draws trades between teams.
2. **Act as a cheap-set supplier to collectors below us.** Our LAT 0.5 and MAL 0.7 cards are worth little to us. Rares are the lever: a MAL rare into t17's 78 bid scores about +24 (78 − 49 − fee 4.9).
3. **Sunday: become the Chamberí buyer (1.6×).** Bid for CHA from teams that value it low. Never sell CHA.
4. **Duels:** Aleks closes every duel inside our limit, early (decay 0.06–0.08 per round).

**Stop doing:**
- **Racing for the LAV page.**
  - Team 10 now bids 110 for LAV-09. Our 91 bid scores 0 even if it fills and ties up 91 of our 380 P, which we need for the 270 P venue bond.
  - Cancel it unless H2 shows the page bonus is priced in.
- **Autoflip on LAT commons:** they score at most +4.
- **Haggling for flip stock.**
- **Selling to teams above us** (t13, t18, t08, t10, t12, t04, t14) unless our gain clearly exceeds theirs.
  - All SAL buyers are leaders (t13, t18, t08), so hold SAL-06 or offer it only `to` a team below us.

## Levers nobody is using yet
- **Board broker on the Market Test.**
  - Evidence: no venue exists; level 2 isn't open yet.
  - Exploit: the operator builds the broker overnight and replays a 10-trader, 16-tick book offline. It matches every crossing pair, best bid against best ask, in the first tick, before impatient traders leave.
- **0-fee venue.**
  - Evidence: every one of the 35 trades between teams paid El Rastro's fee (it is the only venue).
  - Exploit: open it the moment level 2 is ours. Dani pitches "0% fee" in the room.
- **Rares sourced from Abuela.**
  - Evidence: the dealer medians show only commons, uncommons and packs, and all rare trades were between teams.
  - Exploit: if Abuela sells MAL-09/10, buy at her first price (≤73 keeps our cash level) and fill t17's two bids, 1329 and 1330 → about +48. t17 is below #10 on the board, so this is safe to feed.
- **MAL spares into t17's uncommon bids (MAL-07/08 at 26).**
  - A 2nd copy is worth 4.4 to us, so a sale scores about +19.
  - A 1st copy scores only +6.2: skip it.
- **Abuela's budget is being spent on deals that don't help us level up.**
  - Autoflip takes her opening price, which doesn't count toward unlocking Chato, and it uses up the 8 deals per hour.
  - Reserve 3 deals per hour for negotiated and Chato deals.

## Plan, anchored to the schedule
**Tonight (half weight):**
1. **Now, operator (`trade.py`):** run H2, then cancel the LAV-09 bid (offer 1371) unless the bonus is priced in.
2. **Now, Lucas (`/api/me`):**
   - Do we hold any MAL rare? If yes, accept t17's 78 → +24.
   - MAL-07/08 spares? Accept t17's 26.
   - Check SAL-06 and LAV-04 values.
3. **Now, operator:** run H1 (Abuela rare quote). If it passes, flip into t17 only.
4. **Now, operator:** add an "above us" block-list to `autoflip.py`, `loop.py` sells and `trade.py` listings. Raise autoflip's minimum to cover rares; drop LAT commons.
5. **~22:20 practice duels, Aleks:** test the protocol, including `days` handling. Log messages-to-close and limit breaches.
6. **Before 23:00, Lucas:** confirm in `/api/levels` that we've earned Chato's head start (negotiated Abuela deals, not opening-price ones).

**Overnight:**
- Operator: board broker plus offline sim.
- Aleks: Duels II two-issue logic: concede days that our `your_days_weight` says are cheap, ask price in return.
- Lucas: judge-facing write-up of the architecture.
- Dani: room script for the 0-fee venue.

**Saturday:**
- **09:00 open:** Chato's 3 ladder deals (`abuela_bot.py --dealer chato --ladder --deals 3`). Once we reach level 2, open the venue: board, fee 0 (H4). The stall covers the first bench.
- **Hour 4.0–4.05 (RET release, +150 P, a pack):** open the pack. List LAT/MAL/RET spares `to` collectors below us.
- **Benches at hours 5, 7, 9, 11, 13, 15, 16 (hard) and 17:** broker live. Compare each session against the half-point baseline (H3).
- **Hour 6.5, Duels I; hour 13, Duels II:** Aleks.

**Sunday (hour 18, CHA release):**
- Post CHA bids at the low prices sellers will take (commons ~10, uncommons ~20). Our values are 16 and 40.
- Lucas and Dani find CHA holders in the room.

## Hypotheses to test
| # | Hypothesis | Cheapest experiment | Deciding metric |
|---|---|---|---|
| H1 | Abuela sells MAL/LAT rares at ≤73 | Open a buy thread for MAL-09, read her opening, close | Her opening/final price, and `neg_points` after the flip (+24 expected) |
| H2 | The page bonus is priced into `your_value` | `GET /api/me/value?card=LAV-09` | Result > 91 means the bonus counts; = 91 means cancel the bid |
| H3 | A board broker beats the auto stall | Offline replay tonight, then the first bench with a board venue | Bench efficiency above the stall's half-point share |
| H4 | `fee_bps: 0` is accepted | Open the venue with 0 (a refused opening costs nothing) | 200 vs 400 |
| H5 | A 0-fee venue draws trades between teams | Dani's pitch plus 1 h live | Market-making "value created on our venue" > 0 |
| H6 | Early duel closes beat holding out | Practice duels: close by round 2 vs round 6 | Pie share in Duels I |
| H7 | Opening-price Abuela deals don't count toward unlocking Chato | Compare our head-start status when Chato activates against the log of negotiated deals | `/api/levels` access tick |
