# Chief of staff handoff (Sun 00:10). A new Chief session reads this first

**Role:** the only session Lucas talks to; decides inside the limits; writes `intel/directives.md` (newest on top);
routes by SendMessage; never writes to the game (the Operator does). Reply in Lucas's language (rioplatense), brief,
[V]/[L]/[?] labels; an independent verifier before any directive that moves > 20 P or changes a rule. Lucas wants #1.
Messages to other teams: transactional only, never our strategy (memory: no-strategy-leaks-to-rivals).

**Sessions (ListAgents):** Operator `-3d` (only game writer; overnight Dealer Lab → intel/dealer-lab.md; 08:45
checklist) · Builder `-ce` (reactor/FLIP/matchmaker/hints/eggs; branch `duelist-loop` for Aleks; Red Castiza build
PAUSED until Lucas approves in its session) · Market `-27` (intel/market-sunday.md, club forecast) · Analyst `-6c`
(intel/score-model.md §4: scoring fit, t10 decomposition, Sunday Monte Carlo) · Duel Lab `-38` (intel/duel-lab.md:
FINAL params for Duels III) · pitch `-a1`/`-a5` (judges/pitch/final/) · Aleks on his Mac (reads PLAN.md block #1-31).

**Standing (Sat close, tick 1445, paused):** t10 37.74 · t18 30.98 · t12 30.56 · **us 30.49 (#4)** · t03 29.81. Game total
(0.5·Fri + Sat): t10 leads us by ≈ 9-10.6 [L]. 70% of t10's lead = market value created on its v07 (our 10:18
venue deal fed it). Our mm turned +2.2 at the close (field-relative) → ≈ +0.7-2.2 board at the next snapshot [L].
P(#1 final) ≤ 9%, P(top 2) 21-45% [Analyst, L].

**Sunday facts:** +150 P at 09:00; Don Ernesto open to all since Sat tick 1091 (no neg-safe Ernesto deal for us: skip L5, dealer-lab-ladder §6); Sunday ticks 15 s [V]. The clock is paused at game 13.367
in ROUND 2 (Saturday): if it RESUMES, ≈ 1.5-3 h of Saturday's round remain (hard Market Test 14.65, bench 15.0)
before round 3 + the CHA release at 16.65; if it JUMPS, Duels III ≈ 10:00, Final ≈ 11:30, close ≈ 12:00 [L].
The Operator reads /api/clock + /api/schedule at 08:55. Duels III/Final: 12 ticks, 10% decay, 4 at once [V].

**Plan files:** intel/sunday-plan.md (timeline, cash, guardrails, Saturday-tail rules: v10 pairs first, no ladder
until round 3, no cash team trades in the tail) · intel/cha-plan.md (team bids first; CHA rares from Pícaros 48-52;
last card from a TEAM for +50) · intel/dealer-lab.md (per-dealer playbook, castizo scripts, ladder plan) ·
intel/duel-lab.md (Duels III params) · intel/market-sunday.md (club pairs, test plan) · score-model §4 (Analyst).
Ladder fit [L]: Σ dealers level × (best-3 share sum)/45 → Ernesto counts 5×, Abuela 1×.

**Cash:** 392 + 150. CHA ≈ 330 (floor 0 for CHA only) · MAL close (we hold MAL-01..06, 08; need 07/09/10; Team 15's
spare MAL-07 = the last card) · ≤ 75 club bonuses (if approved) · 50 reserve. Open: SAL-11 bid 20252 (115 → t04),
LAV-03 → t04, LAV-04 → t01. Reserved: all SAL, LAV, RET page cards, RET-11, MAL-01..06/08.

**Club Castizo / Red Castiza:** 6 members t07, t09, t08, t15, t04, t02 (+ maybe t13); page
https://claude.ai/artifact/9HVLftiHAKMwgPwTQbLff1 (private: Lucas shares). Bonus tiers 1/2/3/5 P (+3 page close),
cap 15/team/day (directive 22:55) — Chief's advice: cash bonuses OFF until the desk confirms fair play ("volume and
friends count for nothing"). Venue rotation by value: big deals on v10 (≥ 75% of club VC). Want-lists empty.

**Do not:** sell page cards; dealer-to-dealer flips; ladder deals in the Saturday tail; trade on rival venues (v07
etc.); help t10. Eggs/badges don't score (we have Sharp ear, Trickster tricked, Castizo + MAL-06 gift).

## Overnight program (Sun 00:20) → everything lands by 06:30-07:30; the Chief merges it at 06:41 into intel/sunday-final.md
| Who | Job | Output |
|---|---|---|
| Auditor A (no context) | why we lost Fri/Sat vs t10/t06/t18/t12, 10 lessons | intel/audit-why-we-lost.md |
| Auditor B (no context) | red-team + aggressive per-stage plan, both clock cases, rival slow-down | intel/sunday-redteam.md |
| Auditor C (no context) | Market Test + real-trades scoring, board venue or not | intel/market-test-audit.md |
| Auditor D (no context) | code audit of origin/duelist-loop, tests, go/no-go | intel/duelist-audit.md |
| Auditor E (no context) | club contrarian review + final one-pager + per-team pitches | scratchpad club-castizo.html, intel/club-pitch.md |
| Duel Lab -38 | t10-style opponent, 15 s latency, config sweep → SUNDAY v2 | intel/duel-lab.md (top) |
| Market -27 | per-team bot negotiation models, CHA/MAL bid ladders, 09:00 v10 pairs | intel/market-sunday.md (NEGOTIATION) |
| Analyst -6c | per-stage EV both cases, cash split, deny list, P(#1) levers | score-model §4-5, intel/deny-list.md |
| Operator -3d | CHA + MAL fast-start books (dry run), 08:45 checklist, 08:55 clock case | run/cha_book.json, run/mal_book.json, dealer-lab §FAST-START |
| Builder -ce | tools/club.py: waits for Lucas's approval in its session | run/club_orders.json, intel/club-orders.md |
