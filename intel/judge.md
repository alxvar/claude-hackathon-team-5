# Judge (claude-opus-5-5, Sat 17:07)

## Verdict
Gaining on the leader, but the pack behind is closing fast. We are #2 at 29.73, 0.07 behind t14 (29.8). Over 60 min we moved +1.4 while t14 moved −0.5. Behind us, t01 (+3.9), t16 (+4.7) and t03 (+4.9) climbed faster than we did. `neg_points` was flat at 63.2 for the last 15 min (we went −0.3), so the ladder is our only live mover.

## Our strategies: keep / kill / scale
- **Dealer bot at Pilar (−2 steps):** scale. MAL-06 sold at 20 (her 16→19, never jumped): ladder 0.333 → 0.373 (+0.040), 0 neg. It confirms the step rule a second time.
- **Pícaros L4 buys:** stop, as already decided. SAL-09 and SAL-10 at 54 gave +0.070 and +0.063 ladder at 0 neg. Five more teams unlocked L4 at ticks 761-802, and the Analyst measured only ~+0.36 board for slot 2. Cash is 72, now ~92 after MAL-06, still under the 100 floor.
- **Flags:** paused; keep one probe only. +10 ×3, −10 ×1, then 0 ×3 (16:53) means net +20 and a cap [L].
- **Maker book (7 offers):** fix it.
  - 12512 sells LAV-02 to t07 for **0 P**. That scores −1.3 for us and hands t07 the card's whole value (up to the cap if it closes a page).
  - The five spare asks at 6-11 P have not filled. Only 5% of asks fill.
- **Trading loop:** keep, low yield. One accept since 15:29 (swap SAL-04 → RET-04, +6.2). Everything else in its log is old errors.
- **In-room / team buys:** keep, with care. MAL-08 was bought from t14 at 15 (+2.5). t14 was #1, so the "our gain ≥ 3× theirs" rule applied, and t14's gain is not in the data.

## Check the scout
- **Holds:**
  - Pícaros L4 is crowded: five unlocks at ticks 761-802.
  - Cash depends on the fever resales.
  - MAL-09 (value 49) sells at ≥ 55 for 0 neg.
  - Team 7 is a safe buyer.
- **Does not hold:**
  - **RET-04 is no longer a spare.** We hold one copy worth 83.9 because the RET page is complete. Selling it costs ~73.
  - **LAT-04 is a single copy worth 5, not 1.2.** At 9.5 the gain is +4.5, not +6.3.
  - **Offer 12179 (SAL-10 to t08 at 93) is gone.** It expired at tick 819 and is not in our open offers.
  - **The climb rates are wrong.** The scout gives t03 +6.1/h and t06 +3.7/h, and says t06 gained +2.2 in 15 min. Metrics show t03 +4.9, t06 +2.9 and t06 −0.8.
  - **MAL-08 went the other way.** t14 did not buy it from us; we bought it from t14.
  - **"t06 bought RET-04 from us" is false.** The feed shows t06 → t14.
  - **Its "who to sell to" table is stale.** It comes from tick 631, when t03 was #16; t03 is now #6, 1.5 below us.

## The 3 changes with the highest expected gain
1. **L4 slot 3: sell a spare LAV-02 (worth 1.3) to Pícaros.**
   - How: offer-only, ask high and step −2/−3, never at their opening bid, with the trick guard on.
   - In the same thread, send **one** flag probe, and only for a structured mismatch (card, price or direction ≠ the words).
   - Effect: a ladder slot at ~0 neg (slots 1-2 gave +0.07 / +0.063 before the field diluted them), plus a +10 flag if the cap is per hour.
   - Risk: a capped flag scores 0. A finality-type flag costs −10, so never send one.
2. **Clean the maker book now (`trade.py`).**
   - Cancel 12512 (LAV-02 at 0).
   - Cancel or verify the asks to t16 (SAL-01/02, 2.8 below us) and t03 (LAT-03, LAV-04, 1.5 below). Both are rising ~+5/h, inside the 6-point page-closer gap, and their page status is not in the data.
   - Re-list the true spares (LAV-02 ×2, LAV-03, LAV-04, SAL-04, LAT-03) as maker to low teams: t07, t08, t15, t09, t02, t04. Price them at 6-9, the recent common fills ran 4-10.
   - Effect: ≈ +3-5 neg per fill (≈ +0.5-0.8 board). Risk: slow fills.
3. **Fever resale with a floor (18:04-20:04).**
   - SAL-09 and SAL-10 go to Pilar with −2 steps, accepting ≥ 85 early.
   - In the last 30 min, drop to ≥ 63, our value, so neither rare is held into Sunday.
   - The MAL-09 → Pilar job at 17:30 runs at ≥ 55.
   - Effect: cash 92 → ~240 for the CHA page at 0 neg, plus a possible L3 slot.
   - Risk: every team that bought SAL rares from Pícaros (6 deals, median 58) dumps into the same window. Whether Pilar's price holds up under that is not in the data.
