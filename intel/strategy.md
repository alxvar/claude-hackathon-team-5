# Strategist (claude-opus-5-5, Fri 22:18)

## How the points really work
- **Negotiating (30)** has three parts:
  - **Duels.** Ours is 0.0. No session has scored yet: the practice at hour 2.0 doesn't count, and the first scored one is Duels I at hour 6.5. The field is at zero.
  - **Ladder.** Capped at the best 3 deals per level, and higher levels weigh more. Ours is 0.064, all from level 1. Chato (level 2) has 0 of our 3 slots filled, and a missing deal counts 0.
  - **Team trades.** Uncapped. Our `neg_points` is 24.1.
- **Market-making (30).** No Market Test has run, and no team venue appears in the metrics or the feed, so every team is at 0. The free auto stall earns half the bench points by default. The full points go to the mean of the top three, so the only upside is a broker that beats `auto`.
- **Judges (40).** The largest share, and not in the metrics.
- **Relative and weighted.** The leader (Team 13) has 27.8 and we have 16.4, a gap of 11.4. Friday counts half.
- **Cheapest points.** Market-making (30, everyone at 0), then duels (everyone at 0), then Chato's 3 ladder slots. Neg-trades is where the field competes hardest.
- **Data conflicts to resolve:**
  - **`neg_points` history.** The lane log says it fell 26.3 → 14.5 after the MAL-07 buy. The metrics say 26.3 → 24.1 over 15 min, with our SAL-08 buy at 18 (t12) and LAV-04 sale at 9 (t07) in between. The exact breakdown is not in the data.
  - **LAV-09.** "Only one LAV-09 exists" contradicts RULES (rares print 30 copies), and Chato lists LAV-09 at 77.
  - **Team 10's 110 bid.** It is no longer in the top bids. A LAV-09 ask at 110 is now on the book.

## Our winning strategy
- **1. Own Market-making.** Open a `board` venue with fee 0 and our own broker.
  - The broker computes the max-surplus matching on `bench_offers`: sort bids descending and asks ascending, pair while bid > ask, and don't greedily cross early pairs.
  - This beats `auto`, which crosses the best pair every tick.
  - A fee of 0 also undercuts El Rastro's 5% + 1 P, drawing other teams' trades onto our venue. That value scores for us; fees never do.
  - Nobody is here yet, and it is worth 30 points.
- **2. Fill Chato's 3 ladder slots before he opens to all at hour 2.63 (~22:58).** Two kinds of deal fit:
  - Buys below our value: LAV-06 and LAV-07 at ≤29, worth 32.5 each.
  - A sale above our value: MAL-07, worth 17.5.
- **3. Sell our low-multiplier cards to non-leaders near the buyer's value.**
  - Our low sets: LAT 0.5, MAL 0.7, SAL 0.9.
  - Buyers to target: t17, t15, t06, t04.
  - Never sell to t13, t12, t08 or t18 (the top 4).
- **4. Sunday: buy Chamberí at 1.6×.** A CHA uncommon is worth 40 to us and a rare 112. Buy from teams below those values, and from dealers only below value.
- **Stop doing:**
  - Autoflip and packs.
  - Any dealer buy above our value.
  - The LAV-09 bidding war.
  - Selling first copies below our value. Our LAV-04 ask at 9 loses 4 if it is a first copy (worth 13).
  - Feeding the top 4.

## Levers nobody is using yet
- **Own venue + optimal broker.** No team venue or Market-making score exists in the data. We exploit it by having the broker ready before the first bench (hour 3.0).
- **Zero-fee venue.** All 46 team trades so far paid house fees, and no alternative venue is listed. We open at fee 0 so other teams' trade value lands on our book.
- **Selling to dealers for the ladder.** The dealer table shows no team selling to Chato, and only 2 uncommon sells to Abuela. Selling MAL-07 to Chato above 17.5 fills a ladder slot and should score positive.
- **Duels II on delivery day.** No duel has scored yet. Aleks's duelist should ask for `days` first, concede days where our weight is low, and close early because decay is 0.08 per round.
- **`/api/me/value?card=` for the page bonus.** No log entry has priced it yet. This one read settles whether LAV-09 is worth chasing.

## Plan, anchored to the schedule
1. **Now, ticks 115–118 (operator).**
   - Read `/api/me`: copy counts and LAV page status.
   - Cancel the LAV-04 ask if it is a first copy.
   - Run `/api/me/value?card=LAV-09`.
   - Impact: stops a −4 sale and decides the LAV-09 question.
2. **Hour 2.0, ~22:20 (Aleks).** Run the practice duels with `agents/duelist/`. Log the protocol, how decay behaves, and how alias rivals open.
   - Impact: 0 points tonight, readiness for Duels I.
3. **22:15–22:55 (dealer bot, operator).** Run `abuela_bot.py --dealer chato --ladder --deals 3`, restricted to:
   - selling MAL-07, any price above 17.5, pushed high;
   - buying LAV-06 and LAV-07 at ≤29, only if we don't already hold them.
   - Buy LAV-09 at ≤77 only if step 1 shows the page bonus is priced.
   - Impact: fills level-2 ladder slots ahead of the field. The exact point value is not in the data.
4. **22:20–23:00 (Lucas, Dani, in the room).**
   - t17 bids 78 for MAL-09 (#9). If we hold a MAL-09 (worth 49), list it `to` t17 at 78: +29.
   - t04 bids 85 for LAV-10. Sell only a spare copy (worth 22.75): +62. Keep a first copy (worth 91).
   - Skip t18's LAT-09/LAT-10 bids at 55. Team 18 is in the top 4.
5. **Overnight (operator).**
   - Write `agents/broker/`: max-surplus matching, with a patience rule that matches early when a trader's ticks run out (for the hard test at hour 16).
   - Replay it on a synthetic book against greedy `auto`.
   - Keep cash ≥270 for the bond (250 + 20); we have 342 now.
6. **Sat 09:00 (operator).**
   - Check `/api/clock` and `/api/schedule`: when does hour 3.0 fall?
   - If the broker beat `auto` in replay, open the board venue (fee 0) before the bench.
   - Otherwise keep the free stall for 3.0 and switch by 5.0.
   - Impact: up to the full Market-making share against a field at the half-share stall.
7. **Hour 4.05.** The 150 P grant and the RET pack arrive. Gifts don't count. Keep RET first copies, which are worth 1.1×.
8. **Hours 6.5 and 13.0 (Aleks).**
   - Duels I: always close inside our limit, and early.
   - Duels II: trade on `days`.
9. **Hour 16.0 (broker).** The hard Market Test: switch on the impatience mode.
10. **Hour 18.0, Sunday (Lucas, Dani, trader).**
    - Bid for CHA cards from non-leaders below 40 (uncommons) and 112 (rares).
    - Sell our remaining LAT/MAL to CHA-indifferent collectors.

## Hypotheses to test
- **Dealer buys score asymmetrically**: only above-value buys subtract, below-value ones score about 0.
  - Experiment: buy one Abuela common below our value with nothing else pending, and read `neg_points` before and after.
  - Decides: whether Chato's LAV buys are neutral.
- **Selling to a dealer scores price − value.**
  - Experiment: sell one spare (worth 25%) to Abuela, with nothing else pending.
  - Decides: the `neg_points` delta.
- **The page bonus is priced into our value.**
  - Experiment: `/api/me/value?card=<last missing LAV card>`.
  - Decides: whether it shows more than book × 1.3.
- **Round 1 (Friday) runs until game hour 4.0, so the 3.0 bench counts toward Friday.**
  - Experiment: `/api/clock` at 23:00 and at Sat 09:00.
  - Decides: which round is active during the bench.
- **The board broker beats `auto`.**
  - Experiment: replay the first `bench_offers` through both.
  - Decides: realised share of the possible gains.
- **A fee-0 venue pulls trades away from El Rastro.**
  - Experiment: open it and watch the first 2 hours.
  - Decides: value traded on our venue vs on El Rastro.
