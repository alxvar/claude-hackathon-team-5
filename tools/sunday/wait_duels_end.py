"""Block until the feed shows duels.finished for NAME (e.g. "Duels III") after now, or until --tick T / --until HHMM.
Exit 0 on finished, 2 on the fallback. Reads data/feed.jsonl by byte offset (no wc/tail quirks).
    python3 wait_duels_end.py "Duels III" --tick 1900 --until 1300"""
import json, os, sys, time, urllib.request
ROOT = "/Users/lucaswiese/Documents/claude-hackathon-team-5"
name = sys.argv[1]
tick_cap = int(sys.argv[sys.argv.index("--tick") + 1]) if "--tick" in sys.argv else None
until = int(sys.argv[sys.argv.index("--until") + 1]) if "--until" in sys.argv else None
path = ROOT + "/data/feed.jsonl"
pos = os.path.getsize(path)
def tick():
    try:
        r = urllib.request.Request(os.environ["BAZAAR_URL"] + "/api/clock", headers={"X-Team-Key": os.environ["BAZAAR_KEY"]})
        return json.load(urllib.request.urlopen(r, timeout=8)).get("tick", 0)
    except Exception:  # noqa: BLE001
        return 0
while True:
    with open(path) as f:
        f.seek(pos); chunk = f.read(); pos = f.tell()
    for line in chunk.splitlines():
        if '"duels.finished"' in line and name in line:
            print(time.strftime("%H:%M:%S"), "duels.finished", name, flush=True); sys.exit(0)
    if tick_cap and tick() >= tick_cap: print("tick fallback", tick_cap, flush=True); sys.exit(2)
    if until and int(time.strftime("%H%M")) >= until: print("time fallback", until, flush=True); sys.exit(2)
    time.sleep(20)
