# Judge (claude-opus-5-5, Fri 22:30)

## Verdict
**Falling behind.** We are 16.5, #9 (−1.3 over 60 min). Team 13 is 30.0 (+2.2), so the gap widened from 10.0 to 13.5. `neg_points` rose +6.0 (24.1 → 30.1), but the score moved only +0.1, where D7 predicts about +0.9. Two things fit that gap: the field is filling Chato slots (t02, t04, t08 unlocked at ticks 121-126) while we have 0 completed Chato deals, and the leader is rising.

## Our strategies: keep / kill / scale
- **Autoflip: KILL (stays off).** Measured −11.8 on the MAL-07 buy against +6 at best on a resale.
- **Dealer bot on Chato: KEEP, capped at ≤32.**
  - Thread 228 (LAV-06): Chato is at 31, we are at 30. It has been stuck on `hold_accept_duel_live` since 22:24.
  - A buy below our value scores about 0 `neg_points`; its only payoff is the level-2 ladder, where we have no deals.
- **Trading loop: VERIFY it is alive.** Its last log line is a `rate_limited` error at 21:50, with nothing in 38 min. Uptime is not in the data.
- **Our listings: KEEP the format, but retarget.**
  - Market-priced team sales scored +7.7 (LAV-04 at 9) and +6.0 (SAL-06 at 26).
  - Offer 1415 (LAV-04 at 9, "to anyone") is unfilled while two rival asks sit at 10, so demand has stalled.
  - MAL-06 (17.5) is not listed at all.
- **Our bids: NONE open.** The 10 bids from 21:20 are gone. Purchases from teams score value − price − fee (+1.9 on SAL-08), so this lane is idle.
- **In-room trades: SCALE for LAV-06/07 only.** These are the only buys that score `neg_points` (value 32.5).

## Check the scout
- **Holds:**
  - Team 7 bought LAV commons at 9-10 (ticks 105-107).
  - LAV-04 at 9 gains +5.8 (cheapest copy 3.2).
  - SAL-08 went from 18 to 35.
  - Team 4 bids 85 for LAV-10 (it is offer 2021, not 1909).
- **Wrong:**
  - "Team 17 sits below the top 3": it is now **#3 at 23.7 (+8.9 / 15 min)**, so never feed it. Dani's table naming Team 17 as best MAL buyer is stale for the same reason.
  - "Team 10 bids 110 for LAV-09": per D6, the bid is gone and Team 10 holds LAV-09.
  - "Team 17 +5.9 / 60 min": the metrics say +12.1.
  - "Team 2 looks like a LAV-06 seller": it *bids* 7 for LAV-06, which makes it a buyer.
- **Not in the data:** the SAL-07 ask at 32 is not in the asks list.
- **Feeds a team above us:** "Team 8 at 24" is Dani's estimate; no open Team 8 MAL-uncommon bid exists. Team 8 is #5, above us.

## The 3 changes with the highest expected gain
1. **Close level-2 Chato deals the tick the duels end.**
   - Accept LAV-06 at 31 (≤32.5), then run `abuela_bot.py --dealer chato` for LAV-07 with cap 32.
   - Effect: fills empty level-2 ladder slots (a missing deal counts 0) and enables the D3 page test, `GET /api/me/value?card=LAV-09`.
   - Risk: the duel end tick is not in the data, and Saturday's Duels I freezes accepts again (D8).
2. **List MAL-06 `to` t15 at 22** (t15 is #17 and paid 21 for MAL-06 at tick 103), next to the existing MAL-07 offer at 22.
   - Effect: about +4.5, with no fee because they accept.
   - Risk: if unfilled by tick ~140, step to 21 rather than switch to Team 8 or Team 17.
3. **Cancel offer 1415 and re-list LAV-04 at 9 `to` t07** (Team 7 is #13 and bought LAV at 9-10). Use t01 as the second choice; it collects LAV and has no trades yet.
   - Effect: about +5.8 per copy, and a leader can no longer take it.
   - Risk: Team 7's LAV demand may already be filled; there have been no LAV buys since tick 107.
- **Hold:** LAV-10 (single copy, worth 91 > 85 bid) and both packs, pending Lucas.
- **Updated D5 buyers if a pack gives a rare:**
  - Avoid t12 (82, #2) and t17 (#3) for MAL-10.
  - MAL-09 → t08 at 68.
  - LAT-09/10 → t18 at 55.
