# Sunday FINAL plan (Chief, Sun 06:45 draft → contrarian-checked 07:30)

_One page. It merges every overnight output: audits A-E, red team, adversary-t10, holdings, ops-contention, mechanics-hunt, Duel Lab SUNDAY v2 + the crosscheck, Market §0, Analyst §4, Operator §FAST-START. Directives 00:14-01:40 hold. [V] measured · [L] modelled · [?] open._

## Facts that drive everything
- **Scoring [V, deck slide 5]:** Negotiating 30 (duels · dealers/ladder · team trades) · Market-making 30 = **Market Test 22.5 + Real trades 7.5** · Judges 40. Final game = (0.5·Fri + Sat + Sun)/2.5, so **1 Sunday point = 0.4 final**.
- **Relative scoring [V ladder, L+ trades]:** each part is graded against the field's top-3 mean. Value past OUR cap still raises the reference and lowers rivals below it. So no "stop at the cap" for MAL, v10 VC or fodder; and **never sell below value** (it lowers the reference for everyone, so rivals gain).
- **Clock:** case **J ≈ 80%**: round 3 at ≈ 09:00 with 15 s ticks; CHA released at t+0; Duels III ≈ 11:00; Final + dealers close ≈ 14:00 (warning 13:48); freeze 15:00. Case **A ≈ 15%**: the Saturday tail resumes (≈ 197 min) before round 3. The Operator decides at 08:55 on `/api/clock` `round`.
- **Cash:** 392 + 150 = 542. CHA worst case 282 (the public bids are capped at the dealer price) → MAL ≈ 126 always fits → fodder float ≤ 60 → reserve.
- **Odds [Analyst, L]:** P(top 2) 13-15% (flip doesn't land) / 24-27% (flip lands); P(#1) ≤ 1-6.5%. The plan maximises expected points and the #2-#5 race.

## Stages, ranked by expected Sunday points (case J)
| # | Stage | Exp. Sunday pts | P | Owner | First action |
|---|---|---|---|---|---|
| 1 | **CHA page** (1.6 multiplier) | +7 (sd 3) | ≤ 282 | Operator | t+0 per dealer-lab §FAST-START: 10 public bids capped at dealer accept (9/22/54); Pícaros CHA-09 thread `--offer-only` at t+0, then CHA-10; silver pack after release (gate: ≥ 2 CHA missing); Abuela threads; LAST card = one pre-agreed, addressed post from a NON-rival (+50) |
| 2 | **Duels III + Final** | ≈ +7 with set C (+5.4 / +2.7 over today's setup) | 0 | Aleks | sha 29aa1be, set C, code policy, Haiku text, failover 8 s, AUTOSWITCH C → A once (≥ 12 spoke-duels and deal rate < 0.60); live by 10:30 |
| 3 | **v10 real trades** | up to 7.5 (full) | 0 | Lucas, Dani, Market | 08:30 WhatsApps: RET-09 t07 → t09 (+156 est., likely full marks alone) + SAL-02 t09 → t07, both on v10 addressed; then the Team 16 rows after the 08:30 rival check; no VC stop; zero negatives |
| 4 | **MAL close** | +1 own, plus −0.4-1.1 each for t18/t12/t03 | ≈ 126 | Operator | GO when ≥ 150 P is left after CHA: MAL-09/10 from the Pícaros ≤ 49, MAL-07 LAST from Team 15 (pre-agreed, addressed) |
| 5 | **Ladder fodder** | +1-2 | float ≤ 60 | Operator from the Analyst's live-tuning | LAT-06/07/08 maker bids ≤ 12 on v15 at t+0 (0 copies held); sell above opening: Pilar > 16 (19-21) first, Chato > 13; Workshop 3 LAV commons → 1 uncommon |
| 6 | **Market Test** | 11.25 (stall par) | 0 | — | Keep the stall v10. Lucas asks the desk at 09:00: "If one venue beats the stall's efficiency and nobody else does, does it get the full Market Test points for that session?" |
| 7 | **Denial (free)** | protects | 0 | all | Never sell a page card/CHA card to a rival; no deal with t10 as a party; no trades on v07; public bids never above dealer price; MAL-08 never sold |

**Case A (Saturday tail first):** v10 pairs only (Saturday points; our Saturday trade part is ≈ capped); no ladder deals; no cash team trades; CHA and the rest start at round 3. Duels and freeze times move with the schedule; re-read at 08:55.

## Hard rules for the day
- Only the Operator writes to the game; the duelist (Aleks's Mac) is the only other writer. One duelist process, ever.
- **Duel window:** at T−5 min before Duels III and the Final: `tools/daemons.sh stop trader swaps opps`; no new dealer threads, no book.json edits, no restarts; restart in order at `duels.finished`.
- Trader at 09:00: `CASH_FLOOR=464 tools/daemons.sh restart trader` (caps: --max-ratio 0.8, --exclude CHA-*,MAL-*); lower the floor as the books fill. Dealer bots restarted on main (TRICK guard).
- Live tuning: the Operator applies the Analyst's lines inside the bands (intel/live-tuning.md); anything outside the bands → Chief.
- Messages to other teams: transactional only (card, price, market). Club texts: market-sunday §0.5, never matches.md raw.
- Club: v10 hosts 2 of every 3 club (member ↔ member) deals; non-member deals go on v10 outside the rotation; no cash bonuses.

## Residual risks we could not close
1. Rival bots may change overnight (t10 did on Saturday); the duel sims fit Fri/Sat behaviour. Insurance: AUTOSWITCH C → A, plus `--rollback` to main.
2. Organiser rulings: the clock case and the above-stall Market Test payoff.
3. Single machine (Lucas's Mac runs the Operator, daemons and analysts): a network outage (22:50-23:24 last night) stops everything. The phone hotspot stays ready.
4. The club depends on other teams installing an accept rule; the 08:30 pairs are WhatsApp-agreed, so they don't depend on it.
5. CHA print runs and Pícaros bait-and-switch: rares bought at t+0, card checks in code and in simple_buy.py.
