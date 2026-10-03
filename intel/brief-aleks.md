# Aleks — Saturday brief (read this first; then PLAN.md "RIGHT NOW" and intel/saturday-plan.md §1 and §4D)

## The game in 30 seconds
100 points: Negotiating 30 (duels + dealer ladder + trades between teams) · Market-making 30 · Judges 40. Friday counts
20%, Saturday 40%, Sunday 40%; scores are relative to the field. **Duels are ours to win inside Negotiating**: ~102
scored duels today (Duels I: 34, Duels II: 68), more on Sunday. Lucas runs trading, dealers and the market; Dani runs
the organisers' desk, the room and the judges' story. Nobody else touches the duelist.

## Your day (times: clock JUMPS to hour 4.0 at 09:00 / RESUMES at 2.65 — Lucas confirms at 09:00)
| When | What |
|---|---|
| 09:00-11:00 | Duelist fixes below, each with a regression test on `docs/duels/`. Push small commits. |
| before Duels I (11:30 / ~12:51) | `uv run --project . pytest -q`: all tests green → start `agents/duelist/supervise.sh`. Laptop on mains + `caffeinate`. |
| during Duels I | Watch `intel/duel-review.md` (written after every wave by our duel monitor) and the alerts. Tune between waves. |
| 13:00-17:30 | Duels II prep (`days`), using what Duels I taught you. |
| Duels II (18:00 / ~19:21) | Same loop. |
| Sunday | 15 s ticks: Sonnet as strategist (Opus peaked at 14.2 s against a 10 s budget). |

## What we know (measured on Friday's 30 practice duels) [V]
- result = our surplus × (1 − decay)^rounds, where **rounds = min(our priced offers, theirs)**. Silence costs no decay.
- 11 deals of 24 finished; 9 of 12 closed when the rival spoke; ~14% of value lost to decay (duel 175 lost 31%).
- Two "silent" rivals accepted our opener (164, 258): some rivals are accept-only bots.
- Duel 181: their 73 sat inside our 85 limit from tick 141; we never decided again → lost ~10.6. Cause: `runner.due()`
  only fires on rival changes; the last-tick trigger was removed in revert 00f94c0.
- Duels 103/104: both sides held 10 ticks to the deadline.
- Prompts say decay is "per tick" (`agent.py:148,178`, `prompts/negotiator.md:11`, `prompts/strategist.md:26-28`): wrong.
- Anchors (seller ~1.45-1.65× limit, buyer ~0.6×) drew instant accepts and no walk-aways: keep them unless data says no.

## Fixes before Duels I (your call on the exact numbers; these are the problems to solve)
1. Decide on time, not only on rival moves: at `ticks_left ≤ 3` always decide; at ≤ 2 accept any in-limit standing offer
   in code.
2. Close by sending the rival's own standing price from `ticks_left ≤ 4`, so THEY spend their accept (avoids collisions
   when several duels end on the same tick).
3. Don't pay another round of decay for a small gap: accept an in-limit offer when the gap is small relative to what one
   more round costs (≈ 2d/(1−d) × our surplus).
4. Break mutual holds after ~3 still ticks.
5. Silent rivals: concede on a schedule toward a floor (silence costs no decay; a deal beats 0).
6. Fix the decay wording in the prompts; read session parameters from the payload, not hard-coded.

## Hypotheses to test live (and log what you learn in team/aleks.md)
- How fast do rivals concede, by rival alias? Does opening harder pay at 6% vs 8% vs 10% decay?
- Duels II `days`: the payload shape (`your_days_weight`, `days_meaning`) was never seen: test a number / list / dict
  offline first; concede days that are cheap for us in exchange for price.
- Is a duel accept counted against the team's 1 accept per tick? (desk question Q6 — Dani asks at 09:00.)

## Hard guardrails (the only rules that must never break)
- **Never two duelist processes** on the team key (one host; a stopped cold standby copy on Lucas's machine only).
- **Never accept or offer outside our limit**: limits are enforced in code, the LLM only writes the words.
- **Tests green before every start**; a failing test means don't restart, tell Lucas.
- Check your Anthropic key's spend limit before 11:00 (Console → Settings → Billing → Spend limits).

## How we stay in sync
- You write `team/aleks.md` (Now line + one log line per change/result). Lucas's sessions read it on every prompt.
- Our **duel monitor** watches every live duel and pushes Lucas and Dani on: an in-limit offer not accepted near the
  deadline, a deal outside the limit, our side silent while the rival offers, a deadlock. If Dani comes to you with an
  alert, look at the duel id it names.
- After each wave the monitor appends a review to `intel/duel-review.md` with concrete suggestions.

## First prompt for your Claude Code
> You are Aleks's Claude Code for Team 5. Read intel/brief-aleks.md, then PLAN.md "RIGHT NOW" (Aleks) and
> intel/saturday-plan.md §4D. Implement the duelist fixes with regression tests on docs/duels/ before Duels I; run all
> tests before any start; never run two duelist processes; keep team/aleks.md current.
