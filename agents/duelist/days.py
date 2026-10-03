"""What each delivery day is worth to us, read from the duel's `your_days_weight` and `days_meaning`.

Duels II settles a price and a delivery day from 0 to 10, and each side has a private weight per day (RULES.md).
Friday's practice showed neither field (both null), so this reads the shapes the weight is likely to take:
- a list of 11 numbers, or a dict keyed by day ("0" to "10"): what each day is worth;
- a number w: w per day toward the days we prefer, which `days_meaning` names ("each day later costs you w");
  a negative w with no such words prefers the early days (w x day);
- a dict with a number per day and a direction ({"per_day": 2, "prefers": "early"}) or a best day
  ({"best_day": 3, "per_day": 1.5}: each day away from it costs 1.5).

Values are stated against our best day, so every day is worth 0 or less. If the game counts the day as a cost,
that is exact; if as a bonus, it errs on the safe side by a constant. When the direction is a guess (`sure`
False), each day counts at the worse of the early and late readings. Any other shape reads as None: code leaves
the duel to the models, who get the raw weight.

The first deals of Duels II tell whether the reading is right: `review` sets our predicted result next to the
game's (`records.summary`). If they differ, fix the reading here.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

DAYS = range(11)
_EARLY = re.compile(r"\b(?:earl(?:y|ier|iest)|soon(?:er|est)?|fast(?:er|est)?|quick(?:er|ly)?|urgent\w*|asap|"
                    r"lower days?|fewer days)\b", re.IGNORECASE)
_LATE = re.compile(r"\b(?:lat(?:e|er|est)|delay\w*|slow(?:er)?|more time|higher days?|more days)\b", re.IGNORECASE)
_COST = re.compile(r"\b(?:costs?|costing|los(?:e|es|t|ing)|penalt\w*|subtract\w*|minus|deduct\w*|reduc\w*)\b",
                   re.IGNORECASE)
_PREFER = re.compile(r"\b(?:prefer\w*|want\w*|better|rather|like\w*|favou?r\w*)\b", re.IGNORECASE)
_NUMBER = re.compile(r"-?\d+(?:\.\d+)?")
PER_DAY_KEYS = ("per_day", "weight", "value", "w", "slope", "points_per_day", "value_per_day", "cost_per_day",
                "penalty", "penalty_per_day")
DIRECTION_KEYS = ("prefers", "prefer", "preference", "direction", "wants", "better")   # values like "early"
TEXT_KEYS = ("meaning", "description", "note")
BEST_KEYS = ("best_day", "ideal_day", "ideal", "target_day", "preferred_day", "best")


@dataclass(frozen=True)
class DayValues:
    values: tuple[float, ...]     # day 0 to 10: what the day adds to a deal for us, 0 at our best day, else less
    sure: bool                    # False: the direction is a guess, and each day counts at the worse reading
    how: str                      # one line on how we read the weight, for the console, the records, the strategist

    def __call__(self, day: int | None) -> float:
        """The day's value; a missing day counts as our worst."""
        if day is None:
            return min(self.values)
        return self.values[min(max(int(day), 0), 10)]

    @property
    def best(self) -> int:
        """Our best day; among equals, the one nearest the middle (it leaves the rival room on both sides)."""
        top = max(self.values)
        return min((d for d in DAYS if self.values[d] == top), key=lambda d: abs(d - 5))

    def table(self, currency: str = "P") -> str:
        return ", ".join(f"day {d}: {_amount(-v)} {currency}" for d, v in enumerate(self.values))


def _amount(x: float) -> str:
    x = round(x, 2) + 0.0                         # no "-0"
    return f"{x:g}"


def _number(x: Any) -> float | None:
    if isinstance(x, bool):
        return None
    if isinstance(x, int | float):
        return float(x)
    if isinstance(x, str) and (m := _NUMBER.search(x)):
        return float(m.group())
    return None


def direction(text: str) -> str | None:
    """"early" or "late": the days the text says we prefer. Without a word of preference, a cost word turns the
    direction it names around ("each day later costs you 2" prefers early; "you prefer early delivery, each day
    costs 2" doesn't). Words in parentheses are skipped ("0 (soonest) to 10 (latest)" labels the scale, not a
    preference); both directions, or neither, read as None."""
    text = re.sub(r"\([^)]*\)", " ", text.replace("_", " "))
    early, late = bool(_EARLY.search(text)), bool(_LATE.search(text))
    if early == late:
        return None
    named = "early" if early else "late"
    if _COST.search(text) and not _PREFER.search(text):
        return "late" if named == "early" else "early"
    return named


def _relative(values: list[float]) -> tuple[float, ...]:
    top = max(values)
    return tuple(round(v - top, 4) + 0.0 for v in values)


def _per_day(w: float, prefer: str | None, how: str) -> DayValues:
    w = abs(w)
    if w == 0:
        return DayValues(tuple(0.0 for _ in DAYS), True, f"{how}: the day doesn't matter to us")
    if prefer == "early":
        return DayValues(tuple(-w * d + 0.0 for d in DAYS), True, f"{how}: each day after day 0 costs you "
                                                                     f"{_amount(w)}")
    if prefer == "late":
        return DayValues(tuple(-w * (10 - d) + 0.0 for d in DAYS), True, f"{how}: each day before day 10 costs you "
                                                                            f"{_amount(w)}")
    return DayValues(tuple(-w * max(d, 10 - d) + 0.0 for d in DAYS), False,
                     f"{how}, direction unknown: each day counts at the worse of the early and late readings "
                     f"({_amount(w)} per day)")


def read_days(weight: Any, meaning: str | None = None) -> DayValues | None:
    """Our value of each day from the game's weight and its explanation; None when the shape isn't one we know."""
    text = meaning or ""
    if isinstance(weight, str):
        text, weight = f"{weight} {text}", _number(weight)
    if isinstance(weight, list | tuple):
        values = [_number(x) for x in weight]
        if len(values) == 11 and all(v is not None for v in values):
            return DayValues(_relative(values), True, "a value for each day (list)")
        return None
    if isinstance(weight, dict):
        by_day = {int(k): _number(v) for k, v in weight.items() if str(k).strip().isdigit()}
        if set(by_day) >= set(DAYS) and all(by_day[d] is not None for d in DAYS):
            return DayValues(_relative([by_day[d] for d in DAYS]), True, "a value for each day (by day)")
        w = next((n for k in PER_DAY_KEYS if (n := _number(weight.get(k))) is not None), None)
        if w is None:
            return None
        best = next((n for k in BEST_KEYS if (n := _number(weight.get(k))) is not None), None)
        if best is not None and 0 <= best <= 10:
            return DayValues(tuple(-abs(w) * abs(d - best) + 0.0 for d in DAYS), True,
                             f"each day away from day {best:g} costs you {_amount(abs(w))}")
        stated = " ".join(str(weight[k]) for k in DIRECTION_KEYS if weight.get(k) is not None)
        prefer = direction(f"prefer {stated}") if stated else None
        if prefer is None:
            prefer = direction(" ".join([*(str(weight[k]) for k in TEXT_KEYS if weight.get(k) is not None),
                                         *map(str, weight), text]))
        return _per_day(w, prefer, f"{_amount(abs(w))} per day ({json.dumps(weight)[:80]})")
    w = _number(weight)
    if w is None:
        return None
    prefer = direction(text) if text else None
    if prefer is None and w < 0:
        prefer = "early"                          # w x day with a negative w: the early days are worth more
    return _per_day(w, prefer, f"{_amount(w)} per day" + (" (direction from the game's words)" if text and prefer else ""))
