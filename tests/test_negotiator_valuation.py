"""Reservation prices preserve positive gain, our page goals, and shared cash/asset commitments."""
import asyncio
import json
from pathlib import Path

import pytest

from agents.duelist.agent import BandPlan, Decision
from agents.duelist.model import Observation, Role
from agents.negotiator import (Asset, Card, Fees, MarketData, NegotiatorAgent, Params, Surplus, TeamGoals,
                               TeamState, TradeUnavailable, calculate_limit)
from engine import Reply


def state(**changes):
    values = dict(cards=tuple(Card(ref=f"{s}-{i:02d}", set=s, book=b, page=True)
                             for s in ("RET", "CHA", "MAL") for i, b in ((1, 10), (2, 25), (3, 70))),
                  affinity={"RET": 1.6, "CHA": 1.3, "MAL": 0.5}, cash=500)
    values.update(changes)
    return TeamState(**values)


def goals(**changes):
    return TeamGoals(**changes)


def test_set_affinity_and_desire_change_how_far_we_will_bid():
    wanted = calculate_limit("RET-03", Role.BUYER, state())
    neutral = calculate_limit("MAL-03", Role.BUYER, state())
    unwanted = calculate_limit("RET-03", Role.BUYER, state(), goals(card_desires={"RET-03": "unwanted"}))
    assert wanted.marginal_value == 112 and wanted.limit == 109 and wanted.desire == "wanted"
    assert neutral.marginal_value == 35 and neutral.limit == 29
    assert unwanted.limit == 72 and unwanted.minimum_gain > wanted.minimum_gain


def test_last_missing_target_card_adds_the_completion_bonus_once():
    s = state(assets=(Asset(id=1, ref="RET-01"), Asset(id=2, ref="RET-02")))
    result = calculate_limit("RET-03", Role.BUYER, s)
    assert result.card_value == 112 and result.page_value == 42 and result.marginal_value == 154
    assert result.limit == 150 and result.missing_cards == ("RET-03",)
    authoritative = calculate_limit("RET-03", Role.BUYER, s.model_copy(update={"buy_values": {"RET-03": 154}}))
    assert authoritative.marginal_value == 154 and authoritative.limit == 150


def test_an_unfinished_page_gets_priority_but_not_an_imagined_bonus():
    result = calculate_limit("RET-03", Role.BUYER, state(assets=(Asset(id=1, ref="RET-01"),)))
    assert result.page_value == 0 and result.marginal_value == 112


def test_spares_and_lower_value_sets_have_lower_sale_floors():
    s = state(assets=(Asset(id=1, ref="RET-03", your_value=112), Asset(id=2, ref="RET-03", your_value=28),
                     Asset(id=3, ref="MAL-03", your_value=35)))
    spare = calculate_limit("RET-03", Role.SELLER, s)
    low_affinity = calculate_limit("MAL-03", Role.SELLER, s)
    assert spare.asset_id == 2 and spare.marginal_value == 28 and spare.limit == 31
    assert spare.desire == "unwanted"
    assert low_affinity.marginal_value == 35 and low_affinity.limit == 39
    unwanted = calculate_limit("MAL-03", Role.SELLER, s, goals(card_desires={"MAL-03": "unwanted"}))
    assert unwanted.limit == 38 < low_affinity.limit


def test_the_next_copy_is_worth_less_even_in_a_target_set():
    first = calculate_limit("RET-03", Role.BUYER, state())
    second = calculate_limit("RET-03", Role.BUYER, state(assets=(Asset(id=1, ref="RET-03"),)))
    assert first.marginal_value == 112 and second.marginal_value == 28
    assert second.limit < first.limit and second.page_value == 0


def test_last_target_copy_reserved_and_completed_pages_are_protected():
    s = state(assets=(Asset(id=1, ref="RET-01"),))
    with pytest.raises(TradeUnavailable, match="collection goals"):
        calculate_limit("RET-01", Role.SELLER, s)
    # An explicit unwanted card can leave an unfinished target page.
    result = calculate_limit("RET-01", Role.SELLER, s, goals(card_desires={"RET-01": "unwanted"}))
    assert result.limit == 19
    complete = s.model_copy(update={"assets": tuple(Asset(id=i, ref=f"RET-{i:02d}") for i in (1, 2, 3))})
    with pytest.raises(TradeUnavailable, match="completed page"):
        calculate_limit("RET-01", Role.SELLER, complete, goals(card_desires={"RET-01": "unwanted"}))
    spare = s.model_copy(update={"assets": (Asset(id=1, ref="RET-01"), Asset(id=2, ref="RET-01"))})
    with pytest.raises(TradeUnavailable, match="unreserved"):
        calculate_limit("RET-01", Role.SELLER, spare, goals(reserved_cards={"RET-01"}))


def test_committed_copies_do_not_count_as_spares():
    s = state(assets=(Asset(id=1, ref="RET-01"), Asset(id=2, ref="RET-01")), committed_assets=frozenset({1}))
    with pytest.raises(TradeUnavailable, match="collection goals"):
        calculate_limit("RET-01", Role.SELLER, s)


def test_an_outgoing_page_card_cannot_create_a_phantom_completion_bonus():
    s = state(assets=(Asset(id=1, ref="RET-01"), Asset(id=2, ref="RET-02")), committed_assets=frozenset({1}),
              buy_values={"RET-03": 154})
    result = calculate_limit("RET-03", Role.BUYER, s)
    assert result.marginal_value == 112 and result.limit == 109


def test_explicitly_unprotected_complete_page_includes_the_lost_bonus():
    s = state(assets=tuple(Asset(id=i, ref=f"RET-{i:02d}") for i in (1, 2, 3)))
    result = calculate_limit("RET-03", Role.SELLER, s,
                             goals(protect_completed_pages=False, protect_target_pages=False))
    assert result.marginal_value == 154 and result.page_value == 42 and result.limit == 170


def test_cash_reserve_committed_bids_and_fees_cap_our_bid():
    s = state(cash=310, committed_cash=30, buy_values={"RET-03": 100})
    fees = Fees(bps=500, per_card=1)
    result = calculate_limit("RET-03", Role.BUYER, s, fees=fees)
    assert result.available_cash == 80 and result.limit == 75
    assert result.limit + fees.at(result.limit) <= 80
    assert result.limit + 1 + fees.at(result.limit + 1) > 80
    with pytest.raises(TradeUnavailable, match="affordable"):
        calculate_limit("RET-03", Role.BUYER, s.model_copy(update={"cash": 230}), fees=fees)


@pytest.mark.parametrize("bps,fixed", [(0, 0), (500, 1), (100, 0), (9999, 3)])
@pytest.mark.parametrize("role", [Role.BUYER, Role.SELLER])
def test_fee_rounded_limits_preserve_required_profit_and_are_tight(bps, fixed, role):
    s = state(cash=10_000_000, assets=(Asset(id=1, ref="MAL-03", your_value=35.15),),
              buy_values={"MAL-03": 35.15})
    fees = Fees(bps=bps, per_card=fixed)
    result = calculate_limit("MAL-03", role, s, fees=fees)
    if role is Role.BUYER:
        gain = result.marginal_value - result.limit - fees.at(result.limit)
        beyond = result.marginal_value - (result.limit + 1) - fees.at(result.limit + 1)
    else:
        gain = result.limit - fees.at(result.limit) - result.marginal_value
        beyond = (result.limit - 1) - fees.at(result.limit - 1) - result.marginal_value
    assert gain + 1e-8 >= result.minimum_gain and beyond < result.minimum_gain


def test_unknown_multiplier_incoming_bid_and_absent_card_block_the_trade():
    with pytest.raises(TradeUnavailable, match="multiplier"):
        calculate_limit("RET-03", Role.BUYER, state(affinity={"MAL": 0.5}))
    with pytest.raises(TradeUnavailable, match="incoming"):
        calculate_limit("RET-03", Role.BUYER, state(incoming_cards=frozenset({"RET-03"})))
    with pytest.raises(TradeUnavailable, match="uncommitted"):
        calculate_limit("MAL-03", Role.SELLER, state())


def test_trade_cost_buffer_covers_other_collection_losses():
    s = state(assets=(Asset(id=1, ref="MAL-03"),))
    costly = s.model_copy(update={"trade_cost_buffer": 2.5})
    assert calculate_limit("MAL-03", Role.BUYER, costly).limit < calculate_limit("MAL-03", Role.BUYER, s).limit
    assert calculate_limit("MAL-03", Role.SELLER, costly).limit > calculate_limit("MAL-03", Role.SELLER, s).limit


def test_snapshot_adapter_reuses_existing_payloads_without_fetching():
    s = state()
    catalog = {"sets": [{"id": name, "cards": [{"id": c.ref, "book": c.book, "page": c.page}
                                               for c in s.cards if c.set == name]}
                        for name in ("RET", "CHA", "MAL")], "values": {"copy_marginals": [1, 0.25, 0.1]}}
    me = {"id": "t05", "cash": 500, "affinity": s.affinity,
          "assets": [{"id": 1, "kind": "card", "ref": "RET-01", "your_value": 16},
                     {"id": 2, "kind": "pack", "ref": "sobre_barrio"}],
          "album": {"pages": [{"set": "MAL", "complete": True}]}}
    offers = ({"maker": "t05", "give": {"assets": [1]}, "want": {"cards": ["CHA-03"]}},
              {"maker": "t05", "give": {"cash": 40}, "want": {"types": ["card:RET-03"]}},
              {"maker": "t09", "give": {"cash": 900}},
              {"maker": "t05", "status": "cancelled", "give": {"cash": 900}})
    adapted = TeamState.from_snapshots(catalog, me, offers=offers)
    assert adapted.committed_assets == {1} and adapted.committed_cash == 40
    assert adapted.incoming_cards == {"CHA-03", "RET-03"} and len(adapted.assets) == 1
    assert adapted.completed_sets == {"MAL"}


def test_recorded_team_and_catalog_snapshot_produce_a_private_bid_limit():
    raw = json.loads((Path(__file__).parent / "fixtures" / "opportunities_friday.json").read_text())
    snapshot = TeamState.from_snapshots(raw["catalog"], raw["me"])
    result = calculate_limit("LAV-09", Role.BUYER, snapshot)
    assert result.limit > 0
    assert result.limit <= result.marginal_value - result.minimum_gain
    assert result.limit <= raw["me"]["cash"] - TeamGoals().cash_floor


class Fake:
    label = "fake"

    def __init__(self, result):
        self.result, self.seen = result, []

    async def parse(self, schema, system, messages):
        self.seen.append((system, messages))
        return Reply(self.result, 0, 0, 0, 0, "fake")


def test_for_trade_computes_our_limit_and_refreshes_before_guarding_the_move():
    strategist = Fake(BandPlan(read="They moved.", target=110, best=110, worst=110, days=None, angle="Offer target."))
    negotiator = Fake(Decision(action="offer", price=110, message="I can do 110 P."))
    market = MarketData(item="RET-03", source="offline", best_ask=120)
    agent = NegotiatorAgent.for_trade("draft", Role.BUYER, "RET-03", market, state(),
                                      strategist=strategist, negotiator=negotiator)
    assert agent.view.limit == 109
    original = agent.view
    move = asyncio.run(agent.respond(Observation(view=original, ticks_left=8), team_state=state(cash=250)))
    assert agent.view.limit == 50 and move.price == 50
    assert move.meta["reservation"]["available_cash"] == 50
    assert "Private reservation-price calculation" in strategist.seen[0][0]
    assert "minimum_gain" not in json.dumps(negotiator.seen)
    assert "cash_floor" not in json.dumps(negotiator.seen)
    assert "internal preference" in strategist.seen[0][0]


def test_goal_overrides_are_part_of_params_and_do_not_require_a_system_limit():
    params = Params(goals=goals(target_sets=frozenset({"MAL"}), card_desires={"RET-03": "unwanted"}, cash_floor=100,
                                unwanted=Surplus(buy_share=0.5, sell_share=0.01)))
    fake = Fake(None)
    agent = NegotiatorAgent.for_trade(1, Role.BUYER, "RET-03", MarketData(item="RET-03", source="offline"),
                                      state(), params, strategist=fake, negotiator=fake)
    assert agent.view.limit == 56 and agent.reservation.desire == "unwanted" and not fake.seen
