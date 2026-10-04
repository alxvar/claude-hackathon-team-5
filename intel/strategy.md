# Strategist (claude-opus-5-5, Sun 00:12)

## How the points really work
- **Board = Negotiating + Market** (ours 22.99 + 7.5 = 30.49). Judges' 40 come on top and sit outside the board.
- **Remaining game.** Final game part = (0.5·Fri + Sat + Sun)/2.5 ≈ (1.5 × today's board + round 3)/2.5 [L: RULES weights].
  - To catch Team 10 (37.6) we must beat it by **≈10.7 board in round 3**.
  - Team 18 needs only 1.2 more. Team 12 is 0.1 behind us.
- **Negotiating** (relative, leader = top):
  - Team trades: ΔV − p − taker fee, capped at 50 per trade [V]. ≈ +0.05 board per point [V Sat 17:46].
  - Dealer deals: never add. Losses count in full.
  - Ladder: best 3 deals per level. Its board effect has been flat since 17:45 [L].
  - Flags: spent (≈3 scored per team [V]).
  - Duels: 35.39 pts, 0.54/deal in Duels II.
  - Round 3 should reset neg and ladder for everyone (round 2 did [V]).
- **Market 30 = Market Test 7.5 + Real trades 22.5** [organisers' deck].
  - Market Test: six benches, nobody above the stall. Everyone sits at 7.5, so it gives no differential.
  - Real trades: the best market on the board is 12.5, i.e. +5 of 22.5. Every other team shows 0. **This is the field's weakest component and the only one with room for +10.7.**
  - What earns the full 22.5: not in the data (desk question). VC is net: a card moving to a lower-multiplier holder subtracts (−10.2 at tick 398 [V]).
- **Judges 40**: format and time not in the data. It is the only block bigger than Team 10's lead.

## Our winning strategy
1. **Own the real-trades component on v10 (the Club Castizo desk).**
   - Broker page-finishing trades and cashless duplicate swaps between non-rivals, collector ← dumper only (buyer's set multiplier > seller's, judged from the collects/dumps profiles).
   - Being the first venue with VC in round 3 sets the top-3 reference.
   - Never put t10, t18, t12 or t06 on either side.
2. **CHA page (1.6×), bought from teams wherever possible.**
   - Every CHA card bought from a team below value scores (value − price). A dealer buy scores 0.
   - At Saturday's clearing prices (9 / 24.5 / 70) a full team-sourced page is worth ≈ +35 commons, +46 uncommons, +84 rares, + the capped close. That is about 258 P of cash vs ≈330 via dealers.
   - Fallback: Abuela commons at ≤ 10 (adds L1 ladder), then Pícaros rares at 48-54 (Chief). The last card always comes from a team, as maker.
3. **Duels III + Grand Final**: maximise the deal rate (2 of the last 10 were no-deal) in ≤ 2 exchanges at 10% decay.
4. **Stop:**
   - Egg probes, flags, Chato.
   - Dealer threads for the ladder alone (until H3).
   - LAV-03/04 asks to t04/t01 (they fail the feeding rule): cancel at 09:00.
   - RET-12, gold pack, any board bond (Lucas: keep the stall).

## Levers nobody is using yet
- **Venue real trades.**
  - Evidence: all 46 Friday team trades were on El Rastro. Saturday's best market was only +5 of 22.5.
  - Exploit: brokered trades on v10 from the open (Lucas + Dani).
  - First trade: the RET-09 → t09 match (VC ≈ +134). Confirm whether the seller is t07 or t08 first: the logs disagree, and t07 collects RET.
- **Cashless swaps of our spares for CHA cards.**
  - Spares: LAV-02 (two spare copies at 1.3 each), LAV-03 and LAV-04 (3.2 each). LAT-03/04 (5 each) only if Lucas OKs releasing them.
  - A first-copy CHA common is worth 16 to us, so a swap ≈ +11 to +14.7 neg each and saves CHA cash.
  - Evidence of non-use: not in the data. The swap feature is confirmed [V], but no swap counts appear on the feed tables.
- **Duel twins.** RULES: every pair plays "on the same scenarios", once as seller and once as buyer.
  - If our buyer-side twin duel (same item, adjacent id) carries the rival's limit and days weight, we know both sides.
  - Days: in our last 10 duels every buyer weight (3.68-7.75) exceeds every seller weight (1.15-3.34). If that holds, days = 0 maximises the pie. As seller, trade days for price.
- **RET-11 to a team, not a dealer.**
  - Pilar at 198 scores 0 (clipped). A team sale at > 198 scores positive: t12 paid 216 [V tick 1245].
  - Only t07 (20.2) passes the feeding rule. Offer it as maker on a club venue at ~216 after 09:00. Pilar ≥ 198 is the fallback.

## Plan, anchored to the schedule
| When | Who | Move | Expected impact |
|---|---|---|---|
| 08:30-08:55 | Operator | Restart all bots on HEAD 918f823. Cancel 19979/19981. Read the feed's `offer.listed` for the maker of the SAL-11 245 ask | Clean start |
| 08:30-08:55 | Aleks | Duel-twin and days analysis on our 136 duels (offline, 0 P) | Sets the Duels III rules |
| 09:00 | Dani | Desk: what earns the full 22.5? Does the round reset neg and ladder? Judging format and time | Removes the biggest unknowns |
| 09:00-09:03 (round 3, CHA release, +150) | Operator | Read /api/me (H1). Open sobre_plata after the release, before any trade (pack drag cost −9.6 on the SAL close). SAL-11 counter ≤ 125 if t04 is the maker; cancel if no fill in 10 min | SAL-11 ≈ +2.3 board |
| 09:00-11:00 | Operator + Dani | CHA maker bids addressed to non-rival teams. Spare-for-CHA swaps. Abuela commons ≤ 10. Pícaros rares ≤ 54 with the trick guard on (check the card id) | CHA +3.2-5.6 final [L] |
| 09:00-14:00 | Lucas + Dani | v10 club: RET-09 → t09 first, then matches.md pairs every 12 min, swaps first | Sim: +3.9-4.8 of 5 for +89 VC |
| 09:21 / 11:21 / 13:21 benches | Market | Stall only; record | 0 |
| ~10:00 | Operator | RET-11 ask to t07 at ~216; Pilar ≥ 198 if unfilled by 12:00 | +18 neg, or 0 |
| 11:00 Duels III | Aleks | Twin and days rules, close in ≤ 2 exchanges | Not in data |
| 11:00-12:00 | Dani | Pitch draft: measured-facts pipeline (cap 50, pack drag, flags, ladder) and the club as market design | Judges 40 |
| 12:00-13:30 | Operator | Last CHA card from a team, as maker. MAL close only if CHA came in under budget (directive) | +50-capped close |
| by 13:45 (warning 13:48) | Operator | All dealer deals done before the 14:00 stall closure | — |
| 14:00 Grand Final (big screen) | Aleks; Lucas + Dani | Duelist live; pitch rehearsal | Judges visibility |
| to 14:54 | Operator | Cash into non-negative team buys only | Cash scores 0 |

## Hypotheses to test
- **H1. Round 3 resets neg and ladder.** Test: read /api/me at 09:00-09:03. Decides: neg_points → 0.
- **H2. Real trades scale with VC relative to the top-3 mean.** Test: the first club trade on v10 (RET-09). Decides: our `market` at the next board refresh.
- **H3. The ladder moves the board on Sunday.** Test: one Abuela CHA common at ≤ 10 in a clean window. Decides: `negotiating` changes while neg_points stays flat.
- **H4. Duel twins reveal the rival's limit and weight.** Test: offline pairing of our 136 duels. Decides: whether rivals' accepted prices in our seller duels respect our twin buyer limit; buyer weight > seller weight in every pair.
- **H5. Low-CHA teams sell CHA at Saturday clearing prices.** Test: maker bids at 9 / 24 / 70 for 10 min. Decides: fill rate (Saturday baseline: 9% of bids filled).
