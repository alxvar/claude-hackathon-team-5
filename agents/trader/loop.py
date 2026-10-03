"""E3 on autopilot: every tick, take the one offer that gains the most value at our private values.

Where offers come from: El Rastro's public board, the public boards of the open team venues, and the offers
addressed `to` us (private: only GET /api/me/offers shows them). Three shapes qualify:
- sell: a team pays cash for a card we hold; gain = cash - fee - what our least valuable copy is worth to us;
- buy:  a team sells card(s) for cash; gain = our value of the card(s) - cash - fee;
- swap: a team gives card(s) for card(s) we hold, no cash; gain = value received - value given - fee.
Anything with a pack, cash on both sides, or a specific asset of ours wanted is skipped.

Fee: the venue's own (fee_bps, fee_per_card; the higher of current and pending), else El Rastro's 5% + 1 P per card.
Bars: --min-gain (buys, swaps), --min-gain-sell (sells). On a venue owned by a top-4 team the bar is at least 15
(its owner scores the value created there); never on a venue we own. Never the last copy of a card in a page we have
completed or are building, never a copy whose value carries a page bonus. One accept per tick (the team limit), none
while a scored duel needs it (tools/arbiter.py), never below the cash floor.

    source .env && python3 -u agents/trader/loop.py --min-gain 3
    source .env && python3 -u agents/trader/loop.py --dry-run --once     # log candidates, never accept
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
sys.path.insert(0, str(ROOT / "tools"))
from bazaar_sdk import Bazaar, BazaarError  # noqa: E402
from arbiter import should_hold_accept  # noqa: E402

LOG = ROOT / "logs" / "trader.jsonl"
HOUSE = "rastro"
HOUSE_FEE = (500, 1)  # El Rastro: 5% + 1 P per card
RARITY_BOOK = {"common": 10, "uncommon": 25, "rare": 70, "epic": 180, "legendary": 450}
PAGE_RARITIES = ("common", "uncommon", "rare")  # a page = the commons, uncommons and rares of a set
LEADER_BAR = 15     # minimum gain on a venue owned by a top-4 team
REFRESH_TICKS = 10  # venues and leaderboard are re-read this often


def log(event):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    event = {"t": time.strftime("%H:%M:%S"), **event}
    with LOG.open("a") as f:
        f.write(json.dumps(event) + "\n")
    print(json.dumps(event), flush=True)


def fee(price, cards, bps=HOUSE_FEE[0], per_card=HOUSE_FEE[1]):
    return -(-int(price) * int(bps) // 10000) + int(per_card) * cards  # ceil(price * bps / 10000) + per card


class State:
    def __init__(self):
        self.values, self.tried = {}, set()
        self.venues, self.top4, self.own_venues = {}, set(), set()
        self.venues_tick = self.lb_tick = None


def refresh(b, st, me, tick):
    """Venues (owner, fees) and the top 4, at most once per REFRESH_TICKS ticks; on a failed read keep the last ones."""
    due = lambda last: last is None or tick is None or tick - last >= REFRESH_TICKS  # noqa: E731
    if due(st.venues_tick):
        try:
            vs = {}
            for v in b.venues().get("venues") or []:
                p = v.get("pending_fee") or {}
                vs[v["venue"]] = {"owner": v.get("owner"), "status": v.get("status"), "house": v.get("house"),
                                  "fee_bps": max(v.get("fee_bps") or 0, p.get("fee_bps") or 0),
                                  "fee_per_card": max(v.get("fee_per_card") or 0, p.get("fee_per_card") or 0)}
            st.venues, st.venues_tick = vs, tick
        except BazaarError as e:
            log({"event": "error", "where": "venues", "code": e.code})
    mine = me.get("venue")
    st.own_venues = {v for v, x in st.venues.items() if x["owner"] == me["id"]}
    if mine:
        st.own_venues.add(mine.get("venue") if isinstance(mine, dict) else mine)
    if due(st.lb_tick):
        try:
            teams = b.leaderboard().get("teams") or []
            if all(t.get("rank") for t in teams):
                st.top4 = {t["team"] for t in teams if t["rank"] <= 4}
            else:
                st.top4 = {t["team"] for t in sorted(teams, key=lambda t: -(t.get("score") or 0))[:4]}
            st.lb_tick = tick
        except BazaarError as e:
            log({"event": "error", "where": "leaderboard", "code": e.code})


def gather(b, me_id, st):
    """Open offers we could take: addressed to us, then every open public board but our own venue's."""
    own, found = set(), []
    try:
        for o in b.my_offers().get("offers") or []:
            if o.get("maker") == me_id:
                own.add(o["id"])
            elif o.get("to") == me_id:
                found.append(o)
    except BazaarError as e:
        log({"event": "error", "where": "my_offers", "code": e.code})
    boards = [HOUSE] + sorted(v for v, x in st.venues.items()
                              if v != HOUSE and x["status"] == "open" and v not in st.own_venues)
    for v in boards:
        try:
            for o in b.board(v).get("offers") or []:
                o.setdefault("venue", v)
                found.append(o)
        except BazaarError as e:
            log({"event": "error", "where": f"board {v}", "code": e.code})
    out, seen = [], set()
    for o in found:  # board makers are pseudonyms: our own offers are known by id from my_offers
        if o["id"] in seen or o["id"] in own or o["id"] in st.tried or o.get("maker") == me_id:
            continue
        if o.get("status", "open") != "open" or o.get("to") not in (None, me_id):
            continue
        seen.add(o["id"])
        out.append(o)
    return out


def wanted_cards(want):
    """Card refs an offer wants (any copy), or None if it wants a non-card type (a pack)."""
    refs = list(want.get("cards") or [])
    for t in want.get("types") or []:
        if not t.startswith("card:"):
            return None
        refs.append(t.split(":", 1)[1])
    return refs


def pick_copies(refs, held, me, protect_missing):
    """(asset ids we hand over, their value to us, why not). Gives our least valuable copy of each card."""
    if len(set(refs)) != len(refs):
        return None, 0.0, "wants two copies of one card"
    pages = {p["set"]: p for p in (me.get("album") or {}).get("pages") or []}
    aff = me.get("affinity") or {}
    ids, loss = [], 0.0
    for r in refs:
        copies = held.get(r)
        if not copies:
            return None, 0.0, f"we hold no {r}"
        c = min(copies, key=lambda a: a["your_value"])
        s = c.get("set") or r.split("-")[0]
        base = RARITY_BOOK.get(c.get("rarity"), 0) * aff.get(s, 1.0)
        if c["your_value"] > base + 0.5:
            return None, 0.0, f"{r} carries a page bonus ({c['your_value']} > book x m {base:g})"
        p = pages.get(s)
        if len(copies) == 1 and c.get("rarity") in PAGE_RARITIES and p and \
                (p.get("complete") or p["of"] - p["have"] <= protect_missing):
            return None, 0.0, f"last {r} of page {s} ({p['have']}/{p['of']})"
        ids.append(c["id"])
        loss += c["your_value"]
    return ids, loss, ""


def received_value(b, assets, st):
    """Our value of the cards we'd receive (b.value, cached). A repeated card counts once (conservative)."""
    total = 0.0
    for r in {a["ref"] for a in assets}:
        if r not in st.values:
            st.values[r] = b.value(r)["your_value"]
        total += st.values[r]
    return total


def evaluate(b, o, me, held, st, args):
    """A candidate dict for one offer, or None if its shape isn't one we trade. `ok` = it clears every rule."""
    g, w = o.get("give") or {}, o.get("want") or {}
    gcash, wcash, gassets = g.get("cash") or 0, w.get("cash") or 0, g.get("assets") or []
    refs = wanted_cards(w)
    if refs is None or any(a.get("kind") != "card" for a in gassets) or g.get("types") or w.get("assets"):
        return None  # packs, or a specific asset of ours wanted
    if gcash and not gassets and refs and not wcash:
        kind = "sell"
    elif gassets and not gcash and wcash and not refs:
        kind = "buy"
    elif gassets and not gcash and refs and not wcash:
        kind = "swap"
    else:
        return None
    venue = o.get("venue") or HOUSE
    vinfo = st.venues.get(venue)
    owner = vinfo["owner"] if vinfo else ("world" if venue == HOUSE else "?")
    bps, per_card = (vinfo["fee_bps"], vinfo["fee_per_card"]) if vinfo else HOUSE_FEE
    if not vinfo and venue != HOUSE:
        st.venues_tick = None  # a venue we haven't seen: re-read the list next tick
    bar = args.min_gain_sell if kind == "sell" else args.min_gain
    if owner in st.top4 or owner == "?":
        bar = max(bar, LEADER_BAR)
    c = {"offer": o["id"], "kind": kind, "venue": venue, "owner": owner, "bar": bar, "assets": None,
         "to_us": o.get("to") == me["id"], "ok": False, "skip": ""}
    if kind in ("sell", "swap"):
        ids, loss, why = pick_copies(refs, held, me, args.protect_missing)
        if ids is None:
            c.update(skip=why, what=f"{kind} {refs}", gain=None)
            return c
        c["assets"] = ids
    if kind == "sell":
        c["gain"] = gcash - fee(gcash, len(refs), bps, per_card) - loss
        c["what"] = f"sell {refs} for {gcash}"
    elif kind == "buy":
        cost = wcash + fee(wcash, len(gassets), bps, per_card)
        c["gain"] = received_value(b, gassets, st) - cost
        c["what"] = f"buy {[a['ref'] for a in gassets]} for {wcash}"
        if me["cash"] - cost < args.cash_floor:
            c["skip"] = f"cash floor ({me['cash']} - {cost} < {args.cash_floor})"
    else:
        got = [a["ref"] for a in gassets]
        if set(got) & set(refs):
            c.update(skip="same card on both sides", what=f"swap {got} for {refs}", gain=None)
            return c
        f = fee(0, len(gassets) + len(refs), bps, per_card)  # [Uncertain] per-card fee counted on both legs
        c["gain"] = received_value(b, gassets, st) - loss - f
        c["what"] = f"swap {got} for {refs}"
        if me["cash"] - f < args.cash_floor:
            c["skip"] = f"cash floor ({me['cash']} - fee {f} < {args.cash_floor})"
    if venue in st.own_venues or owner == me["id"]:
        c["skip"] = "our own venue"
    c["gain"] = round(c["gain"], 2)
    c["ok"] = not c["skip"] and c["gain"] >= bar
    return c


def step(b, args, st):
    """One tick: read, evaluate, accept the best candidate (or log it, in --dry-run). Returns the best candidate."""
    me = b.me()
    tick = me.get("tick")
    held = {}
    for a in me["assets"]:
        if a["kind"] == "card":
            held.setdefault(a["ref"], []).append(a)
    if st.values.get("_cash") != me["cash"] or st.values.get("_n") != len(me["assets"]):
        st.values = {"_cash": me["cash"], "_n": len(me["assets"])}  # holdings changed: values changed too
    refresh(b, st, me, tick)
    offers = gather(b, me["id"], st)
    cands = []
    for o in offers:
        try:
            c = evaluate(b, o, me, held, st, args)
        except BazaarError as e:  # e.g. b.value refused for one card: skip that offer, not the tick
            log({"event": "error", "where": f"offer {o.get('id')}", "code": e.code})
            continue
        if c:
            cands.append(c)
    ok = sorted((c for c in cands if c["ok"]), key=lambda c: -c["gain"])
    best = ok[0] if ok else None
    hold, why = should_hold_accept(b, tick) if best else (False, "")
    if args.dry_run:
        top = sorted(cands, key=lambda c: -(c["gain"] if c["gain"] is not None else -1e9))[:args.show]
        log({"event": "dry_run", "tick": tick, "offers_seen": len(offers), "candidates": len(cands),
             "top4": sorted(st.top4), "venues": {v: x["owner"] for v, x in st.venues.items()},
             "would_accept": best and {k: best[k] for k in ("offer", "what", "gain", "venue", "owner", "bar")},
             "arbiter_hold": hold, "arbiter_why": why})
        for c in top:
            log({"event": "candidate", **{k: c.get(k) for k in
                                          ("offer", "kind", "what", "gain", "bar", "ok", "skip", "venue", "owner", "to_us")}})
        return best
    if hold:
        log({"event": "hold_accept", "offer": best["offer"], "what": best["what"], "why": why})
    elif best:
        st.tried.add(best["offer"])
        info = {"offer": best["offer"], "what": best["what"], "venue": best["venue"], "owner": best["owner"],
                "to_us": best["to_us"]}
        try:
            b.accept(best["offer"], assets=best["assets"])
            log({"event": "accept", **info, "expected_gain": round(best["gain"], 1)})
        except BazaarError as e:
            log({"event": "refused", **info, "code": e.code})
    return best


def pace(b, gap):
    """At most one request every `gap` seconds from this process (the team's 5 req/s is shared)."""
    call, last = b._call, [0.0]

    def paced(*a, **k):
        wait = last[0] + gap - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        try:
            return call(*a, **k)
        finally:
            last[0] = time.monotonic()

    b._call = paced
    return b


def parse_args(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-gain", type=float, default=3.0, help="buys and swaps: our value gained, fee included")
    ap.add_argument("--min-gain-sell", type=float, default=6.0,
                    help="sells into bids: higher bar, every sale also scores for the buyer (LOG finding 7)")
    ap.add_argument("--cash-floor", type=int, default=200)
    ap.add_argument("--protect-missing", type=int, default=2,
                    help="never give the last copy of a card whose page misses at most this many cards (or is complete)")
    ap.add_argument("--dry-run", action="store_true", help="compute and log candidates, never accept")
    ap.add_argument("--once", action="store_true", help="one iteration, then exit")
    ap.add_argument("--show", type=int, default=12, help="--dry-run: how many candidates to log")
    ap.add_argument("--pace", type=float, default=0.3, help="seconds between this process's requests")
    return ap.parse_args(argv)


def main(argv=None):
    global LOG
    args = parse_args(argv)
    if args.dry_run:
        LOG = ROOT / "logs" / "trader-dry.jsonl"
    b = pace(Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"]), args.pace)
    st = State()
    while True:
        try:
            step(b, args, st)
        except BazaarError as e:
            log({"event": "error", "code": e.code, "message": e.message[:150]})
        if args.once:
            return
        b.wait_tick()


if __name__ == "__main__":
    main()
