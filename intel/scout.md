# Scout (claude-sonnet-5-5, Sat 18:41)

## Top 3 actions now
1. **Open the silver pack (asset 1013) only after Chief OK, then run the Workshop.** The SAL page is closed (SAL 10/10, settlement tick 988, neg_points 78.7 → 119.1). The 18:20 hold ("until SAL-06 settles, then ask the Chief") has lapsed. Evidence: the pack is valued 76.5 in the holdings table, and the unopened-pack drag cost us 2.4 on SAL-06. A pull adds a duplicate card at 25% value, so the pack's value is realised without a trade. Workshop spares: LAV-02 ×3 and LAV-03/04 ×2 each are worth 1.3-3.2 each; LAT-03 and LAT-04 stand at 5 each. Executor: Operator via `POST /api/taller` with three same-rarity spares. Effect: collection value rises, with no neg_points or ladder change [V Sat 16:15, +11.8 value]. Confidence: med, since the Chief must confirm and the pack gain is not in the data.
2. **Keep the v10 ads and the two low-priced maker offers live to the non-rival buyers.** Offers 15180 and 15181 are MAL-02/05 → t15 at 9, and 15055 and 15196 go to t09 at 9 and 6. Evidence: our market gap was the decisive lever (mm 7.5 vs 9.15-12.5). Value created on our venue is net and can go negative, so only send a card to a buyer who values it more than we do. Team 15 and Team 9 are listed as buyers (t15 collects RET/LAT/MAL, t09 RET/SAL). Their board ranks are #12 and #17, so they are not rivals and the feeding rule is fine. Executor: Operator and the ad job; Dani asks t09 and t15 to accept in the room. Effect: this lifts mm_points only, not neg_points. Confidence: low-med.
3. **Do not chase any more ladder or flag points, and do not sell reserved cards.** Evidence: negotiating stayed flat at 21.88 while the ladder went 0.373 → 0.437, and flag 8 scored 0. Selling any SAL card now books the page bonus as a loss (t01 −4.27). Executor: Operator, by keeping the reserved list as it is. Effect: protects the +40.4. Confidence: high.

## What the climbing teams are doing
- **Team 18** (+0.9 in 15 min, now #5, collects RET) is buying RET commons and rares. t18 → t07 LAT-01 at 8 (tick 904) is the sort of cheap flow that adds up.
- **Team 6** (#2, 31.7, 0.3 behind us) sold RET-09 at 84 to t12 (tick 895) and RET-03 at 6 to t12 (tick 905). It cashes in the rares dealers sell and trades heavily (52 deals, 593 listings).
- **Team 16** (+0.5, 26.5) has just unlocked L5 and posts RET bids at 13 and 5. It is vacuuming up RET uncommons and commons and could compete with us for RET cards.
- **Team 12** (53 deals, −2.9 in 60 min) trades heavily without gaining. Volume alone doesn't pay.

## Threats
- **Team 6 and Team 14** are 0.3 and 0.5 behind us (31.7, 31.5), so any v10 or team trade that helps them hurts us. Never send them value.
- **Team 10** has a live bid on RET-09 at 30 (offer 15314) and sits at #6 (28.4) and allied with t01. Stay clear of it.
- **Team 3** is #4 (29.6) with the highest negotiating score, and Team 13's v20-v24 venues give its owner market-making points whenever others trade there. No offer of ours goes on a rival venue.
