"""Collector: the single source of truth every agent reads. Read-only, no LLM.

Every ~15 s: appends new feed events to data/feed.jsonl (by id), our state to data/me.jsonl (cash, score parts incl.
mm_points and bench_points, and our venue's value_created/trades/traders) and each new leaderboard snapshot to data/leaderboard.jsonl when they change, and rewrites data/board.json (El Rastro's open
offers, each tagged with the team behind it via the feed's offer.listed events). Every 2 minutes it rebuilds
intel/metrics.md (tools/metrics.py).

    source .env && python3 -u tools/collector.py
"""
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
sys.path.insert(0, str(ROOT / "tools"))
from bazaar_sdk import Bazaar, BazaarError  # noqa: E402
import metrics  # noqa: E402

DATA = ROOT / "data"
POLL, METRICS_EVERY = 15, 120


def append(path, obj):
    with path.open("a") as f:
        f.write(json.dumps(obj) + "\n")


ME_SCORE = ("score", "rank", "negotiating", "market", "neg_points", "mm_points", "ladder_points", "duel_points",
            "bench_efficiency", "bench_points", "deals")
ME_VENUE = ("value_created", "trades", "traders", "volume")


def me_row(me, t=None):
    """One data/me.jsonl row from GET /api/me: score parts plus our venue's numbers (venue_value_created, ...)."""
    s, v = me.get("score") or {}, me.get("venue") if isinstance(me.get("venue"), dict) else {}
    return {"t": time.time() if t is None else t, "tick": me.get("tick"), "cash": me.get("cash"),
            "level": me.get("level"), **{k: s.get(k) for k in ME_SCORE},
            **{f"venue_{k}": v.get(k) for k in ME_VENUE}}


def changed(row, last):
    """True when anything but the time and tick moved (a row is logged only then)."""
    return last is None or {k: v for k, v in row.items() if k not in ("t", "tick")} != \
        {k: v for k, v in last.items() if k not in ("t", "tick")}


def last_id(path):
    if not path.exists():
        return 0
    best = 0
    with path.open() as f:
        for line in f:
            best = max(best, json.loads(line)["id"])
    return best


def main():
    DATA.mkdir(exist_ok=True)
    b = Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"])
    pub = Bazaar(b.url, ""); pub._headers = {}  # keyless: public reads don't spend the team key's 5 req/s (duelist)
    feed_path, seen = DATA / "feed.jsonl", last_id(DATA / "feed.jsonl")
    makers, last_me, last_snap, last_metrics = {}, None, None, 0
    while True:
        try:
            for e in pub.feed(limit=1000).get("events", []):
                if e["id"] > seen:
                    append(feed_path, e)
                    seen = e["id"]
                if e["type"] == "offer.listed":
                    makers[e["payload"]["offer"]["id"]] = e["actor"]
            me = b.me()
            mine = me_row(me)
            if changed(mine, last_me):
                append(DATA / "me.jsonl", mine)
                last_me = mine
            lb = pub.leaderboard()
            if lb.get("snapshot_tick") != last_snap:
                append(DATA / "leaderboard.jsonl", {"t": time.time(), "tick": lb.get("snapshot_tick"),
                       "teams": [{k: t.get(k) for k in ("team", "name", "score", "negotiating", "market", "deals",
                                                    "album_filled", "album_slots", "pages_complete", "rarest")}
                                 for t in lb.get("teams", [])]})
                last_snap = lb.get("snapshot_tick")
            board = pub.board("rastro").get("offers", [])
            for o in board:
                o["team"] = makers.get(o["id"], "?")
            (DATA / "board.json").write_text(json.dumps({"t": time.time(), "me": me.get("id"), "offers": board}))
            if time.time() - last_metrics > METRICS_EVERY:
                metrics.write(b)
                last_metrics = time.time()
        except BazaarError as e:
            print(time.strftime("%H:%M:%S"), "collector:", e.code, e.message[:120], flush=True)
        except Exception as e:  # keep collecting through anything
            print(time.strftime("%H:%M:%S"), "collector error:", repr(e)[:200], flush=True)
        time.sleep(POLL)


if __name__ == "__main__":
    main()
