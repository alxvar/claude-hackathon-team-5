"""Writes STATUS.md from the live server (read-only) and, with --push, commits it every few minutes.

Score, cash, next scheduled events, our dealer deals, an Abuela price benchmark built from every
team's public settlements, duel results, levels. Only this script touches STATUS.md.

    source .env && python3 tools/status.py                      # write STATUS.md once
    source .env && python3 tools/status.py --every 300 --push   # keep it fresh on GitHub
"""
import argparse
import collections
import json
import os
import statistics
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
from bazaar_sdk import Bazaar, BazaarError  # noqa: E402

OUT = ROOT / "STATUS.md"
SETTLEMENTS = ROOT / "logs" / "feed_settlements.jsonl"  # local cache: the feed only keeps recent events


def fmt(x, nd=2):
    return "—" if x is None else (f"{x:.{nd}f}" if isinstance(x, float) else str(x))


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(fmt(c) for c in r) + " |" for r in rows]
    return out if rows else out + ["| " + " | ".join(["—"] * len(head)) + " |"]


def cached_settlements(b):
    """Every settlement seen so far, kept locally by id."""
    seen = {}
    if SETTLEMENTS.exists():
        for line in SETTLEMENTS.read_text().splitlines():
            s = json.loads(line)
            seen[s["settlement"]] = s
    new = [e["payload"] for e in b.feed(limit=1000).get("events", []) if e["type"] == "settlement"]
    fresh = [s for s in new if s["settlement"] not in seen]
    if fresh:
        SETTLEMENTS.parent.mkdir(parents=True, exist_ok=True)
        with SETTLEMENTS.open("a") as f:
            for s in fresh:
                f.write(json.dumps(s) + "\n")
                seen[s["settlement"]] = s
    return list(seen.values())


def item_key(it, rarity):
    return it["ref"] if it["kind"] == "pack" else f"{rarity.get(it['ref'], '?')} card"


def build(b):
    clock, me, sched = b.clock(), b.me(), b.schedule()
    s = me.get("score") or {}
    lb = b.leaderboard()
    cat = b.catalog()
    rarity = {c["id"]: c["rarity"] for st in cat["sets"] for c in st["cards"]}
    L = [
        "# Team 5 — live status",
        "",
        f"_Auto-updated by `tools/status.py` (read-only). Last update **{time.strftime('%a %H:%M')}** · tick "
        f"{clock['tick']} ({fmt(clock['tick_seconds'], 0)} s/tick) · game hour {fmt(clock['t_hours'])} · "
        f"{'PAUSED' if clock.get('paused') else 'running'} · today closes {clock.get('closes', '?')[11:16]}._",
        "",
        "## Score",
        "",
    ]
    L += table(["Total", "Rank", "Negotiating", "Market", "Duel pts", "Ladder pts", "Bench eff.", "Deals", "Level",
                "Cash", "Album"],
               [[s.get("score"), s.get("rank"), s.get("negotiating"), s.get("market"), s.get("duel_points"),
                 s.get("ladder_points"), s.get("bench_efficiency"), s.get("deals"), me.get("level"), me.get("cash"),
                 f"{s.get('album_filled')}/{s.get('album_slots')}"]])
    teams = sorted(lb.get("teams", []), key=lambda t: -(t.get("score") or 0))
    top = [[i + 1, t["name"], t.get("score"), t.get("negotiating"), t.get("market"), t.get("deals")]
           for i, t in enumerate(teams) if i < 5 or t.get("team") == me.get("id")]
    L += ["", f"Leaderboard (snapshot at tick {lb.get('snapshot_tick')}; refreshes every few minutes):", ""]
    L += table(["#", "Team", "Score", "Negotiating", "Market", "Deals"], top)

    L += ["", "## Next on the schedule", "",
          "_ETA assumes the current tick length and no pause._", ""]
    t_now, secs = clock["t_hours"], clock["tick_seconds"]
    try:
        to_close = (datetime.fromisoformat(clock["closes"]) - datetime.now().astimezone()).total_seconds() / 60
    except (KeyError, ValueError):
        to_close = None
    rows = []
    for e in sched.get("upcoming", [])[:8]:
        eta = (e["at_hours"] - t_now) * secs  # 60 ticks per game hour → minutes
        when = f"~{eta:.0f} min" + (" (after today's close)" if to_close is not None and eta > to_close else "")
        rows.append([fmt(e["at_hours"], 2), when, e["action"], e.get("note", "")])
    L += table(["Game hour", "ETA", "Action", "Note"], rows)

    L += ["", "## Our dealer deals", "",
          "_Her first = her first price in the conversation. A deal at her first price probably doesn't count as negotiated._", ""]
    rows = []
    for t in sorted(b.my_threads()["threads"], key=lambda t: t["id"]):
        if t.get("kind") != "persona":
            continue
        side = "buy" if "buy" in t["topic"] else "sell"
        hers = [m["offer"] for m in t["messages"] if m["sender"] == t["with"] and m.get("offer")]
        ours = [m["offer"] for m in t["messages"] if m["sender"] != t["with"] and m.get("offer")]
        cash = (lambda o: o["want"]["cash"]) if side == "buy" else (lambda o: o["give"]["cash"])
        ours_cash = (lambda o: o["give"]["cash"]) if side == "buy" else (lambda o: o["want"]["cash"])
        first = cash(hers[0]) if hers else None
        settled = [o for o in hers + ours if o.get("status") == "settled"]
        price = (cash(settled[0]) if settled[0]["maker"] == t["with"] else ours_cash(settled[0])) if settled else None
        vs = f"{(price - first) / first:+.0%}" if price is not None and first else "—"
        topic = t["topic"][side]
        what = topic.get("pack") or topic.get("card") or (f"{len(topic.get('assets', []))} card(s)" if "assets" in topic else json.dumps(topic))
        rows.append([t["id"], t["with"], side, what, first, ours_cash(ours[0]) if ours else None, price, vs,
                     len(t["messages"]), t["status"], t.get("closed_reason") or ""])
    L += table(["Thread", "Dealer", "Side", "Item", "Her first", "Our first", "Deal", "vs her first", "Msgs",
                "Status", "Closed"], rows)

    L += ["", "## Abuela benchmark: every team's deals with her (public feed)", ""]
    by = collections.defaultdict(lambda: {"us": [], "all": []})
    for st in cached_settlements(b):
        if st.get("persona") != "abuela":
            continue
        for it in st.get("items", []):
            side = "team buys" if it["frm"] == "abuela" else "team sells"
            k = (item_key(it, rarity), side)
            by[k]["all"].append(st["price"])
            if me.get("id") in st.get("parties", []):
                by[k]["us"].append(st["price"])
    rows = [[k[0], k[1], len(v["all"]), statistics.median(v["all"]), min(v["all"]), max(v["all"]),
             len(v["us"]), statistics.mean(v["us"]) if v["us"] else None]
            for k, v in sorted(by.items())]
    L += table(["Item", "Side", "All deals", "Median", "Min", "Max", "Ours", "Our avg"], rows)

    L += ["", "## Duels", ""]
    try:
        live, done = b.duels().get("duels", []), b.duels(done=True).get("duels", [])
    except BazaarError as e:
        live, done = [], []
        L += [f"_duels unavailable: {e.code}_"]
    L += [f"Live: {len(live)} · finished: {len(done)}", ""]
    for d in done[-12:]:
        L.append("- " + json.dumps({k: v for k, v in d.items() if k not in ("messages", "transcript")})[:300])

    L += ["", "## Dealers", ""]
    unlocked = set(me.get("unlocked") or [])
    L += table(["Dealer", "Status", "Level", "Open to us", "Sells", "Buys", "Deals/hour"],
               [[d["id"], d.get("status"), d.get("level"), d["id"] in unlocked,
                 ", ".join(str(m.get("pack") or m.get("rarity")) + (f" ({m['list_price']} P)" if m.get("list_price") else "")
                           for m in (d.get("menu") or {}).get("sells", [])),
                 ", ".join(str(m.get("rarity") or m.get("pack")) for m in (d.get("menu") or {}).get("buys", [])),
                 (d.get("menu") or {}).get("deals_per_team_per_hour")]
                for d in b.dealers().get("personas", [])])
    lv = b.levels().get("levels", [])
    L += ["", "## Levels", ""] + ([f"- {x.get('name')}: {x.get('status')} — {x.get('how') or x.get('line', '')}"
                                    for x in lv] or ["_None announced yet._"])
    return "\n".join(L) + "\n"


def push():
    git = ["git", "-C", str(ROOT)]
    subprocess.run(git + ["pull", "--rebase", "--autostash", "-q"], check=False)
    if subprocess.run(git + ["diff", "--quiet", "--", "STATUS.md"]).returncode == 0 and \
            subprocess.run(git + ["ls-files", "--error-unmatch", "STATUS.md"], capture_output=True).returncode == 0:
        return
    subprocess.run(git + ["add", "STATUS.md"], check=True)
    subprocess.run(git + ["commit", "-q", "-m", f"status: {time.strftime('%H:%M')}", "--", "STATUS.md"], check=True)
    subprocess.run(git + ["push", "-q", "origin", "main"], check=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--every", type=int, default=0, help="seconds between updates; 0 = once")
    ap.add_argument("--push", action="store_true", help="commit and push STATUS.md when it changes")
    args = ap.parse_args()
    b = Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"])
    while True:
        try:
            body = build(b)
            old = OUT.read_text() if OUT.exists() else ""
            if body.split("\n", 3)[3:] != old.split("\n", 3)[3:]:  # ignore the timestamp line
                OUT.write_text(body)
                if args.push:
                    push()
            print(time.strftime("%H:%M:%S"), "status ok", flush=True)
        except Exception as e:  # keep running through a bad read or a git hiccup
            print(time.strftime("%H:%M:%S"), "status error:", repr(e)[:300], flush=True)
        if not args.every:
            break
        time.sleep(args.every)


if __name__ == "__main__":
    main()
