"""Flip: buy from a dealer the cards we value least, list them for the teams that collect them.

Why it scores (LOG finding 11): `neg_points` counts only trades between teams, at OUR private values. Selling a card
worth 12.5 P to us (a La Latina uncommon, multiplier 0.5) for 26 P scores +13.5 whatever we paid the dealer, and a
dealer purchase neither scores nor subtracts. So the dealer is a cheap source, and the teams are the scoring buyers.

    source .env && python3 -u agents/trader/flip.py LAT-08:20:26 LAT-07:22:26
    (card:most we pay the dealer:price we list it at)
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
sys.path.insert(0, str(ROOT / "agents" / "dealers"))
import abuela_bot as bot  # noqa: E402
from bazaar_sdk import Bazaar, BazaarError  # noqa: E402

CASH_FLOOR = 200


def main():
    b = Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"])
    for spec in sys.argv[1:]:
        card, cap, price = spec.split(":")
        cap, price = int(cap), int(price)
        if b.me()["cash"] - cap < CASH_FLOOR:
            bot.log({"event": "flip_stop", "reason": "cash floor"})
            break
        if b.duels().get("duels"):
            bot.log({"event": "flip_wait", "reason": "duel live: the team's one accept per tick is the duel's"})
            b.wait_tick()
        before = {a["id"] for a in b.me()["assets"]}
        t = bot.negotiate(b, {"buy": {"card": card}}, "buy", cap)
        if t["status"] != "deal":
            bot.log({"event": "flip_skip", "card": card, "status": t["status"]})
            continue
        b.wait_tick()  # the purchase settles on the next tick
        new = [a for a in b.me()["assets"] if a["id"] not in before and a["ref"] == card]
        if not new:
            bot.log({"event": "flip_missing", "card": card})
            continue
        try:
            o = b.list_offer({"assets": [new[0]["id"]]}, {"cash": price}, venue="rastro", expires_in_ticks=180)
            bot.log({"event": "flip_listed", "card": card, "asset": new[0]["id"], "our_value": new[0]["your_value"],
                     "price": price, "offer": o["id"]})
        except BazaarError as e:
            bot.log({"event": "flip_list_failed", "card": card, "code": e.code})


if __name__ == "__main__":
    main()
