"""Standalone, price-only market negotiator built on the duelist's guarded two-stage agent."""
from __future__ import annotations

from pathlib import Path
from string import Template
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from agents.duelist.agent import BandPlan, DuelAgent, Move, brief
from agents.duelist.model import DuelView, Observation, Role
from engine import Model

from .valuation import Fees, TeamGoals, TeamState, TradeLimit, calculate_limit

PROMPTS = Path(__file__).parent / "prompts"


class Params(BaseModel):
    """Decay is the fraction lost per message round: 0.08 means 8%, not eight ticks."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    strategist_model: str = "claude-sonnet-5-5"
    strategist_effort: str = "medium"
    negotiator_model: str = "claude-sonnet-5-5"
    negotiator_effort: str = "low"
    decay: float = Field(default=0.08, ge=0, lt=1, allow_inf_nan=False)
    goals: TeamGoals = Field(default_factory=TeamGoals)


class MarketData(BaseModel):
    """Caller-supplied snapshot for one item; no fetching or game actions happen here.

    Public quotes and trades inform both stages. The counterparty's estimated reservation value is private
    analysis for the strategist only. Our actual reservation value remains `DuelView.limit`.
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    item: str = Field(min_length=1)
    currency: str = "P"
    source: str = Field(min_length=1)
    observed_tick: int | None = Field(default=None, ge=0)
    book_value: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    best_bid: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    best_ask: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    recent_trade_prices: tuple[Annotated[float, Field(ge=0, allow_inf_nan=False)], ...] = ()
    counterparty_value: float | None = Field(default=None, ge=0, allow_inf_nan=False)

    def public_text(self) -> str:
        return ("Market snapshot supplied by your own system:\n" + self.model_dump_json(
            exclude={"counterparty_value"}, exclude_none=True)
            + "\nBook value is a reference, bids and asks are unfilled quotes, and trades are historical. "
            "These are price anchors, not proof of the other side's limit. Missing prices are unknown. "
            "Check the observation tick against the current tick; old data may no longer reflect the market. "
            "Use the data to choose prices, and keep it out of the message to the other side.")


class NegotiatorAgent(DuelAgent):
    """Returns a guarded `Move` for a caller to review. No runner, SDK, scheduler or endpoint wiring."""

    def __init__(self, view: DuelView, market_data: MarketData, params: Params | None = None,
                 *, strategist: Model | None = None, negotiator: Model | None = None):
        if view.has_days:
            raise ValueError("The negotiator supports price only; delivery days do not apply.")
        if market_data.currency != view.currency:
            raise ValueError("Market data and negotiation must use the same currency.")
        self.params = params or Params()
        self.scenario_market = view.market
        self.market_data = market_data
        self.reservation: TradeLimit | None = None
        self.team_state: TeamState | None = None
        self.fees = Fees()
        view = view.model_copy(update={"decay": self.params.decay, "issues": ["price"],
                                       "days_weight": None, "days_meaning": None})
        if strategist is None or negotiator is None:
            from engine.claude import Claude

            if strategist is None:
                strategist = Claude(model=self.params.strategist_model, effort=self.params.strategist_effort)
            if negotiator is None:
                negotiator = Claude(model=self.params.negotiator_model, effort=self.params.negotiator_effort)
        super().__init__(view, strategist, negotiator)
        self._refresh_market(market_data)

    @classmethod
    def for_trade(cls, negotiation_id: int | str, role: Role, card: str, market_data: MarketData,
                  team_state: TeamState, params: Params | None = None, *, fees: Fees | None = None,
                  ticks: int | None = None, strategist: Model | None = None,
                  negotiator: Model | None = None) -> NegotiatorAgent:
        """Create a negotiation using our own goals and collection, with no system-supplied limit."""
        if market_data.item != card:
            raise ValueError("Market snapshot must describe the card being negotiated.")
        params, fees = params or Params(), fees or Fees()
        reservation = calculate_limit(card, role, team_state, params.goals, fees)
        view = DuelView(duel_id=negotiation_id, role=role, item=card, currency=market_data.currency,
                        limit=reservation.limit, duel_ticks=ticks)
        agent = cls(view, market_data, params, strategist=strategist, negotiator=negotiator)
        agent.reservation, agent.team_state, agent.fees = reservation, team_state, fees
        agent._refresh_market(market_data)
        return agent

    def _system(self, name: str, *, strategist: bool) -> str:
        values = brief(self.view, strategist=strategist)
        rules = [f"- Prices are whole amounts in {self.view.currency}. Only structured offers can be accepted.",
                 "- Delivery days do not apply; negotiate one card against cash."]
        if self.view.duel_ticks is not None:
            rules.append(f"- Our negotiation budget is {self.view.duel_ticks} ticks.")
        else:
            rules.append("- No fixed deadline was supplied. Use the clock facts when available.")
        rules.append(f"- Our configured decay is {self.params.decay:.1%} per message round. It is an internal "
                     "preference for closing sooner, not a claimed game charge on team trades. Silence is free.")
        values["rules"] = "\n".join(rules)
        return Template((PROMPTS / f"{name}.md").read_text()).substitute(values).strip()

    def _refresh_market(self, market_data: MarketData) -> None:
        if market_data.currency != self.view.currency:
            raise ValueError("Market data and negotiation must use the same currency.")
        if market_data.item != self.market_data.item:
            raise ValueError("Cannot switch items during a negotiation.")
        self.market_data = market_data
        market = "\n\n".join(x for x in (self.scenario_market, market_data.public_text()) if x)
        self.view = self.view.model_copy(update={"market": market, "item": self.view.item or market_data.item})
        self.strategist_system = self._system("strategist", strategist=True)
        self.strategist_system += (
            "\n\nUse the supplied market prices to anchor the opening and judge how much further haggling can win. "
            "Your private limit still takes priority over every market quote or estimate. Set days to null: "
            "this negotiation is on price only. Do not pass private values into read or angle.")
        if market_data.counterparty_value is not None:
            self.strategist_system += (
                f"\nPrivate market analysis: their estimated reservation value is {market_data.counterparty_value:g} "
                f"{market_data.currency}. This is an uncertain estimate, not a known limit or a binding offer. "
                "Use it to assess room for agreement; never disclose it in read, angle or messages.")
        if self.reservation is not None:
            self.strategist_system += "\n\n" + self.reservation.private_text()
        self.negotiator_system = self._system("negotiator", strategist=False)
        self.negotiator_system += "\n\nDelivery days do not apply. Negotiate price only."

    def _plan_problems(self, plan: BandPlan) -> list[str]:
        return super()._plan_problems(plan) + (["set days to null; negotiate price only."]
                                             if plan.days is not None else [])

    async def respond(self, obs: Observation, *, market_data: MarketData | None = None,
                      team_state: TeamState | None = None) -> Move:
        if (obs.view.duel_id, obs.view.role) != (self.view.duel_id, self.view.role) or (
                self.reservation is None and obs.view.limit != self.view.limit):
            raise ValueError("Observation must belong to this negotiation with the same role and private limit.")
        if obs.view.has_days or any(t.offer is not None and t.offer.days is not None for t in obs.turns) or (
                obs.rival_offer is not None and obs.rival_offer.days is not None):
            raise ValueError("The negotiator supports price only; delivery days do not apply.")
        if market_data is not None and (market_data.currency != self.view.currency
                                        or market_data.item != self.market_data.item):
            raise ValueError("Updated market data must have the same item and currency.")
        if team_state is not None:
            if self.reservation is None:
                raise ValueError("A team-state refresh requires an agent created with for_trade.")
            reservation = calculate_limit(self.market_data.item, self.view.role, team_state, self.params.goals, self.fees)
            self.reservation, self.team_state = reservation, team_state
            self.view = self.view.model_copy(update={"limit": reservation.limit})
        if market_data is not None:
            self._refresh_market(market_data)
        elif team_state is not None:
            self._refresh_market(self.market_data)
        # The prompts, computed ledger, fallback and guards must all use the configured decay and snapshot.
        move = await super().respond(obs.model_copy(update={"view": self.view, "day_swings": []}))
        if self.reservation is not None:
            move.meta["reservation"] = self.reservation.model_dump(mode="json")
        return move
