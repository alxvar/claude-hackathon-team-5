# Scout (claude-sonnet-5-5, Sat 12:54)

## Top 3 actions now
1. **Close the RET page with the last missing cards (check `value?card` first).** We hold RET-01..05 (commons), 06-08 (uncommons) and 09-10 (rares), but the page bonus is not yet counted. RET-01 to RET-10 each read 83.9, 100.4 or 149.9, which is the bonus already priced in, and RET-01's cap test already booked +50. Not in the data: which RET card, if any, is still missing. Check before spending. Operator, manual. Effect: at most +50 neg_points, and only if a team trade completes it. Confidence: low.
2. **Keep ladder sells to Pilar, small steps, offer-only.** Evidence: MAL-07 at 19 gave +0.050, MAL-06 at 19 gave +0.040, and SAL-08 at 23 after a jump gave only +0.019. Pilar median is 22 over 15 trades (uncommon). Next cards: none left in our holdings that qualify (no MAL/SAL uncommons held), so use the next uncommon we hold only at a price ≥ our value and Pilar's final ≥ 18. Her limit is 6 deals/team/hour. L3 has 3 deals already, and the cap is [L] ~0.15, with ladder now 0.181. Expected effect: ≈ 0, since we are past the cap [L]. Confidence: low. Skip unless the first deal moves the ladder.
3. **Sell spare commons as maker, only to teams more than 10 points below us.** The nine open offers are 4-11 P (e.g. 8247 SAL-01 at 11 to t06, 8050 MAL-04 at 9 to t15). Evidence: t04 bids RET-02 at 10, and RET-05 asks sit at 12. Our RET-01..05 are page cards, so do not sell them. Executor: `trade.py`, keeping the asks addressed to t15, t16 and t06. Effect: cash for Sunday's CHA page. Our value gain is about +2 to +4.7 per trade, as with SAL-01 at 7 (+4.7). Confidence: med.

## What the climbing teams are doing
- **Team 14 (#1, +3.3/h)** has only 23 deals. It collects LAV/RET/LAT and bought LAV-10 at 82 from Team 16 (tick 375, Team 6 as buyer). Fewer deals, bigger value per deal.
- **Team 6 (+6.4/h)** has 31 deals and bid LAV-09 at 99 and SAL-09 at 68. It bought RET-09 at 84 (t06→t02, tick 504). It is paying near-book prices for page cards.
- **Team 12 (#4)** sold SAL-10 at 76 to t08 (tick 556) and bought LAT-07 at 19 and LAT-01 at 7. It sells rares to buyers at book and buys cheap uncommons and commons.
- **Dealers are competing for epics.** Team 8 sold LAV-11 to Pilar at 140.

## Threats
- **Team 6 bids LAV-09 at 99 and RET-09 at 84.** It is racing us for LAV/RET rares. Our LAV-09/10 and RET-09/10 are page cards, so do not sell them.
- **Team 13 (#7) bids 2 P for RET-01 to RET-05.** It is a lowball sweep and no threat, but never sell to it. Its venue v03 feeds it value created.
- **A team trade on our venue v10 can go negative (−5.2 earlier).** Avoid mm exposure from SAL/MAL dumps to teams that value them less.
