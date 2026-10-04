"""Prints one line per change that matters, for a Claude Code Monitor (read-only, ~1 request/s on average).

Events (only what the operator acts on): our score components (not the relative score), our rank moving 2+ places
or the top 4 changing (the guardrails), organiser announcements and levels (not other teams' unlocks), dealers,
duels starting/ending, our deals settling, analysts writing (scout, judge, strategy), new lines in
intel/directives.md (Lucas's decisions), teammates' commits that touch team/, PLAN.md or CLAUDE.md.

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
    pub = Bazaar(b.url, ""); pub._headers = {}  # keyless: public reads don't spend the team key's 5 req/s (duelist)
    last = {}
    while True:
        try:
            me = b.me()
            s = me.get("score") or {}
            mine = {k: s.get(k) for k in ("score", "negotiating", "market", "neg_points", "ladder_points", "duel_points",
                                          "bench_efficiency", "deals")}
            d = {k: v for k, v in mine.items() if last.get("mine") and v != last["mine"].get(k)}
            if set(d) - {"score", "negotiating"}:  # the relative score moves every snapshot; only our components matter
                emit("OUR SCORE", f"{json.dumps(d)} (cash {me.get('cash')}, level {me.get('level')})")
            last["mine"] = mine

            lb = pub.leaderboard()
            if lb.get("snapshot_tick") != last.get("snap"):
                teams = sorted(lb.get("teams", []), key=lambda t: -(t.get("score") or 0))
                rank = next((i + 1 for i, t in enumerate(teams) if t.get("team") == me.get("id")), None)
                top = " | ".join(f"{i + 1} {t['name'].replace('Team ', 'T')} {t.get('score'):.1f}" for i, t in enumerate(teams[:5]))
                top4 = sorted(t.get("team") for t in teams[:4])  # the guardrails: never feed the top 4
                if last.get("snap") is not None and (abs((rank or 0) - last.get("rank", rank or 0)) >= 2 or top4 != last.get("top4")):
                    emit("LEADERBOARD", f"tick {lb.get('snapshot_tick')}: {top} || us #{rank} {s.get('score')} (top 4 now {top4})")
                    last["rank"] = rank
                last.setdefault("rank", rank)
                last["top4"] = top4
                last["snap"] = lb.get("snapshot_tick")

            ev = pub.feed(limit=200).get("events", [])
            seen = last.setdefault("feed", max((e["id"] for e in ev), default=0))
            for e in ev:
                if e["id"] <= seen:
                    continue
                p = e.get("payload", {})
                if e["type"] == "level.unlocked" and p.get("team") != me.get("id"):
                    continue  # another team unlocked a level: noise
                if e["type"] in ("announcement", "level.announced", "level.activated", "schedule.fired") or "level" in e["type"]:
                    emit("GAME", f"{e['type']} {json.dumps(p)[:200]}")
                elif e["type"] == "settlement" and me.get("id") in p.get("parties", []):
                    emit("OUR DEAL", f"{p.get('persona') or 'team trade'} {p.get('price')} P {[i['ref'] for i in p.get('items', [])]}")
            last["feed"] = max([seen] + [e["id"] for e in ev])

            lv = json.dumps(pub.levels().get("levels", []), sort_keys=True)
            dl = sorted((d["id"], d.get("status")) for d in pub.dealers().get("personas", []))
            if "lv" in last and (lv != last["lv"] or dl != last["dl"]):
                emit("LEVELS/DEALERS", f"levels {lv[:300]} · dealers {dl}")
            last["lv"], last["dl"] = lv, dl

            live = len(b.duels().get("duels", []))
            if "duels" in last and live != last["duels"]:
                emit("DUELS", f"{live} live (was {last['duels']})")
            last["duels"] = live

            d = ROOT / "intel" / "directives.md"  # Lucas's decisions, written by his strategy session: new lines only
            if d.exists() and d.stat().st_mtime != last.get("dir_t"):
                now = d.read_text().splitlines()
                if "dir" in last:
                    for line in [x for x in now if x.strip() and x not in last["dir"]]:
                        emit("DIRECTIVE", line[:300])
                last["dir"], last["dir_t"] = set(now), d.stat().st_mtime
            for name in ("scout.md", "judge.md", "strategy.md"):  # an analyst wrote: surface its first recommendation
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
                        files = subprocess.run(["git", "-C", str(ROOT), "show", "--name-only", "--format=", msg.split()[0]],
                                               capture_output=True, text=True).stdout.split()
                        if who != ME and any(f.startswith(("team/", "PLAN.md", "CLAUDE.md", "intel/directives.md")) for f in files):
                            emit("TEAMMATE PUSH", f"{who}: {msg} ({', '.join(files[:4])})")
                last["head"] = head
        except Exception as e:  # keep watching through a bad read
            emit("WATCH ERROR", repr(e)[:200])
        time.sleep(POLL)


if __name__ == "__main__":
    main()
