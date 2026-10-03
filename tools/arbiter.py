"""Accept arbiter: may our bots spend the team's one accept this tick, or does a duel need it? (plan §5)

Hold only when BOTH hold true:
- a duel session that SCORES is live. The practice session is not: a duel's `session` number is looked up in the
  feed's `duels.scheduled` events (data/feed.jsonl, then one GET /api/feed per unknown session), whose name says
  "Practice duels"; with no event found, session 1 is the practice (RULES.md: "The first session of the weekend is
  a practice round that does not score"). /api/schedule can't tell: it lists only sessions still to come;
- one of our live duels in it needs the accept soon: the rival's standing offer is inside our limit, or
  ticks_left <= 3. With days (Duels II), "inside" is on the whole package, as the duelist values it: the price's
  margin over our limit plus what the day is worth to us (agents/duelist/days.read_days, guards.worth); a duel whose
  day weight can't be read counts any standing offer (Aleks's review 10:20: else 6 duels at once freeze our bots).
GET /api/duels is read at most once per tick (cached by tick).

ARBITER_HOLDS (env, default off; Chief 13:00 from the organisers' Duels deck [V]: duel messages and accepts have their
own limits and never block trading): off, it decides as above but never holds; each tick it would have held goes to
logs/arbiter.jsonl ("would have held"), so Duels II can show no duel accept ever failed. ARBITER_HOLDS=1 holds again.

    from arbiter import should_hold_accept
    hold, why = should_hold_accept(b, tick)      # tick: the current tick if the caller has it (saves a clock read)
    source .env && python3 tools/arbiter.py      # what it decides right now
"""
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
from bazaar_sdk import Bazaar, BazaarError  # noqa: E402

FEED = ROOT / "data" / "feed.jsonl"
LOG = ROOT / "logs" / "arbiter.jsonl"
SOON = 3  # ticks_left at or below this: the duel may need the accept now
DONE = {"deal", "no_deal", "closed", "expired", "settled", "done", "walked", "cancelled", "failed"}
UNSCORED_WORDS = ("practice", "not scored", "unscored")

_cache = {"tick": None, "duels": None}  # the last GET /api/duels, by tick
_sessions = {}                           # session number -> scored? (True/False)
_last = {"scored_live": False}           # last known state, for when the read fails
_logged = {"key": None}                  # the last (tick, reason) written to LOG


def reset():
    """Forget every cache (tests)."""
    _cache.update(tick=None, duels=None)
    _sessions.clear()
    _logged["key"] = None
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


def _day_values(duel):
    """What each delivery day is worth to us, read as the duelist reads it; None when the weight can't be read.
    days.py is stdlib only: the bots that import this module run on a bare python3 (no pydantic for guards.py)."""
    try:
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        from agents.duelist.days import read_days
        return read_days(duel.get("your_days_weight", duel.get("days_weight")), duel.get("days_meaning"))
    except Exception:  # noqa: BLE001
        return None


def _inside_limit(duel):
    """The rival's standing offer is worth >= 0 to us: guards.worth = the price's margin over our limit plus, with
    days, the day's value (0 at our best day, less elsewhere; an offer without a day counts at our worst)."""
    o = duel.get("rival_offer")
    if not o or o.get("price") is None or duel.get("your_limit") is None:
        return False
    margin = (duel["your_limit"] - o["price"]) if duel.get("role") == "buyer" else (o["price"] - duel["your_limit"])
    if "days" in (duel.get("issues") or []):
        dv = _day_values(duel)
        if dv is None:
            return True  # can't value the day: any standing offer counts (the duelist leaves these to the models)
        return margin + dv(o.get("days")) >= 0
    return margin >= 0


def _duels(b, tick):
    if tick is None or _cache["tick"] != tick:
        _cache.update(tick=tick, duels=b.duels().get("duels") or [])
    return _cache["duels"]


def holds_enabled() -> bool:
    return os.environ.get("ARBITER_HOLDS", "").strip().lower() in ("1", "true", "on", "yes")


def should_hold_accept(b, tick=None):
    """(hold, reason). hold=True: leave this tick's accept to the duels. With ARBITER_HOLDS off, never True: a tick it
    would have held is logged to LOG and the reason says "would have held"."""
    hold, why = decide(b, tick)
    if not hold or holds_enabled():
        return hold, why
    key = (_cache["tick"] if tick is None else tick, why)
    if _logged["key"] != key:
        _logged["key"] = key
        try:
            LOG.parent.mkdir(parents=True, exist_ok=True)
            with LOG.open("a") as f:
                f.write(json.dumps({"t": time.strftime("%H:%M:%S"), "tick": key[0], "pid": os.getpid(),
                                    "caller": Path(sys.argv[0]).name, "event": "would_have_held", "why": why}) + "\n")
        except OSError:
            pass
    return False, f"would have held: {why} (ARBITER_HOLDS off)"


def decide(b, tick=None):
    """(hold, reason) by the duel rules above, whatever ARBITER_HOLDS says."""
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
