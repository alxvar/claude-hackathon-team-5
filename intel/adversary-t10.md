# Adversary file: Team 10 (Sun 00:50, adversarial strategist, no prior context, read-only)

_Sources: bazaar-kit/RULES.md; intel/GAME.md, chief-handoff.md, sunday-plan.md, directives.md (top), teams.md, rivals.md,
score-model.md §4-5, market-sunday.md §0.6 and §7, market-test-audit.md, audit-why-we-lost.md, dealer-lab-ladder.md, club-pitch.md;
data/leaderboard.jsonl (last snapshot, tick 1440); data/feed.jsonl (all 62 t10 settlements, 470 t10 listings, 54 v07 ads, 191 t10
dealer threads on Fri+Sat, t10 eggs, gifts and packs). Checked by an independent verifier (13/13 claims and the arithmetic PASS; its
8 flags are fixed below). No keyed calls. Labels: **[V]** read from the feed or board, **[L]** inferred, **[?]** open.
Times are relative: **T0** = round 3 starts (CHA released, +150 P), **D3** = Duels III starts, **F** = the Final. The Operator turns them
into wall times at 08:55 (`/api/clock` `round`, `/api/schedule`); the files disagree (jump: T0 09:00, D3 ≈ 10:00, F ≈ 11:30; resume:
T0 ≈ 10:40; the 23:25 schedule read: D3 ≈ 11:00, dealers close ≈ 14:00)._

## 0. Bottom line

- **The lead is wide [V board 1440].** On 0.5·Fri + Sat, t10 has 56.37. Behind it: t18 46.89 (−9.48), us 45.73 (−10.64), t12 45.63,
  t03 44.51, t06 43.14. In final points (÷ 2.5) t10 is ≈ 4.3 ahead of us. It keeps #1 unless its Sunday round falls ≈ 10 points below
  the best rival's. It could lose its whole v07 market (7.5) and still win.
  - Our P(#1) stays low: ≤ 4% in every variant per standings.md, ≤ 9% in score-model's best case (t10 loses its VC) [L]. The
    moves below cost little and also decide the #2-#5 race, where four teams sit within 1.5 final points.
- **Top threats from t10 [L]:**
  1. Its v07 ad bot turns our public footprint (dealer-thread topics, addressed offers) into "t05 is hunting X: list PUBLIC on v07"
     ads, with the pair matched in the same tick, while our club agrees deals on WhatsApp.
  2. A CHA flip into our public last-card bid, plus a fast first hour of round 3 from selling Saturday inventory (MAL-09/10/11,
     RET-11).
  3. v07 stays the top value-created venue, and its duelist stays ≈ 2-4 points better than ours.
- **Top counters:**
  1. **Pyramid routing:** make v10 the clear #1 value-created (VC) venue with 2-4 large pre-agreed trades. Then send the extra club
     deals to two member markets kept just below v10, so v07 drops out of the top-three mean.
  2. **Close CHA without paying t10:** dealers first, the last card agreed in advance and addressed, no open last-card bid.
  3. **Get the duelist to full strength** before D3.

## Part 1: Team 10's Sunday, from its side

### 1.1 Team 10's Saturday round (the base it defends)

| Part | t10 | Us | Label |
|---|---|---|---|
| Market Test (stall level) | 11.25 | 11.25 | V (market-test-audit §1) |
| Real trades (v07 value created) | **7.50** (full from tick 720 to the close) | ≈ 0 (≈ +2.2 board-relative at the close) | V / L |
| Duels | ≈ 9.2-11.5 | ≈ 6.9 | L (audit §2.1) |
| Team trades + ladder | ≤ 18 | ≈ 17.6 | L |
| **Saturday round** | **45.99** | 35.74 | V |

- A stall team that hits every cap scores 48.75, so t10 ran at 94% of the ceiling.
- Its edge is structural:
  - a board venue that hosted 11 fills [V];
  - a strong duelist (≈ +3.7 swing over us in 20 ticks of Duels II, 1240-1260 [V audit]);
  - a bot that keeps dealing. It made 26 deals after 18:32 on Saturday; we made 1 [V].

### 1.2 Team 10's Sunday plan, written as Team 10 would

> Goal: a Sunday round no worse than the best rival's minus 9. Keep variance low, fill every capped part early, never book a loss.

1. **Market.**
   - Keep v07 the #1 value-created venue. Run the ad bot every 20 ticks (the per-venue limit [V GAME.md]) and match whatever the
     public feed shows people hunting.
   - Our Saturday base was Team 6's public offers: its bids filled by t12 and t13, its asks bought by t14 (6 of 11 fills had t06
     as maker [V]). That needs no friends.
   - In round 3 the high-value flow is CHA, so host CHA pairs between other teams on v07.
2. **Fill the fresh trade cap in the first hour by selling inventory into round 3.** Cards bought in round 2 sell for new gains in
   round 3:
   - MAL-11: t01 and t17 bid ≈ 150 [V dealer-lab-ladder].
   - MAL-09 and MAL-10: t09 bids 56 each [V scout].
   - RET-11 to Pilar, who told us on Saturday "Vuelva el domingo con el Palacio de Cristal" (= RET-11) [V eggs.md tick 1373]. We
     bought RET-11 from the Pícaros 33 ticks later (1406) [V].
3. **Fill the fresh ladder early.** Take the best 3 deals per dealer in the first 90 minutes:
   - Pícaros → Pilar cycles if a fever is announced;
   - one Ernesto (L5) deal;
   - three flags on Pícaros lies if the flag cap resets per round [?].
4. **Duels.** Leave the duelist alone and keep trading through D3 and F. Our MAL-11 and SAL-11 team trades (ticks 1264, 1296)
   happened inside Duels II (1239-1431) [V].
5. **CHA, depending on our multiplier.**
   - Low (likely, §1.4 note): flip Pícaros rares at ≈ 50 to teams that hunt them. Our pattern [V]: the SAL-11 epic, bought from
     the Pícaros at 155 and sold to t17 at 207 within 29 ticks (+40 cash net of the 12 P El Rastro fee).
   - High: race for the page with bots and close it on a cheap team trade, as we closed RET (the last card, RET-03, from t06 for
     12 [V tick 1033]).
6. **Pages.** Close LAV or MAL with a team trade (+50) if one card is missing.
7. **Allies.**
   - t01 (reported ally; [?], one t10 ↔ t01 trade in the whole feed [V]).
   - t03, our main counterparty: 124 of our 470 listings were addressed to it [V].
8. **Never:**
   - book a loss (losses count in full);
   - sell a page card (Team 6 fell from #2 to #6 that way [V]);
   - trade on v10, where our SAL-07 sale cut Team 5's market to the stall (tick 398 [V]). Team 10 stopped listing on v10 after tick
     813 [V].

### 1.3 Predicted Team 10 actions, with timing

| # | When | Predicted action | P [L] | Evidence | Our tell |
|---|---|---|---|---|---|
| 1 | first tick → +10 min | The bot resumes and relists duplicate commons (LAT-02/04, SAL-01..05, RET-03, LAV-04/05) at 6-13 P, mostly addressed to t03, t17, t06, t14, t04 | 0.9 | 470 listings: 345 addressed, 396 on El Rastro [V] | `offer.listed` maker t10 |
| 2 | every 20 ticks from the open (5 min at 15 s) | v07 ads that name pairs it finds in the public feed. In round 3 they read like "CHA-09: t05 is hunting it at the dealers, tXX sells at YY: list PUBLIC on v07" | 0.85 | Ads at 1295-1355 named hunts by t05, t07 and t12 [V]. Everything in a dealer thread is public: the topic with team and card [V `thread.opened`], every message, and every dealer offer naming its card (e.g. Chato → t05 `card:LAT-10` at 97, tick 1371) [V `thread.message`]. Addressed offers are public too [V GAME.md] | `venue.announcement` v07 naming t05 or club members |
| 3 | T0 → T0+60 | Sells its Saturday inventory for fresh round-3 gains: MAL-11 ≈ 150 (t01/t17), MAL-09/10 ≈ 56 (t09), RET-11 to Pilar | 0.6 | Bought MAL-10 (585), MAL-09 (967), MAL-11 (1264) and RET-11 (1406); none sold [V]. Its MAL value is disputed: 0.5 per score-model, but paying 195 for MAL-11 implies ≥ 1.1 [?] | t10 asks for MAL-09/10/11; a t10 → Pilar RET-11 settlement |
| 4 | T0 → T0+90 | Fresh-ladder program: 3 negotiated deals per dealer, Pícaros ↔ Pilar cycles if a fever comes, one Ernesto deal | 0.8 | 191 dealer threads Fri+Sat, 175 of them on Saturday (Abuela 61, Pícaros 58, Chato 38, Pilar 30, Ernesto 4 over both days); 5 Pícaros → Pilar SAL round trips (1094-1327) [V] | `thread.opened` team t10 |
| 5 | T0 → T0+30 | CHA. Dealer threads for CHA within minutes. Low multiplier: asks to CHA hunters at 1.3-1.5× its cost within 15-30 min. High: open bids for CHA cards and fast takes of any cheap CHA ask | 0.75 (one of the two) | SAL-11 (epic): bought at 155 (1267), open ask 212 the same tick, addressed to t17 at 207 (1286), settled 1296 [V] | **Its first CHA offer: an ask means a seller (low multiplier), a bid means a collector** |
| 6 | first hour of round 3 | Three flags on Pícaros lies, if the cap resets per round | 0.5 | +0.46 and +0.88 board at 1080/1090 with no settlement ≈ 3 flags [L] | t10 board rises with no settlement |
| 7 | any time | Closes a page by team trade (+50 capped): LAV (LAV-01/03 never seen bought [L]) or MAL (would need MAL-07/08 back) | 0.4 | RET close at 1024-1033: dealer rares, then a 12 P team buy for the last card [V] | t10 bids for LAV-01/03/07 or MAL-07/08 |
| 8 | D3 → end, F | Duelist runs; trading continues through the duels | 0.95 | MAL-11 (1264) and SAL-11 (1296) team trades during Duels II (1239-1431) [V] | — |
| 9 | any time | Uses t01: sells MAL-11 or CHA to t01; t01 posts public offers on v07 | 0.3 | 1 trade t10 → t01 (tick 311), 8 t10 offers addressed to t01, t01 listed 7 on v07 [V]; the alliance itself is hearsay [?] | Any t10 ↔ t01 settlement and its venue |
| 10 | resume case: until round 3 | Keeps v07's broker up for the hard Market Test (14.65) and the 15.0 bench; few trades (Saturday caps full) | 0.8 | Saturday trade and ladder parts near their caps [L] | — |
| 11 | each Sunday bench | Its board broker beats the stall. If "full points to the top-three mean" is nonlinear, that is up to +11.25 Sunday points | 0.1 | 51 board-venue sessions, 0 above the stall [V market-test-audit]; no effect on our stall score | t10 market above the stall share after a bench |

**Note on t10's multipliers [L].**
- LAV ≥ 1.17 (it bid 205-210 for LAV-11, 6 times).
- MAL ≥ 1.1 if MAL-11 was a hold.
- RET high (it collected the page and bought the epic).
- SAL ≈ 0.9 and LAT low (it dumps both).

If LAV, MAL and RET take 1.6, 1.3 and 1.1, its **CHA is 0.5-0.7, which makes t10 a CHA seller and flipper, not a collector.** If MAL
is really 0.5, CHA could be high. Row 5's first offer settles it within about 30 minutes.

### 1.4 How Team 10 counters a closed 7-team club on v10 (ranked by likelihood × damage)

1. **It uses our information for free.** Its bot already reads the public feed (dealer-thread topics, dealer messages and offers,
   addressed offers) and turns it into pairs on v07 (row 2).
   - Damage: club pairs and our CHA hunt get advertised to every seller. Prices rise, and a public crossing offer on v07 is matched
     in the same tick, while our club runs on WhatsApp.
   - Likelihood: certain; the code exists.
2. **It barely needs our members.** Of v07's 11 Saturday fills [V]:
   - 4 were ours as maker (351, 404, 714, 760). They are already gone: we stopped trading on v07 at 17:00.
   - 2 more involved club members: t04 sold into our bid at 404, and t04 sold to t09 at 683.
   - The other 5 were Team 6 as maker (bids and asks) with the rivals t12, t13 and t14 on the other side.
   - Team 8 posted 204 listings on v07 for 0 fills.
   - So poaching members is a side show for t10. Its base is t06's offers plus rival takers, and the real counter is pushing v07
     out of the top-three VC venues (Part 3 #1).
   - It will still name t04 and t08 in ads, as it did at tick 1201 [V].
3. **It flips CHA into our bids (if its CHA is low).**
   - It cannot drain our dealer supply: each team gets its own hourly allotment [V RULES].
   - It can take copies other teams hold, and it can sell into a public last-card bid. Pícaros cost ≈ 50; our open last-card bid
     goes up to 168 for a rare (cha-plan). If its CHA value is 35, t10 nets ≈ +30-35 neg_points: −15 on the dealer leg, counted in
     full, then +50 capped on the sale. At a trade-part reference of N ≈ 125 that is ≈ 2.5 Sunday points [L].
4. **It raises its own VC with large third-party trades.** It hosts CHA and rare pairs on v07, so v07 stays at or above the
   top-three mean.
5. **It offers the same perks without a club.**
   - It buys members' duplicates on the members' own markets, which gives those markets VC: our pitch's "your market gets deals" hook.
   - It has cash, a bot and a "fair broker" record.
   - Medium-low likelihood.
6. **"Matching our prices at 0%" is no lever.** v07 and v10 are both at 0% [V: v10 fee 0 since tick 230]. The fight is over where
   the counterparties are, and over speed.
7. **It complains to the desk.**
   - The pitch: a closed club that excludes the top teams, plus any cash bonus, looks like feeding. RULES (Fair play): "when one
     team keeps handing another the whole value of their deals, those deals count for nothing until the organisers have looked."
     A club as such is not covered; lopsided deals or side payments would be.
   - Low likelihood, high damage. It only works if we pay bonuses or make lopsided deals.
8. **It sabotages v10 with negative-VC fills.**
   - Precedent: its SAL-07 sale to t15 on v10 at tick 398 took us from 12.5 to 7.5 for the rest of Saturday [V]; whether that was
     deliberate is [?].
   - A first-copy card listed cheaply on v10 is taken by a fast low-multiplier bot, and our VC goes negative.
   - It costs t10 a trade loss unless its trade part is already over the cap, in which case it is free.
   - Low likelihood, but it zeroes our round's real trades.

## Part 2: Pre-mortem. Team 5 finished Sunday at #5

Context [V board 1440]: #2-#6 sit within 3.75 game points (1.5 final). Any one cause below (3-7.5 Sunday points) is enough on its
own. Ranked by likelihood [L].

| # | Cause (how it happened) | Cost (Sunday pts) | Early-warning signal (who watches) | Prevention |
|---|---|---|---|---|
| 1 | **The clock jump squeezed everything.** CHA at 09:00, D3 ≈ 10:00, F ≈ 11:30, close ≈ 12:00. Three humans ran six jobs: the duelist started late, CHA buys collided with D3, and club deals were never posted | 5-10 | 08:55: `/api/clock` `round` = 3, or `/api/schedule` puts D3 before 10:15 (Operator). At T0+20: < 3 CHA cards held, or 0 club fills (Chief) | Decide the squeezed plan before 08:58: Aleks only duels (live at T0+30, before D3); Operator only the automated CHA book (45-min budget); Lucas and Dani only the **3 largest pre-agreed pairs**, posted in the first 10 min. Drop the MAL close and rebates. No re-planning after 09:00 |
| 2 | **Club flow went to v07 or nowhere.** Members' bots kept spraying El Rastro and v07, WhatsApp was too slow, and t10's bot matched the same cards on v07 in one tick | 5-7.5 (+ t10 keeps its 7.5) | At T0+30: < 2 club fills on v10; club members' `offer.listed` on v07; v07 ads naming club pairs (Market session) | Both sides of each pre-agreed pair post at the first tick, addressed on v10. Give each member a one-line config ("want-list bids and spare asks: v10"). Check each member's venue share every 30 min and drop members who don't route. **3 big pairs beat 20 small ones** |
| 3 | **CHA stalled at 8-9/10.** The last card was visible (an open bid, a dealer thread or a message naming it); flippers and other 1.6 teams priced it up, or only rivals held it | 3.6-8 | Rival CHA asks ≥ 1.4× the dealer list within 30 min of T0; our team bids unfilled after 20 ticks; a v07 ad saying "t05 hunting CHA-xx" (Operator) | Buy every non-last card from dealers in the first hour (our allotment, ≤ list = 0 neg + ladder). Choose the last card as **the one a club member holds**, agree it in advance on WhatsApp, and post it addressed. The last card never appears in any public place before that post: no open bid, no dealer thread, no message. If only t10 holds it, the Chief decides by target: for #2, buy; for #1, don't |
| 4 | **The duelist misread days or stalled.** Saturday's wave-1 day bug swung ≈ 3.7 points in 20 ticks | 3-8 | First wave: `missing_days`, a deal outside our limit, every opener on the same day, rounds ≥ 4, deal rate < 0.8, a timeout fallback firing (Aleks, Analyst) | duelist-audit must-dos: params baked in or checked at start, a timeout fallback (S2), 561 tests green, `--policy llm`. A human watches the first 4 duels. Kill switch: 2 out-of-limit deals → stop and restart on the safe config |
| 5 | **The field outran us while we idled.** On Saturday we made 1 deal after 18:32 while t10 made 26. The fresh round-3 trade and ladder references were set by teams that filled them first | 2-4 | Board flat or falling for 3 snapshots while t18, t12 and t03 rise; our round-3 deals < half of t10's by T0+90; empty L3-L5 ladder slots at T0+60 (Analyst) | Fresh ladder in the first 90 min (best 3 per dealer; buys ≤ list, sells above the opening bid). Keep a steady stream of zero-cash swaps. Add a deals-per-30-min line to STATUS |
| 6 | **A negative trade on v10.** A card moved to a lower-value holder (as at tick 398), or a rival dumped first copies on v10 into fast low-multiplier bots | 7.5 (floors at 0) | Any v10 settlement where the buyer dumps that set or the seller collects it; `mm_points` falling; rival asks appearing on v10 (radar) | Price open club bids on v10 at **duplicate value** (a first-copy holder won't fill them). Club sell-side on v10 addressed only. Build a positive VC buffer in the first hour. If a rival does it twice, tell the desk; never retaliate |
| 7 | **Cash ran out, or losses counted in full.** Dealer finals above value, MAL chased alongside CHA, rebates; then no cash for the last card | 1-5 | Cash < 200 before CHA reaches 8/10; any `neg_points` drop after a buy; a dealer final above the accept cap taken; MAL buys before CHA ≥ 9/10 (Operator) | Bucket floors in code: CHA 330, last-card reserve 170 locked, MAL only after CHA ≥ 9/10 and ≥ 150 P left. Every buy must clear ΔV − price ≥ 0. No dealer buy above list |
| 8 | **The club was zeroed, or a guardrail broke.** Cash bonuses or lopsided deals triggered a fair-play review (possibly after a rival's complaint); or a bot sold a page card (−130; Team 6 fell from #2 to #6) | 7.5-9 | An organiser announcement on alliances; any club deal where one side's gain is ≥ 3× the other's; any `offer.listed` by t05 containing a reserved card (Chief, Operator) | **Zero cash bonuses** (club-pitch already proposes it). Every deal leaves both sides better off at their own values, written on the club page. The reserved list is enforced in code before every post |

## Part 3: Five counter-moves against Team 10 (legal: both sides of every trade gain at their own values, no feeding, no spam)

EV is in Sunday round points (× 0.4 = final) [L throughout].

### 1. Pyramid routing: v10 the clear #1, then two member markets just below it

- **Why it hits t10.** Real trades = 7.5 × min(1, VC_i / M), where M is the mean VC of the **top three venues** [L strong,
  market-test-audit §2].
  - If v10 is the top venue, M ≤ VC_v10, so we stay at full whatever M does.
  - t10's share is VC_v07 / M, so every member market that climbs above v07 raises M and pushes v07 below full, or out of the top
    three.
- **Example** (any units; only the ratios matter). v07 80, v10 200 and a third venue at 40 give M = 107, so t10 keeps 75% (−1.9).
  Add two members at 150 and 140: M = 163, so t10 keeps 49% (−3.8). We stay at 7.5 in both.
- **How.**
  - Fill v10 first with 2-4 big pre-agreed trades between non-rivals: RET-09 t07 → t09 (matchmaker estimate +67.6), and CHA
    rares from low-CHA holders to 1.6 collectors (≈ +60-80 each in the same units, more if the card completes a page). The
    matchmaker's units may be 3-4× the scoring units [? market-sunday §1]; the ranking of trades holds either way.
  - Once v10 holds ≥ 1.5× the next venue, send the extra club deals to the markets of **two** members (t09's v21 and t08's v06
    had real Saturday activity). Keep each one below v10.
  - This replaces club-pitch's "≤ ~30 VC per member market" guardrail, which protects us only while v10 is not on top.
- **Resume case.** Fire RET-09 in the first 30 min of the Saturday tail. It lifts our Saturday real trades toward the full 7.5
  (from ≈ 1-3). It cuts t10's Saturday share only if v10's VC passes ≈ 1.84 M. At the 1440 snapshot the top three were t10 at
  1.39 M, t06 at 0.94 M and t09 at 0.68 M, with M ≤ ≈ 15 scoring units [L market-test-audit §3b, score-model §3h]. So the bar is
  ≈ 28 scoring units or less, which RET-09 alone may clear if the matchmaker's +67.6 is even a quarter in scoring units [?].
- **EV:** us +5 to +7.5 per round; t10 −1.5 to −4 per round if executed. P(executed) ≈ 0.5, so ≈ +4-5 net against t10.
- **Owner:** Lucas and Dani (pairs), Market session (M tracking every snapshot).

### 2. Close CHA without paying t10

- **Steps.**
  - Every non-last card from dealers in the first hour, at ≤ list: Pícaros rares 48-54, Abuela commons ≤ 9 and uncommons ≤ 22.
    These score 0 neg and fill ladder slots.
  - Choose the last card by **who holds it**: a club member or a non-rival, agreed in advance and posted with `to`.
  - No open last-card bid, ever.
  - Accept that the hunt itself is public. Every dealer topic, message and offer is in the feed, naming the card [V], so the v07
    ad bot will see which CHA cards we buy from dealers. What can stay hidden is **the last card**: never open a dealer thread for
    it, never name it in any message, never bid for it openly. It surfaces only as the one addressed post agreed on WhatsApp.
    Buy the other cards fast, so the bot's ads come after we have filled them.
  - Never fill or accept a CHA offer from t10 or t01. If t10 is the only holder of the last card, the Chief decides as in Part 2 #3.
- **Why it hits t10:** it removes the buyer for t10's flips (row 5). A flip with no team buyer leaves t10 holding a dealer card
  above its value, a loss counted in full.
- **EV:** protects our +8-14 (sunday-plan) and denies t10 ≈ 2.5-3.6 per capped flip sale. ≈ +2-4 against t10.

### 3. Duelist at full strength before D3

- **Steps:** the Duel Lab FINAL params plus the guards, after duelist-audit's two must-dos (params check, timeout fallback). Then a
  canary on the first 4 duels, the kill-switch rule, and a live check by T0+30, whatever the clock case.
- **Why it hits t10:**
  - Duels are its other edge (≈ 30-40% of the lead [V audit §2]).
  - Every part is graded against the field: if we become the duel leader, t10's duel part is graded against us.
  - We meet t10, under an alias, in about 4 of the 68 Duels III duels and 2 of the 34 in the Final, and each pie is zero-sum.
- **EV:** ≈ +2.6-2.7 over Duels III and ≈ +1.3 over the Final [L Duel Lab], plus the relative effect.

### 4. Deny t10's round-3 fast start

- **Steps.**
  - No Team 5 trade with t10, or with t01 when the card is one t10 needs. That covers LAV-01/03/07, MAL-07/08 (MAL-08 is already
    never-sell) and any CHA.
  - Cancel the LAV-03 → t04 and LAV-04 → t01 asks at the first tick (the strategist already says so).
  - When the matcher finds a club member who wants a card t10 is selling (MAL-09/10 to t09, for example), offer that member a
    club or non-rival seller first, with a gain for both sides.
- **Why:** t10's easiest Sunday points are capped +50 trades in the first hour (row 3, row 7). Each one denied is ≈ 3.6 Sunday
  points it doesn't get [L, N ≈ 125].
- **EV:** small and uncertain (0 to −3.6 for t10; supply of commons is deep), but the cost is 0.

### 5. Make the club impossible to attack, and watch v10 every tick

- **Steps.**
  - Zero cash bonuses.
  - Every deal positive at both sides' own values, the rule written on the club page.
  - Open v10 bids priced at duplicate value only.
  - Every v10 settlement checked within one tick, with the buyer's and seller's multiplier.
  - If a rival injects negative VC on v10 twice, a factual note to the desk. Never retaliation, and never a trade on v07.
- **Why:** this shuts t10's two cheap counters, the fair-play complaint (§1.4 #7) and v10 sabotage (§1.4 #8). Each one would
  zero 7.5.
- **EV:** ≈ +1 (7.5 × P(incident) ≈ 0.15), and it protects counter 1.

**Cheap extra (not t10-specific).** In round 3, probe one flag on a clean Pícaros lie (words against structure, or a false fact)
**before** saying the estampita line. Whether flags reset per round is [?], and t10 probably harvests them (row 6). If they score,
3 flags = +30 neg ≈ +2 Sunday points [L].

**Outside the game.** t10's lead is ≈ 4.3 final points, and the judges award 40 after the close. The pitch is where #1 is decided
more than any trade [L: the judges' scale is unknown].

**Not doing:**
- no trades on v07, ever;
- no wash or round-trip trades to inflate v10;
- no paying members for flow;
- no false or bad-faith messages to t10 or its ally;
- no spam ads (v10 announcements stay within 1 per 20 ticks and stay factual);
- no sharing our scoring model with any team (memory: no-strategy-leaks-to-rivals).
