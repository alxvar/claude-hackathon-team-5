"""Money amounts in free text (from regateo's agent_sdk.prices), and writing them in primas.

The duels carry prices as structured fields, so text amounts only matter for one check: never write an amount
past our limit, not even to reject it, since it tells the rival where our limit is.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

_CUR_PREFIX = r"(?P<pre>[$€£P]|(?:USD|EUR|GBP|US\$)\s?)"
_NUMBER = r"(?P<num>\d{1,3}(?:[, ]\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)"
_SCALE = r"(?P<scale>\s?(?:k|K|thousand)\b)"
_CUR_SUFFIX = r"(?P<post>\s?(?:[$€£]|P\b|primas?\b|USD|EUR|GBP|dollars?|euros?|bucks))"

_MONEY = re.compile(rf"(?<![\w.]){_CUR_PREFIX}?{_NUMBER}{_SCALE}?{_CUR_SUFFIX}?(?![\w%]|\.\d)", re.IGNORECASE)
_SCALES = {"k": 1e3, "thousand": 1e3}


@dataclass(frozen=True)
class PriceMention:
    value: float
    currency: bool      # had a currency symbol or word, or a k scale


def find_prices(text: str) -> list[PriceMention]:
    out = []
    for m in _MONEY.finditer(text):
        num = float(re.sub(r"[, ]", "", m.group("num")))
        scale = (m.group("scale") or "").strip().lower()
        if scale:
            num *= _SCALES[scale]
        out.append(PriceMention(value=round(num, 2), currency=bool(m.group("pre") or m.group("post") or scale)))
    return out


def money(price: float, currency: str = "P") -> str:
    num = f"{price:,.0f}" if float(price).is_integer() else f"{price:,.2f}"
    return f"{num} {currency}"
