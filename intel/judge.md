# Judge (claude-opus-5-5, Sat 11:02)

## Verdict
Gaining: #2 at 27.8, 0.5 behind Team 18 (28.3). Over 15 min we gained +3.6 while Team 18 lost 2.0. Over 60 min Team 18 still out-gained us (+14.3 vs +12.5). The 15-min gain came from market (7.3 → 12.5, one trade on v10). `neg_points` has been flat at 28.5 since tick 276 (62 ticks).

## Our strategies: keep / kill / scale
- **In-room page closing (Lucas → Team 10): scale.** RET-01 at 20 as maker scored +50.0 and is our only positive `neg_points` today. RET net is +28.5.
- **Chato buys: kill.** He sold RET-09/10 at 87/86 (−10, −9) and RET-06 at 30. All 6 of our Chato deals were above list and none moved the ladder.
- **Dealer bot (Abuela): pause until Pilar.** It moved the ladder +0.004 on RET-07, but the RET page is done. Any further card we buy is a 2nd copy at 25% value (a RET common is worth 2.75 vs a 9 price), so every buy now subtracts.
- **Trading loop (loop.py): keep, low value.** The log shows no accepts today, only errors and a pause/resume. It stops for Duels I per the directive.
- **Maker book (book.py): keep, but fix it.** 16 asks are live with 0 fills since tick 276. Problems:
  - Three cards have duplicate asks to the same team, where the cheaper one supersedes the other: LAV-03 → t07 at 7 and 5, SAL-02 → t16 at 7 and 4, LAT-04 → t15 at 5 and 4.
  - MAL-07 → t01 at 22 targets a team that bought MAL-07 at 14 (tick 311) and MAL-06 at 20 (tick 321).
  - Our MAL asks at 22 sit above the 14-20 clears.
- **Reciprocal venue with Team 10: scale.** One t10 → t01 trade on v10 added +4.99 market and lifted us level with t12.

## Check the scout
- **Holds:**
  - Score 27.8, +3.6 in 15 min, `neg_points` flat at 28.5.
  - MAL clears at 14 and 20 sit below our 22 asks.
  - t02 bids 27 for RET-10.
  - t18 and t02 are within 0.6 of us; never feed them.
  - We have no 2nd RET copies.
- **Does not hold:**
  - "10 deals in the last 10 duels" are practice duels (session 1). Our duel score is 0.0, so they are no evidence for Duels I.
  - LAT-08 is not offer 4648 at 20; the live ask is 4971 at 18 → t15.
  - t02 bids 65 for SAL-09, not 68.
  - The tick-234 trade (t13 → t15) says nothing about Team 18.
  - It misses that t01 already bought MAL-06 and MAL-07.
  - "t02 may be closing RET" is unverified. t02 also sold RET-06 to t14 at 14.

## The 3 changes with the highest expected gain
1. **Align the Duels I accept hold with the real start (operator, now).**
   - The plan says Duels I starts at 11:30; the directive stops the trader at 11:50.
   - Read `/api/schedule`. If duels start before 11:50, stop loop.py and dealer threads at the actual start. This stays within the directive's intent: "until Duels I ends".
   - Effect: protects 34 scored duels; a missed duel deal scores 0. Its size in points is not in the data.
   - Risk: none; the loop has made no accepts today.
2. **Clean the book and route each live ask through Dani in the room.** This is the method that filled RET-01.
   - Cancel the superseded duplicates 4735, 4737 and 4738.
   - Re-address MAL-07 away from t01, to t17, t15 or t13. t13 is #6, outside the top 4, and collects MAL.
   - Step MAL-06 and MAL-07 to 20.
   - List the unlisted LAV-04 spare (2 copies held, 3.2 each).
   - Dani points each addressee at its live offer.
   - Effect: the current book sums to about +40 `neg_points` if everything fills (e.g. MAL at 20 = +2.5, SAL-01 at 10 = +7.8, LAT-08 at 18 = +5.5). That is about +6 board at the 0.16 rate [L]. It also builds cash toward the ~300 P CHA page.
   - Risk: feeding a climber. t01 is +11.1/60 min but 7.2 below us. No sales to t18, t02, t12 or t14.
3. **Pitch non-top-4 traders to settle on v10 at 0% (Dani, during Duels I).**
   - Targets are teams already trading MAL/LAT/SAL among themselves: t01, t04, t15, t17, t10.
   - Effect: one trade gave +4.99 market. More trades are the cheapest board points while our accepts are frozen.
   - Risk: reciprocity with t10. Keep the market session's alert on a > 2:1 imbalance. Our broker must stay up (a down venue scores 0).
