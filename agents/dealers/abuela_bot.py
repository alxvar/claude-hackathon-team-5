"""Dealer bot: negotiated deals with a dealer (Abuela by default; `--dealer` for the others), for the ladder
and the level unlocks.

Buys the missing cards we value most, from what the dealer's menu sells (cheapest rarity first), never
above our private value; with --sell-spares it first sells spare copies. Every deal is countered at least once, so none closes at her opening
price. Waits for the server's tick, never repeats a price, holds every accept (her final offers too) while a
scored duel needs the team's accept (tools/arbiter.py), and never lets cash drop below the venue bond.

Hard limits (intel/ORCHESTRATOR.md), checked with a fresh value lookup right before every buy:
- never a page-completing card from a dealer: our value of it above book x our affinity + 0.5 means it carries the
  page bonus, which scores only through a TEAM trade (a dealer buy of it scores <= 0);
- pay at most our value, or value - 4 while we hold an unopened pack.
An exception inside a negotiation closes that dealer conversation (best effort), logs it and stops the run. Requests
are paced 0.25 s apart (1 s in --dry-run).

    source .env && python3 agents/dealers/abuela_bot.py --dry-run
    source .env && python3 agents/dealers/abuela_bot.py --deals 3
    source .env && python3 agents/dealers/abuela_bot.py --dealer <id> --deals 3 --dry-run
"""
import argparse
import collections
import json
import math
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
sys.path.insert(0, str(ROOT / "tools"))
from bazaar_sdk import Bazaar, BazaarError  # noqa: E402
from arbiter import should_hold_accept  # noqa: E402

# A 429 (RULES: "too early ... wait for it rather than retrying"): wait for the next tick and decide again, so a
# refused accept goes back through the duel arbiter instead of the SDK retrying it blind (wait_on_tick=False).
TICK_WAIT = {"wait_for_tick", "rate_limited", "http_429"}

DEALER = "abuela"
CASH_FLOOR = 200     # overridden by --cash-floor (the GUARDRAIL in intel/directives.md decides it)
EXPECTED_PRICE = 0.92  # dealers end near 0.9x list in the public data (Abuela: common 9 of 10, uncommon 21-24 of 25)
MIN_GAIN = 3         # buy only if our value beats the expected price by this much; never pay above value - MIN_GAIN
PACK_MARGIN = 4      # hard limit: while we hold an unopened pack, pay a dealer at most value - 4
PAGE_SLACK = 0.5     # our value above book x affinity + this: the card carries a page bonus (it completes a page)
GAP_S, DRY_GAP_S = 0.25, 1.0  # seconds between requests, value lookups included (--dry-run: <= 1 GET per second)
FIRST_COUNTER = 0.55  # buy: open at 55% of her first ask; sell: ask her first bid / 0.55
STEP = 0.3           # each counter closes 30% of the gap, at least 1 P
LOG = ROOT / "logs" / "dealers" / f"abuela-{time.strftime('%Y%m%d-%H%M%S')}.jsonl"
STATE = ROOT / "run" / "dealers.json"  # per dealer, across runs: the tick our last conversation closed; a pause
REOPEN_TICKS = 10    # never open a conversation with a dealer sooner than this after the last one closed (Sat 09:47:
                     # a walk on thread 367, then thread 373 with her 5 s later)
SILENT_TICKS = 4     # our word is the last and she hasn't said anything for this many ticks: close, pause her
SILENT_PAUSE_S = 30 * 60

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


class PacedBazaar(Bazaar):
    """The SDK with every request at least `min_gap` seconds after the previous one, so a sweep of value lookups
    never bursts into the team's shared 5 requests per second."""

    def __init__(self, url, key, min_gap=GAP_S, **kw):
        super().__init__(url, key, **kw)
        self.min_gap, self._last = min_gap, None

    def _call(self, *a, **k):
        if self._last is not None:
            wait = self._last + self.min_gap - time.monotonic()
            if wait > 0:
                time.sleep(wait)
        try:
            return super()._call(*a, **k)
        finally:
            self._last = time.monotonic()


def log(event: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    event = {"t": time.strftime("%H:%M:%S"), **event}
    with LOG.open("a") as f:
        f.write(json.dumps(event) + "\n")
    print(json.dumps(event), flush=True)


# ---------------------------------------------------------------------------------------------------- hard limits

def value_of(b, card: str) -> float:
    return float(b.value(card)["your_value"])


def card_index(cat: dict) -> dict:
    return {c["id"]: {"set": s["id"], "book": c["book"], "rarity": c["rarity"], "released": bool(s.get("released"))}
            for s in cat["sets"] for c in s["cards"]}


def packs_held(me: dict) -> int:
    """Unopened packs among our assets (each one drags a trade's score: GAME.md)."""
    return sum(1 for a in me.get("assets", []) if a.get("kind") == "pack")


def page_bonus(value: float, book: float, affinity: float) -> bool:
    """Our value of one more copy above book x affinity: it carries the page bonus (it would complete a page). That
    bonus scores only through a TEAM trade; bought from a dealer it scores <= 0 (GAME.md)."""
    return value > book * affinity + PAGE_SLACK


def hard_cap(value: float, packs: int) -> int:
    """The most we may pay a dealer: our value, or value - 4 while we hold an unopened pack (ORCHESTRATOR.md)."""
    return math.floor(value - (PACK_MARGIN if packs else 0))


def check_buy(b, card: str, cards: dict, me: dict) -> tuple:
    """Fresh value lookup right before a dealer buy (an earlier buy may have made this card a page's last one).
    -> (value, hard cap, None) when we may buy it, (value, None, why not) when we may not."""
    c = cards.get(card)
    aff = (me.get("affinity") or {}).get(c["set"]) if c else None
    if aff is None:
        return None, None, f"unknown card or affinity: {card}"
    v = value_of(b, card)
    if page_bonus(v, c["book"], aff):
        return v, None, f"page bonus: value {v:g} > book {c['book']} x {aff} + {PAGE_SLACK} (team trades only)"
    return v, hard_cap(v, packs_held(me)), None


# ---------------------------------------------------------------------------------------------------- negotiation

def her_price(offer: dict, side: str) -> int:
    """Cash in her offer: what she asks when we buy, what she pays when we sell."""
    want, give = offer.get("want", {}).get("cash", 0), offer.get("give", {}).get("cash", 0)
    return int(want if side == "buy" else give)


class DealerPaused(Exception):
    pass


def _dealers() -> dict:
    try:
        return json.loads(STATE.read_text())
    except (OSError, ValueError):
        return {}


def _note(dealer: str, **fields) -> None:
    st = _dealers()
    st.setdefault(dealer, {}).update(fields)
    STATE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(st))
    tmp.replace(STATE)


def gate(b) -> None:
    """Before a new conversation with DEALER: refuse while she is paused for silence (DealerPaused: the run halts),
    and wait until REOPEN_TICKS have passed since our last conversation with her closed."""
    s = _dealers().get(DEALER, {})
    while True:
        tick = b.clock()["tick"]
        if s.get("paused_until_tick") is not None and tick < s["paused_until_tick"]:
            raise DealerPaused(f"{DEALER} is paused until tick {s['paused_until_tick']} (she went silent)")
        if s.get("closed_tick") is None or tick - s["closed_tick"] >= REOPEN_TICKS:
            return
        log({"event": "reopen_wait", "dealer": DEALER, "closed_tick": s["closed_tick"], "tick": tick})
        b.wait_tick()


def negotiate(b: Bazaar, topic: dict, side: str, cap: int, tid: int = None, fast: bool = False) -> dict:
    """side 'buy': cap = the most we pay. side 'sell': cap = the least we take.
    With `tid`, pick up an open conversation where it stands. An exception closes the conversation (best effort: an
    open one blocks the next run) and returns status "error"; Ctrl-C closes it too, then propagates. A conversation
    where we already accepted is left alone: the deal settles on the next tick and closing could withdraw it."""
    accepted = []
    resume = tid is not None
    try:
        if tid is None:
            gate(b)
            tid = b.open_thread(DEALER, topic=topic)["id"]
        return _haggle(b, tid, topic, side, cap, fast, resume, accepted)
    except BaseException as e:
        log({"event": "error", "thread": tid, "topic": topic, "error": repr(e)[:300]})
        if tid is not None and accepted:
            log({"event": "left_open_after_accept", "thread": tid, "offer": accepted[-1]})
        elif tid is not None:
            try:
                b.close_thread(tid)
                log({"event": "closed_after_error", "thread": tid})
            except Exception as e2:
                log({"event": "close_failed", "thread": tid, "error": repr(e2)[:200]})
        if not isinstance(e, Exception):
            raise
        return {"id": tid, "status": "error", "error": repr(e)[:300]}
    finally:
        if tid is not None:                       # the REOPEN_TICKS gate counts from here
            try:
                _note(DEALER, closed_tick=b.clock()["tick"])
            except Exception as e:
                log({"event": "note_failed", "thread": tid, "error": repr(e)[:200]})


def _haggle(b, tid, topic, side, cap, fast, resume, accepted):
    better = (lambda x, y: x < y) if side == "buy" else (lambda x, y: x > y)  # x better for us than y
    first = ours = None
    turn = 0
    if resume:
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
    heard, quiet = None, 0
    while True:
        t = b.thread(tid)
        if t["status"] != "open":
            log({"event": "end", "thread": tid, "status": t["status"], "reason": t.get("closed_reason"),
                 "her_first": first, "ours_last": ours})
            return t
        msgs = t.get("messages") or []            # one pass of this loop per tick
        n_hers = sum(1 for m in msgs if m.get("sender") == DEALER)
        waiting = not msgs or msgs[-1].get("sender") != DEALER     # our word (or nothing yet) is the last
        quiet = quiet + 1 if waiting and n_hers == heard else 0
        heard = n_hers
        if quiet >= SILENT_TICKS:
            b.close_thread(tid)
            c = b.clock()
            until = c["tick"] + math.ceil(SILENT_PAUSE_S / float(c.get("tick_seconds") or 30))
            _note(DEALER, paused_until_tick=until)
            log({"event": "silent_dealer", "thread": tid, "quiet_ticks": quiet, "paused_until_tick": until})
            return {**t, "status": "closed", "closed_reason": "silent dealer"}
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
            hold, why = should_hold_accept(b)
            if hold:  # a final offer too: a scored duel's accept is worth more than one dealer deal
                log({"event": "hold_accept_duel", "thread": tid, "final": o.get("final"), "why": why})
                b.wait_tick()
                continue
            try:
                b.accept(o["id"])
            except BazaarError as e:
                if e.code not in TICK_WAIT:
                    raise
                log({"event": "accept_waits", "thread": tid, "code": e.code})   # the team's accept is taken
                b.wait_tick()
                continue
            accepted.append(o["id"])
            log({"event": "accept", "thread": tid, "price": price, "negotiated": price != first})
            b.wait_tick()
            continue
        if o.get("final") or nxt == ours:  # final outside our cap, or we can't move without repeating
            b.close_thread(tid)
            log({"event": "walk", "thread": tid, "her": price, "ours": ours, "final": o.get("final")})
            continue
        if ours is not None and msgs and msgs[-1].get("sender") != DEALER:
            log({"event": "hold", "thread": tid, "her": price, "ours": ours})   # she hasn't answered our counter:
            b.wait_tick()                                                       # a new one would bid against us
            continue
        text = TEXTS[side][min(turn, len(TEXTS[side]) - 1)].format(p=nxt)
        try:
            b.say(tid, text, price=nxt)
        except BazaarError as e:
            if e.code not in TICK_WAIT:
                raise
            log({"event": "say_waits", "thread": tid, "code": e.code})
            b.wait_tick()
            continue
        log({"event": "say", "thread": tid, "price": nxt, "text": text})
        ours, turn = nxt, turn + 1
        b.wait_tick()


# ---------------------------------------------------------------------------------------------------- the plan

def plan(b: Bazaar) -> tuple:
    """-> (me, spares to sell, buys as (expected gain, our value, card), spend budget, card index, cards never to buy
    from a dealer as (card, our value): they carry a page bonus)."""
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
    cards = card_index(b.catalog())
    aff = me.get("affinity") or {}
    menu = b.dealer(DEALER).get("menu", {}).get("sells", [])
    list_price = {m["rarity"]: m.get("list_price", 0) for m in menu if "rarity" in m}
    buys, blocked = [], []  # buys: our private value minus the price we expect to pay
    for card, c in cards.items():
        if not c["released"] or c["rarity"] not in list_price:
            continue
        v = value_of(b, card)
        if aff.get(c["set"]) is None or page_bonus(v, c["book"], aff[c["set"]]):
            blocked.append((card, v))  # the page bonus scores only through a team trade
            continue
        gain = v - EXPECTED_PRICE * list_price[c["rarity"]]
        if gain >= MIN_GAIN:
            buys.append((round(gain, 1), v, card))
    buys.sort(reverse=True)
    budget = max(0, me["cash"] - CASH_FLOOR)
    return me, sells, buys, budget, cards, blocked


def main(argv=None) -> None:
    global DEALER, CASH_FLOOR
    ap = argparse.ArgumentParser()
    ap.add_argument("--deals", type=int, default=3, help="stop after this many deals")
    ap.add_argument("--cash-floor", type=int, default=CASH_FLOOR, help="never let cash fall below this (GUARDRAIL)")
    ap.add_argument("--dealer", default="abuela", help="dealer id, as GET /api/dealers lists it")
    ap.add_argument("--max-buy", type=int, default=0, help="optional extra cap per card (0 = our value is the cap)")
    ap.add_argument("--min-sell", type=int, default=3, help="never sell a spare for less than this")
    ap.add_argument("--sell-spares", action="store_true",
                    help="also sell unlisted spares to Abuela (a spare sold to a team at book scores more)")
    ap.add_argument("--resume-cap", type=int, default=0,
                    help="pick up an open Abuela conversation with this cap instead of refusing to start")
    ap.add_argument("--ladder", action="store_true",
                    help="new dealer: N negotiated deals on the cheapest card items of the menu (ladder only; dealer gains score 0)")
    ap.add_argument("--no-buy", action="store_true",
                    help="sell only: a dealer deal never adds neg_points (gains 0, losses in full: GAME.md); buy from teams instead")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, write nothing")
    args = ap.parse_args(argv)
    b = PacedBazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"],
                    min_gap=DRY_GAP_S if args.dry_run else GAP_S, wait_on_tick=False)

    DEALER = args.dealer
    CASH_FLOOR = args.cash_floor
    me, sells, buys, budget, cards, blocked = plan(b)
    packs = packs_held(me)
    clock = b.clock()
    print(f"tick {clock['tick']} ({clock['tick_seconds']}s) · cash {me['cash']} P · spend budget {budget} P · "
          f"accept hold: {should_hold_accept(b, clock['tick'])}")
    print(f"unopened packs held: {packs} → dealer buys capped at {'value − 4' if packs else 'our value'}"
          f" (and value − {MIN_GAIN} by the bot's own margin)")
    print("sell (spares):", [(a["ref"], a["id"], a["your_value"]) for a in sells])
    print(f"dealer {DEALER} · buy (expected gain, our value, card, cap):",
          [(g, v, c, min(int(v - MIN_GAIN), hard_cap(v, packs), budget)) for g, v, c in buys[:8]])
    print(f"dealer {DEALER} · never buy (page bonus, team trades only):", blocked)
    busy = [t for t in b.my_threads()["threads"] if t["with"] == DEALER and t["status"] == "open"]
    if busy:
        print(f"{DEALER} already has an open conversation with us (thread {busy[0]['id']}).")
    if args.dry_run or (busy and not args.resume_cap):
        return

    halted = []  # a negotiation raised: its thread is closed, no new one opens this run

    def score():
        sc = b.me().get("score") or {}
        return {k: sc.get(k) for k in ("negotiating", "neg_points", "ladder_points")}

    def done_one(t, label):
        if t["status"] == "error":
            halted.append(label)
            log({"event": "halt", "deal": label, "error": t.get("error")})
            return False
        before = done_one.last
        after = score()
        log({"event": "score", "deal": label, "status": t["status"], "before": before, "after": after})
        done_one.last = after
        return t["status"] == "deal"
    done_one.last = score()

    def buy_round(limit):
        n = 0
        for gain, value, ref in buys:
            if n >= limit or halted:
                break
            if ref in bought:
                continue
            m = b.me()
            room = max(0, m["cash"] - CASH_FLOOR)
            if room < 1:
                log({"event": "skip_buy", "card": ref, "reason": "cash floor", "cash": m["cash"]})
                break
            v, hard, why = check_buy(b, ref, cards, m)
            bought.add(ref)
            if why:
                log({"event": "skip_buy", "card": ref, "reason": why})
                continue
            cap = min(int(v - MIN_GAIN), hard, room)
            if args.max_buy:
                cap = min(cap, args.max_buy)
            if cap < 1:
                log({"event": "skip_buy", "card": ref, "reason": f"cap {cap}: value {v:g}, packs held {packs_held(m)}"})
                continue
            n += done_one(negotiate(b, {"buy": {"card": ref}}, "buy", cap), f"buy {ref}")
        return n

    def ladder_round(limit):
        """Ladder-only deals (a new dealer: 3 negotiated deals per level count, higher levels weigh more): the
        cheapest card items on the menu, never above 90% of list. A dealer deal never adds neg_points (GAME.md)."""
        menu = b.dealer(DEALER).get("menu", {}).get("sells", [])
        n = 0
        m0 = b.me()
        aff = m0.get("affinity") or {}
        held = {a["ref"] for a in m0["assets"] if a["kind"] == "card"}
        for m in sorted(menu, key=lambda m: m.get("list_price", 0)):
            if "rarity" not in m:
                continue  # packs: their value to us is unknown, and buying above value subtracts (LOG finding 13)
            options = []
            for card, c in cards.items():
                if not c["released"] or c["rarity"] != m["rarity"] or card in held:
                    continue
                v = value_of(b, card)
                if aff.get(c["set"]) is None or page_bonus(v, c["book"], aff[c["set"]]):
                    log({"event": "skip_ladder", "card": card, "reason": f"page bonus: value {v:g} (team trades only)"})
                    continue
                options.append((v, card))
            options.sort(reverse=True)
            while n < limit and options and not halted:
                _, card = options.pop(0)
                me_now = b.me()
                value, hard, why = check_buy(b, card, cards, me_now)  # a deal just made may make it a page's last card
                if why:
                    log({"event": "skip_ladder", "card": card, "reason": why})
                    continue
                cap = min(int(m.get("list_price", 0) * 0.9), int(value) - 1, hard,
                          max(0, me_now["cash"] - CASH_FLOOR))
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
        log({"event": "done", "deals": deals, "cash": b.me()["cash"], "score": score(), "halted": halted})
        return
    if busy:  # pick it up: whoever opened it has stopped
        t0 = busy[0]
        side = "buy" if "buy" in t0["topic"] else "sell"
        cap, why = args.resume_cap, None
        if side == "buy":  # the same hard limits as a fresh buy
            card = (t0["topic"].get("buy") or {}).get("card")
            if card is None:
                why = "not a single card (never a pack)"
            else:
                _, hard, why = check_buy(b, card, cards, b.me())
                cap = min(cap, hard) if hard is not None else cap
                if not why and cap < 1:
                    why = f"cap {cap} below 1 P"
        if why:
            log({"event": "refuse_resume", "thread": t0["id"], "topic": t0["topic"], "reason": why})
            try:
                b.close_thread(t0["id"])
            except BazaarError as e:
                log({"event": "close_failed", "thread": t0["id"], "error": e.code})
        else:
            t = negotiate(b, t0["topic"], side, cap, tid=t0["id"])
            deals += t["status"] == "deal"
            if t["status"] == "error":
                halted.append("resume")
    if not args.no_buy:
        deals += buy_round(args.deals)  # what we can afford now, best expected gain first
    for a in (sells if args.sell_spares else []):  # spares are worth ~1 P to us: cash in, value up
        if deals >= args.deals or halted:
            break
        cap = max(args.min_sell, int(a["your_value"]) + MIN_GAIN)
        deals += done_one(negotiate(b, {"sell": {"assets": [a["id"]]}}, "sell", cap), f"sell {a['ref']}")
    if not args.no_buy:
        deals += buy_round(args.deals - deals)  # the rest, with the cash the sales brought in
    log({"event": "done", "deals": deals, "cash": b.me()["cash"], "score": score(), "halted": halted})


if __name__ == "__main__":
    main()
