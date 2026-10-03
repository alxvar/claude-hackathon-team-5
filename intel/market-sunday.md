# Market plan for Sunday (Market session) · written Sat 22:50

_Sources: `intel/matches.md` (matchmaker, 22:47, tick 1410), leaderboard snapshot 1420 (us 30.49), `intel/market-log.md`. Labels: [V] measured, [L] inferred, [?] unknown. Regenerate: `python3 make_sunday.py` in the Market session's scratchpad._

## 1. What Sunday is worth and what it takes

- **Market Test: nothing to do [L].** The deck says Market Test = 7.5; every stall team already shows 7.5 after six benches and no venue has ever shown more than 7.5 + 5.0. Keep the free stall v10 (auto, 0%). No board venue: it adds only the broker-down risk.
- **Real trades [L, strong]: points = 5.0 × min(1, our VC / mean VC of the top three venues), floor 0.** Fitted on Saturday's snapshots to 0.01. VC = buyer's value − seller's value, summed over the round's trades on v10. Sunday is a new round, so our −5.2 should be gone [L].
- **What counts is VC at the close, not the first hour.** A lead decays as other venues trade.

Simulation [L, model: 11 rival venues with Saturday's trade mix, 12% of trades negative, 6 h of play]. Our score by VC at the close:

| Field trades at | rivals' top-three mean (median, p90) | VC 40 | 60 | 100 | 150 | 200 |
|---|---|---|---|---|---|---|
| Saturday's hourly rate | 60, 96 | 3.3 | 4.2 | 4.9 | 5.0 | 5.0 |
| 2× (15 s ticks, +550 P a team) | 108, 155 | 2.0 | 2.9 | 4.1 | 4.8 | 5.0 |
| 3× | 156, 213 | 1.4 | 2.1 | 3.2 | 4.3 | 4.8 |

VC needed for full marks with 80% confidence (2× case): **35 after 30 min · 50 after 1 h · 80 after 2 h · 100 after 3 h · 125 after 4 h · 170 at the close.** In trades: two big ones (a rare or a page finisher, +40 to +68) plus one common or uncommon first-copy trade every 30-40 minutes, and **no negative trade** (one wiped us, Team 12 and Team 7 on Saturday).

## 2. The 10 best v10 trades for 09:00

Filter: buyer is not a rival (fixed t13, t17, and any team within 3 board of us or above) · page finishers only for buyers more than 5 below us · tier A = seller shown holding 2+ copies, tier B = one copy seen (ask before posting), tier C = rival seller. One card per seller and buyer. VC = the matchmaker's LOW estimate.

| # | Tier | Card | Seller → Buyer | ~Price | VC (low) | Spare check | Flags |
|---|---|---|---|---|---|---|---|
| 1 | A | RET-09 El Ángel Caído | Team 7 → Team 9 | 70 | +67.6 | spare seen (2 copies) | PAGE FINISHER for Team 9 (-7.2 vs us) |
| 2 | A | RET-08 Palacio de Velázquez | Team 7 → Team 1 | 23 | +14 | spare seen (2 copies) | — |
| 3 | A | SAL-03 Perrito con Abrigo | Team 1 → Team 8 | 9 | +12.9 | spare seen (3 copies) | — |
| 4 | A | LAV-02 El Frutero de Argumosa | Team 16 → Team 9 | 9 | +11.2 | spare seen (2 copies) | — |
| 5 | A | SAL-05 Taxi Blanco | Team 8 → Team 7 | 9 | +7.9 | spare seen (4 copies) | — |
| 6 | A | SAL-01 Escaparate de Serrano | Team 1 → Team 7 | 9 | +7.8 | spare seen (3 copies) | — |
| 7 | A | RET-01 Barca del Estanque | Team 2 → Team 16 | 9 | +7.4 | spare seen (2 copies) | — |
| 8 | A | RET-03 El Titiritero | Team 4 → Team 16 | 9 | +7.1 | spare seen (2 copies) | — |
| 9 | A | SAL-02 El Portero | Team 9 → Team 7 | 9 | +6.5 | spare seen (2 copies) | — |
| 10 | A | MAL-04 El Tatuador | Team 1 → Team 2 | 4 | +2.8 | spare seen (2 copies) | — |

Sum of the 10: **+145.2 VC** (tier A alone: +145.2).

**Two-way swaps (card for card, price 0, settle by acceptance on v10):**

- Team 9 ↔ Team 7: RET-09 goes to Team 9, SAL-02 goes to Team 7 · VC +74.1 · DM to Team 7: "Hi Team 7! Swap idea, no cash: your spare El Ángel Caído (RET-09) for Team 9's spare El Portero (SAL-02). Post it on v10 as give RET-09, want SAL-02, addressed to Team 9; they accept. Only if RET-09 is a spare for you." · DM to Team 9: "Hi Team 9! Team 7 is posting a swap for you on v10: their RET-09 for your SAL-02. Accept it if SAL-02 is a spare for you."
- Team 1 ↔ Team 7: RET-08 goes to Team 1, SAL-01 goes to Team 7 · VC +21.8 · DM to Team 7: "Hi Team 7! Swap idea, no cash: your spare Palacio de Velázquez (RET-08) for Team 1's spare Escaparate de Serrano (SAL-01). Post it on v10 as give RET-08, want SAL-01, addressed to Team 1; they accept. Only if RET-08 is a spare for you." · DM to Team 1: "Hi Team 1! Team 7 is posting a swap for you on v10: their RET-08 for your SAL-01. Accept it if SAL-01 is a spare for you."
- Team 8 ↔ Team 1: SAL-03 goes to Team 8, RET-03 goes to Team 1 · VC +15 · DM to Team 1: "Hi Team 1! Swap idea, no cash: your spare Perrito con Abrigo (SAL-03) for Team 8's spare El Titiritero (RET-03). Post it on v10 as give SAL-03, want RET-03, addressed to Team 8; they accept. Only if SAL-03 is a spare for you." · DM to Team 8: "Hi Team 8! Team 1 is posting a swap for you on v10: their SAL-03 for your RET-03. Accept it if RET-03 is a spare for you."
- Team 7 ↔ Team 8: SAL-05 goes to Team 7, MAL-02 goes to Team 8 · VC +15.1 · DM to Team 8: "Hi Team 8! Swap idea, no cash: your spare Taxi Blanco (SAL-05) for Team 7's spare Plaza del Dos de Mayo (MAL-02). Post it on v10 as give SAL-05, want MAL-02, addressed to Team 7; they accept. Only if SAL-05 is a spare for you." · DM to Team 7: "Hi Team 7! Team 8 is posting a swap for you on v10: their SAL-05 for your MAL-02. Accept it if MAL-02 is a spare for you."

### Ready DMs (format B: seller's open ask first; see the test in §3)

**1. RET-09 · Team 7 → Team 9 at ~70 P**
- Seller-ask first, to Team 7: "Hi Team 7! Is your El Ángel Caído (RET-09) a spare? If yes, post it on v10 as an open ask at ~70 P: Team 9 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 9: "El Ángel Caído (RET-09) is on v10 at ~70 P, 0% fee. Accept it there."
- Buyer-bid first, to Team 9: "Hi Team 9! Post an open bid for El Ángel Caído (RET-09) at ~70 P on v10 (0% fee): Team 7 holds a spare and the stall crosses it the same tick." Then to Team 7: "There is a bid for RET-09 at ~70 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**2. RET-08 · Team 7 → Team 1 at ~23 P**
- Seller-ask first, to Team 7: "Hi Team 7! Is your Palacio de Velázquez (RET-08) a spare? If yes, post it on v10 as an open ask at ~23 P: Team 1 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 1: "Palacio de Velázquez (RET-08) is on v10 at ~23 P, 0% fee. Accept it there."
- Buyer-bid first, to Team 1: "Hi Team 1! Post an open bid for Palacio de Velázquez (RET-08) at ~23 P on v10 (0% fee): Team 7 holds a spare and the stall crosses it the same tick." Then to Team 7: "There is a bid for RET-08 at ~23 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**3. SAL-03 · Team 1 → Team 8 at ~9 P**
- Seller-ask first, to Team 1: "Hi Team 1! Is your Perrito con Abrigo (SAL-03) a spare? If yes, post it on v10 as an open ask at ~9 P: Team 8 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 8: "Perrito con Abrigo (SAL-03) is on v10 at ~9 P, 0% fee. Accept it there."
- Buyer-bid first, to Team 8: "Hi Team 8! Post an open bid for Perrito con Abrigo (SAL-03) at ~9 P on v10 (0% fee): Team 1 holds a spare and the stall crosses it the same tick." Then to Team 1: "There is a bid for SAL-03 at ~9 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**4. LAV-02 · Team 16 → Team 9 at ~9 P**
- Seller-ask first, to Team 16: "Hi Team 16! Is your El Frutero de Argumosa (LAV-02) a spare? If yes, post it on v10 as an open ask at ~9 P: Team 9 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 9: "El Frutero de Argumosa (LAV-02) is on v10 at ~9 P, 0% fee. Accept it there."
- Buyer-bid first, to Team 9: "Hi Team 9! Post an open bid for El Frutero de Argumosa (LAV-02) at ~9 P on v10 (0% fee): Team 16 holds a spare and the stall crosses it the same tick." Then to Team 16: "There is a bid for LAV-02 at ~9 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**5. SAL-05 · Team 8 → Team 7 at ~9 P**
- Seller-ask first, to Team 8: "Hi Team 8! Is your Taxi Blanco (SAL-05) a spare? If yes, post it on v10 as an open ask at ~9 P: Team 7 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 7: "Taxi Blanco (SAL-05) is on v10 at ~9 P, 0% fee. Accept it there."
- Buyer-bid first, to Team 7: "Hi Team 7! Post an open bid for Taxi Blanco (SAL-05) at ~9 P on v10 (0% fee): Team 8 holds a spare and the stall crosses it the same tick." Then to Team 8: "There is a bid for SAL-05 at ~9 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**6. SAL-01 · Team 1 → Team 7 at ~9 P**
- Seller-ask first, to Team 1: "Hi Team 1! Is your Escaparate de Serrano (SAL-01) a spare? If yes, post it on v10 as an open ask at ~9 P: Team 7 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 7: "Escaparate de Serrano (SAL-01) is on v10 at ~9 P, 0% fee. Accept it there."
- Buyer-bid first, to Team 7: "Hi Team 7! Post an open bid for Escaparate de Serrano (SAL-01) at ~9 P on v10 (0% fee): Team 1 holds a spare and the stall crosses it the same tick." Then to Team 1: "There is a bid for SAL-01 at ~9 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**7. RET-01 · Team 2 → Team 16 at ~9 P**
- Seller-ask first, to Team 2: "Hi Team 2! Is your Barca del Estanque (RET-01) a spare? If yes, post it on v10 as an open ask at ~9 P: Team 16 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 16: "Barca del Estanque (RET-01) is on v10 at ~9 P, 0% fee. Accept it there."
- Buyer-bid first, to Team 16: "Hi Team 16! Post an open bid for Barca del Estanque (RET-01) at ~9 P on v10 (0% fee): Team 2 holds a spare and the stall crosses it the same tick." Then to Team 2: "There is a bid for RET-01 at ~9 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**8. RET-03 · Team 4 → Team 16 at ~9 P**
- Seller-ask first, to Team 4: "Hi Team 4! Is your El Titiritero (RET-03) a spare? If yes, post it on v10 as an open ask at ~9 P: Team 16 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 16: "El Titiritero (RET-03) is on v10 at ~9 P, 0% fee. Accept it there."
- Buyer-bid first, to Team 16: "Hi Team 16! Post an open bid for El Titiritero (RET-03) at ~9 P on v10 (0% fee): Team 4 holds a spare and the stall crosses it the same tick." Then to Team 4: "There is a bid for RET-03 at ~9 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**9. SAL-02 · Team 9 → Team 7 at ~9 P**
- Seller-ask first, to Team 9: "Hi Team 9! Is your El Portero (SAL-02) a spare? If yes, post it on v10 as an open ask at ~9 P: Team 7 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 7: "El Portero (SAL-02) is on v10 at ~9 P, 0% fee. Accept it there."
- Buyer-bid first, to Team 7: "Hi Team 7! Post an open bid for El Portero (SAL-02) at ~9 P on v10 (0% fee): Team 9 holds a spare and the stall crosses it the same tick." Then to Team 9: "There is a bid for SAL-02 at ~9 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

**10. MAL-04 · Team 1 → Team 2 at ~4 P**
- Seller-ask first, to Team 1: "Hi Team 1! Is your El Tatuador (MAL-04) a spare? If yes, post it on v10 as an open ask at ~4 P: Team 2 is looking for it, and v10 is 0% (El Rastro takes 5% + 1 P)." Then to Team 2: "El Tatuador (MAL-04) is on v10 at ~4 P, 0% fee. Accept it there."
- Buyer-bid first, to Team 2: "Hi Team 2! Post an open bid for El Tatuador (MAL-04) at ~4 P on v10 (0% fee): Team 1 holds a spare and the stall crosses it the same tick." Then to Team 1: "There is a bid for MAL-04 at ~4 P on v10. If yours is a spare, post an ask at that price and it crosses at once."

## 3. Test plan, first 30 minutes (09:00-09:30), measured live

Question: which pitch gets a fill on v10 fastest. One variable at a time, 5 pairs per arm, pairs alternated down the list above so both arms get similar VC.

| Arm | Pairs | Pitch | Rebate |
|---|---|---|---|
| A | #1, #3, #5, #7, #9 | seller's open ask first, then tell the buyer | 10 P to the seller per fill |
| B | #2, #4, #6, #8, #10 | buyer's open bid first, then tell the seller | 10 P to the seller per fill |

- **Metrics (the Market session logs them from the feed):** minutes from DM to listing · listing → fill · fills per arm by 09:30 · VC sign of each fill (mm before → after).
- **09:30 decision:** the arm with more fills becomes the default for the rest of the list. If neither has a fill, the price is not the problem (Saturday: a 10 P rebate got zero listings in 105 minutes): switch to swaps (no cash, both sides gain) and to in-person asks in the room.
- **Rebate size test, 09:30-10:00:** only if arm A or B produced listings but no fills: raise to 20 P on the three largest-VC pairs. Never pay for a card that is not a spare.
- **Stop rule:** any fill that lowers mm → pause the pitch for that seller and ask what it sold (page card or only copy).
- **Why seller-ask is my prior [V, Saturday]:** 30 of 35 fills on team venues were open offers taken by board-scanning bots; only 5 were addressed. On an auto stall a bid and an ask for the same card cross in the same tick whichever comes first.

## 4. Desk question for Dani (in writing)

> On Saturday the best market on the leaderboard showed 12.5 = 7.5 (the Market Test) + 5.0. No venue showed more than +5.0 for real trades, and several sat at exactly +5.0 for hours. The Payday deck says real trades are worth 22.5. **What earns the full 22.5: is +5.0 a cap for Saturday, a share of the round, or does the scale change on Sunday?** Second question: our stall shows `value_created` 9.0 in its venue detail while our score shows `mm_points` −5.2 for the same two trades. **Which of the two is scored, and does a negative total subtract or stop at zero?**

## 5. Standing rules for v10 on Sunday

- Open offers, not addressed ones (addressed offers did not fill on Saturday), except swaps, which are addressed and accepted.
- Spares only on the selling side: both the SAL-07 sale on v10 and the MAL swap on Team 7's stall cost a whole day's score.
- No rival buyers; page finishers only for teams more than 5 board below us.
- The Market session watches every v10 listing (page-risk tag) and fill (mm before → after) from 09:00 and reports each to the Chief.

