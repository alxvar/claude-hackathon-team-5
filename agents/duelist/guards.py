"""Checks for the hard invariants (from regateo's agent_sdk.guards). They never choose a move: they only say
what is wrong with one, as feedback a model can act on."""
from __future__ import annotations

import re

from .model import DuelView, Offer, sign
from .prices import find_prices, money

# Any agreement vocabulary, negated or not: "I can't accept", "the moment we agree", "a solid deal".
_AGREEMENT = re.compile(r"\b(?:accept\w*|agree\w*|deal\w*|sold|works for me|sounds good|let's do it)\b", re.IGNORECASE)


def day_value(view: DuelView, day: int | None) -> float:
    """What the delivery day adds to a deal for us: 0 or less, against our best day (`days.read_days`). 0 on price
    only or when we can't read the weight; a days duel's offer without a day counts at our worst day."""
    dv = view.day_values
    return 0.0 if dv is None else dv(day)


def worth(view: DuelView, price: float, day: int | None = None) -> float:
    """What a deal at `price` on `day` is worth to us before decay: the price's margin over our limit plus the
    day's value. On price only, the margin alone."""
    return sign(view.role) * (price - view.limit) + day_value(view, day)


def price_at(view: DuelView, value: float, day: int | None = None) -> float:
    """The price at which a deal on `day` is worth `value` to us; at 0, our limit with the day's cost on top."""
    return view.limit + sign(view.role) * (value - day_value(view, day))


def past_limit(view: DuelView, price: float, day: int | None = None) -> bool:
    """True when a deal at `price` (on `day`, in a days duel) is worth less than nothing to us: the price is past
    our limit, or its margin doesn't cover what the day costs us. A deal worth exactly zero is allowed."""
    return worth(view, price, day) < 0


def mentions_past_limit(view: DuelView, message: str) -> list[float]:
    """Amounts written in the message that are past our limit (on price: the day's cost doesn't change what the
    amount tells the rival). If any amount is currency-marked, only marked ones count ("day 3", "2 cards" aren't
    prices)."""
    found = find_prices(message)
    if any(p.currency for p in found):
        found = [p for p in found if p.currency]
    s = sign(view.role)
    return sorted({p.value for p in found if s * p.value < s * view.limit})


def standing_problems(view: DuelView, price: int | None, their: Offer | None, day: int | None = None) -> list[str]:
    """An offer worse for us than the rival's standing offer (with days: the whole package): accepting theirs
    would get more."""
    if price is None or their is None:
        return []
    if worth(view, price, day) >= worth(view, their.price, their.days):
        return []
    on = lambda d: f" on day {d}" if view.has_days and d is not None else ""  # noqa: E731
    theirs, ours = money(their.price, view.currency) + on(their.days), money(price, view.currency) + on(day)
    return [f"their standing offer, {theirs}, is already better for you than your offer of {ours}. Accept their "
            f"offer, or offer something better for you than theirs."]


def reads_as_agreement(message: str) -> bool:
    return bool(_AGREEMENT.search(message))
