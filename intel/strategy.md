# Strategist (claude-opus-5-5, Sat 19:43)

## How the points really work
- **Negotiating 30** = duels + ladder + team-trade value. All of it is relative.
  - Team trade: min(50, ΔV − price − taker fee). At ≈0.05 board per neg point [V, tick 910], a capped trade ≈ +2.4 board.
  - Dealer deals: gains clip to 0, losses count in full.
  - Ladder is spent for the board this round: `negotiating` stayed flat at 21.88 while ladder went 0.373 → 0.437.
  - Flags are spent: ≈3 scored per team, net +20.
  - Our neg has been flat at 119.1 since tick 988.
- **Market 30** = bench efficiency (stall = half; full = mean of top 3) + NET value created on our venue.
  - We are at 7.5 (stall only). Rivals are at 9.15-12.5. **This is the whole gap to #1.**
  - One positive trade on v10 measured +4.99; a value-destroying one measured −5.2.
- **Judges 40**: no scoring data.
- **Rounds start at the `round` event, not when the doors open.** Round 2 fired at Sat tick 160 (hour 2.7), so Friday's round ran into Saturday morning [V].
  - Round 3 fires at hour 16.65 ≈ **Sun 11:34**.
  - So Sun 09:00-11:34 is still round 2 [L]. That includes the **hard bench (≈09:34)** and a bench at ≈09:55.
  - Round 3 is only ≈3.4 h: CHA release, grant, 2 benches (≈11:55, ≈13:55; the 21.0 bench falls after close), Duels III.
  - Round 3 has weight 1, the same as Saturday's 14 h. **An hour of Sunday afternoon outweighs several Saturday hours.**
- **Cheapest points (field near zero):**
  - Venue value created: few measured trades anywhere.
  - L4/L5 ladder slots after the round-3 reset: Banco only 2 team sales and Picaros 3 common buys in the last 60 ticks.
  - The `days` pie in Duels II/III.

## Our winning strategy
- **Tonight (round 2):** market + Duels II + page-closer pricing of our LAV spares. Neg from small trades is noise: +2-3 neg ≈ 0.1 board.
- **Sun 09:00-11:34 (still round 2):** hard bench and v10 value created; sell the spares we don't need tomorrow for cash.
- **Round 3: be the CHA buyer.** Our 1.6 is the top multiplier, so we outbid any team with a lower CHA multiplier.
  - Card values to us: common 16, uncommon 40, rare 112, bonus 106.
  - Score sources: team buys below value (each scores value − price), one capped page close (+50), and a fresh ladder at L3-L5.
  - Leaders' visible play is RET/LAV collecting (t10, t14). CHA is new for everyone, and nobody starts round 3 ahead.
- **Stop:**
  - Spare sales at 6-9: 0 fills since tick 988, ≈+2 each.
  - Dealer threads tonight: ladder spent, gains clip.
  - Egg hunting: RULES say easter eggs never count.
  - Any trade on v07 (t10's venue).
  - Selling LAV/RET/SAL page cards.

## Levers nobody is using yet
1. **v10 trades don't need our key.** The auto venue crosses on its own, so Dani's room pairs keep scoring through Duels II after the 20:25 bot stop.
   - Vet each pair: buyer's multiplier > seller's, and the seller holds ≥2 copies (the tick-398 lesson).
2. **Our LAV spares are page-closers, not 6 P commons.** We hold LAV-02 ×2 extra (1.3), one extra LAV-03 (3.2) and one extra LAV-04 (3.2).
   - t07 (21.8, 10.1 below us) bought LAV ×7. A close sold at 35 ≈ +32 neg ≈ +1.6 board.
   - Asks 16601/16870 at 6 waste that.
3. **Round-3 ladder reset.** Ladder reset to 0 at round 2 [V], and L3 paid +0.050 ≈ 3× L2 [V].
   - Few teams trade at L4/L5. Keep spare commons/uncommons as ammunition: sales above the opening bid, at ≥ our value, in −2/−3 steps.
4. **Pre-staging for a 3.4 h round.** Have cash, a bid list, dealer scripts and room sellers ready before 11:34.
5. **Silver pack (77.4) held for CHA.** Saturday's grant pack opened after the RET release pulled RET-05.

## Plan, anchored to the schedule
| When | Who | Move | Impact |
|---|---|---|---|
| now | Operator | Cancel 16601 and 16870 (LAV at 6). Let the MAL asks to t15/t09 run. Keep MAL-01, MAL-04, LAT-03, LAT-04 for round 3 | frees page-closer pricing |
| now | Dani → Operator | Ask t07 which LAV card it lacks. Maker ask addressed to t07 at 35 (El Rastro), only if t07 is still ≥10 below us | ≈+1.6 board per fill |
| 19:45-22:10 | Dani + Market | v10 pairs vetted with the radar; rebate per GUARDRAIL (cap 30, settle 22:45) | up to ≈+5 board |
| ≈19:55, ≈21:55 | Market | Record the benches; flag any rival bench above stall | evidence for Sunday's broker |
| before ≈20:34 | Aleks | Dry `days` payload through PLAN #24. Set DAYS_READ from the first live `days_meaning`, not from "auto" | protects the 13.93 duel score |
| 22:45 | Operator | Rebate settlement at fee 0 on v15, against a card worth ≥ the owed amount | ≈0 neg instead of ≈−15 |
| 22:50 | Operator | One read of `/api/dealers/banco`. One test bid `want: cards ["CHA-01"]` (a refusal costs nothing) | tells us if CHA bids pre-stage |
| Sun 09:00 | Operator | `/api/clock` round = 2? neg still 119.1? | confirms round-2 window |
| Sun ≈09:34 | Market | Hard bench: a board broker only if it already beats the stall in replays, else stall | round-2 market |
| 09:00-11:30 | Dani | Line up CHA sellers among low-multiplier teams (prices fixed by the Operator). Sell non-ammo spares | cash for CHA |
| ≈11:34 | Operator | Open sobre_plata. Maker bids on every CHA card from teams (see bid rule below) | team buys score value − price |
| 11:34-14:00 | Operator | Abuela commons/uncommons below list (score 0, may move the ladder); Chato rares only if teams fail (86-87 < 112). Cheapest common last, via a team: worth ≤ 50 + price | page close +50 ≈ +2.4 |
| 11:34-14:00 | Operator | 3 deals each at L3 Pilar, L4 Picaros, L5 Banco (if Banco buys anything we hold) | fresh ladder |
| ≈13:34 | Aleks | Duels III: 12 ticks, 10% decay; close within ≤3 exchanges | duel share |
| 14:00 | Operator | Cash → 0 into non-negative CHA buys | — |

Bid rule at ≈11:34: one copy each (a 2nd copy is worth 25%), each bid at ≤ value − 10. A rare at ≤62 scores ≈ +50.

## Hypotheses to test
1. **Sun 09:00-11:34 is round 2.** Test: read `/api/clock` and `/api/me` at 09:00. Decides by: round = 2 and neg 119.1 unchanged.
2. **The ladder counts again on the board in round 3.** Test: the first Pilar or Picaros sale after 11:34. Decides by: `ladder_points` and board `negotiating` both move.
3. **Banco buys a card we hold.** Test: read `/api/dealers/banco` tonight. Decides by: its "how" text, or a thread topic it accepts.
4. **A pack opened after the release can pull CHA.** Test: open sobre_plata after 11:34. Decides by: the pull contains CHA. Also, if a pack's `your_value` exceeds Abuela's haggled ≈19, it is worth buying.
5. **CHA bids pre-stage before the release.** Test: one bid at 22:50. Decides by: refused or accepted.
6. **Value created on v10 is cumulative per round, so a later dump erases it.** Test: compare `mm_points` before and after each v10 trade. Decides by: a negative trade lowers our total (tick 398 says yes). If confirmed, ask the desk whether the bench charges fees (§3 Q5) before considering a post-rebate fee raise to deter dumps.
7. **t10's +5.7/60 min comes from market (v07).** Test: compare t10's leaderboard components across two snapshots. Decides by: which of market or negotiating rose. If market, no team of ours or any partner routes trades to v07.
