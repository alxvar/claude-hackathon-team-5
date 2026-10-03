"""One file per duel, kept in the repo, so every duel we play can be studied and the agent improved.

The runner's JSONL log (`logs/duelist/`, gitignored) is the raw trace of one run. A record is the whole duel in one
place, whichever run saw it: the session, how we read it, every raw payload, every decision with its latency and
cost, what we sent, the game's final payload, and our score before and after. Records live in `docs/duels/` and are
committed, so the team shares them and they survive a restart or a lost laptop. Nothing secret goes in them: the
payloads carry our limit for that duel, which means nothing once the duel is over.

Also kept: the public feed's duel events (`feed.jsonl`), which may name the team behind a rival's alias, and
`review` turns all of it into one table (`docs/duels/README.md`).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .adapter import as_number, as_offer, as_role, first
from .model import Role

RECORDS = Path(__file__).resolve().parents[2] / "docs" / "duels"


def duel_key(raw: dict[str, Any]) -> Any:
    return first(raw, "id", "duel_id", "duel")


class Records:
    def __init__(self, folder: Path = RECORDS):
        self.folder = folder
        folder.mkdir(parents=True, exist_ok=True)
        self.feed_path = folder / "feed.jsonl"
        self._feed_ids = {e.get("id") for e in self._read_jsonl(self.feed_path)}

    def path(self, key: Any) -> Path:
        return self.folder / f"duel-{key}.json"

    def load(self, key: Any) -> dict[str, Any] | None:
        p = self.path(key)
        try:
            return json.loads(p.read_text()) if p.exists() else None
        except json.JSONDecodeError:
            return None

    def finished(self, key: Any) -> bool:
        """Saved with the game's final payload: nothing more to learn about it."""
        rec = self.load(key)
        return bool(rec and rec.get("done"))

    def save(self, key: Any, **fields: Any) -> Path:
        """Merges `fields` into the duel's record; lists of events are extended, never replaced."""
        rec = self.load(key) or {"duel": key}
        for k, v in fields.items():
            if v is None:
                continue
            if isinstance(v, list) and isinstance(rec.get(k), list):
                seen = {json.dumps(x, sort_keys=True, default=str) for x in rec[k]}
                rec[k] += [x for x in v if json.dumps(x, sort_keys=True, default=str) not in seen]
            else:
                rec[k] = v
        p = self.path(key)
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(rec, indent=1, default=str, ensure_ascii=False))
        tmp.replace(p)
        return p

    def add_score(self, tick: Any, score: dict[str, Any]) -> None:
        """Our score whenever duel points move: duels end several at a time, so this is a timeline, not per duel."""
        p = self.folder / "scores.jsonl"
        last = (self._read_jsonl(p) or [{}])[-1]
        if last.get("duel_points") != score.get("duel_points"):
            with p.open("a") as f:
                f.write(json.dumps({"tick": tick, **{k: score.get(k) for k in
                                    ("duel_points", "negotiating", "score", "rank")}}) + "\n")

    def sessions(self) -> dict[Any, dict[str, Any]]:
        """Each duel session's params (name, duel_ticks, decay) by number, from the feed's `duels.scheduled`."""
        return sessions_in(self._read_jsonl(self.feed_path))

    def add_feed(self, events: list[dict[str, Any]]) -> int:
        """Keeps the feed's duel events (new ones only). Returns how many were new."""
        fresh = [e for e in events if str(e.get("type", "")).startswith("duel") and e.get("id") not in self._feed_ids]
        if fresh:
            with self.feed_path.open("a") as f:
                for e in sorted(fresh, key=lambda e: e.get("id") or 0):
                    f.write(json.dumps(e, default=str, ensure_ascii=False) + "\n")
                    self._feed_ids.add(e.get("id"))
        return len(fresh)

    def all(self) -> list[dict[str, Any]]:
        out = []
        for p in sorted(self.folder.glob("duel-*.json")):
            try:
                out.append(json.loads(p.read_text()))
            except json.JSONDecodeError:
                continue
        return out

    @staticmethod
    def _read_jsonl(p: Path) -> list[dict[str, Any]]:
        if not p.exists():
            return []
        out = []
        for line in p.read_text().splitlines():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return out


def sessions_in(events: list[dict[str, Any]]) -> dict[Any, dict[str, Any]]:
    return {e["payload"]["session"]: e["payload"] for e in events
            if e.get("type") == "duels.scheduled" and "session" in (e.get("payload") or {})}


# The review

def summary(rec: dict[str, Any], sessions: dict[Any, dict[str, Any]] | None = None) -> dict[str, Any]:
    """One row per duel. The session's name comes from the feed by the duel's own session number: Friday's
    records carry the schedule's next session ("Duels I") for the practice."""
    done = rec.get("done") or {}
    last = (rec.get("payloads") or [{}])[-1].get("raw") or {} if rec.get("payloads") else {}
    raw = {**last, **done}
    view = rec.get("view") or {}
    role = as_role(view.get("role") or first(raw, "role", "your_role", "side"))
    limit = view.get("limit")
    if limit is None:
        limit = as_number(first(raw, "your_limit", "limit", "your_cost", "your_value", "cost", "value"))
    sent = [s.get("move") or {} for s in rec.get("sent") or []]
    offers = [m.get("price") for m in sent if m.get("action") == "offer" and m.get("price") is not None]
    price = as_number(first(raw, "price", "deal_price", "final_price", "agreed_price"))
    if price is None and (o := as_offer(first(raw, "deal", "agreement", "final_offer"))):
        price = o.price
    status = first(raw, "status", "state", "outcome", "result")
    surplus = None
    if price is not None and limit is not None and role is not None:
        surplus = price - limit if role is Role.SELLER else limit - price
    decisions = rec.get("decisions") or []
    took = [d["took_s"] for d in decisions if d.get("took_s") is not None]
    return {
        "duel": rec.get("duel"),
        "session": ((sessions or {}).get(raw.get("session")) or rec.get("session") or {}).get("name"),
        "rival": view.get("rival") or first(raw, "rival", "rival_alias", "opponent", "alias"),
        "role": role.value if role else None,
        "limit": limit,
        "our_first": offers[0] if offers else None,
        "our_last": offers[-1] if offers else None,
        "moves": len(sent),
        "status": status if not isinstance(status, dict) else json.dumps(status),
        "price": price,
        "surplus": surplus,
        "points": first(raw, "points", "score", "share", "pie_share", "captured"),
        "avg_s": round(sum(took) / len(took), 1) if took else None,
        "max_s": max(took) if took else None,
        "cost_usd": round(sum(d.get("cost_usd") or 0 for d in decisions), 4),
        "fallbacks": sum(1 for s in sent if s.get("meta", {}).get("fallback")),
    }


COLUMNS = ["duel", "session", "rival", "role", "limit", "our_first", "our_last", "moves", "status", "price",
           "surplus", "points", "avg_s", "max_s", "cost_usd", "fallbacks"]


def review(records: Records) -> str:
    sessions = records.sessions()
    rows = [summary(r, sessions) for r in records.all()]
    cell = (lambda v: "" if v is None else str(v).replace("|", "/"))
    lines = ["# Duel records", "",
             "_Written by `uv run python -m agents.duelist review`. One `duel-<id>.json` per duel holds everything; "
             "`feed.jsonl` holds the public feed's duel events (they may name the team behind an alias); `scores.jsonl` our duel points over time._", "",
             "| " + " | ".join(COLUMNS) + " |", "|" + "---|" * len(COLUMNS)]
    lines += ["| " + " | ".join(cell(r[c]) for c in COLUMNS) + " |" for r in rows]
    if rows:
        deals = [r for r in rows if r["surplus"] is not None]
        took = [r["avg_s"] for r in rows if r["avg_s"] is not None]
        lines += ["", f"{len(rows)} duels · {len(deals)} with a price · "
                      f"mean surplus {round(sum(r['surplus'] for r in deals) / len(deals), 1) if deals else '—'} · "
                      f"mean decision {round(sum(took) / len(took), 1) if took else '—'} s · "
                      f"model spend ${round(sum(r['cost_usd'] for r in rows), 3)}"]
    return "\n".join(lines) + "\n"
