"""Autoflip: fill other teams' bids with cards bought from a dealer, whenever it scores.

Every tick: read El Rastro's bids, keep those for cards the dealer sells (commons and uncommons of released sets)
where `bid - fee - our value of the card >= MIN_SCORE` (that is what the sale adds to neg_points, LOG finding 11) and
the cash comes back (bid - fee >= expected dealer price - MAX_CASH_LOSS). Buy the best one from the dealer, then
accept the bid with it. One flip at a time (one conversation per dealer), nothing while a duel is live.

    source .env && python3 -u agents/trader/autoflip.py
"""
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
sys.path.insert(0, str(ROOT / "agents" / "dealers"))
import abuela_bot as bot  # noqa: E402
from bazaar_sdk import Bazaar, BazaarError  # noqa: E402

MIN_SCORE = 8          # what the sale must add to neg_points
MAX_CASH_LOSS = 4      # how much cash a flip may lose (the score is what counts)
EXPECTED = {"common": 12, "uncommon": 29}  # Abuela's OPENING price: a flip takes it at once (bids last minutes)
CASH_FLOOR = 200


def fee(price):
    return math.ceil(price * 0.05) + 1


def best_flip(b, me, cat, tried):
    rar = {c["id"]: (c["rarity"], s["id"]) for s in cat["sets"] if s.get("released") for c in s["cards"]}
    held = {a["ref"] for a in me["assets"] if a["kind"] == "card"}
    best = None
    for o in b.board("rastro")["offers"]:
        g, w = o["give"], o["want"]
        cards = w.get("cards") or [t.split(":", 1)[1] for t in w.get("types", []) if t.startswith("card:")]
        if o["maker"] == me["id"] or o["id"] in tried or not g.get("cash") or len(cards) != 1 or g.get("assets"):
            continue
        card = cards[0]
        if card not in rar or rar[card][0] not in EXPECTED or card in held:  # held cards: loop.py sells those
            continue
        value = b.value(card)["your_value"]
        score = g["cash"] - fee(g["cash"]) - value
        cash = g["cash"] - fee(g["cash"]) - EXPECTED[rar[card][0]]
        if score >= MIN_SCORE and cash >= -MAX_CASH_LOSS and (best is None or score > best["score"]):
            best = {"offer": o["id"], "card": card, "bid": g["cash"], "score": round(score, 1), "cash": cash,
                    "cap": g["cash"] - fee(g["cash"]) + MAX_CASH_LOSS}
    return best


def main():
    b = Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"])
    cat, tried = b.catalog(), set()
    while True:
        try:
            me = b.me()
            f = best_flip(b, me, cat, tried) if me["cash"] > CASH_FLOOR + 30 else None
            if not f or b.duels().get("duels"):
                b.wait_tick()
                continue
            tried.add(f["offer"])
            bot.log({"event": "autoflip_start", **f})
            before = {a["id"] for a in me["assets"]}
            t = bot.negotiate(b, {"buy": {"card": f["card"]}}, "buy", f["cap"], fast=True)
            if t["status"] != "deal":
                bot.log({"event": "autoflip_no_deal", "card": f["card"], "status": t["status"]})
                continue
            b.wait_tick()  # the purchase settles
            new = [a for a in b.me()["assets"] if a["id"] not in before and a["ref"] == f["card"]]
            if not new:
                bot.log({"event": "autoflip_missing", "card": f["card"]})
                continue
            try:
                b.accept(f["offer"], assets=[new[0]["id"]])
                bot.log({"event": "autoflip_sold", "card": f["card"], "bid": f["bid"], "expected_score": f["score"]})
            except BazaarError as e:  # the bid is gone: list it at the bid instead
                o = b.list_offer({"assets": [new[0]["id"]]}, {"cash": f["bid"]}, venue="rastro", expires_in_ticks=180)
                bot.log({"event": "autoflip_listed", "card": f["card"], "price": f["bid"], "offer": o["id"], "why": e.code})
        except BazaarError as e:
            bot.log({"event": "autoflip_error", "code": e.code, "message": e.message[:150]})
            b.wait_tick()


if __name__ == "__main__":
    main()
