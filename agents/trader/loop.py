"""E3 on autopilot: every tick, take the one offer that gains the most value at our private values.

Where offers come from: El Rastro's public board, the public boards of the open team venues, and the offers
addressed `to` us (private: only GET /api/me/offers shows them). Three shapes qualify:
- sell: a team pays cash for a card we hold; gain = cash - fee - what our least valuable copy is worth to us;
- buy:  a team sells card(s) for cash; gain = our value of the card(s) - cash - fee;
- swap: a team gives card(s) for card(s) we hold, no cash; gain = value received - value given - fee.
Anything with a pack, cash on both sides, or a specific asset of ours wanted is skipped.

Fee: the venue's own (fee_bps, fee_per_card; the higher of current and pending), else El Rastro's 5% + 1 P per card.
Bars: --min-gain (buys, swaps), --min-gain-sell (sells). On a venue owned by a top-4 team the bar is at least 15
(its owner scores the value created there); never on a venue we own.

What we never give away (sells and swaps):
- a copy already in one of OUR open offers (GET /api/me/offers; if that read fails, no accept at all that tick);
- the last copy of a card of a set we are building (--build, default RET,CHA) or of LAV, of a page we completed or
  that misses at most --protect-missing cards; a copy whose value carries a page bonus;
- a card to a top-4 team; and to a team that is unknown or less than 10 points below us, nothing at >= 1.5 x book
  (a price like that is likely a page-closer for them). The counterparty: its maker when that is a team id, else
  data/board.json's `team` (when under 2 min old), else the feed's offer.listed actor (data/feed.jsonl, then one
  GET /api/feed per tick at most).
One accept per tick (the team limit), none while a scored duel needs it (tools/arbiter.py), never below the cash floor.
Nothing while the clock is paused or the doors are closed. A refused accept is retried next tick unless the refusal
won't clear by itself (gone, not found, insufficient...). b.value is not asked for a card whose most possible value
can't clear the bar.

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
import policy  # noqa: E402

LOG = ROOT / "logs" / "trader.jsonl"
BOARD = ROOT / "data" / "board.json"   # the collector's copy of El Rastro's board, each offer tagged with its `team`
FEED = ROOT / "data" / "feed.jsonl"    # the collector's copy of the public feed
HOUSE = "rastro"
HOUSE_FEE = (500, 1)  # El Rastro: 5% + 1 P per card
RARITY_BOOK = {"common": 10, "uncommon": 25, "rare": 70, "epic": 180, "legendary": 450}
PAGE_RARITIES = ("common", "uncommon", "rare")  # a page = the commons, uncommons and rares of a set
KEEP_SETS = {"LAV"}  # never give the last copy of a card of these sets (on top of --build)
LEADER_BAR = 15     # minimum gain on a venue owned by a top-4 team
REFRESH_TICKS = 10  # venues and leaderboard are re-read this often
BOARD_FRESH = 120   # seconds: an older data/board.json is not trusted
FEED_GAP = policy.PAGE_CLOSER_GAP   # board points: a team at least this far below us may get a page-closer (16:20: 6)
ASK_LEFT = 3        # our own live ask for a card wins over a worse accept unless it expires within this many ticks
CLOSER_X = 1.5      # a price at or above this many times book is treated as a likely page-closer
CLOSED_SLEEP = 30   # seconds between clock checks while paused or closed
ERROR_SLEEP = 5     # seconds after an unexpected error
TERMINAL = {"cancelled", "canceled", "expired", "settled", "filled", "closed", "done", "withdrawn", "rejected"}
TRANSIENT = {"wait_for_tick", "rate_limited", "network", "bad_response", "too_many_failures", "http_429"}
CONTENTION = {"wait_for_tick", "rate_limited", "http_429"}  # always retried; other transient ones MAX_RETRIES times
MAX_RETRIES = 3


def log(event):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    event = {"t": time.strftime("%H:%M:%S"), **event}
    with LOG.open("a") as f:
        f.write(json.dumps(event) + "\n")
    print(json.dumps(event), flush=True)


def fee(price, cards, bps=HOUSE_FEE[0], per_card=HOUSE_FEE[1]):
    return -(-int(price) * int(bps) // 10000) + int(per_card) * cards  # ceil(price * bps / 10000) + per card


def transient(code):
    """A refusal that clears by itself (rate, the per-tick accept limit, the network, a server error)."""
    return code in TRANSIENT or str(code).startswith("http_5")


class State:
    def __init__(self):
        self.values, self.tried, self.retries = {}, set(), {}
        self.venues, self.top4, self.own_venues, self.scores = {}, set(), set(), {}
        self.venues_tick = self.lb_tick = None
        self.locked, self.offers_ok = set(), True        # asset ids in our open offers; did my_offers read this tick
        self.own_asks = {}                               # ref -> [(offer, cash, expires_tick)]: our live asks
        self.bid_cash = 0                                # cash in our open bids (the book's CHA bids): kept above the floor
        self.board_teams, self.listed = {}, {}           # offer id -> team: board.json (fresh), feed offer.listed
        self.feed_pos, self.live_feed_tick = 0, "never"
        self.tick, self.closed = None, False


def refresh(b, st, me, tick):
    """Venues (owner, fees) and the leaderboard, at most once per REFRESH_TICKS ticks; on a failed read keep the last."""
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
            st.scores = {t["team"]: t.get("score") for t in teams if t.get("team")}
            st.lb_tick = tick
        except BazaarError as e:
            log({"event": "error", "where": "leaderboard", "code": e.code})


def gather(b, me_id, st):
    """Open offers we could take: addressed to us, then every open public board but our own venue's.
    Also sets st.locked (asset ids in our own open offers) and st.offers_ok (False: my_offers failed this tick)."""
    own, found, locked, bid_cash, asks = set(), [], set(), 0, {}
    try:
        for o in b.my_offers().get("offers") or []:
            if o.get("maker") == me_id:
                own.add(o["id"])
                if o.get("status", "open") not in TERMINAL:
                    give = (o.get("give") or {}).get("assets") or []
                    locked |= {a["id"] for a in give if "id" in a}
                    bid_cash += (o.get("give") or {}).get("cash") or 0
                    if len(give) == 1 and (o.get("want") or {}).get("cash") and give[0].get("ref"):
                        asks.setdefault(give[0]["ref"], []).append((o["id"], o["want"]["cash"], o.get("expires_tick")))
            elif o.get("to") == me_id:
                found.append(o)
        st.locked, st.offers_ok, st.bid_cash, st.own_asks = locked, True, bid_cash, asks
    except BazaarError as e:
        st.locked, st.offers_ok = set(), False
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


# ------------------------------------------------------------------ who is behind an offer

def read_board_teams(st, now=None):
    """offer id -> team from data/board.json, only when it is under BOARD_FRESH seconds old."""
    st.board_teams = {}
    try:
        d = json.loads(BOARD.read_text())
        if (now or time.time()) - float(d.get("t") or 0) < BOARD_FRESH:
            st.board_teams = {o["id"]: o["team"] for o in d.get("offers") or [] if o.get("team") not in (None, "?")}
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        pass  # missing, stale or half-written: the feed answers instead


def _note_listed(st, e):
    try:
        if e.get("type") == "offer.listed":
            oid = ((e.get("payload") or {}).get("offer") or {}).get("id")
            if oid is not None and e.get("actor"):
                st.listed[oid] = e["actor"]
    except (AttributeError, TypeError):
        pass  # an event of another shape: ignore it


def read_local_feed(st):
    """New offer.listed events in data/feed.jsonl since the last read (complete lines only)."""
    try:
        with FEED.open("rb") as f:
            f.seek(0, 2)
            if f.tell() < st.feed_pos:
                st.feed_pos = 0  # rewritten: read it again
            f.seek(st.feed_pos)
            chunk = f.read()
    except OSError:
        return
    end = chunk.rfind(b"\n") + 1
    for line in chunk[:end].splitlines():
        if b'"offer.listed"' in line:
            try:
                _note_listed(st, json.loads(line))
            except ValueError:  # includes a bad UTF-8 or JSON line
                pass
    st.feed_pos += end


def bidder(b, o, st):
    """The team behind an offer, or None if nobody can tell."""
    if o.get("maker") in st.scores:
        return o["maker"]  # addressed offers may carry the real team id
    oid = o["id"]
    if oid in st.board_teams:
        return st.board_teams[oid]
    if oid not in st.listed and st.live_feed_tick != st.tick:
        st.live_feed_tick = st.tick  # one live read per tick at most
        try:
            for e in b.feed(limit=1000).get("events") or []:
                _note_listed(st, e)
        except BazaarError as e:
            log({"event": "error", "where": "feed", "code": e.code})
    return st.listed.get(oid)


def feeding_skip(b, o, me, st, price, book):
    """Why giving these cards to this offer's maker would feed a rival ("" = fine), and who the maker is."""
    team = bidder(b, o, st)
    if not st.scores:
        return "leaderboard unknown: no sales or swaps", team
    teams = [{"team": t, "score": s} for t, s in st.scores.items()]
    ok, why = policy.check(team, teams=teams, page_closer=False)     # their gain unknown: top 5 and rivals skip
    if not ok:
        return why, team
    ours = st.scores.get(me["id"])
    if ours is None:
        ours = (me.get("score") or {}).get("score") if isinstance(me.get("score"), dict) else None
    theirs = st.scores.get(team)
    near = team is None or ours is None or theirs is None or theirs > ours - FEED_GAP
    if near and price >= CLOSER_X * book:
        who = "an unknown team" if team is None else f"{team} ({theirs} vs our {ours})"
        return f"{price} >= {CLOSER_X} x book {book} to {who}: likely a page-closer", team
    return "", team


# ------------------------------------------------------------------ cards

def wanted_cards(want):
    """Card refs an offer wants (any copy), or None if it wants a non-card type (a pack)."""
    refs = list(want.get("cards") or [])
    for t in want.get("types") or []:
        if not t.startswith("card:"):
            return None
        refs.append(t.split(":", 1)[1])
    return refs


def pick_copies(refs, held, me, protect_missing, keep_sets=frozenset(KEEP_SETS)):
    """(asset ids we hand over, their value to us, why not). Gives our least valuable free copy of each card.
    `held` must already leave out the copies in our open offers."""
    if len(set(refs)) != len(refs):
        return None, 0.0, "wants two copies of one card"
    pages = {p["set"]: p for p in (me.get("album") or {}).get("pages") or []}
    aff = me.get("affinity") or {}
    ids, loss = [], 0.0
    for r in refs:
        copies = held.get(r)
        if not copies:
            return None, 0.0, f"no free {r} (none held, or all in our open offers)"
        c = min(copies, key=lambda a: a["your_value"])
        s = c.get("set") or r.split("-")[0]
        base = RARITY_BOOK.get(c.get("rarity"), 0) * aff.get(s, 1.0)
        if c["your_value"] > base + 0.5:
            return None, 0.0, f"{r} carries a page bonus ({c['your_value']} > book x m {base:g})"
        if len(copies) == 1 and s in keep_sets:
            return None, 0.0, f"last free {r}: set {s} is kept (--build / LAV)"
        p = pages.get(s)
        if len(copies) == 1 and c.get("rarity") in PAGE_RARITIES and p and \
                (p.get("complete") or p["of"] - p["have"] <= protect_missing):
            return None, 0.0, f"last {r} of page {s} ({p['have']}/{p['of']})"
        ids.append(c["id"])
        loss += c["your_value"]
    return ids, loss, ""


def value_bound(assets, me, st):
    """The most these cards can be worth to us, without asking b.value; None if only b.value can tell (an epic or
    legendary, an unknown rarity, or the last missing card of one of our pages, whose value carries the page bonus).
    One more copy is worth book x m, a 2nd 25%, a 3rd 10% (GAME.md); unopened packs only lower it."""
    aff = me.get("affinity") or {}
    pages = {p["set"]: p for p in (me.get("album") or {}).get("pages") or []}
    owned = {}
    for a in me.get("assets") or []:
        owned[a.get("ref")] = owned.get(a.get("ref"), 0) + 1
    total, done = 0.0, set()
    for a in assets:
        r = a["ref"]
        if r in done:
            continue
        done.add(r)
        if r in st.values:
            total += st.values[r]
            continue
        rar, s = a.get("rarity"), a.get("set") or r.split("-")[0]
        if rar not in PAGE_RARITIES:
            return None
        n, p = owned.get(r, 0), pages.get(s)
        if n == 0 and p and not p.get("complete") and p["of"] - p["have"] == 1:
            return None
        m = aff.get(s, max(aff.values(), default=2.0))
        total += RARITY_BOOK[rar] * m * (1.0 if n == 0 else 0.25 if n == 1 else 0.1)
    return total + 0.5


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
         "to_us": o.get("to") == me["id"], "ok": False, "skip": "", "bidder": None}
    got = [a["ref"] for a in gassets]
    c["what"] = {"sell": f"sell {refs} for {gcash}", "buy": f"buy {got} for {wcash}", "swap": f"swap {got} for {refs}"}[kind]
    loss = 0.0
    if kind in ("sell", "swap"):
        ids, loss, why = pick_copies(refs, held, me, args.protect_missing, KEEP_SETS | set(args.build))
        if ids is None:
            c.update(skip=why, gain=None)
            return c
        c["assets"] = ids
        if kind == "swap" and set(got) & set(refs):
            c.update(skip="same card on both sides", gain=None)
            return c
    if kind == "sell":
        c["gain"] = gcash - fee(gcash, len(refs), bps, per_card) - loss
    else:
        cost = wcash + fee(wcash, len(gassets) + (len(refs) if kind == "swap" else 0), bps, per_card)
        # [Uncertain] a swap's per-card fee counted on both legs
        if me["cash"] - st.bid_cash - cost < args.cash_floor:
            c["skip"] = f"cash floor ({me['cash']} - {st.bid_cash} in our bids - {cost} < {args.cash_floor})"
        if venue in st.own_venues or owner == me["id"]:
            c["skip"] = "our own venue"
        bound = value_bound(gassets, me, st)
        if c["skip"] or (bound is not None and bound - cost - loss < bar):
            c.update(skip=c["skip"] or f"can't clear the bar: worth at most {bound:.1f} to us", gain=None)
            return c  # no b.value lookup for an offer that can't pass
        c["gain"] = received_value(b, gassets, st) - cost - loss
    if venue in st.own_venues or owner == me["id"]:
        c["skip"] = "our own venue"
    c["gain"] = round(c["gain"], 2)
    c["ok"] = not c["skip"] and c["gain"] >= bar
    if c["ok"] and kind in ("sell", "swap"):  # Chief 16:30: our own live ask for this card may be worth more
        for r in refs:
            for oid, cash, exp in st.own_asks.get(r, []):
                left = None if exp is None or st.tick is None else exp - st.tick
                if cash - loss / max(len(refs), 1) > c["gain"] and (left is None or left > ASK_LEFT):
                    c.update(skip=f"our live ask {oid} sells {r} at {cash}: better than +{c['gain']:g}", ok=False)
    if c["ok"] and kind in ("sell", "swap"):  # who gets our card(s); only for offers that pass, it may cost a GET
        price = gcash if kind == "sell" else sum(RARITY_BOOK.get(a.get("rarity"), 0) for a in gassets)
        book = sum(RARITY_BOOK.get((held[r][0] or {}).get("rarity"), 0) for r in refs)
        why, c["bidder"] = feeding_skip(b, o, me, st, price, book)
        if why:
            c.update(skip=why, ok=False)
    elif c["ok"] and kind == "buy":           # policy (16:20): never the top 5 nor a rival, their gain unknown
        team = bidder(b, o, st)
        ok, why = policy.check(team, teams=[{"team": t, "score": s} for t, s in st.scores.items()])
        c["bidder"] = team
        if not ok:
            c.update(skip=why, ok=False)
    return c


def step(b, args, st):
    """One tick: read, evaluate, accept the best candidate (or log it, in --dry-run). Returns the best candidate."""
    me = b.me()
    tick = st.tick = me.get("tick")
    holdings = (me["cash"], tuple(sorted(a["id"] for a in me["assets"])))
    if st.values.get("_holdings") != holdings:
        st.values = {"_holdings": holdings}  # any card in or out (a 1-for-1 swap too): values changed
    refresh(b, st, me, tick)
    offers = gather(b, me["id"], st)
    held = {}  # our cards, minus the copies already promised in our own open offers
    for a in me["assets"]:
        if a["kind"] == "card" and a["id"] not in st.locked:
            held.setdefault(a["ref"], []).append(a)
    read_board_teams(st)
    read_local_feed(st)
    cands = []
    if not st.offers_ok:
        log({"event": "skip_tick", "tick": tick, "why": "my_offers unreadable: can't tell our offers and copies"})
        offers = []
    for o in offers:
        try:
            c = evaluate(b, o, me, held, st, args)
        except Exception as e:  # e.g. b.value refused for one card, an odd shape: skip that offer, not the tick
            log({"event": "error", "where": f"offer {o.get('id')}", "code": getattr(e, "code", type(e).__name__)})
            continue
        if c:
            cands.append(c)
    ok = sorted((c for c in cands if c["ok"]), key=lambda c: -c["gain"])
    best = ok[0] if ok else None
    hold, why = should_hold_accept(b, tick) if best else (False, "")
    if args.dry_run:
        top = sorted(cands, key=lambda c: -(c["gain"] if c["gain"] is not None else -1e9))[:args.show]
        log({"event": "dry_run", "tick": tick, "offers_seen": len(offers), "candidates": len(cands),
             "locked": sorted(st.locked), "top4": sorted(st.top4), "venues": {v: x["owner"] for v, x in st.venues.items()},
             "would_accept": best and {k: best[k] for k in ("offer", "what", "gain", "venue", "owner", "bar", "bidder")},
             "arbiter_hold": hold, "arbiter_why": why})
        for c in top:
            log({"event": "candidate", **{k: c.get(k) for k in ("offer", "kind", "what", "gain", "bar", "ok", "skip",
                                                                 "venue", "owner", "bidder", "to_us")}})
        return best
    if hold:
        log({"event": "hold_accept", "offer": best["offer"], "what": best["what"], "why": why})
    elif best:
        info = {"offer": best["offer"], "what": best["what"], "venue": best["venue"], "owner": best["owner"],
                "bidder": best["bidder"], "to_us": best["to_us"]}
        try:
            b.accept(best["offer"], assets=best["assets"])
            st.tried.add(best["offer"])
            log({"event": "accept", **info, "expected_gain": round(best["gain"], 1)})
        except BazaarError as e:
            n = st.retries[best["offer"]] = st.retries.get(best["offer"], 0) + 1
            retry = transient(e.code) and (e.code in CONTENTION or n < MAX_RETRIES)
            if not retry:
                st.tried.add(best["offer"])  # gone, not found, insufficient, or failing again and again
            log({"event": "refused", **info, "code": e.code, "retry": retry})
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
    ap.add_argument("--build", type=lambda s: [x.strip().upper() for x in s.split(",") if x.strip()],
                    default="RET,CHA", help="sets whose pages we are building: never give the last copy of their cards")
    ap.add_argument("--dry-run", action="store_true", help="compute and log candidates, never accept")
    ap.add_argument("--once", action="store_true", help="one iteration, then exit")
    ap.add_argument("--show", type=int, default=12, help="--dry-run: how many candidates to log")
    ap.add_argument("--pace", type=float, default=0.3, help="seconds between this process's requests")
    return ap.parse_args(argv)


def is_closed(clock):
    return bool(clock.get("paused")) or clock.get("doors", "open") != "open"


def main(argv=None):
    global LOG
    args = parse_args(argv)
    if args.dry_run:
        LOG = ROOT / "logs" / "trader-dry.jsonl"
    # wait_on_tick=False: a refused accept is not silently retried next tick, past the arbiter
    b = pace(Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"],
                    wait_on_tick=False), args.pace)
    st, clock = State(), None
    while True:
        try:
            clock = b.clock() if clock is None else b.wait_tick()
            if is_closed(clock):
                if args.dry_run and args.once:  # a one-shot look is harmless: evaluate anyway, never accept
                    log({"event": "clock", "note": "paused or doors closed; --dry-run --once evaluates anyway",
                         "tick": clock.get("tick"), "paused": clock.get("paused"), "doors": clock.get("doors")})
                else:
                    if not st.closed:
                        log({"event": "closed", "tick": clock.get("tick"), "paused": clock.get("paused"),
                             "doors": clock.get("doors"), "next_opens": clock.get("next_opens")})
                    st.closed = True
                    if args.once:
                        return
                    time.sleep(CLOSED_SLEEP)
                    continue
            elif st.closed:
                st.closed = False
                log({"event": "open", "tick": clock.get("tick")})
            step(b, args, st)
        except Exception as e:  # never die, never spin: log, pause, and go back to waiting for the tick
            log({"event": "error", "where": "loop", "code": getattr(e, "code", type(e).__name__),
                 "message": str(getattr(e, "message", "") or e)[:150]})
            if args.once:
                return
            time.sleep(ERROR_SLEEP)
        if args.once:
            return


if __name__ == "__main__":
    main()
