# Judge (claude-opus-5-5, Sat 23:53)

## Verdict
**Holding #3, but drifting down.** We score 30.49: −0.4 over 60 min, 7.1 behind Team 10 (37.6) and 0.8 behind Team 18 (31.3, +1.2/60 min). Team 12 sits 0.1 behind us at 30.4. Our `neg_points` has been flat at 119.1 since tick 988, about 457 ticks with no scored deal. Market has stayed at 7.5 (the stall) all of Saturday, while the top market is 12.5.

## Our strategies: keep / kill / scale
- **Team trades (page closes, swaps): SCALE.** These were Saturday's best scores:
  - SAL-06 from t08 at 28: +40.4
  - Swap with t07: +15.5
  - Swap with t08: +6.2
  - Board impact measured at ≈ +0.05 per `neg_point`.
- **Trading loop: KEEP, restart on HEAD.**
  - It has had no accept since 17:46.
  - From 22:41 it logged 5 × `unknown_card sobre_bienvenida`; the fix is commit 918f823, picked up only at restart.
  - The network errors ran from 22:55 to 23:24.
- **Dealer bot: KEEP, but only for at-or-below-value buys.**
  - Its last thread (Pícaros LAV-04) walked at her final of 4. Our neg and ladder did not change.
  - Ladder went 0.373 → 0.437 with `negotiating` flat [L], so do not chase the ladder.
- **Egg probes (dealer threads at ticks 1367-1370, closed at the dealer's first price): KILL.**
  - The Castizo egg already paid MAL-06 + a badge; the score effect of badges is not in the data.
- **SAL-11 bid (20252, 115 → t04): KEEP, but verify.**
  - It is unfilled through 19620 and its re-post.
  - A SAL-11 ask at 245 stands on El Rastro, and its maker is masked. If that maker is t04, 115 will not fill.
- **Book asks LAV-03 → t04 at 6 and LAV-04 → t01 at 6: KILL unless they are not page closers.**
  - Our gain is about +2.8 each.
  - Neither buyer is ≥ 10 below us (t04 25.1, t01 25.6), and Dani's table finds no buyer that passes the feeding rule.
  - Both expire at tick 1455 anyway.
- **v10 venue / club: SCALE.** Market stayed at 7.5 through six benches. The 22.5 real-trades part is untouched and is the largest open lever.
- **Flags: DONE.** We got 3 scored (net +20); the 8th flag scored 0 at 17:43.
- **Duels (Aleks): KEEP.** Duel points are 35.39; 2 of the last 10 duels in session 3 ended with no deal.

## Check the scout
| Claim | Verdict |
|---|---|
| Team 12 sits 0.1 behind us | Holds (30.4 vs 30.5). |
| t18 bought LAT-10 at 72; t12 paid 86 | Holds. |
| t06 sold RET-10 at 84 and RET-11 at 216, −2.7/60 min | Holds. |
| Team 10 is "selling epics" | **Wrong.** t08→t10 means Team 10 *bought* MAL-11 at 195; it sold only SAL-11 at 207. |
| "A non-member sale on v10 hands the venue owner value" | **Wrong.** v10 is **our** venue: value created there scores for us (+4.99 at tick 311). |
| The directive lists t10 among the club's non-rivals | **Wrong.** The 22:55 candidates are t15, t04, t07, t08, t09, t02; the 21:30 directive names t10 as a team never to help. |
| RET-09 match is "t08→t09" yet "68 VC from RET-09 t07→t09" | **Contradicts itself**, and Market (23:35) says t07 while Lucas (21:40) says t08. t07 bought RET 9 times (a collector), so t08 (which dumps RET) is the likelier seller. Confirm before brokering. |
| Pícaros rare median 55 | Holds, but n=1. The ≤ 54 accept rests on two buys at tick 904. |
| LAV-03/04 asks at 6 are "fine" | Unchecked against the feeding rule (see above). |

## The 3 changes with the highest expected gain
1. **CHA page at the open, in order.**
   - Order: rares from the Pícaros at ≤ 54 (value 112, so neg = 0), then uncommons and commons at ≤ value, then the cheapest common last from a team, as maker.
   - Before buying, open `sobre_plata` (71.6) right after CHA is released. Pack drag cut the SAL close from +50 to +40.4.
   - Expected gain: +3.2-5.6 final [L, Analyst].
   - Risk: Pícaros bait-and-switch. Check the card id in the structured offer before every accept. Also watch cash: 392 + 150 = 542 against ≈ 330 for CHA.
2. **v10 club deals, Lucas and Dani in the room from 09:00.**
   - First: settle whether RET-09 comes from t07 or t08, then broker the trade to t09 on v10, addressed.
   - Only route trades where the buyer's value exceeds the seller's. A sale to a lower-multiplier holder cost us −10.2 at tick 398. Never put a top-5 team on either side.
   - Expected gain: +3.9-4.8 of the 5 real-trades points [L, Market sim].
   - Risk: one bad route wipes the venue's gain, as at tick 398.
3. **SAL-11: identify the maker of the 245 ask before 09:00** (from the feed's `offer.listed`).
   - If the maker is t04, counter once at the 125 cap at the open. If no fill within 10 min, cancel and free the cash for CHA.
   - Expected gain: +37-47 neg, ≈ +2.3 board (directive's figure).
   - Risk: a public bid lets rivals see the target. Floor 260 still holds after this buy (542 − 125 = 417).
- Also before 09:00: restart the trader on HEAD (918f823), and either cancel the LAV-03/04 asks or reprice them to page price only if the buyer is a confirmed non-closer.
