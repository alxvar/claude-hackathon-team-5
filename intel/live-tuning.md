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
| Team-bid ladder: start / step / every_ticks | start ±2 steps; step ±1; every_ticks 20-60 | ≤ the book's `max` (rares 90, uncommons 30, commons 12); last card ≤ value − 50 | **≥ 2 bids unfilled for ≥ 80 ticks** while a live ask sits within `max` → +1 step; fills in < 20 ticks at `start` → next card's start −1 step |
| Which CHA card next | reorder the remaining cards by fill chance × gain | the LAST card stays a team trade (CHA-05/CHA-08 rule) | M3 after each fill |
| Ladder upgrade (replace a slot) | only if the new share ≥ old share + 0.10 | never a 4th deal at a level whose best 3 are full, unless it upgrades | M2 for ≥ 2 deals at that dealer |
| v10: next pair to fire; rebate per trade | pairs from `intel/matches.md`; rebate 5/10 P | rebate total ≤ 80 P; non-rivals only | one **negative** VC trade (mm_points falls) → stop that pair type at once (no sample needed: losses count in full) |
| Thread allocation | ≤ 6 open, duel windows first | 1 accept/tick, 5 rps shared | — |
| **Ladder fodder** (only once the Chief approves the pipeline) | team buys of uncommons/duplicates at ≤ our value; dealer sales at ≥ our value: Pilar target 19-20, Chato 14-16 | never a page card, CHA card or MAL-08; ≤ 3 deals per dealer level unless it upgrades a slot (+0.10 share); float ≤ 60 P | M2: ≥ 2 fodder sales at a dealer before moving its target ±10% |

## 3. Outside the bands → the Chief (the Analyst sends one line with EV, cost and evidence)

- Any price **above list or above our value** (it creates a loss), or a cap outside ±10%.
- **Trade surplus → ladder (a mechanic we don't use) [L]:** once M5 shows our trade part capped (a positive team trade moves
  negotiating ≈ 0, field drift removed), a dealer SALE below our value costs nothing on trades as long as the loss ≤ the surplus.
  Each sale buys a ladder slot. Candidate: RET-11 → Pilar (L3, ≈ +0.9-1.7 round pts at full share) at a loss ≤ the gain of the
  last trade that didn't register. One L3 slot lifts P(top 2) ≈ 27% → 34% (score-model §4.4). Needs the Chief's go each time.
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
_(empty until Sunday's open)_
