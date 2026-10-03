# Scout (claude-sonnet-5-5, Sat 11:20)

## Top 3 actions now

1. **Hold the line until Duels I (11:50), then stop the accepts.** Operator action: leave loop.py and the dealer threads as the 11:17 guardrail says, and post no new asks that need our accept. Evidence: #2 at 28.1, with #1 at 28.6 and #3 at 27.9, so the gap is 0.5. Duels are 0.0 and a missed duel deal scores 0. Effect: protects the duel score, with no neg_points change. Confidence: high.

2. **Sell LAT-08 at 25 (offer 5425, t03) and SAL-08 at 25 (offer 5351, t03), and take counters at ≥ 20.** Operator, already live. Evidence: t03 is #11 and is 11.4 points below us. Teams.md says t03 collects LAT/SAL/LAV, and its SAL-01 buy at 7 scored us +4.7. At t380 Team 2 → Team 9 sold SAL-08 at 20, so the clearing price is ~20. LAT-08 is worth 12.5 to us, which gives ≈ +7.5 at 20 and +12.5 at 25. SAL-08 is worth 22.5, so only ≈ −2.5 at 20 and +2.5 at 25. Keep SAL-08 at 25 or higher. Effect: about +10 to +15 neg_points in total if both fill at 25; the value of an extra SAL-08 sale is small. Confidence: med.

3. **Answer Team 9's open bids with addressed asks.** Operator, via trade.py. Evidence: Team 9 (#16, 12.2, a buyer of LAV) bids 8 for RET-02 and RET-03, 22 for RET-06 and RET-07, and 8 for SAL-05. Team 9 is 16 points below us and is no threat. We hold 5 RET commons, all worth 83.9, but they are page cards, so selling one breaks our page and **we do not sell any of them**. Offer only spares: SAL-05 (our copy is the first, worth 9) at 9 to t09 is the only fit. Offer 5788 already asks 30 for it, and Team 9's bid is 8. Re-address SAL-05 at 9–10, which is ≈ +0 to +1, mainly to create value on v07 for Team 10. Confidence: low.

## What the climbing teams are doing
- **Team 10 (+3.5 / +7.5)** completed pages through team trades. Our RET-01 buy from t10 (+50) is one example, and it now trades on v10. Its market score rose 7.3 → 12.5 after t10 → t01 MAL-07 at 14.
- **Team 1 (+7.5 / 60 min)** is buying rares from teams. At t376 it paid 76 for SAL-10 (Team 1 → Team 6, shown in the log as t01→t06) while collecting SAL.
- **Team 4 (+4.0 / 60 min)** is selling spares to #1 and #2: MAL-06 to t01 at 20, RET-05 to t02 at 8. It is a seller and a buyer in both sets at once.
- **Team 13 (#1)** buys MAL×6 and SAL×2 and is selling RET-08 to t14 at 20. It has 45 deals, the most of any team.

## Threats
- **Feeding Team 13 and Team 18.** Do not sell MAL or SAL spares publicly. t13 collects MAL/SAL, and t18 collects RET/LAT. Keep asks addressed to teams outside the top 4.
- **Team 9 is bidding 52 for RET-09 and RET-10** (offers 5781 and 5782). That is well below the 77 list, so it is no direct risk. It does show that team rare prices for RET are ~52 and falling. Do not pay Chato above 77 for a rare.
- **Team 2 is the #5 at 25.2 and flat.** It bids for SAL-09 at 58 and LAV-02/LAV-04, which our spares can supply. They are top-4 teams in the team ranking, so we do not feed them.
