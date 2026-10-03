# Scout (claude-sonnet-5-5, Sun 00:34)

## Top 3 actions now
1. **Cancel SAL-11 bid 20252 (115 → t04) at the first tick Sunday** (Operator, trade.py cancel). Lucas's 00:50 GUARDRAIL: ≈ +0.2 pts per 115 P vs MAL ≈ 0.7 per 100 P. Cash is 392 and the CHA reserve comes first. Effect: frees 115 P for CHA. Confidence: high.
2. **CHA page from the Pícaros, then MAL close** (Operator, abuela_bot `--dealer`). Settled targets: Pícaros CHA rare 48-52, accept ≤ 54; after one walk-and-reopen accept ≤ 57; 62 only for the LAST missing card. Run the trick guard on every offer. Team bids come first, and the last card is bought from a team (the page-closing +50 cap applies only to team trades). Our CHA value is 1.6×, so rares are worth 112 against dealer prices of about 50, which means no dealer loss. Effect: it feeds the page bonus (106 at CHA) via a team trade. Lucas's estimate is +3.2-5.6 final [L]. Confidence: med.
3. **Offer MAL-09/MAL-10 holders a deal, and close the MAL page via a team trade** (Operator, with Dani in the room). t09 bids 56 each for MAL-09 and MAL-10 (offers 19719, 20251), and t09 is #16 at 23.3, so it is not a rival. Our MAL bids must stay at or below our own value; MAL-08 is never sold. The page bonus scores only through a team trade, and Sunday is a fresh round, so +50 can count in full. Don't outbid t09 above value. Confidence: low-med.

## What the climbing teams are doing
- **Team 18 (#2, +1.2 in 60 min)** collects RET/LAT. It bought LAT-10 from t13 at 72 (tick 1332), with the team-trade buyer list showing LAT×2 and RET×1. Slow steady gains from team trades, with little dealer activity (23 dealer trades).
- **Team 12 (#4, 70 deals)** buys heavily on LAT (×8) and made the RET-11 epic buy from t06 at 216 (tick 1245). It is also the buyer on LAT-10 (86) and LAV-08 (14, from t08). It takes cheap cards from teams that are dumping them.
- **Team 10 (#1, 37.6)** holds a v10-style position and sells SAL-11 (207 to t17) and MAL-11 (195 bought from t08). It sits at the top, and its dumps run to cheap RET-03 (8).

## Threats
- **Team 10 and Team 18 are far ahead** (37.6 / 31.3 against our 30.5). Do not sell RET or LAT page-closers to them.
- **Team 12 (#4, 30.4)** is level with us and collects RET/MAL/LAT, so it competes for MAL and RET cards. Its MAL buying could outbid our MAL close.
- **Team 9 bids 56 for both MAL rares** (it is a MAL collector, #16). The same card is worth more to a closer, so a price war would push us above our MAL value of 17.5 for uncommons and rares, which would cost neg_points.
