"""Sell ONE card to a dealer, negotiated, offer-only (never our accept), never at the dealer's opening price.

    set -a; . ./.env; set +a; python3 dealer_sell.py SAL-08 --dealer pilar --ask 36 --step 2 --floor 25

We ask high and step down; the dealer bids. When her bid is >= our floor, is not her opening bid (RULES: a deal at the
opening price never counts) and is final or within 1 of our ask, we offer exactly her bid as our ask, once, and wait
for her to accept. A final below the floor walks; 8 ticks stuck walks. Warm words, never our value or floor.
"""
import argparse
import os
import sys

sys.path.insert(0, "/Users/lucaswiese/Documents/claude-hackathon-team-5/agents/dealers")
import abuela_bot as ab  # noqa: E402

NAMES = {"chato": "Chato", "pilar": "Doña Pilar", "abuela": "Abuela", "picaros": "Paco, Nando"}
WARM = [
    "¡Buenos días, {name}! This {set} card is a lovely one: {p} P?",
    "Gracias, {name}, it's a pleasure to deal with you. {p} P, ¿te parece?",
    "It would sit beautifully in your collection, de verdad. {p} P?",
    "You're very kind to consider it, {name}. {p} P and it's yours.",
    "Muy amable. ¿{p} P y cerramos con una sonrisa?",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("card")
    ap.add_argument("--dealer", required=True)
    ap.add_argument("--ask", type=int, required=True, help="our opening ask")
    ap.add_argument("--step", type=int, required=True)
    ap.add_argument("--floor", type=int, required=True, help="the least we take on her FINAL (>= our value)")
    ap.add_argument("--min-ask", type=int, default=0, help="our lowest ask before her final (default: floor)")
    ap.add_argument("--accept-at", type=int, default=0, help="take a non-final bid at or above this (default: within 1 of our ask)")
    args = ap.parse_args()
    ab.DEALER = args.dealer
    b = ab.PacedBazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"],
                       min_gap=ab.GAP_S)
    me = b.me()
    asset = next((a for a in me["assets"] if a.get("ref") == args.card), None)
    if asset is None:
        sys.exit(f"we don't hold {args.card}")
    locked = {x["id"] for o in b.my_offers()["offers"] if o.get("maker") == me["id"] and o.get("status") == "open"
              for x in (o.get("give") or {}).get("assets") or []}
    if asset["id"] in locked:
        sys.exit(f"{args.card} is in one of our open offers: cancel it first (one channel per card)")
    value = float(asset.get("your_value") or b.value(args.card)["your_value"])  # the held copy (/value = one more copy)
    if args.floor < value:
        sys.exit(f"floor {args.floor} below value {value}")
    if any(t["with"] == args.dealer and t["status"] == "open" for t in b.my_threads()["threads"]):
        sys.exit(f"{args.dealer} already has an open conversation with us")
    before = {k: (me.get("score") or {}).get(k) for k in ("neg_points", "ladder_points")}
    t = b.open_thread(args.dealer, topic={"sell": {"assets": [asset["id"]]}})
    tid, ours, first, stuck, turn, matched, idle = t["id"], None, None, 0, 0, None, 0
    ab.log({"event": "open", "thread": tid, "card": args.card, "sell": True, "ask": args.ask, "floor": args.floor,
            "value": value, "dealer": args.dealer})
    while True:
        t = b.thread(tid)
        if t["status"] != "open":
            after = {k: (b.me().get("score") or {}).get(k) for k in ("neg_points", "ladder_points")}
            ab.log({"event": "end", "thread": tid, "status": t["status"], "first": first, "ours": ours,
                    "before": before, "after": after})
            print(t["status"], "her first", first, "ours", ours, before, "→", after)
            return
        hers = [o for o in t.get("standing_offers", []) if o.get("maker") == args.dealer and o.get("status") == "open"]
        if not hers:  # her offer expired (4 ticks) or none yet: walk after 6 empty ticks, never spin silently
            idle += 1
            if idle >= 6:
                b.close_thread(tid)
                ab.log({"event": "walk", "thread": tid, "ours": ours, "why": "no live dealer offer for 6 ticks"})
                continue
            b.wait_tick()
            continue
        idle = 0
        o = hers[-1]
        bid = ab.her_price(o, "sell")
        first = bid if first is None else first
        ab.log({"event": "tick", "thread": tid, "her_bid": bid, "final": o.get("final"), "ours": ours})
        if matched is not None:  # we offered her own bid: wait for her accept
            b.wait_tick()
            continue
        take = (o.get("final") and bid >= args.floor) or (args.accept_at and bid >= args.accept_at) or             (not args.accept_at and bid >= args.floor and ours is not None and ours - bid <= 1)
        if take and bid != first and ours is not None:
            b.say(tid, WARM[min(turn, len(WARM) - 1)].format(p=bid, set=args.card[:3], name=NAMES.get(args.dealer, args.dealer)), price=bid)
            matched = bid
            ab.log({"event": "offer_her_bid", "thread": tid, "price": bid})
            b.wait_tick()
            continue
        if o.get("final") and (bid < args.floor or bid == first):
            b.close_thread(tid)
            ab.log({"event": "walk", "thread": tid, "her_bid": bid, "ours": ours, "why": "final below floor or opening"})
            continue
        nxt = args.ask if ours is None else max(ours - args.step, args.min_ask or args.floor)  # small steps, never jump to her bid
        if ours is not None and nxt >= ours:  # can't move without repeating: stay silent
            stuck += 1
            if stuck >= 8:
                b.close_thread(tid)
                ab.log({"event": "walk", "thread": tid, "her_bid": bid, "ours": ours, "why": "stuck 8 ticks"})
                continue
            b.wait_tick()
            continue
        stuck = 0
        b.say(tid, WARM[min(turn, len(WARM) - 1)].format(p=nxt, set=args.card[:3], name=NAMES.get(args.dealer, args.dealer)), price=nxt)
        ab.log({"event": "say", "thread": tid, "price": nxt})
        ours, turn = nxt, turn + 1
        b.wait_tick()


if __name__ == "__main__":
    main()
