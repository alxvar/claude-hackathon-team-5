# Judge (claude-opus-5-5, Sat 21:12)

## Verdict
Holding #3 but slipping: 31.3, −0.4 over 15 min and −0.6 over 60 min. The gap to t06 (32.6, +0.1 over 60 min) widened by 0.7 in an hour, and the gap to t10 (33.6) held at 2.3. `neg_points` has been flat at 119.1 since tick 988, so 235 ticks without a scored gain.

## Our strategies: keep / kill / scale
- **Dealer bot: hold.** Its last runs scored 0. Pícaros LAV-04 walked at their final 4, which equalled their opening. Neg stayed 119.1, and the ladder was capped [L].
- **RET-11 buy from the Pícaros at 128: done, never repeat.** Neg 0 (clipped), ladder +0.483 (+0.046), and it cost 128 of the CHA reserve (cash 392). Its board effect is not in the data: the score fell 31.6 → 31.3 afterwards.
- **RET-11 → Pilar job (floor 198): keep, but expect no fill.** Pilar's epic sell median is 179 (n=1), and she paid 140 for LAV-11. A sale at ≥ 198 scores 0, so keeping the card is fine.
- **Trading loop: keep and restart after Duels II.** Last fills: 15:48 (+6.2) and 17:46 (+15.5); none since. Last night's errors were stale (rate limit and DNS).
- **Our maker asks (3): mixed.**
  - LAV-04 → t01 at 6 and LAV-03 → t04 at 6 are true spares worth 3.2 each, about +2.8 each. Both are unfilled since ≤ 20:12.
  - **MAL-03 → t09 at 9 (17696): kill.** MAL-03 is our only copy (value 7). Selling it breaks the Sunday MAL page that Lucas decided, and t09 doesn't collect MAL.
- **v10 swap desk and rebate: scale, but with no evidence yet.** No v10 fill tonight is in the data. Our venue's VC is net and verified to go negative: t15's SAL-07 at tick 398 took mm 4.99 → −5.2.
- **DENY buys: keep the rule.** None used, nothing to judge.

## Check the scout
- **Holds:**
  - t10's 205 bid for LAV-11 (17778) and the Pilar epic median of 179.
  - Dealer sale at ≥ 198 = 0 neg.
  - t13↔t14 swap at 0 P (tick 1202).
  - t02 up 1.6 over 60 min, with MAL-10 at 30.
  - t07's RET buys at 66 and 77; t12's LAT-09 at 55.
  - t09 bids 56 for MAL-09/10.
  - v07 is t10's venue.
- **Wrong or loose:**
  - "Our MAL cards are 07 and 08 only held partially" is false. We hold MAL-01 to 05 and MAL-08, and miss 06, 07, 09 and 10.
  - "Buy the MAL closer from t15" is loose. The page needs 4 cards, not one closer. The only MAL ask live now is MAL-06 at 28, which is −10.5 against our value of 17.5.
  - "Team 15 lists MAL-07" is not in the asks shown; only the directive mentions it.
  - Our own duplicates do not feed the 22.5 real-trades lever. Only VC between other teams on v10 counts, so our LAV spares are irrelevant to the swap desk.
  - "t06 1.0 ahead" is now 1.3.

## The 3 changes with the highest expected gain
1. **Confirm the duelist is live before Duels II.** Now tick 1223; start ≈ tick 1239.
   - How: Lucas checks Aleks's agent in the room. The organisers said "make sure your agent is running".
   - Effect: protects a 68-duel session; session 2 closed 9 of the last 10 duels. Duel score is 13.93; a down agent scores 0.
   - Risk: none.
2. **v10 tonight: rebate and swap pairs only for positive value created.**
   - How: at the 22:45 settlement, pay the 5 P/card rebate (cap 30) only for v10 trades where the card went to a higher-multiplier holder. Lucas/Dani broker pairs from `intel/matches.md` only between non-top-3 teams (never t10/t06/t03).
   - Effect: +0.8 to 1.6 final [L, Analyst], at ≤ 30 P.
   - Risk: a dump to a low-multiplier team turns our VC negative (−5.2 precedent), or we broker a rival's page close.
3. **Cancel 17696 (MAL-03) now and relist our true spares.**
   - How: cancel via `trade.py` before it can fill (it expires at tick 1237). Then post our 2 spare LAV-02 copies (1.3 each) as maker asks at 6, addressed to t01 and t17 (LAV collectors, ≥ 10 below us). Reprice per §4A after 10 min unfilled.
   - Effect: keeps the MAL page buildable; +4.7 neg per spare sold.
   - Risk: small. LAV-03/04 at 6 have gone unfilled for about an hour, so these may not fill either.
