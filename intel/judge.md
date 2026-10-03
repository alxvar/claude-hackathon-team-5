# Judge (claude-opus-5-5, Sat 17:56)

## Verdict
Holding #3 at 30.0 but losing ground on the top two over the hour: us −0.0/60 min, Team 6 +2.1 (30.7), Team 14 +0.9 (31.4); gap to #1 is 1.4.

## Our strategies: keep / kill / scale
- **Dealer bot: kill, except card-for-cash where our value is lower.** `negotiating` stayed flat at 21.88 while ladder went 0.373 → 0.437 across 3 deals, and flags scored 0 on probe 8. In hindsight, selling SAL-06 to Pilar at 25 (tick 669) now costs us a 35-45 P buyback. Rule: no dealer sale of a card from a page we might finish.
- **Trading loop: keep.** The t07 swap (SAL-07 for LAT-01) gave +15.5 neg and moved the board 29.24 → 29.98, our best move this hour. The t08 swap on v11 gave +6.2. Only 2 accepts since 15:29, so the loop is starved of offers to accept.
- **Our bids and listings: scale.** We have 5 live offers against the plan's 20-30. The MAL-02/05 asks at 9 (value 7, +2 each) and LAV-03 at 6 (value 3.2) have been unfilled for a while with no fill data. Offer 14062 sells LAV-02 to t17 for 0 P: kill it unless it is a swap leg. As a pure gift it is −1.3 neg for us and value for t17.
- **SAL-06 page bid 14040: keep, top priority.** Value 82.1 at 35 P as maker gives ≈ +47 neg ≈ +2.3 board, enough to pass Team 14 if they stay flat. It expires at tick 944, about 25 ticks from now.
- **In-room trades (Dani): keep.** Both swaps above came from the room. The v10 room plan has no settlement yet.

## Check the scout
- Holds: team trades are uncapped on the board (+15.5 neg → +0.74 board ≈ 0.048/np).
- Holds: Team 6 is +3.3 in 15 min, and the RET-09 t06→t12 trade at 84 happened.
- Holds: t01 (1.3 below us) and t10 (2.3 below) are both within 3.0, so both are rivals.
- Holds: t07 is the busiest buyer (LAV×7, RET×5, LAT×4).
- Holds: LAV-02 at 0 is not a sale.
- Wrong: "35 P hits the +50 cap". 82.1 − 35 = 47.1, so we are under the cap. The cap binds only at ≤ 32 P.
- Wrong: "Team 14 paid us 15 for MAL-08". We bought MAL-08 from t14 at 15 (tick 760, +2.5).
- Unverified: "2 trades ≈ the +5 cap" on v10 is [L]. The only measurements are +4.99 and −5.2, so the sign risk is real and measured.
- Not in data: whether t02 holds SAL-06. The scout correctly flags this; its "med" confidence is not supported.

## The 3 changes with the highest expected gain
1. **Confirm the SAL-06 holder in person now.**
   - Dani asks t02 whether it holds SAL-06 and to accept 14040. In parallel he asks t17 and t13 whether they hold it, so the 18:20 fallback bid goes to a confirmed holder.
   - If 14040 lapses at tick 944, re-post to t02 immediately with expires doubled (60 → ask 120). Stay inside the 45 cap.
   - Effect: +47 neg ≈ +2.3 board, the only lever that can pass Team 14 this hour.
   - Risk: addressed bids are public on the feed, so t10 sees our interest and can outbid. Keep each bid short-lived.
2. **v10 room plan, value-created check per pairing before Dani pushes.**
   - Allow a pairing only if the buyer holds 0 copies and collects the set while the seller dumps it (per `teams.md`). That rule covers t02 SAL-03 → t08 (t08 collects SAL) and t02 RET-03 → t07 (t07 collects RET).
   - Drop t07 RET-01 → t09: t07 collects RET, so the card moves away from a RET collector and value created can go negative, as with −5.2 on SAL-07.
   - Never include t01, t10, t03 or t06.
   - Effect: up to ≈ +3 board [L].
   - Risk: one negative trade erases a positive one. Multipliers of other teams are not in the data.
3. **Fill the maker book with true spares to non-rivals ≥ 10 below us.**
   - LAT-03 and LAT-04 (value 5) at 8 to t15 (LAT×6).
   - MAL-01, 03 and 04 (value 7; the MAL page is dead) at 9 to t15 or t13.
   - LAV-04 second copy (3.2) at 6 to t09.
   - Re-post anything unfilled after 10 min at 2× ticks.
   - Effect: +2-3 neg each, ≈ +0.7 board for about 7 fills.
   - Risk: low; a MAL or LAT card could complete someone's page. Keep to the ≥ 10-below rule, and t17 (5.1 below) is excluded.
