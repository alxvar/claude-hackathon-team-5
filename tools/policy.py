"""Counterparty policy for every writer (Chief, Sat 16:20: the board is compressed, #1-#4 within 2 of us, #6-#8 within 3).

1. Never trade with the live top TOP_N unless our gain >= TOP_RATIO x theirs (theirs unknown: skip).
2. A page-closer (a card that may complete the counterparty's page) only to a team >= PAGE_CLOSER_GAP below us: a
   +50 (~ +4.7 board) jump can't lift a team 6 below past us, and our gain on those sales is +30-40 (unknown: skip).
3. RIVALS (Team 13, Team 17): no trade where their gain > ours (theirs unknown: skip).
4. Never our LAST copy of a card of a complete page (Chief 17:05): copies committed in our open offers (asks, swaps)
   count as already gone, so two parallel offers can't each take "the spare". `last_copy(...)`; before a manual
   Workshop conversion: `python3 tools/policy.py can-give LAV-03` (reads /api/me and /api/me/offers).

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


def committed(offers, me_id: str = ME) -> set:
    """Asset ids in our open (or queued) offers."""
    return {a["id"] if isinstance(a, dict) else a for o in offers or []
            if o.get("maker") == me_id and o.get("status", "open") in ("open", "queued")
            for a in (o.get("give") or {}).get("assets") or []}


def last_copy(me: dict, ref: str, *, committed_ids=(), giving=()) -> str:
    """Why giving `giving` (asset ids) would take our last copy of `ref` in a complete page ("" = fine). Copies in
    `committed_ids` (our open offers) are already gone."""
    st = str(ref).split("-")[0]
    pages = {p.get("set"): p for p in (me.get("album") or {}).get("pages") or []}
    try:
        page_card = 1 <= int(str(ref).split("-")[1]) <= 10
    except (IndexError, ValueError):
        page_card = False
    if not page_card or not (pages.get(st) or {}).get("complete"):
        return ""
    gone = set(committed_ids) | set(giving)
    left = [a for a in me.get("assets") or [] if a.get("kind") == "card" and a.get("ref") == ref and a["id"] not in gone]
    return "" if left else f"{ref}: our last copy outside open offers of the complete {st} page"


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


def main(argv=None) -> None:
    import argparse
    import os
    import sys
    ap = argparse.ArgumentParser(description="policy checks", allow_abbrev=False)
    ap.add_argument("cmd", choices=["can-give"])
    ap.add_argument("card")
    args = ap.parse_args(argv)
    sys.path.insert(0, str(ROOT / "bazaar-kit"))
    from bazaar_sdk import Bazaar
    b = Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"])
    me = b.me()
    gone = committed(b.my_offers().get("offers"), me["id"])
    free = [a for a in me.get("assets") or [] if a.get("ref") == args.card and a["id"] not in gone]
    if args.card in reserved_refs():
        print(f"NO: {args.card} is reserved (run/reserved.json)")
        return
    if not free:
        print(f"NO: no free copy of {args.card} (none held, or all in our open offers)")
        return
    a = min(free, key=lambda x: x.get("your_value") or 0)
    why = last_copy(me, args.card, committed_ids=gone, giving={a["id"]})
    print(f"NO: {why}" if why else f"YES: give asset {a['id']} ({args.card}, worth {a.get('your_value')} to us)")


if __name__ == "__main__":
    main()
