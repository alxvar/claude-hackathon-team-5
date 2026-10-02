"""Team-to-team trades on El Rastro (experiment E3): trade on the gap between our private values and other teams'.

    source .env && python3 agents/trader/trade.py scan                  # offers worth taking, our sellable cards
    source .env && python3 agents/trader/trade.py accept <offer_id>     # take an offer (checks it gains value)
    source .env && python3 agents/trader/trade.py sell <asset_id> <P>   # list one of our cards
    source .env && python3 agents/trader/trade.py want <card> <P>       # bid for any copy of a card
    source .env && python3 agents/trader/trade.py mine                  # our open offers

Every action prints the score before it, so the next `mine`/`scan` shows what the trade did.
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
from bazaar_sdk import Bazaar  # noqa: E402

FEE_BPS, FEE_PER_CARD = 500, 1  # El Rastro: 5% + 1 P per card
EXPIRES = 120                   # ticks an offer of ours stays up


def score(b):
    s = b.me().get("score") or {}
    return {k: s.get(k) for k in ("score", "negotiating", "neg_points", "ladder_points", "rank")}


def scan(b):
    me = b.me()
    held = {}
    for a in me["assets"]:
        if a["kind"] == "card":
            held.setdefault(a["ref"], []).append(a)
    for o in b.board("rastro")["offers"]:
        if o["maker"] == me["id"]:
            continue
        g, w = o["give"], o["want"]
        cards = w.get("cards") or [t.split(":", 1)[1] for t in w.get("types", []) if t.startswith("card:")]
        if g.get("cash") and cards and all(c in held for c in cards):  # they pay cash for a card we hold
            lose = sum(min(a["your_value"] for a in held[c]) for c in cards)
            print(f"SELL INTO {o['id']}: they pay {g['cash']} P for {cards}; worth {lose:.1f} to us → gain {g['cash'] - lose:+.1f}")
        if g.get("assets") and w.get("cash") and not cards:  # they sell a card for cash
            refs = [a["ref"] for a in g["assets"]]
            v = sum(b.value(r)["your_value"] for r in refs)
            fee = w["cash"] * FEE_BPS / 10000 + FEE_PER_CARD * len(refs)
            if v - w["cash"] - fee > 0:
                print(f"BUY {o['id']}: {refs} for {w['cash']} P (+fee {fee:.1f}); worth {v:.1f} to us → gain {v - w['cash'] - fee:+.1f}")
    print("score:", score(b))


def main():
    b = Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"])
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "scan":
        scan(b)
    elif cmd == "accept":
        print("before:", score(b))
        print(json.dumps(b.accept(int(args[0])))[:300])
    elif cmd == "sell":
        print("before:", score(b))
        print(json.dumps(b.list_offer({"assets": [int(args[0])]}, {"cash": int(args[1])}, venue="rastro",
                                      expires_in_ticks=EXPIRES))[:300])
    elif cmd == "want":
        print("before:", score(b))
        print(json.dumps(b.list_offer({"cash": int(args[1])}, {"cards": [args[0]]}, venue="rastro",
                                      expires_in_ticks=EXPIRES))[:300])
    elif cmd == "mine":
        me = b.me()
        for o in b.my_offers()["offers"]:
            if o["maker"] == me["id"]:
                print(o["id"], o["status"], "give", o["give"].get("cash") or [a["ref"] for a in o["give"].get("assets", [])],
                      "want", o["want"].get("cash") or o["want"].get("cards") or o["want"].get("types"), "expires", o.get("expires_tick"))
        print("score:", score(b), "cash:", me["cash"])


if __name__ == "__main__":
    main()
