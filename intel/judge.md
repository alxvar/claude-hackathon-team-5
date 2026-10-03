# Judge (claude-opus-5-5, Sat 20:22)

## Verdict
**Falling behind the leaders.** We are #3 at 31.6 (−0.0 over 60 min). Team 10 is at 34.0 (+1.9) and Team 6 at 32.6 (+1.1). `neg_points` has been flat at 119.1 since tick 988, which is 213 ticks without a scored deal. The gap to #1 is 2.4.

## Our strategies: keep / kill / scale
- **In-room page closes: scale.** SAL-06 from t08 at 28 gave +40.4 `neg_points` (tick 988), and the board went #4 → #3. That one trade is about 1/3 of our total `neg_points`.
- **Dealer bot: kill.**
  - The ladder is capped, flat at 0.437 since 17:45.
  - The last 8 threads (ticks 1044-1076) were all closed with no deal.
  - Picaros LAV-04 walked at her final of 4 (worth 3.2), with 0 effect.
- **Trading loop (auto-accept): keep. Restart only on the Chief's clearance.**
  - It made 2 accepts today: SAL-04/RET-04 swap +6.2 and SAL-07/LAT-01 swap +15.5. That is our best non-page source.
  - Its log has no event between the 17:46 accept and the 20:15 pause.
- **Maker book: shrink to fillable asks.** 0 fills since tick 988.
  - MAL-08: unfilled since 19:29 (24 → 20).
  - LAV-04: unfilled since 19:29 (9 → 7 → 6).
  - MAL-02 → t08 at 40: worth 7 to us, no fill. The buyer is #13 (23.5, 8.1 below us; not a rival, but the ask won't fill at 40).
  - Best case for the whole book is about +2.5 each.
- **v10 / market lever: unmeasured.** Our current `mm_points` and the v10 fills tonight are not in the data. Report them before spending more effort.
- **Duels II: keep.** The last 10 shown are 9 deals and 1 no-deal (`duel` 13.93). Per-duel surplus is not in the data.
- **Flags: done** (net +20, cap reached [V]).

## Check the scout
**Holds:**
- Team 7's RET×8 and LAV×7.
- RET-09 t04→t07 at 66 and RET-10 t06→t07 at 77.
- Team 12's LAT×6, 64 deals, LAT-09 at 55.
- Team 3 sits 1.6-1.8 behind us and is rising.
- MAL-08's best gain is +2.5.

**Wrong:**
- **"Any trade on v10 lifts Team 10's market."** v10 is OUR venue. Team 10's venue is v07. Following this would kill our only market lever.
- **"t04 is a live MAL-08 buyer."** t04 bought MAL-08 from t12 at 14 (tick 1142), so it now holds one. A second copy is worth 25% to them.
- **Team 10's "+2.5 in 60 min".** Metrics say +1.9. "Market-making plus our old swap" is not in the data, and that swap was at 10:18.
- **Team 12's "+1.1/60".** Metrics say +1.0 (+1.1 is Team 15).
- **"Team 6 is a seller, not a buyer".** It bought SAL×4 and RET×2.

**Incoherent:** Action 3 says "bid for RET-09/10" while we hold both. Drop it.

## The 3 changes with the highest expected gain
1. **After resume, fill v10 with 1-2 positive value-created trades between non-rivals (Dani in the room).**
   - Pairs: a seller with a spare in a set it dumps, a buyer that collects that set and lacks the card. Examples: t13 (dumps LAT/LAV/MAL) → t07, t09 or t16 (RET/LAV collectors), each 4+ points below us.
   - Never t10, t06, t03 or t14.
   - Effect: ≈ +5 board per directive 17:40/19:40 [L]. That alone closes the 2.4 gap.
   - Main risk: negative value created when a card moves to a lower-multiplier or second-copy holder (t15 SAL-07 at tick 398 took us +4.99 → −5.2). Only pass trades where the buyer collects the set and lacks the card.
2. **Settle the 22:45 rebate as a ≥ 0 trade, not a gift.**
   - Buy, on v15 at fee 0, one card we lack from the partner at the owed amount (≤ 30 P). MAL-06 or MAL-07 is worth 17.5 to us. Partner holdings are not in the data, so Dani must confirm one in person.
   - Effect: about 0 to +3 `neg_points` instead of about −15 (the Operator's own estimate for a cheap card on El Rastro).
   - Risk: no partner holds such a card. Then cap the price at our value and settle the remainder per Lucas.
3. **Re-target the maker book. Executable by the Operator on resume.**
   - Cancel MAL-02 at 40 → t08.
   - Stop pitching MAL-08 to t04. Keep it → t01 at 20, or re-address it to a non-rival MAL buyer passing the feeding rule (t17 MAL×5 or t13 MAL×7) at 20, as maker.
   - Keep LAV-03 and LAV-04 at 6 (+2.8 each).
   - Effect: +2 to +8 `neg_points` (≈ 0.1-0.4 board at 0.05/np).
   - Risk: near-zero cost. Fills are rare (5% of asks filled on Friday).

Not recommended: re-buying the MAL page (4 cards missing; cash 120 vs floor 100) and dealer deals of any kind.
