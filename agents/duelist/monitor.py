"""Live monitor for the duelist: a local page that shows our duels as they happen (every message, our decisions and
holds, deals as they land) and every duel in the field as it closes.

    ~/.local/bin/uv run --project . python -m agents.duelist monitor            # then open http://127.0.0.1:8766

Read-only, and no load on the team key: our duels come from the records the live duelist writes (`docs/duels/`,
rewritten on every change it sees, so the page trails the game by the duelist's 2 s poll), the field from the
game's public feed, clock and schedule (keyless routes: 60 requests a second per IP). The game publishes other
teams' duels only as they close (`duel.closed`: duel, item, deal or no deal): no teams, prices or messages.
"""
from __future__ import annotations

import json
import os
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .records import RECORDS, sessions_in

ROOT = Path(__file__).resolve().parents[2]
LOGS = ROOT / "logs" / "duelist"
PAGE = Path(__file__).parent / "monitor.html"
URL = os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai")
FINAL = {"deal", "no_deal", "closed", "expired", "settled", "done", "walked", "cancelled", "failed"}
DUEL_EVENTS = ("duel.closed", "duels.scheduled", "duels.finished")


def get_json(path: str, timeout: float = 8.0) -> Any:
    """A keyless public read: never the team key."""
    with urllib.request.urlopen(urllib.request.Request(URL + path, headers={"Accept": "application/json"}),
                                timeout=timeout) as resp:
        return json.loads(resp.read())


class Public:
    """The game's public side, polled in the background: clock every 3 s, feed every 5 s (duel events kept, since
    the feed holds only the last few hundred events), schedule every minute."""

    def __init__(self, feed_file: Path = RECORDS / "feed.jsonl"):
        self.clock: dict[str, Any] = {}
        self.schedule: dict[str, Any] = {}
        self.events: dict[Any, dict[str, Any]] = {}
        self.errors: dict[str, str] = {}
        self.read_at: dict[str, float] = {}
        self.lock = threading.Lock()
        if feed_file.exists():
            for line in feed_file.read_text().splitlines():
                try:
                    self.keep([json.loads(line)])
                except json.JSONDecodeError:
                    continue

    def keep(self, events: list[dict[str, Any]]) -> None:
        with self.lock:
            for e in events:
                if e.get("type") in DUEL_EVENTS and e.get("id") is not None:
                    self.events[e["id"]] = e

    def poll(self, what: str, path: str, every: float) -> None:
        if time.monotonic() - self.read_at.get(what, -1e9) < every:
            return
        self.read_at[what] = time.monotonic()
        try:
            data = get_json(path)
        except Exception as e:                    # shown on the page; the loop goes on
            self.errors[what] = f"{type(e).__name__}: {e}"[:200]
            return
        self.errors.pop(what, None)
        if what == "feed":
            self.keep(data.get("events", []))
        else:
            with self.lock:
                setattr(self, what, data)

    def run(self) -> None:
        while True:
            self.poll("clock", "/api/clock", 3)
            self.poll("feed", "/api/feed?limit=300", 5)
            self.poll("schedule", "/api/schedule", 60)
            time.sleep(0.5)

    def start(self) -> Public:
        threading.Thread(target=self.run, daemon=True).start()
        return self


# Our duels, from the records

def latest_raw(rec: dict[str, Any]) -> dict[str, Any]:
    """The duel as the game last showed it: the final payload when it's over, else the last one seen."""
    last = (rec.get("payloads") or [{}])[-1].get("raw") or {}
    return {**last, **(rec.get("done") or {})} if rec.get("done") else last


def our_side(sign: int, limit: float, price: float | None) -> float | None:
    """What a price leaves us over our limit (price only): seller price - cost, buyer value - price."""
    return None if price is None or limit is None else sign * (price - limit)


def timeline(rec: dict[str, Any], raw: dict[str, Any]) -> list[dict[str, Any]]:
    """The messages as the game shows them, with our decision behind each of ours, plus what we decided without
    sending a message: holds (nothing sent) and acceptances."""
    msgs = [{"kind": "message", "tick": m.get("tick"), "mine": m.get("from") == "you", "who": m.get("from"),
             "text": m.get("text") or "", "price": m.get("price"), "days": m.get("days")}
            for m in raw.get("messages") or [] if isinstance(m, dict)]
    sent = {(s.get("tick"), (s.get("move") or {}).get("action")) for s in rec.get("sent") or []}
    out = list(msgs)
    for d in rec.get("decisions") or []:
        move, tick = d.get("move") or {}, d.get("tick")
        meta = move.get("meta") or {}
        note = {"tick": tick, "action": move.get("action"), "price": move.get("price"), "days": move.get("days"),
                "took_s": d.get("took_s"), "cost_usd": d.get("cost_usd"), "rule": meta.get("rule"),
                "fallback": meta.get("fallback"), "band": meta.get("band"),
                "read": (meta.get("plan") or {}).get("read"), "angle": (meta.get("plan") or {}).get("angle")}
        hold = d.get("hold") or (move.get("action") in ("offer", "message") and (tick, move.get("action")) not in sent)
        mine = next((m for m in msgs if m["mine"] and m["tick"] == tick and "decision" not in m), None)
        if move.get("action") == "accept":
            out.append({"kind": "accept", **note, "sent": (tick, "accept") in sent})
        elif hold:
            out.append({"kind": "hold", **note})
        elif mine is not None:
            mine["decision"] = note
    order = {"message": 0, "hold": 1, "accept": 2}
    return sorted(out, key=lambda e: (e["tick"] if e["tick"] is not None else -1, order[e["kind"]]))


def duel(rec: dict[str, Any], tick: int | None, sessions: dict[Any, dict[str, Any]]) -> dict[str, Any]:
    raw = latest_raw(rec)
    view = rec.get("view") or {}
    role = raw.get("role") or view.get("role")
    s = 1 if role == "seller" else -1
    limit = raw.get("your_limit", view.get("limit"))
    status = str(raw.get("status") or "?")
    deadline = raw.get("deadline_tick")
    if status not in FINAL and deadline is not None and tick is not None and tick >= deadline:
        status = "ended"                                   # over, result not in yet
    ours, theirs = raw.get("your_offer") or {}, raw.get("rival_offer") or {}
    decay = raw.get("decay_per_round") or view.get("decay") or 0
    rounds = raw.get("rounds") or 0
    their_gain = our_side(s, limit, theirs.get("price"))
    session = raw.get("session")
    events = timeline(rec, raw)
    costs = [d.get("cost_usd") or 0 for d in rec.get("decisions") or []]
    took = [d.get("took_s") for d in rec.get("decisions") or [] if d.get("took_s")]
    return {
        "id": rec.get("duel"), "session": session,
        "session_name": (sessions.get(session) or rec.get("session") or {}).get("name"),
        "role": role, "item": raw.get("item") or view.get("item"), "rival": raw.get("rival") or view.get("rival"),
        "issues": raw.get("issues") or view.get("issues") or ["price"], "limit": limit, "decay": decay,
        "status": status, "live": status == "live", "deadline": deadline,
        "ticks_left": deadline - tick if status == "live" and deadline is not None and tick is not None else None,
        "first_tick": next((e["tick"] for e in events if e.get("tick") is not None), rec.get("first_tick")),
        "rounds": rounds, "our_offer": ours.get("price"), "our_days": ours.get("days"),
        "their_offer": theirs.get("price"), "their_days": theirs.get("days"),
        "worth_now": round(their_gain * (1 - decay) ** rounds, 1) if their_gain is not None and their_gain > 0
        and "days" not in (raw.get("issues") or []) else None,
        "price": raw.get("price"), "days": raw.get("days"), "result": raw.get("result"),
        "surplus": our_side(s, limit, raw.get("price")),
        "messages": [sum(1 for e in events if e["kind"] == "message" and e["mine"] is m) for m in (True, False)],
        "holds": sum(1 for e in events if e["kind"] == "hold"),
        "cost_usd": round(sum(costs), 4), "avg_s": round(sum(took) / len(took), 1) if took else None,
        "events": events,
    }


class Ours:
    """Our duel records, re-read only when a file changes."""

    def __init__(self, folder: Path = RECORDS):
        self.folder = folder
        self.cache: dict[Path, tuple[float, dict[str, Any]]] = {}

    def all(self) -> list[dict[str, Any]]:
        out = []
        for p in self.folder.glob("duel-*.json"):
            try:
                m = p.stat().st_mtime
                if p not in self.cache or self.cache[p][0] != m:
                    self.cache[p] = (m, json.loads(p.read_text()))
                out.append(self.cache[p][1])
            except (OSError, json.JSONDecodeError):
                continue                                   # mid-write or gone: next poll
        return out

    def newest_change(self) -> float | None:
        return max((m for m, _ in self.cache.values()), default=None)


def duelist_status(logs: Path = LOGS, now: float | None = None) -> dict[str, Any]:
    """Is the duelist running (the pid in its lock file is alive), and when did it last write its log."""
    now = time.time() if now is None else now
    pid = None
    try:
        pid = int((logs / "run.lock").read_text().split()[1])
        os.kill(pid, 0)
        running = True
    except (OSError, ValueError, IndexError):
        running = False
    log = max(logs.glob("duels-*.jsonl"), key=lambda p: p.stat().st_mtime, default=None)
    errors = []
    if log is not None:
        with log.open("rb") as f:
            f.seek(max(0, log.stat().st_size - 200_000))
            for line in f.read().decode(errors="replace").splitlines()[1:]:
                try:
                    e = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if e.get("event") in ("error", "send_error", "foreign_message") and now - e.get("ts", 0) < 1800:
                    errors.append({"ago_s": round(now - e["ts"]), "event": e["event"], "duel": e.get("duel"),
                                   "what": str(e.get("code") or e.get("error") or e.get("where") or "")[:160]})
    return {"running": running, "pid": pid if running else None,
            "log_age_s": round(now - log.stat().st_mtime) if log else None, "errors": errors[-5:][::-1]}


def field(events: list[dict[str, Any]], ours: set[Any]) -> dict[str, Any]:
    """Every duel in the game, from the public feed: sessions and how far along they are, and each closing."""
    sessions: dict[Any, dict[str, Any]] = {}
    closed = []
    for e in sorted(events, key=lambda e: e["id"]):
        p = e.get("payload") or {}
        num = p.get("session")
        s = sessions.setdefault(num, {"session": num, "name": None, "total": None, "closed": 0, "deals": 0,
                                      "ours_closed": 0, "ours_deals": 0, "finished": False, "items": {}})
        if e["type"] == "duels.scheduled":
            s.update(name=p.get("name"), total=p.get("duels"), duel_ticks=p.get("duel_ticks"), decay=p.get("decay"),
                     started_tick=e.get("tick"))
        elif e["type"] == "duels.finished":
            s["finished"] = True
        elif e["type"] == "duel.closed":
            deal = p.get("status") == "deal"
            mine = p.get("duel") in ours
            s["closed"] += 1
            s["deals"] += deal
            s["ours_closed"] += mine
            s["ours_deals"] += deal and mine
            item = s["items"].setdefault(p.get("item"), [0, 0])
            item[0] += 1
            item[1] += deal
            closed.append({"tick": e.get("tick"), "duel": p.get("duel"), "session": num, "item": p.get("item"),
                           "status": p.get("status"), "ours": mine})
    for s in sessions.values():
        s["items"] = sorted(({"item": k, "closed": v[0], "deals": v[1]} for k, v in s["items"].items()),
                            key=lambda r: -r["closed"])
    return {"sessions": sorted(sessions.values(), key=lambda s: s["session"] or 0), "closed": closed[::-1][:400]}


def next_session(schedule: dict[str, Any], clock: dict[str, Any]) -> dict[str, Any] | None:
    """The next duel session on the schedule, with its tick and minutes away (a game hour is 60 minutes of ticks
    at any pace: 60 ticks of 60 s on Friday, 120 of 30 s on Saturday)."""
    nxt = next((u for u in schedule.get("upcoming", []) if u.get("action") == "duels"), None)
    t, tick, secs = clock.get("t_hours"), clock.get("tick"), clock.get("tick_seconds")
    if nxt is None:
        return None
    out = {"name": (nxt.get("params") or {}).get("name"), "at_hours": nxt.get("at_hours"), **(nxt.get("params") or {})}
    if None not in (t, tick, secs):
        hours = nxt["at_hours"] - t
        out.update(minutes=round(hours * 60), tick=round(tick + hours * 3600 / secs))
    return out


def state(public: Public, ours: Ours) -> dict[str, Any]:
    with public.lock:
        clock, schedule, events = dict(public.clock), dict(public.schedule), list(public.events.values())
    tick = clock.get("tick")
    recs = ours.all()
    sessions = sessions_in(events)
    duels = sorted((duel(r, tick, sessions) for r in recs), key=lambda d: (d["session"] or 0, d["id"] or 0))
    score = None
    try:
        lines = (RECORDS / "scores.jsonl").read_text().splitlines()
        score = json.loads(lines[-1]) if lines else None
    except (OSError, json.JSONDecodeError):
        pass
    newest = ours.newest_change()
    return {"now": time.time(), "clock": clock, "next_session": next_session(schedule, clock),
            "duelist": {**duelist_status(), "records_age_s": round(time.time() - newest) if newest else None},
            "public_errors": dict(public.errors), "score": score, "duels": duels,
            "field": field(events, {d["id"] for d in duels})}


def serve(port: int = 8766, host: str = "127.0.0.1") -> None:
    public, ours = Public().start(), Ours()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path.split("?")[0] == "/api/state":
                body, kind = json.dumps(state(public, ours), default=str).encode(), "application/json"
            elif self.path in ("/", "/index.html"):
                body, kind = PAGE.read_bytes(), "text/html; charset=utf-8"
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", kind)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_: Any) -> None:
            pass

    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"duel monitor on http://{host}:{port} (read-only: records in {RECORDS}, the game's public feed)",
          flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nmonitor stopped")
