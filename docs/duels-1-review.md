# Duels I review and the plan for Duels II (Aleks, Sat 13:40)

For Aleks's 15:30 decision (PLAN.md #10, #14, #15), the Chief and the Analyst, and Aleks's Builder.
Data: our 34 records in `docs/duels/`, our duel points over time (`docs/duels/scores.jsonl`), the public feed in the
hub, and the Analyst's §1d in `intel/score-model.md`. Every counterfactual below accepts or keeps an offer the rival
**actually made**, so it is computed rather than modelled, unless it says otherwise.

## 1. What happened

- **30 deals in 34 duels (88%)**; the field closed 76% (85% without Team 11, whose agent never speaks).
- **13.93 duel points**: about 0.41 per duel. The points rose in jumps that line up with our deals closing. Each jump
  fits *our share of the gap between the two limits × 0.94^rounds* [L]. On 17 deals that closed alone in a scoring
  interval, our share averaged **0.58** (0.16 to 0.94).
- **Decay took 19%** of deal value (112 of 591 P) at 4.4 rounds per deal.
  - The 9 deals closed in 0-1 rounds kept 95% (25.4 P each).
  - The 8 deals that took 7-12 rounds kept 57% (8.5 P each).
- The four no-deals were unavoidable:
  - 2367: the rival never came inside our 72.
  - 2414, 2415 and 2523: silent rivals; 2414/2415 are most likely Team 11 [L].
- The Analyst puts our pure duel part at 8-9.5 Saturday points, against 10.8-11 for the cleanest teams: upper-mid, not
  top [L]. (My earlier "biggest negotiating gain among the top 8" mixed in ladder gains.)

### What decided our results
- **Soft rivals paid most, and they paid because our opener was ambitious.** 7 deals landed beyond 60% of our
  opener's distance from our limit: 2584 (49.8 P), 2585 (60.2), 2531 (42.3), 2534 (29.7), 2535 (33.6), 2447 (28.3),
  2446 (28.0, a silent rival that took our opener).
- **Some rivals concede twice quickly and then hold.** They move ~10 P twice, then sit, and our deadline rule takes
  their number: 2430, 2431, 2530, shares 0.16-0.24. Nothing we sent after their hold moved them.
- **Each rival team plays us twice with identical wording.** 8 pairs of consecutive ids match ("We can do N P. Thank
  you for the talk." in 2584/2585; "N?" in 2366/2367). The alias changes per duel; the wording doesn't. In Duels II each
  team plays us 4 times.
- **How rivals answer our steps** (112 rival moves; the fit is weak, R² 0.11):
  - their step ≈ 0.24 × ours + 0.06 × gap + 1.4;
  - our small steps (under 10% of the gap, mean 3.8 P) drew 5.5 P back;
  - steps of 10-25% of the gap drew 4.4 P for 6.5 P;
  - steps of a quarter or more of the gap drew 4.8 P for 7.5 P.

  When we sent nothing, they still moved 37% of the time (2.2 P on average). **Small steps at large gaps were good
  trades; big steps mostly gave price away; 1-2 P steps wasted rounds.**

## 2. What the data says about the proposals on the table

| Proposal | Tested on Duels I | Verdict |
|---|---|---|
| Accept the rival's first in-limit offer | 343 P vs our 479 | No: haggling paid (as the Analyst found) |
| Break-even accept (rival's last step < S × d/(1−d)) | 447 P (−31): helps once (2296 +3.2), hurts 5 times (2535 −25.8) | **Don't ship.** Rivals' steps are lumpy: a small one is often followed by a big one |
| Same, after two small steps in a row | 477 P (−1) | Neutral: not worth the code |
| Accept a rival that repeated its in-limit price | 449 P (−29) | No (2535 repeated our limit, then came down 43) |
| Anchor closer (opener at 60% / 75% of today's distance) | −82.5 P in 7 deals / −42.9 P in 5. Even 2 fewer rounds in all 12 long deals at the same price gains only +13.6 | **Don't.** The best deals came from rivals that met our ambitious opener |
| Merged rule: a step < max(3 P, ¼ of the gap) is held | Holds 96 of our 171 follow-up offers, including the small steps that drew 5.5 P back | **Keep the 3 P floor, drop the ¼** (use 5%) |
| Merged rule: after 4 priced offers, hold unless they move ¼ of the gap | 20 duels had more than 4 of our offers (162 P); in those worth 71 P the rival had no in-limit offer by our 4th offer | **Drop it**: the haggling after offer 4 is what paid |

## 3. Plan for Duels II (18:29: 68 duels, 6 at once, 8% decay, price + delivery day)

### 3.1 Delivery days: the biggest lever
The organisers' example: the seller gains +1 per day later, the buyer loses 4 per day later, so the pie is 50 at day 0
and 20 at day 10. If the score is our share of the **best** pie [L], a deal on the wrong day caps both sides: at day 10
the two shares can't add up to more than 40%.

Rules for the strategist, and the facts code gives it:
1. **Read the rival's day from its first priced offer.** Most rivals will propose their own best day.
2. **Same side as ours** (their day costs us at most 2 P): take their day at once. It's free for us, and the pie is at
   its biggest there. Then haggle price only.
3. **Opposite side:** C = what their day costs us (from our day table).
   - **Give the day** when our weight is low:
     - the rule: C is small next to the price at stake, or our weight sits in the bottom half of the weights we've
       seen this session;
     - before we have data: |weight| ≤ 1.5 P/day, or C ≤ 15 P;
     - how: offer their day with the price moved by C plus a premium of about C (seller up, buyer down), in the
       first or second message.

     Our worth never drops (`guards.worth`), and the bigger pie is shared.
   - **Hold our day** when our weight is high, and offer up to about C/2 in price to keep it.
   - **In between:** offer a menu in words ("day 0 at 120, or day 10 at 105"). It costs no extra round, and their
     next offer shows which they value.
4. **Never settle on a middle day** when weights are linear: the pie is largest at a corner, and day 5 throws away half
   the gain.
5. **Settle the day within the first two messages, then never move it.** At 8% a round, a two-issue haggle is expensive.
6. **If the direction is a guess** (`DayValues.sure` False), don't give the day first; follow the rival's day only if
   the worse reading costs ≤ 2 P.

Code (Builder):
- **Strategist days guide:** replace the current generic paragraph with rules 1-6.
- **Ledger, days duels:**
  - their day;
  - whether it is on our side;
  - what it costs us (C);
  - "if you give it, ask at least C more";
  - our weight's rank among the weights seen this session (kept in the runner).
- **Negotiator:** may add the menu in words (structure binds one package).
- **Tests:**
  - the deck's example both ways (seller +1/day facing a day-0 buyer → "give, ask ≥ 10 more"; buyer −4/day facing a
    day-10 seller → "hold");
  - a worth-neutral day swap passes the small-step rule (step ≤ 0 is sent);
  - weight rank.

### 3.2 Rounds: keep the floor, remove the rest
- `MIN_STEP_SHARE` 0.25 → **0.05**. The 3 P floor stays; it targets the 1-2 P steps (277/278, 2356).
- `OFFER_BUDGET`: **remove** the rule and its ledger line.
- Strategist bullet:
  - **keep** "few, clear steps" and "don't chase a holder";
  - **delete** "Plan on no more than four offers", and the line telling it to move at least the smallest step even
    at large gaps;
  - **add**: "while the gap is wide, small steps (or none) draw more from them than big ones; save big moves for the
    close".
- Tests updated to the new numbers (the Builder's 6 stay, re-parameterised).

### 3.3 Leave alone
- **Opener:** as it is.
- **Accepts:** keep the small-gap and deadline closers; no break-even rule.
- **Silent walk:** keep the 30% floor. Near our limit the share is ~0, so walking further buys nothing.

### 3.4 Engine
- **Strategist at `--effort medium` for Duels II.** Smoke test (days duel): Opus low 3.9-7.5 s, medium 6.4-8.1 s;
  Sonnet negotiator ~2-3 s; that fits 30 s ticks. Sunday (15 s ticks) goes back to low, or to Sonnet.
- Duels I: 1 timeout (25 s), 1 draft past the limit blocked, $1.62 in model spend, 5.1 s mean decision.
- **Desk question (Dani):** with 6 duels at once, are duel accepts limited per duel or per team per tick? Our runner
  takes one per tick across all duels and lines them up by deadline. In Duels I every code accept still came at 2
  ticks left (8 of 8). With 6 concurrent duels the line could force accepts up to 6 ticks early.

### 3.5 Stretch, only if 3.1 and 3.2 are done: remember each rival team by its wording
When a rival's first message matches the wording of a rival from an earlier duel this session, give the strategist one
fact: what that team did there. Examples: "accepted our opener within 1 round", or "conceded twice, then held at N;
our later steps moved nothing". Use: open higher against teams that met our opener; stop conceding after a
quick-then-hold team's hold, and take their number at the end.

## 4. Timeline (PLAN.md #10)
| When | What | Who |
|---|---|---|
| 15:30 | Decide 3.1-3.4 (and 3.5 or not) | Aleks |
| 17:00 | Coded, tests green, merged | Aleks's Builder |
| 17:45 | Restart: `agents/duelist/supervise.sh --negotiator-model claude-sonnet-5-5 --effort medium`; check the log's first line | Aleks |
| First Duels II wave | Day reading on the console matches `days_meaning`; `review`: `pred` = `points`; rounds per deal < 4.4; no new standoff no-deals | Aleks |
