"""Text-only dealer chat for the easter egg (no price ever, so no deal is possible). Prints every dealer reply verbatim
and any egg.* feed events. python3 egg_talk.py DEALER 'TOPIC_JSON' 'TEXT' [WAIT_S]"""
import json, os, sys, time
sys.path.insert(0, "/Users/lucaswiese/Documents/claude-hackathon-team-5/bazaar-kit")
from bazaar_sdk import Bazaar  # noqa: E402

dealer, topic, text = sys.argv[1], json.loads(sys.argv[2]), sys.argv[3]
wait = int(sys.argv[4]) if len(sys.argv) > 4 else 100
b = Bazaar(os.environ["BAZAAR_URL"], os.environ["BAZAAR_KEY"], wait_on_tick=False, timeout=8.0)
if any(t["with"] == dealer and t["status"] == "open" for t in b.my_threads()["threads"]):
    sys.exit(f"{dealer} thread already open")
assets0 = {a["id"] for a in b.me()["assets"]}
try:
    t = b.open_thread(dealer, topic=topic)
except Exception as e:  # noqa: BLE001
    print("open with topic failed:", repr(e)[:150], "→ retry without topic"); t = b.open_thread(dealer)
tid = t["id"]; print(time.strftime("%H:%M:%S"), "opened", tid, dealer, json.dumps(topic), flush=True)
seen = set()
def dump():
    th = b.thread(tid)
    for m in th.get("messages", []):
        if m.get("id") in seen: continue
        seen.add(m.get("id"))
        print(time.strftime("%H:%M:%S"), f"[{m.get('sender')}] offer={json.dumps(m.get('offer'))[:200]}\n  {m.get('text')}", flush=True)
    return th
time.sleep(3); dump()
b.say(tid, text); print(time.strftime("%H:%M:%S"), "sent (text only):", text, flush=True)
t0 = time.time()
while time.time() - t0 < wait:
    time.sleep(12)
    th = dump()
    if th["status"] != "open": print("thread", th["status"]); break
new = [a for a in b.me()["assets"] if a["id"] not in assets0]
print("NEW ASSETS:", json.dumps(new)[:400], flush=True)
try:
    if b.thread(tid)["status"] == "open": b.close_thread(tid); print("closed", tid, flush=True)
except Exception as e:  # noqa: BLE001
    print("close err", repr(e)[:100])
