"""Pícaros flag probe: a BUY thread for one rare, text-only messages (no price, so no deal is possible), print every
Pícaros message with its structured card vs the card named in the words. Flags are filed by hand.

    python3 flag_probe.py MAL-10 --until 1756
"""
import json, os, re, sys, time, urllib.request
sys.path.insert(0, "/Users/lucaswiese/Documents/claude-hackathon-team-5/bazaar-kit")
from bazaar_sdk import Bazaar  # noqa: E402

TEXTS = ["¡Hola, Paco y Nando! We heard you might have {name}. Could you tell us about it?",
         "Gracias. What is the exact card in your offer, please?",
         "Muy amable. We're thinking about it; tell us more about this copy.",
         "Interesting. Is that the same card you described?",
         "We need a moment to count our primas, amigos.",
         "Gracias por la charla. We'll think it over."]


def main():
    card, until = sys.argv[1], int(sys.argv[sys.argv.index("--until") + 1])
    url, key = os.environ["BAZAAR_URL"], os.environ["BAZAAR_KEY"]
    b = Bazaar(url, key, wait_on_tick=False, timeout=8.0, retries=1)
    cat = urllib.request.urlopen(urllib.request.Request(url + "/api/catalog", headers={"X-Team-Key": key}), timeout=8).read().decode()
    names = dict(re.findall(r'\{"id":"([A-Z]{3}-\d\d)","name":"([^"]+)"', cat))
    if any(t["with"] == "picaros" and t["status"] == "open" for t in b.my_threads()["threads"]):
        sys.exit("picaros thread already open")
    t = b.open_thread("picaros", topic={"buy": {"card": card}})
    tid, sent, seen = t["id"], 0, set()
    print(json.dumps({"t": time.strftime("%H:%M:%S"), "event": "open", "thread": tid, "card": card}), flush=True)
    while int(time.strftime("%H%M")) < until:
        try:
            t = b.thread(tid)
        except Exception as e:  # noqa: BLE001
            print("ERR", repr(e)[:100], flush=True); time.sleep(15); continue
        if t["status"] != "open":
            print(json.dumps({"event": "closed_by_them", "status": t["status"]}), flush=True); return
        msgs = t.get("messages", [])
        for m in msgs:
            if m.get("id") in seen or m.get("sender") != "picaros":
                seen.add(m.get("id")); continue
            seen.add(m.get("id"))
            g = (m.get("offer") or {}).get("give") or {}
            refs = [a.get("ref") for a in g.get("assets", [])] + [x.split(":", 1)[1] for x in g.get("types", []) if x.startswith("card:")]
            text = m.get("text") or ""
            named = [r for r, n in names.items() if n.lower() in text.lower()]
            mism = bool(refs) and (refs != [card] or (named and any(r not in refs for r in named)))
            print(json.dumps({"t": time.strftime("%H:%M:%S"), "msg": m.get("id"), "struct": refs, "named": named,
                              "price": (m.get("offer") or {}).get("want", {}).get("cash") if m.get("offer") else None,
                              "MISMATCH": mism, "text": text[:300]}), flush=True)
        if msgs and msgs[-1].get("sender") == "picaros" and sent < len(TEXTS):
            try:
                b.say(tid, TEXTS[sent].format(name=names.get(card, card)))
                sent += 1
            except Exception as e:  # noqa: BLE001
                print("say_wait", repr(e)[:80], flush=True)
        time.sleep(15)
    try:
        b.close_thread(tid); print(json.dumps({"event": "closed", "thread": tid}), flush=True)
    except Exception as e:  # noqa: BLE001
        print("close_err", repr(e)[:100], flush=True)


if __name__ == "__main__":
    main()
