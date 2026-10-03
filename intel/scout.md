# Scout (claude-sonnet-5-5, Sat 16:30)

## Top 3 actions now

1. **Sell LAV-02 / LAV-04 spares to Team 7 (#17, 10.6 below us) as maker.**
   - Action: the Operator or `trade.py` posts an ask addressed to t07 at ~9-10 P. Run `policy.py can-give` first. It currently says LAV-02 YES, LAV-04 NO, so only LAV-02 goes.
   - Evidence: the 4.3 gain per card is a Dani estimate ("9.5 est."), not an open bid. Our spares are worth 3.2 each.
   - Effect: about +4 neg_points per card, and no fee as maker. That is ≈ +0.4 board at 0.094 per neg_point.
   - Confidence: low-med. t07 shows no live bid, and our ask 10716 (LAV-03 at 6 to t09) is still open.

2. **Fill Team 16's and Team 15's live bids with our spares.**
   - Evidence: t16 bids RET-01 at 5 (offer 11385), RET-07 at 14 (11355) and LAV-06 at 12 (11362). Our own asks to t16 and t15 are already posted: 10885 SAL-01 at 11, 11379 SAL-02 at 11, 10959 MAL-02 at 9 and 11046 MAL-05 at 9.
   - Action: the Operator keeps those asks alive. Do not sell the RET or LAV page cards: RET-01 is our complete-page card, so `can-give` refuses it.
   - Effect: small positive neg_points. Past fills of this kind gave +2.0 (MAL-01 at 5) and +4.7 (SAL-01 at 7).
   - Confidence: med. t16 and t15 are on the safe list.

3. **Pilar ladder sells in the Salamanca fever (18:03-20:03).**
   - Action: sell SAL-04 or SAL-08, held for this window, to Pilar at ≥ our value (SAL-08 is worth 22.5). Use small −2/−3 steps, then offer-only. Operator, `abuela_bot.py --dealer pilar`.
   - Evidence: Pilar paid SAL-06 25 at tick 669 for +6.2 neg, and +0.040 ladder for MAL-06 with small steps. Ladder is at 0.2 and the L3 slot pays about 3× L2. Pilar's median uncommon is 18 over 6 deals.
   - Effect: neg is not hurt when the price is ≥ value. Ladder +0.01 to +0.04.
   - Confidence: med. The ladder may be saturating (Analyst's cap near ~0.15 is [L], yet 0.2 is already reached).

## What the climbing teams are doing

- **Team 1 (+3.3 in 15 min) and Team 16 (+4.5):** Team 16 is the one that moved most. Team 16 took LAT-09 (rare) from Team 3 for 88 P at tick 724 (Team 3 is the buyer, +2.9). Team 16 is also bidding on rares and uncommons, so the gains are not in the data beyond that. Team 1's source of gain is not in the data.
- **Team 3 (+2.9/+5.6):** its buys are LAT×2, SAL×1. Its rare purchase at 88 sits above the usual rare price of 70, so it likely gains from LAT-09's page value.
- **Team 12 (#1, 43 deals):** its edge is volume plus dealer trades (26). It is not a safe counterparty.

## Threats

- **t03 bids 69 for LAV-10 (offer 11295).** We hold LAV-10 (worth 177.1, page piece). Never sell it. t03 is #8, but the card would close nothing for us.
- **Board compression.** #1-#6 sit within 1.5 points, and t16 and t1 are climbing fast. Their rises could push us down.
- **Rare 25 P bid by t04 on RET-10 (11366)** is far below our value of 149.9. Ignore it.
