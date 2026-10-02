"""Checks for the hard invariants (from regateo's agent_sdk.guards). They never choose a move: they only say
what is wrong with one, as feedback a model can act on."""
from __future__ import annotations

import re

from .model import DuelView, sign
from .prices import find_prices, money

# Any agreement vocabulary, negated or not: "I can't accept", "the moment we agree", "a solid deal".
_AGREEMENT = re.compile(r"\b(?:accept\w*|agree\w*|deal\w*|sold|works for me|sounds good|let's do it)\b", re.IGNORECASE)


def past_limit(view: DuelView, price: float) -> bool:
    """True when `price` is worse for us than our limit. A price at the limit is allowed (it scores zero)."""
    s = sign(view.role)
    return s * price < s * view.limit


def mentions_past_limit(view: DuelView, message: str) -> list[float]:
    """Amounts written in the message that are past our limit. If any amount is currency-marked, only marked
    ones count ("day 3", "2 cards" aren't prices)."""
    found = find_prices(message)
    if any(p.currency for p in found):
        found = [p for p in found if p.currency]
    return sorted({p.value for p in found if past_limit(view, p.value)})


def standing_problems(view: DuelView, price: int | None, their_price: int | None) -> list[str]:
    """An offer worse for us than the rival's standing offer: accepting theirs would get more."""
    if price is None or their_price is None:
        return []
    s = sign(view.role)
    if s * price >= s * their_price:
        return []
    theirs, ours = money(their_price, view.currency), money(price, view.currency)
    return [f"their standing offer, {theirs}, is already better for you than your offer of {ours}. Accept their "
            f"offer, or offer a price better for you than {theirs}."]


def reads_as_agreement(message: str) -> bool:
    return bool(_AGREEMENT.search(message))
