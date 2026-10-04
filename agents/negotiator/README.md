# Negotiator

A standalone market negotiator based on the duelist's two-stage agent and code-enforced price bands. Use
`NegotiatorAgent.for_trade` to negotiate one card against cash: **our own collection and goals determine the
private limit**, with no limit supplied by the game. Both stages use `claude-sonnet-5-5` by default, medium effort
for strategy and low effort for message writing.

No runner, scheduler, dealer, trading loop, database or game endpoint is connected. Importing it does not start
anything. Calling `respond` calls the models and returns a move; it does not send the move. Delivery days are
unsupported and day-bearing inputs are rejected.

## Our private value and limit

`TeamState` carries our catalog, actual set multipliers, holdings, cash and existing commitments. The calculator
uses the same valuation basis as the hub's demand model:

- One more copy: book × our set multiplier × its copy marginal (defaults 1, 0.25, 0.10). Only the last missing
  page card adds the immediate completion bonus: page book × our set multiplier × page bonus (default 0.25).
- A copy sold: its marginal loss, conservatively taking at least the selected asset's `your_value`. When page
  protection is explicitly disabled, losing the last page copy also includes the lost completion bonus.
- An optional authoritative value of one more copy can replace the calculated buy value; its included page
  bonus is never added twice. A pending outgoing page card cannot create a phantom completion bonus.
- No future completion bonus is invented for an unfinished page. An optional `trade_cost_buffer` covers other
  collection effects, such as an unopened pack's value dropping after a trade.

`Params.goals` configures our desires. Confirmed initial goals: build **RET and CHA** and protect completed pages.
Defaults also keep the last needed target-page copy, reserve **200 P** in cash and require **3 P** of gain. Explicit
per-card desires are `wanted`, `neutral`, `unwanted`, or `keep`; `reserved_cards` are never offered. A last target
copy can be marked unwanted to leave an unfinished page; completed-page protection still takes priority.

Goals set the fraction of private value we insist on retaining as profit, subject to the 3 P minimum:

| Desire | Buy: retain as profit | Sell: profit above value lost |
| --- | ---: | ---: |
| Wanted | 2% | 15% |
| Neutral | 15% | 10% |
| Unwanted | 35% | 2% |

These are configurable initial policy choices, not game constants. Missing target-page cards default to wanted;
spare copies default to unwanted; others default to neutral. Set multipliers already express how much we value
each set. Priorities let us bid closer to value for needed cards and accept less profit on expendable spares,
while every permitted trade still covers the collection loss, fees and required gain.

The **buy cap** is the largest whole price where price + our fees fits both (private marginal value − required
profit − cost buffer) and our available cash after reserves and committed bids. The **sell floor** is the smallest
whole price where price − our fees covers (collection value lost + required profit + cost buffer). Fee rounding is
exact. Supply `Fees(bps=500, per_card=1)` if we are the El Rastro taker; the default is zero fees for a maker or
fee-free venue. Unknown private multipliers, protected cards, unavailable copies, already-incoming cards and
insufficient budget raise `TradeUnavailable` before model calls.

`agent.reservation` explains the calculated limit, private value, required profit, page effects, selected asset
and cash constraint. The strategist sees this breakdown; the message writer sees only the safe band and public
market data. The limit is a walk-away price, not our target or opening anchor. The strategist is told to use
market prices and the counterparty's estimated value to capture more than the minimum.

## Offline inputs and usage

`TeamState.from_snapshots` adapts already-loaded catalog, team and offer payloads without fetching anything.
`MarketData` supplies book prices, bids, asks, recent trades, source and observation tick; an optional counterparty
reservation-value estimate goes only to strategy. Quotes remain distinct from completed trades.

```python
from agents.duelist.model import Observation, Role
from agents.negotiator import Fees, MarketData, NegotiatorAgent, Params, TeamGoals, TeamState

# These dictionaries are caller-supplied snapshots; this module makes no game requests.
state = TeamState.from_snapshots(catalog_snapshot, team_snapshot, offers=tuple(offer_snapshots))
params = Params(decay=0.08, goals=TeamGoals(
    target_sets={"RET", "CHA"},
    card_desires={"CHA-03": "wanted", "MAL-02": "unwanted"},
    reserved_cards={"SAL-08"},
))
market = MarketData(item="CHA-03", source="caller market snapshot", observed_tick=100,
                    best_bid=20, best_ask=30, recent_trade_prices=(24, 26))
agent = NegotiatorAgent.for_trade("draft-CHA-03", Role.BUYER, "CHA-03", market, state,
                                 params, fees=Fees())
print(agent.reservation)  # Computed without calling a model or supplying a limit.
# In an async caller, when we decide to use it:
# move = await agent.respond(Observation(view=agent.view, tick=101))
# The caller decides whether to send move; this module has no execution connection.
```

Supply a fresh `team_state=` and/or `market_data=` to `respond` to reprice before the next decision. A refreshed
state that makes the trade ineligible raises `TradeUnavailable`; future execution must handle any existing
standing offer accordingly. The computed limit also appears in the returned move's private metadata.

`Params.decay` defaults to 8% per message round, as an **internal preference for closing sooner**, rather than a
claim that actual team trades incur duel decay. Zero removes this discount. The inherited ledger describes
remaining room above our walk-away price, not actual team-trade score. Our custom prompts explain the distinction.

Inject `strategist=` and `negotiator=` implementations of `engine.Model` for offline tests. The direct constructor
with an explicit `DuelView.limit` remains available for simulations; `for_trade` is the collection-aware entry point.
This module handles a single card/cash negotiation; bundles, swaps and live counterparty/venue policy checks
belong to the future execution integration.
