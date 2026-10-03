# Judge (claude-opus-5-5, Sun 00:39)

## Verdict
Holding at #3 but slipping. 30.49 (+0.0 over 15 min, −0.4 over 60 min) against Team 10 at 37.6 (gap 7.1) and Team 18 at 31.3 (+1.2/60 min; the gap grew to 0.8). Team 12 is 0.1 behind. `neg_points` have sat at 119.1 since tick 988, about 450 ticks without a scoring deal. Sunday is round 3, so expect a reset to 0 (round 2 reset [V]); the levers that matter are new deals.

## Our strategies: keep / kill / scale
- **Dealer bot**: keep, but only for CHA/MAL cards at ≤ value.
  - The last 8 threads closed with no deal. The Pícaros LAV-04 thread walked (neg and ladder unchanged).
  - Ladder 0.483, but the board ignored ladder gains Sat 17:45 [L]. No ladder-only threads.
- **Trading loop**: keep in sells-only mode (cash-floor 9999).
  - Saturday: 2 accepts, +6.2 (SAL-04/RET-04 swap) and +15.5 (SAL-07/LAT-01); the rest was a `sobre_bienvenida` unknown_card loop and network errors.
  - At 09:00, verify that the 918f823 pack-ref fix is live: zero unknown_card lines.
- **Addressed spares** (LAV-03 → t04 at 6, LAV-04 → t01 at 6): kill. Let them expire at tick 1455.
  - Addressed offers fill at 0.3% vs 3.5% for open asks, and the gain is about 2.8 each.
- **SAL-11 bid 20252** (115 → t04): kill at the first tick (00:50 GUARDRAIL).
- **Flags**: dead. The cap was hit and probe 8 scored 0.
- **Team trades / page closes**: scale. They are our only proven board mover: SAL close +40.4, swap +15.5 → about +0.05 board per point (Sat).
- **v10 / Club Castizo**: scale, carefully.
  - The real-trades target is 40-50 net VC.
  - Our venue went to −5.2 once (SAL dumped to a low-multiplier holder).
  - The club engine is paused until Lucas gives an explicit go.
- **Duels**: not ours. 136 finished, 35.39 pts; the last 10 went 8 deals / 2 no-deals.

## Check the scout
- **Holds**:
  - SAL-11 cancel (cash 392, matches the GUARDRAIL).
  - Pícaros CHA targets 48-52 / ≤ 54 / 57 / 62, matching the 00:25 directive.
  - CHA rare value 112 (1.6 × 70).
  - Last CHA card from a team, since the page bonus scores only via a team trade [L].
  - Team 18 +1.2/60 min; Team 12 competes for MAL.
- **"Lucas's estimate +3.2-5.6"**: not in the data I have.
- **Wrong: "MAL value 17.5 for uncommons and rares."** A MAL rare is worth 49 (70 × 0.7); only uncommons are 17.5.
  - t09's 56 bids for MAL-09/10 are above our rare value: outbidding them costs neg_points.
  - The directive route is a Pícaros MAL rare at ≤ 49.
- **Wrong scope**: MAL is missing MAL-07, MAL-09 and MAL-10 (we hold 01-06 and 08). "Offer MAL-09/10 holders a deal" ignores MAL-07.
- **Wrong set**: "Don't sell RET/LAT closers to Team 10/18". Team 10 collects LAV/RET, not LAT. Our LAV spares are its set too.

## The 3 changes with the highest expected gain
1. **CHA page in round 3, packs first.**
   - Open the `sobre_plata` (71.6) the moment CHA releases, before any CHA buy. Pack drag cut the SAL close from the 50 cap to 40.4.
   - Then buy dealer rares at ≤ 54 (they score 0 because the price is below our 112).
   - Buy the last CHA card from a team, as the maker: up to +50, about +2.5 board at Saturday's rate [L].
   - Risk: cash (CHA needs 242-384 P by case; we have 392 before the SAL-11 cancel) and rivals bidding CHA first.
2. **MAL close, only after CHA leaves ≥ 150 P.**
   - MAL-07 from a dealer at ≤ 17.5; MAL-09/10 from the Pícaros at ≤ 49; the last card from a team (MAL bonus ≈ 46.4).
   - Never match t09's 56.
   - Risk: no dealer offers ≤ 49 before 14:00. Then stop: a partial page scores nothing extra.
3. **v10 VC, front-loaded.**
   - Lucas/Dani agree RET-09 t07 → t09 by WhatsApp at 09:00 (≈ +68 VC, most of the 40-50 target), addressed on v10.
   - Spares go as open asks per the 01:35 directive, at ≥ 9-10 (the common clearing price).
   - Risk: LAV/LAT spares can close a page for Team 10, Team 18 or Team 3, who would book up to 50 against our ~8. Pull any spare the moment a top-4 team bids for it.
