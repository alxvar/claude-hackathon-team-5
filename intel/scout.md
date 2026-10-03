# Scout (claude-sonnet-5-5, Sat 19:08)

## Top 3 actions now
1. **Keep the DENY buy armed (Operator, `deny.py`); do not self-trigger.**
   - Evidence: t10 is +3.3 / +4.1 (15 / 60 min) and bought RET-03 from t06 at 12 (tick 1033). t14 and t10 both "collect LAV/RET". Board is 31.7 / 31.7 / 31.7 / 31.4 for us, t06, t10, t14.
   - Action: buy only on a Chief "DENY <card> <offer id>" line: team seller, ≤35 P incl. fee, cash ≥85 (we hold 120), never a rival venue.
   - Effect: removes a rival's ≈ +2.4 board page close for ≈ −1 board. Which card each rival lacks is not in the data. Confidence: low-med.
2. **Re-post the expiring spare sells to non-rival buyers (Operator, `trade.py`, as maker with 2× ticks).**
   - Offers 15571 and 15572 (MAL-02 and MAL-05 at 9 to t15) expire at tick 1071; 15599 (LAV-03 at 6 to t09) at 1073; 15932 (LAV-02 at 0 to t01) at 1072.
   - Buyers are not top-4: t09 is #17 (19.3), t15 #11 (24.5), t01 #12 (24.1).
   - Evidence: the clearing price for commons is 9 (LAT 7.5). t09 and t15 still collect MAL/RET/SAL.
   - Effect: small `neg_points` (our spare copies are worth 1.3–7 each). The aim is the "value created on our venue" lever, only if Market confirms the venue and that the buyer holds the 2nd copy, so value created stays positive. Confidence: low.
3. **Aleks decides the Duels II `--days-read` setting before the 19:30 freeze.**
   - Evidence: the Duel Lab says the day reading is the biggest swing left (right 0.47, backwards −0.18 per duel). Our duel score is 13.93, and the recent Session-2 duels (2522–2585) are mostly deals.
   - Effect: protects the duel part of the score; the size is not in the data. Confidence: med.

## What the climbing teams are doing
- **t10** (+3.3 / +4.1) is the only fast climber, and the cause is not in the data. Visible: 12 team trades (RET-03 from t06 at 12, tick 1033) and a level-5 unlock at tick 971 ("5 deals with pilar").
- **t16** (+0.7 / +1.6) is concentrating RET: it bought RET-08 (13), RET-05 (5) and RET-07 (13) from t15 at ticks 1022–23. It still bids RET-06 at 13 and RET-01/02/03 at 4.
- **t18** (+0.6 / +1.6) and **t12** (+1.4 / +0.8) are climbing. t12 bought RET-09 from t06 at 84 (tick 895) and has 56 deals, but the cause is not in the data.
- **t07** is accumulating RET: RET-08 from t09 at 24 (tick 1057), and a bid on RET-09 at 31.

## Threats
- **Three teams are tied with us at 31.7** (t06, t10, t14 at 31.4). A single +1 board event changes first place. t10 moved +3.3 in 15 min while we moved −0.3.
- **Top-4 teams are trading with each other.** The t06→t10 RET-03 trade at 12 passed through a leader's hands. If it ran on a rival venue, it feeds that owner's market.
- **Ladder is flat for the board.** All three 19:05 ladder sells walked (ladder 0.437, `negotiating` flat per the 17:45 note). Our remaining levers are denial buys, v10 value created, Duels II, and the CHA release on Sunday (our unopened silver pack stays kept for it).
