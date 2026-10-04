# Judge (claude-opus-5-5, Sun 03:45)

## Verdict
**Holding #3** at 30.5, flat for 60 min while closed. We trail Team 10 by 7.1 (37.6) and Team 18 by 0.8 (31.3), and lead Team 12 by only 0.1 (30.4).

## Our strategies: keep / kill / scale
- **Team trades (bids, asks, swaps): SCALE.** They are the only lever with a measured board effect (≈ +0.05 board per neg point, tick 910). They produced +40.4 (SAL-06 page close, tick 988), +15.5 (t07 swap, tick 904) and +6.2 (t08 swap, tick 669). 17 team trades came from 414 listings, so most listings go unfilled.
- **Addressed asks (19979 LAV-03 → t04, 19981 LAV-04 → t01, at 6): CHANGE.** Both are unfilled and expire at tick 1455. Addressed asks fill at 0.3% vs 3.5% for open asks.
- **Trading loop: KEEP, but fix it.** It made 2 accepts all Saturday (+6.2, +15.5). Since then it has logged 5× `unknown_card sobre_bienvenida` and repeated DNS errors (22:55-23:24). Directive: sells-only until 09:00.
- **Dealer bot: KEEP, only for CHA buys and approved fodder.** The last thread (LAV-04 to Pícaros) correctly walked at a final of 4 below our floor of 7, with neg_points unchanged. Ladder 0.437 → 0.483 did not move `negotiating` per Chief 17:45 [L]. The −2.7 window at tick 632 shows dealer losses still leak.
- **Flags: KILL** (already done). Net +20; the cap is reached (the 17:43 probe scored 0).
- **Duels (Aleks): not ours.** 35.39 duel points; 8 of the last 10 closed.
- **v10 venue VC: no current number in the metrics.** Directive target: 40-50 net by the close.

## Check the scout
- **Holds:**
  - Rank gaps: 0.1 over #4 and 0.8 under #2.
  - LAT-10 t13 → t18 at 72 vs the 86 t12 paid.
  - t12 bought RET-11 at 216; t10 sold RET-03 at 8.
  - SAL-10 bid 68 is below our 122.6: do not sell.
  - Maker gain on LAV-03/04 at 6 = 2.8 each.
- **Wrong: "Team 10 sells epics … MAL-11 to t10 at 195".** The feed shows t08 → t10, so Team 10 *bought* MAL-11. It sold only SAL-11 (207).
- **Wrong: "t01 bids 152 for MAL-11 … open bids against us".** We hold no MAL-11 (only MAL-01..06 and MAL-08), so the bid doesn't apply to us.
- **Unsupported: "Team 10 hosts the cheap trades".** Not in the data.
- **Wrong reason: "t09 passes the feeding rule" (scout #2).** t09 is 7.2 below us, not ≥ 10. Row #1 is approved under the directive's ≥ 6 rule, and it isn't our sale, so the conclusion stands.
- **Risk in scout #3:** re-posting the LAV spares OPEN lets Team 10 (#1, collects LAV) take them. If one closes its page, Team 10 books up to +50 while we gain 2.8.

## The 3 changes with the highest expected gain
1. **Run the CHA fast start exactly as directed at round 3's first tick.**
   - Pícaros CHA-09/10 run `--offer-only`, with the Operator checking card and rarity before each accept. Open the pack, then post the capped maker bids.
   - CHA values (common 16, uncommon 40, rare 112, bonus 106) exceed dealer prices, so each buy scores and the close is worth up to +50.
   - Risks: bait-and-switch (7160, 8507) and print runs running out.
   - **Cash check:** we have 392 P. CHA case B is 250 P, which leaves 142, below the MAL GO line of 150. MAL is no-go unless Sunday's grant arrives (amount not in the data) or spares sell first. `CASH_FLOOR=464` keeps the trader sells-only until the books fill.
2. **Fire v10 row #1 (RET-09 t07 → t09, addressed, pre-agreed) first at 09:00, then rows #2/#3 at 08:30 per the directive.**
   - Effect: +67.6 VC, alone near the 40-50 real-trades target.
   - Risk: t09's holdings are unconfirmed. Lucas/Dani check before posting; skip the row if the RET-09 doesn't finish t09's page.
3. **Re-post the LAV spares OPEN only on a venue/price Team 10 can't use cheaply.**
   - Otherwise keep them addressed to vetted teams (t01/t04 are fine; both are outside the top 4).
   - Before 09:00, ask the Chief to exclude LAV-* from the open-ask rule (directive 00:37) while t10 still collects LAV.
   - Effect: protects us from a ≤ +50 leader gain, at a cost of ≤ 5.6 to us.
   - Before restart, also fix the loop's `sobre_bienvenida` error and add a DNS retry backoff, so it can't stall during the 09:00-11:00 accept window.
