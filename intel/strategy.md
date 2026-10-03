# Strategist (claude-opus-5-5, Sat 21:18)

## How the points really work
- **Negotiating 30, relative to the field.**
  - Team trades are the only live sub-lever. They move the board by ≈ +0.05 per `neg_point` [V, one window, 17:46]. We have had no scored gain since tick 988 (119.1).
  - The ladder is spent: `negotiating` stayed at 21.88 while the ladder went 0.373 → 0.437 [L]. Flags are capped at ≈ 3 scored per team [V].
  - Duels stand at 13.93.
  - Per-trade cap is +50, form open: flat 50 or 5×book. Dealer deals score min(0, ΔV − p).
- **Market-making 30 = Market Test 7.5 + real trades 22.5** (organisers' deck).
  - The bench is already maxed on our stall: 0.878 to 0.891, so 0.5 each, and no broker upside (Market, 21:15).
  - Real trades = 5.0 × min(1, VC / top-3 mean). **The best market in the whole field shows +5.0 of 22.5.** About 17.5 points are unclaimed by every team. This is the cheapest open component.
  - Value created (VC) is net. It goes negative when a card moves to a lower-multiplier holder (v10: +4.99 → −5.2 at tick 398).
- **Judges 40**: the largest share. The format is not in the data.
- **Rounds** (from `/api/schedule`):
  - Sunday opens at game hour 13.363. CHA, Round 3 and the 150 P grant come at 16.65 to 16.7.
  - Sunday morning until the round event is therefore still **round 2** [L]. Directive 21:10 says "+150 at 09:00", so the wall time of the round event must be checked at the open.
  - Round 3's benches are at 17, 19 and 21. The 14.65 (hard) and 15.0 benches fall in round 2.
- **Stale inputs, ignore them:**
  - The judge's "#3, 31.3": metrics show #2 at 31.93.
  - The scout's "t10 has v10": v10 is ours, t10's venue is v07.
  - The scout's "spare MAL-03": it is our only copy.

## Our winning strategy
- **Sunday: become the monopsony CHA buyer from teams, not from dealers.**
  - Our 1.6 is the top multiplier, so every CHA card is worth more to us than to its holder.
  - Each team buy below value scores separately, up to the cap. At clearing prices (common 9, uncommon 24.5, rare 70) against values of 16 / 40 / 112, that is about +7 / +15.5 / +42 per card, before the page closer.
  - Dealer CHA buys at ≤ value score 0 neg but fill ladder slots (best 3 per level, round 3 starts at 0). Use dealers only for cards no team sells.
- **Tonight and Sunday: v10 as a page-finder and swap desk between non-rival teams** (the 22.5 lever).
  - Move cards from teams that dump a set to teams that collect it.
  - Never route a top-5 team's trades or a dump to a low collector.
- **Stop doing:**
  - Dealer threads for the ladder (spent) and flags (capped).
  - Pícaros small talk.
  - Selling any LAV/RET/SAL card: complete pages, so a sale books the bonus as a loss.
  - Selling MAL-03. Offer 17696 expires at tick 1237: never relist it.
  - Bidding MAL-09/10 against t09's 56. That is above our value of 49, so it loses.

## Levers nobody is using yet
1. **Cap-form arbitrage on the closer.**
   - Every page close so far had a common as the last card, so 5×book = 50 and the form is untested.
   - Make CHA's closer an **uncommon bought from a team**.
     - If the cap is 5×book: 40 + 106 − 25 = +121 (cap 125).
     - If the cap is flat 50: we lose only that uncommon's standalone +15, versus about +7 for a common closer.
   - Downside ≈ −8 neg, upside ≈ +63.
2. **Real trades at 5.0/22.5 for everyone.** No v10 fill tonight is in the data. Pairs from Dani's profiles, dumper → collector, non-rival, eligible for the ad filter:
   - t12 SAL → t09 (t12 sold SAL-09 to t09 at 70, tick 1231, not on v10).
   - t08 RET/LAV → t07 or t04.
   - t12 LAV → t04.
   - t02 SAL-03 → t08 (the dry-run pair).
   - Exclude any seller with a complete page in that set (t15: LAT, RET and LAV).
3. **Round 3 starts later than the doors.** CHA release and round 3 land together, so CHA trades count fresh. Any MAL card bought before 16.65 lands in round 2 instead. Time the MAL closer after the round event.
4. **Silver-pack drag.** The SAL close scored +40.4 instead of +50 because of it.
   - Open `sobre_plata` right after the CHA release and before the first CHA team trade.
   - If it pulls CHA, that is free supply.

## Plan, anchored to the schedule
| When | Who | Move | Impact |
|---|---|---|---|
| Now (Duels II, 11.65) | Lucas → Aleks | Confirm the duelist is live, on mains power, with `days` handling | Protects the 13.93 duel line |
| Now | Operator | Let 17696 expire or cancel it; no MAL sales | Keeps the MAL option open |
| During Duels II | Builder | Build `intel/matches.md` from the `teams.md` collects/dumps lists × open bids; non-rivals only; giver holds 2+ | Feeds the ads and Dani |
| After Duels II → 13.0 bench | Lucas/Dani in the room | Broker the pairs above on v10 (rebate per 21:30 GUARDRAIL); refuse any pair where the receiver doesn't collect the set | Each positive pair raises our VC; target 5.0 → more |
| After Duels II | Operator | Maker asks for the LAV-02/03/04 spares (1.3 / 3.2) to t07 or t09 (≥ 10 below us) | ≈ +3 to +5 neg each |
| Tonight | Operator | RET-11 → Pilar job, floor 198 (directive) | 0 neg; keep the card otherwise |
| 22:45 | Market | Rebate settlement per GUARDRAIL | — |
| Sun open (13.363) | Operator | Read `/api/clock`, `/api/schedule` and `neg_points`; log when the round 3 event fires | Fixes the timing of every later move |
| Before 16.65 | Lucas/Dani | Tell the room "we buy CHA cards"; the operator prices them | Supply queued for the release |
| CHA release (16.65) | Operator | 1) Open `sobre_plata`. 2) Maker bids for all 10 CHA cards at the clearing levels on El Rastro or a non-rival venue. 3) Dealer CHA buys only at ≤ value, ≤ 3 per level, for the ladder. 4) Closer = a team-bought uncommon. | CHA ≈ +3.2 to +5.6 final [L, Analyst], more if the cap is 5×book |
| 17.0 / 19.0 / 21.0 benches | Market | Keep the stall or v10 live | Holds 7.5 |
| 18.65 Duels III | Aleks | 4 concurrent, 12 ticks, 10% decay: close fast | — |
| After CHA, if under budget | Operator | MAL close per directive; closer MAL-07 (uncommon) from a team after round 3 fires | ≈ +27 net (est. from the measured formulas) |
| Before 21.65 (stalls close) | Operator | All dealer deals done; cash into non-negative buys | — |

## Hypotheses to test
- **Sunday before 16.65 is round 2.**
  - Test: read `neg_points` at the Sunday open and at the round event.
  - Decides: whether it stays at 119.1 until 16.65.
- **Cap = 5×book, not flat 50.**
  - Test: CHA's closer is an uncommon from a team.
  - Decides: the measured `neg_points` jump; > 50 means 5×book.
- **The full 22.5 needs VC above the top-3 mean, or another factor.**
  - Test: Dani asks the desk; then `mm_points` / the market line after the first positive v10 pair.
  - Decides: the market component moving above 5.0.
- **A fresh-round ladder moves the board.**
  - Test: one Abuela CHA buy below list early in round 3.
  - Decides: `negotiating` at the next ~10-tick refresh.
- **The silver pack can pull CHA after the release.**
  - Test: open it at 16.65.
  - Decides: `pack.opened` best card, and the next trade's neg equal to ΔV − p with no drag.
