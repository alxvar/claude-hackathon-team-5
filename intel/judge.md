# Judge (claude-opus-5-5, Sun 11:12)

## Verdict
Holding, not gaining on #1. At 11:09 we are #4 at 32.2, level with t18 (32.2, −1.2/15 min). We trail t10 by 0.7 and t12 by 2.7. Over 60 min we made +2.2, against t12 +3.5, t03 +2.2, t18 +1.2 and t10 +0.6. t03 is 2.0 behind and climbing (+1.2/15 min).

## Our strategies: keep / kill / scale
- **Dealer bot (spares → Pícaros/Abuela): stop new threads; it is done.** Ladder went 0.253 → 0.342 and `neg_points` stayed flat. We have no spares left. Walking on LAT-03 at 5 (her opening = our value) was correct. Whether the ladder still moves the board is unproven ([L] flat on Sat 17:45).
- **Trading loop: keep it running passively.** It has no Sunday fills; Saturday gave +6.2 and +15.5. Our holdings are far above any bid (CHA bids top out at 19 vs our 146-218), so it cannot sell a page card.
- **LAT-06/07/08 bids at 9: keep.** They are ≥ 0 (worth 12.5 each, we are the maker) but worth only ~+3.5 each. Unfilled since at least tick 1910-1940. Posting time is not in the data.
- **MAL close (22816, 48 → t08): keep it, but the plan is stale.** MAL-07 went t15 → t03 at tick 1647, so "MAL-07 → t15" targets a team that may no longer hold it. t08 has been silent all weekend.
- **CHA bids pulled and book cleared: correct.** The page is complete; it scored +50 at tick 1585.
- **RET-11 round trip (bought from the Pícaros at 128, sold to t02 at 240): unexplained.** Predicted ≈ +42 (240 − 198 value). Measured: `neg_points` 50 → 50 and no score change logged since tick 1585.
- **v10 reward and ad: no evidence yet.** No v10 settlements or `mm_points` appear in the metrics ("not in the data"). It is Lucas's GUARDRAIL, so it stays.

## Check the scout
- Holds: MAL-07 t15 → t03 at 9 (tick 1647) · MAL-09 value 49 · t02 bought RET-11 from us at 240 · t13 bought SAL-11 from t18 at 238 · don't buy LAT/LAV/SAL commons (first LAT copy worth 5, asks at 8-9).
- Wrong or stale:
  - "We are #3 at 32.4, t10 0.2 behind, t18 1.0 ahead." Now we are #4, t10 is 0.7 ahead, and t18 is level.
  - "t10 falling." It is +0.7 in 15 min.
  - "CHA bids 15-64 P." The top bid is 19.
  - "t02 bought CHA-05 from us." It sold CHA-05 to us at 72.
  - "We hold the LAT page." We hold only LAT-03.
  - "Pícaros MAL-09 was a bait-and-switch." Not in the data: the log shows 73 → 49 against our 48, closed.
- "Accept nothing" is too broad: ≥ 0 non-last MAL buys still help.

## The 3 changes with the highest expected gain
1. **Sequence the MAL close: MAL-07 first, MAL-09 last.**
   - Have mal_close post an addressed bid to t03 for MAL-07 as the NON-last card. Price ≤ 17.5 (value), kept low (t03 paid 9) so t03 gains little. This is allowed: the 10:25 directive limits only the LAST card to non-rivals.
   - Once MAL-07 lands, 22816 (t08, non-rival) becomes the last card. mal_close then reprices it to ≤ value-when-last − 50 per `/api/me/value`.
   - Effect: ≈ +47-50 `neg_points` if buys still score (CHA did). At Saturday's ≈ 0.05 board/point, that is enough to pass t18 and t10.
   - Risk: if 22816 fills first, MAL-07 becomes the last card and its only known holder is a rival (blocked). The Chief should decide now whether to pause 22816 until MAL-07 is held; the cost is low given t08's silence.
2. **Resolve the RET-11 anomaly before the MAL spend and any further sale.**
   - The Analyst re-runs M5 on tick 1730 (expected +42, measured 0). Check: a Sunday team-trade cap at 50, sale gains not scoring, or pack drag.
   - Effect: shows whether MAL adds to our own score or only lowers rivals' reference (the 01:40 logic). Cash doesn't score, so MAL stays GO either way.
   - Risk: Analyst time only.
3. **Tighten the v10 reward rival list to match the 09:28 directive.**
   - The log shows "never t10/t13" plus policy.check. Confirm t12, t18 and t03 are excluded in `policy.check`, so no ≥ 0 buy pays a #1-#5 rival.
   - Effect: closes a feeding leak in the #3 race.
   - Risk: none; code check by the Builder.
