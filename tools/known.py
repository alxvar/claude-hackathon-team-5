"""What teams told Lucas about their own album (Chief 21:50): run/known_holdings.json beats the feed's lower bound.

    {"t15": {"complete": ["LAT", "RET", "LAV"], "missing": ["MAL-09", "MAL-10"]}}

A complete set holds every page card (01-10); a set with missing cards holds its other page cards and none of the
missing ones; a team listed here buys only the cards it said it misses. Read by tools/matchmaker.py and
tools/v10_radar.py; keys that aren't team ids ("_note") are ignored.

    import known
    k = known.load()
    known.holds(k, "t15", "RET-03")   # True / False / None (not known)
    known.buys(k, "t15", "RET-03")    # False: t15 buys only MAL-09 and MAL-10
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOWN = ROOT / "run" / "known_holdings.json"
_CARD = re.compile(r"[A-Z]{3}-\d{2}")
_TEAM = re.compile(r"t\d{2}")


def load(path: Path | None = None) -> dict:
    """{team: {"complete": {sets}, "missing": {cards}}}; {} when the file is absent or unreadable."""
    try:
        data = json.loads(Path(path or KNOWN).read_text())
    except (OSError, ValueError):
        return {}
    out = {}
    for team, k in (data.items() if isinstance(data, dict) else ()):
        if _TEAM.fullmatch(str(team)) and isinstance(k, dict):
            out[team] = {"complete": {str(x).upper() for x in k.get("complete") or []},
                         "missing": {c for c in k.get("missing") or [] if _CARD.fullmatch(str(c))}}
    return out


def _page_card(card: str) -> bool:
    try:
        return 1 <= int(str(card).split("-")[1]) <= 10
    except (IndexError, ValueError):
        return False


def holds(known: dict, team: str, card: str) -> bool | None:
    """Whether `team` holds a copy of page card `card` by what it told us; None when its set isn't covered."""
    k = (known or {}).get(team)
    if not k or not _page_card(card):
        return None
    if card in k["missing"]:
        return False
    st = card.split("-")[0]
    if st in k["complete"] or st in {c.split("-")[0] for c in k["missing"]}:
        return True
    return None


def buys(known: dict, team: str, card: str) -> bool | None:
    """Whether `team` wants `card`: only the cards it said it misses; None when the team isn't known."""
    k = (known or {}).get(team)
    return None if not k else card in k["missing"]


def apply(n: dict, known: dict, page_cards: dict) -> dict:
    """(team, card) → copies with the known facts on top: at least 1 copy of every held page card, none of a missing
    one. `page_cards`: {set: [page card ids]}."""
    n = dict(n)
    for team, k in (known or {}).items():
        for st in (k["complete"] | {c.split("-")[0] for c in k["missing"]}) & set(page_cards):
            for card in page_cards[st]:
                if card in k["missing"]:
                    n.pop((team, card), None)
                else:
                    n[(team, card)] = max(n.get((team, card), 0), 1)
    return n
