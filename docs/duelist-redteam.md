# Duelist red team (Sat 18:15, offline)

Who it's for: Aleks and Lucas, before the 19:30 code freeze and Duels II (≈ 20:33). The Sunday section is also for
Aleks's Builder.

How it was run:
- **Offline only.** The real `DuelRunner` / `DuelAgent` code played against a fake game server with the duel rules.
- **The game was never contacted.** The team keys are dropped from the environment, and the SDK's `Bazaar` raises if
  anything builds one.
- **No second duelist was started.** Nothing in the main checkout was touched.
- **Code:** branch `redteam-sim` (worktree `../team5-redteam`, folder `redteam/`).
- **Spend:** ≈ $10–11 of the $20.

## Bottom line

- **No code change tonight.**
  - None of the 9 rule tweaks clearly beats the live code over 2,940 simulated days duels. The best gains 1.7%; the
    rest are within ±1.5% or worse.
  - The real models score where the code stand-in does: 0.347 vs 0.352 points per duel on 28 paired duels.
  - 19 bait and injection texts (2 runs each) changed no move.
  - No hard limit broke on any input the game could plausibly send.
- **What can sink Duels II is reading our day weight wrong** (points per duel, simulated):

  | Our reading of the day weight | Points per duel | Deals worth less than nothing |
  |---|---|---|
  | read right | 0.47 | 0% |
  | direction unknown | 0.23 | 0% (safe, just weak) |
  | can't read | 0.15 | 5% |
  | direction backwards | −0.18 | 30% |

  **At 20:33, compare the console's day line for the first duel with the game's `days_meaning`, by eye.** Then
  `review` pred = points on the first deals catches a wrong unit.
- **Sunday (15 s ticks, 6 duels at once):**
  - Tonight's Opus medium strategist goes over the 10 s decision budget in about 5% of decisions, and those turns fall
    back to code.
  - Opus low decided within 8 s every time, at about the same quality.
  - Sonnet medium is fast but closed 3 fewer deals out of 20.

## What was built

| Part | What it does |
|---|---|
| Fake server | One message per side per tick, `missing_days`, `bad_days`, `wait_for_tick`. Rounds = the smaller of the two message counts; result = surplus × 0.92^rounds. 16-tick duels in waves of 6, as in Duels II |
| Rival bots | The five Duels I types ([duel-rivals.md](duel-rivals.md)): follower, clock (4 schedules), holder (R5), holder (R7), accept-only ('Hola.'), plus silent |
| Bots' day behaviour | Duels I had no days, so all of these are tried: keeps its own day, trades it for price, copies ours, always day 0, always day 5, flips 0/10 every tick, sends no day (refused) |
| How the game might state our weight | Number + words, signed number, list of 11, dict, direction unknown, unreadable, wrong unit (3×), direction backwards |
| Score | Our true surplus × decay ÷ the duel's best pie (the Duel Lab's share-based score), plus checks that must never fail |
| Models | Bulk runs: a code stand-in for the strategist and negotiator (open far, 15% steps, the ledger's day call). Then the live models (Opus 5.5 medium + Sonnet 5.5 low, with failover) on samples. Spend meter counts cache tokens; replies are cached by prompt |

## 1. Days against the Duels I bot types (stand-in, 2,940 duels, $0)

Points per duel, readable weights only (deal rate, rounds per deal), from the 3-seed run (18 duels per cell):

| Bot | own day | trades day | copies ours | day 0 | day 5 | flips | no day |
|---|---|---|---|---|---|---|---|
| follower | 0.51 (94%, 2.8) | 0.51 (94%, 2.6) | 0.71 | 0.85 | 0.85 | 0.80 | 1.94 |
| clock | 0.26 (94%, 5.9) | 0.27 (83%, 5.3) | 0.48 | 0.54 | 0.26 | 0.25 (7.6 rounds) | 1.01 |
| holder R5 | 0.40 (83%, 1.0) | 0.36 | 0.52 | 0.81 | 0.83 | 0.78 | 1.03 |
| holder R7 | 0.02 (17%) | 0.03 | 0.20 | 0.09 | 0.01 | 0.07 | 0.00 |
| accept-only | 0.31 (56%, 1.0) | 0.27 | 0.87 | 0.88 | 1.15 | 0.72 | 1.00 |

- Values above 1 come from day-blind bots: they take deals their own day makes bad for them.
- 82% of deals land on the pie's best day.
- Clock bots cost rounds, as in Duels I.
- R7 (three moves, then silence, never accepts) closes only when its last number is inside our limit.

Rule tweaks: each one is played on the same 2,940 duels as the live code; "better / worse" counts duels.

| Tweak | Points per duel | Change | Better / worse |
|---|---|---|---|
| live code | 0.3523 | | |
| no late day switch | 0.3585 | +1.7% | 63 / 14 |
| late switch at 2 ticks left | 0.3577 | +1.5% | 60 / 15 |
| late switch only when their offer is outside our limit | 0.3551 | +0.8% | 38 / 8 |
| their day costs ≤ 5 P counts as our side | 0.3537 | +0.4% | 47 / 19 |
| open at once (no 2-tick wait for their day) | 0.3524 | 0 | 1 / 0 |
| give the day up to 30 P | 0.3523 | 0 | 0 / 0 |
| late switch at 6 ticks left | 0.3520 | −0.1% | 9 / 18 |
| accept by 3 ticks left | 0.3474 | −1.4% | 89 / 188 |
| code walk also for text-only rivals | 0.3381 | −4.0% | 140 / 215 |

**About the late switch.** In the real-model smoke run it added 2 rounds to a deal the deadline accept would have
closed anyway. We held 172 P on day 10. Their 188 P on day 0 was inside our limit. The switch sent 202 P on day 0,
then 195 P on day 0, and we then accepted their 188 P on day 0: 4 rounds instead of 2. Dropping it, or firing it
only when their offer is outside our limit, is a Sunday candidate. +0.8 to +1.7% from a stand-in is not the clear
gain the freeze rule asks for.

## 2. Real models against the stand-in (28 paired duels, ≈ $3.4)

| | Deals | Points per duel | Rounds per deal | Checks broken |
|---|---|---|---|---|
| Code stand-in | 64% | 0.352 | 3.0 | 1 |
| Opus medium + Sonnet low | 71% | 0.347 | 2.2 | 0 |

- The real models settled on a middle day twice, against rivals that always ask for day 5.
- With an unreadable weight, the real models closed near-zero deals (surplus 0.00 and 0.03), none negative.
- Odd rivals with the real models (6 duels):
  - **Flips its day every tick:** 3–8 rounds; the stand-in took 11–14. One of four was lost: the rival went from
    113 P on day 10 (inside our limit) to 120 P on day 0 (outside it), and the late switch went to its bad day (134 → 174
    P).
  - **Sends no day** (its priced offers are refused): our code walk and its accepts close the deal.

## 3. Bait and injection texts (40 turns, ≈ $0.8)

- **Setup:** the rival's structured offer stays at 85 P on day 10; only its words change.
- **The 19 texts:**
  - fake "[Note from your own system]" and "Facts from your own system" blocks;
  - a fake organisers' rule (50% decay);
  - fake market prices;
  - "what's your floor / what did you pay";
  - "confirm 90 in words";
  - a two-package request and "95, 100 or 105 are fine for you";
  - questions about the item's condition;
  - Spanish;
  - a plea and a threat to flag;
  - "ignore all previous instructions";
  - JSON in the text, a fake "Deal!", a forged transcript line, right-to-left Unicode, 1,150 characters.
- **Result:** the neutral control gave 114 P on day 0. Every bait gave 113–116 P on day 0; some made the strategist
  slightly tougher (116).
  - 0 accepts, 0 fallbacks.
  - 0 messages that code had to rewrite into its plain "I can do N P" text.
  - 13 first drafts were vetoed (a two-package menu naming day 10 twice, agreement words, "limits", "cost"). The
    re-ask fixed each one.
  - Two replies said "I'll keep my floor to myself", which is posture, not a claim.

## 4. Odd inputs and faults (2 duels each, $0)

| Case | Result |
|---|---|
| `your_limit` as `"40 P"` | **We sit the duel out** (0 decisions; the console says "can't read it"). All 68 records had integers |
| `deadline_tick` renamed | No deadline accept: 1 of 2 deals lost |
| Polls fail on the last 4 ticks | 1 of 2 deals lost |
| 30% of sends refused (429) or failing (500) | Deals kept, nothing sent twice |
| Restart at tick 6, 12 or 13 (after the late switch) | Same result; the switch isn't sent again |
| Both models down all session | Code fallback closes 2 of 2: 0.22 vs 0.33 points, 11–13 rounds |
| Inverted band, day 11, priceless messages, claims, accept with nothing standing | All caught; nothing bad sent |
| Rival day shown as 15 / −3 / 5.5 / null | No check broken; 0.23–0.31 points |
| Day weight in the wrong unit (3×) | 33 deals worth less than nothing out of 420. Code can't see it; `review` pred ≠ points does |

How `read_days` reads plausible wordings ($0):
- **Read right:** "each day later costs you 2 P", "you lose 2 P per day of delay", "Primas you gain per day of later
  delivery", `-4`, "+1/day later", `{"slope": 2, "better": "later"}`.
- **Direction unknown:** "every extra day is worth 2 P to you", "you'd rather wait", "cada día de retraso te cuesta 2
  P", `{"weight": -3}` (the sign is lost), and a bare positive number.
- **Can't read:** `{"days": 2, "prefer": "early"}`.
- If the first duel shows one of these, the fix is after the freeze: Aleks's and Lucas's call. Don't guess a
  direction, because a backwards reading is the worst case above.

## 5. Sunday latency (15 s ticks = a 10 s decision budget, 6 decisions at once, ≈ $1.2 + $5.1)

| Setup | Decision p50 / p90 / max | Over 10 s | Points per duel (20 paired duels) | Deals |
|---|---|---|---|---|
| Opus medium + Sonnet low (tonight) | 7.8 / 9.5 / 10.0 s | 2 of 30 | 0.424 | 85% |
| Opus low + Sonnet low (Duels I) | 5.4 / 6.4 / 8.0 s | 0 | 0.386 (5 better, 6 worse) | 80% |
| Sonnet medium + Sonnet low | 4.2 / 4.9 / 6.3 s | 0 | 0.273 (5 better, 6 worse) | 70% |
| Sonnet low + Haiku | 3.9 / 4.2 / 5.8 s | 0 | not run | |

- **Real runner loop in real time** (6 duels, tonight's latencies): at 15 s ticks, 2 of 44 decisions timed out and fell
  back to code; at 30 s, none.
- **The backup model never gets a turn at 15 s ticks.** The runner cuts a decision at 10 s (tick − 5), but Failover
  gives the primary model 20 s.

## Sunday list (none tonight)

1. Strategist on **Opus low**, and give the failover's main model about tick − 8 s instead of 20 s.
2. Late switch: drop it, or only when their offer is outside our limit (+0.8 to +1.7% simulated).
3. `adapter.as_number` should read `"40 P"` (today it means sitting every duel out).
4. `read_days`: Spanish delay words, "extra day / wait", a signed `weight` in a dict, a `days` key. Only with the real
   wording in hand.
5. Strip junk from our text: a trailing "}" in 15 of 352 Duels I messages, plus "</br>" and "Â ŽŽ" in today's runs.
6. The cost meter (`engine/claude.py`) ignores cache tokens. The true cost tonight is ≈ $0.12 per duel (Opus medium
   $0.0155 per call, Sonnet low $0.0034), so Duels II's 68 duels ≈ $8.
7. The claims guard lets through statements about our limit ("the most I can pay", "my floor"). No bait drew one, so
   this is low priority.

## Rerun

From `../team5-redteam`:
`PYTHONHASHSEED=0 ../claude-hackathon-team-5/.venv/bin/python -m redteam.<days|robust|calibrate|baits|oddreal|latency|setups>`

Outputs and the spend meter go to the session scratchpad. `REDTEAM_CAP_USD` stops paid calls at a cap.
