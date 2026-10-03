# Scout (claude-sonnet-5-5, Sat 13:10)

## Top 3 actions now
1. **Open Abuela thread 8762 (bid 18 for SAL-06) and step up slowly; stop chasing Chato.** Evidence: Chato's 33 → 32 held against our silent 26 (13:08 log, nothing spent). Abuela is at 29 → 27 against our 18, and every Abuela deal under her list has moved the ladder ("Ladder and early unlock count only below-list dealer deals" [L]). Executor: `abuela_bot.py --dealer abuela --ladder`, Operator. Effect: a level-1 slot, small ladder gain. Not worth more than ~22 per card. Confidence: med-low. Note SAL is worth only 0.9× to us, so any price above ~25 is a neg loss.
2. **Sell Pilar uncommons offer-only at ≥ our value (0 neg cost), small steps.** Evidence: MAL-06 at 19 with small steps → ladder +0.040 (0.141 → 0.181); the jump to 23 on SAL-08 gave only +0.019. We hold no MAL or SAL uncommons now (MAL-06/07 and SAL-08 are sold). Not in the data: which spare uncommons we could still sell. Executor: Operator, only after a spare uncommon exists. Confidence: low. It would give ladder gains only if the cap hasn't been reached; the cap is unknown (Analyst guesses ~0.15 [L], but 0.181 has already passed it).
3. **Sell the spare commons to non-top-4 teams as maker (already live).** Evidence: t14 (#1) is dumping RET commons at 9 (ticks 591-598), so RET is a liquid market. Our 10 offers are all addressed at 4-11 P. Targets from the page-gap desk: Team 7 (#17, 12.9 below us) for LAT-04, LAV-02/03/04 (est. 9.5 each), and Team 9 for SAL-02 (est. 8). Our own asks are 4-6, so reprice to 8-9 for Team 7. Executor: `trade.py`, Operator. Effect: +4 to +6 each, but small. Confidence: med.

## What the climbing teams are doing
- **Team 14 (#1, 31.2, −2.6/15 min, +2.2/60 min) is selling RET commons at 9 to t09, t04 and t15** (ticks 591-598, 5 trades) and collects LAV/RET/LAT. Its score fell 2.6 in 15 min even so, so we are not chasing it. RET commons clear at 9, matching our own prices.
- **Team 6 (+5.2/60 min) and Team 10 (+4.2/60 min) are holding rare buys at 70-84.** RET-09 t06→t02 at 84 (tick 504); MAL-10 t03→t10 at 74 (tick 585). Teams are paying list-ish prices for rares, so our RET-09/10 (149.9 each) are priced far above the market and nothing is for sale.
- **Team 18 (#2, +3.2/60 min) has 29 deals, 16 of them with dealers.** Team 8 sold LAV-11 to Pilar at 140 (tick 550), so dealers pay well above team bids for epics.

## Threats
- **Team 14 is #1 and 2.3 points above us** (31.2 vs 28.9). Don't sell it LAV/RET/LAT page cards. We feed t14 nothing now: our open offers go to t06, t09, t03, t15, t07 and t16 (none top-4).
- **t04 bids 26-27 for RET-06/08 and 64 for LAT-09.** RET-06/08 are worth 100.4 to us as part of our own page: don't sell them.
- **Our L3 and L2 ladder look capped:** 0.181, and Chato refuses list-26 buys. The gap to Team 14 is not closable by dealers alone.
