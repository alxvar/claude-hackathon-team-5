"""Prints one line per change that matters, for a Claude Code Monitor (read-only, ~1 request/s on average).

Events: leaderboard snapshot (top 5 + us), our live score components, organiser announcements, levels and
dealers, duels starting/ending, commits on origin/main by someone else, our dealer deals settling.

    source .env && python3 -u tools/watch.py
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
from bazaar_sdk import Bazaar  # noqa: E402

POLL = 30
ME = subprocess.run(["git", "-C", str(ROOT), "config", "user.name"], capture_output=True, text=True).stdout.strip()


def emit(kind, msg):
    print(f"{time.strftime('%H:%M')} {kind}: {msg}", flush=True)


def main():
    b = Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"])
    last = {}
    while True:
        try:
            me = b.me()
            s = me.get("score") or {}
            mine = {k: s.get(k) for k in ("score", "negotiating", "market", "neg_points", "ladder_points", "duel_points",
                                          "bench_efficiency", "deals")}
            if last.get("mine") and mine != last["mine"]:
                d = {k: v for k, v in mine.items() if v != last["mine"].get(k)}
                emit("OUR SCORE", f"{json.dumps(d)} (cash {me.get('cash')}, level {me.get('level')})")
            last["mine"] = mine

            lb = b.leaderboard()
            if lb.get("snapshot_tick") != last.get("snap"):
                teams = sorted(lb.get("teams", []), key=lambda t: -(t.get("score") or 0))
                rank = next((i + 1 for i, t in enumerate(teams) if t.get("team") == me.get("id")), None)
                top = " | ".join(f"{i + 1} {t['name'].replace('Team ', 'T')} {t.get('score'):.1f}" for i, t in enumerate(teams[:5]))
                if last.get("snap") is not None:
                    emit("LEADERBOARD", f"tick {lb.get('snapshot_tick')}: {top} || us #{rank} {s.get('score')}")
                last["snap"] = lb.get("snapshot_tick")

            ev = b.feed(limit=200).get("events", [])
            seen = last.setdefault("feed", max((e["id"] for e in ev), default=0))
            for e in ev:
                if e["id"] <= seen:
                    continue
                p = e.get("payload", {})
                if e["type"] in ("announcement", "level.announced", "level.activated", "schedule.fired") or "level" in e["type"]:
                    emit("GAME", f"{e['type']} {json.dumps(p)[:200]}")
                elif e["type"] == "settlement" and me.get("id") in p.get("parties", []):
                    emit("OUR DEAL", f"{p.get('persona') or 'team trade'} {p.get('price')} P {[i['ref'] for i in p.get('items', [])]}")
            last["feed"] = max([seen] + [e["id"] for e in ev])

            lv = json.dumps(b.levels().get("levels", []), sort_keys=True)
            dl = sorted((d["id"], d.get("status")) for d in b.dealers().get("personas", []))
            if "lv" in last and (lv != last["lv"] or dl != last["dl"]):
                emit("LEVELS/DEALERS", f"levels {lv[:300]} · dealers {dl}")
            last["lv"], last["dl"] = lv, dl

            live = len(b.duels().get("duels", []))
            if "duels" in last and live != last["duels"]:
                emit("DUELS", f"{live} live (was {last['duels']})")
            last["duels"] = live

            for name in ("scout.md", "judge.md"):  # an analyst wrote: surface its first recommendation
                f = ROOT / "intel" / name
                if f.exists() and f.stat().st_mtime != last.get(name):
                    if name in last:
                        body = f.read_text().splitlines()
                        first = next((l for l in body if l.strip().startswith(("1.", "- ", "**1"))), "")
                        emit("INTEL", f"{name}: {first[:220]}")
                    last[name] = f.stat().st_mtime
            if int(time.time()) // 60 != last.get("git_min"):  # once a minute
                last["git_min"] = int(time.time()) // 60
                subprocess.run(["git", "-C", str(ROOT), "fetch", "-q"], capture_output=True)
                head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "origin/main"], capture_output=True, text=True).stdout.strip()
                if last.get("head") and head != last["head"]:
                    out = subprocess.run(["git", "-C", str(ROOT), "log", "--format=%an|%h %s", f"{last['head']}..{head}"],
                                         capture_output=True, text=True).stdout.splitlines()
                    for line in out:
                        who, msg = line.split("|", 1)
                        if who != ME:
                            emit("TEAMMATE PUSH", f"{who}: {msg}")
                last["head"] = head
        except Exception as e:  # keep watching through a bad read
            emit("WATCH ERROR", repr(e)[:200])
        time.sleep(POLL)


if __name__ == "__main__":
    main()
