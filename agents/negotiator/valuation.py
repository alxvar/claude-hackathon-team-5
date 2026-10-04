"""Pure reservation-price calculation from our collection and goals; no API or database reads."""
from __future__ import annotations

from collections import Counter
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from agents.duelist.model import Role

Value = Annotated[float, Field(ge=0, allow_inf_nan=False)]
Share = Annotated[float, Field(ge=0, lt=1, allow_inf_nan=False)]
Desire = Literal["wanted", "neutral", "unwanted", "keep"]


class Snapshot(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class Card(Snapshot):
    ref: str
    set: str
    book: Value
    page: bool


class Asset(Snapshot):
    id: int
    ref: str
    your_value: Value | None = None


class TeamState(Snapshot):
    """Our private, caller-supplied snapshots. A missing multiplier is unknown, never assumed to be one."""
    cards: tuple[Card, ...]
    assets: tuple[Asset, ...] = ()
    affinity: dict[str, Value]
    cash: Value
    committed_cash: Value = 0
    committed_assets: frozenset[int] = frozenset()
    incoming_cards: frozenset[str] = frozenset()
    completed_sets: frozenset[str] = frozenset()
    # Optional authoritative values of ONE MORE copy, including any immediate completion bonus.
    buy_values: dict[str, Value] = Field(default_factory=dict)
    copy_marginals: tuple[Value, ...] = (1, 0.25, 0.10)
    page_bonus: Value = 0.25
    # Conservative allowance for other collection effects, such as unopened-pack value lost on a trade.
    trade_cost_buffer: Value = 0

    @model_validator(mode="after")
    def consistent(self) -> TeamState:
        if not self.copy_marginals or any(a < b for a, b in zip(self.copy_marginals, self.copy_marginals[1:])):
            raise ValueError("copy_marginals must be nonempty and decrease with each extra copy")
        if len({c.ref for c in self.cards}) != len(self.cards):
            raise ValueError("catalog card references must be unique")
        if len({a.id for a in self.assets}) != len(self.assets):
            raise ValueError("asset ids must be unique")
        return self

    @classmethod
    def from_snapshots(cls, catalog: dict, me: dict, *, offers: tuple[dict, ...] = (),
                       buy_values: dict[str, float] | None = None, trade_cost_buffer: float = 0) -> TeamState:
        """Adapt already-loaded /api/catalog, /api/me and /api/me/offers payloads. Fetches nothing."""
        mine = [o for o in offers if o.get("maker") == me["id"] and o.get("status", "open") in ("open", "queued")]
        values = catalog.get("values") or {}
        return cls(
            cards=tuple(Card(ref=c["id"], set=s["id"], book=c["book"], page=c["page"])
                        for s in catalog["sets"] for c in s["cards"] if not c.get("hidden")),
            assets=tuple(Asset(id=a["id"], ref=a["ref"], your_value=a.get("your_value"))
                         for a in me["assets"] if a.get("kind") == "card"),
            affinity=me["affinity"], cash=me["cash"],
            committed_cash=sum((o.get("give") or {}).get("cash", 0) for o in mine),
            committed_assets=frozenset(a["id"] if isinstance(a, dict) else a for o in mine
                                      for a in (o.get("give") or {}).get("assets") or []),
            incoming_cards=frozenset(r for o in mine for r in (
                *((o.get("want") or {}).get("cards") or []),
                *(t[5:] for t in (o.get("want") or {}).get("types", []) if t.startswith("card:")))),
            completed_sets=frozenset(p["set"] for p in (me.get("album") or {}).get("pages", []) if p.get("complete")),
            buy_values=buy_values or {}, copy_marginals=values.get("copy_marginals", (1, 0.25, 0.10)),
            page_bonus=values.get("page_bonus", 0.25), trade_cost_buffer=trade_cost_buffer,
        )


class Surplus(Snapshot):
    buy_share: Share
    sell_share: Share


class TeamGoals(Snapshot):
    """Wanted purchases may spend more of their value; unwanted sales may keep less profit, never a loss."""
    target_sets: frozenset[str] = frozenset({"RET", "CHA"})
    card_desires: dict[str, Desire] = Field(default_factory=dict)
    reserved_cards: frozenset[str] = frozenset()
    protect_completed_pages: bool = True
    protect_target_pages: bool = True
    cash_floor: Value = 200
    min_gain: Value = 3
    wanted: Surplus = Field(default_factory=lambda: Surplus(buy_share=0.02, sell_share=0.15))
    neutral: Surplus = Field(default_factory=lambda: Surplus(buy_share=0.15, sell_share=0.10))
    unwanted: Surplus = Field(default_factory=lambda: Surplus(buy_share=0.35, sell_share=0.02))


class Fees(Snapshot):
    """Fees WE pay on this trade. Maker or a fee-free venue: zero; El Rastro taker: 500 bps + 1 P."""
    bps: int = Field(default=0, ge=0, lt=10000)
    per_card: int = Field(default=0, ge=0)

    def at(self, price: int) -> int:
        return (price * self.bps + 9999) // 10000 + self.per_card


class TradeUnavailable(ValueError):
    """Our goals, holdings or budget leave no eligible trade."""


class TradeLimit(Snapshot):
    card: str
    role: Role
    limit: int
    economic_limit: int
    card_value: float
    page_value: float
    marginal_value: float
    minimum_gain: float
    trade_cost_buffer: float
    desire: Desire
    missing_cards: tuple[str, ...]
    asset_id: int | None = None
    available_cash: float | None = None

    def private_text(self) -> str:
        return ("Private reservation-price calculation from our own holdings and goals:\n" + self.model_dump_json()
                + "\nThe limit includes our required gain and any cash constraint, so it is a walk-away price, "
                "not an opening price or a zero-value trade. Try to get substantially better terms. Wanted cards "
                "can justify closing nearer the limit; unwanted spares justify taking a smaller positive profit. "
                "Our set affinity is already priced in. Only immediate page completion is counted as value; "
                "do not invent a future bonus or exceed the limit for an unfinished page. "
                "Keep all of these private numbers and goals out of read, angle and the rival's messages.")


def _d(value: float) -> Decimal:
    return Decimal(str(value))


def _buy_limit(budget: Decimal, fees: Fees) -> int:
    lo, hi = 0, max(0, int(budget.to_integral_value(rounding=ROUND_FLOOR)))
    while lo < hi:
        price = (lo + hi + 1) // 2
        if Decimal(price + fees.at(price)) <= budget:
            lo = price
        else:
            hi = price - 1
    return lo


def _sell_limit(required: Decimal, fees: Fees) -> int:
    lo = 1
    # Cover a whole fee-rounding unit before dividing by the net share.
    hi = max(1, int(((required + fees.per_card + 1) / (1 - Decimal(fees.bps) / 10000)).to_integral_value(
        rounding=ROUND_CEILING)))
    while lo < hi:
        price = (lo + hi) // 2
        if Decimal(price - fees.at(price)) >= required:
            hi = price
        else:
            lo = price + 1
    return lo


def calculate_limit(card: str, role: Role, state: TeamState, goals: TeamGoals | None = None,
                    fees: Fees | None = None) -> TradeLimit:
    """For one card against cash, return an explained private limit without trusting an LLM to set it."""
    role = Role(role)
    goals, fees = goals or TeamGoals(), fees or Fees()
    cat = next((c for c in state.cards if c.ref == card), None)
    if cat is None or cat.set not in state.affinity:
        raise TradeUnavailable(f"Unknown card or private set multiplier: {card}")
    counts = Counter(a.ref for a in state.assets)
    free_counts = Counter(a.ref for a in state.assets if a.id not in state.committed_assets)
    page = tuple(c.ref for c in state.cards if c.set == cat.set and c.page)
    missing = tuple(r for r in page if free_counts[r] == 0)
    complete = cat.set in state.completed_sets or bool(page) and all(counts[r] for r in page)
    explicit = goals.card_desires.get(card)
    desire: Desire = explicit or (
        "wanted" if cat.page and card in missing and cat.set in goals.target_sets
        else "unwanted" if counts[card] >= 2 else "neutral")
    policy = getattr(goals, "wanted" if desire == "keep" else desire)
    multiplier = _d(state.affinity[cat.set])
    base = _d(cat.book) * multiplier
    bonus = sum((_d(c.book) for c in state.cards if c.set == cat.set and c.page), Decimal(0))
    bonus *= _d(state.page_bonus) * multiplier
    asset_id, available = None, None
    page_value = Decimal(0)
    if role is Role.BUYER:
        if card in state.incoming_cards:
            raise TradeUnavailable(f"{card} already has an incoming offer")
        marginal = _d(state.copy_marginals[min(counts[card], len(state.copy_marginals) - 1)])
        card_value = base * marginal
        if cat.page and counts[card] == 0 and missing == (card,):
            page_value = bonus
        value = _d(state.buy_values[card]) if card in state.buy_values else card_value + page_value
        if any(a.id in state.committed_assets and a.ref in page for a in state.assets):
            # Current API values can include a page that an already-promised outgoing copy will break.
            value = min(value, card_value + page_value)
        # The authoritative buy value includes the bonus; don't add it a second time.
        if card in state.buy_values:
            card_value, page_value = value, Decimal(0)
        minimum = max(_d(goals.min_gain), value * _d(policy.buy_share))
        available = max(Decimal(0), _d(state.cash) - _d(state.committed_cash) - _d(goals.cash_floor))
        economic = _buy_limit(value - _d(state.trade_cost_buffer), fees)
        limit = _buy_limit(min(value - minimum - _d(state.trade_cost_buffer), available), fees)
        if limit < 1:
            raise TradeUnavailable(f"No profitable, affordable bid for {card}")
    else:
        free = [a for a in state.assets if a.ref == card and a.id not in state.committed_assets]
        if not free or card in goals.reserved_cards:
            raise TradeUnavailable(f"No uncommitted, unreserved copy of {card}")
        last = free_counts[card] == 1
        if cat.page and last and complete and goals.protect_completed_pages:
            raise TradeUnavailable(f"Keep the last free copy of {card} in the completed page")
        if last and (desire == "keep" or cat.page and cat.set in goals.target_sets
                     and goals.protect_target_pages and explicit != "unwanted"):
            raise TradeUnavailable(f"Keep {card} for our collection goals")
        asset = min(free, key=lambda a: a.your_value if a.your_value is not None else float("inf"))
        asset_id = asset.id
        marginal = _d(state.copy_marginals[min(free_counts[card] - 1, len(state.copy_marginals) - 1)])
        card_value = max(base * marginal, _d(asset.your_value) if asset.your_value is not None else Decimal(0))
        if cat.page and last and complete:
            page_value = bonus
        value = card_value + page_value
        minimum = max(_d(goals.min_gain), value * _d(policy.sell_share))
        economic = _sell_limit(value + _d(state.trade_cost_buffer), fees)
        limit = _sell_limit(value + minimum + _d(state.trade_cost_buffer), fees)
    return TradeLimit(card=card, role=role, limit=limit, economic_limit=economic, card_value=float(card_value),
                      page_value=float(page_value), marginal_value=float(value), minimum_gain=float(minimum),
                      trade_cost_buffer=state.trade_cost_buffer, desire=desire, missing_cards=missing,
                      asset_id=asset_id, available_cash=float(available) if available is not None else None)
