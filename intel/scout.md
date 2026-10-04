# Scout (claude-sonnet-5-5, Sun 06:29)

## Top 3 actions now

1. **Wait for Sunday 09:00, then run the CHA fast start (Operator, `simple_buy.py`)**
   - Action: both CHA rares from the Pícaros at the first tick of round 3, with `--offer-only`. Operator checks card and rarity before accepting. Public CHA bids stay capped at 9 / 22 / 54. Open the silver pack right after the release.
   - Evidence: the game is closed until Sun 09:00 (tick 1445). Pícaros print runs run low (SAL-09 29/30, SAL-11 9/9). Our CHA multiplier is 1.6. Cash is 392.
   - Effect: CHA page finish. The per-trade cap is 50, and it is likely lower with pack drag (SAL close gave +40.4). The 25% page bonus counts only via a team trade [L].
   - Confidence: med.

2. **Close the MAL page after CHA if ≥ 150 P is left (Operator; seller by Lucas/Dani WhatsApp)**
   - Action: we hold MAL-01..05, MAL-06 and MAL-08. The directive says GO at ≥ 150 P. Check `/api/me/value` for the missing MAL cards, and the open MAL asks (MAL-03 12, MAL-01 12, MAL-04 12 are on El Rastro but we already hold those).
   - Evidence: the directive (01:40) estimates about +30 np past our cap. The rate is ≈ 0.05 board per np (Sat 17:46). We have 119.1 np.
   - Effect: about +1.5 board at that rate. It also lowers t18/t12/t03 through the relative reference [L].
   - Confidence: low-med. Which MAL card is missing is not in the data.

3. **Keep the open sells on El Rastro and sell spares OPEN (Operator, `trade.py`)**
   - Action: LAV-03 → t04 (19979) and LAV-04 → t01 (19981) expire at tick 1455. The game is paused, so repost them as open asks at ≥ 6. Open asks fill 10× more than addressed ones (3.5% vs 0.3%).
   - Evidence: our spares are worth 3.2 each (LAV-03/04 ×2) and 1.3 (LAV-02 ×3). The El Rastro ask for LAV-02 is 10, so open asks at about 9-10 are plausible.
   - Effect: small, +1 to +3 np per sale. Never sell a page card, and not to the top 4 (t10, t18, t12).
   - Confidence: med.

## What the climbing teams are doing
- **Team 12** (+0.4, #4) bought RET-11 epic at 216 from t06, then LAT-10 at 86 and LAT-06 at 20. It collects RET/MAL/LAT with 29 team trades. It is the only top-4 team still climbing.
- **Team 18** (+0.8, #2) bought LAT-10 at 72 from t13 at tick 1332. It collects RET/LAT and is the biggest climber.
- **Team 10** (#1, 37.6) feeds on epics: MAL-11 at 195 and SAL-11 sold at 207. It has 467 listings and 62 deals.
- **Team 16** (+0.3) has 796 listings and collects RET. Its prices are low (c 4 / u 14 / r 50), so it is a possible cheap buyer.

## Threats
- Team 10 leads by 7.1 points. Any trade on its venue, or any sale to it, feeds it. Never sell to t10, t18 or t12 (the feeding rule).
- Epic competition: Pilar pays ~140 for epics. RET-11 goes to Pilar only at ≥ 198, per the directive. Team 12 (216 for RET-11) is the benchmark price.
- Teams that bid for our holdings: t09 bids 68 for SAL-10 and 20 for SAL-06. t09 is at 23.3 (#16), which is fine under the feeding rule, but those are our page cards, so do not sell them.
