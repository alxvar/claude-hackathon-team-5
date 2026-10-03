"""Chato steady-step buyer (plan §4C): one negotiated buy, fixed step, never a repeated price, never above the cap.

    set -a; . ./.env; set +a; python3 agents/dealers/chato_steady.py RET-09 --cap 90 --open 57 --step 3 --cash-floor 100

Rares: open 55-60, constant +2 to +4 (never +1: early final 91-93; never jumps), bid just under his standing offer.
Uncommons: open 13-20, +1 per round, bid one under his standing offer (final 28-29).
Accepts his offer when it is within the cap and (final, or within 1 of ours). Stuck (next would repeat): stays silent
that tick instead of re-sending; walks after 8 stuck ticks (or 8 ticks of wall time stuck: Sat 13:02 a run sat 4+ min
silent at its cap) or on a final above the cap. Holds the accept during scored
duels (the dealer bot's arbiter). --offer-only: never accepts; offers his standing price instead, so he accepts and
spends the accept (dealer deals during scored duels without touching the team's one accept per tick).
"""
import argparse
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import abuela_bot as ab  # noqa: E402


WARM = [  # same price logic, warm words (Chief/Lucas 10:08): greet, thank every move, a human detail; never value/cap/cash
    "¡Hola, {name}! Buenos días. We're building our {page} page this morning: could you do {p} P for this one?",
    "Gracias, {name}, that's kind of you. We're a small team counting every prima: {p} P?",
    "Muy amable. This one would fill a gap on our {page} page. {p} P, ¿qué te parece?",
    "Thank you for working with us, de verdad. {p} P is what we can stretch to right now.",
    "Ay, {name}, you drive a fair bargain. ¿{p} P y cerramos con una sonrisa?",
    "We really appreciate the patience. {p} P? It would make our morning.",
]
NAMES = {"chato": "Chato", "abuela": "Abuela", "pilar": "Doña Pilar"}
PAGES = {"SAL": "Salamanca", "LAT": "La Latina", "LAV": "Lavapiés", "MAL": "Malasaña", "RET": "El Retiro",
         "CHA": "Chamberí"}


def words(turn, price, args):
    return WARM[0 if turn == 0 else 1 + (turn - 1) % (len(WARM) - 1)].format(
        p=price, name=NAMES.get(args.dealer, args.dealer.title()), page=PAGES.get(args.card[:3], args.card[:3]))


def page_check(b, args, cards):
    """(our hard cap, None) or (None, why not): never buy a page's last card from a dealer (its bonus scores only
    in a team trade). Re-read before opening and before every accept or matching offer."""
    _, hard, why = ab.check_buy(b, args.card, cards, b.me())
    return hard, why


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument("card")
    ap.add_argument("--cap", type=int, required=True)
    ap.add_argument("--open", type=int, required=True)
    ap.add_argument("--step", type=int, required=True)
    ap.add_argument("--cash-floor", type=int, required=True)
    ap.add_argument("--dealer", default="chato")
    ap.add_argument("--resume", type=int, default=0, help="pick up our open thread with this id (new cap)")
    ap.add_argument("--offer-only", action="store_true", help="never accept: offer his standing price instead")
    args = ap.parse_args(argv)
    ab.DEALER, ab.CASH_FLOOR = args.dealer, args.cash_floor
    b = ab.PacedBazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"],
                       min_gap=ab.GAP_S)
    me = b.me()
    held = {a["ref"] for a in me["assets"] if a["kind"] == "card"}
    if args.card in held:
        sys.exit(f"already hold {args.card}")
    cards = ab.card_index(b.catalog())
    hard, why = page_check(b, args, cards)
    if why:
        sys.exit(f"refused: {why}")
    cap = min(args.cap, me["cash"] - args.cash_floor, hard)
    if cap < args.open:
        sys.exit(f"cash {me['cash']} - floor {args.cash_floor} leaves cap {cap} < open {args.open}")
    if not args.resume and any(t["with"] == args.dealer and t["status"] == "open" for t in b.my_threads()["threads"]):
        sys.exit(f"{args.dealer} already has an open conversation with us")
    before = {k: (me.get("score") or {}).get(k) for k in ("neg_points", "ladder_points")}
    ours = None
    if args.resume:
        t = b.thread(args.resume)
        for m in t["messages"]:
            o = m.get("offer") or {}
            if o and m["sender"] != args.dealer:
                ours = int(o.get("give", {}).get("cash", 0))
    else:
        t = b.open_thread(args.dealer, topic={"buy": {"card": args.card}})
    tid, first, stuck, turn = t["id"], None, 0, 0 if ours is None else 1
    stuck_since, stuck_s = None, 8 * float(b.clock().get("tick_seconds") or 30)
    ab.log({"event": "open", "thread": tid, "card": args.card, "cap": cap, "open": args.open, "step": args.step})
    try:
        _loop(b, args, tid, first, stuck, turn, ours, cap, before, stuck_since, stuck_s, cards)
    finally:
        ab.watchdog_off()


def _loop(b, args, tid, first, stuck, turn, ours, cap, before, stuck_since, stuck_s, cards):
    idle, accepted = 0, False
    while True:
        ab.watchdog()
        t = b.thread(tid)
        if t["status"] != "open":
            after = {k: (b.me().get("score") or {}).get(k) for k in ("neg_points", "ladder_points")}
            ab.log({"event": "end", "thread": tid, "status": t["status"], "first": first, "ours": ours,
                    "before": before, "after": after})
            print(t["status"], "first", first, "ours", ours, before, "→", after)
            return
        hers = [o for o in t.get("standing_offers", []) if o.get("maker") == args.dealer and o.get("status") == "open"]
        if not hers:                              # his offer expired (4 ticks) and nobody moves: Sat 13:02 / 13:12
            idle += 1
            ab.log({"event": "no_live_offer", "thread": tid, "ticks": idle, "ours": ours})
            if idle >= ab.NO_OFFER_TICKS and not accepted:
                b.close_thread(tid)
                ab.log({"event": "walk", "thread": tid, "ours": ours,
                        "why": f"no live offer from {args.dealer} for {idle} ticks"})
                continue
            b.wait_tick()
            continue
        idle = 0
        o = hers[-1]
        price = ab.her_price(o, "buy")
        first = price if first is None else first
        ab.log({"event": "tick", "thread": tid, "his": price, "final": o.get("final"), "ours": ours})
        if price <= cap and ours is not None and (o.get("final") or price - ours <= 1):
            _, why = page_check(b, args, cards)
            if why:                               # another buy made this card the page's last one: teams only
                b.close_thread(tid)
                ab.log({"event": "walk", "thread": tid, "his": price, "ours": ours, "why": why})
                continue
            if args.offer_only:                   # never our accept: offer his price and let him accept
                if price == first:                # RULES: a deal at his OPENING price never counts: one notch below
                    price -= 1
                if ours == price:
                    ab.log({"event": "offer_matched_waiting", "thread": tid, "price": price})
                    b.wait_tick()
                    continue
                b.say(tid, words(turn, price, args), price=price)
                turn += 1
                ab.log({"event": "offer_his_price", "thread": tid, "price": price, "final": o.get("final")})
                ours = price
                b.wait_tick()
                continue
            hold, why = ab.should_hold_accept(b)
            if hold:
                ab.log({"event": "hold_accept_duel", "why": why})
                b.wait_tick()
                continue
            b.accept(o["id"])
            accepted = True
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
            stuck_since = stuck_since or time.monotonic()
            waited = time.monotonic() - stuck_since
            if stuck >= 8 or waited >= stuck_s:  # he holds above our cap: walk rather than sit in a thread
                b.close_thread(tid)
                ab.log({"event": "walk", "thread": tid, "his": price, "ours": ours,
                        "why": f"stuck {stuck} ticks, {waited:.0f} s"})
                continue
            b.wait_tick()
            continue
        stuck, stuck_since = 0, None
        b.say(tid, words(turn, nxt, args), price=nxt)
        turn += 1
        ab.log({"event": "say", "thread": tid, "price": nxt})
        ours = nxt
        b.wait_tick()


if __name__ == "__main__":
    main()
