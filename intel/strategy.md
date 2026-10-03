# Strategist (claude-opus-5-5, Sat 18:07)

## How the points really work
- **Final** = game (0.5·Fri + Sat + Sun)/2.5 × 60 + **judges 40** [desk]. The judges are the largest single block. The pitch is 3 min, free format, Sunday after 15:00.
- **Negotiating 30** is made of three parts:
  - Team trades: min(cap, ΔV − p − taker fee), not capped in total; ≈ 0.048 board per neg point (t07 swap: +15.5 → +0.74).
  - Duels: our score is 13.93.
  - Ladder: [L] spent for us. `negotiating` stayed at 21.88 while the ladder went 0.373 → 0.437.
  - Flags: spent (3 scored, +20 net).
- **Market 30** has two parts:
  - Bench: the stall earns half; the full points go to the top-3 mean.
  - Value created (VC) between other teams on our venue: net, signed. One trade moved our market 7.5 → 12.5, the next moved it back to 7.5 at −5.2 [V].
  - Our market is 7.5 against the leaders' 9.15-12.5. **This is the field gap we can close fastest.**
- **Relative scoring**: we are #3 at 29.9. t14 is 1.9 ahead, t06 0.7 ahead, t03 (28.6) and t01 (28.3) are close behind.
- **Rounds are cut by `round` events, not by calendar days** [V: Saturday's reset fired at tick 160, not at 09:00]. Converted to wall time [L, from fever 9.15 ≈ 18:04 and close 14.077 = 23:00 / Sun 09:00]:
  - Round 3 starts at game hour 16.65 ≈ **Sun 11:34**.
  - So **Sunday 09:00-11:34 still scores in round 2**: about 2.5 h of 15 s ticks, plus the hard bench (≈ 09:34) and a bench (≈ 09:55).
  - Round 3 is only ≈ 11:34-15:00, with benches ≈ 11:55, 13:55 and 15:55 (after the close: keep the venue open).
- **Cap form is still open**: flat 50 vs 5×book. Every capped observation was a common, so the form decides how Sunday's page should close (see below).

## Our winning strategy
**Tonight:** close SAL, keep v10 VC positive, win Duels II. **Tomorrow:** CHA page and CHA trades in a 3.4 h round 3, closed on an uncommon.

1. **SAL-06 close** (bid 14268, 42 P → t02): +40.1 neg ≈ +1.9 board. The cap binds only at ≤ 32 P. Pilar pays ~31 in the fever, so 42-45 wins.
2. **v10 VC is worth more than any trade**, because one +5 trade = +5 market. It is also the biggest risk, since a single negative trade erased it. Only room-arranged pairings: seller dumps the set, buyer collects it, buyer holds 0 copies, no rival (judge's rule).
3. **CHA (1.6×)**: values are common 16, uncommon 40, rare 112, page bonus 106.
   - Every CHA buy from a team at below value scores in full: e.g. common at 8 → +8, rare at 85 → +27.
   - Dealer buys at ≤ value score 0; use them only for supply.
   - Rares first: 30 copies, and ~3 teams hold 1.6 for some set.
4. **Close CHA on an uncommon, not the cheapest common.**
   - If the cap is flat 50: we lose ≈ 7 vs closing on a common (58 vs 65).
   - If the cap is 5×book (125): we gain ≈ +64 (129 vs 65).
   - Closing on a rare: −19 / +64. The uncommon has the best downside.
   - The cap headroom (value + bonus − 50) is also our outbid budget for the scarcest card.
5. **Stop:**
   - Ladder-only deals, flags, and Workshop runs (0 score).
   - Selling MAL/LAT at +2. Hold MAL-01..05, MAL-08 and LAT-03/04 as **CHA swap currency**: no cash, about +9 per common swapped vs +2 now.
   - The 0-P LAV-02 offers 14199/14226, unless a card comes back.

## Levers nobody is using yet
- **Sunday 09:00-11:34 = round 2.**
  - Evidence: the schedule puts the `round` event at 16.65 and Saturday's reset came at the round event. No rival behaviour on this is in the data.
  - Exploit: run the full maker book and v10 pairings at 09:00, and make sure the venue is right for the 09:34 hard bench.
- **Uncommon closer for the cap.**
  - Evidence: GAME.md marks flat-50 vs 5×book as open, with n=3, all commons.
  - Exploit: the CHA page closes on the uncommon we buy from a team.
- **Board mechanism as a VC veto** [?]: on `auto`, every trade on v10 crosses, including negative ones. A broker would match only the agreed pairs (identified by exact card + price), but makers show as pseudonyms. Test before any use.
- **Swaps as Sunday cash.**
  - Evidence: cash is 151, or 109 after SAL-06. With the +150 grant that is ≈ 259, against ≈ 265 for a full CHA page at clearing prices.
  - The t07 swap scored +15.5 for 0 P.
- **Banco L5 head start**: we have negotiated L4 deals (SAL-09/10 bought 73 → 54; Café sold 4 → 5). A missing deal counts 0 at the highest-weight level, so 3 sells of spares above its opening, not 1.

## Plan, anchored to the schedule
1. **Now-18:32 · Operator + Dani.**
   - Hold 14268 and counter up to 45. Dani confirms in person that t02 holds SAL-06.
   - At 18:20, fallback t17 then t13, one at a time. Expected ≈ +1.9 board.
2. **Now-19:55 · Dani + Operator.** v10 pairings that pass the judge's rule: t02 SAL-03 → t08 and t02 RET-03 → t07. Drop t07 RET-01 → t09. Expected up to ≈ +3-5 market [L].
3. **≈ 19:55 bench (11.0) · Market session.** Record `bench_offers` and run a replay check of broker vs stall. No venue change tonight without a replay ≥ stall + 2 pp.
4. **≈ 20:34 Duels II (68 duels, 6 at a time, decay 8%) · Aleks.**
   - Send full price + days packages and concede the days we weight low.
   - Close by sending the rival's own standing price.
   - At ≤ 2 ticks left, accept any in-limit offer.
5. **Banco active · Operator.** Sell spares (LAV-02 ×2, LAV-03, LAV-04) above its opening bid and ≥ value. Never a page card.
6. **≈ 21:55 bench; 22:00-23:00 · Operator.** Re-post unfilled maker offers at 2× ticks. Cash ≥ 100 overnight (guardrail).
7. **Sun 09:00-11:34 (round 2) · Operator + Dani.**
   - Maker book and positive v10 pairings.
   - Venue live and supervised for the 09:34 hard bench and the 09:55 bench.
8. **Sun 11:34 CHA + grant (11:37) · Operator, Dani, Lucas.**
   - Bid all 10 CHA cards to teams that pulled them (`pack.opened`) or list them, at ≤ value.
   - Order: rares, then commons, then the uncommon closer last.
   - Offer MAL/LAT swaps to MAL collectors (t13, t17, t15; never t01/t03/t10/t14/t06).
9. **Sun 13:34 Duels III · Aleks.** 4 at a time, 12 ticks, decay 10%: close in ≤ 2 exchanges.
10. **14:00:** cash → 0 into non-negative buys.
11. **15:00-16:00 · Lucas + Dani.** 3-min pitch: measured-facts table, cap discovery, round-boundary exploit, VC control. Rehearse tonight during Duels II.

## Hypotheses to test
| Hypothesis | Cheapest experiment | Deciding metric |
|---|---|---|
| Sun 09:00-11:34 scores in round 2 | One maker fill at 09:05 | `neg_points` adds to Saturday's total and does not reset until the 11:34 `round` event |
| Cap = 5×book (not flat 50) | Close CHA on an uncommon bought from a team | Score > 50 means 5×book; exactly 50 means flat |
| Ladder still moves the board | One Banco sale above its opening | Our `negotiating` vs t14's at the next refresh (≈ 10 ticks) |
| v10 can switch to `board` and veto negative VC | Read the v10 venue record and the API for a mechanism change (no write) | The endpoint exists, and its cost is not in the data |
| VC saturates near +5 market [L] | Next positive v10 pairing | `market` rises above 12.5 or stays flat |
| Sunday packs contain CHA after release | Watch `pack.opened` `best` after 11:34 | Any CHA pulls, i.e. whether our kept pack is worth opening |
