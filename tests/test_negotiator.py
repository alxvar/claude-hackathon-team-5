"""Offline behavioral tests for the dormant market negotiator."""
import asyncio
import json

import pytest
from pydantic import ValidationError

from agents.duelist.agent import BandPlan, Decision
from agents.duelist.model import DuelView, Observation, Offer, Role, Turn
from agents.negotiator import MarketData, NegotiatorAgent, Params
from engine import LLMError, Reply


class FakeModel:
    label = "fake"

    def __init__(self, result):
        self.result = result
        self.seen = []

    async def parse(self, schema, system, messages):
        self.seen.append((system, messages))
        if isinstance(self.result, Exception):
            raise self.result
        return Reply(self.result, 0, 0, 0, 0, "fake")


def snapshot(**changes):
    return MarketData(item="RET-03", source="offline test", observed_tick=100, book_value=55,
                      best_bid=50, best_ask=70, recent_trade_prices=(58, 62), **changes)


def setup(role=Role.SELLER, params=None):
    view = DuelView(duel_id="test", role=role, limit=37, item="RET-03", decay=0.25, duel_ticks=12)
    strategist = FakeModel(BandPlan(read="They moved.", target=60, best=62, worst=58, days=None,
                                    angle="Offer the target."))
    negotiator = FakeModel(Decision(action="offer", price=60, message="I can do 60 P."))
    agent = NegotiatorAgent(view, snapshot(counterparty_value=123), params,
                            strategist=strategist, negotiator=negotiator)
    return agent, Observation(view=view, tick=101, ticks_left=8), strategist, negotiator


def test_default_models_have_separate_efforts_and_construction_sends_nothing(monkeypatch):
    created = []

    def fake_claude(**kwargs):
        created.append(kwargs)
        return FakeModel(None)

    monkeypatch.setattr("engine.claude.Claude", fake_claude)
    agent = NegotiatorAgent(DuelView(duel_id=1, role=Role.BUYER, limit=80), snapshot())
    assert created == [{"model": "claude-sonnet-5-5", "effort": "medium"},
                       {"model": "claude-sonnet-5-5", "effort": "low"}]
    assert agent.view.decay == 0.08
    assert not agent.strategist.seen and not agent.negotiator.seen


def test_market_data_reaches_both_stages_but_private_values_only_reach_strategist():
    agent, obs, strategist, negotiator = setup()
    move = asyncio.run(agent.respond(obs))
    assert (move.action, move.price, move.days) == ("offer", 60, None)
    for model in (strategist, negotiator):
        system, _ = model.seen[0]
        for fact in ('"book_value":55.0', '"best_bid":50.0', '"best_ask":70.0', '"recent_trade_prices":[58.0,62.0]'):
            assert fact in system
        assert "unfilled quotes" in system and "historical" in system
    assert "37 P" in strategist.seen[0][0] and "123 P" in strategist.seen[0][0]
    assert "37 P" not in json.dumps(negotiator.seen) and "123 P" not in json.dumps(negotiator.seen)


@pytest.mark.parametrize("decay", [0, 0.08, 0.16])
def test_configured_decay_controls_prompts_and_live_ledger(decay):
    agent, obs, strategist, _ = setup(params=Params(decay=decay))
    obs.rival_offer = Offer(price=57)
    obs.rounds = 2
    asyncio.run(agent.respond(obs))
    system, messages = strategist.seen[0]
    assert agent.view.decay == decay and obs.view.decay == 0.25
    text = json.dumps(messages)
    assert "shrinks the value of any deal by about 25%" not in system
    assert "Each round costs any deal about 25%" not in text
    if decay:
        assert f"{decay:.1%}" in system and f"{decay:.0%}" in text
        assert f"worth about {round(20 * (1 - decay) ** 2)} P" in text
    else:
        assert "Each round costs" not in text and "Every round shrinks" not in system


def test_snapshot_can_be_refreshed_before_both_model_calls():
    agent, obs, strategist, negotiator = setup()
    updated = MarketData(item="RET-03", source="new snapshot", observed_tick=101, best_ask=90)
    asyncio.run(agent.respond(obs, market_data=updated))
    for model in (strategist, negotiator):
        assert '"best_ask":90.0' in model.seen[0][0]
        assert '"best_ask":70.0' not in model.seen[0][0]
    assert "123 P" not in strategist.seen[0][0]


@pytest.mark.parametrize("role, bad, limit", [(Role.SELLER, 10, 37), (Role.BUYER, 100, 37)])
def test_inherited_guards_repair_offers_past_our_limit(role, bad, limit):
    agent, obs, strategist, negotiator = setup(role)
    strategist.result = BandPlan(read="", target=bad, best=bad, worst=bad, days=None, angle="")
    negotiator.result = Decision(action="offer", price=bad, message=f"I can do {bad} P.")
    move = asyncio.run(agent.respond(obs))
    assert move.action == "offer" and move.price == limit and move.days is None


def test_fallback_returns_price_only_when_models_fail():
    agent, obs, strategist, _ = setup()
    strategist.result = LLMError("offline failure")
    move = asyncio.run(agent.respond(obs))
    assert move.action == "offer" and move.price >= agent.view.limit and move.days is None


def test_day_bearing_inputs_are_rejected_without_model_calls():
    agent, obs, strategist, negotiator = setup()
    for update in ({"view": obs.view.model_copy(update={"issues": ["price", "days"]})},
                   {"rival_offer": Offer(price=60, days=4)},
                   {"turns": [Turn(mine=True, offer=Offer(price=60, days=4))]}):
        with pytest.raises(ValueError, match="price only"):
            asyncio.run(agent.respond(obs.model_copy(update=update)))
    with pytest.raises(ValueError, match="price only"):
        NegotiatorAgent(obs.view.model_copy(update={"issues": ["price", "days"]}), snapshot(),
                        strategist=strategist, negotiator=negotiator)
    assert not strategist.seen and not negotiator.seen


def test_invalid_snapshot_and_observation_are_rejected():
    agent, obs, strategist, _ = setup()
    for updated in (MarketData(item="other", source="test"), MarketData(item="RET-03", source="test", currency="EUR")):
        with pytest.raises(ValueError):
            asyncio.run(agent.respond(obs, market_data=updated))
    with pytest.raises(ValueError, match="same role and private limit"):
        asyncio.run(agent.respond(obs.model_copy(update={"view": obs.view.model_copy(update={"limit": 1})})))
    assert not strategist.seen


@pytest.mark.parametrize("decay", [-0.01, 1, 8, float("nan"), float("inf")])
def test_invalid_decay_is_rejected(decay):
    with pytest.raises(ValidationError):
        Params(decay=decay)


def test_invalid_trade_prices_are_rejected():
    with pytest.raises(ValidationError):
        MarketData(item="RET-03", source="test", recent_trade_prices=(float("nan"),))
