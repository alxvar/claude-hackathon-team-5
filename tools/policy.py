"""Counterparty policy for every writer (Chief, Sat 16:20: the board is compressed, #1-#4 within 2 of us, #6-#8 within 3).

1. Never trade with a rival unless our gain >= TOP_RATIO x theirs (theirs unknown: skip). A rival: the live top
   TOP_N, or any team within RIVAL_WITHIN board points of us (Chief 17:45: t10, #6 and 1.33 behind, slipped through).
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
TOP_N = 6
RIVAL_WITHIN = 3.0
TOP_RATIO = 3.0
PAGE_CLOSER_GAP = 6
RIVALS = frozenset({"t13", "t17"})
BOOK_ONLY = ("CHA-", "MAL-")   # directive 07:05: these sets are bought only through the Operator's books
NEVER_VENUES = frozenset({"v07"})   # Chief 07:15 (contra-market): Team 10's venue, whatever the leaderboard says
VENUE_ALLOW = None   # run/venue_allow.json ({"venues": ["v24"]}): rival venues allowed anyway (a venue pact); OFF when absent
_allow_cache: dict = {}


def venue_allow(path: Path | None = None) -> frozenset:
    """Rival-owned venues we may trade on anyway (Chief 10:35: the Team 13 pact, v24), from run/venue_allow.json,
    re-read whenever the file changes so the Operator turns it on or off without a restart. Absent, empty or unreadable:
    none (the default). Never v07 (NEVER_VENUES wins)."""
    p = Path(path or VENUE_ALLOW or ROOT / "run" / "venue_allow.json")
    try:
        stamp = p.stat().st_mtime_ns
    except OSError:
        return frozenset()
    if _allow_cache.get("key") != (str(p), stamp):
        try:
            data = json.loads(p.read_text())
            vs = data.get("venues") if isinstance(data, dict) else data
            vs = frozenset(v for v in vs or [] if isinstance(v, str)) - NEVER_VENUES
        except (OSError, ValueError, TypeError, AttributeError):
            vs = frozenset()
        _allow_cache.update(key=(str(p), stamp), venues=vs)
    return _allow_cache["venues"]


def reserved_refs(path: Path | None = None, handoff: Path | None = None) -> set:
    """Cards no bot gives away: run/reserved.json ({"cards": [...]} or a bare list of refs), else the cards named in
    the handoff's "## Reserved" section. Paths resolve at call time (tests point RESERVED/HANDOFF at tmp files)."""
    path, handoff = path or RESERVED, handoff or HANDOFF
    try:
        data = json.loads(Path(path).read_text())
        refs = data.get("cards") if isinstance(data, dict) else data
        if isinstance(refs, list):
            return {r for r in refs if isinstance(r, str) and _CARD.fullmatch(r)}
        print(f"policy: {path} has no list of cards: using the handoff", flush=True)
    except OSError:
        pass
    except ValueError as e:
        print(f"policy: {path} unreadable ({e}): using the handoff", flush=True)
    try:
        text = Path(handoff).read_text()
    except OSError:
        return set()
    m = re.search(r"^## Reserved[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return set(_CARD.findall(m.group(1))) if m else set()


def rival_venue(venue, owner, rivals) -> str:
    """Why a fill on `venue` would feed a rival ("" = fine): every trade on a team venue raises its owner's market
    score, so never v07, never a venue owned by `rivals` (rivals() | RIVALS), and never a team venue while the rivals
    or its owner are unknown. El Rastro ("rastro", the house) is always fine."""
    if venue in (None, "rastro"):
        return ""
    if venue in NEVER_VENUES:
        return f"{venue}: never (Team 10's venue)"
    if venue in venue_allow():
        return ""                                    # a venue pact (run/venue_allow.json): its owner still never trades
    if rivals is None:
        return f"{venue}: rivals unknown (no leaderboard read)"
    if not owner or owner == "?":
        return f"{venue}: owner unknown"
    if owner in rivals or owner in RIVALS:
        return f"{venue}: a rival's venue ({owner})"
    return ""


def book_only(ref) -> bool:
    """A card no taker script buys (reactor BUY lines, rbuy.py): its set goes through the Operator's books only."""
    return isinstance(ref, str) and ref.startswith(BOOK_ONLY)


def is_card(ref) -> bool:
    """A card id (SET-NN). Packs ("sobre_bienvenida") and other assets aren't: /api/me/value answers unknown_card for
    them (trader, Sat 22:41-22:45), so every value lookup skips them (Chief 23:30)."""
    return isinstance(ref, str) and bool(_CARD.fullmatch(ref))


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


def rivals(teams, me: str = ME, n: int | None = None, within: float | None = None) -> set:
    """The live top N plus every team within RIVAL_WITHIN board points of us (above or below); never us."""
    n, within = n or TOP_N, RIVAL_WITHIN if within is None else within
    out = top(teams, n)
    score = {t["team"]: t.get("score") for t in teams or []}
    ours = score.get(me)
    if ours is not None:
        out |= {t for t, s in score.items() if s is not None and abs(s - ours) <= within}
    out.discard(me)
    return out


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
    if team in rivals(teams, me):
        if our_gain is None or their_gain is None or our_gain < TOP_RATIO * max(their_gain, 0.0) or our_gain <= 0:
            return False, (f"{team} is in the top {TOP_N} or within {RIVAL_WITHIN:g} of us: only if our gain >= "
                           f"{TOP_RATIO:g}x theirs (ours {our_gain}, theirs {their_gain})")
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
