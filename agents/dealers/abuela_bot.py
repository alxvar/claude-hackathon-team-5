"""Dealer bot: negotiated deals with a dealer (Abuela by default; `--dealer` for the others), for the ladder
and the level unlocks.

Buys the missing cards we value most, from what the dealer's menu sells (cheapest rarity first), never
above our private value; with --sell-spares it first sells spare copies. Every deal is countered at least once, so none closes at her opening
price. Waits for the server's tick, never repeats a price, never accepts while a duel is live
(unless her offer is final), and never lets cash drop below the venue bond.

    source .env && python3 agents/dealers/abuela_bot.py --dry-run
    source .env && python3 agents/dealers/abuela_bot.py --deals 3
    source .env && python3 agents/dealers/abuela_bot.py --dealer <id> --deals 3 --dry-run
"""
import argparse
import collections
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
from bazaar_sdk import Bazaar, BazaarError  # noqa: E402

DEALER = "abuela"
CASH_FLOOR = 270     # venue bond (250) + opening fee (20)
EXPECTED_PRICE = 0.92  # dealers end near 0.9x list in the public data (Abuela: common 9 of 10, uncommon 21-24 of 25)
MIN_GAIN = 3         # buy only if our value beats the expected price by this much; never pay above value - MIN_GAIN
FIRST_COUNTER = 0.55  # buy: open at 55% of her first ask; sell: ask her first bid / 0.55
STEP = 0.3           # each counter closes 30% of the gap, at least 1 P
LOG = ROOT / "logs" / "dealers" / f"abuela-{time.strftime('%Y%m%d-%H%M%S')}.jsonl"

TEXTS = {
    "buy": [
        "Hola, Abuela! What a lovely stall. Could you do {p} P?",
        "Gracias, Abuela. I'm filling my album on a small budget: {p} P?",
        "You're very kind. Let me stretch a little: {p} P.",
        "I'd love to take it home today. Would {p} P work?",
        "Almost there, Abuela! {p} P and it's a deal for me.",
    ],
    "sell": [
        "Hola, Abuela! A spare one for your grandchildren's albums. {p} P?",
        "It's in perfect shape, Abuela. Could you do {p} P?",
        "You're very kind. I can come down a little: {p} P.",
        "Let's meet nicely, Abuela. {p} P?",
        "Almost there! {p} P and it's yours.",
    ],
}


def log(event: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    event = {"t": time.strftime("%H:%M:%S"), **event}
    with LOG.open("a") as f:
        f.write(json.dumps(event) + "\n")
    print(json.dumps(event), flush=True)


def her_price(offer: dict, side: str) -> int:
    """Cash in her offer: what she asks when we buy, what she pays when we sell."""
    want, give = offer.get("want", {}).get("cash", 0), offer.get("give", {}).get("cash", 0)
    return int(want if side == "buy" else give)


def duel_live(b: Bazaar) -> bool:
    try:
        return bool(b.duels().get("duels"))
    except BazaarError:
        return False


def negotiate(b: Bazaar, topic: dict, side: str, cap: int, tid: int = None, fast: bool = False) -> dict:
    """side 'buy': cap = the most we pay. side 'sell': cap = the least we take.
    With `tid`, pick up an open conversation where it stands."""
    better = (lambda x, y: x < y) if side == "buy" else (lambda x, y: x > y)  # x better for us than y
    first = ours = None
    turn = 0
    if tid is None:
        tid = b.open_thread(DEALER, topic=topic)["id"]
    else:
        for m in b.thread(tid)["messages"]:
            o = m.get("offer") or {}
            if not o:
                continue
            if m["sender"] == DEALER:
                first = first if first is not None else her_price(o, side)
            else:
                ours = int(o.get("give", {}).get("cash", 0) if side == "buy" else o.get("want", {}).get("cash", 0))
                turn += 1
    log({"event": "open", "thread": tid, "topic": topic, "cap": cap, "her_first": first, "ours": ours})
    while True:
        t = b.thread(tid)
        if t["status"] != "open":
            log({"event": "end", "thread": tid, "status": t["status"], "reason": t.get("closed_reason"),
                 "her_first": first, "ours_last": ours})
            return t
        hers = [o for o in t.get("standing_offers", []) if o.get("maker") == DEALER and o.get("status") == "open"]
        if not hers:
            b.wait_tick()
            continue
        o = hers[-1]
        price = her_price(o, side)
        first = first if first is not None else price
        within_cap = not better(cap, price)  # her price is at least as good for us as our cap
        if ours is None:
            nxt = round(first * FIRST_COUNTER) if side == "buy" else round(first / FIRST_COUNTER)
        else:
            gap = abs(price - ours)
            nxt = ours + max(1, round(gap * STEP)) if side == "buy" else ours - max(1, round(gap * STEP))
        nxt = min(nxt, cap) if side == "buy" else max(nxt, cap)
        crosses = ours is not None and not better(nxt, price)  # our next counter would match or pass hers
        close = ours is not None and abs(price - ours) <= 1
        log({"event": "tick", "thread": tid, "her": price, "final": o.get("final"), "ours": ours, "next": nxt})

        if within_cap and (o.get("final") or crosses or close or fast):  # fast: take her price now (a flip)
            if duel_live(b) and not o.get("final"):
                log({"event": "hold_accept_duel_live", "thread": tid})
                b.wait_tick()
                continue
            b.accept(o["id"])
            log({"event": "accept", "thread": tid, "price": price, "negotiated": price != first})
            b.wait_tick()
            continue
        if o.get("final") or nxt == ours:  # final outside our cap, or we can't move without repeating
            b.close_thread(tid)
            log({"event": "walk", "thread": tid, "her": price, "ours": ours, "final": o.get("final")})
            continue
        text = TEXTS[side][min(turn, len(TEXTS[side]) - 1)].format(p=nxt)
        b.say(tid, text, price=nxt)
        log({"event": "say", "thread": tid, "price": nxt, "text": text})
        ours, turn = nxt, turn + 1
        b.wait_tick()


def plan(b: Bazaar) -> tuple:
    me = b.me()
    by_ref = collections.defaultdict(list)
    for a in me["assets"]:
        if a["kind"] == "card":
            by_ref[a["ref"]].append(a)
    listed = {x["id"] for o in b.my_offers()["offers"] if o.get("maker") == me["id"] and o.get("status") == "open"
              for x in o.get("give", {}).get("assets", [])}
    sells = [a for copies in by_ref.values() if copies[0]["rarity"] in ("common", "uncommon") for a in copies[1:]
             if a["id"] not in listed]  # a spare already listed for other teams stays there
    sells.sort(key=lambda a: a["your_value"])
    cat = b.catalog()
    menu = b.dealer(DEALER).get("menu", {}).get("sells", [])
    list_price = {m["rarity"]: m.get("list_price", 0) for m in menu if "rarity" in m}
    buys = []  # (expected gain, our value, card): our private value minus the price we expect to pay
    for s in cat["sets"]:
        if not s.get("released"):
            continue
        for c in s["cards"]:
            if c["rarity"] in list_price:
                v = b.value(c["id"])["your_value"]
                gain = v - EXPECTED_PRICE * list_price[c["rarity"]]
                if gain >= MIN_GAIN:
                    buys.append((round(gain, 1), v, c["id"]))
    buys.sort(reverse=True)
    budget = max(0, me["cash"] - CASH_FLOOR)
    return me, sells, buys, budget


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deals", type=int, default=3, help="stop after this many deals")
    ap.add_argument("--dealer", default="abuela", help="dealer id, as GET /api/dealers lists it")
    ap.add_argument("--max-buy", type=int, default=0, help="optional extra cap per card (0 = our value is the cap)")
    ap.add_argument("--min-sell", type=int, default=3, help="never sell a spare for less than this")
    ap.add_argument("--sell-spares", action="store_true",
                    help="also sell unlisted spares to Abuela (a spare sold to a team at book scores more)")
    ap.add_argument("--resume-cap", type=int, default=0,
                    help="pick up an open Abuela conversation with this cap instead of refusing to start")
    ap.add_argument("--ladder", action="store_true",
                    help="new dealer: N negotiated deals on the cheapest menu items, packs included (ladder only)")
    ap.add_argument("--no-buy", action="store_true",
                    help="sell only: dealer buys barely move neg_points (LOG finding 0); buy from teams instead")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, write nothing")
    args = ap.parse_args()
    b = Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"])

    global DEALER
    DEALER = args.dealer
    me, sells, buys, budget = plan(b)
    clock = b.clock()
    print(f"tick {clock['tick']} ({clock['tick_seconds']}s) · cash {me['cash']} P · spend budget {budget} P · "
          f"duel live: {duel_live(b)}")
    print("sell (spares):", [(a["ref"], a["id"], a["your_value"]) for a in sells])
    print(f"dealer {DEALER} · buy (expected gain, our value, card):", buys[:8])
    busy = [t for t in b.my_threads()["threads"] if t["with"] == DEALER and t["status"] == "open"]
    if busy:
        print(f"Abuela already has an open conversation with us (thread {busy[0]['id']}).")
    if args.dry_run or (busy and not args.resume_cap):
        return

    def score():
        sc = b.me().get("score") or {}
        return {k: sc.get(k) for k in ("negotiating", "neg_points", "ladder_points")}

    def done_one(t, label):
        before = done_one.last
        after = score()
        log({"event": "score", "deal": label, "status": t["status"], "before": before, "after": after})
        done_one.last = after
        return t["status"] == "deal"
    done_one.last = score()

    def buy_round(limit):
        n = 0
        for gain, value, ref in buys:
            if n >= limit or ref in bought:
                continue
            cap = min(int(value - MIN_GAIN), max(0, b.me()["cash"] - CASH_FLOOR))
            if args.max_buy:
                cap = min(cap, args.max_buy)
            if cap < 1:
                log({"event": "skip_buy", "card": ref, "reason": "cash floor", "cash": b.me()["cash"]})
                break
            bought.add(ref)
            n += done_one(negotiate(b, {"buy": {"card": ref}}, "buy", cap), f"buy {ref}")
        return n

    def ladder_round(limit):
        """Ladder-only deals (a new dealer: 3 negotiated deals per level count, higher levels weigh more): the
        cheapest items on the menu, packs included, never above 90% of list. Dealer deals barely move neg_points."""
        menu = b.dealer(DEALER).get("menu", {}).get("sells", [])
        n = 0
        cat = b.catalog()
        held = {a["ref"] for a in b.me()["assets"] if a["kind"] == "card"}
        for m in sorted(menu, key=lambda m: m.get("list_price", 0)):
            if "rarity" not in m:
                continue  # packs: their value to us is unknown, and buying above value subtracts (LOG finding 13)
            options = sorted(((b.value(c["id"])["your_value"], c["id"]) for s in cat["sets"] if s.get("released")
                              for c in s["cards"] if c["rarity"] == m["rarity"] and c["id"] not in held), reverse=True)
            while n < limit and options:
                value, card = options.pop(0)
                cap = min(int(m.get("list_price", 0) * 0.9), int(value) - 1, max(0, b.me()["cash"] - CASH_FLOOR))
                if cap < 1:
                    break  # never above our private value
                topic = {"buy": {"card": card}}
                t = negotiate(b, topic, "buy", cap)
                n += done_one(t, f"ladder {topic}")
                if t["status"] != "deal" or "per_team_per_hour" in m and n >= m["per_team_per_hour"]:
                    break
        return n

    bought, deals = set(), 0
    if args.ladder:
        deals += ladder_round(args.deals)
        log({"event": "done", "deals": deals, "cash": b.me()["cash"], "score": score()})
        return
    if busy:  # pick it up: whoever opened it has stopped
        t0 = busy[0]
        side = "buy" if "buy" in t0["topic"] else "sell"
        t = negotiate(b, t0["topic"], side, args.resume_cap, tid=t0["id"])
        deals += t["status"] == "deal"
    if not args.no_buy:
        deals += buy_round(args.deals)  # what we can afford now, best expected gain first
    for a in (sells if args.sell_spares else []):  # spares are worth ~1 P to us: cash in, value up
        if deals >= args.deals:
            break
        cap = max(args.min_sell, int(a["your_value"]) + MIN_GAIN)
        deals += done_one(negotiate(b, {"sell": {"assets": [a["id"]]}}, "sell", cap), f"sell {a['ref']}")
    if not args.no_buy:
        deals += buy_round(args.deals - deals)  # the rest, with the cash the sales brought in
    log({"event": "done", "deals": deals, "cash": b.me()["cash"], "score": score()})


if __name__ == "__main__":
    main()
