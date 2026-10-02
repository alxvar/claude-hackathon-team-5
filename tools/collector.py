"""Collector: the single source of truth every agent reads. Read-only, no LLM.

Every ~15 s: appends new feed events to data/feed.jsonl (by id), our state to data/me.jsonl and each new
leaderboard snapshot to data/leaderboard.jsonl when they change, and rewrites data/board.json (El Rastro's open
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
    feed_path, seen = DATA / "feed.jsonl", last_id(DATA / "feed.jsonl")
    makers, last_me, last_snap, last_metrics = {}, None, None, 0
    while True:
        try:
            for e in b.feed(limit=1000).get("events", []):
                if e["id"] > seen:
                    append(feed_path, e)
                    seen = e["id"]
                if e["type"] == "offer.listed":
                    makers[e["payload"]["offer"]["id"]] = e["actor"]
            me = b.me()
            s = me.get("score") or {}
            mine = {"t": time.time(), "tick": me.get("tick"), "cash": me.get("cash"), "level": me.get("level"),
                    **{k: s.get(k) for k in ("score", "rank", "negotiating", "market", "neg_points", "ladder_points",
                                             "duel_points", "bench_efficiency", "deals")}}
            if last_me is None or {k: v for k, v in mine.items() if k not in ("t", "tick")} != \
                    {k: v for k, v in last_me.items() if k not in ("t", "tick")}:
                append(DATA / "me.jsonl", mine)
                last_me = mine
            lb = b.leaderboard()
            if lb.get("snapshot_tick") != last_snap:
                append(DATA / "leaderboard.jsonl", {"t": time.time(), "tick": lb.get("snapshot_tick"),
                       "teams": [{k: t.get(k) for k in ("team", "name", "score", "negotiating", "market", "deals")}
                                 for t in lb.get("teams", [])]})
                last_snap = lb.get("snapshot_tick")
            board = b.board("rastro").get("offers", [])
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
