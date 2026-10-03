"""Checks for the hard invariants (from regateo's agent_sdk.guards). They never choose a move: they only say
what is wrong with one, as feedback a model can act on."""
from __future__ import annotations

import re

from .model import DuelView, Offer, sign
from .prices import find_prices, money

# Any agreement vocabulary, negated or not: "I can't accept", "the moment we agree", "a solid deal".
_AGREEMENT = re.compile(r"\b(?:accept\w*|agree\w*|deal\w*|sold|works for me|sounds good|let's do it)\b", re.IGNORECASE)
# Words that state a fact about the item, money, other parties or the game. A false fact, or words that contradict
# the structured offer, earn whoever flags them +10 (Saturday, intel/GAME.md); "final" or urgency is posture and
# safe. Duels I: 65 of our 205 messages invented facts ("carefully sourced", "needs repairs", "track record").
_CLAIM = re.compile(r"\b(?:quality|condition|reputation|repair\w*|sourc\w*|histor\w*|track record|locat\w*|famous|"
                    r"loyal\w*|rare|rarity|landmark|budget\w*|limit\w*|costs?|costing|paid|carry\w*|stock|"
                    r"market\w*|demand|sought[- ]after|scarc\w*|collector\w*|vintage|authentic\w*|genuine|"
                    r"printing|(?:other|another|competing)\s+(?:buyers?|sellers?|offers?|bidders?|teams?)|"
                    # the negotiator answers Spanish in Spanish (2356, 2534)
                    r"calidad|ubicaci\w+|hist[oó]ri\w+|rar[oa]s?|rareza|escas\w+|mercado|presupuesto|costes?|"
                    r"costos?|l[ií]mites?|demanda|coleccionista\w*|famos[oa]s?|"
                    r"otr[oa]s?\s+(?:compradore?s?|vendedore?s?|ofertas?))\b",
                    re.IGNORECASE)
_NUMBER = re.compile(r"\d+(?:[.,]\d+)*")
_DAY_BEFORE = re.compile(r"\bdays?\s*$", re.IGNORECASE)


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


def claim_words(message: str) -> list[str]:
    return sorted({m.group(0).lower() for m in _CLAIM.finditer(message)})


def stray_numbers(view: DuelView, message: str, price: float | None, day: int | None) -> list[str]:
    """Numbers in the message other than the offer's price and day. In a days duel, one other package named after
    the offer passes, as a menu in words ("120 P on day 0; or, if you prefer, 105 P on day 10"), when it is a real
    day and inside our limit; the offer comes first so the words can't read as a different offer."""
    found = []
    for m in _NUMBER.finditer(message):
        value = float(m.group(0).replace(",", ""))
        found.append((value, bool(_DAY_BEFORE.search(message[:m.start()])), m.group(0)))
    extra = [(v, is_day, raw) for v, is_day, raw in found if not ((is_day and v == day) or (not is_day and v == price))]
    if not extra:
        return []
    prices, days = [v for v, d, _ in extra if not d], [v for v, d, _ in extra if d]
    if view.has_days and price is not None and found[0] not in extra and len(prices) <= 1 and len(days) <= 1:
        other_day = days[0] if days else day
        other_price = prices[0] if prices else price
        if other_day is not None and float(other_day).is_integer() and 0 <= other_day <= 10 \
                and not past_limit(view, other_price, int(other_day)):
            return []
    return [raw for _, _, raw in extra]


def claims(view: DuelView, message: str, price: float | None, day: int | None) -> list[str]:
    """What in a message could be flagged as a false claim, as feedback: claim words, and stray numbers."""
    out = []
    if words := claim_words(message):
        out.append(f"the message states facts ({', '.join(words)}). Say nothing about the item (its quality, "
                   "condition, history, location, rarity or demand), costs, budgets, limits, other buyers, sellers "
                   "or offers, or the market: talk only about prices, days, the moves on both sides and how you see "
                   "the gap.")
    if numbers := stray_numbers(view, message, price, day):
        out.append(f"the message names {', '.join(numbers)}: write no number but your price"
                   + (" and your day (a menu names your offer first, then one other package)." if view.has_days
                      else "."))
    return out


def reads_as_agreement(message: str) -> bool:
    return bool(_AGREEMENT.search(message))
