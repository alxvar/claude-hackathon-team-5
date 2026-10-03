"""Phone alert policy (Chief, Sat 17:40): every sender goes through here. Never writes to the game.

- Dani gets ACT items only: a person must get a named team to accept a named offer. Title
  "ACT · <what> · offer <id> · until HH:MM" (the offer's real expiry, wall time). At most ACT_PER_HOUR across all
  senders and processes (run/alerts_state.json, file-locked). An optional key (e.g. swaps' (team, give, get)) sends at
  most once per its window.
- Closing the loop: when an ACTed offer fills, expires or is cancelled, Dani gets "✓ DONE · <what>" or
  "✗ VOID · <what>" at priority 2 (close() by the sender that sees it, sweep() for our own offers, and expiry by time).
- Lucas gets CRITICAL only (duel failover, duelist tests red, the Chief's pages): critical().
- Everything else: log only.
- rivals(): the live top 6 and anyone within 3.0 board points of us: never an ACT that helps one.

    from alerts import act, close, critical, rivals
"""
from __future__ import annotations

import fcntl
import json
import time
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "run" / "alerts_state.json"
ACT_PER_HOUR = 4
ME = "t05"

try:
    from notify import notify as _notify
except Exception:  # noqa: BLE001
    try:
        from tools.notify import notify as _notify
    except Exception:  # noqa: BLE001
        _notify = None


def hhmm(ts: float) -> str:
    return time.strftime("%H:%M", time.localtime(ts))


def until_ts(expires_tick, tick, tick_seconds, now=None) -> float | None:
    """Wall time an offer expires, from its expires_tick and the clock."""
    if expires_tick is None or tick is None:
        return None
    return (now or time.time()) + max(0, int(expires_tick) - int(tick)) * float(tick_seconds or 30)


def rivals(teams, me: str = ME) -> set:
    """policy.rivals: the live top 6 plus every team within 3.0 board points of us; never us. Re-read at send time."""
    import policy
    return policy.rivals(teams, me)


@contextmanager
def _state(path: Path | None):
    path = Path(path or STATE)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(path) + ".lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            data = json.loads(path.read_text())
        except (OSError, ValueError):
            data = {}
        data.setdefault("acts", [])
        data.setdefault("keys", {})
        yield data
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=1))
        tmp.replace(path)
        fcntl.flock(lock, fcntl.LOCK_UN)


def act(what: str, offer, until: float | None, body: str, *, source: str, asset=None, want=None, want_n=None,
        key: str | None = None, key_every_s: float = 0, notifier=None, state: Path | None = None, now=None,
        log=print, quiet_close: bool = False) -> bool:
    """One ACT to Dani. False when it isn't sent (cap, key window, expired, no channel)."""
    notifier = notifier if notifier is not None else _notify
    now = now or time.time()
    if until is not None and until <= now:
        log(f"alerts: not sent (already expired): {what}")
        return False
    with _state(state) as s:
        if key and now - s["keys"].get(key, 0) < key_every_s:
            log(f"alerts: not sent (same {key} within {key_every_s / 3600:g} h): {what}")
            return False
        recent = [a for a in s["acts"] if now - a.get("sent", 0) < 3600]
        if len(recent) >= ACT_PER_HOUR:
            log(f"alerts: not sent (cap {ACT_PER_HOUR}/h reached): {what}")
            return False
        title = f"ACT · {what} · offer {offer} · until {hhmm(until) if until else '?'}"
        ok = bool(notifier and notifier("dani", title, body, priority=4, tags=["handshake"]))
        s["acts"].append({"offer": offer, "what": what, "until": until, "sent": now, "source": source,
                          "asset": asset, "want": want, "want_n": want_n, "closed": None, "quiet_close": quiet_close})
        s["acts"] = [a for a in s["acts"] if now - a.get("sent", 0) < 6 * 3600]
        if key:
            s["keys"][key] = now
        log(f"alerts: ACT {'sent' if ok else 'logged (no channel)'}: {title}")
        return True


def close(offer, done: bool, *, notifier=None, state: Path | None = None, now=None, log=print) -> bool:
    """Close one ACTed offer: DONE (filled) or VOID (expired, cancelled). Once per offer."""
    notifier = notifier if notifier is not None else _notify
    now = now or time.time()
    with _state(state) as s:
        for a in s["acts"]:
            if a.get("offer") == offer and not a.get("closed"):
                a["closed"] = {"done": done, "at": now}
                title = f"{'✓ DONE' if done else '✗ VOID'} · {a['what']}"
                if notifier and not a.get("quiet_close"):   # a suggestion just lapses: no VOID push
                    notifier("dani", title, f"Offer {offer}: {'filled' if done else 'expired or cancelled'}.",
                             priority=2, tags=["white_check_mark" if done else "x"])
                log(f"alerts: {title} (offer {offer})")
                return True
    return False


def open_acts(source: str | None = None, state: Path | None = None) -> list:
    with _state(state) as s:
        return [dict(a) for a in s["acts"] if not a.get("closed") and (source is None or a.get("source") == source)]


def sweep(*, open_offer_ids, asset_ids, counts, notifier=None, state: Path | None = None, now=None, log=print,
          sources=("opps", "swaps")) -> int:
    """Our own ACTed offers (opps, swaps): gone from /api/me/offers → DONE if its asset left us or the wanted card
    arrived, else VOID; still open past its expiry (+60 s) → VOID. Returns how many were closed."""
    now = now or time.time()
    closed = 0
    for a in open_acts(state=state):
        if a.get("source") not in sources:
            continue
        gone = a["offer"] not in open_offer_ids
        if gone:
            done = (a.get("asset") is not None and a["asset"] not in asset_ids) or \
                (a.get("want") is not None and counts.get(a["want"], 0) > (a.get("want_n") or 0))
            closed += close(a["offer"], done, notifier=notifier, state=state, now=now, log=log)
        elif a.get("until") and now > a["until"] + 60:
            closed += close(a["offer"], False, notifier=notifier, state=state, now=now, log=log)
    return closed


def expire(*, notifier=None, state: Path | None = None, now=None, log=print) -> int:
    """Any source: an ACT past its expiry (+60 s) that nobody closed is VOID."""
    now = now or time.time()
    n = 0
    for a in open_acts(state=state):
        if a.get("until") and now > a["until"] + 60:
            n += close(a["offer"], False, notifier=notifier, state=state, now=now, log=log)
    return n


def critical(title: str, body: str, *, notifier=None, tags=("rotating_light",)) -> bool:
    notifier = notifier or _notify
    """Lucas: CRITICAL only (duel failover, duelist tests red, the Chief's pages)."""
    return bool(notifier and notifier("lucas", title, body, priority=5, tags=list(tags)))
