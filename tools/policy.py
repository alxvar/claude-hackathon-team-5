"""Counterparty policy for every writer (Chief, Sat 16:20: the board is compressed, #1-#4 within 2 of us, #6-#8 within 3).

1. Never trade with the live top TOP_N unless our gain >= TOP_RATIO x theirs (theirs unknown: skip).
2. A page-closer (a card that may complete the counterparty's page) only to a team >= PAGE_CLOSER_GAP below us: a
   +50 (~ +4.7 board) jump can't lift a team 6 below past us, and our gain on those sales is +30-40 (unknown: skip).
3. RIVALS (Team 13, Team 17): no trade where their gain > ours (theirs unknown: skip).

    from policy import check
    ok, why = check("t16", teams=leaderboard_teams, our_gain=8.0, their_gain=3.1, page_closer=False)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESERVED, HANDOFF = ROOT / "run" / "reserved.json", ROOT / "run" / "operator-handoff.md"
_CARD = re.compile(r"\b[A-Z]{3}-\d{2}\b")

ME = "t05"
TOP_N = 5
TOP_RATIO = 3.0
PAGE_CLOSER_GAP = 6
RIVALS = frozenset({"t13", "t17"})


def reserved_refs(path: Path = RESERVED, handoff: Path = HANDOFF) -> set:
    """Cards no bot gives away: run/reserved.json {"cards": [...]}, else the cards named in the handoff's
    "## Reserved" section."""
    try:
        return set(json.loads(Path(path).read_text()).get("cards") or [])
    except (OSError, ValueError, AttributeError):
        pass
    try:
        text = Path(handoff).read_text()
    except OSError:
        return set()
    m = re.search(r"^## Reserved[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return set(_CARD.findall(m.group(1))) if m else set()


def ranked(teams) -> list:
    return sorted(teams or [], key=lambda t: -(t.get("score") or 0))


def top(teams, n: int = TOP_N) -> set:
    return {t["team"] for t in ranked(teams)[:n]}


def gap(team, teams, me: str = ME):
    """Our score minus theirs (> 0: they are below us), or None when either is unknown."""
    score = {t["team"]: t.get("score") for t in teams or []}
    ours, theirs = score.get(me), score.get(team)
    return None if ours is None or theirs is None else ours - theirs


def check(team, *, teams, our_gain=None, their_gain=None, page_closer=False, me: str = ME) -> tuple[bool, str]:
    """(may we trade with `team`, why not). Unknown team or leaderboard: no."""
    if not team or not teams:
        return False, "counterparty or leaderboard unknown"
    if team == me:
        return False, "ourselves"
    if team in top(teams):
        if our_gain is None or their_gain is None or our_gain < TOP_RATIO * max(their_gain, 0.0) or our_gain <= 0:
            return False, (f"{team} is in the top {TOP_N}: only if our gain >= {TOP_RATIO:g}x theirs "
                           f"(ours {our_gain}, theirs {their_gain})")
    if team in RIVALS and (their_gain is None or our_gain is None or their_gain > our_gain):
        return False, f"{team} is a rival: no trade where their gain ({their_gain}) > ours ({our_gain})"
    if page_closer:
        g = gap(team, teams, me)
        if g is None or g < PAGE_CLOSER_GAP:
            return False, f"page-closer for {team}: needs >= {PAGE_CLOSER_GAP} below us (gap {g})"
    return True, ""
