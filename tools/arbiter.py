"""Accept arbiter: may our bots spend the team's one accept this tick, or does a duel need it? (plan §5)

Hold only when BOTH hold true:
- a duel session that SCORES is live. The practice session is not: a duel's `session` number is looked up in the
  feed's `duels.scheduled` events (data/feed.jsonl, then one GET /api/feed per unknown session), whose name says
  "Practice duels"; with no event found, session 1 is the practice (RULES.md: "The first session of the weekend is
  a practice round that does not score"). /api/schedule can't tell: it lists only sessions still to come;
- one of our live duels in it needs the accept soon: the rival's standing offer is inside our limit, or
  ticks_left <= 3.
GET /api/duels is read at most once per tick (cached by tick).

    from arbiter import should_hold_accept
    hold, why = should_hold_accept(b, tick)      # tick: the current tick if the caller has it (saves a clock read)
    source .env && python3 tools/arbiter.py      # what it decides right now
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
from bazaar_sdk import Bazaar, BazaarError  # noqa: E402

FEED = ROOT / "data" / "feed.jsonl"
SOON = 3  # ticks_left at or below this: the duel may need the accept now
DONE = {"deal", "no_deal", "closed", "expired", "settled", "done", "walked", "cancelled", "failed"}
UNSCORED_WORDS = ("practice", "not scored", "unscored")

_cache = {"tick": None, "duels": None}  # the last GET /api/duels, by tick
_sessions = {}                           # session number -> scored? (True/False)
_last = {"scored_live": False}           # last known state, for when the read fails


def reset():
    """Forget every cache (tests)."""
    _cache.update(tick=None, duels=None)
    _sessions.clear()
    _last["scored_live"] = False


def _scored_from_event(payload):
    if "scored" in payload:
        return bool(payload["scored"])
    text = f"{payload.get('name', '')} {payload.get('note', '')}".lower()
    return not any(w in text for w in UNSCORED_WORDS)


def _scan(events):
    for e in events:
        if e.get("type") == "duels.scheduled" and "session" in (e.get("payload") or {}):
            _sessions[e["payload"]["session"]] = _scored_from_event(e["payload"])


def session_scored(b, duel):
    """Does this duel's session score? An explicit flag in the payload wins, then the feed, then RULES.md."""
    if "scored" in duel:
        return bool(duel["scored"])
    if duel.get("practice") is not None:
        return not duel["practice"]
    s = duel.get("session")
    if s not in _sessions and FEED.exists():
        with FEED.open() as f:
            _scan(json.loads(line) for line in f if '"duels.scheduled"' in line)
    if s not in _sessions:
        try:
            _scan(b.feed(limit=1000).get("events", []))
        except BazaarError:
            pass
        _sessions.setdefault(s, s != 1)  # [Uncertain] fallback: only session 1 is the practice
    return _sessions[s]


def _inside_limit(duel):
    o = duel.get("rival_offer")
    if not o or o.get("price") is None or duel.get("your_limit") is None:
        return False
    if "days" in (duel.get("issues") or []):
        return True  # price + days: the limit alone can't tell, so any standing offer counts [Uncertain]
    price, limit = o["price"], duel["your_limit"]
    return price <= limit if duel.get("role") == "buyer" else price >= limit


def _duels(b, tick):
    if tick is None or _cache["tick"] != tick:
        _cache.update(tick=tick, duels=b.duels().get("duels") or [])
    return _cache["duels"]


def should_hold_accept(b, tick=None):
    """(hold, reason). hold=True: leave this tick's accept to the duels."""
    try:
        if tick is None:
            tick = b.clock()["tick"]
        duels = _duels(b, tick)
    except BazaarError as e:  # can't see the duels: keep to what we last saw
        return _last["scored_live"], f"duels read failed ({e.code}); last seen scored duel live: {_last['scored_live']}"
    live = [d for d in duels if d.get("status") not in DONE]
    scored = [d for d in live if session_scored(b, d)]
    _last["scored_live"] = bool(scored)
    if not live:
        return False, "no live duel"
    if not scored:
        return False, f"{len(live)} live duel(s), none in a scored session (sessions {sorted({d.get('session') for d in live}, key=str)})"
    for d in scored:
        left = d.get("ticks_left")
        if left is None and d.get("deadline_tick") is not None:
            left = d["deadline_tick"] - tick
        if _inside_limit(d):
            return True, f"duel {d.get('duel')}: rival offer {d['rival_offer'].get('price')} inside our limit"
        if left is not None and left <= SOON:
            return True, f"duel {d.get('duel')}: {left} tick(s) left"
    return False, f"{len(scored)} scored duel(s) live, none needs the accept now"


if __name__ == "__main__":
    bz = Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"])
    print(should_hold_accept(bz))
