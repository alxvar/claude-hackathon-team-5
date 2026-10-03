# Market plan for Sunday (Market session) · written Sun 00:18

_Sources: intel/matches.md (matchmaker run 00:13, tick 1440; its VC estimates move between runs, so re-read it before acting), leaderboard snapshot 1440 (us 30.49), intel/market-log.md, intel/directives.md (Club Castizo, Sat 22:55). Labels: [V] measured, [L] inferred, [?] unknown. An independent verifier audited the 22:52 draft; its ten flags are applied here._

## 0. NEGOTIATION (Chief's overnight ask; read-only analysis of data/feed.jsonl to tick 1445)

**Data and its limits [V]:** 7608 cash offers (asks and bids) and 176 team-to-team settlements over Friday and Saturday; 149 fills could be tied to their offer. The feed has NO team-to-team threads or counter messages (threads exist only with dealers), so a 'counter' can only be seen as a new offer in the opposite direction. Per team there are 2 to 22 accepts: the per-team rows are counts, not fitted curves. Ratios are price ÷ book (common 10, uncommon 25, rare 70, epic 180). Ticks were 60 s on Friday and 30 s on Saturday; Sunday is 15 s, so a bot that acts once per tick keeps its latency in ticks and a human-driven team doubles it.

### 0.1 How the market answers an offer (all teams, Saturday, open offers)

| Offer | price ÷ book | listed | filled | filled within 2 ticks |
|---|---|---|---|---|
| bid | 0-0.7 | 1305 | 12 (0.9%) | 4 (0.3%) |
| bid | 0.7-1.0 | 149 | 9 (6.0%) | 3 (2.0%) |
| bid | 1-1.3 | 46 | 5 (10.9%) | 1 (2.2%) |
| bid | 1.3-∞ | 5 | 1 (20.0%) | 1 (20.0%) |
| ask | 0-0.7 | 401 | 20 (5.0%) | 12 (3.0%) |
| ask | 0.7-1.0 | 1373 | 25 (1.8%) | 9 (0.7%) |
| ask | 1-1.3 | 1424 | 24 (1.7%) | 11 (0.8%) |
| ask | 1.3-∞ | 535 | 1 (0.2%) | 0 (0.0%) |

- **Price does not buy speed.** An open bid at or above book was filled within 2 ticks 2 times out of 51; a cheap ask (≤ 0.7 book) within 2 ticks 12 times out of 401. About 2% of all offers ever fill.
- **Addressed offers are almost never accepted:** 20 of 1881 (1.1%); when accepted, median 4 ticks, 10 of 20 within 2 ticks. The fast ones were pairs that had clearly agreed first (Team 8's four bids on v21 at tick 707-714, all taken in 1-2 ticks).
- **A second, better offer does not help:** first listings of a card filled 47/580 (8.1%); re-listings 68/6506 (1.0%); re-listings at an improved price 33/1581 (2.1%). Bots do not chase a rising bid.
- **What buyers pay against their own value** (asks taken, 49 cases where the Analyst has the buyer's multiplier): median 0.75 of value, 90% at or under 1.12. Clearing prices on Saturday (filled, price ÷ book): commons asks 0.5-0.9 (median 0.7), uncommons 0.76-1.04 (0.96), rares 1.0-1.2 (1.07); filled bids sit lower (commons and uncommons 0.6, rares 1.0).
- **Cheap asks get sniped:** of the 20 asks at ≤ 0.7 book that filled, 12 went within 2 ticks.

### 0.2 Per team (counts over both days; 'fast' = at least 5 accepts and half of them within 2 ticks)

| Team | Asks it took (n · median ÷ book · max) | Bids it hit (n · median · min) | Accept latency (median ticks · ≤ 2 ticks) | Addressed to it: accepted | Counters | Type |
|---|---|---|---|---|---|---|
| Team 1 | 9 · 0.80 · 1.03 | 0 · — · — | 6 · 3/9 | 0/109 | 2/109 | slow or manual |
| Team 2 | 5 · 0.80 · 1.20 | 4 · 1.50 · 0.40 | 1 · 9/9 | 1/147 | 3/146 | fast bot taker |
| Team 3 | 2 · 0.65 · 0.70 | 0 · — · — | 4.5 · 1/2 | 1/219 | 0/218 | few accepts |
| Team 4 | 12 · 0.65 · 1.20 | 3 · 0.89 · 0.50 | 4 · 6/15 | 2/93 | 0/91 | slow or manual |
| Team 5 | 2 · 0.96 · 1.12 | 0 · — · — | 7.5 · 0/2 | 0/52 | 1/52 | few accepts |
| Team 6 | 3 · 1.09 · 1.17 | 8 · 0.70 · 0.50 | 2 · 6/11 | 1/163 | 0/162 | fast bot taker |
| Team 7 | 10 · 1.00 · 1.76 | 1 · 0.84 · 0.84 | 8 · 2/11 | 0/102 | 0/102 | slow or manual |
| Team 8 | 3 · 0.60 · 1.09 | 3 · 0.80 · 0.56 | 11.0 · 0/6 | 3/65 | 2/62 | slow or manual |
| Team 9 | 8 · 0.90 · 1.12 | 1 · 1.04 · 1.04 | 8 · 3/9 | 1/156 | 18/155 | slow or manual, counters |
| Team 10 | 3 · 1.06 · 1.20 | 6 · 0.90 · 0.60 | 6 · 2/9 | 2/44 | 0/42 | slow or manual |
| Team 12 | 12 · 0.79 · 1.23 | 10 · 0.66 · 0.40 | 4.0 · 8/22 | 1/59 | 3/58 | slow or manual |
| Team 13 | 5 · 1.00 · 1.20 | 5 · 0.56 · 0.40 | 2.0 · 6/10 | 4/187 | 0/183 | fast bot taker |
| Team 14 | 7 · 0.70 · 1.00 | 3 · 0.60 · 0.52 | 1.0 · 8/10 | 0/61 | 0/61 | fast bot taker |
| Team 15 | 5 · 0.90 · 1.04 | 5 · 0.80 · 0.52 | 7.0 · 2/10 | 1/145 | 2/144 | slow or manual |
| Team 16 | 3 · 0.50 · 0.97 | 3 · 0.40 · 0.40 | 3.5 · 3/6 | 2/130 | 0/128 | fast bot taker |
| Team 17 | 5 · 1.04 · 1.12 | 0 · — · — | 5 · 0/5 | 1/119 | 1/118 | slow or manual |
| Team 18 | 0 · — · — | 3 · 1.00 · 0.92 | 4 · 1/3 | 0/27 | 0/27 | few accepts |

- **Fast bot takers: Team 2, Team 6, Team 13, Team 14, Team 16.** They accept a priced-right open offer within 1-2 ticks; an open ask or bid is enough for them. Everyone else needs a WhatsApp agreement first.
- **Only Team 9 counters** (18 of 155 unfilled addressed offers answered with its own price, e.g. our LAV-02 ask at 8 → its bid at 2; a MAL-10 bid at 70 → its ask at 81). Its counter is its real price: accept it or leave it.
- **Reaction to a 2nd bid, per team:** not measurable (too few cases per team). Market-wide a better re-listing fills no more often than the first (above).
- **Sellers that hit bids below book:** Team 12 (10 bids hit, median 0.66), Team 6 (8, 0.70), Team 13 (5, 0.56; it sold MAL-10 into a 30 P bid), Team 16 (3, 0.40). Sellers that hold out for book or more: Team 18, Team 2, Team 9.

### 0.3 Our Sunday buys: what closes within 2 ticks

Simulation [L]: a posted open bid, raised every 2 ticks, against the Saturday fill table (it assumes Sunday's bots answer per tick as Saturday's did).

| Ladder (price ÷ book) | closes within 2 ticks | within 10 ticks |
|---|---|---|
| open 0.8, step +0.1, max 1 | 2% | 10% |
| open 1, step +0.1, max 1.3 | 2% | 40% |
| open 1, step +0.15, max 1.6 | 2% | 40% |
| open 1.3, step +0, max 1.3 | 20% | 67% |
| open 1.6, step +0, max 1.6 | 20% | 67% |

**No bid ladder closes within 2 ticks with any reliability** (the ≥ 1.3 row rests on 5 bids). What does close in the same tick is our own accept. So the rule is a procedure, not a price:

1. **A standing ask at or under our max: accept it the tick it appears** (one accept per tick; the trader's auto-accept does this). That is the only move nobody can snipe.
2. **No ask: agree by WhatsApp first**, then the seller posts an ask addressed to us and we accept in the same tick. Addressed offers without that agreement fill 1% of the time.
3. **Fallback bid** only for fast bot sellers (Teams 12, 6, 13, 16 hit bids): one bid at the max, not a ladder; raising it does not raise the odds.

| Buy | Book | Our value | Take any ask up to | Fallback bid | Max | Note |
|---|---|---|---|---|---|---|
| CHA common | 10 | 16 | 12 | 10 | 13 | Saturday's new set (RET) cleared at 0.8-1.2 book for commons in the first hours, rares at 1.2 (84 P). Max = 0.8 × our value, so every buy keeps at least 20% of value as points. |
| CHA uncommon | 25 | 40 | 30 | 25 | 32 | Saturday's new set (RET) cleared at 0.8-1.2 book for commons in the first hours, rares at 1.2 (84 P). Max = 0.8 × our value, so every buy keeps at least 20% of value as points. |
| CHA rare | 70 | 112 | 84 | 70 | 90 | Saturday's new set (RET) cleared at 0.8-1.2 book for commons in the first hours, rares at 1.2 (84 P). Max = 0.8 × our value, so every buy keeps at least 20% of value as points. |
| MAL-07 (uncommon) | 25 | 17.5 (+46 only as the card that closes the page) | 17 | none | 17; about 40 as the page closer | **WhatsApp: Team 15** holds the spare and listed it at 14 P on v10 on Saturday. History: 14, 17, 25, 26 P. Ask for an addressed ask at 14-16 P on a 0% venue (not v10: we cannot trade on our own stall). No live ask or bid at the close. |
| MAL-09, MAL-10 (rares) | 70 | 49 each | 49 | none | 49 | **Do not chase from teams.** Team 9 has standing bids at 56 P for both, above our value; MAL-10's fills were 65, 70, 74 P, with one 30 P dump by Team 13 into a bid. From teams they cost more than they are worth to us; the directive's route (dealers first) stands. Take a team ask only at ≤ 49. |

Our MAL page still lacks MAL-07, MAL-09 and MAL-10 [V, /api/me at 00:20]: MAL-07 is the closer only after both rares are in.

### 0.4 Our Sunday sells (spares only)

Spares [V, /api/me]: LAV-02 ×2, LAV-03 ×1, LAV-04 ×1; LAT-03 and LAT-04 are single cards of a set we do not collect (LAT 0.5, 2 of 10 held).

- **Our asks do not sell:** 1 of 328 asks filled on Saturday, against 4 of 22 bids. Market-wide an ask at ≤ 0.7 book fills 5% of the time and above that under 2%. Lowering the price is not the lever.
- **What sells:** hitting a standing bid (immediate), or a pre-agreed buyer. No bid is live for any of our spares at the close; Saturday's LAV common fills were 3 to 10 P and the LAV buyers were Team 8 (3 buys), then Teams 9, 7, 4, 6, 13.
- **Prices:** LAV commons: ask 7 (0.7 book) open on a member's 0% venue, floor 4 (our spare is worth 3.25 to us as a 2nd copy); LAT-03/04: ask 6, floor 5 (our value). One ask per card, no re-listing ladder: re-listings fill 1%.
- **Best use of the LAV-02 spares:** Team 9 has asked for LAV-02 (matchmaker) and Team 9 counters with its own price: offer it by WhatsApp, expect a counter near 2-8 P, accept anything ≥ 4. The trade has to sit on another member's venue, so its VC goes to that member: a club favour, not v10 points.

### 0.5 The 09:00 v10 list, in order, and who needs a WhatsApp first

| # | Buyer | Seller | Card | Price | Expected VC (low) | Pre-agree by WhatsApp? |
|---|---|---|---|---|---|---|
| 1 | Team 9 | Team 7 | RET-09 | ~70 | +67.6 | YES: Team 9 (slow or manual, counters); page finisher: Chief's OK first |
| 2 | Team 7 | Team 8 | SAL-05 | ~9 | +7.9 | YES: Team 7 (slow or manual) |
| 3 | Team 7 | Team 9 | SAL-02 | ~9 | +6.5 | YES: Team 7 (slow or manual) |
| 4 | Team 8 | Team 7 | MAL-02 | ~9 | +7.2 | YES: Team 8 (slow or manual); Team 7: confirm it is a spare |
| 5 | Team 1 | Team 7 | RET-08 | ~22 | +13.7 | YES: Team 1 (slow or manual); Team 1: outside the club, Chief's OK |
| 6 | Team 8 | Team 1 | SAL-03 | ~9 | +12.9 | YES: Team 8 (slow or manual); Team 1: outside the club, Chief's OK |
| 7 | Team 9 | Team 16 | LAV-02 | ~9 | +11.2 | YES: Team 9 (slow or manual, counters); Team 16: outside the club, Chief's OK |
| 8 | Team 7 | Team 1 | SAL-01 | ~9 | +7.8 | YES: Team 7 (slow or manual); Team 1: outside the club, Chief's OK |
| 9 | Team 16 | Team 2 | RET-01 | ~9 | +7.4 | YES: Team 16: outside the club, Chief's OK |
| 10 | Team 16 | Team 4 | RET-03 | ~9 | +7.1 | YES: Team 16: outside the club, Chief's OK |

8 of the 10 buyers are slow or manual accepters, and the others sit outside the club, so **every row needs a WhatsApp (or the Chief's OK) first**; the seller then posts an OPEN ask on v10 at the agreed price and the buyer accepts (or posts the matching bid: the stall crosses them in that tick).

### 0.6 Who Team 10 trades with (to offer them better terms first)

- **Team 10's own trades, both days [V]:** 16 in all: Team 6 3, Team 8 2, Team 12 2, Team 13 2, Team 4 1, Team 5 1, Team 1 1, Team 15 1, Team 3 1, Team 9 1, Team 17 1. It trades little and with everyone; no single partner dominates. Its two largest deals were with Team 8 (MAL-11 at 195) and Team 17 (SAL-11 at 207), both on El Rastro.
- **Who fed its market v07 [V, §7]:** Team 6 (maker of 6 of 11 fills), us (4, stopped), Team 4 (1); takers Teams 12 and 14 (3 each); Team 8 is the heaviest lister there.
- **Better terms first, in this order:** Team 8 (club candidate, heaviest v07 lister, already sold Team 10 its epic), Team 4 (club candidate, v07 maker), then Team 9 (it holds bids for the MAL rares Team 10 sells). Teams 6, 12, 13 and 14 are rivals: no terms, they follow listings. Team 1 is the reported ally.

## 1. What Sunday is worth and what it takes

- **Market Test: nothing to do [L].** The deck says Market Test = 7.5. After six benches every stall team shows 7.5 and no team has ever shown a market above 12.5 [V, all snapshots]. Keep the free stall v10 (auto, 0%). No board venue: it adds only the broker-down risk.
- **Real trades [L]: points = 5.0 × min(1, our VC / mean VC of the top three venues).** An inference: it reproduced one event (snapshot 560, Team 6's rare trade) for three teams to 0.01, and nothing has contradicted it. VC = buyer's value − seller's value, summed over the round's trades on v10. A negative total looks floored at zero (we sat at exactly 7.5 with mm −5.2) [L]; §4 asks the desk. Sunday is a new round, so our −5.2 should be gone [L].
- **What counts is VC at the close, not the first hour.** A lead decays as other venues trade.

Simulation [L, model; every parameter is an assumption: 11 rival venues with Saturday's uneven trade counts, 12% of trades negative, 6 h of play]. Our score by VC at the close:

| Field trades at | rivals' top-three mean (median, p90) | VC 40 | 60 | 80 | 100 | 150 | 200 |
|---|---|---|---|---|---|---|---|
| Saturday's hourly rate | 59, 96 | 3.3 | 4.2 | 4.7 | 4.9 | 5.0 | 5.0 |
| 2× (15 s ticks, +550 P a team) | 108, 156 | 2.0 | 2.9 | 3.6 | 4.1 | 4.8 | 5.0 |
| 3× | 156, 213 | 1.4 | 2.1 | 2.7 | 3.2 | 4.2 | 4.8 |

Our VC needed for full marks with 80% confidence (2× case): **35 after 30 min · 50 after 1 h · 80 after 2 h · 100 after 3 h · 125 after 4 h · 170 at the close.** In trades: two big ones (a rare or a page finisher) plus one common or uncommon first-copy trade every 30-40 minutes, and **no negative trade**: one bad trade took a venue's real-trades score to zero three times on Saturday (ours, Team 12's, Team 7's).

## 2. The 10 best v10 trades for 09:00

Built from the match list above. Filter: no rival buyer (fixed t13, t17, and any team within 3 board of us or above) · page finishers only for buyers more than 5 below us · each seller's card and each buyer's want used once. Order: Club Castizo pairs first (both teams among the candidates Team 7, Team 9, Team 8, Team 15, Team 4, Team 2), then pairs that need a team outside the club, then rival sellers. VC = the matchmaker's LOW estimate.

| # | Group | Card | Seller → Buyer | ~Price | VC (low) | Spare check | Flags |
|---|---|---|---|---|---|---|---|
| 1 | club | RET-09 El Ángel Caído | Team 7 → Team 9 | 70 | +67.6 | spare seen (2 copies listed) | PAGE FINISHER for Team 9 (-7.3 board vs us) |
| 2 | club | SAL-05 Taxi Blanco | Team 8 → Team 7 | 9 | +7.9 | spare seen (4 copies listed) | — |
| 3 | club | SAL-02 El Portero | Team 9 → Team 7 | 9 | +6.5 | spare seen (2 copies listed) | — |
| 4 | club | MAL-02 Plaza del Dos de Mayo | Team 7 → Team 8 | 9 | +7.2 | ASK FIRST: one copy seen (seller dumps the set) | — |
| 5 | outside | RET-08 Palacio de Velázquez | Team 7 → Team 1 | 22 | +13.7 | spare seen (2 copies listed) | Team 1: Team 10's reported ally (directive 17:45) |
| 6 | outside | SAL-03 Perrito con Abrigo | Team 1 → Team 8 | 9 | +12.9 | spare seen (3 copies listed) | Team 1: Team 10's reported ally (directive 17:45) |
| 7 | outside | LAV-02 El Frutero de Argumosa | Team 16 → Team 9 | 9 | +11.2 | spare seen (2 copies listed) | Team 16: runs its own market (market score 10.16) |
| 8 | outside | SAL-01 Escaparate de Serrano | Team 1 → Team 7 | 9 | +7.8 | spare seen (3 copies listed) | Team 1: Team 10's reported ally (directive 17:45) |
| 9 | outside | RET-01 Barca del Estanque | Team 2 → Team 16 | 9 | +7.4 | spare seen (2 copies listed) | Team 16: runs its own market (market score 10.16) |
| 10 | outside | RET-03 El Titiritero | Team 4 → Team 16 | 9 | +7.1 | spare seen (2 copies listed) | Team 16: runs its own market (market score 10.16) |

- Club pairs: 4, **+89.2 VC**; +67.6 of it is one trade, RET-09 Team 7 → Team 9, whose estimate has read between +68 and +134 across tonight's matchmaker runs.
- All ten: +149.3. The outside pairs involve Team 1 or Team 16; each needs the Chief's OK (flags).
- intel/wants.md was still empty at this run: real want-lists should add club pairs.

**Two-way swaps (card for card, price 0, settle by acceptance on v10).** These reuse cards from the table: a swap replaces the two cash trades, it does not add to them.

- Team 7 ↔ Team 9: RET-09 goes to Team 9, SAL-02 goes to Team 7 · VC +74.1
  - To Team 7: "Hi Team 7! Swap idea, no cash: your spare El Ángel Caído (RET-09) for Team 9's El Portero (SAL-02). If RET-09 is a spare for you, post it on v10 as give RET-09, want SAL-02, addressed to Team 9; they accept."
  - To Team 9: "Hi Team 9! Team 7 is posting a swap for you on v10: their RET-09 for your spare SAL-02. Accept it only if SAL-02 is a spare for you."
- Team 8 ↔ Team 7: SAL-05 goes to Team 7, MAL-02 goes to Team 8 · VC +15.1 · one leg has only one copy seen: confirm it is a spare before anything is posted
  - To Team 8: "Hi Team 8! Swap idea, no cash: your spare Taxi Blanco (SAL-05) for Team 7's Plaza del Dos de Mayo (MAL-02). If SAL-05 is a spare for you, post it on v10 as give SAL-05, want MAL-02, addressed to Team 7; they accept."
  - To Team 7: "Hi Team 7! Team 8 is posting a swap for you on v10: their SAL-05 for your MAL-02. Accept it only if MAL-02 is a spare for you."
- Team 7 ↔ Team 1: RET-08 goes to Team 1, SAL-01 goes to Team 7 · VC +21.5
  - To Team 7: "Hi Team 7! Swap idea, no cash: your spare Palacio de Velázquez (RET-08) for Team 1's Escaparate de Serrano (SAL-01). If RET-08 is a spare for you, post it on v10 as give RET-08, want SAL-01, addressed to Team 1; they accept."
  - To Team 1: "Hi Team 1! Team 7 is posting a swap for you on v10: their RET-08 for your spare SAL-01. Accept it only if SAL-01 is a spare for you."

### Ready DMs

**1. RET-09 · Team 7 → Team 9 at ~70 P**
- Seller-ask first. To Team 7: "Hi Team 7! Is your El Ángel Caído (RET-09) a spare? If yes, post it on v10 as an open ask at ~70 P: Team 9 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 9: "El Ángel Caído (RET-09) is on v10 at ~70 P, 0% fee. Accept it there."
- Buyer-bid first. To Team 9: "Hi Team 9! Post an open bid for El Ángel Caído (RET-09) at ~70 P on v10 (0% fee): Team 7 has listed it and the stall crosses a matching ask the same tick." Then to Team 7: "There is a bid for RET-09 at ~70 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**2. SAL-05 · Team 8 → Team 7 at ~9 P**
- Seller-ask first. To Team 8: "Hi Team 8! Is your Taxi Blanco (SAL-05) a spare? If yes, post it on v10 as an open ask at ~9 P: Team 7 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 7: "Taxi Blanco (SAL-05) is on v10 at ~9 P, 0% fee. Accept it there."
- Buyer-bid first. To Team 7: "Hi Team 7! Post an open bid for Taxi Blanco (SAL-05) at ~9 P on v10 (0% fee): Team 8 has listed it and the stall crosses a matching ask the same tick." Then to Team 8: "There is a bid for SAL-05 at ~9 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**3. SAL-02 · Team 9 → Team 7 at ~9 P**
- Seller-ask first. To Team 9: "Hi Team 9! Is your El Portero (SAL-02) a spare? If yes, post it on v10 as an open ask at ~9 P: Team 7 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 7: "El Portero (SAL-02) is on v10 at ~9 P, 0% fee. Accept it there."
- Buyer-bid first. To Team 7: "Hi Team 7! Post an open bid for El Portero (SAL-02) at ~9 P on v10 (0% fee): Team 9 has listed it and the stall crosses a matching ask the same tick." Then to Team 9: "There is a bid for SAL-02 at ~9 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**4. MAL-02 · Team 7 → Team 8 at ~9 P**
- Seller-ask first. To Team 7: "Hi Team 7! Is your Plaza del Dos de Mayo (MAL-02) a spare? If yes, post it on v10 as an open ask at ~9 P: Team 8 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 8: "Plaza del Dos de Mayo (MAL-02) is on v10 at ~9 P, 0% fee. Accept it there."
- Buyer-bid first. To Team 8: "Hi Team 8! Post an open bid for Plaza del Dos de Mayo (MAL-02) at ~9 P on v10 (0% fee): Team 7 has listed it and the stall crosses a matching ask the same tick." Then to Team 7: "There is a bid for MAL-02 at ~9 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**5. RET-08 · Team 7 → Team 1 at ~22 P**
- Seller-ask first. To Team 7: "Hi Team 7! Is your Palacio de Velázquez (RET-08) a spare? If yes, post it on v10 as an open ask at ~22 P: Team 1 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 1: "Palacio de Velázquez (RET-08) is on v10 at ~22 P, 0% fee. Accept it there."
- Buyer-bid first. To Team 1: "Hi Team 1! Post an open bid for Palacio de Velázquez (RET-08) at ~22 P on v10 (0% fee): Team 7 has listed it and the stall crosses a matching ask the same tick." Then to Team 7: "There is a bid for RET-08 at ~22 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**6. SAL-03 · Team 1 → Team 8 at ~9 P**
- Seller-ask first. To Team 1: "Hi Team 1! Is your Perrito con Abrigo (SAL-03) a spare? If yes, post it on v10 as an open ask at ~9 P: Team 8 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 8: "Perrito con Abrigo (SAL-03) is on v10 at ~9 P, 0% fee. Accept it there."
- Buyer-bid first. To Team 8: "Hi Team 8! Post an open bid for Perrito con Abrigo (SAL-03) at ~9 P on v10 (0% fee): Team 1 has listed it and the stall crosses a matching ask the same tick." Then to Team 1: "There is a bid for SAL-03 at ~9 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**7. LAV-02 · Team 16 → Team 9 at ~9 P**
- Seller-ask first. To Team 16: "Hi Team 16! Is your El Frutero de Argumosa (LAV-02) a spare? If yes, post it on v10 as an open ask at ~9 P: Team 9 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 9: "El Frutero de Argumosa (LAV-02) is on v10 at ~9 P, 0% fee. Accept it there."
- Buyer-bid first. To Team 9: "Hi Team 9! Post an open bid for El Frutero de Argumosa (LAV-02) at ~9 P on v10 (0% fee): Team 16 has listed it and the stall crosses a matching ask the same tick." Then to Team 16: "There is a bid for LAV-02 at ~9 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**8. SAL-01 · Team 1 → Team 7 at ~9 P**
- Seller-ask first. To Team 1: "Hi Team 1! Is your Escaparate de Serrano (SAL-01) a spare? If yes, post it on v10 as an open ask at ~9 P: Team 7 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 7: "Escaparate de Serrano (SAL-01) is on v10 at ~9 P, 0% fee. Accept it there."
- Buyer-bid first. To Team 7: "Hi Team 7! Post an open bid for Escaparate de Serrano (SAL-01) at ~9 P on v10 (0% fee): Team 1 has listed it and the stall crosses a matching ask the same tick." Then to Team 1: "There is a bid for SAL-01 at ~9 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**9. RET-01 · Team 2 → Team 16 at ~9 P**
- Seller-ask first. To Team 2: "Hi Team 2! Is your Barca del Estanque (RET-01) a spare? If yes, post it on v10 as an open ask at ~9 P: Team 16 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 16: "Barca del Estanque (RET-01) is on v10 at ~9 P, 0% fee. Accept it there."
- Buyer-bid first. To Team 16: "Hi Team 16! Post an open bid for Barca del Estanque (RET-01) at ~9 P on v10 (0% fee): Team 2 has listed it and the stall crosses a matching ask the same tick." Then to Team 2: "There is a bid for RET-01 at ~9 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**10. RET-03 · Team 4 → Team 16 at ~9 P**
- Seller-ask first. To Team 4: "Hi Team 4! Is your El Titiritero (RET-03) a spare? If yes, post it on v10 as an open ask at ~9 P: Team 16 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 16: "El Titiritero (RET-03) is on v10 at ~9 P, 0% fee. Accept it there."
- Buyer-bid first. To Team 16: "Hi Team 16! Post an open bid for El Titiritero (RET-03) at ~9 P on v10 (0% fee): Team 4 has listed it and the stall crosses a matching ask the same tick." Then to Team 4: "There is a bid for RET-03 at ~9 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

## 3. Test plan, first 30 minutes (09:00-09:30), measured live

Incentive is fixed by the directive (Club Castizo, Sat 22:55): seller's bonus per member-to-member deal on v10 of 1 P common, 2 P uncommon, 3 P rare, 5 P epic, +3 P if it completes the buyer's page, cap 15 P per team per day. It replaces Saturday's public rebate, so the test is about the pitch, not the price.

| Arm | Pairs from §2 | Pitch |
|---|---|---|
| A | odd numbers | seller's open ask first, then tell the buyer |
| B | even numbers | buyer's open bid first, then tell the seller |

- **Metrics (the Market session logs them from the feed):** minutes from DM to listing · listing to fill · fills per arm by 09:30 · VC sign of each fill (mm before → after).
- **09:30 decision:** the arm with more fills becomes the default. If neither has a fill, price is not the problem (Saturday: a 10 P rebate got zero listings in 105 minutes): move to swaps (no cash, both sides gain) and to asking in person in the room.
- **Stop rule:** any fill that lowers mm: pause that seller's pitches and ask what it sold (a page card or an only copy).
- **Prior [V, Saturday]:** 30 of 35 fills on team venues were open offers taken by board-scanning bots; 5 were addressed. On an auto stall a bid and an ask for the same card cross in the same tick whichever comes first [L].

## 4. Desk question for Dani (in writing)

> On Saturday the best market on the leaderboard showed 12.5 = 7.5 (the Market Test) + 5.0. No venue showed more than +5.0 for real trades, and several sat at exactly +5.0 for hours. The Payday deck says real trades are worth 22.5. **What earns the full 22.5: is +5.0 a cap for Saturday, a share of the round, or does the scale change on Sunday?** Second question: our stall shows `value_created` 9.0 in its venue detail while our score shows `mm_points` −5.2 for the same two trades. **Which of the two is scored, and does a negative total subtract or stop at zero?**

## 5. Standing rules for v10 on Sunday

- Open offers for cash trades (on Saturday 30 of 35 venue fills were open offers); swaps are addressed and accepted.
- Spares only on the giving side: the SAL-07 sale on v10 and the MAL swap on Team 7's stall each cost that venue its whole real-trades score (up to 5 points).
- No rival buyers; page finishers only for teams more than 5 board below us.
- Club deals on v10, none on v07 (directive 22:55).
- The Market session watches every v10 listing (page-risk tag) and fill (mm before → after) from 09:00 and reports each to the Chief.

## 6. Club forecast [L, model on top of estimates]

Inputs: the club pairs in §2 (+89.2 VC in all, +67.6 in the one big trade) and the §1 simulation. Rivals' VC in these units is NOT measured: the leaderboard shows only relative points. The score column is the simulation's mean at Saturday's pace / at 2×.

| Scenario at the close | VC on v10 | our points (1× / 2×) |
|---|---|---|
| Directive (all club deals on v10), everything executed | +89 | **4.8 / 3.9** |
| Directive, only the big trade executes | +68 | **4.4 / 3.2** |
| Directive, everything but the big trade | +22 | **2.0 / 1.1** |
| Rotation (the Chief's 22:52 question): half of the deals by count on v10, big trade elsewhere | +11 | **1.0 / 0.5** |
| Rotation, but the big trade on v10 and half of the rest | +78 | **4.6 / 3.5** |
| Club pairs + the outside pairs of §2, all on v10 | +149 | **5.0 / 4.8** |

- **By time, directive case:** if the big trade lands in the first hour, v10 holds +68, above the 50 needed after 1 h; by 12:00 the bar is about 100 and by the close 170 (2× case), so the +89.2 on the list is not enough by itself to stay at full marks all day: the want-lists have to add pairs.
- **A rotation over members' venues by count gives v10 about 1 point or less** unless the big trade settles on v10. The 22:55 directive (all club deals on v10) avoids that. If a rotation comes back, rotate by VC, not by count.
- **The big trade is a page finisher for Team 9** (-7.3 board vs us): the Chief's call.
- **Team 10** keeps full marks only while its VC is at least the top-three mean; it had 11 fills on Saturday and loses the 4 we made (§7).

## 7. Team 10's market (v07): who fed it on Saturday, and how to pull each [V counts from the feed]

v07 had 11 fills. Makers (whose offer was filled): Team 6 6, Team 5 4, Team 4 1. Takers: Team 14 3, Team 12 3, Team 3 1, Team 4 1, Team 9 1, Team 6 1, Team 13 1. Listings on v07: Team 8 204, Team 5 135, Team 6 104, Team 4 55, Team 13 19, Team 9 10, Team 16 8.

| Team | Role on v07 | How to pull it |
|---|---|---|
| Team 5 (us) | maker of 4 of its 11 fills | Stopped since 17:00 (Chief). Sunday: none of our offers on v07. That removes 4 of its 11 Saturday fills. |
| Team 6 | maker of 6 fills (bids for RET/LAT commons) | A rival with its own venue v01: do not recruit. Its bids are filled by sellers who look for the best bid; club sellers listing on v10 are not there to be found. |
| Team 8 | 204 listings on v07 | Club candidate: ask it to post on v10 instead of v07 (its bot sprays the same listings over several venues, so the venue looks like a setting on its side [L]). The biggest lever on v07's listing depth. |
| Team 4 | 55 listings, maker of 1 fill | Club candidate: same ask. |
| Teams 12, 14 (takers) | bought from v07's asks | Board-scanning bots: they follow the listings. No pitch; both are rivals. |
| Team 1 | reported ally of Team 10 | Not recruitable while that holds; the Market session's watch reports every t01 ↔ t10 trade and its venue. |

## 8. Pitch to Team 13 (draft; conflicts with the 22:55 directive, so the Chief decides first)

The Chief asked (22:52) for a pitch to Team 13 as a 7th member with its MAD RUSH venue in a rotation. The directive written three minutes later makes the club 5 teams with every club deal on v10, and Team 13 is on our fixed-rival list. Facts [V]: Team 13 has opened 4 venues in turn (v03, v22, v23, v24), each replacing the last, so it runs one at a time; it is one of the two heaviest listers (with Team 8); its market score is 6.77 against the free stall's 7.5; it is -5.5 board vs us.

> Hi Team 13! Straight numbers: your market shows less than a free stall on the board, and ours shows exactly the stall's number: neither of us is earning real-trades points. A venue only scores when two OTHER teams trade on it, and nobody routes to a venue just because it says "0% fee". A few of us are fixing that together: we share want-lists and spares, a matcher finds the pairs (a spare for a missing card, both sides gain), and the matched trades get posted where the club agrees. What we ask: your want-list and spare list tonight, and spares only, never a page card: one bad trade wipes a venue's score. In?

- The draft leaves the venue open on purpose. Under the directive the deals go on v10 and Team 13 gets the club's perks (card search, alerts, swaps), not a venue in a rotation. If the Chief wants the rotation, add: "your venue is in the rotation from the first hour".

