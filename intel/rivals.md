# How Team 13 and Team 18 score, and what to copy (Builder, Sat 12:00; independently verified; now the Analyst's)

_Sources: `data/feed.jsonl` (settlements de-duplicated by id; Friday = ticks < 159), `/api/dealers` menus (Saturday's;
Friday deals are judged against them), the leaderboard (tick 420), our `/api/me` (11:50) and the hub's demand model
(`hub.team_mult`, run 124). **Estimates** ("est.") are book × multiplier − price at the hub's multipliers [L]. They
**ignore copy marginals** (a 2nd copy is worth 25%, a 3rd 10%) and page bonuses, so they are biased low on sales of
duplicates and on page closes. Example: our SAL-01 sale at 7 is est. −2.0 but measured **+4.7** [V]. Verified deltas
are used wherever they exist. Raw counts cross-check exactly with the leaderboard's deal counts (45 / 28 / 35)._

## Live (Analyst; newest first)

### Sun 10:56 · snapshot 1842 (phase 0.58)
- **Real trades today: 1 in the whole field** (t07's v29). v07 / v02 / v01 / v10 at 0. New board venues: t14 v27 (1589), **t18 v28
  "Mercado Chamberí" (1662)**, t07 v29 (1758).
- t12 sold SAL-06 to Pilar at 25; t18 sold LAV-08 to Pilar at 19 and SAL-05 to t07 at 5 (ladder and fodder). t10: no deals since 1745.
- Board: t12 34.61 · t18 33.38 · **us 32.40 (#3)** · t10 32.18 · t03 29.07.

### Sun 10:26 · snapshot 1722 (phase 0.43; the 10:16 hard Market Test is now in: every board +≈ 2.1)
- **t13's mechanic, a dealer → team closer flip** [V feed]: LAV-07 bought from Abuela at 25 (tick 1711), sold to t12 at 40 one tick later
  (1712). t13 books a team-trade margin, and the buyer still gets the +50 closer because the LAST hop is a team trade. Its Sunday ≈ 35.
- Running totals: t12 67.79 · t10 65.57 · t18 63.43 · **us 61.07** · t03 57.48 · t13 52.55. Sunday so far: t18 38.5 · t12 35.2 · t13 35.0 ·
  t03 30.2 · **us 29.4** · t06 23.6 · t10 21.4.

### Sun 10:23 · tick 1715
- **t12 closed LAV via a TEAM trade: LAV-07 from t13 at 40 on El Rastro (tick 1712) → +50 closer** (≈ +6-10 Sunday, pre-duel scale).
- **t10 closed SAL via Chato** (SAL-08 at 30, tick 1715): a dealer close, no bonus.
- **t13 is the closer broker:** CHA-01 → t18 (72), SAL-10 → t03 (108), LAV-07 → t12 (40). It sells page closers to whoever asks.
- t03 bought MAL-07 from t15 at 9 (tick 1647): t15's spare MAL-07 (once our MAL closer source) is gone.

### Sun 09:58 · snapshot 1602 (phase 0.28)
- Sunday so far (±1): t18 30.0 · t13 24.1 · **us 20.6 (CHA closer +50 via t02 at 72)** · t03 20.2 · t08 18.1 · t12 16.6 · t06 13.9 · t10 10.2.
- **t03** sold RET-09 to Pilar at 73 and RET-10 at 67 (L3 ladder slots; it doesn't hold the RET page). It still lacks SAL-03 for SAL 10/10.
  t15's public SAL-03 ask at 7 expired unfilled (tick 1593).
- **t06** closed CHA via Abuela (CHA-05 at 9): a dealer close, no bonus. t18 (via t13) and us (via t02) closed through team trades.
- t10 and t12: still no Sunday deals; their Sunday is market VC + duels so far.

### Sun 09:40 · snapshot 1542 (phase 0.20)
- Running game totals: t10 56.37 · t18 52.86 · t12 52.65 · **us 50.65** · t03 46.94 · t06 43.85. Sunday so far (±1): t18 ≈ +30 · t13 ≈ +25
  · t03 ≈ +12 · us ≈ +11 · t06 ≈ +8 · **t10 and t12 ≈ 0 (no Sunday deals yet)**.
- **t13 is the hub feeding our rivals** [V feed]: bought SAL-11 from t18 (238), sold CHA-01 to t18 (72, t18's CHA closer) and SAL-10 to
  t03 (108, toward t03's SAL page). t13 values epics high and sells page cards at ~70-110: our RET-11 buyer and CHA-05 source.
- t03: SAL 9/10 (lacked SAL-03 and SAL-10 on the feed; bought SAL-10). If SAL-03 comes from a team, t03 closes SAL (+50) and
  enters the #3 race.

### Sun 09:32 · snapshot 1502 (phase 0.15)
- **t18: CHA sprint, 9/10 by tick 1506 (lacks CHA-01)** [V feed]: CHA-09 Pícaros 58 (1484), CHA-06 Chato 31 (1485), CHA-10 Pícaros 54
  (1491), CHA-07 Chato 31, CHA-02/03/04 Abuela 9-10, CHA-08 Chato 31, CHA-11 epic Pícaros 145 (1496). It **sold SAL-11 to t13 at 238**
  on El Rastro (1494). Sunday round ≈ +25 so far; game total 50.61 vs ours 50.07. Its CHA closer needs a TEAM seller of CHA-01 (+50).
  Chato buys at 31 sit above list 26: no ladder for t18 there (it bought speed).
- t13 pays big for epics (SAL-11 at 238): a buyer for our RET-11.
- t10, t12, t06: no Sunday deals yet (Sunday ≈ 0).

### Sun 09:20 · first round-3 snapshot 1462 (Saturday final)
- **t12 +7.03 at the close** with no trade of its own: its Saturday market went 10.88 → 17.91, i.e. its v02 real trades went from 0 to
  ≈ +6.7 when the close recomputed values (the same recompute flipped our mm −5.2 → +2.2: us +2.72). t12 is now #2 on the game
  total (52.66). Watch v02 on Sunday: it may carry the same VC logic.
- t06 −0.90, t14 −0.34, t17 −0.21: their market parts fell at the close (the top-3 mean rose with t12).
- Board drops at the open (t10 −1.94, t18 −1.61, t03 −1.53) are the phase-0.08 blend of round 3, not losses.

### Sat 23:00 · final snapshot 1440 (doors closed; clock paused at game 13.367, round 2 still active)
- Board: t10 37.58 · t18 31.26 · **us 30.49 (#3)** · t12 30.42 · t03 29.67 · t06 28.76 · t14 27.67. Game total (0.5·Fri + Sat):
  t10 56.37 · t18 46.89 · us 45.73 · t12 45.63 · t03 44.51 · t06 43.14 (intel/standings.md).
- **t06 fell #2 → #6 by selling a page card** (tick 1417-1418): it sold RET-06 to t07 at 30 on El Rastro and bought another
  RET-06 from Chato at 61 (list 26). Negotiating −2.12 board ≈ −13.7 neg_points [V attrib]. That confirms the guardrail: never
  sell a card from a complete page (the deck's −130), and dealer buys above list never count.
- **t18 climbed on late Pilar sells**: SAL-10 at 71 (tick ≈ 1395, +0.82 board ≈ +6.3 np) and RET-07 at 25 (1426, +0.28). These are
  ladder slots at L3. A copyable play for Sunday's fresh ladder: our RET-11 and MAL-08 go to Pilar (score-model §4.5).
- t12: LAV-08 from t08 at 14 on v11 (+0.73 board ≈ +4.7 np); market −0.25 (bench session 6; v02 is a board venue below the stall).
- t10: RET-11 from the Pícaros at 142, and t12: MAL-11 from the Pícaros at 139. Neither moved the board (dealer buys never score
  negotiation; ladder already capped).
- **Our mm_points −5.2 → +2.2 at the close** with no v10 trade (score-model §3h): the next snapshot shows the board effect.

### t14 deep dive (Sat 19:10; Chief's ask: "Team 14 says it is 100% sure to win")
- **Pages [V leaderboard, L feed]:** pages_complete 3 since snapshot 950. Feed-visible: RET 10/10; LAV 8/10 (missing LAV-01,
  LAV-08); LAT 8/10 (missing LAT-06, LAT-07); SAL 4/10; MAL 1/10. With 3 complete pages, LAV and LAT are most likely complete
  through unseen starting cards → **no near-complete page left; a page close by t14 tonight is unlikely**. No t14 bid for
  LAT-06/LAV-01/LAV-08 seen; t10's addressed LAT-07 offer to t14 (993) never settled.
- **Recent play:** dumps commons as asks at 9-12 on El Rastro/v01 (ticks 705-769); swap offers SAL-05/03/02 for LAV-05/LAT-05/LAV-03
  (955); ladder at every level while below the cap (Pilar ×7, Chato ×3, Pícaros ×4 incl. RET-09 57, RET-10 57, SAL-09 58);
  fever cash: SAL-09 → Pilar 78, SAL-08 → Pilar 27/29, MAL-10 → Chato 49.
- **Duels:** aliases hide team ids; Aleks's book: 16/17 rival teams scripted, 1 silent, 0 LLM in Duels I. t14's pure Duels I
  part ≈ 7-10 of 12 [L].
- **Eggs/hints:** none for t14 (2 Abuela gifts, 3 Workshop crafts). No visible hidden edge.
- **Sunday:** cash not public; it raised cash in the fever. CHA multiplier unknown (if 1.6, its CHA page is worth the same +50 as ours).
- **Market:** v14 stall, one trade all day (418); market 9.53 = 7.5 + VC ≈ 2.0 → room ≈ +3 to the cap.


### Sat 22:25 · snapshot 1370
- Board: t10 37.91 · t06 31.42 · **us 30.87 (#3)** · t12 30.57 · t18 30.11 · t03 30.03 · t14 28.20.
- **t10's lead decomposed** (game total = 0.5·Fri + Sat, snapshot 1360): Friday ½ +0.39 · Saturday negotiating +2.84 ·
  **Saturday market +7.50** (v07 value created at the cap vs our 0). 70% of its lead is market; repeatable Sunday.
- **t14 completed its SAL page through a DEALER** (SAL-06 from Abuela at 24, tick 1371): no page bonus scored (dealer gains
  clipped). Its SAL rares came from the Pícaros (57/56), SAL-07/08 from Abuela.

### Sat 22:10 · snapshot 1340
- Board: t10 38.29 · t06 32.63 · **t12 31.02** · **us 30.95 (#4)** · t18 30.05 · t03 29.97 · t14 28.37.
- Game total so far (0.5·Fri + Sat): t10 57.44 · t06 48.95 · t12 46.53 · **us 46.42** · t18 45.08 · t03 44.95 · t14 42.55.
- t12 +1.55 at 1310 with no team trade (Duels II or dealer deals) [L]; t18 +1.92 at 1340: LAT-10 bought from t13 at 72 (1332),
  likely its LAT page close.

### Sat 21:58 · snapshot 1300 (Duels II running since 1239)
- Board: **t10 38.36** · t06 32.55 · **us 30.85 (#3)** · t14 28.63. On 0.5·Fri + Sat (= 1.5 × board): **t10 57.54 · t06 48.82 ·
  us 46.28** · t14 42.95. To finish #1 we'd need to beat t10 by > 11.3 points of Sunday's 60-point round; t06 by > 2.5.
- **t10's Duels II edge [L]:** Saturday negotiating +5.6 since 1240, ≈ +2.5-3.5 of it from duels (windows without t10 deals:
  +1.03, +1.14, +0.08, −0.27); ours −1.6 over the same windows (duel part graded below the field's rise + ladder erosion).
  t10's duel part ≈ 2.3-3.0 board above ours.
- t10 also flipped epics: SAL-11 from the Pícaros at 155 (1267) → sold to a team at 207 (1296); bought MAL-11 from a team at 195.
- t06: RET-11 from the Pícaros at 137 → sold at 216 on El Rastro (1245); RET-10 sold 84, re-bought from the Pícaros at 58.

### Sat 19:41 · snapshot 1130
- Board: **t10 34.02** · t06 32.80 · **us 31.92 (#3)** · t14 30.32 · t18 30.26 · t03 29.75.
- **t10 keeps the SAL-rare cash loop + L4** [V feed]: Pilar SAL-09 84 (1101), Pícaros SAL-10 55 (1108), Pilar SAL-10 80 (1121),
  Pícaros SAL-09 55 (1128): +25-30 cash per round trip and fresh ladder share while below its cap. +0.65 at 1110, +0.24 at 1130.
- t06 +0.82 at 1110: Pícaros RET-09 at 54 (L4) + Pilar LAT-08 20.
- **t14 −0.77 at 1110**: bought SAL-11 (epic) from the Pícaros at 140 (1104); a loss if its SAL value < 140 [L].
- Epic churn: t16 sold SAL-11 to Don Ernesto at 116 then bought another from the Pícaros at 146; t08 bought MAL-11 at 128.

### Sat 19:27 · snapshot 1100
- Board: **t10 33.13 (#1)** · t06 32.08 · **us 31.68 (#3)** · t14 31.19 · t18 30.28 · t03 29.42.
- **t10 +0.46 (1080) and +0.88 (1090) with no settlement of its own** while the field was flat → matches ≈ 3 scored flags on
  Pícaros lies (+10 neg_points each) [L]. Then +0.21 at 1100 (Pícaros SAL-09 54, Abuela MAL-07 19).
- t06 +0.54 at 1100: MAL-04 → Pícaros 5 (L4); SAL-09 → Chato at 29 [? a loss on paper].
- Don Ernesto open to all since 1091; t08 sold LAV-11 (epic) to him at 120 after buying it from the Pícaros at 147.
- t12 and t14 keep the SAL-rare loop (Pícaros ~52 → Pilar 76-87).

### Sat 19:11 · snapshot 1070
- Board: **us 31.68 (#1)** · t06 31.60 · t10 31.58 · t14 31.28 · **t18 30.31 (+0.90: Pícaros LAT-09 at 55)** · t03 29.51 · t16 27.39.
- t14 −0.48 since 1040: Pícaros SAL-10 56 (1044) → Pilar 87 (1052), a SAL-rare loop; its ladder erodes between deals.
- t12 runs the same loop (Pícaros SAL-09 48 → Pilar 80). t08 bought LAV-11 (epic) from the Pícaros at 147.
- Eggs at Abuela: us (1047), t16 (1049), t13 (1053). Eggs never score (RULES).

### Sat 18:56 · snapshot 1040: four-way tie at the top
- Board: t14 31.76 · **us 31.68** · t06 31.68 · **t10 31.68 (+3.33)** · t03 29.61 · t18 29.43 · t16 27.48.
- **t10 closed its RET page cheaply** [V feed]: Pícaros RET-09 59 (1024) + RET-10 53 (1028) (dealer, 0 neg), Abuela RET-04 10,
  then the closer RET-03 from **t06 at 12** (team trade, 1033). Copy for Sunday's CHA.
- t14 +0.50 at 1020: Pícaros SAL-09 58 (1027), Pilar SAL-09 78 (1035): a SAL-rare cash loop plus L3/L4 slots.
- t18 repeated the epic flip (Pícaros SAL-11 at 139, tick 1035). t17 buys rares from the Pícaros (SAL-09 56, LAV-09 58, LAV-10 56)
  and sold SAL-09 to Pilar at 72.
- t16 +0.71 at 1030: RET-08 and RET-07 from t15 at 13, RET-05 at 5 (team trades: RET collector).

### Sat 18:40 · snapshot 1010
- Board: **us 32.00 (#1)** · t06 31.68 · t14 31.53 · t03 29.64 · t18 28.77 · t10 28.35 · t16 26.49.
- **t18 epic flip** [V feed]: SAL-11 bought from the Pícaros at 139 (925) → sold to Pilar at **199** in the fever (994): +60 cash
  and an L3 slot; t18 +0.87 board at 1000. Not for us: cash 120 < 139, and our ladder is capped (cash-only gain).
- t10's addressed LAT-07 offer to t14 (23, tick 993) has NOT settled (no settlement through 1011). t14's LAT stays 8/10 (feed).
- t16 sells LAV-02/04 to the Pícaros at 5 (L4); t02 sells RET-08 to the Pícaros (11), LAV-08 to Pilar (16).

### Sat 18:25 · snapshot 980 (fever on; Don Ernesto live for early teams since 971)
- Board: t06 31.68 · t14 31.52 · **us 29.97 (#3, flat)** · t03 29.64 · t18 27.90 · t10 28.26 (+0.59: Pícaros MAL-09 57 + Pilar SAL-10 74/75).
- **t08 runs a SAL-rare cash loop** [V feed]: Pícaros SAL-10 at 53 → Pilar 78 (958 → 965); Pícaros SAL-09 at 52 (971); earlier
  Pilar SAL-09 77. +25 cash per loop; neg 0 only for a team that values the rare between the two prices. Not for us (our SAL
  rares are page cards; a 2nd SAL copy is worth 15.75 to us → −36 neg_points on the buy).
- t07 sells LAT-06 / RET-06 / RET-01 to Chato, Pilar and the Pícaros; t03 sold LAV-06 to the Pícaros at 11.

### Sat 18:12 · snapshot 950 (Salamanca fever since ~18:04; Don Ernesto announced at 932)
- Board: **t06 31.73 (#1)** · t14 31.56 · **us 29.97 (#3)** · t03 29.20 · t18 27.93 · t10 27.67 · t16 26.03 · t12 25.84 · **t01 23.98 (#12)**.
- **t01 −4.27 at 950** [V board]: its only event was SELL SAL-07 → Pilar at 29 (948). Reading [L]: SAL-07 was a page card; a
  dealer sale counts the page-bonus loss in full (≈ −90 neg_points). Guardrail for us: never sell a page card to a dealer.
- t06 +1.14 at 940: Pícaros BUY RET-10 at 55 (935, L4). t18 +0.83 at 930: Pícaros BUY SAL-11 (epic) at 139 (below list 162).
- t14 is buying RET commons at 9 from Abuela (RET-01/02/05) and RET-03 from t02 at 7; pages 2 → 3.
- Fever prices to Pilar: SAL-08 27-28 (t04, t14, t17, t10), SAL-07 29-30 (t01, t07), SAL-09 77 (t08).

### Sat 17:57 · snapshot 920 (bench 4 started 17:55)
- Board: **t14 31.89** · t06 30.62 · **us 29.98 (#3)** · t03 28.57 · t01 28.52 · t10 27.65 · t18 26.99.
- t14 +0.46: Pícaros BUY RET-10 at 57 (920), after RET-09 at 57 (852): t14 keeps filling L4 below list, and its RET set grows.
- On Saturday alone t06 (39.59) and t14 (38.80) lead; for the game total (0.5·Fri + Sat) t14 47.83 · t06 45.93 · us 44.97.
- t15 bought MAL-09 from the Pícaros at 60 (920).

### Sat 17:54 · snapshots 900-910
- Board at 910: t14 31.43 · t06 30.73 · **us 29.98 (#3)** · t03 28.75 · t01 28.71 · t10 27.74 · t18 27.04 · t16 26.23 · t12 26.06.
- **t06 flipped a Pícaros rare** [V feed]: bought RET-09 from the Pícaros at 52 (887, L4 slot), sold it to t12 at 84 on El Rastro
  (895). t12 +2.18 at 900 (likely its RET page), then **t12's market fell 12.43 → 7.50 at 910** (v02's value created below the
  reference) → #9.
- Copyable [L]: buy a rare below list from the Pícaros, sell it to a team collector at ~80-85: a dealer buy at ≤ our value
  costs 0, the team sale scores price − our value. Only for sets where our value is below the resale price.
- t13 bought LAV-09 from the Pícaros at 63; t07 sold LAV-10 to Chato at 75.

### Sat 17:42 · snapshot 890 (Los Pícaros open to all since ~17:35)
- Board: t14 30.75 · **us 29.38 (#2)** · t06 29.37 · t01 29.06 · t03 28.75 · t12 27.98 · t10 27.81 · t18 27.04.
- t14 erodes 0.1-0.2 per snapshot (its ladder below the field cap); we hold exactly flat (ours capped) [L].
- **t06 +1.98 at 890**: RET-09 bought from the Pícaros at 52 (887; L4 slot) [+ possibly a page step]. **t01 +0.66 at 870**:
  LAV-10 from the Pícaros at 63 (864).
- Pícaros buy commons/uncommons cheaply: t12 LAV-03 5, LAV-07 11; t08 RET-08 11.

### Sat 17:27 · snapshot 860
- Board: **t14 31.15 (#1)** · us 29.38 · t03 29.09 · t01 28.69 · t12 28.51 · t10 27.98 · t06 27.42 · t18 27.13.
- **t14 +1.47 in two snapshots, all ladder** [V feed]: Pilar SELL MAL-06 19 (842; its 2nd Pilar deal → Pícaros early unlock),
  Chato SELL MAL-10 49 (845), Pícaros BUY RET-09 57 (852, below list 63). One deal per level, fresh slots.
- **t03 +1.25**: a 5-card El Rastro bundle (844): RET-01, RET-02, MAL-01, MAL-04 → t07 for LAV-10 + 38 P (cash direction [?]).
- Pícaros: t08 bought SAL-10 at 62 (835) and sold RET-06 at 12 (839); t04 sold LAV-08 12, MAL-01 5; **t16 bought SAL-11
  (epic) at 167** (858, above list 162).
- t15 is liquidating SAL commons to Abuela at 6 (SAL-01/02/03) and sold one RET-01 to Abuela at 6 (803).
- Organisers (850): "Salamanca fever starting in 45 min" → 18:04 as mapped.

### Sat 17:11 · snapshot 830
- Board: **us 29.73 (#1)** · t14 29.68 · t01 28.89 · t12 28.70 · t10 28.25 · t03 27.99 · t06 27.85 · t18 27.79. Quiet window:
  the field drifts −0.1 to −0.2 per snapshot; we held flat.
- **t15 is selling SAL to Pilar before the fever** (SAL-07 24, SAL-08 25) and sold one RET-01 to Abuela at 6 (tick 803):
  one of the duplicates planned for v10 is gone. t08 sold SAL-09 to Pilar at 70 (812) and SAL-07 at 24 (821).
- t13 keeps looping LAV uncommons through Pilar (LAV-06 17, LAV-07 18).
- No v10 trades yet.

### Sat 16:57 · snapshot 800
- Board: t14 29.85 · **us 29.73 (#2)** · t01 29.09 · t12 28.62 · t10 28.36 · t03 28.20 · t06 28.00 · t18 27.85.
- **The whole field fell 0.6-0.7 board** this window (t14 −0.71, t18 −0.68, t06 −0.68, t17 −0.67, t01 −0.61): L4 deals by the
  early teams (t01 MAL-10 59, t03 LAV-09 59, us SAL-10 54) lifted the ladder reference. Only t03 (+0.37: L4 slot) and t16
  (+0.66) rose.
- SAL rares are being hoarded before the fever: t06 bought SAL-09 from t15 at 68; t15 bought LAV-09 from Chato at 89.
- t15 ↔ t07 keep swapping (LAV-08 ↔ LAV-07, tick 787).

### Sat 16:53 · snapshot 780
- Board: **us 30.02 (#1)** · t14 29.83 · t12 29.12 · t01 29.04 · t10 28.98 · t18 28.61 · t03 27.79.
- t01 +0.73 (LAV-09 from the Pícaros at 58, an L4 slot) → #4. t06 +0.54 (Pilar SAL-07 23, MAL-08 18). Everyone else drifted
  −0.1 to −0.4 (the ladder and trade references rising).
- t08 bought SAL-09 from Chato at 77 (above list); t02 bought SAL-09 from the Pícaros at 67. SAL rares are being stocked for
  Pilar's fever (18:04-20:04).

### Sat 16:44 · snapshot 770 (Los Pícaros live since 16:35)
- Board: t14 30.06 · **us 29.53 (#2)** · t12 29.33 · t10 29.24 · t18 28.75 · t01 28.31 · t03 27.86.
- **Our two flags on Pícaros lies scored +10 neg_points each (≈ +0.57 board each).** t02 likely flagged too (+0.54 net, no
  scoring event; it got "they stopped printing this one yesterday" at 763) [L].
- Pícaros early access (tick 761): t02, t03, t04, t05, t08, t09, t10, t16. t02 bought SAL-09 from them at 67 (above list 63).
- t17 +0.65 (Chato MAL-08 sell at 15, ladder); t06 +0.51 (RET-04 sold to t14 on v07 at 5).

### Sat 16:26 · snapshot 740
- Board: **t12 29.90 (#1)** · t14 29.88 · t10 28.93 · t18 28.87 · **t01 28.55 (#5, surging)** · **us 28.43 (#6)** · t03 26.12.
- **t01 +5.0 Saturday points in 3 snapshots** [V]: three Pilar sells into empty L3 slots, LAV-06 at 19 (718), MAL-08 at 20
  (726) and **SAL-10 at 70** (737). A team with ~no ladder gains most from fresh slots; t01 also made no other deals.
- **Pilar buys SAL rares at 65-70 before the fever** [V]: t08 SAL-10 69 (722), SAL-09 65 (731); t01 SAL-10 70. During the fever
  (18:04-20:04, +25% over book) a SAL rare should fetch ≈ 87.
- Field-wide drift at 730 (t14 −0.41, t18 −0.57, t10 −0.21, us −0.33 Saturday points): the ladder reference rising with
  t01's and t08's Pilar deals [L].
- Workshop crafts: t18 (La Chulapa), t16 (Vermut del Domingo), t08 (Teatro Valle-Inclán), t10 (La Vía Láctea).
- Ours: bought MAL-01 from t06 at 5 on v07 (714): neg_points +2.0.

### Sat 16:12 · snapshot 710 (bench 3 scored)
- Board: t14 30.27 · t12 29.73 · t18 29.25 · t10 28.59 · **us 28.53 (#5, 1.74 behind)** · t13 26.09 · t17 25.43.
- Bench 3 moved board venues up: t13 5.49 → 6.08, t03 3.61 → 4.75, t06 11.64 → 11.89; stalls stay 7.5 (our efficiency
  0.933 → 0.878, still 7.5).
- RET-06 is the hot uncommon: t04 → t09 on v07 at 28, t03 → Pilar 25, t06 → t04 at 26, t06 ← Abuela 21, t12 → t16 at 14.
  t06 runs the Abuela-Pilar loop too (LAV-08 → Pilar 16, RET-06 ← Abuela 21).
- Workshop users at 709: us (→ MAL-06) and t12 (→ RET-06).

### Sat 15:56 · snapshot 680 (resumed 15:30; bench 3 started 15:55)
- Board: t14 30.28 · t12 29.79 · t18 29.29 · t10 28.92 · **us 28.34 (#5, 1.94 behind)** · t13 25.50 · t17 25.43.
- t18 +0.73 Saturday points: sold RET-08 to t04 at 27 on El Rastro (645). t14 −0.35 with no events (field drift).
- Market: t12 back to 12.50 (v02: t07 → t04 MAL-03 at 7, tick 679); t10 12.46 → 12.28 (v07: t12 → t06 LAT-02 at 4, 648).
- Rares to Pilar: t02 sold LAT-10 at 50 (660) and LAT-08 at 19 (666); t04 bought LAT-10 from Chato at 81 (657).
- Swaps continue: t15 ↔ t07 RET-02 ↔ LAV-04 (661); ours: RET-04 (spare) ↔ SAL-04 with t08 on v11 (669, +6.2 neg_points).

### Sat 14:10 · paused since 13:26 (tick 630)
- **Swap offers are now common** [V feed, 183 since tick 160]: t13 56, t15 45, t08 28, t10 22, t06 19, t04 5, t05 4, t12 4.
- **t13 is hunting RET commons by swap** (ticks 626-627, addressed on t03's v20): LAV-05 or MAL-02 for RET-01..05, to t04, t15,
  t08, t10, t06; plus LAT-07/LAT-08 from t02/t12. Reading [L]: t13 is assembling a RET page; a page close by team trade or swap is
  worth up to +50 neg_points (≈ +4.7 board). Known RET-common holders: t09, t04, t15 (bought from t14 at 9).
  t13 also posted a public swap on our v10 (606: LAV-05 for RET-01).
- Our first swap offers went out at 630 (LAT-04 + MAL-04 for SAL-07 to t15; LAV-02 for MAL-01 to t07 on v15).

### Sat 13:40 · snapshot 630 (game paused since ~13:26)
- Board: t14 30.77 · t12 29.60 · t10 28.88 · t18 28.81 · **us 28.15 (#5)** · t17 25.79 · t13 25.54 · t01 24.97.
- **Card-for-card swaps on El Rastro** [V feed]: t15 ↔ t07 swapped three times at price 0 (607 LAV-08 ↔ LAV-06, 613 LAV-03 ↔
  MAL-08, 616 MAL-01 ↔ SAL-02). A swap of duplicates for lacks scores for both sides (value gained at private values, no cash);
  on a 0% venue, the venue owner books both sides' gains as value created. We haven't made a swap yet.
- **t13 keeps looping uncommons through Pilar** [V feed]: LAV-07 → Pilar 17 (601), LAV-08 → Pilar 18 (610), rebuys LAV-08 from t07 at
  20 (611) and LAV-07 from Abuela at 22 (612). It still slid to #7: its ladder-heavy score erodes as everyone sells to Pilar.
- t12 bought RET-10 from Chato at 90 (626, above list 77); t08 bought a silver pack at 162 (613).

### Sat 13:10 · snapshot 600
- Board: t14 30.42 · t12 29.88 · t10 29.51 · t18 29.21 · **us 28.96 (#5)** · t13 26.77 · t17 26.17.
- **t14 sells RET commons on t12's v02** (5 at 9 as maker, ticks 591-598; buyers t09 ×3, t04, t15): t14 banks neg_points,
  t12's market hits the 12.5 cap. RET collectors (live demand): t09, t04, t15 [L].
- **t04 liquidates commons to Abuela at 5** (7 sales, 594-600): cash for Sunday's CHA? [L].
- t10 bought MAL-10 at 74 from t03 (tick 585) despite reading ~0.5 on MAL [?]; t03's Saturday part +2.6 on the sale.
- t06 bought LAV-09 from Chato at 84 (tick 593, above list 77).

### Sat 12:56 · snapshot 570
- Board: t14 31.76 · t18 29.98 · **us 29.57 (#3)** · t12 28.91 · t10 28.70 · t17 27.70 · t13 27.69.
- **t14 market (10.6) is passive** [V]: one v14 trade (t15 → t12 LAT-07 at 19, tick 418), nothing since; it fell from 11.86
  when t06's VC rose. t06 (v01, board): 2nd trade t12 → t08 SAL-10 at 76 (tick 556) → market 9.83 → 11.64.
- t12 sells SAL rares (SAL-10 at 76 to t08): t12 dumps SAL [V]; t08 values SAL ≥ 1.1 [L].
- Pilar sells keep coming: t09 MAL-08 21 / SAL-07 24, t04 RET-08 22, t12 RET-07 25, t08 LAV-11 (epic) at 140.

### Sat 12:42 · snapshot 540
- Board: **t14 32.96 (#1)** · t12 30.53 · **t10 29.56 (#3, +3.6)** · t18 29.40 · t17 29.33 · t13 28.23 · **us 27.49 (#7)**.
- **t14 back to #1:** duels (part 6.4 → ~12.6 incl. deals) + Pilar LAT-08 at 20 (best uncommon share seen) + Chato BUY LAT-10
  at 86 (above list 77) that completed its LAT page (pages 1 → 2). A page closed through a DEALER scores 0 neg_points (gains
  clipped) [L]: not a play to copy.
- **t10 (#3):** duels 5.0 → 10.3 plus two Pilar sells at the top of her range (SAL-08 24, RET-08 25).
- **t04 sells patiently:** SAL-08 → Pilar at 25 (opened 40, 6 messages) vs our 23 (copied in the 12:42 note to the Chief).
- t12 is sliding in duels (12.0 → 9.5).

### Sat 12:30 · snapshot 510 (Duels I running)
- Board: t12 31.91 · **t17 29.29 (#2, +2.5)** · t14 28.85 · t13 27.71 · t18 27.48 · **us 27.03 (#6)** · t10 25.98 · t01 25.97.
- **t17 closed its MAL page** [V: pages 1 → 2]: bought MAL-10 from **t18** at 70 + 5 fee as taker on El Rastro (tick 508).
  Saturday part +4.7 in that window (page close ≈ 0.6 × 0.235 × 50 ≈ 7 minus duel slippage). t18 (#5) sold a page-closer to a
  top-3 rival for ~+20 neg_points.
- **The field is copying the dealer-sell ladder play** [V feed, 509-513]: t08 MAL-06 → Pilar 17, t16 LAT-07 → Pilar 17,
  t14 LAT-08 → Pilar 20, t10 SAL-08 → Pilar 24, t06 LAV-08 → Chato 13, t07 LAT-10 ← Chato 89. All teams are level 3 now.
  If the ladder part is graded against the field, every rival's deal lowers what ours is worth: do ours early.
- t13 is the weakest top team in duels (duel part 8.3 → 5.4); t14 9.9 → 6.4. t12 and t01 lead the duel part (~11.5-11.9).

### Sat 12:12 · snapshot 480 (Duels I running)
- Board: **t12 32.19** · t14 31.16 · t13 29.68 · t17 26.77 · t18 24.88 · **us 24.76 (#6)** · t10 24.0 · t04 23.9.
- Duels now carry 40% of Saturday Negotiating (intel/score-model.md §1b); the moves since 460 are mostly duels. Duel part
  (Saturday points, max 12): t12 12.0, t15 10.3, t14 9.9, t09 8.8, t13 8.3, t03 8.3, **us 8.2**.
- **t12 (#1):** full duel part from the first wave, plus market 11.74 (v02 value created). It buys LAT duplicates from t15 on
  others' venues (v14 tick 418, v17 tick 433), which feeds those venues' owners, not itself.
- **t13's Pilar-Abuela loop [V feed, ladder effect L]:** sells an uncommon to Pilar, rebuys the same card from Abuela below
  list: Pilar SELL LAV-08 @18 (t462), LAV-06 @18 (t467); Abuela BUY LAV-08 @23 (t469), LAV-06 @23 (t474). Same holdings at
  the end, −5 P and about −5 neg_points per card (≈ −0.47 board), bought ladder at level 3 (sell) and level 1 (buy ≤ list).
- **t17 (#4):** market 10.26 from one trade on its v17 stall (t15 → t12 LAT-01 at 7); cut the stall's fee to 0 at tick 429.
- t18 dropped to #5: its duel part fell 7.9 → 5.0.

## The board [V, leaderboard tick 420]

| Team | Rank | Score | Negotiating | Market | Deals |
|---|---|---|---|---|---|
| t14 | #1 | 29.05 | 17.19 | 11.86 | |
| t13 | | 27.72 | **24.39** (top) | 3.33 | 45 |
| t18 | | 26.66 | 19.16 | 7.5 | 28 |
| us (t05) | | 22.66 | 15.16 | 7.5 | 35 |

- Market leaders: t10 12.5, **t14 11.86**, t12 11.74.
- Our parts [V, /api/me]: neg_points 35.2, ladder 0.055, duels 0, bench 0.5, **mm_points −5.2**.
- Hub multipliers [L]. Each team has the same six numbers (1.6, 1.3, 1.1, 0.9, 0.7, 0.5) shuffled (RULES.md:24),
  so MAL and SAL can't both be 1.6.
  - **t13:** MAL 1.35 / SAL 1.35, most consistent with {1.6, 1.3}; LAV 1.07, RET 0.91, LAT 0.59.
  - **t18:** RET 1.51 (likely 1.6), LAT 1.21, SAL 1.17, LAV 0.70, MAL 0.67.

## 1. Dealer deals [V counts and prices]

| | Friday | Saturday | Buys vs list | Unlocks |
|---|---|---|---|---|
| **t13** | 15: 7 Abuela buys, 6 Abuela sells, 2 Chato sells | 15: 3 Abuela buys (packs), 8 Abuela sells, 2 Chato buys, 1 Chato sell, 1 Pilar sell | never above list: Abuela 8 below (5 packs), 2 at; Chato 2 **at** list (LAV-06/07 at 26) | Chato t98 ("6 deals with abuela"); **Pilar t262 ("3 deals with chato")** |
| **t18** | 8: 6 Abuela buys, 1 Chato buy, 1 Chato sell | 8: 6 Abuela buys, 2 Chato buys | Abuela 10 below, 2 at; Chato 3 above (LAT-08 32, RET-09/10 86) | Chato t98 ("3 deals with abuela"); no Pilar |
| **us** | 15: 7 Abuela buys, 5 Abuela sells, 2 Chato buys, 1 Chato sell | 8: 5 Abuela buys, 3 Chato buys | Abuela 11 below, 1 above (MAL-07 29, = Abuela's Friday opening ask); every Chato buy above list (31, 93, 87, 86, 30) | Chato t98 ("6 deals with abuela"); no Pilar |

- **t13 sells commons to Abuela** [V]. 14 sales at 5-6 P: t13 opens at 20-22, she bids 5, and it ends after 5-7
  rounds. They look like spare copies [L]: it sold two copies each of SAL-01 and LAT-04, and SAL-05 and MAL-01 while
  holding earlier copies. A spare sold at ≥ its 25% value scores ≥ 0.
- **The Pilar unlock is unexplained [?].** t13's 4 Chato deals before her level activated (tick 262):
  - 2 buys at exactly list. t13 stepped LAV-06 from 9 and LAV-07 from 12 up to 26, and **Chato accepted t13's number**.
  - 2 sales where **t13 accepted Chato's final** (LAT-09 at 46 after his opening 39, MAL-06 at 15 after 13).

  The server says "3", but "at or below list counts" predicts 4 and "below list only" predicts 2. Who accepted is a
  possible confound. We had 0 at-or-below-list Chato deals, and our one sale was at his opening bid (RULES.md:35: never
  counts). **Not a GAME.md change**: n = 1, and RULES.md:35 only says "a negotiated one does".
- Level 2 [?]. t18's "3" matches its 3 card buys before t98 with its 2 packs left out; t13's "6" matches 5 card buys
  plus 1 sale. Our "6" doesn't fit cleanly: 3 card buys, 4 sales (2 at her opening bid), and MAL-07 at her opening ask
  (t98, settled just before the unlock event).
- Opening prices: the scan matched threads by asset id, which misses buy threads (dealer sell offers name the card by
  type). Counts are unaffected; per-deal opening prices for buys aren't reported here.

## 2. Team trades [V prices; est. L, biased low on duplicates and page closes]

| | Friday | Saturday | Notes |
|---|---|---|---|
| **t13** | 9 (6 buys, 3 sells), est. +122 | 6 (2 buys, 4 sells), est. +22 | Buys in its high sets at or near clearing: SAL-09 at 74 (+20), SAL-10 at 70 (+24), MAL-10 at 65 (+30, t331), MAL commons at 6 (+7.5 each). Sells LAT: LAT-09 at 65 (+24), LAT-01+07 at 40 (+19). Saturday sales est. −6.5, −8.5, −2.7 (likely duplicates, so better than that [L]). All on El Rastro but two small sales on t12's v02. |
| **t18** | 9 (2 buys, 7 sells), est. −2 | 3, est. −31 *excluding the page bonus* | RET-02 bought at **49** from t02 as maker (it posted the bid). Its negotiating rose **16.25 → 22.08** between ticks 220 and 230 [V leaderboard], which fits a capped +50 page close, not −34 [L]. It sold SAL-01 and MAL-04 twice each (duplicates [L]). It scores on pages [L]. |
| **us** | 9 (3 buys, 6 sells), est. +40 incl. the LAV close | **+56.7 measured** [V]: RET-01 page close +50.0, SAL-01 +4.7, +2.0 | Friday LAT/MAL uncommon sales near clearing est. +8.5, +9.5, +8.5. |

**What t13 does that we do less** [L]: trade by trade, it buys cards of the sets it values most (MAL/SAL) at or near
clearing and sells cards of the set it values least (LAT): est. +7 to +30 on its best trades, some negative ones too.
It never pays a dealer above list.

## 3. Venues and value created

- t13's **v03** (board, opened t129; fee 0% since t251/t316) has had **0 trades** [V]. t13 promotes it with
  announcements every 10-20 ticks, including a "Club welcome" offer of spare commons at 5 P. t18's **v18** stall (3%,
  auto): 0 trades [V]. Neither scores much market: t13 3.33, t18 7.5.
- Our **v10** (0% since t230): 2 trades by other teams [V].
  - t10 → t01, MAL-07 at 14: est. +5.0, measured +4.99.
  - t10 → t15, SAL-07 at 26: est. −2.8, measured **−10.19** (mm_points 4.99 → −5.2) [V].

  The hub's t15 SAL estimate rests on n = 3: the value-created estimates hit 1 of 2 [L]. Value created is copy-weighted in
  `tools/v10_radar.py` since b3b0e61.

## 4. Three plays we're not making (handed to the Analyst)

1. **Sunday: buy CHA from teams, not dealers** [L].
   - A dealer buy below our value scores 0 (gains clipped, GAME.md). A team buy scores value − price.
   - Per card, as maker at clearing (9 / 24.5 / 70): **+7 / +15.5 / +42**. At the plan's bids (10 / 25 / 80):
     +6 / +15 / +32. A taker pays 2 / 3 / 5 more in fees.
   - Ceiling ≈ +150 if all nine non-closing cards came from teams at clearing. The closing card is capped at +50 in
     total (not on top).
   - Realistic: supply-dependent (minted 0; teams get CHA from packs and dealers).
   - Changes intel/cha-plan.md: team bids from the release, dealers as a timed fallback.
2. **Sell our low-multiplier cards at clearing to non-top-4 collectors** [L].
   - Ceiling ≈ +60 neg_points if every listing fills. Holdings per /api/me 11:50; LAT at its own clearing 7.5 / 21.5,
     MAL/SAL at 9 / 24.5.
   - Expect a fraction: 5% of asks fill, 9% of bids (GAME.md).
   - The book asks a spare LAT-04 at 4, SAL-02 at 4 and LAV-03 at 5, against clearing ~7.5-9: raising them adds
     ≈ +11 if they fill.
   - The trader's min-gain-sell 6 refuses a collector's 9 P bid for a spare LAT-04 **on El Rastro** (9 − 2 fee − 1.2 =
     5.8). On a 0% venue it nets 7.8 and is accepted.
3. **Stop paying dealers above list** [?].
   - Our 5 Chato buys paid **44 P over list** and earned no ladder or unlock. t13's at-list Chato buys came with an
     early Pilar unlock (consistent with, not proof of, a price-vs-list rule).
   - Cost 0; saves the premium. For Sunday's CHA rares: bid Chato at list (77) before paying more.

**Epics and legendaries:** none has traded, been pulled as a pack's best card, or been offered for sale [V]. Signs of
demand: t12 bid 88 for SAL-11 (t105); t06 posted swap offers wanting LAV-12 (t395) and SAL-12 (t396). `bargains` pages
Lucas if one is offered at value − price − fee ≥ 20.
