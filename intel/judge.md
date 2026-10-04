# Judge (claude-opus-5-5, Sun 05:49)

## Verdict
Holding at #3 (30.5). We trail Team 10 by 7.1 and Team 18 by 0.8, and lead Team 12 by only 0.1. `neg_points` has sat at 119.1 since tick 988, about 460 ticks with no scored deal.

## Our strategies: keep / kill / scale
- **In-room / page team trades: SCALE.** They are our two largest gains: SAL-06 from t08 at 28 (+40.4) and the t07 swap SAL-07↔LAT-01 (+15.5).
- **Trading loop: KEEP, fix first.** It made 2 accepts all Saturday (+6.2, +15.5). It hit `unknown_card sobre_bienvenida` every minute (22:41–22:45) and DNS errors on `/api/clock` overnight.
- **Our bids/listings: CHANGE.** We posted 414 listings for 17 team trades. Only 2 offers are live, both addressed asks at 6, which is the low-fill mode (0.3% vs 3.5% for open asks).
- **Dealer bot: KEEP, fodder only (directive 00:44).**
  - Ladder went 0.437 → 0.483, but the board did not move with ladder (21.88 flat across 0.373 → 0.437 [L]).
  - Last thread 1554 walked correctly at Pícaros' opening bid of 4.
- **Flags: KILL.** The cap is spent (net +20; flag 8 scored 0 after 62 min).
- **Duels (Aleks): KEEP.** Duel points are 35.39; the last 10 show 8 deals and 2 no_deal.

## Check the scout
- **Holds:**
  - Spare LAV-03/04 are worth 3.2 each.
  - t09 is #16 at 23.3, so RET-09 t07→t09 passes the feeding rule.
  - +67.6 VC is from directive 01:00.
  - Team 12 at 30.4 is 0.1 behind us.
  - ≈0.05 board per neg point, as measured at Sat 17:46.
- **Fails:** "t04 and t01 both ≥ 10 below us" is false.
  - t01 is 25.6 (4.9 below) and t04 is 25.1 (5.4 below).
  - Both collect LAV. Whether LAV-03/04 closes their page is not in the data.
  - A page closer at 6 could hand them up to +50 for our +2.8.
- **Fails:** "MAL-07 and MAL-09 are the missing cards" is incomplete.
  - We hold MAL-01..06 and MAL-08, so MAL-07, MAL-09 and MAL-10 are all missing.
  - That is 1 uncommon + 2 rares, about 166 P at Rastro clearing prices (MAL uncommon 26, rare 70).
- **Fails:** the RET-11 "bid below ~198 loses" threat is misread. We hold RET-11 (value 198); the directive is a sale to Pilar at ≥ 198.
- **Unverified:** "Team 18 +0.8 per 30 ticks" comes from tick 1424. The metrics show +0.0 over 60 min because the market is closed.

## The 3 changes with the highest expected gain
1. **MAL cash gate check, before 09:00 (Operator).**
   - Cash is 392. CHA costs A 242 / B 250 / C 282, which leaves 150 / 142 / 110.
   - Only case A meets the "≥ 150 after CHA" GO (directive 01:40). The 00:46 log line "full MAL fits in every case" contradicts this.
   - Plan the MAL close for 3 cards, not 2.
   - Fund the gap with the RET-11 → Pilar thread at ≥ 198 (score-neutral, as directed). If she won't pay, MAL waits.
   - Effect: unlocks a +30 np close past our cap. Risk: Pilar's only epic price in the data is 140 (LAV-11), so 198 may not fill.
2. **Cancel offers 19979 and 19981 now; the server accepts cancels while closed [V] (Operator, `trade.py`).**
   - Both buyers fail the ≥ 10-below rule.
   - Relist LAV spares at page-closer price (§4A: open 35–45, adjust; low-multiplier buyers won't pay 45), addressed only to teams ≥ 10 below us.
   - Never relist at 6 as open asks: Team 10 (#1) collects LAV.
   - Effect: avoids up to +50 to near rivals. Risk: forgo about +5.6.
3. **Fix the trader before the 09:00 restart (Builder).**
   - Drop `sobre_bienvenida` from its card list.
   - Retry on DNS error instead of looping errors.
   - Restart with the cash floor per the 00:40 log (464, above our 392 cash, so it only sells, as intended).
   - Effect: restores the lever that produced +21.7 on Saturday. Risk: low; stop it at T−5 before Duels III per directive 01:30.
