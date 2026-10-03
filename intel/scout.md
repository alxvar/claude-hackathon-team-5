# Scout (claude-sonnet-5-5, Sat 16:41)

## Top 3 actions now
1. **Keep the Pícaros thread (SAL-09 bid 45, offer 11761, open to tick 775) alive and flag every checkable lie** (Operator, `POST /api/flags`; offer-only, small steps, never accept their terms). Evidence: flags moved `neg_points` 43.2 → 53.2 → 63.2 (n=2, clean windows). Their open buy of SAL-09 sits at 73 against our 45, and their last-seen sell was 10 → 13. Effect: +10.0 per correct flag (≈ +0.7 board each). The tick-775 expiry needs a move, not a repeat; the 4-tick expiry rule applies. Confidence: high on the +10 per correct flag, med on a fresh lie appearing each message. Stop at the first refused or penalised flag.
2. **SAL-09 / SAL-10 / SAL-07 bids on El Rastro: do not chase.** Bids: t03 SAL-10 at 73 (offer 11505), t06 SAL-09 at 68 (11579). We have no SAL-09 or SAL-10 and hold SAL-08 only as a reserved card. Our bid for SAL-07 at 20 (10569) expires at tick 772. Sell SAL-08 (worth 22.5) to Pilar during the Salamanca fever 18:03-20:03; it is a ladder-slot play only, with no neg_points gain. Confidence: med. If a team holder will sell SAL-09 or SAL-10 at ≤ 68, check value − price first.
3. **Sell spares to Team 7 (#17, 10.6 below us) and Team 16.** Existing asks: LAV-04 at 6 to t03 (11377), SAL-02 at 11 to t16 (11379), LAV-03 at 6 to t09 (11426), SAL-01 at 11 to t16 (11530), LAT-03 at 7 to t03 (11460). Evidence: Team 7 buys LAV×5, RET×3, and the file puts the gain at +4.3 to +6.3 per spare. Run `tools/policy.py can-give` first; it says NO for LAV-03/04, RET-04 and SAL-01. Effect: about +2 to +5 each as maker. Confidence: med.

## What the climbing teams are doing
- **Team 3 (+7.3 in 60 min):** it sells MAL-10 for 74 and buys LAT-09 at 88 (tick 724). It is also bidding 73 for SAL-10 (offer 11505), i.e. buying rares from teams.
- **Team 16 (+4.4):** it bids across many cards (RET-07 15, LAV-06 12, RET-01 5, LAV-01 3, MAL-03 1) and bought RET-06 at 14 (tick 711). That is low-ball bid volume plus rare buys; it has 32 deals.
- **Team 1 (+3.1 in 60 min):** 21 deals, buying MAL×4 and SAL×4 from teams. It reaches the scoreboard through steady small-value buys.
- **Top of the board (t14, t12, t10, t18):** flat or falling, so we lead the climbers with +1.6 over 60 min.

## Threats
- Team 14 leads at 30.1 against our 29.5, and Team 12 is at 29.3. Our four-bids reciprocity with Team 10 (#4) is a mild feed; keep its value created capped.
- Flag lies are public in the feed, so the field will copy the flag lever soon and we lose the exclusivity. Move fast.
- Team 13 (#10, 60 deals) is still pushing venue v03; never trade there, since it feeds that venue's owner.
