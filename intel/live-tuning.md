# Live tuning (Analyst; Sunday, every 15 min; the Operator reads it)

Our answer to Team 10's learning loop: compare what happened with the books every 15 min, and propose changes **only inside
the pre-approved bands below**. Anything outside a band goes to the Chief, not to the Operator.
Read-only: the loop never writes to the game. Sources: `data/feed.jsonl` (settlements, `thread.message` dealer offers,
`duel.closed`), `data/me.jsonl` (neg_points, ladder_points, mm_points, venue_value_created, duel_points, cash),
`run/cha_book.json`, `run/mal_book.json`, keyless `/api/leaderboard`.

## 1. Metrics (actual vs book)

| # | Metric | How | Book reference |
|---|---|---|---|
| M1 | Dealer finals per dealer × rarity: our final price, rounds to close, walk/deal, the dealer's last counter | our threads (`thread.message` offers from the persona) + every team's Sunday dealer settlements | `dealer.target`, `accept_max`, `walk_on_final_ge` |
| M2 | Ladder share per dealer deal | Δ`ladder_points` × 45 / level at each of our dealer deals | full share = level/45 per slot |
| M3 | Team-bid fills: cards held / book, ticks from post to fill, P spent vs plan | our settlements + live bids | `team_bid.start/step/every_ticks/max`; CHA ≈ 330 P, MAL ≈ 140 P |
| M4 | Trade score per team trade: Δneg_points vs (value − price) | `me.jsonl` | the trade's expected gain |
| M5 | Trade part capped? Δ(board negotiating) after a positive team trade | snapshot before/after, field drift removed (`attrib.py`) | ≈ 0.05-0.2 board per np while live; **≈ 0 = capped** |
| M6 | v10: trades, value created, mm_points, board market | `me.jsonl`, board | each pair's expected VC (`intel/matches.md`) |
| M7 | Duel waves: deals/duels, P per deal, decay lost, no-deals with an in-limit rival offer | `waves.py` on `docs/duels/` + `duel.closed` | Duels II: 56/68 deals, 0.54 per deal |
| M8 | Board: our negotiating/market vs the model; rivals' jumps attributed | `attrib.py`, Saturday-only → Sunday-only series | score-model §4.8 |

## 2. Pre-approved bands (the Operator may apply these on the Analyst's line, no Chief needed)

| Knob | Band | Hard limit (never crossed) | Trigger (minimum sample) |
|---|---|---|---|
| Dealer `accept_max` / `target` per dealer × rarity | **±10%** of the book value | ≤ MENU list **and** ≤ our value (0 neg); Pícaros CHA rares ≤ 57 (62 only the short clock) | **≥ 3 Sunday finals** for that dealer × rarity (ours + field), median outside the target band by > 5%, **in 2 consecutive windows** |
| Walk threshold (`walk_on_final_ge`) | ±3 P | never above list | ≥ 2 of our walks at that dealer with a later deal by another team below our walk price |
| Next dealer for a card | any fallback the book already lists | never a dealer for the LAST card | M1 shows the planned dealer's stock gone, or 2 walks there |
| Team-bid ladder: start / step / every_ticks | start ±2 steps; step ±1; every_ticks 20-60 | **PUBLIC CHA team bids ≤ 54 / 22 / 9** (rare / uncommon / common; directive 07:05). Anything higher only as an ADDRESSED, pre-agreed deal with a non-rival (the book's old 90/30/12 maxima apply there and nowhere else); last card ≤ value − 50 | **≥ 2 bids unfilled for ≥ 80 ticks** while a live ask sits within the public cap → +1 step (never above 54/22/9); fills in < 20 ticks at `start` → next card's start −1 step |
| Which CHA card next | reorder the remaining cards by fill chance × gain | the LAST card stays a team trade (CHA-05/CHA-08 rule) | M3 after each fill |
| Ladder upgrade (replace a slot) | only if the new share ≥ old share + 0.10 | never a 4th deal at a level whose best 3 are full, unless it upgrades | M2 for ≥ 2 deals at that dealer |
| v10: next pair to fire; rebate per trade | pairs from `intel/matches.md`; rebate 5/10 P | rebate total ≤ 80 P; non-rivals only | one **negative** VC trade (mm_points falls) → stop that pair type at once (no sample needed: losses count in full) |
| Thread allocation | ≤ 6 open, duel windows first | 1 accept/tick, 5 rps shared | — |
| **Ladder fodder** (APPROVED, directive 02:30; only **after CHA**, the **silver pack first**) | buy LAT uncommons (and other cards we hold **0** copies of) at **price + fee ≤ 12.5**: ≤ 12 as maker, ≤ 10 as a Rastro taker; sell to **Pilar > 16** (target 19-20) first, then **Chato > 13** (target 15) | never a page card, CHA card or MAL-08; never above our copy's value on the buy; never at or below the dealer's opening on the sale; ≤ 3 deals per dealer level unless a slot upgrades by ≥ +0.10 share; float ≤ 60 P; rival sellers only if their gain ≤ 10 P | M2: ≥ 2 fodder sales at a dealer before moving its target ±10%; stop at a dealer after 2 walks |

## 3. Outside the bands → the Chief (the Analyst sends one line with EV, cost and evidence)

- Any price **above list or above our value** (it creates a loss), or a cap outside ±10%.
- **Past our caps (score-model §4.13, Sun 01:35) [L]: references are field-relative (ladder: shown by data; trades: L+).**
  Once capped, every +Δ raises the reference by Δ/3 and lowers each rival below it. So **MAL and positive trades stay worth doing
  past our trade cap**, and **v10 has no VC stop** (only the zero-negative rule).
  **Surplus → ladder (RET-11 below value) is downgraded:** a loss lowers our T, so it lowers the reference and every rival below
  the cap gains ≈ 0.5-1.7. That roughly cancels the ladder slot. Escalate only if the slot is clearly worth more than loss/3 on
  the trade reference.
- **M5 now reads both ways:** a positive team trade that moves our negotiating ≈ 0 (field drift removed) means we are capped. Then
  report "past cap: +Δ/3 to the reference" for each further trade, and never a below-value sale.
- MAL go/no-go beyond the 150 P gate; any cash move > 50 P between stages; Ernesto, gold pack, legendary.
- Selling any page card; any trade with a rival (live top 6 or within 3.0 of us); a page-closer for a rival.
- Venue changes (closing v10, opening a board venue).
- Duel parameters: Aleks and the Duel Lab only. The loop reports M7; it never tunes the duelist.
- One observation that contradicts the model (e.g. a dealer final far outside every Saturday price): report, don't act, until
  the minimum sample is met.

## 4. Noise rules
- Saturday n is small per dealer × rarity (often 3-10); Sunday dealer versions may change (`persona.updated`). Use Sunday data
  once n ≥ 3; until then, the book stands.
- Never re-tune on a single walk or a single fill. Two consecutive windows for any price band move.
- Field settlements count as evidence for prices, not for limits: limits are per conversation (secret).

## 5. Output format (newest first, one block per 15 min)
`HH:MM · tick · case A/B`, then: a metrics table (M1-M8, actual vs book, n); **PROPOSE** lines inside the bands (`knob: old → new ·
evidence (n) · expected effect`); **ESCALATE** lines for the Chief (EV, cost, action); "no change" when nothing passes the samples.

## 6. Advisory analysts on Sunday (Chief's ask) [L, from their Saturday output]
| Analyst | Saturday | Keep? |
|---|---|---|
| **Judge** (Opus, 53 commits) | keep/kill review of our own strategies; caught the trading loop failing (unknown_card ×5, network errors) and our flat neg_points | **Keep, every 30 min.** The only one that audits our own processes |
| **Scout** (Sonnet, 164 commits) | live top-3 actions; useful when it reads bids/asks, but repeats directives and proposes unverified items (e.g. selling MAL-09/10 we don't hold) | **Keep at 15 min, filtered:** only actions with verified holdings (/api/me), no repeats of directives |
| **Strategist** (Opus, 19 commits) | thesis-level; its core claim ("real trades: room for +10.7 of 22.5") contradicts the measured cap (+5 board, field-normalised: score-model §3h) and mixes board and round units | **Drop** (or once at 09:00). It changes slowly and risks steering toward an unmeasured 22.5 |
All three commit every ~5 min: cut to their cadence above to reduce git churn on the shared tree.

## Live log

### 13:41 · LAST CALL before the ≈ 14:00 dealer close
- Our ladder hasn't moved since tick ≈ 1822 (0.364). **Chato L2 is still empty for us; t03 is filling its own (MAL-06 at 18, LAT-07 at 13).**
  If a spare uncommon exists: sell to Chato at 14-16 now (≈ +1.8 Sunday ≈ +0.7 final). Never buy from Chato.
- Standing (final basis): us 93.15 · t12 85.43 · t10 84.65 · t03 84.62 (lead ≈ 7.7). Next: the Grand Final ≈ 14:00 (one duelist, f57a002).

### 13:14 · LADDER MAX BEFORE 13:55 (Chief's ask) · ladder now 0.364
| Dealer (level, full slot) | Our best 3 | Gap | Action at ≥ 0 (never above our value: losses count in full) | Gain |
|---|---|---|---|---|
| Abuela L1 (0.022) | CHA-01/02/03 ≈ full | none | none | 0 |
| **Chato L2 (0.044)** | **EMPTY** | 3 slots | **SELL spare uncommons at 14-16** (> opening 13). **Don't BUY**: his floor = list, and our 18 buys at list scored 0 | **≈ +0.09 raw ≈ +1.8 Sunday ≈ +0.7 board** |
| Pilar L3 (0.067) | 18 / 17 / 17 (≈ 0.33-0.49) | all weak | sell uncommons at **19-21** (share 0.6-1.0), each replaces a weak slot | +0.02-0.045 raw each (≈ +0.4-0.9 Sunday) |
| Pícaros L4 (0.089) | CHA-09 0.84 · MAL-10 0.91 · LAT-04 ≈ 0.65 | 1 weak | none at ≥ 0 (MAL-09 must come from a TEAM as the closer) | 0 |
| Ernesto L5 (0.111) | empty | 3 slots | none at ≥ 0 (our CHA-11 is worth 288 vs ≈ 118 there; legendaries list at 585) | 0 |
**PROPOSE:** (1) Chato: 3 spare uncommons at 14-16. If we have none, buy first-copy LAT uncommons from non-rival teams at ≤ 12 on v10 / El Rastro and
sell them to Chato at ≥ 13.5. (2) Pilar: next uncommons at ≥ 19. Dealers close ≈ 14:00 (warning 13:48).

### 12:22 · tick ≈ 2170 · CORRECTIONS
- **No Sunday cap of 50 on team trades** [V: RET-03 sale → neg 50.0 → 52.2]. Positive team trades count again: a first copy bought at ≤ value,
  a spare sold at ≥ value. **MAL closer GO** (score-model §4.14): MAL-09 ≤ 49 at the Pícaros, then MAL-07 LAST from a non-rival team at ≤ 13.5.
- **Venue rule (hard limit):** none of our offers on rival venues (**v07 t10, v02 t12, v28 t18, v20 t03**). Our RET-03 sale settled on v07 and fed
  t10's real trades. Use v10 (club pairs: our VC) or El Rastro.
- **Chato L2 slots are EMPTY for us:** sell spare uncommons at 14-16 (> opening 13). Upgrade Pilar at ≥ 19. (t03 is filling every dealer.)

### 10:46 · snapshot 1802 (phase ≈ 0.53)
- Pícaros SELLS: LAT-04 at 5 (1794) and spare LAV-04 at 5 (1800), both at ≥ value, 0 neg → ladder 0.253 → **0.311**. The Pícaros' best 3:
  CHA-09 (0.075) · MAL-10 (0.081) · a common sell (≈ 0.03-0.06).
- **PROPOSE:** MAL-09 at the Pícaros ≤ 49 now **upgrades** the common slot (share ≈ 0.9 vs ≈ 0.4-0.65: passes the +0.10 rule). No more common sells
  to the Pícaros (they'd be a 4th deal that doesn't upgrade).
- Board: us 32.43 (+0.30), 0.29 behind t10 and 0.42 behind t18. Projection §3k: #3 ≈ 3 away on the final basis. v10 is still 0 trades.

### 10:36 · snapshot 1762 (phase ≈ 0.47)
| Metric | Actual | Book | n | Note |
|---|---|---|---|---|
| M1 Pícaros MAL rare | **MAL-10 at 46** (tick 1757) | target 44-48, accept ≤ 49 (our value) | 1 | **contradicts the 07:25 premise** ("0 of 8 Saturday finals < 57"): a ≤ 49 MAL buy CAN fill |
| M2 ladder | 0.172 → **0.253** (+0.081 ≈ 0.91 of an L4 slot) | full 0.089 | — | Pícaros best 3: CHA-09 (0.075) + MAL-10 (0.081) + one slot open |
| M4 trades | neg **50.0 flat**: the RET-11 sale (240, tick 1730) added 0 | — | — | **working rule: Sunday team-trade gains capped at 50 per round** (score-model §3j) |
| MAL page | holds 01-06, 08, **10** · missing **07, 09** | — | — | under the 50 cap a MAL closer adds 0 trade points: buy MAL-09 only at ≤ 49 (L4 slot #3) |
**PROPOSE (in the bands):** MAL-09 at the Pícaros at ≤ 49 (the third L4 slot, 0 neg). No MAL-07 above value.

### 10:11 · tick ≈ 1665 · snapshot 1662 (phase 0.35)
| Metric | Actual | Note |
|---|---|---|
| Our deals | **none since tick 1585** (25 min): neg 50, ladder 0.172, cash 373 | relative scoring: idle = slipping (board −0.27 per snapshot) |
| M6 v10 | **0 trades today, mm 0**: the Sunday real-trades part (up to 7.5) is untouched | the RET-09 / club pairs never fired |
| Open offers | **RET-11 → t02 at 240 on El Rastro** (1663; ≈ +42 np if it fills, the taker pays the fee) · fodder bids LAT-06/07/08 at 9 (v15) | OK in the bands |
| M8 Sunday (±1) | t18 29.7 · t13 23.8 · t03 20.8 · **us 19.8** · t12 16.0 · t10 9.7 | running: t10 59.80 · t12 58.28 · t18 57.36 · **us 55.43** · t03 51.86 |
**ESCALATE:** v10 pairs are the largest idle lever: ≈ +2.6 EV, up to +7.5 Sunday, 0 P, and they squeeze t10/t12's top-3 mean. Fire the
pre-agreed pairs now (RET-09 → t09 first). Duels III ≈ 11:00 will absorb attention.

### 09:57 · snapshot 1602 (phase 0.28)
| Metric | Actual | Note |
|---|---|---|
| M5 trade cap | +50 np moved our Sunday round ≈ 11 → 20.6 (+9.6). Before Duels III the trade part is on a 15 scale (×0.6 once duels score) → **N ≈ 78 [L]: NOT capped** | more positive team trades still add directly |
| M8 Sunday round (±1) | t18 30.0 · t13 24.1 · **us 20.6** · t03 20.2 · t12 16.6 · t06 13.9 · t10 10.2 | running totals: t10 59.19 · t12 57.26 · t18 55.18 · **us 54.13** · t03 50.10 |
**PROPOSE:** keep pushing positive team trades. **RET-11 → t13 at ≥ 248 is worth ≈ +5-6 Sunday pts now** (≈ +3-4 after the duel rescale).
SAL-03 watch: t15's public ask at 7 (t03's SAL closer) expired unfilled at tick 1593. If it relists, ask t15 to pull it.

### 09:52 · tick 1586 · case J
- **CHA page CLOSED with the +50** [V me.jsonl: neg_points 0 → **50.0** at tick 1585]. Route: CHA-06 from Abuela at 22 (1553), CHA-07
  from the Workshop, **CHA-05 last from t02 at 72 on El Rastro** (team trade, closer). Cash 373. Pages 3 → 4 at the next snapshot.
- t06 closed CHA at tick 1586 via **Abuela** (CHA-05 at 9): a dealer close, so **no bonus** for t06. t18 closed via t13 (team): +50.
- Next 0-P / trade items: **RET-11 → t13 at ≥ 248** (up to +50 more, but our trade part may now be near its cap: M5 test on the next
  positive team trade); v10 pairs (mm still 0); fodder to Pilar at ≥ 19; MAL gate at ≈ 12:00.
**PROPOSE:** none new. **ESCALATE:** none (the closer is done).

### 09:41 · tick 1544 · case J (snapshot 1542, phase ≈ 0.20)
| Metric | Actual | Book | n | Note |
|---|---|---|---|---|
| M3 CHA held | **7/10**: 01, 02, 03, 04, 08, 09, 10 (09 Pícaros 55, 10 from the pack) · missing **05, 06, 07** (07 may be the Workshop uncommon: check /api/me) | 10 | — | cash 467 |
| M3 team-bid fills | **0 fills in ≈ 100 ticks**; live bids CHA-05 at 9, CHA-06 at 22 (public, El Rastro) · **no live CHA asks anywhere**; the only CHA team trade today: t13 → t18 CHA-01 at 72 | public caps 54/22/9 | 2 bids | the step-up trigger needs a live ask in the cap: none exists |
| M1/M2 Pilar fodder | LAT-06 at 18, LAV-07 (spare) at 17 → shares ≈ 0.4 / 0.2 | target 19-20 | 2 | n = 2 reached: next Pilar fodder target **≥ 19** (band) |
| M4/M5 trades | neg_points **0** | — | — | we have no team trade yet; t18 has its +50 closer |
| M8 Sunday round (≈ ±1) | t18 ≈ +25 + its closer (rising) · us ≈ +10 · t03 rising (+0.90 board) · t10/t12 ≈ 0 | — | — | |
**PROPOSE (inside the bands):**
1. **CHA-06 → Abuela at 20-21 (accept ≤ 22) now**: the C+45 fallback in the book is due, with no team seller in sight.
2. **CHA-07**: if /api/me shows it missing → Abuela after CHA-06, same band.
3. **Pilar fodder: hold ≥ 19** (two sales at 17-18 gave only 0.2-0.4 shares).
**ESCALATE (Chief):** **CHA-05, the closer, can only come from a team, and no ask exists.** Addressed request to **t13**
(it sold CHA-01 to t18 at 72 on El Rastro) at ≤ 72 incl. fee. It's our only +50 route today; ask in the same message as RET-11 at ≥ 248.

### 09:25 · tick ≈ 1490 · case J (round 3 since tick 1446; snapshot 1482, phase 0.12)
| Metric | Actual | Book | n | Note |
|---|---|---|---|---|
| M1 Pícaros CHA rare | CHA-09 at **55** (tick 1472) | ≤ 57 → 60 → 62 (07:25) | 1 (ours) + t18 at 58 | inside the band |
| M2 ladder share | 0.075 raw = **0.84 of an L4 slot** | full = 0.089 | 1 | good |
| M3 CHA held / spent | 1 of 10 · 55 P (cash 487) | ≈ 330 P plan | — | CHA-10 next at the Pícaros |
| M6 v10 | 0 trades, mm 0.0 | RET-09 pair | — | the pair hasn't fired yet |
| M8 Sunday round (≈ ±1) | us **≈ +12.3** (negotiating; ladder vs a tiny early reference) · t03 +5.8 · t10/t12/t18/t06 ≈ 0 | — | — | early numbers shrink as the field deals |
**PROPOSE:** no change (n < 3 for every band). **ESCALATE:** none. Watch: t18 is racing the same CHA rares (CHA-09 at 58); t18 bought
CHA-06 from Chato at 31 (above list 26: no ladder for it).
