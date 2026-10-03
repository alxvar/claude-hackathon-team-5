"""Round-close archiver: freeze what a round looked like before the next one overwrites it. Read-only, no LLM.

A snapshot writes into archive/<YYYY-MM-DD>-round<N>/ (the date of the game day the round belongs to):
data-logs-<HHMMSS>.tgz (data/ and logs/; a file holding a key from .env is left out), leaderboard-<HHMMSS>.json
(GET /api/leaderboard), me-<HHMMSS>.json (GET /api/me: tick, cash, level and the score fields only, never the
assets or starter_broker_key) and one line in index.jsonl. Watch mode reads the public clock every N seconds and
snapshots when the doors close (the day's end) and when the round number changes (labelled with the round that ended).

    source .env && python3 tools/archive_round.py --now          # a manual snapshot of the current round
    source .env && python3 -u tools/archive_round.py --every 60  # watch (the `archiver` daemon)
"""
import argparse
import io
import json
import os
import sys
import tarfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
from bazaar_sdk import Bazaar, BazaarError  # noqa: E402

ARCHIVE = ROOT / "archive"
STATE = ROOT / "run" / "archiver.json"  # the last clock read, so a restart doesn't miss a boundary
SOURCES = ("data", "logs")
SECRETS = ("BAZAAR_KEY", "ANTHROPIC_API_KEY", "BROKER_KEY")
ME_FIELDS = ("id", "name", "tick", "cash", "level", "score")


def say(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def get_clock(url):
    with urllib.request.urlopen(url.rstrip("/") + "/api/clock", timeout=15) as r:  # public: no key spent
        return json.loads(r.read())


def label(clock):
    """<date of the clock's game day>-round<N>; today's local date if the clock doesn't say."""
    date = next((d.get("opens", "")[:10] for d in clock.get("days", []) if d.get("day") == clock.get("today")), "")
    return f"{date or time.strftime('%Y-%m-%d')}-round{clock.get('round', 0)}"


def tar_sources(dest, root=ROOT):
    """data/ and logs/ into dest (.tgz), leaving out any file that holds a key. Returns the files left out."""
    secrets = [os.environ[k].encode() for k in SECRETS if os.environ.get(k)]
    skipped = []
    tmp = dest.with_suffix(".tmp")
    with tarfile.open(tmp, "w:gz") as tar:
        for src in SOURCES:
            for p in sorted((root / src).rglob("*")):
                if not p.is_file():
                    continue
                try:
                    blob = p.read_bytes()  # a copy: the collector keeps writing while we read
                except OSError:
                    continue
                if any(s in blob for s in secrets):
                    skipped.append(str(p.relative_to(root)))
                    continue
                info = tarfile.TarInfo(str(p.relative_to(root)))
                info.size, info.mtime = len(blob), int(p.stat().st_mtime)
                tar.addfile(info, io.BytesIO(blob))
    os.replace(tmp, dest)
    return skipped


def snapshot(b, clock, reason, archive=ARCHIVE, root=ROOT):
    """One snapshot of the round `clock` describes. Returns its folder."""
    out = archive / label(clock)
    out.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%H%M%S")
    skipped = tar_sources(out / f"data-logs-{stamp}.tgz", root)
    entry = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "stamp": stamp, "reason": reason, "tick": clock.get("tick"),
             "round": clock.get("round"), "round_name": clock.get("round_name"), "skipped_files": skipped}
    try:
        (out / f"leaderboard-{stamp}.json").write_text(json.dumps(b.leaderboard(), indent=1))
        time.sleep(1)  # one game request per second
        me = b.me()
        (out / f"me-{stamp}.json").write_text(json.dumps({k: me.get(k) for k in ME_FIELDS}, indent=1))
    except BazaarError as e:
        entry["error"] = f"{e.code}: {e.message[:150]}"
    with (out / "index.jsonl").open("a") as f:
        f.write(json.dumps(entry) + "\n")
    say(f"snapshot {out.relative_to(archive.parent)} ({reason})" + (f" · skipped {skipped}" if skipped else "")
        + (f" · {entry['error']}" if "error" in entry else ""))
    return out


def triggers(prev, cur):
    """Why a snapshot is due between two clock reads, and of which clock: [(reason, clock)]."""
    if prev is None:
        return []
    due = []
    if prev.get("doors") != "closed" and cur.get("doors") == "closed":
        due.append((f"day closed ({cur.get('today_name') or cur.get('today')})", cur))
    if cur.get("round") is not None and prev.get("round") is not None and cur["round"] != prev["round"]:
        due.append((f"round {prev['round']} -> {cur['round']}", prev))  # file it under the round that ended
    return due


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--now", action="store_true", help="one snapshot of the current round, then exit")
    ap.add_argument("--every", type=int, default=0, help="watch: read the clock every N seconds")
    args = ap.parse_args()
    url = os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai")
    b = Bazaar(url, os.environ["BAZAAR_KEY"])
    if args.now or not args.every:
        snapshot(b, get_clock(url), "manual")
        return
    try:
        prev = json.loads(STATE.read_text())
    except (OSError, ValueError):
        prev = None
    say(f"archiver: watching the clock every {args.every} s")
    while True:
        try:
            cur = get_clock(url)
            for reason, clock in triggers(prev, cur):
                snapshot(b, clock, reason)
            prev = cur
            STATE.parent.mkdir(exist_ok=True)
            STATE.write_text(json.dumps(cur))
        except Exception as e:  # keep watching through anything
            say("archiver error:", repr(e)[:200])
        time.sleep(args.every)


if __name__ == "__main__":
    main()
