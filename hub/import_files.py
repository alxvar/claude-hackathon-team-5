"""Load JSONL history into the hub; duplicates are skipped, so files can overlap and be loaded twice.

    uv run python -m hub.import_files data/feed.jsonl data/leaderboard.jsonl data/me.jsonl        # Lucas
    uv run python -m hub.import_files logs/dashboard/*.jsonl                                       # Dani
    uv run python -m hub.import_files docs/duels/feed.jsonl data/hub/feed-*.jsonl                  # anyone

Each line is classified by its shape, not its file name: a feed event ({id, type, payload}), a leaderboard snapshot
({tick, teams: [...] or {...}}), or one of our /api/me rows ({tick, cash or neg_points}). Anything else is counted
and skipped. Friday's history exists only in these files (the feed keeps the newest 500 events).
"""
import argparse
import json
import socket
import sys
from pathlib import Path

from psycopg.types.json import Jsonb

from hub.collect import SQL_LB, SQL_TEAM, Store
from hub.db import ROOT

BATCH = 2000


def classify(row: dict) -> str:
    if "id" in row and "type" in row and "payload" in row:
        return "event"
    if "teams" in row and "tick" in row:
        return "leaderboard"
    if "tick" in row and ("cash" in row or "neg_points" in row):
        return "me"
    return "other"


def event_id(row: dict, known_settlements: set):
    """The id to store an event under, or None to skip it. Real ids are positive. Backfilled settlements in Lucas's
    Friday file carry id -1: they get id = −settlement number, unless that settlement is already stored."""
    i = row.get("id")
    if isinstance(i, int) and not isinstance(i, bool) and i > 0:
        return i
    sid = (row.get("payload") or {}).get("settlement") if row.get("type") == "settlement" else None
    if isinstance(sid, int) and sid > 0 and sid not in known_settlements:
        return -sid
    return None


def leaderboard_teams(row: dict) -> list:
    """Lucas's files hold a list of teams, Dani's a dict keyed by team id; both become [{team, ...}]."""
    teams = row.get("teams")
    if isinstance(teams, dict):
        return [{"team": tid, **(v or {})} for tid, v in teams.items()]
    return [t for t in teams or [] if isinstance(t, dict)]


def import_file(store: Store, path: Path, source: str) -> dict:
    counts = {"event": 0, "event_new": 0, "no_id": 0, "leaderboard": 0, "me": 0, "other": 0, "bad": 0}
    events = []
    with store._c().cursor() as cur:
        cur.execute("select (payload->>'settlement')::bigint from hub.events where type = 'settlement'")
        known_settlements = {r[0] for r in cur.fetchall()}

    def flush():
        if events:
            counts["event_new"] += store.put_events(sorted(events, key=lambda e: e["id"]))
            events.clear()

    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError:
                counts["bad"] += 1
                continue
            kind = classify(row) if isinstance(row, dict) else "other"
            counts[kind] += 1
            if kind == "event":
                i = event_id(row, known_settlements)
                if i is None:
                    counts["no_id"] += 1
                    continue
                if row.get("type") == "settlement":
                    known_settlements.add((row.get("payload") or {}).get("settlement"))
                events.append({**row, "id": i})
                if len(events) >= BATCH:
                    flush()
            elif kind == "leaderboard":
                teams = leaderboard_teams(row)
                lb = {"snapshot_tick": row["tick"], "teams": teams}
                c = store._c()
                with c.transaction(), c.cursor() as cur:
                    cur.execute(SQL_LB, (row["tick"], row["tick"], None, None, source, Jsonb(row)))
                    cur.executemany(SQL_TEAM, [(row["tick"], t.get("team"), t.get("name"), t.get("rank"),
                                                t.get("score"), t.get("negotiating"), t.get("market"), t.get("level"),
                                                t.get("album_filled"), t.get("album_slots"), t.get("pages_complete"),
                                                t.get("luck"), t.get("deals"), t.get("venue"))
                                               for t in lb["teams"] if t.get("team")])
            elif kind == "me":
                with store._c().cursor() as cur:
                    cur.execute("""insert into hub.me_snapshots (tick, t, source, data) values (%s, %s, %s, %s)
                                   on conflict do nothing""",
                                (row["tick"], row.get("t") if isinstance(row.get("t"), (int, float)) else None,
                                 source, Jsonb(row)))
    flush()
    return counts


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--source", default=None, help="label stored with the rows (default: host:path)")
    a = ap.parse_args(argv)
    host = socket.gethostname().split(".")[0]
    for path in a.files:
        if not path.exists():
            print(f"{path}: missing, skipped")
            continue
        try:
            rel = path.resolve().relative_to(ROOT)
        except ValueError:
            rel = path
        source = a.source or f"{host}:{rel}"
        store = Store(source)
        c = import_file(store, path, source)
        store.reset()
        print(f"{path}: {c['event']} events ({c['event_new']} new, {c['no_id']} without a usable id), "
              f"{c['leaderboard']} leaderboard snapshots, "
              f"{c['me']} me rows, {c['other']} other, {c['bad']} unreadable")


if __name__ == "__main__":
    sys.exit(main())
