# Scout (claude-sonnet-5-5, Sat 09:41)

## Top 3 actions now
1. **Sell page-completer spares to teams below us, as makers.** Our offers 3056/3057/3058 (LAV-04→t07, LAV-02→t09, LAV-03→t16, all at 10) are already live. Add the SAL-02 (worth 2.2) copy at 9, addressed to t03 (#10, 11.7). Evidence: the best-buyer table says SAL-02 → Team 3 at an estimated 9, gain +4.8, with Team 16 at 9 and Team 6 at 8 also in the market. Our offers 3066/3067 put SAL-01 and SAL-02 both to t07, which only collects LAV/LAT, so the better home for SAL-02 is t03 or t16. Executor: operator, via trade.py list. Effect: about +4 to +5 neg_points per copy, 0 fee as maker. Confidence: med.
2. **Rares for the RET page: ask teams first, and don't buy from Chato above 90.** t15 bids 59 for RET-10 (offer 2991). t02 bids 12 for RET-10 and 10 for RET-09, so t02 does not value them. Chato's rare median is 90 (7 deals), against our RET rare value of 77. Operator: post addressed bids at ≤70 for RET-09 and RET-10 and watch the feed for holders. Dani asks the room who holds them. Effect: each rare costs −5 to −13 if bought from Chato, versus a gain of up to 7 at ≤70. Confidence: low-med. The holders are not in the data. Competition: t15 is bidding 59 for RET-10, and t15 is #12 (10.3), a team that can't use the page-completing trick on us. We should not outbid it past 74.
3. **Keep the Abuela ladder bot on RET-04 (offer 3126, bid 7, Abuela opened 12).** Cap 9 is fine. Abuela commons end at 9-10 after 5-7 rounds, and our RET common value is 11. Evidence: the Abuela deals moved our ladder 0.054 → 0.064. Ladder is 0.0 after the reset, so these are the cheap points. Add a second negotiated Abuela deal (uncommon at ≤24) for the ladder. Executor: abuela_bot with `--cash-floor`. Confidence: med.

## What the climbing teams are doing
- **t01 (#15, 8.4) is buying everywhere:** SAL-10 at 72 from t02 (tick 163), SAL-05 at 9, SAL-02 at 9, MAL-04 at 8, MAL-02 at 3 from t06, LAT-08 at 25 from t01→t14. It is a volume buyer at about the clearing prices. This is why MAL-06/07 → t01 at 26 (offers 3054/3055) are good sells.
- **t15 (+5.4, #12) buys LAT ×6 and MAL ×2, and bids for RET.** It paid 60 for LAT-10 (tick 142), and its bids are 59 for RET-10 and 21 for RET-07. It is a buyer to sell to and a rival on RET rares.
- **t06 (+0.4, #11) lists 112 offers and sold LAV-05 to us at 8.** t06's cards are available (LAT-01 at 5, MAL-02 at 3, LAT-10 at 60), so sweeping cheap RET listings from it is plausible.

## Threats
- **Leaders feeding:** t13 (#1, 26.5) bids 2 on RET commons and 15 for LAV-07. Never sell to it. Its venue v03 is lobbying for team trades.
- **t12 (#2, 23.2) collects LAV.** None of our LAV spares may go to it or t10, t14, t04 (all LAV buyers near us). Offers 3056-3058 go to t07, t09 and t16, which are fine.
- **Cash:** 402 P against a 370 floor leaves only about 32 P free. The ~280 P RET page and the 270 P venue bond don't both fit, which blocks all buys until the floor drops to 100.
