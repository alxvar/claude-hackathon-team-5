# Duelist: fewer rounds per deal (handoff to Aleks's Builder session on Aleks's Mac, Sat 11:58)

For Aleks's Builder session (on the same Mac as the live duelist), not Lucas's. Deploy before **Duels II (~18:29)**,
after Duels I is over. Questions go to Aleks.

## Why
Each duel scores our share of the gap between the two limits × (1 − decay)^rounds. Rounds = min(our messages, theirs),
priced or not; silence is free. Decay per round is 6% in Duels I, 8% in Duels II and 10% on Sunday.
In the 34 practice duels (`docs/duels/`):
- 3.5 rounds per deal cost 15% of deal value at 6%. The same pattern would cost ~25% at 8% and ~31% at 10%.
- 26 of our 75 concessions were steps of 3 P or less. They sit in the five longest duels (175, 176, 269, 277, 278:
  5-11 rounds each). 277: 175 → 173 → 160 → 158 → 156 … against a rival at 118, 11 rounds, 51% of the value kept.
  278: 10 messages to buy at the price the rival had offered from its first message.
- Cause: `prompts/strategist.md` asks for concessions "by less than they did, in shrinking steps", which suits
  free talk and here produces many small rounds.
- **Not the fix: meeting in the middle.** Deals landed at a median 64% of the way from their opener to ours. Jumping
  to the openers' midpoint would have scored ~16% less on the 17 deals with two openers (rough counterfactual). Keep
  the direction of the haggle; compress it into fewer, bigger steps.

## The change
Rule of thumb: the models choose the price; code decides whether a message is worth a round.

### 1. Code: a move that isn't worth a round is not sent (`agent.held`, `agent.py` ~l.579)
`held` already turns a near-copy of our standing offer into a hold (ff9a66d); `runner.is_hold` then sends nothing.
Extend it with two rules, applied only on the model path (`respond`) and only once both sides have a standing offer:
- **Small step:** a concession (toward them) smaller than `max(MIN_STEP_P, MIN_STEP_SHARE × gap)` becomes a hold.
  Gap = our standing offer's worth − their standing offer's worth, both via `guards.worth` (days duels: a day-only
  change is a step in worth). Constants: `MIN_STEP_P = 3`, `MIN_STEP_SHARE = 0.25`.
- **Offer budget:** once we have sent `OFFER_BUDGET = 4` priced offers (opener included), a further priced offer
  becomes a hold unless their standing offer has moved toward us by at least the same minimum step since our last
  offer.
- Held moves keep the existing shape: `Move("offer", text, price=ours.price, days=ours.days, meta={..., "rule":
  "small step" | "offer budget", "drafted": move.price})`, so the record shows what was held and why.

Exempt (send as today):
- accepts;
- the last `CLOSING_TICKS = 3` ticks (`ticks_left <= 3`);
- the opener;
- the code paths `close`, `their_price`, `silent_move` (silence adds no round) and `safe_move`;
- a move that isn't a concession (back toward our side or unchanged: unchanged is already a hold).

### 2. Facts (`agent.ledger`): tell the strategist what code will do
Only once both sides have offered:
- `- Offers your side has sent: N. Plan on at most 4 in the whole duel; after the fourth, nothing more is sent until
  the last 3 ticks unless they move at least X.`
- `- The smallest step worth sending now: X (a quarter of the gap, at least 3 P). A smaller step is not sent.`

### 3. Prompt (`prompts/strategist.md`): replace the "Tie your movement to theirs" bullet with these two

> - Move in few, clear steps. The facts below the conversation show how far each side has moved. Concede only when
>   they have moved since your last offer, and over the whole duel give up less than they do, but don't answer each
>   of their steps with one of yours: every message your side sends can cost a round, and theirs cost you nothing
>   until you answer. When you move, move at least the smallest step the facts name, never a point or two; a
>   smaller step is not sent. Plan on no more than four offers in the whole duel: the opener, two moves and a
>   closing offer. If they haven't moved, hold: set the target at your last offer, and your side sends nothing this
>   tick. A rival that repeats the same offer has not moved.
> - A rival that repeats the same offer is holding. Don't chase it with small steps. If its offer is within your
>   limit, hold (silence costs nothing) and let it stand to the end, where it can be accepted. If it's outside your
>   limit, make one clear step and hold again.

Leave the rest of the prompt alone (the opener guidance, the standoff exception, the small-gap and last-tick rules).

## Tests (`tests/test_duelist.py`; each new test must fail on the current code)
1. 277's pattern (seller, standing 175 vs their 118): a drafted 173 is held (`rule: small step`). A drafted 160 is
   sent.
2. 278's pattern (buyer, standing 82 vs their 111): a drafted 84 is held.
3. Budget: a 5th priced offer is held when their offer hasn't moved. It is sent when they moved ≥ the minimum step,
   or when `ticks_left <= 3`.
4. Untouched: an accept, the opener, `silent_move`, `their_price` and `close` behave as before.
5. Days duel: a day-only change counts as a step in worth (worth via `guards.worth`); below the minimum it is held.
6. The ledger shows both new lines once both sides have offered, and neither line before.

Run `uv run --project . pytest -q`; the full suite must be green.

## Constraints
- **The duelist is live for Duels I in this repo folder until ~13:35.** `supervise.sh` restarts a crashed process on
  whatever code is checked out here, so don't edit `agents/duelist/` in this folder until Duels I is over (`GET
  /api/duels` shows nothing live). Build in a separate git worktree (`git worktree add ../team5-rounds main`), run the
  tests there, and merge, pull and push only after Duels I.
- **Never a second duelist:** no `agents.duelist run` in the worktree. `pytest` only; `smoke` is fine (it calls the
  models and sends nothing to the game).
- Limits stay enforced by `final`; nothing here may loosen it.
- Restart the live duelist on the new code before Duels II only with Aleks's go: stop the supervisor, then
  `agents/duelist/supervise.sh --negotiator-model claude-sonnet-5-5`, then check the log's first line.

## Done
- One commit (prompt + ledger + `held` + tests), suite green, pushed after Duels I.
- One line in `team/aleks.md` with the commit and the test count.
- After Duels II's first wave, `intel/duel-review.md` should show rounds per deal and the share of value lost to decay
  below Duels I's numbers.
