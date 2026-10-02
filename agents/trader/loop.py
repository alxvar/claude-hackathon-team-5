"""E3 on autopilot: every tick, take any El Rastro offer that gains value at our private values.

Two kinds of offer qualify:
- a team bids cash for a card we hold, and the cash minus the fee beats what that copy is worth to us;
- a team sells a card for less than it is worth to us, fee included.
When we accept, we pay El Rastro's fee (5% + 1 P per card). One accept per tick (the team limit), none while a
duel is live, never below the cash floor. Our own bids and listings stay up; their fills show up in the score.

    source .env && python3 -u agents/trader/loop.py --min-gain 3
"""
import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
from bazaar_sdk import Bazaar, BazaarError  # noqa: E402

LOG = ROOT / "logs" / "trader.jsonl"


def log(event):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    event = {"t": time.strftime("%H:%M:%S"), **event}
    with LOG.open("a") as f:
        f.write(json.dumps(event) + "\n")
    print(json.dumps(event), flush=True)


def fee(price, cards):
    return math.ceil(price * 0.05) + cards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-gain", type=float, default=3.0)
    ap.add_argument("--cash-floor", type=int, default=200)
    args = ap.parse_args()
    b = Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"])
    values, tried = {}, set()
    while True:
        try:
            me = b.me()
            held = {}
            for a in me["assets"]:
                if a["kind"] == "card":
                    held.setdefault(a["ref"], []).append(a)
            if values.get("_cash") != me["cash"] or values.get("_n") != len(me["assets"]):
                values = {"_cash": me["cash"], "_n": len(me["assets"])}  # holdings changed: values changed too
            best = None
            for o in b.board("rastro")["offers"]:
                if o["maker"] == me["id"] or o["id"] in tried:
                    continue
                g, w = o["give"], o["want"]
                cards = w.get("cards") or [t.split(":", 1)[1] for t in w.get("types", []) if t.startswith("card:")]
                if g.get("cash") and cards and len(cards) == 1 and cards[0] in held and not g.get("assets"):
                    copy = min(held[cards[0]], key=lambda a: a["your_value"])  # give away our least valuable copy
                    gain = g["cash"] - fee(g["cash"], 1) - copy["your_value"]
                    cand = (gain, o["id"], [copy["id"]], f"sell {cards[0]} for {g['cash']}")
                elif g.get("assets") and w.get("cash") and not cards and not w.get("assets"):
                    refs = [a["ref"] for a in g["assets"]]
                    for r in refs:
                        if r not in values:
                            values[r] = b.value(r)["your_value"]
                    cost = w["cash"] + fee(w["cash"], len(refs))
                    if me["cash"] - cost < args.cash_floor:
                        continue
                    gain = sum(values[r] for r in refs) - cost
                    cand = (gain, o["id"], None, f"buy {refs} for {w['cash']}")
                else:
                    continue
                if gain >= args.min_gain and (best is None or gain > best[0]):
                    best = cand
            if best and not b.duels().get("duels"):
                gain, oid, assets, what = best
                tried.add(oid)
                try:
                    b.accept(oid, assets=assets)
                    log({"event": "accept", "offer": oid, "what": what, "expected_gain": round(gain, 1)})
                except BazaarError as e:
                    log({"event": "refused", "offer": oid, "what": what, "code": e.code})
        except BazaarError as e:
            log({"event": "error", "code": e.code, "message": e.message[:150]})
        b.wait_tick()


if __name__ == "__main__":
    main()
