# Strategist (claude-opus-5-5, Sat 10:49)

## How the points really work
- **Negotiating 30** has three parts: duels, ladder and team-trade value.
  - Ours now: `neg_points` 28.5, ladder 0.055, duel **0.0**.
  - Team trades score ΔV − price − fee (taker only), capped at +50 per trade. The cap is flat 50 or 5×book.
  - Dealer deals score min(0, ·). They pay only through the ladder.
  - The ladder takes the best 3 deals per level, and a missing deal counts 0. Higher levels weigh more.
  - We have 0 at levels 2 and 3: none of our 6 Chato deals counted, and we have no Pilar deal.
- **Market 30** has two parts.
  - Bench: the stall is half, and full points go to the mean of the top 3. Our bench number is not in the data.
  - Value created between other teams on our venue: t12 scored 9.9 against the stall's 5.94 from just 2 trades (snapshot 250). That is the cheapest relative component on the board.
- **Judges 40**: the largest single block, and it is not a function of trades.
- **Everything is relative.** Our +50 RET close came with +5.0 board in 15 min, so ≈0.1 board per `neg_point` today [L].
  - The gap to #1 (t18 30.3) is 6.1, about 60 points.
  - t14 (−0.8) and t13 (−2.1) can each pass us with a single +50.
- **Where the field is weak**:
  - Duels: 102 scored today, and everyone sits near 0 before Duels I.
  - Team venues: Friday had 0 trades on them, and only t12 has a measured gain.
  - Higher ladder levels: only t13 is known to be at level 3.
- **Cap consequence**: cash scores nothing at the end. The best use of a P is a team buy where our value − price approaches 50.
  - Page-closer at 9: +50 (5.5 per P).
  - CHA common at 9: +7.
  - CHA rare at 70: +42.

## Our winning strategy
**Today: win duels, monetise spares, host other teams' trades. Sunday: buy CHA (1.6×) from teams, not dealers.**
- **Duels (102)** are the biggest untouched pool. The measured rule is rounds = min(our messages, theirs). So we play:
  - one anchor, then silence;
  - accept an in-limit offer by ticks_left ≤ 3.
  - Practice lost ~14% to decay; ≤ 2 rounds at 6% loses ≤ 11.6%.
- **Book fills**: about +60 `neg_points` sits in 13 addressed asks, and Saturday has had 0 fills.
  - The only Saturday fill (RET-01, +50) came from an in-room push.
  - So the constraint is human contact, not price.
- **Venue v10 (0%, auto)**: every trade between other teams on it scores market points for us. We sell it as "0% vs El Rastro's 5% + 1 P".
- **Sunday CHA**:
  - Team buys below value score; dealer buys score 0 at best.
  - At Friday clearing prices, a full page from teams costs ≈258 P. It yields ≈ 5×7 + 3×15.5 + 2×42 ≈ 165, with the closer replaced by +50.
  - The close is a team trade (the page bonus scores only that way).
- **Stop**:
  - Chato buys (−21.5 today, 0 ladder, no unlock).
  - Abuela deals for the ladder alone (level 1's best 3 are banked).
  - Packs, deals at a dealer's opening price, buying to resell, public asks.
  - Feeding t18/t2/t12, and in practice t14/t13 too (both within one page-close of us).
- **Why this beats the leaders**: t18 pays up (RET-02 at 49) and t2 flips with markups. Both buy points with cash. We buy points with measured formulas, and cash is worthless at the end.

## Levers nobody is using yet
1. **Brokering other teams' trades onto v10.**
   - Evidence: Friday had 0 team-venue trades and all 46 went through El Rastro. Only t12 (+3.96 market from 2 trades) and t13's lobbying show any use.
   - Exploit: Dani matches public bids and asks between non-top-4 teams and says "repost on v10 at 0%". A page-close between two others there creates big value for our venue.
2. **The close order depends on the cap's form.**
   - If the cap is 5×book, closing CHA with a rare from a team scores up to 218 − 70 = 148, against 50 for a common close.
   - If the cap is flat 50, the common close is better (92 vs 57 total for the same two buys).
   - Nobody has measured this. Dani asks the desk now.
3. **High-value singles for the +50 cap.** First copies of LAV/RET/CHA epics and legendaries are worth 234/585 (LAV), 198/495 (RET) and 288/720 (CHA) to us.
   - `pack.opened` publicly shows each pull's best card.
   - Builder: scan the feed for LAV-11/12, RET-11/12 and CHA-11/12 holders. Operator: post addressed bids to non-top teams at ≤ value − 50.
   - This needs cash above the 100 floor, which only Lucas can grant by GUARDRAIL.
4. **Dealer sales for ladder levels 2 and 3.**
   - Every ladder test so far was a buy. A negotiated sale at ≥ our value costs 0 `neg_points`.
   - We have 0 at levels 2 and 3, and those weigh more.
5. **Flags**: a correct flag scores. Radio Rastro airs news where "some of it is true", and dealers "lie". No team is known to flag; what a flag scores is not in the data.

## Plan, anchored to the schedule (wall ≈ game hour + 6.83 h; Sunday mapping not in the data)
1. **Now–11:40 (operator)**:
   - Offer 4322 (SAL-01 → t03 at 40) fails §4A: a 40 fill implies it closes t03's page, and t03 is only 6.9 below us. Let it expire at tick 311.
   - Repost SAL-01 at 40 addressed to t16 (SAL/LAT collector, ~11 below us).
   - Repost all expiries with 2× the ticks wanted.
2. **Now (Dani)**:
   - Ask the desk: cap form (flat vs 5×book), flag scoring, whether auto-venue crossings use the team's accept, and the ladder rule for dealer sales.
   - In-room push on live asks: t01 (MAL-07 4448), t17 (MAL-06/02), t15 (LAT-08/04, MAL-04), t07, t09, t16.
3. **11:40 / 11:50 (operator, directive)**: dealer threads stop, then the trader stops. Bench 5.0 runs on v10.
4. **Duels I ≈ 11:59 → (Aleks)**: one anchor, then silence. Accept in-limit offers at ticks_left ≤ 3. No restating prices.
5. **During Duels I (Lucas + Dani)**:
   - Draft the judges' pitch: measured-fact table, cap test, the two page closes.
   - Run the v10 brokering pitch to non-top-4 pairs.
6. **After Duels I (operator)**: one Pilar sale of a spare uncommon (LAT-08 or MAL-06), only if no team fill, at ≥ our value and above her list. Measure the ladder delta.
7. **≈16:00–18:00 SAL fever**: if SAL-08 is unsold to a team, sell it to Pilar at ≥ 31 (0 `neg_points`, cash plus a level-3 deal).
8. **Duels II ≈ 18:29**: zero dealer threads (directive); Aleks runs the `days` logic.
9. **Evening to 23:00**: push book fills to fund CHA.
   - Cash on hand is 107; Sunday's grant is 150; the book is ≈ +160 P if everything fills.
   - Lucas orders the board-venue bond (270) against the CHA page (~258); both don't fit.
10. **Sunday, CHA release (game hour 16.65)**:
    - Operator posts addressed bids to the teams that list or pull CHA; Dani pushes in the room.
    - No Chato CHA buys while team asks at ≤ value exist.
    - Close per the cap answer. Never sell CHA to a team that collects it.

## Hypotheses to test
- **H1, cap = flat 50 or 5×book.**
  - Experiment: desk question, otherwise Sunday's first uncommon/rare close with uncapped gain > 50.
  - Decides by: measured score of 50 vs > 50.
- **H2, negotiated dealer sales at ≥ value count for the ladder.**
  - Experiment: one Pilar sale after Duels I.
  - Decides by: `ladder_points` delta (Abuela reference: +0.003–0.018 per deal).
- **H3, other teams' trades on v10 lift our market score.**
  - Experiment: the first brokered non-top-4 trade on v10.
  - Decides by: our market component vs the stall teams (5.94) in the next snapshot.
- **H4, min-message duels keep more of the pie.**
  - Experiment: Duels I, comparing duels where we sent ≤ 2 messages with those where we sent more.
  - Decides by: duel points per finished duel and `rounds`.
- **H5, correct flags pay.**
  - Experiment: the desk answer, then one flag on a Radio item that the feed contradicts.
  - Decides by: score change after the flag.
- **H6, auto-venue fills don't consume an accept.**
  - Experiment: desk answer, or watching a v10 cross during a duel tick.
  - Decides by: whether the crossing team's duel accept fails on the same tick. If not, "fills without your accept" becomes the v10 pitch.
