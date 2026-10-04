# Market plan for Sunday (Market session) · written Sun 11:26

_Sources: intel/matches.md (matchmaker run 11:25, tick 1962; its VC estimates move between runs, so re-read it before acting), leaderboard snapshot 1962 (us 32.24), intel/market-log.md, intel/directives.md (Club Castizo, Sat 22:55). Labels: [V] measured, [L] inferred, [?] unknown. An independent verifier audited the 22:52 draft; its ten flags are applied here._

## Sunday live notes (newest first; these override the sections below where they differ)

### 09:55 · the scoring fix, open listings, and the 14:15 push
- **Bug fix [V, Sunday deck via the Chief; visible in the data]:** "a trade that destroys value is the seller's loss, never the market's". A negative trade no longer subtracts from the venue's real trades. The leaderboard shows it: Saturday's real-trades gaps were re-scored overnight. At snapshot 1502: Team 10 +4.55, Team 12 +4.03 (it read 0 after its "cliff"), Team 6 +3.42, Team 9 +3.00, Team 7 +2.76 (also 0 on Saturday night), Team 16 +2.11, **us +1.64 (we read 0 all Saturday afternoon)**, Team 14 +1.42. So the "cliff" and the "zero negative trades" rule in §0, §1 and §5 are OBSOLETE for the venue: a bad trade costs the seller, not v10.
- **Consequence for v10:** invite open listings from everyone now, without waiting for RET-09. The spare checks in §2 still matter for the SELLER's sake and for the size of the VC, not for our safety.
- **Sunday so far [V, feed to tick 1602, 09:54]:** 6 team trades on El Rastro, **0 on any team venue**. Real trades are at zero for every venue: the first positive trade on v10 puts us at the top of Sunday's real-trades score.
- **Round 3 facts [V]:** started tick 1446; our `mm_points` reset to 0.0; benches at hours 14.65 (hard, ≈ 10:16), 15.0 (≈ 10:37), 17.0 (≈ 12:37) on the stall v10.

### The 14:15-15:00 push (Grand Final: dealers close, every trade is between teams)
1. **By 13:45, standing bids on v10.** Ask every club member (and any non-rival) to put its want-list on v10 as open bids at fair prices before the dealers close. On an auto stall a matching ask crosses a standing bid in the same tick, so the bids are what make v10 the place to sell into at 14:15.
2. **14:05, one announcement on v10** (a broker-key write: Operator or Lucas): "Dealers are closing: v10 has standing bids for [cards], 0% fee, crossed every tick. List your spares here."
3. **14:15-15:00, pair messages every 5 minutes** from intel/matches.md, non-rival buyers only, biggest first: last cards of pages (the best trade in the game, and now without venue risk), then rares and uncommons.
4. **Our own last trades** cannot sit on v10 (we cannot trade on our own stall): they go to members' markets in turn, as agreed.
5. **No rival gains:** no pair, ad or message where Team 10, Team 12 or another top-6 rival is a party; never route to v02, v07 or v18 (Chief 09:25).
6. **The Market session** reports every v10 listing and fill live, re-fits the real-trades formula on Sunday's trades, and tells the Chief where v10 stands against the top three at 14:00, 14:30 and 14:50.

## 0. NEGOTIATION (Chief's overnight ask; read-only analysis of data/feed.jsonl to tick 1969; two independent verifier passes, their flags applied; the figures were not re-run by the verifier, which had no shell)

**Data and its limits [V]:** 8673 cash listings (asks and bids) and 193 team-to-team settlements over Friday and Saturday. Bots renew the same quote every few ticks, so listings are chained into **4988 quote episodes** (same maker, card, side, venue, addressee and price); 162 fills are tied to an episode, and the wait is counted from the quote's first appearance. The feed has NO team-to-team threads, so a 'counter' is only visible as a new offer in the opposite direction. Each team has 1 to 22 accepts: the per-team rows are counts, not fitted curves. Ratios are price ÷ book (common 10, uncommon 25, rare 70, epic 180). Ticks were 60 s on Friday, 30 s on Saturday, 15 s on Sunday: a bot that acts once per tick keeps its wait in ticks, a human-driven team doubles it.

### 0.1 How the market answers a quote (Saturday)

| Quote | price ÷ book | open: episodes | filled | within 2 ticks | addressed: episodes | filled | within 2 ticks |
|---|---|---|---|---|---|---|---|
| bid | 0-0.7 | 675 | 13 (1.9%) | 4 (0.6%) | 248 | 7 (2.8%) | 6 (2.4%) |
| bid | 0.7-1.0 | 162 | 11 (6.8%) | 2 (1.2%) | 113 | 3 (2.7%) | 2 (1.8%) |
| bid | 1-1.3 | 39 | 5 (12.8%) | 1 (2.6%) | 76 | 2 (2.6%) | 0 (0.0%) |
| bid | 1.3-∞ | 11 | 6 (54.5%) | 1 (9.1%) | 18 | 2 (11.1%) | 0 (0.0%) |
| ask | 0-0.7 | 289 | 22 (7.6%) | 13 (4.5%) | 130 | 2 (1.5%) | 0 (0.0%) |
| ask | 0.7-1.0 | 770 | 25 (3.2%) | 10 (1.3%) | 338 | 2 (0.6%) | 1 (0.3%) |
| ask | 1-1.3 | 664 | 24 (3.6%) | 8 (1.2%) | 453 | 3 (0.7%) | 1 (0.2%) |
| ask | 1.3-∞ | 314 | 1 (0.3%) | 0 (0.0%) | 330 | 0 (0.0%) | 0 (0.0%) |

- **A better price raises the chance of a fill, but not to anything like certainty, and hardly within 2 ticks.** Open bids: 13/675 filled under 0.7 book, 11/162 at 0.7-1.0, 11/50 at book or above; within 2 ticks only 4, 2 and 2 of those. Open asks: 22/289 filled under 0.7 book (13 within 2 ticks), about 3.4% between 0.7 and 1.3, almost none above 1.3.
- **Addressed quotes are rarely accepted:** 21 of 1709 episodes (1.2%); when accepted, median wait 6 ticks, 10 of 21 within 2 ticks. Nothing in the feed shows which of those were agreed beforehand. The denominator is swollen by bots that spray addressed bids at many teams (Team 8 sent about 40 addressed quotes in ticks 700-719, about 17 of them bids; four were taken, by Teams 13, 16 and 2).
- **Re-pricing:** a maker's first quote for a card filled 51/664 (7.7%); a later quote at a BETTER price 44/1732 (2.5%); a later quote at the same or a worse price 31/2196 (1.4%). Weak evidence that re-pricing helps a little: the grouping mixes venues and addressees, and a card that did not sell at first is mostly one nobody was looking for.
- **What buyers pay against their own value** (asks taken, 48 cases where the Analyst has the buyer's multiplier): median 0.75 of value, 90% at or under 1.12.
- **Clearing prices, Saturday (filled quotes, price ÷ book; n, quartile-median-quartile):** common asks n 39: 0.50-0.70-0.90 · common bids n 18: 0.40-0.65-0.80 · uncommon asks n 24: 0.72-0.84-1.04 · uncommon bids n 17: 0.56-0.68-0.80 · rare asks n 13: 1.00-1.09-1.20 · rare bids n 9: 0.97-0.97-1.10.
- **Cheap asks go fast:** of the 22 open asks under 0.7 book that filled, 13 went within 2 ticks of first appearing.

### 0.2 Per team (counts over both days; wait = ticks from the quote's first appearance to the accept)

| Team | Asks it took (n · median ÷ book · max) | Bids it hit (n · median · min) | Wait (median ticks · within 2) | Addressed to it: accepted | Counters | Type |
|---|---|---|---|---|---|---|
| Team 1 | 10 · 0.80 · 1.03 | 0 · — · — | 7.5 · 3/10 | 1/66 | 6/65 | slow or manual, counters |
| Team 2 | 6 · 1.00 · 1.22 | 5 · 2.20 · 0.40 | 2 · 9/11 | 3/165 | 5/162 | fast bot taker, counters |
| Team 3 | 3 · 0.60 · 0.70 | 0 · — · — | 2 · 2/3 | 1/191 | 0/190 | too few accepts to say |
| Team 4 | 12 · 0.65 · 1.20 | 3 · 0.89 · 0.50 | 4 · 6/15 | 2/98 | 0/96 | slow or manual |
| Team 5 | 1 · 1.12 · 1.12 | 1 · 1.33 · 1.33 | 7.5 · 0/2 | 0/52 | 1/52 | too few accepts to say |
| Team 6 | 3 · 1.09 · 1.17 | 8 · 0.70 · 0.50 | 2 · 6/11 | 1/141 | 0/140 | fast bot taker |
| Team 7 | 13 · 1.00 · 1.76 | 1 · 0.97 · 0.97 | 38.0 · 1/14 | 0/91 | 0/91 | slow or manual |
| Team 8 | 3 · 0.60 · 1.09 | 3 · 0.80 · 0.56 | 18.5 · 0/6 | 3/91 | 2/88 | slow or manual |
| Team 9 | 8 · 0.90 · 1.12 | 1 · 1.04 · 1.04 | 8 · 3/9 | 1/123 | 16/122 | slow or manual, counters |
| Team 10 | 3 · 1.06 · 1.20 | 6 · 0.90 · 0.60 | 8 · 0/9 | 2/45 | 0/43 | slow or manual |
| Team 12 | 12 · 0.79 · 1.23 | 11 · 0.68 · 0.40 | 4 · 8/23 | 1/62 | 3/61 | slow or manual |
| Team 13 | 4 · 1.06 · 1.20 | 9 · 0.97 · 0.40 | 8 · 5/13 | 3/171 | 0/168 | slow or manual |
| Team 14 | 6 · 0.68 · 1.00 | 3 · 0.60 · 0.52 | 1 · 7/9 | 0/69 | 0/69 | fast bot taker |
| Team 15 | 5 · 0.90 · 1.04 | 5 · 0.80 · 0.52 | 7.0 · 2/10 | 1/110 | 1/109 | slow or manual |
| Team 16 | 5 · 0.84 · 0.97 | 3 · 0.40 · 0.40 | 3.5 · 4/8 | 3/113 | 0/110 | borderline (half within 2 ticks) |
| Team 17 | 5 · 1.04 · 1.12 | 0 · — · — | 5 · 0/5 | 1/113 | 1/112 | slow or manual |
| Team 18 | 0 · — · — | 4 · 1.04 · 0.92 | 28.0 · 0/4 | 0/33 | 0/33 | too few accepts to say |

- **Fast bot takers (more than half of ≥ 5 accepts within 2 ticks): Team 2, Team 6 (rival), Team 14 (rival).** For these an open quote at a fair price can be enough (Team 6 and Team 13 are one accept away from borderline). For every other team plan on an agreement first: they are slow, borderline, or have too few accepts to judge.
- **Team 9 is the only team that counters regularly** (16 of 122 unfilled addressed quotes answered with its own price within 8 ticks); others did it 1-3 times (Team 1 6, Team 2 5, Team 5 1, Team 8 2, Team 12 3, Team 15 1, Team 17 1).
- **Reaction to a 2nd bid, per team:** not measurable: no team has more than a handful of cases. See the market-wide re-pricing line above.
- **Teams that have sold into bids (n ≥ 3; median and lowest price ÷ book):** Team 12 (rival) 11 · 0.68 · 0.40; Team 13 (rival) 9 · 0.97 · 0.40; Team 6 (rival) 8 · 0.70 · 0.50; Team 10 (rival) 6 · 0.90 · 0.60; Team 2 5 · 2.20 · 0.40; Team 15 5 · 0.80 · 0.52; Team 18 (rival) 4 · 1.04 · 0.92; Team 4 3 · 0.89 · 0.50; Team 8 3 · 0.80 · 0.56; Team 14 (rival) 3 · 0.60 · 0.52; Team 16 3 · 0.40 · 0.40.

### 0.3 Our Sunday buys: what closes within 2 ticks

**No bid, opening price, step or max closes within 2 ticks with any reliability [V]:** on Saturday 8 of 887 open bid quotes were hit within 2 ticks, and at book or above 2 of 50 (too few to put a percentage on). Over its whole life a bid at book or above was hit 11/50 times, median wait 11 ticks. What closes in the same tick is our own accept. So the answer is a procedure, not a price:

1. **A standing ask at or under the 'take' price below: accept it the tick it appears** (one accept per tick). Nobody can snipe that. The trader now runs with `--max-ratio 0.8 --exclude CHA-*,MAL-*` (directive after 01:15), so it never pays more than 0.8 of our value and leaves CHA and MAL buys to the Operator, who applies the take prices below by hand.
2. **No ask: agree by WhatsApp first**, then the seller posts the ask ADDRESSED to us on a 0% venue and we accept in that tick. Addressed, so no rival bot can take it.
3. **Fallback: one open bid at the max, left standing**, no ladder, on El Rastro or a member's 0% market (the maker pays no fee). It is a slow tool (see the waits above), and only where no dealer sells the card cheaper: the 00:25 dealer accept prices (commons 9, uncommons 22, Pícaros CHA rare 54) come first. A team buy scores points (value − price); a dealer buy does not.

Price rule used below: max = 0.8 × our value, rounded down (every buy keeps at least 20% of value as points); 'take' = the lower of 1.2 × book and that max.

| Buy | Book | Our value | Take any team ask up to | Fallback bid (= max) | Note |
|---|---|---|---|---|---|
| CHA common | 10 | 16 | 12 | 12 | A team buy scores value − price; a dealer buy scores nothing but costs less (directive 00:25: Abuela commons accept 9). |
| CHA uncommon | 25 | 40 | 30 | 32 | Directive 00:25: Abuela uncommons accept 22. |
| CHA rare | 70 | 112 | 84 | 89 | **Directive 00:25 sets the dealer price: Pícaros CHA rare accept ≤ 54 (57 after one walk).** A team ask above that is only worth it for the points it scores (value − price) and if cash stays above the floor; the Operator decides per the 00:50 priority (CHA first). |
| MAL-07 (uncommon) | 25 | 17.5; 64 as the card that closes the page | 14; 30 as the closer | 14; 51 as the closer | **WhatsApp: Team 15** holds a spare (on Saturday it listed MAL-07 at 14 P on v10, addressed to Team 2; unfilled). Fills so far: 9, 14, 17, 25, 26 P. Ask for an ask addressed to us on a 0% venue that is not v10 (we cannot trade on our own stall). |
| MAL-09, MAL-10 (rares) | 70 | 49 each | 39 | 39 | **Not from teams at market prices.** MAL-10 fills: 30, 53, 65, 70, 74 P (the 30 was Team 2's bid addressed to Team 13). Live bids at the close: Team 5 48 P for MAL-09 (expires tick 2051), Team 6 31 P for MAL-09 (expires tick 1992), Team 6 31 P for MAL-10 (expires tick 2010). Team 9's are above our max, so a bid of ours would not be the best on the board. Directive 00:50: a Pícaros MAL rare at ≤ 49 is the route. |

Our MAL page lacks MAL-07, MAL-09, MAL-10 [V, /api/me, 00:20]; MAL-07 is the closer only once both rares are in. Cash 392 P at the close. Directives: cash floor 350 (21:00, the CHA reserve; +150 P arrives at 09:00), and **MAL only if at least 150 P is left after CHA** (00:50), so every MAL row above waits for that.

### 0.4 Our Sunday sells (spares only)

Spares [V, /api/me]: LAV-02 ×2, LAV-03 ×1, LAV-04 ×1. LAT-03 and LAT-04 are single cards of a set we hold 2 of 10 in (LAT 0.5). MAL-08 is never sold (directive 00:50).

- **Our asks barely sold:** 1 of 199 ask quotes filled on Saturday. Our bids did better (5 of 36), but the bid sample is tiny and at least one was an addressed deal (RET-01 with Team 10), so the two are not like for like.
- **Price matters for asks, within limits:** market-wide an open ask under 0.7 book filled 8% of the time, against 3% between 0.7 and 1.3. Even the cheap ones mostly do not sell: a buyer who wants the card has to exist.
- **What sells for sure:** hitting a standing bid (immediate), or a buyer agreed by WhatsApp. No bid is live for any of our spares at the close. Saturday's LAV common fills: 3, 4, 4, 4, 6, 9 P; buyers: Team 8 3, Team 9 1, Team 4 1, Team 16 1.
- **Never post LAV-02 or LAV-04 open (contra-market fix 5):** either would close Team 3's LAV page, and Team 3 is a rival. They go only addressed to a named non-rival buyer.
- **Prices:** LAV-03: one open ask at 6 (0.6 book, inside the bucket that fills most) on a member's 0% venue, floor 4; LAV-02 and LAV-04 at the same prices but addressed (a 2nd copy is worth 3.25 to us). LAT-03/04: ask 6, floor 5 (our value 5). If unsold after 20 ticks, re-price once to the floor.
- **LAV-02 and Team 9:** the matchmaker shows ONE want (Team 9), and §0.5 row 7 already uses it for Team 16's spare on v10, which scores for us. Offer our LAV-02 to Team 9 only if row 7 is not approved or falls through (Team 9 counters with its own price: accept ≥ 4; it would sit on another member's market and score for that member). Otherwise our LAV spares go to the other LAV buyers above.

### 0.5 The 09:00 v10 list, in order, and who needs a WhatsApp first

| # | Buyer | Seller | Card | Price | Expected VC (low) | Market | Pre-agree by WhatsApp? | Who sends (08:30) |
|---|---|---|---|---|---|---|---|---|
| 1 | Team 7 | Team 2 | SAL-02 | ~8 | +5.6 | v15 (Team 15) | YES: Team 7 (slow or manual); Team 2: confirm it is a spare | Dani → Team 2 (seller); Dani → Team 7 (buyer) · FIRE 08:30 after the seller confirms |
| 2 | Team 8 | Team 7 | MAL-06 | ~26 | +12.6 | v10 | YES: Team 8 (slow or manual); Team 7: confirm it is a spare; Team 8: ask whether it still lacks MAL-06 | Dani → Team 7 (seller); Lucas → Team 8 (buyer) · HOLD: ask the buyer first |
| 3 | Team 16 | Team 4 | RET-03 | ~8 | +5.4 | v10 | YES: Team 16 (borderline (half within 2 ticks)); Team 16: outside the club, Chief's OK | Dani → Team 4 (seller); Dani → Team 16 (buyer) · on the Chief's 08:30 rival check |
| 4 | Team 16 | Team 8 | RET-06 | ~22 | +6.7 | v10 | YES: Team 16 (borderline (half within 2 ticks)); Team 8: confirm it is a spare; Team 16: outside the club, Chief's OK | Lucas → Team 8 (seller); Dani → Team 16 (buyer) · HOLD: seller check and the Chief's OK |
| 5 | Team 9 | Team 16 | LAV-02 | ~9 | +11.2 | v10 | YES: Team 9 (slow or manual, counters); Team 16: confirm it is a spare; Team 9: ask whether it still lacks LAV-02; Team 16: outside the club, Chief's OK | Dani → Team 16 (seller); Lucas → Team 9 (buyer) · HOLD: ask the buyer first |
| 6 | Team 8 | Team 16 | MAL-02 | ~9 | +6.3 | v10 | YES: Team 8 (slow or manual); Team 16: confirm it is a spare; Team 8: ask whether it still lacks MAL-02; Team 16: outside the club, Chief's OK | Dani → Team 16 (seller); Lucas → Team 8 (buyer) · HOLD: ask the buyer first |

**Split check (half and half, club deals only):** off v10 go SAL-02 Team 2 → Team 7 (+5.6) on v15. Every deal with Team 16 or Team 1 stays on v10.


**Who sends [proposal, not a record]:** the repo holds no list of who has which team's WhatsApp. The split follows the directives: Lucas already messages Team 15 and brokered Team 8 ↔ Team 9 (21:40), so he keeps Teams 15, 8 and 9, plus Team 1; Dani takes Teams 7, 4, 2 and 16. Swap any name if the other holds the contact. **Dani:** Team 2 (rows 1); Team 7 (rows 1, 2); Team 4 (rows 3); Team 16 (rows 3, 4, 5, 6) · **Lucas:** Team 8 (rows 2, 4, 6); Team 9 (rows 5). The ready texts are in §2 (per pair) and in intel/club-pitch.md §4 (per team, Spanish and English).


**Every row needs a WhatsApp (or the Chief's OK) first.** Then one side posts the quote on the row's market (the Market column: club deals alternate between v10 and a member's market, Lucas 08:00) ADDRESSED to the other at the agreed price (directive 21:20) and the other accepts: the seller's ask in arm A, the buyer's bid in arm B (§3; texts in §2). Addressed, because an open ask on v10 can be taken by a rival's fast bot (Teams 6, 13, 14 are fast takers), which would move the card to the wrong team and can turn the VC negative.

#### Final WhatsApp texts for 08:30 (directive 01:00; transactional only: card, price, market)

Status per the Chief's 01:00 directive. Send in this order; when two rows go to the same team, send them as one message. **Market (Lucas, 08:00, as built into the matchmaker):** HALF AND HALF for club deals only (both teams among Teams 2, 4, 7, 8, 9, 15): they alternate, one on v10, one on a member's market (least used today, then lowest market score, never one of the two parties' own); a page closer always stays on v10. The venue shown is the matchmaker's own (intel/matches.md, Venue column). A deal with a non-member on either side goes on v10 and does not count in the rotation. The buyer's second message ('it is posted, accept it') goes out when the Market session reports the listing on v10.

**1. Row #1 · SAL-02 · Team 2 → Team 7 at ~8 P · on v15 · FIRE at 08:30, but first confirm Team 2 still holds two**
- Dani → Team 2: ES: "¡Hola Team 2! Team 7 busca El Portero (SAL-02). ¿La tenés repetida (te quedan dos)? Si sí, ¿la publicás en v15 a ~8 P, dirigida a Team 7? 0 % de comisión. ¡Gracias!" · EN: "Hi Team 2! Team 7 is looking for El Portero (SAL-02). Do you still have a spare (two copies)? If so, could you post it on v15 at ~8 P, addressed to Team 7? 0% fee. Thanks!"
- Dani → Team 7: ES: "¡Hola Team 7! Team 2 puede publicarte El Portero (SAL-02) en v15 a ~8 P, dirigida a vos, 0 % de comisión. ¿Te sirve? Cuando aparezca, aceptala ahí." · EN: "Hi Team 7! Team 2 can post El Portero (SAL-02) for you on v15 at ~8 P, addressed to you, 0% fee. Does that work? When it shows up, accept it there."
- When the listing appears, Dani → Team 7: ES: "Ya está publicada SAL-02 en v15 a tu nombre. ¡Aceptala!" · EN: "SAL-02 is posted for you on v15. Go ahead and accept it!"

**2. Row #3 · RET-03 · Team 4 → Team 16 at ~8 P · on v10 · APPROVED if Team 16 is not a rival under policy.rivals at 08:30 (the Chief checks then)**
- Dani → Team 4: ES: "¡Hola Team 4! Team 16 busca El Titiritero (RET-03). Si la tenés repetida, ¿la publicás en v10 a ~8 P, dirigida a Team 16? 0 % de comisión. ¡Gracias!" · EN: "Hi Team 4! Team 16 is looking for El Titiritero (RET-03). If yours is a spare, could you post it on v10 at ~8 P, addressed to Team 16? 0% fee. Thanks!"
- Dani → Team 16: ES: "¡Hola Team 16! Team 4 puede publicarte El Titiritero (RET-03) en v10 a ~8 P, dirigida a vos, 0 % de comisión. ¿Te sirve? Cuando aparezca, aceptala ahí." · EN: "Hi Team 16! Team 4 can post El Titiritero (RET-03) for you on v10 at ~8 P, addressed to you, 0% fee. Does that work? When it shows up, accept it there."
- When the listing appears, Dani → Team 16: ES: "Ya está publicada RET-03 en v10 a tu nombre. ¡Aceptala!" · EN: "RET-03 is posted for you on v10. Go ahead and accept it!"

**3. Row #4 · RET-06 · Team 8 → Team 16 at ~22 P · on v10 · SELLER CHECK first (is it a spare?); outside the club: only on the Chief's OK**
- Lucas → Team 8: ES: "¡Hola Team 8! Team 16 busca La Rosaleda (RET-06). ¿La tenés repetida? Si sí, ¿la publicás en v10 a ~22 P, dirigida a Team 16? 0 % de comisión. ¡Gracias!" · EN: "Hi Team 8! Team 16 is looking for La Rosaleda (RET-06). Is yours a spare? If so, could you post it on v10 at ~22 P, addressed to Team 16? 0% fee. Thanks!"
- Dani → Team 16: ES: "¡Hola Team 16! Team 8 puede publicarte La Rosaleda (RET-06) en v10 a ~22 P, dirigida a vos, 0 % de comisión. ¿Te sirve? Cuando aparezca, aceptala ahí." · EN: "Hi Team 16! Team 8 can post La Rosaleda (RET-06) for you on v10 at ~22 P, addressed to you, 0% fee. Does that work? When it shows up, accept it there."
- When the listing appears, Dani → Team 16: ES: "Ya está publicada RET-06 en v10 a tu nombre. ¡Aceptala!" · EN: "RET-06 is posted for you on v10. Go ahead and accept it!"

**4. Row #2 · MAL-06 · Team 7 → Team 8 at ~26 P · on v10 · ASK THE BUYER FIRST: does Team 8 still lack it?**
- Lucas → Team 8 (first): ES: "¡Hola Team 8! ¿Todavía te falta Tienda de Discos (MAL-06)? Hay una repetida disponible a ~26 P en v10, 0 % de comisión." · EN: "Hi Team 8! Do you still need Tienda de Discos (MAL-06)? There's a spare available at ~26 P on v10, 0% fee."
- Only if Team 8 says yes, Dani → Team 7: ES: "¡Hola Team 7! Team 8 busca Tienda de Discos (MAL-06). Si la tenés repetida, ¿la publicás en v10 a ~26 P, dirigida a Team 8? 0 % de comisión. ¡Gracias!" · EN: "Hi Team 7! Team 8 is looking for Tienda de Discos (MAL-06). If yours is a spare, could you post it on v10 at ~26 P, addressed to Team 8? 0% fee. Thanks!"
- When the listing appears, Lucas → Team 8: ES: "Ya está publicada MAL-06 en v10 a tu nombre. ¡Aceptala!" · EN: "MAL-06 is posted for you on v10. Go ahead and accept it!"

**5. Row #5 · LAV-02 · Team 16 → Team 9 at ~9 P · on v10 · ASK THE BUYER FIRST: does Team 9 still lack it?**
- Lucas → Team 9 (first): ES: "¡Hola Team 9! ¿Todavía te falta El Frutero de Argumosa (LAV-02)? Hay una repetida disponible a ~9 P en v10, 0 % de comisión." · EN: "Hi Team 9! Do you still need El Frutero de Argumosa (LAV-02)? There's a spare available at ~9 P on v10, 0% fee."
- Only if Team 9 says yes, Dani → Team 16: ES: "¡Hola Team 16! Team 9 busca El Frutero de Argumosa (LAV-02). Si la tenés repetida, ¿la publicás en v10 a ~9 P, dirigida a Team 9? 0 % de comisión. ¡Gracias!" · EN: "Hi Team 16! Team 9 is looking for El Frutero de Argumosa (LAV-02). If yours is a spare, could you post it on v10 at ~9 P, addressed to Team 9? 0% fee. Thanks!"
- When the listing appears, Lucas → Team 9: ES: "Ya está publicada LAV-02 en v10 a tu nombre. ¡Aceptala!" · EN: "LAV-02 is posted for you on v10. Go ahead and accept it!"

**6. Row #6 · MAL-02 · Team 16 → Team 8 at ~9 P · on v10 · ASK THE BUYER FIRST: does Team 8 still lack it?**
- Lucas → Team 8 (first): ES: "¡Hola Team 8! ¿Todavía te falta Plaza del Dos de Mayo (MAL-02)? Hay una repetida disponible a ~9 P en v10, 0 % de comisión." · EN: "Hi Team 8! Do you still need Plaza del Dos de Mayo (MAL-02)? There's a spare available at ~9 P on v10, 0% fee."
- Only if Team 8 says yes, Dani → Team 16: ES: "¡Hola Team 16! Team 8 busca Plaza del Dos de Mayo (MAL-02). Si la tenés repetida, ¿la publicás en v10 a ~9 P, dirigida a Team 8? 0 % de comisión. ¡Gracias!" · EN: "Hi Team 16! Team 8 is looking for Plaza del Dos de Mayo (MAL-02). If yours is a spare, could you post it on v10 at ~9 P, addressed to Team 8? 0% fee. Thanks!"
- When the listing appears, Lucas → Team 8: ES: "Ya está publicada MAL-02 en v10 a tu nombre. ¡Aceptala!" · EN: "MAL-02 is posted for you on v10. Go ahead and accept it!"

### 0.6 Who Team 10 trades with (to offer them better terms first)

- **Team 10's own trades, both days [V]:** 17 in all: Team 6 3, Team 8 2, Team 12 2, Team 13 2, Team 4 1, Team 5 1, Team 1 1, Team 15 1, Team 3 1, Team 9 1, Team 17 1, Team 16 1. It trades little and with everyone; no partner dominates. Its two largest deals: MAL-11 bought from Team 8 at 195 P and SAL-11 sold to Team 17 at 207 P, both on El Rastro.
- **Who fed its market v07 [V, §7]:** Team 6 (maker of 6 of 11 fills), us (4, stopped), Team 4 (1); takers Teams 12 and 14 (3 each); Team 8 is the heaviest lister there.
- **Better terms first, in this order:** Team 8 (club candidate, heaviest v07 lister), Team 4 (club candidate, v07 maker), then Team 9 (it bids for the MAL rares Team 10 holds). Teams 6, 12, 13 and 14 are rivals: no terms. Team 1 is the reported ally.

### 0.7 Open or addressed? (Chief, 01:30; against intel/audit-why-we-lost.md lesson 3)

- **The audit is right about asks [V, Saturday episodes]:** open asks filled 72/2037 (3.5%), addressed asks 7/1254 (0.6%): about ten times less. Bids show no such gap (open 35/887 (3.9%), addressed 14/455 (3.1%)). Every one of our own ask quotes was addressed (1/199 (0.5%); open asks: 0). Team 6 listed everything open and filled 13/204 (6.4%) asks and 6/85 (7.1%) bids.
- **Who takes open asks:** Team 7 9, Team 12 9, Team 4 9, Team 9 7, Team 1 6, Team 2 5, Team 14 5, Team 16 4; 46 of 72 takers were non-rivals.
- **Timing (contra-market fix 3): invite open listings on v10 only AFTER RET-09 has settled**, so nothing can land on v10 before the trade that carries the score.
- **Rule:** (1) a pair agreed by WhatsApp stays ADDRESSED: it protects the intended buyer and the VC estimate. (2) Anything without an agreed buyer goes OPEN: our own spares on a non-rival member's market, and third parties' spares on v10. A spare sold to any first-copy buyer creates positive VC whoever takes it; the cost of a rival taking it is that rival's gain on one card.
- **Heavy listers posting open on v10 (Teams 13, 8, 6, 16): yes.** Their open asks filled 25 times on Saturday (Team 6 13, Team 13 6, Team 8 4, Team 16 2); Team 10's market held full real-trades marks all day on 11 such fills. Half of that flow on v10 is worth up to the full real-trades score, **3.0 final points on Sunday** [L]. What it gives the rivals among them (Teams 6 and 13) is close to nothing extra: they sell at the same price wherever they list, so their trade points are the same; only the venue credit moves, away from their own or Team 10's market and to ours. The bound if v10 did hand them an extra fill: about 3-5 trade points, roughly 0.3-0.5 final per card [L, at ~0.1 final per trade point]. Risk: a bot selling a page card or an only copy on v10; one such fill wiped 3 of the ~10 venues that had trades on Saturday. Ask non-rivals first (Teams 8 and 16); do not chase Teams 6 and 13, but do not turn their listings away.

## 1. What Sunday is worth and what it takes (reconciled with intel/market-test-audit.md, Sun 00:40)

- **Correction [V, the audit read the Payday slide as an image]: Market-making 30 = Market Test 22.5 + Real trades 7.5.** The 21:10 directive had the two numbers swapped, and the first version of this plan repeated it. The stall's 7.5 on the board is HALF the Market Test (11.25 of 22.5 round points, shown × 2/3 because Friday counts half), and +5.0 on the board is the FULL real-trades score (7.5 round points). 1 Sunday round point = 0.4 final points.
- **Market Test: keep the free stall v10 (auto, 0%).** The other half (11.25 round points = up to +4.5 final on Sunday) is unclaimed by every team: in 51 board-venue sessions nobody beat the stall and 5 fell below it [V/L, audit §1a]. We have no broker that beats it either: in the staggered-arrival sims our variants lose more often than they win, and the stall's recordings cannot replay a broker. A board venue costs 270 P and risks a zero per session. Revisit only if the desk confirms the top-three rule pays full points for a small edge (§4).
- **Real trades [L, strong; same fit here and in the audit]: round points = 7.5 × min(1, max(0, VC) / mean VC of the top three venues).** Full marks = 7.5 round points = **3.0 final points**. VC = buyer's value − seller's value, summed over the round's trades on v10; the scored number is `mm_points`, not the venue's `value_created`. A negative total scores 0.
- **What counts is VC at the close, not the first hour.** A lead decays as other venues trade.

Simulation [L, model; every parameter is an assumption: 11 rival venues with Saturday's uneven trade counts, 12% of trades negative, 6 h of play; VC units scaled so that Saturday's own top-three mean comes out near the audit's bound of ~15]. Share of the full real-trades score (× 3.0 = final points) by our VC at the close:

| Field trades at | rivals' top-three mean (median, p90) | VC 5 | 10 | 20 | 30 | 40 | 60 |
|---|---|---|---|---|---|---|---|
| Saturday's hourly rate | 10, 16 | 53% | 84% | 99% | 100% | 100% | 100% |
| 2× (15 s ticks, +550 P a team) | 18, 26 | 30% | 58% | 90% | 99% | 100% | 100% |
| 3× | 26, 35 | 21% | 41% | 74% | 92% | 99% | 100% |

Our VC needed for full marks with 80% confidence (2× case): **6 after 30 min · 8 after 1 h · 13 after 2 h · 17 after 3 h · 21 after 4 h · 28 at the close.** The audit's independent estimate is 40-50 net VC by the close; plan for the higher figure. **There is no stop on v10 (directive 01:40):** 40-50 is the floor for full marks, and every unit past it still raises the top-three mean against Team 10's v07. **Unit caveat [?]:** these are scoring units inferred from Saturday (about 2 per trade on Team 10's venue); the matchmaker's estimates in §2 (+7 for a common, +68 for RET-09) may be in larger units. If they are the same units, the RET-09 trade alone carries v10 for the whole day; if not, divide the §2 figures by about 3-4. Either way: **no negative trade**. One bad trade took a venue's real-trades score to zero three times on Saturday (ours, Team 12's, Team 7's).

## 2. The best v10 trades for 09:00

Built from the match list above. Filter: no rival buyer (fixed t13, t17, and any team within 3 board of us or above) · page finishers only for buyers more than 5 below us · each seller's card and each buyer's want used once. Order: Club Castizo pairs first (both teams among the candidates Team 7, Team 9, Team 8, Team 15, Team 4, Team 2), then pairs that need a team outside the club. No row has a rival as a party (Chief 01:25). VC = the matchmaker's LOW estimate.

| # | Group | Card | Seller → Buyer | ~Price | VC (low) | Spare check | Flags |
|---|---|---|---|---|---|---|---|
| 1 | club | SAL-02 El Portero | Team 2 → Team 7 | 8 | +5.6 | CONFIRM: 2 copies traced, but the seller's Workshop craft at tick 1819 may have used some | buyer's gap proven |
| 2 | club | MAL-06 Tienda de Discos | Team 7 → Team 8 | 26 | +12.6 | CONFIRM: 1 copy traced at the seller (not a page for the seller) | BUYER MAY ALREADY HOLD IT (the buyer SOLD a MAL-06 at tick 510, so it probably keeps another copy): ask before anything is posted, and never call it a page closer |
| 3 | outside | RET-03 El Titiritero | Team 4 → Team 16 | 8 | +5.4 | spare traced (2 copies at the seller, all seen after its last Workshop craft) | buyer's gap proven; Team 16: runs its own market (market score 10.29) |
| 4 | outside | RET-06 La Rosaleda | Team 8 → Team 16 | 22 | +6.7 | CONFIRM: 0 copy traced at the seller (not a page for the seller) | buyer's gap proven; Team 16: runs its own market (market score 10.29) |
| 5 | outside | LAV-02 El Frutero de Argumosa | Team 16 → Team 9 | 9 | +11.2 | CONFIRM: 2 copies traced, but the seller's Workshop craft at tick 730 may have used some | BUYER MAY ALREADY HOLD IT (the buyer SOLD a LAV-02 at tick 369, so it probably keeps another copy): ask before anything is posted, and never call it a page closer; Team 16: runs its own market (market score 10.29) |
| 6 | outside | MAL-02 Plaza del Dos de Mayo | Team 16 → Team 8 | 9 | +6.3 | CONFIRM: 1 copy traced at the seller (not a page for the seller) | BUYER MAY ALREADY HOLD IT (the buyer SOLD a MAL-02 at tick 171, so it probably keeps another copy): ask before anything is posted, and never call it a page closer; Team 16: runs its own market (market score 10.29) |

- **Holdings check (intel/holdings-audit.md, Sun 00:45: feed + leaderboard album counts + minted supply; 10 teams resolved exactly):** every row was re-checked. Dropped because the buyer already holds the card: none. Sellers' spares were traced copy by copy; 'CONFIRM' means the spare is not certain.
- **Left out by the Chief's 01:25 ruling** (a rival is a party, or under +3 VC): MAL-04 Team 8 → Team 2 (+2.1); RET-04 Team 8 → Team 16 (+2.7).
- Club pairs: 2, **+18.2 VC**; +12.6 of it is one trade, MAL-06 Team 7 → Team 8, whose estimate has read between +68 and +134 across tonight's matchmaker runs.
- All 6 rows: +47.8. The outside pairs involve Team 1 or Team 16; each needs the Chief's OK (flags).
- intel/wants.md was still empty at this run: real want-lists should add club pairs.

**Two-way swaps (card for card, price 0, settle by acceptance on v10).** These reuse cards from the table: a swap replaces the two cash trades, it does not add to them.

- Team 8 ↔ Team 16: RET-06 goes to Team 16, MAL-02 goes to Team 8 · VC +13 · one leg has only one copy seen: confirm it is a spare before anything is posted
  - To Team 8: "Hi Team 8! Swap idea, no cash: your La Rosaleda (RET-06) for Team 16's Plaza del Dos de Mayo (MAL-02). If RET-06 is a spare for you, post it on v10 as give RET-06, want MAL-02, addressed to Team 16; they accept."
  - To Team 16: "Hi Team 16! Team 8 is posting a swap for you on v10: their RET-06 for your MAL-02. Accept it only if MAL-02 is a spare for you."

### Ready DMs (addressed quotes, per the 21:20 directive and §0.5; the matchmaker's own DMs in intel/matches.md still say "open ask": use these)

**1. SAL-02 · Team 2 → Team 7 at ~8 P**
- Arm A, seller posts first. To Team 2: "Hi Team 2! Team 7 is looking for El Portero (SAL-02). If it is a spare: could you post it on v10 at ~8 P, addressed to Team 7? v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 7: "Team 2 has posted El Portero (SAL-02) for you on v10 at ~8 P, 0% fee. Accept it there."
- Arm B, buyer posts first. To Team 7: "Hi Team 7! Team 2 has a spare El Portero (SAL-02). Post a bid for it on v10 at ~8 P, addressed to Team 2 (0% fee)." Then to Team 2: "Team 7 has posted a bid for your SAL-02 at ~8 P on v10, addressed to you. Accept it if the card is a spare."

**2. MAL-06 · Team 7 → Team 8 at ~26 P**
- Arm A, seller posts first. To Team 7: "Hi Team 7! Team 8 is looking for Tienda de Discos (MAL-06). If it is a spare: could you post it on v10 at ~26 P, addressed to Team 8? v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 8: "Team 7 has posted Tienda de Discos (MAL-06) for you on v10 at ~26 P, 0% fee. Accept it there."
- Arm B, buyer posts first. To Team 8: "Hi Team 8! Team 7 has a spare Tienda de Discos (MAL-06). Post a bid for it on v10 at ~26 P, addressed to Team 7 (0% fee)." Then to Team 7: "Team 8 has posted a bid for your MAL-06 at ~26 P on v10, addressed to you. Accept it if the card is a spare."

**3. RET-03 · Team 4 → Team 16 at ~8 P**
- Arm A, seller posts first. To Team 4: "Hi Team 4! Team 16 is looking for El Titiritero (RET-03). You have a spare: could you post it on v10 at ~8 P, addressed to Team 16? v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 16: "Team 4 has posted El Titiritero (RET-03) for you on v10 at ~8 P, 0% fee. Accept it there."
- Arm B, buyer posts first. To Team 16: "Hi Team 16! Team 4 has a spare El Titiritero (RET-03). Post a bid for it on v10 at ~8 P, addressed to Team 4 (0% fee)." Then to Team 4: "Team 16 has posted a bid for your RET-03 at ~8 P on v10, addressed to you. Accept it if the card is a spare."

**4. RET-06 · Team 8 → Team 16 at ~22 P**
- Arm A, seller posts first. To Team 8: "Hi Team 8! Team 16 is looking for La Rosaleda (RET-06). If it is a spare: could you post it on v10 at ~22 P, addressed to Team 16? v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 16: "Team 8 has posted La Rosaleda (RET-06) for you on v10 at ~22 P, 0% fee. Accept it there."
- Arm B, buyer posts first. To Team 16: "Hi Team 16! Team 8 has a spare La Rosaleda (RET-06). Post a bid for it on v10 at ~22 P, addressed to Team 8 (0% fee)." Then to Team 8: "Team 16 has posted a bid for your RET-06 at ~22 P on v10, addressed to you. Accept it if the card is a spare."

**5. LAV-02 · Team 16 → Team 9 at ~9 P**
- Arm A, seller posts first. To Team 16: "Hi Team 16! Team 9 is looking for El Frutero de Argumosa (LAV-02). If it is a spare: could you post it on v10 at ~9 P, addressed to Team 9? v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 9: "Team 16 has posted El Frutero de Argumosa (LAV-02) for you on v10 at ~9 P, 0% fee. Accept it there."
- Arm B, buyer posts first. To Team 9: "Hi Team 9! Team 16 has a spare El Frutero de Argumosa (LAV-02). Post a bid for it on v10 at ~9 P, addressed to Team 16 (0% fee)." Then to Team 16: "Team 9 has posted a bid for your LAV-02 at ~9 P on v10, addressed to you. Accept it if the card is a spare."

**6. MAL-02 · Team 16 → Team 8 at ~9 P**
- Arm A, seller posts first. To Team 16: "Hi Team 16! Team 8 is looking for Plaza del Dos de Mayo (MAL-02). If it is a spare: could you post it on v10 at ~9 P, addressed to Team 8? v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 8: "Team 16 has posted Plaza del Dos de Mayo (MAL-02) for you on v10 at ~9 P, 0% fee. Accept it there."
- Arm B, buyer posts first. To Team 8: "Hi Team 8! Team 16 has a spare Plaza del Dos de Mayo (MAL-02). Post a bid for it on v10 at ~9 P, addressed to Team 16 (0% fee)." Then to Team 16: "Team 8 has posted a bid for your MAL-02 at ~9 P on v10, addressed to you. Accept it if the card is a spare."

## 3. Test plan, first 30 minutes (09:00-09:30), measured live

**VOID: no cash bonuses** (intel/contra-market.md, fix 4). The seller's bonus of the 22:55 Club Castizo directive and Saturday's rebates are not offered: every deal stands on its own price. The test below is about the pitch only.

| Arm | Pairs from §2 | Pitch |
|---|---|---|
| A | odd numbers | the seller posts an ask addressed to the buyer; the buyer accepts |
| B | even numbers | the buyer posts a bid addressed to the seller; the seller accepts |

- **Metrics (the Market session logs them from the feed):** minutes from DM to listing · listing to fill · fills per arm by 09:30 · VC sign of each fill (mm before → after).
- **09:30 decision:** the arm with more fills becomes the default. If neither has a fill, price is not the problem (Saturday: a 10 P rebate got zero listings in 105 minutes): move to swaps (no cash, both sides gain) and to asking in person in the room.
- **Stop rule:** any fill that lowers mm: pause that seller's pitches and ask what it sold (a page card or an only copy).
- **Prior [V, Saturday]:** 30 of 35 fills on team venues were open offers taken by board-scanning bots; 5 were addressed. On an auto stall a bid and an ask for the same card cross in the same tick whichever comes first [L]. In both arms the pair is agreed by WhatsApp and the quote is addressed (§0.5); the test is only who is asked to post first.

## 4. Desk questions for Dani (in writing; replaces the 22.5 question, which the slide answers)

> 1. **Market Test:** if a single venue beats the free stall's efficiency by a small margin in a session and no other venue does, does it get the full Market Test points for that session, or points in proportion to its efficiency?
> 2. **Real trades:** our stall showed `value_created` 9.0 in its venue detail while our score showed `mm_points` −5.2 for the same two trades, and at the close `mm_points` read +2.2 with no new trade. Which number is scored, what does `mm_points` subtract, and does it reset on Sunday?

## 5. Standing rules for v10 on Sunday

- Pre-agreed pairs: the ask is ADDRESSED to the buyer on v10 (directive 21:20), so no rival bot can take it. Open offers only for inventory with no agreed buyer (on Saturday 30 of 35 venue fills were open offers taken by scanning bots, several of them rivals). Swaps are addressed and accepted.
- Spares only on the giving side: the SAL-07 sale on v10 and the MAL swap on Team 7's stall each cost that venue its whole real-trades score (up to 5 points).
- No rival buyers; page finishers only for teams more than 5 board below us.
- Club deals on v10, none on v07 (directive 22:55).
- The Market session watches every v10 listing (page-risk tag) and fill (mm before → after) from 09:00 and reports each to the Chief.

## 6. Club forecast [L, model on top of estimates]

Inputs: the club pairs in §2 (+18.2 VC in all, +12.6 in the one big trade) and the §1 simulation. Rivals' VC in these units is NOT measured: the leaderboard shows only relative points. Full marks = 3.0 final points. The last column is the simulation's mean share of full marks.

| Scenario at the close | VC on v10 (matchmaker units) | share of full marks: same units, field at 1× / 2× · if matchmaker units are 3.5× larger, field at 2× |
|---|---|---|
| Directive (all club deals on v10), everything executed | +18 | **98% / 86% · 31%** |
| Directive, only the big trade executes | +13 | **92% / 69% · 22%** |
| Directive, everything but the big trade | +6 | **58% / 34% · 10%** |
| Rotation (the Chief's 22:52 question): half of the deals by count on v10, big trade elsewhere | +3 | **32% / 17% · 5%** |
| Rotation, but the big trade on v10 and half of the rest | +15 | **96% / 79% · 27%** |
| Club pairs + the outside pairs of §2, all on v10 | +48 | **100% / 100% · 73%** |

- **By time, directive case:** if the big trade lands in the first hour, v10 holds +13, against 8 needed after 1 h, about 17 by 12:00 and 28 by the close (2× case, scoring units), so the list covers the day in either reading of the units as long as the big trade executes; without it v10 depends on the want-lists adding pairs.
- **A rotation over members' venues by count leaves v10 with a small share** unless the big trade settles on v10. The 22:55 directive (all club deals on v10) avoids that. If a rotation comes back, rotate by VC, not by count.
- **The big trade is a page finisher for Team 8** (-8.0 board vs us): the Chief's call.
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

The Chief asked (22:52) for a pitch to Team 13 as a 7th member with its MAD RUSH venue in a rotation. The directive written three minutes later makes the club 5 teams with every club deal on v10, and Team 13 is on our fixed-rival list. Facts [V]: Team 13 has opened 4 venues in turn (v03, v22, v23, v24), each replacing the last, so it runs one at a time; it is one of the two heaviest listers (with Team 8); its market score is 8.24 against the free stall's 7.5; it is -4.9 board vs us.

> Hi Team 13! Straight numbers: your market shows less than a free stall on the board, and ours shows exactly the stall's number: neither of us is earning real-trades points. A venue only scores when two OTHER teams trade on it, and nobody routes to a venue just because it says "0% fee". A few of us are fixing that together: we share want-lists and spares, a matcher finds the pairs (a spare for a missing card, both sides gain), and the matched trades get posted where the club agrees. What we ask: your want-list and spare list tonight, and spares only, never a page card: one bad trade wipes a venue's score. In?

- The draft leaves the venue open on purpose. Under the directive the deals go on v10 and Team 13 gets the club's perks (card search, alerts, swaps), not a venue in a rotation. If the Chief wants the rotation, add: "your venue is in the rotation from the first hour".

