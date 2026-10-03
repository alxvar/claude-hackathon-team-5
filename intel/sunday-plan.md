# Sunday plan: win the 60 game points (Chief, Sat 22:00)

**Target [L, Analyst snapshot 1300]:** on 0.5·Fri + Sat, t10 57.5 · t06 48.8 · **us 46.3** · t14 43.0. Sunday is a full
round (60 points, weight 1). To finish #1 on the game score we must beat t10 by **> 11.3 Sunday points** (≈ 19% of the
round) and t06 by > 2.5. Judges (40) come after the 15:00 close.

**What the organisers told us (Payday deck, 21:00) [V]:** only deals score (a deal = value added − price paid + price
received); a team-trade gain counts up to 50, a dealer gain only on the ladder, losses count in full; the last card of
a page via a TEAM trade = +50, and selling a page card afterwards = −130; MARKET-MAKING 30 = Market Test 7.5 + REAL
TRADES 22.5 (value two other teams create on your market). A market gets used when it finds the missing card, swaps
without cash, finishes pages. "Zero fee alone is no reason; volume and friends count for nothing."

## ⚠ Saturday's round may continue Sunday morning (Analyst 23:40) [V clock paused at game 13.367 in round 2; L the rest]
The clock is paused in round 2. Before round 3 + the CHA release (game 16.65) come the hard Market Test (14.65) and a bench
(15.0). If the clock RESUMES at 09:00 (instead of jumping), Saturday runs ≈ 1.5-3 h more. Operator: read /api/clock and
/api/schedule at 08:55 and tell the Chief which case applies. In that window:
1. **v10 trades first**: our Saturday market gap turned positive at the close (mm −5.2 → +2.2, a field-relative hurdle), so
   ≈ +2.8 more VC caps us at +5 board = +4.2 Saturday points ≈ +1.7 final, for 0 P. Fire the club/v10 pairs at 09:00
   (RET-09 t07 → t09 first), not at CHA time. Duplicates → first-copy collectors only; a negative trade now costs.
2. **No ladder deals until round 3**: the Saturday ladder is capped. Keep RET-11, MAL-08 and the spares for Sunday's
   fresh ladder.
3. Positive team trades still count for Saturday (≈ 0.074 Saturday points per neg_point).
4. CHA starts at round 3 (16.65). The CHA plan's clock starts then.

## Timeline (wall times [L]; re-read /api/schedule and /api/catalog at 09:00)

| When | What | Owner |
|---|---|---|
| Sat 23:00-23:30 | Duel Lab Sunday notes (accept rule for harder decay, 15 s latency) → intel/duel-lab.md | Duel Lab |
| Sat night | Lucas + Dani collect want-lists by WhatsApp → intel/wants.md; pre-agree 3-5 v10 pairs/swaps for 09:00 | Lucas, Dani |
| 08:30 | Aleks: pull, full suite green, apply the Duel Lab Sunday notes if green, duelist up before 09:00 | Aleks |
| 08:45 | All daemons healthy (tools/daemons.sh status); matchmaker + reactor live; v10 at 0% | Operator, Builder |
| 09:00 | +150 P; CHA release (09:00 or ≈ 09:29 [?]); Don Ernesto open to all | — |
| 09:00 | First Pícaros thread: "Conozco el timo de la estampita…" (no tricks for the day) | Operator |
| 09:00-10:00 | **Market first mover:** the pre-agreed pairs post on v10 (buyers' open bids first; spares only); ads every 10 min; rebate 5/10 P (cap 80, non-rivals) | Lucas, Dani, Operator, Market |
| 09:00-11:20 | **CHA page** per intel/cha-plan.md: team bids first, dealer fallback at ≤ list (also ladder), the LAST card from a team (+50) | Operator (book) |
| 09:30-11:00 | **MAL close** if CHA is on budget: MAL-09/10 (Pícaros ≈ 60), MAL-06 (Abuela ≈ 20), LAST = Team 15's spare MAL-07 by team trade | Operator |
| ≈ 11:00-12:20 | **Duels III** (shorter clock, harder decay, 4 at once, 15 s ticks): Aleks at the screen; Analyst wave reports | Aleks, Analyst |
| all day | Zero-neg ladder deals (fresh Sunday ladder: best 3 per dealer); never a dealer flip; never sell a page card | Operator |
| ≈ 14:00-14:30 | **Grand Final** duels; all dealers close | Aleks |
| 15:00 | Doors close → 1 h to prepare the 3-min pitch (concept picked Saturday night) | Lucas, Dani, pitch session |

## Cash (≈ 392 + 150 = 542 at 09:00)
CHA ≈ 330 (floor 0 for CHA buys only) → MAL ≈ 160 if CHA comes in under budget → rebates ≤ 80 → reserve ≈ 50
(denial buys on the Chief's "DENY" line, cap 35). No legendary, no gold pack (dealer buys never score negotiation).

## Guardrails (unchanged)
Never sell a card from a complete page (LAV, RET, SAL; CHA and MAL once closed) · no offer on a rival-owned venue ·
rivals = live top 6 or within 3.0 of us (policy.rivals) · page-closers only for non-rivals ≥ 6 below us · messages to
other teams transactional only (no strategy) · one live bid per page-closer card.

## Levers ranked by Sunday points [L]
1. CHA page + team buys: +8-14 · 2. Duels III + Final: up to 12 (our 12/12 post-fix deal rate) · 3. v10 real trades:
+2-5 (maybe more: 22.5 unexplained) · 4. MAL close: +1.5-3 · 5. Ladder (fresh): +1-3 · 6. Small swaps: +0.3 each.
