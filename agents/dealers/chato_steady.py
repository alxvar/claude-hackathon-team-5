"""Chato steady-step buyer (plan §4C): one negotiated buy, fixed step, never a repeated price, never above the cap.

    set -a; . ./.env; set +a; python3 agents/dealers/chato_steady.py RET-09 --cap 90 --open 57 --step 3 --cash-floor 100

Rares: open 55-60, constant +2 to +4 (never +1: early final 91-93; never jumps), bid just under his standing offer.
Uncommons: open 13-20, +1 per round, bid one under his standing offer (final 28-29).
Accepts his offer when it is within the cap and (final, or within 1 of ours). Stuck (next would repeat): stays silent
that tick instead of re-sending; walks after 8 stuck ticks or on a final above the cap. Holds the accept during scored
duels (the dealer bot's arbiter).
"""
import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import abuela_bot as ab  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("card")
    ap.add_argument("--cap", type=int, required=True)
    ap.add_argument("--open", type=int, required=True)
    ap.add_argument("--step", type=int, required=True)
    ap.add_argument("--cash-floor", type=int, required=True)
    ap.add_argument("--dealer", default="chato")
    args = ap.parse_args()
    ab.DEALER, ab.CASH_FLOOR = args.dealer, args.cash_floor
    b = ab.PacedBazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"],
                       min_gap=ab.GAP_S)
    me = b.me()
    held = {a["ref"] for a in me["assets"] if a["kind"] == "card"}
    if args.card in held:
        sys.exit(f"already hold {args.card}")
    cap = min(args.cap, me["cash"] - args.cash_floor)
    if cap < args.open:
        sys.exit(f"cash {me['cash']} - floor {args.cash_floor} leaves cap {cap} < open {args.open}")
    if any(t["with"] == args.dealer and t["status"] == "open" for t in b.my_threads()["threads"]):
        sys.exit(f"{args.dealer} already has an open conversation with us")
    before = {k: (me.get("score") or {}).get(k) for k in ("neg_points", "ladder_points")}
    t = b.open_thread(args.dealer, topic={"buy": {"card": args.card}})
    tid, ours, first, stuck = t["id"], None, None, 0
    ab.log({"event": "open", "thread": tid, "card": args.card, "cap": cap, "open": args.open, "step": args.step})
    while True:
        t = b.thread(tid)
        if t["status"] != "open":
            after = {k: (b.me().get("score") or {}).get(k) for k in ("neg_points", "ladder_points")}
            ab.log({"event": "end", "thread": tid, "status": t["status"], "first": first, "ours": ours,
                    "before": before, "after": after})
            print(t["status"], "first", first, "ours", ours, before, "→", after)
            return
        hers = [o for o in t.get("standing_offers", []) if o.get("maker") == args.dealer and o.get("status") == "open"]
        if not hers:
            b.wait_tick()
            continue
        o = hers[-1]
        price = ab.her_price(o, "buy")
        first = price if first is None else first
        ab.log({"event": "tick", "thread": tid, "his": price, "final": o.get("final"), "ours": ours})
        if price <= cap and ours is not None and (o.get("final") or price - ours <= 1):
            hold, why = ab.should_hold_accept(b)
            if hold:
                ab.log({"event": "hold_accept_duel", "why": why})
                b.wait_tick()
                continue
            b.accept(o["id"])
            ab.log({"event": "accept", "thread": tid, "price": price})
            b.wait_tick()
            continue
        if o.get("final") and price > cap:
            b.close_thread(tid)
            ab.log({"event": "walk", "thread": tid, "his": price, "ours": ours})
            continue
        nxt = args.open if ours is None else min(ours + args.step, price - 1, cap)
        if ours is not None and nxt <= ours:  # can't move without repeating: stay silent this tick
            stuck += 1
            if stuck >= 8:  # he holds above our cap: walk rather than sit in a thread
                b.close_thread(tid)
                ab.log({"event": "walk", "thread": tid, "his": price, "ours": ours, "why": "stuck 8 ticks"})
                continue
            b.wait_tick()
            continue
        stuck = 0
        b.say(tid, f"I can do {nxt} P for it.", price=nxt)
        ab.log({"event": "say", "thread": tid, "price": nxt})
        ours = nxt
        b.wait_tick()


if __name__ == "__main__":
    main()
