"""Page-gap engine behind Dani's alerts (plan §6b): who lacks / holds which card, crossed with our spares and our pages.

    source .env && python3 tools/opportunities.py --once --dry-run     # compute and print; posts nothing, notifies nobody
    source .env && python3 -u tools/opportunities.py --every 30        # daemon: post the offer, THEN alert Dani + Lucas

Signals (public): a team that BIDS for card X (offer.listed / live board) or opens a dealer thread to BUY X lacks X; a
team that LISTS X, receives X in a settlement, pulls X as a pack's `best`, gets X as a gift or offers X to a dealer
holds X. The latest signal per (team, card) wins; a live board offer counts as "now". Leaderboard: score, rank.
Our side (team key, GET only): /api/me holdings with per-copy your_value, /api/me/value?card= for cards we miss.

SELL: team T lacks X, we hold a spare copy (never the only copy of a card in a page we build or completed),
T ≤ our score − 10 and outside the top 4. Price: 40 common / 45 uncommon / 95 rare, lowered for cheap buyers to half
of what a last card is worth to them ((book + page bonus) × m, m = the best price/book T paid or bid in that set),
raised to T's live bid, never below our copy value + 3. Gain = price − copy value.
BUY: team H (outside the top 4) holds X that a page we build misses. Bid = H's live ask or book, never above
value − 3 (they accept our bid, so no fee for us). Gain = value − price, capped at 50. Non-collectors rank first.

Alert only if gain ≥ 20 or it completes our page, the signal is ≤ 30 game minutes old, ≤ 3 Dani alerts per hour,
45 min per team, 2 h per (team, card); a SELL also needs the buyer to lack ≤ 1 other card of that set (seen in the last
2 game hours), i.e. ours is its last or second-to-last card (plan §4A): otherwise a 40 P ask won't fill. Everything goes to intel/opportunities.md with its status.
Execution (not --dry-run): post the addressed offer (expires after ~20 min), record its id, THEN notify. At most 3
live opportunity offers, cancelled after 20 min unfilled; cash floor env CASH_FLOOR (default 200).

Reads: public keyless routes (clock, feed, El Rastro's board, leaderboard, catalog), data/feed.jsonl + data/board.json
from the collector when fresh (< 2 min); the team key only for /api/me, /api/me/value (and /api/me/offers when live).
Every request is paced to ≤ 1 per second.
"""
import argparse
import bisect
import json
import math
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
sys.path.insert(0, str(ROOT / "tools"))
from bazaar_sdk import Bazaar, BazaarError, _Http  # noqa: E402
from notify import notify  # noqa: E402

DATA, STATE, OUT = ROOT / "data", ROOT / "run" / "opportunities_state.json", ROOT / "intel" / "opportunities.md"
URL = os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai")

FRESH_S = 120              # collector files younger than this are used instead of fetching
CONF_H = 0.5               # a signal older than 30 game minutes is low confidence: listed, never alerted
MIN_GAIN, GAIN_CAP = 20, 50
SCORE_GAP, TOP_N = 10, 4   # feeding rule: sell only to teams ≥ 10 below us and outside the top 4
ALERTS_PER_H, TEAM_COOLDOWN_S, PAIR_COOLDOWN_S = 3, 45 * 60, 2 * 3600
MAX_LIVE, OFFER_TTL_S, MAX_POSTS_PER_RUN = 3, 20 * 60, 2   # the team posts ≤ 12 listings/tick across all processes
OTHER_LACK_H, MAX_OTHER_LACKS = 2.0, 1  # a sale is a page-closer only if the buyer lacks ≤ 1 other card of that set
BUILD = ("RET", "CHA")     # pages we build (RET Saturday, CHA Sunday; GAME.md)
BASE_ASK = {"common": 40, "uncommon": 45, "rare": 95}
TEAM_RE = re.compile(r"^t\d+$")


# ---------------------------------------------------------------------------------------------------- the game API

class Api:
    """GETs on public keyless routes, the team key only for /api/me*. Writes refuse to run in dry-run mode."""

    def __init__(self, url, key, dry_run, min_gap=1.0):
        self.pub = _Http(url, {}, 15.0, False, 3)
        self.team = Bazaar(url, key, wait_on_tick=False) if key else None
        self.dry_run, self.min_gap, self._last = dry_run, min_gap, 0.0

    def _paced(self, fn, *a, **k):
        wait = self._last + self.min_gap - time.time()
        if wait > 0:
            time.sleep(wait)
        try:
            return fn(*a, **k)
        finally:
            self._last = time.time()

    def _live(self, fn, *a, **k):
        if self.dry_run:
            raise RuntimeError("dry run: game writes (and /api/me/offers) are disabled")
        return self._paced(fn, *a, **k)

    def clock(self):
        return self._paced(self.pub._call, "GET", "/api/clock")

    def feed(self, limit=1000):
        return self._paced(self.pub._call, "GET", "/api/feed", query={"limit": limit})

    def board(self, venue="rastro"):
        return self._paced(self.pub._call, "GET", f"/api/venues/{venue}/offers")

    def leaderboard(self):
        return self._paced(self.pub._call, "GET", "/api/leaderboard")

    def catalog(self):
        return self._paced(self.pub._call, "GET", "/api/catalog")

    def me(self):
        return self._paced(self.team.me)

    def value(self, card):
        return self._paced(self.team.value, card)

    def my_offers(self):  # a read, but only live mode needs it (tonight: team key for /api/me and /api/me/value only)
        return self._live(self.team.my_offers)

    def list_offer(self, give, want, to, expires_in_ticks):
        return self._live(self.team.list_offer, give, want, venue="rastro", to=to, expires_in_ticks=expires_in_ticks)

    def cancel(self, offer_id):
        return self._live(self.team.cancel, offer_id)

    def wait_tick(self):
        c = self.clock()
        time.sleep(max(0.05, float(c.get("next_tick_in", 1.0))) + 0.15)
        return c


# ---------------------------------------------------------------------------------------------------- market data

def load_market(api, now, data_dir=DATA):
    """Feed events (oldest first) and El Rastro's open offers tagged with their team. Uses the collector's files when
    data/board.json was written < 2 min ago, else fetches (and still merges the local feed history)."""
    events, src = {}, "collector"
    fp, bp = Path(data_dir) / "feed.jsonl", Path(data_dir) / "board.json"
    if fp.exists():
        with fp.open() as f:
            for line in f:
                if line.strip():
                    e = json.loads(line)
                    events[e["id"]] = e
    board = None
    if bp.exists():
        b = json.loads(bp.read_text())
        if now - b.get("t", 0) < FRESH_S:
            board = b.get("offers", [])
    if board is None:
        src = "fetched"
        for e in api.feed(1000).get("events", []):
            events[e["id"]] = e
        makers = {e["payload"]["offer"]["id"]: e["actor"] for e in events.values() if e["type"] == "offer.listed"}
        board = api.board("rastro").get("offers", [])
        for o in board:
            o["team"] = makers.get(o["id"], "?")
    return sorted(events.values(), key=lambda e: (e["tick"], e["id"])), board, src


class GameTime:
    """Game hours of a tick, from the events that carry both (backfilled settlements have no `t`)."""

    def __init__(self, events, tick_seconds=60.0):
        pts = sorted({(e["tick"], e["t"]) for e in events if e.get("t") is not None})
        self.ticks, self.hours, self.step = [p[0] for p in pts], [p[1] for p in pts], tick_seconds / 3600

    def of(self, e):
        return e["t"] if e.get("t") is not None else self.at(e["tick"])

    def at(self, tick):
        if not self.ticks:
            return tick / 60
        i = min(max(bisect.bisect_left(self.ticks, tick), 0), len(self.ticks) - 1)
        if i > 0 and abs(self.ticks[i - 1] - tick) < abs(self.ticks[i] - tick):
            i -= 1
        return self.hours[i] + (tick - self.ticks[i]) * self.step


def want_cards(want):
    return list(want.get("cards") or []) + [t.split(":", 1)[1] for t in want.get("types") or [] if t.startswith("card:")]


def is_team(x):
    return bool(x) and bool(TEAM_RE.match(str(x)))


def read_signals(events, board, me_id, gt, now_tick, cards, now_h=None):
    """→ (latest signal per (team, card), profile per (team, set)). A signal: kind lack | hold | gone, game hours,
    source text, live flag, price. Profile: `ratios` (price/book the team paid or bid: a floor on its multiplier) and
    `collects` (it bid for, asked a dealer for, or bought a card of that set)."""
    last, prof = {}, {}

    def put(team, card, kind, hours, tick, eid, src, live=False, price=None):
        if not is_team(team) or team == me_id or card not in cards:
            return
        sig = {"team": team, "card": card, "kind": kind, "hours": hours, "tick": tick, "src": src, "live": live,
               "price": price, "order": (live, tick, eid)}
        if (team, card) not in last or sig["order"] >= last[(team, card)]["order"]:
            last[(team, card)] = sig

    def note(team, card, price=None, collects=True):
        if not is_team(team) or card not in cards:
            return
        p = prof.setdefault((team, cards[card]["set"]), {"ratios": [], "collects": False})
        p["collects"] |= collects
        if price:
            p["ratios"].append(price / cards[card]["book"])

    for e in events:
        p, h, typ = e.get("payload") or {}, gt.of(e), e["type"]
        if typ == "offer.listed":
            o, team = p.get("offer") or {}, e.get("actor")
            give, want = o.get("give") or {}, o.get("want") or {}
            for a in give.get("assets") or []:
                put(team, a.get("ref"), "hold", h, e["tick"], e["id"], f"listed it at {want.get('cash')} P (tick {e['tick']})")
            wc = want_cards(want)
            for c in wc:
                put(team, c, "lack", h, e["tick"], e["id"], f"bid {give.get('cash')} P for it (tick {e['tick']})",
                    price=give.get("cash"))
                if give.get("cash") and len(wc) == 1 and c in cards:
                    note(team, c, give["cash"])
        elif typ == "thread.opened" and p.get("kind") == "persona":
            c = ((p.get("topic") or {}).get("buy") or {}).get("card")
            if c:
                put(p.get("team"), c, "lack", h, e["tick"], e["id"], f"asked {p.get('with')} to sell it (tick {e['tick']})")
                note(p.get("team"), c)
        elif typ == "thread.message" and p.get("kind") == "persona" and p.get("sender") == p.get("team"):
            for a in ((p.get("offer") or {}).get("give") or {}).get("assets") or []:
                put(p.get("team"), a.get("ref"), "hold", h, e["tick"], e["id"],
                    f"offered it to {p.get('with')} (tick {e['tick']})")
        elif typ == "settlement":
            items = [i for i in p.get("items") or [] if i.get("kind") == "card"]
            for i in items:
                put(i.get("to"), i.get("ref"), "hold", h, e["tick"], e["id"],
                    f"bought it at {p.get('price')} P from {i.get('frm')} (tick {e['tick']})")
                put(i.get("frm"), i.get("ref"), "gone", h, e["tick"], e["id"], f"sold it to {i.get('to')} (tick {e['tick']})")
                if items and p.get("price"):
                    note(i.get("to"), i.get("ref"), p["price"] / len(items))
        elif typ == "pack.opened" and (p.get("best") or {}).get("ref"):
            put(p.get("team"), p["best"]["ref"], "hold", h, e["tick"], e["id"], f"pulled it from a pack (tick {e['tick']})")
        elif typ == "gift.given":
            for c in p.get("cards") or []:
                put(p.get("team"), c, "hold", h, e["tick"], e["id"], f"got it as a gift (tick {e['tick']})")

    now_h = gt.at(now_tick) if now_h is None else now_h
    for o in board:
        team, give, want = o.get("team"), o.get("give") or {}, o.get("want") or {}
        for a in give.get("assets") or []:
            put(team, a.get("ref"), "hold", now_h, now_tick, math.inf, f"lists it now at {want.get('cash')} P (offer {o['id']})",
                live=True, price=want.get("cash"))
        for c in want_cards(want):
            put(team, c, "lack", now_h, now_tick, math.inf, f"bids {give.get('cash')} P for it now (offer {o['id']})",
                live=True, price=give.get("cash"))
    return last, prof


# ---------------------------------------------------------------------------------------------------- pricing rules

def fee(price, n_cards=1):
    """El Rastro's taker fee: ceil(5%) + 1 P per card."""
    return math.ceil(price * 0.05) + n_cards


def sell_price(rarity, copy_value, page_extra, m_est=None, live_bid=None):
    """Ask for a spare: base 40/45/95, lowered to half a last card's worth to a buyer with multiplier m_est, raised to
    the buyer's live bid, never below our copy value + 3."""
    base = BASE_ASK.get(rarity)
    if base is None:
        return None
    price = base
    if m_est:
        price = min(base, round(0.5 * page_extra * m_est))
    if live_bid:
        price = max(price, int(live_bid))
    return max(price, math.ceil(copy_value + 3))


def max_buy_price(value, we_accept=False):
    """Highest price within the limit value − 3 − fee (no fee when they accept our bid)."""
    p = math.floor(value - 3)
    while we_accept and p > 0 and p + fee(p) > value - 3:
        p -= 1
    return p


def buy_price(book, value, live_ask=None):
    """Our bid: their live ask or the card's book (a non-collector values it at book × m ≤ book × 1.6), capped at the
    limit. None if even 1 P is above the limit."""
    cap = max_buy_price(value)
    if cap < 1:
        return None
    return max(1, min(int(live_ask) if live_ask else int(book), cap))


# ---------------------------------------------------------------------------------------------------- the engine

def find_opportunities(*, events, board, lb, cat, me, value_of, build=BUILD, cash_floor=200, now_tick, gt,
                       committed_cash=0, now_h=None, our_listed=()):
    """Every SELL / BUY pair the signals support, with hard-limit and feeding checks; status filled in later."""
    cards, sets = {}, {}
    for s in cat["sets"]:
        page = [c for c in s["cards"] if c.get("page", c["rarity"] in BASE_ASK)]
        sets[s["id"]] = {"name": s["name"], "released": s.get("released", True), "page": [c["id"] for c in page],
                         "bonus": (cat.get("values") or {}).get("page_bonus", 0.25) * sum(c["book"] for c in page)}
        for c in s["cards"]:
            cards[c["id"]] = {"set": s["id"], "rarity": c["rarity"], "book": c["book"], "name": c.get("name", c["id"])}
    me_id = me["id"]
    now_h = gt.at(now_tick) if now_h is None else now_h  # game hours: the clock's t_hours when we have it
    last, prof = read_signals(events, board, me_id, gt, now_tick, cards, now_h)

    teams = sorted(lb.get("teams", []), key=lambda t: -(t.get("score") or 0))
    info = {t["team"]: {**t, "rank": i + 1} for i, t in enumerate(teams)}
    top = {t["team"] for t in teams[:TOP_N]}
    ours = (info.get(me_id) or {}).get("score")
    if ours is None:
        ours = (me.get("score") or {}).get("score") or 0

    held = {}
    for a in me.get("assets", []):
        if a.get("kind") == "card":
            held.setdefault(a["ref"], []).append(a)
    complete = {p["set"] for p in (me.get("album") or {}).get("pages", []) if p.get("complete")}
    protected = set(build) | complete
    listed = {a["id"] for o in board if o.get("team") == me_id for a in (o.get("give") or {}).get("assets") or []}
    listed |= set(our_listed)  # live mode: assets in our open offers per /api/me/offers (the board tags can miss some)
    missing = {s: [c for c in sets[s]["page"] if c not in held] for s in build if s in sets}

    opps = []
    for (team, card), sig in last.items():
        c, t = cards[card], info.get(team, {"team": team, "name": team, "score": None, "rank": None})
        age_h = max(0.0, now_h - sig["hours"])
        gap = round(ours - t["score"], 2) if t.get("score") is not None else None
        base = {"team": team, "team_name": t.get("name", team), "rank": t.get("rank"), "their_score": t.get("score"), "gap": gap,
                "card": card, "card_name": c["name"], "set": c["set"], "set_name": sets[c["set"]]["name"],
                "rarity": c["rarity"], "src": sig["src"], "live": sig["live"], "age_min": round(age_h * 60),
                "confident": age_h <= CONF_H, "reasons": []}
        if sig["kind"] == "lack" and card in held:
            copies = [a for a in held[card] if a["id"] not in listed]
            spare = len(copies) >= 2 or (copies and c["set"] not in protected)
            if not spare:
                continue  # the only copy of a page card we build or completed: never for sale
            a = min(copies, key=lambda x: x.get("your_value") or 0)
            v = float(a.get("your_value") or 0)
            p = prof.get((team, c["set"]), {})
            m_est = min(1.6, max(0.5, max(p["ratios"]))) if p.get("ratios") else None
            price = sell_price(c["rarity"], v, c["book"] + sets[c["set"]]["bonus"], m_est,
                               sig["price"] if sig["live"] else None)
            if price is None:
                continue
            others = sorted(k[1] for k, x in last.items() if k[0] == team and k[1] != card and x["kind"] == "lack"
                            and cards[k[1]]["set"] == c["set"] and now_h - x["hours"] <= OTHER_LACK_H)
            o = {**base, "side": "SELL", "price": price, "our_value": v, "gain": round(price - v, 1), "asset": a["id"],
                 "completes": False, "collects": p.get("collects", False), "m_est": m_est, "other_lacks": others}
            if team in top:
                o["reasons"].append("top 4")
            if gap is None or gap < SCORE_GAP:
                o["reasons"].append("not on the leaderboard" if gap is None else f"{-gap:g} above us" if gap < 0
                                    else f"only {gap:g} below us (needs ≥ {SCORE_GAP})")
            if price < v + 3:
                o["reasons"].append("price below value + 3")
            opps.append(o)
        elif sig["kind"] == "hold" and any(card in m for m in missing.values()):
            completes = len(missing[c["set"]]) == 1
            value = value_of(card)
            if value is None:
                continue
            p = prof.get((team, c["set"]), {})
            live_ask = sig["price"] if sig["live"] else None
            price = buy_price(c["book"], value, live_ask)
            o = {**base, "side": "BUY", "price": price, "our_value": value, "completes": completes,
                 "gain": round(min(GAIN_CAP, value - price), 1) if price else 0, "max_price": max_buy_price(value),
                 "collects": p.get("collects", False)}
            if price is None:
                o["reasons"].append(f"worth only {value:g} to us")
            if team in top:
                o["reasons"].append("top 4")
            cash = me.get("cash", 0) - committed_cash
            if price and cash - price < cash_floor:
                o["reasons"].append(f"cash floor {cash_floor} (cash {cash})")
            opps.append(o)
    opps.sort(key=lambda o: (not o["reasons"], o["confident"], len(o.get("other_lacks", ())) <= (MAX_OTHER_LACKS or 99),
                             o["completes"], o["gain"], not o["collects"], -o["age_min"]), reverse=True)
    return opps, {"ours": ours, "top": top, "missing": missing, "held": held, "protected": protected, "me_id": me_id}


def choose_alerts(opps, state, now):
    """Mark each opportunity's status; return the ones to alert now (strategic filter + cooldowns)."""
    alerts = state.get("alerts", [])
    hour = [a for a in alerts if now - a["ts"] < 3600]
    live = [x for x in state.get("live", []) if x.get("status", "live") == "live"]
    picked = []
    for o in opps:
        if o["reasons"]:
            o["status"] = "no: " + "; ".join(o["reasons"])
        elif not (o["gain"] >= MIN_GAIN or o["completes"]):
            o["status"] = f"listed only: gain {o['gain']:g} < {MIN_GAIN}"
        elif MAX_OTHER_LACKS is not None and len(o.get("other_lacks", ())) > MAX_OTHER_LACKS:
            o["status"] = (f"listed only: they also lack {', '.join(o['other_lacks'])}: not their last or "
                           f"second-to-last {o['set']} card")
        elif not o["confident"]:
            o["status"] = f"listed only: signal {o['age_min']} game-min old"
        elif any(x["team"] == o["team"] and x["card"] == o["card"] for x in live):
            o["status"] = "offer already live"
        elif any(a["team"] == o["team"] and a["card"] == o["card"] and now - a["ts"] < PAIR_COOLDOWN_S for a in alerts):
            o["status"] = "cooldown: same team + card within 2 h"
        elif any(a["team"] == o["team"] and now - a["ts"] < TEAM_COOLDOWN_S for a in alerts) or \
                any(p["team"] == o["team"] for p in picked):
            o["status"] = "cooldown: team alerted within 45 min"
        elif len(hour) + len(picked) >= ALERTS_PER_H:
            o["status"] = f"held: {ALERTS_PER_H} alerts in the last hour"
        elif len(live) + len(picked) >= MAX_LIVE:
            o["status"] = f"held: {MAX_LIVE} opportunity offers live"
        elif len(picked) >= MAX_POSTS_PER_RUN:
            o["status"] = "next run"
        else:
            o["status"] = "ALERT"
            picked.append(o)
    return picked


def within_hard_limits(o, cash, cash_floor):
    """The operator's limits (ORCHESTRATOR.md), checked once more right before posting."""
    if o["side"] == "SELL":
        return o["price"] >= o["our_value"] + 3
    return o["price"] is not None and o["price"] <= o["our_value"] - 3 and cash - o["price"] >= cash_floor


# ---------------------------------------------------------------------------------------------------- messages

def message(o, offer_id=None):
    oid = offer_id or "????"
    t, x, n, s, p = o["team_name"], o["card"], o["card_name"], o["set_name"], o["price"]
    if o["side"] == "SELL":
        why = (f"spare copy worth {o['our_value']:g} to us → +{o['gain']:g} at {p} P; {t} is #{o['rank']} at "
               f"{o['their_score']}, {o['gap']:g} below us and outside the top 4 (feeding rule OK); they {o['src']}"
               f"{'; other ' + o['set'] + ' cards they lack: ' + ', '.join(o['other_lacks']) if o.get('other_lacks') else ''}")
        es = (f"Che, les falta la {x} ({n}) para la página de {s}, ¿no? Se la dejamos publicada a su nombre en El Rastro a {p} P, "
              f"oferta {oid}. No tienen que creernos: la ven ustedes mismos, la aceptan y la suman a la página; si es "
              f"la última, la cierran y se llevan el bonus.")
        en = (f"You're missing {x} ({n}) for your {s} page, right? It's on El Rastro addressed to {t} at {p} P, offer {oid}. "
              f"No need to trust us: check it yourselves and accept. If it's your last one, you close the page and "
              f"get the bonus.")
        line = f"Accept offer {oid} on El Rastro"
    else:
        why = (f"{x} is worth {o['our_value']:g} to us{' and COMPLETES our ' + s + ' page' if o['completes'] else ''}"
               f" → +{o['gain']:g} at {p} P (limit {o['max_price']}); {t} #{o['rank']} "
               f"{'collects ' + s if o['collects'] else 'never bid for ' + s}; they {o['src']}")
        if o["collects"]:
            es = (f"Les compramos la {x} a {p} P: la oferta ya está a su nombre en El Rastro (oferta {oid}). "
                  f"La revisan ustedes y, si les cierra, la aceptan.")
            en = (f"We'll buy your {x} for {p} P: the offer is already on El Rastro addressed to {t} (offer {oid}). "
                  f"Check it and accept if it works for you.")
        else:
            es = (f"¿Ustedes juntan {s}? Si no, la {x} les sirve poco: les ofrecemos {p} P y ya está la oferta a su "
                  f"nombre en El Rastro (oferta {oid}). Revísenla antes de aceptar: son {p} P por una carta que no usan.")
            en = (f"Do you collect {s}? If not, {x} does little for you: we're offering {p} P, already on El Rastro "
                  f"addressed to {t} (offer {oid}). Check it before accepting: {p} P for a card you don't use.")
        line = f"Accept offer {oid} on El Rastro (you hand over one {x} for {p} P)"
    title = f"{o['side']} {x} {'to' if o['side'] == 'SELL' else 'from'} {t} at {p} P (+{o['gain']:g})"
    body = (f"{o['side']} {x} ({o['rarity']}, {s}) · {t} · offer {oid} at {p} P"
            f"{'' if offer_id else ' [dry run: not posted]'}\nWhy: {why}\n\nES: {es}\n\nEN: {en}\n\n"
            f"Their agent: \"{line}\"")
    return title, body


# ---------------------------------------------------------------------------------------------------- state, output

def load_state(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return {"alerts": [], "live": []}


def save_state(path, state, now):
    state["alerts"] = [a for a in state.get("alerts", []) if now - a["ts"] < 86400]
    state["live"] = [x for x in state.get("live", []) if x.get("status") == "live" or now - x["ts"] < 86400]
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(state, indent=1))


def reconcile(api, state, events, me_id, now):
    """Live mode: drop tracked offers that closed (filled or expired), cancel ours unfilled after 20 min. Returns the
    asset ids in our open offers, so a copy listed by another process is never offered twice."""
    mine = [o for o in api.my_offers().get("offers", []) if o.get("maker") == me_id and o.get("status") == "open"]
    open_ids = {o["id"] for o in mine}
    for x in state.get("live", []):
        if x.get("status") != "live":
            continue
        if x["offer"] not in open_ids:
            filled = any(e["type"] == "settlement" and e["tick"] >= x.get("tick", 0) and any(
                (x["side"] == "SELL" and i.get("id") == x.get("asset") and i.get("to") == x["team"]) or
                (x["side"] == "BUY" and i.get("ref") == x["card"] and i.get("frm") == x["team"] and i.get("to") == me_id)
                for i in e["payload"].get("items", [])) for e in events)
            x["status"] = "filled" if filled else "closed (expired or cancelled)"
        elif now - x["ts"] > OFFER_TTL_S:
            try:
                api.cancel(x["offer"])
                x["status"] = "cancelled: unfilled 20 min"
            except BazaarError as e:
                print(f"opportunities: cancel {x['offer']} failed: {e.code}", flush=True)
        for a in state.get("alerts", []):
            if a.get("offer") == x["offer"]:
                a["status"] = x["status"]
    cancelled = {x["offer"] for x in state.get("live", []) if x.get("status", "").startswith("cancelled")}
    return {a["id"] for o in mine if o["id"] not in cancelled for a in (o.get("give") or {}).get("assets") or []}


def write_md(path, opps, state, ctx, *, dry_run, now, clock, src):
    L = [f"# Opportunities (auto, {time.strftime('%H:%M', time.localtime(now))}, game tick {clock.get('tick')}, "
         f"t {clock.get('t_hours')} h){' · DRY RUN: nothing posted, nobody notified' if dry_run else ''}", "",
         f"Alert rule: gain ≥ {MIN_GAIN} or it completes our page · signal ≤ {int(CONF_H * 60)} game min old · "
         f"≤ {ALERTS_PER_H} alerts/h · team 45 min · team+card 2 h · sells only to teams ≥ {SCORE_GAP} below us "
         f"({ctx['ours']}) and outside the top 4 ({', '.join(sorted(ctx['top']))}). Data: {src}.", "",
         f"## Ranked now ({len(opps)})", "",
         "| # | side | team | card | price | our value | gain | signal | age (game min) | status |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for i, o in enumerate(opps[:60], 1):
        L.append(f"| {i} | {o['side']} | {o['team_name']} (#{o['rank']}, {o['their_score']}) | {o['card']} {o['rarity']}"
                 f"{' · COMPLETES' if o['completes'] else ''} | {o['price'] if o['price'] is not None else '-'} | {o['our_value']:g} | {o['gain']:g} | "
                 f"{o['src']} | {o['age_min']}{' live' if o['live'] else ''} | {o.get('status', '')} |")
    L += ["", "## Alerts (newest first)", ""]
    for a in sorted(state.get("alerts", []), key=lambda a: -a["ts"])[:20]:
        L.append(f"- {time.strftime('%H:%M', time.localtime(a['ts']))} {a['side']} {a['card']} · {a['team']} at "
                 f"{a['price']} P · offer {a.get('offer')} · {a.get('status', '')}")
    L += ["", "## Our side", "",
          "Pages we build, cards missing: " + "; ".join(f"{s}: {', '.join(m) or 'none'}" for s, m in ctx["missing"].items()),
          "Value of missing cards looked up this run (only those some team holds): " + (", ".join(
              f"{c} {v:g}" for c, v in sorted(ctx.get("values", {}).items()) if v is not None) or "none"),
          "Spares (sellable copies): " + ", ".join(
              f"{r} ×{len(c)} ({min(a.get('your_value') or 0 for a in c):g})" for r, c in sorted(ctx["held"].items())
              if len(c) >= 2 or r.split("-")[0] not in ctx["protected"])]
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(L) + "\n")


# ---------------------------------------------------------------------------------------------------- one run

def run_once(api, *, dry_run, now=None, state_path=STATE, out_path=OUT, data_dir=DATA, build=BUILD,
             cash_floor=None, notifier=notify, log=print):
    now = time.time() if now is None else now
    cash_floor = int(os.environ.get("CASH_FLOOR", 200)) if cash_floor is None else cash_floor
    state = load_state(state_path)
    clock = api.clock()
    events, board, src = load_market(api, now, data_dir)
    lb, cat, me = api.leaderboard(), api.catalog(), api.me()
    gt = GameTime(events, float(clock.get("tick_seconds") or 60))
    now_tick = clock.get("tick") or (events[-1]["tick"] if events else 0)
    our_listed = reconcile(api, state, events, me["id"], now) if not dry_run else set()
    committed = sum(x["price"] for x in state.get("live", []) if x.get("status") == "live" and x["side"] == "BUY")

    values = {}

    def value_of(card):
        if card not in values:
            try:
                values[card] = float(api.value(card)["your_value"])
            except Exception as e:
                log(f"opportunities: value {card} unavailable ({e!r})")
                values[card] = None
        return values[card]

    opps, ctx = find_opportunities(events=events, board=board, lb=lb, cat=cat, me=me, value_of=value_of, build=build,
                                   cash_floor=cash_floor, now_tick=now_tick, gt=gt, committed_cash=committed,
                                   now_h=clock.get("t_hours"), our_listed=our_listed)
    ctx["values"] = values
    picked = choose_alerts(opps, state, now)
    ttl_ticks = math.ceil(OFFER_TTL_S / float(clock.get("tick_seconds") or 60)) + 1
    cash = me.get("cash", 0) - committed
    for o in picked:
        if dry_run:
            o["status"] = "would alert (dry run)"
            title, body = message(o)
            log(f"\n=== WOULD ALERT: {title}\n{body}")
            continue
        if not within_hard_limits(o, cash, cash_floor):
            o["status"] = "blocked by hard limits"
            continue
        give, want = ({"assets": [o["asset"]]}, {"cash": o["price"]}) if o["side"] == "SELL" else \
            ({"cash": o["price"]}, {"cards": [o["card"]]})
        try:
            r = api.list_offer(give, want, o["team"], ttl_ticks)
        except BazaarError as e:
            o["status"] = f"post failed: {e.code}"
            log(f"opportunities: post {o['side']} {o['card']} to {o['team']} failed: {e.code} {e.message[:100]}")
            break  # e.g. the team's 12 listings this tick are used up: try next run
        oid = r.get("id") or (r.get("offer") or {}).get("id")
        if oid is None:  # posted, but we can't point anyone at it: no alert
            o["status"] = "posted without an offer id in the response: check /api/me/offers"
            log(f"opportunities: {o['status']} ({json.dumps(r)[:200]})")
            break
        if o["side"] == "BUY":
            cash -= o["price"]
        rec = {"ts": now, "tick": now_tick, "side": o["side"], "team": o["team"], "card": o["card"], "price": o["price"],
               "offer": oid, "asset": o.get("asset"), "status": "live"}
        state.setdefault("live", []).append(dict(rec))
        state.setdefault("alerts", []).append(dict(rec))
        o["status"] = f"ALERTED · offer {oid} live"
        title, body = message(o, oid)
        for who in ("dani", "lucas"):
            notifier(who, title, body, priority=5 if o["completes"] else 4, tags=["moneybag"])
        log(f"opportunities: posted offer {oid} and alerted: {title}")
    write_md(out_path, opps, state, ctx, dry_run=dry_run, now=now, clock=clock, src=src)
    if not dry_run:
        save_state(state_path, state, now)
    return opps, picked


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--once", action="store_true", help="one run, then exit")
    ap.add_argument("--every", type=int, default=30, help="seconds between runs (then waits for the server's tick)")
    ap.add_argument("--dry-run", action="store_true", help="compute + print; no offers, no cancels, no notifications")
    ap.add_argument("--build", default=",".join(BUILD), help="sets whose pages we build (default RET,CHA)")
    ap.add_argument("--any-gap", action="store_true",
                    help="alert SELLs even when the buyer lacks 2+ other cards of that set (off: page-closers only)")
    a = ap.parse_args(argv)
    if a.any_gap:
        global MAX_OTHER_LACKS
        MAX_OTHER_LACKS = None
    api = Api(URL, os.environ.get("BAZAAR_KEY", ""), a.dry_run)
    build = tuple(s.strip().upper() for s in a.build.split(",") if s.strip())
    while True:
        started = time.time()
        try:
            opps, picked = run_once(api, dry_run=a.dry_run, build=build)
            ok = [o for o in opps if not o["reasons"]]
            sent = len(picked) if a.dry_run else sum(o["status"].startswith("ALERTED") for o in picked)
            print(f"{time.strftime('%H:%M:%S')} opportunities: {len(opps)} found, {len(ok)} pass the hard rules, "
                  f"{sent} {'would alert' if a.dry_run else 'alerted'} → {OUT.relative_to(ROOT)}", flush=True)
        except BazaarError as e:
            print(time.strftime("%H:%M:%S"), "opportunities:", e.code, e.message[:120], flush=True)
        except Exception as e:  # a daemon keeps going through anything
            print(time.strftime("%H:%M:%S"), "opportunities error:", repr(e)[:200], flush=True)
        if a.once:
            return 0
        time.sleep(max(0.0, a.every - (time.time() - started)))
        try:
            api.wait_tick()
        except Exception:
            time.sleep(5)


if __name__ == "__main__":
    sys.exit(main())
