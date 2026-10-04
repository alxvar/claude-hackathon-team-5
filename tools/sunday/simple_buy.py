"""Minimal dealer buy without wait_tick (the drivers hang there): poll every 12 s, small steps, hard deadline.

    python3 simple_buy.py SAL-06 --dealer abuela --open 21 --step 1 --cap 25 --floor-cash 100 --deadline 360
"""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, "/Users/lucaswiese/Documents/claude-hackathon-team-5/bazaar-kit")
from bazaar_sdk import Bazaar  # noqa: E402

TEXT = ["¡Hola, {n}! Buenos días. This one caught my eye: {p} P?",
        "Gracias, {n}, muy amable. {p} P, ¿te parece?",
        "We're a small team counting every prima, de verdad. {p} P?",
        "You're very kind. {p} P and we shake hands?"]
NAMES = {"abuela": "Abuela", "chato": "Chato", "pilar": "Doña Pilar", "picaros": "Paco, Nando"}


def log(**e):
    print(json.dumps({"t": time.strftime("%H:%M:%S"), **e}), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("card")
    ap.add_argument("--dealer", required=True)
    ap.add_argument("--open", type=int, required=True)
    ap.add_argument("--step", type=int, required=True)
    ap.add_argument("--cap", type=int, required=True)
    ap.add_argument("--floor-cash", type=int, required=True)
    ap.add_argument("--deadline", type=int, default=360)
    ap.add_argument("--resume", type=int, default=0)
    ap.add_argument("--offer-only", action="store_true", help="never accept: send their standing price as our offer")
    ap.add_argument("--first-text", default="", help="text of our FIRST priced message (e.g. the Pícaros egg line), {p} = price")
    a = ap.parse_args()
    b = Bazaar(os.environ["BAZAAR_URL"], os.environ["BAZAAR_KEY"], timeout=8.0, wait_on_tick=False, retries=1)
    me = b.me()
    if not a.resume and any(x.get("ref") == a.card for x in me["assets"]):
        sys.exit(f"already hold {a.card}")
    if me["cash"] - a.cap < a.floor_cash:
        sys.exit(f"cash {me['cash']} - cap {a.cap} < floor {a.floor_cash}")
    before = {k: me["score"].get(k) for k in ("neg_points", "ladder_points")}
    ours = None
    if a.resume:
        t = b.thread(a.resume)
        for m in t["messages"]:
            if m.get("sender") != a.dealer and (m.get("offer") or {}).get("give", {}).get("cash"):
                ours = int(m["offer"]["give"]["cash"])
    else:
        t = b.open_thread(a.dealer, topic={"buy": {"card": a.card}})
    tid, turn, first, accepted, t0 = t["id"], (1 if ours else 0), None, False, time.time()
    log(event="open", thread=tid, card=a.card, cap=a.cap)
    name = NAMES.get(a.dealer, a.dealer)
    while time.time() - t0 < a.deadline:
        try:
            t = b.thread(tid)
        except Exception as e:  # noqa: BLE001
            log(event="error", error=repr(e)[:120]); time.sleep(12); continue
        if t["status"] != "open":
            after = {k: b.me()["score"].get(k) for k in ("neg_points", "ladder_points")}
            log(event="end", status=t["status"], first=first, ours=ours, before=before, after=after); return
        hers = [o for o in t.get("standing_offers", []) if o.get("maker") == a.dealer and o.get("status") == "open"]
        if not hers:
            time.sleep(12); continue
        o = hers[-1]
        price = int((o.get("want") or {}).get("cash", 0))
        first = price if first is None else first
        log(event="tick", his=price, final=o.get("final"), ours=ours)
        if not accepted and ours is not None and price <= a.cap and price != first and (o.get("final") or price - ours <= 1):
            g, w = (o.get("give") or {}), (o.get("want") or {})
            refs = [x.get("ref") for x in g.get("assets", [])] + [t.split(":", 1)[1] for t in g.get("types", []) if t.startswith("card:")]
            if refs != [a.card] or g.get("cash") or w.get("assets") or w.get("types"):
                log(event="trick_guard", refs=refs, give=o.get("give"), want=o.get("want")); time.sleep(12); continue
            try:
                if a.offer_only:
                    b.say(tid, TEXT[min(turn, len(TEXT) - 1)].format(n=name, p=price), price=price)
                    log(event="offer_their_price", price=price)
                else:
                    b.accept(o["id"]); log(event="accept", price=price)
                accepted = True
            except Exception as e:  # noqa: BLE001
                log(event="accept_error", error=repr(e)[:120])
            time.sleep(12); continue
        if o.get("final") and price > a.cap:
            b.close_thread(tid); log(event="walk", his=price, ours=ours); continue
        nxt = a.open if ours is None else min(ours + a.step, price - 1, a.cap)
        her_turn = bool(t.get("messages")) and t["messages"][-1].get("sender") == a.dealer
        if ours is None or (nxt > ours and her_turn):  # one message per reply of hers: never two per tick
            try:
                txt = (a.first_text if (ours is None and a.first_text) else TEXT[min(turn, len(TEXT) - 1)]).format(n=name, p=nxt)
                b.say(tid, txt, price=nxt)
                log(event="say", price=nxt); ours, turn = nxt, turn + 1
            except Exception as e:  # noqa: BLE001  one message per tick: try again next poll
                log(event="say_wait", error=repr(e)[:80])
        time.sleep(12)
    log(event="deadline", ours=ours)
    try:
        if b.thread(tid)["status"] == "open":
            b.close_thread(tid); log(event="closed_at_deadline")
    except Exception as e:  # noqa: BLE001
        log(event="close_error", error=repr(e)[:120])


if __name__ == "__main__":
    main()
