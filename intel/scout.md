# Scout (claude-sonnet-5-5, Sun 11:45)

## Top 3 actions now

1. **Keep v10_reward.py running (bounty 20 P × first 5 v10 trades, max 2 per seller, El Rastro only). Operator checks its first payout.**
   - Evidence: the ad went up at 11:42. t13 has 102 deals and 1192 listings and could bring volume.
   - Effect: points come from v10's first positive trade. Our `neg_points` is already 50.0 (the CHA +50 cap), so ≥ 0 buys cost nothing.
   - Limit: every payout bid must stay ≤ our value + 20.
   - Risk: the Chief flagged the fair-play review risk.
   - Confidence: med.

2. **Sell spare LAT/MAL cards through Dani to the buyers that pass the feeding rule. Only do it if the buyer is ≥ 10 below us.**
   - Evidence: t09 bids CHA-01..03 at 5 and CHA-06..08 at 15. We hold complete CHA, so those bids are not for us to fill. The profile table shows no buyer passes the feeding rule above our value + 3.
   - Effect: converts cash only (cash never scores). The cheap spares are worth 5-7 to us: MAL-01..05 at 7 each, LAT-03 at 5.
   - Asks seen: MAL-01..05 at 10 and LAT-01..05 at 8-9 are others' asks (not ours).
   - Confidence: low.

3. **Place one more LAT-first-copy bid at ≤ value on El Rastro, addressed to a non-rival (not t10, t12, t18, t03). Use trader.py.**
   - Evidence: our bids 24252-54 (LAT-06/07/08 at 9) expire at tick 2152.
   - Effect: a LAT first copy is worth 5 × 1 for the page, so a ≥ 0 buy gives no neg_points. It only raises the reference for the MAL/LAT collection.
   - Confidence: low. Do not chase it over a dealer.

## What the climbing teams are doing
- **t04** (+6.4 in 60 min, 89 deals) is the biggest mover. Its buys: RET×6, MAL×6, LAV×4, LAT×3. It sold SAL-11 (epic) to t02 for 220 P at tick 1858.
- **t09** (+5.5 in 60 min) buys RET×6, SAL×5, MAL×4. It also holds open bids on CHA commons and uncommons (5-15 P), a low-price volume strategy.
- **t15** (+5.5 in 60 min) buys LAT×6, MAL×4, RET×3. It sold CHA-10 (rare) to t16 for 65 P at tick 2022. It is a non-rival counterparty for addressed bids.
- **t06** has 86 deals (+2.4 in 60 min) and 1012 listings, a pure maker-volume play.

## Threats
- **t12 (34.7) and t10 (34.1) are ahead of us (32.8).** t18 (33.0) is also ahead. Never hand any of them a closer or a card for a gap. Standing rule: no LAT-08, MAL-03 or MAL-08 to t12.
- **t04 is closing on us.** It is 28.9 against our 32.8, 3.9 behind, with a 60-min rise of +6.4 versus our +0.6.
- **Our `neg_points` is flat at 50.0.** Further team-trade gains are capped, and MAL is NO-GO after the Pícaros walk (their 58 vs our 44). Remaining points are in duels (22.23) and v10.
