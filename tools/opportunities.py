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

Alert only if gain ≥ 20 or it completes our page, the signal is ≤ 30 game minutes AND ≤ 60 real minutes old (the game
clock pauses overnight: real time comes from the collector's (tick, wall time) samples), ≤ 3 Dani alerts per hour,
45 min per team, 2 h per (team, card); a SELL also needs the buyer to lack ≤ 1 other card of that set (seen in the last
2 game hours): a heuristic for "ours is its last or second-to-last card" (plan §4A), since a 40 P ask won't fill
otherwise; a team that signalled only one of several gaps still passes. `--any-gap` turns it off. Everything goes to intel/opportunities.md with its status.
Execution (not --dry-run): post the addressed offer (expires after ~20 min), record its id and save the state, THEN
notify. At most 3 live opportunity offers, cancelled after 20 min unfilled; cash floor env CASH_FLOOR (default 200),
net of the cash in ALL our open bids (/api/me/offers, every process; live mode only).

Reads: public keyless routes (clock, feed, El Rastro's board, leaderboard, catalog), data/feed.jsonl + data/board.json
from the collector when fresh (< 2 min); the team key only for /api/me, /api/me/value (and /api/me/offers when live).
Every request is paced to ≤ 1 per second.
"""
import argparse
import bisect
import itertools
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
BOOK = ROOT / "run" / "book.json"   # the maker book's desired offers (agents/trader/book.py)
URL = os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai")
HOUSE = "rastro"
DEFAULT_VENUE = os.environ.get("DEFAULT_VENUE", "v15")   # Team 15's venue at 0% (Chief 17:45: v07's owner is a rival)

FRESH_S = 120              # collector files younger than this are used instead of fetching
CONF_H = 0.5               # a signal older than 30 game minutes is low confidence: listed, never alerted
WALL_STALE_S = 3600        # ... or older than 60 real minutes, whatever the game clock says (it pauses overnight)
MIN_GAIN, GAIN_CAP = 20, 50
SCORE_GAP, TOP_N = 6, 6    # policy: never a rival (top 6 or within 3, Chief 17:45); page-closers only ≥ 6 below us
RIVALS = frozenset({"t13", "t17"})   # policy: no trade where their gain > ours; unknown here, so none
ALERTS_PER_H, TEAM_COOLDOWN_S, PAIR_COOLDOWN_S = 3, 45 * 60, 2 * 3600
MAX_LIVE, MAX_POSTS_PER_RUN = 3, 2   # the team posts ≤ 12 listings/tick across all processes
OFFER_TTL_TICKS = 20   # in ticks, not minutes: 10 min at Saturday's 30 s, 5 at Sunday's 15 s (page-critical bids)


def expires_param(real_ticks, tick_seconds):
    """`expires_in_ticks` to send for an offer that should live `real_ticks` ticks. The server counts it in Friday's
    60 s ticks: on Saturday (30 s) 60 → 30, 120 → 60, 200 → 100 real ticks (Operator's probe [V]). Sunday's 15 s
    should be x4: check the first post's expires_tick."""
    return math.ceil(real_ticks * 60 / float(tick_seconds or 60))
OTHER_LACK_H, MAX_OTHER_LACKS = 2.0, 1  # a sale closes a page when the buyer lacks ≤ 1 other card of that set
                                         # (its last or second-to-last); no other lack known counts as closing
BUILD = ("RET", "CHA")     # pages we build (RET Saturday, CHA Sunday; GAME.md)
PROTECT = ("LAV",)         # completed: only 2nd/3rd copies are ever for sale (also any page /api/me says is complete)
BASE_ASK = {"common": 40, "uncommon": 45, "rare": 95}
TEAM_RE = re.compile(r"^t\d+$")


# ---------------------------------------------------------------------------------------------------- the game API

class Api:
    """GETs on public keyless routes, the team key only for /api/me*. Writes refuse to run in dry-run mode."""

    def __init__(self, url, key, dry_run, min_gap=1.0):
        self.pub = _Http(url, {}, 15.0, False, 0)  # no SDK retries: they would bypass the pacing; the next run retries
        self.team = Bazaar(url, key, wait_on_tick=False, retries=0) if key else None
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

    def venues(self):
        return self._paced(self.pub._call, "GET", "/api/venues")

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

    def list_offer(self, give, want, to, expires_in_ticks, venue=HOUSE):
        return self._live(self.team.list_offer, give, want, venue=venue, to=to, expires_in_ticks=expires_in_ticks)

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
                try:
                    e = json.loads(line)
                    events[e["id"]] = e
                except (ValueError, KeyError, TypeError):
                    continue  # blank or half-written line
    board = None
    if bp.exists():
        try:
            b = json.loads(bp.read_text())
        except ValueError:
            b = {}  # half-written: fetch instead
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


class WallClock:
    """Real time at which a tick happened, from the collector's (tick, wall time) samples in data/me.jsonl and
    data/leaderboard.jsonl: the first sighting of the last sampled tick at or before it, plus tick_seconds per tick since,
    never later than the first sighting of a later tick. The game clock pauses overnight, so Friday's tick 159 stays
    Friday evening at Saturday 09:00, when the game clock calls it a minute old. With no sample at or before the tick
    (no collector history) it counts back from now, as if the clock never paused."""

    def __init__(self, samples, now, now_tick, tick_seconds=60.0):
        first = {}
        for tick, wall in samples:
            if isinstance(tick, (int, float)) and isinstance(wall, (int, float)) and wall <= now:
                first[tick] = min(wall, first.get(tick, wall))
        self.ticks = sorted(first)
        self.walls = [first[k] for k in self.ticks]
        self.later = list(itertools.accumulate(reversed(self.walls), min))[::-1]  # earliest sighting at index >= i
        self.now, self.now_tick, self.step = now, now_tick, tick_seconds

    @classmethod
    def from_files(cls, data_dir, now, now_tick, tick_seconds=60.0):
        samples = []
        for name in ("me.jsonl", "leaderboard.jsonl"):
            path = Path(data_dir) / name
            if not path.exists():
                continue
            with path.open() as f:
                for line in f:
                    try:
                        r = json.loads(line)
                        samples.append((r.get("tick"), r.get("t")))
                    except (ValueError, AttributeError):
                        continue  # blank or half-written line
        return cls(samples, now, now_tick, tick_seconds)

    def at(self, tick):
        i = bisect.bisect_right(self.ticks, tick)
        if i:
            est = self.walls[i - 1] + (tick - self.ticks[i - 1]) * self.step
        else:
            est = self.now - max(0, self.now_tick - tick) * self.step
        if i < len(self.ticks):
            est = min(est, self.later[i])
        return min(est, self.now)

    def age_s(self, tick):
        return max(0.0, self.now - self.at(tick))


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
                       committed_cash=0, now_h=None, our_listed=(), wall=None, collectors=None):
    """Every SELL / BUY pair the signals support, with hard-limit and feeding checks; status filled in later.
    `wall` (a WallClock) also makes a feed signal older than WALL_STALE_S real seconds low confidence; live board
    offers are standing now, so they never are."""
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
    import policy                                   # rivals: the top 6 or within 3 board points of us (17:45)
    top = policy.rivals(teams, me_id) | ({me_id} if any(t["team"] == me_id for t in teams[:TOP_N]) else set())
    ours = (info.get(me_id) or {}).get("score")
    if ours is None:
        ours = (me.get("score") or {}).get("score") or 0

    held = {}
    for a in me.get("assets", []):
        if a.get("kind") == "card":
            held.setdefault(a["ref"], []).append(a)
    complete = {p["set"] for p in (me.get("album") or {}).get("pages", []) if p.get("complete")}
    protected = set(build) | complete | set(PROTECT)
    listed = {a["id"] for o in board if o.get("team") == me_id for a in (o.get("give") or {}).get("assets") or []}
    listed |= set(our_listed)  # live mode: assets in our open offers per /api/me/offers (the board tags can miss some)
    missing = {s: [c for c in sets[s]["page"] if c not in held] for s in build if s in sets}

    opps = []
    for (team, card), sig in last.items():
        c, t = cards[card], info.get(team, {"team": team, "name": team, "score": None, "rank": None})
        age_h = max(0.0, now_h - sig["hours"])
        wall_age = None if sig["live"] or wall is None else wall.age_s(sig["tick"])
        wall_stale = wall_age is not None and wall_age > WALL_STALE_S
        gap = round(ours - t["score"], 2) if t.get("score") is not None else None
        base = {"team": team, "team_name": t.get("name", team), "rank": t.get("rank"), "their_score": t.get("score"), "gap": gap,
                "card": card, "card_name": c["name"], "set": c["set"], "set_name": sets[c["set"]]["name"],
                "rarity": c["rarity"], "src": sig["src"], "live": sig["live"], "age_min": round(age_h * 60),
                "wall_age_min": None if wall_age is None else round(wall_age / 60), "wall_stale": wall_stale,
                "confident": age_h <= CONF_H and not wall_stale, "reasons": []}
        if sig["kind"] == "lack" and card in held:
            copies = [a for a in held[card] if a["id"] not in listed and a.get("your_value") is not None]
            spare = len(copies) >= 2 or (copies and c["set"] not in protected)
            if not spare:
                continue  # the only copy of a page card we build or completed: never for sale
            a = min(copies, key=lambda x: x.get("your_value") or 0)
            v = float(a["your_value"])
            p = prof.get((team, c["set"]), {})
            m_est = min(1.6, max(0.5, max(p["ratios"]))) if p.get("ratios") else None
            price = sell_price(c["rarity"], v, c["book"] + sets[c["set"]]["bonus"], m_est,
                               sig["price"] if sig["live"] else None)
            if price is None:
                continue
            others = sorted(k[1] for k, x in last.items() if k[0] == team and k[1] != card and x["kind"] == "lack"
                            and cards[k[1]]["set"] == c["set"] and now_h - x["hours"] <= OTHER_LACK_H)
            closing = len(others) <= MAX_OTHER_LACKS
            o = {**base, "side": "SELL", "price": price, "our_value": v, "gain": round(price - v, 1), "asset": a["id"],
                 "completes": False, "collects": p.get("collects", False), "m_est": m_est, "other_lacks": others,
                 "closing": closing}
            if team in top:
                o["reasons"].append(f"rival (top {TOP_N} or within 3 of us)")
            if team in RIVALS:
                o["reasons"].append("rival (Team 13/17): their gain vs ours unknown")
            # Chief 11:50: value created = buyer value - seller value; a sale to a non-collector scored -10.2 [V].
            dumps = collectors is not None and c["set"] in collectors.teams.get(team, {}).get("dumps", set())
            if dumps:
                o["reasons"].append(f"dumps {c['set']} (teams.md): sell only to collectors")
            elif not (p.get("collects") or (collectors is not None and collectors.allows(team, c["set"])[0])):
                o["reasons"].append(f"no sign it collects {c['set']}: sell only to collectors")
            if closing and (gap is None or gap < SCORE_GAP):   # plan §4A: only a page-closer needs the 10-point gap
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
                o["reasons"].append(f"rival (top {TOP_N} or within 3 of us)")
            if team in RIVALS:
                o["reasons"].append("rival (Team 13/17): their gain vs ours unknown")
            if not teams:
                o["reasons"].append(f"leaderboard empty: top {TOP_N} unknown")
            cash = me.get("cash", 0) - committed_cash
            if price and cash - price < cash_floor:
                o["reasons"].append(f"cash floor {cash_floor} (cash {cash})")
            opps.append(o)
    opps.sort(key=lambda o: (not o["reasons"], o["confident"], o.get("closing", False),
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
        elif not o["confident"]:
            o["status"] = (f"listed only: signal {o['wall_age_min']} real min old (game clock paused?)"
                           if o.get("wall_stale") else f"listed only: signal {o['age_min']} game-min old")
        elif any(x["team"] == o["team"] and x["card"] == o["card"] for x in live):
            o["status"] = "offer already live"
        elif o["side"] == "BUY" and any(x.get("side") == "BUY" and x["card"] == o["card"] for x in live + picked):
            o["status"] = "our bid for this card is already out to another holder"
        elif o["side"] == "SELL" and o.get("asset") is not None and any(
                x.get("side") == "SELL" and x.get("asset") == o["asset"] for x in live + picked):
            o["status"] = "this copy is already offered to another team"
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


def venue_for(o, venues, top):
    """(venue id, name) to post `o` on. El Rastro for a trade that completes a page, ours (a BUY that completes) or
    theirs (a SELL to a team with no other known lack in that set: unknown counts as closing): the page bonus's value
    created must not land on a team's venue. Otherwise DEFAULT_VENUE while it is open and its owner is not in the top
    4; otherwise El Rastro."""
    house = (HOUSE, "El Rastro")
    if o.get("completes") or (o["side"] == "SELL" and not o.get("other_lacks")):
        return house
    v = venues.get(DEFAULT_VENUE)
    if DEFAULT_VENUE == HOUSE or not v or v.get("status") != "open" or v.get("owner") in top \
            or v.get("owner") == o.get("team"):         # a rival's venue, or the counterparty's own stall
        return house
    return DEFAULT_VENUE, v.get("name") or DEFAULT_VENUE


# ---------------------------------------------------------------------------------------------------- messages

def message(o, offer_id=None, valid_until=None):
    oid, w = offer_id or "????", o.get("venue_name") or "El Rastro"
    t, x, n, s, p = o["team_name"], o["card"], o["card_name"], o["set_name"], o["price"]
    if o["side"] == "SELL":
        why = (f"spare copy worth {o['our_value']:g} to us → +{o['gain']:g} at {p} P; {t} is #{o['rank']} at "
               f"{o['their_score']}, {o['gap']:g} below us and outside the top 5 (feeding rule OK); they {o['src']}"
               f"{'; other ' + o['set'] + ' cards they lack: ' + ', '.join(o['other_lacks']) if o.get('other_lacks') else ''}")
        # ready-to-send texts: what, offer id, price, thanks; never why (Lucas, Sat 17:20: rivals learn from it)
        es = f"¡Hola, {t}! Les dejamos la {x} ({n}) en {w} a {p} P, a su nombre: oferta {oid}. ¡Gracias!"
        en = f"Hi {t}! {x} ({n}) is on {w} for you at {p} P, offer {oid}. Thanks!"
        line = f"Accept offer {oid} on {w}"
    else:
        why = (f"{x} is worth {o['our_value']:g} to us{' and COMPLETES our ' + s + ' page' if o['completes'] else ''}"
               f" → +{o['gain']:g} at {p} P (limit {o['max_price']}); {t} #{o['rank']} "
               f"{'collects ' + s if o['collects'] else 'never bid for ' + s}; they {o['src']}")
        es = f"¡Hola, {t}! Les compramos la {x} a {p} P: oferta {oid} en {w}, a su nombre. ¡Gracias!"
        en = f"Hi {t}! We'll buy your {x} for {p} P: offer {oid} on {w}, addressed to you. Thanks!"
        line = f"Accept offer {oid} on {w} (you hand over one {x} for {p} P)"
    title = f"{o['side']} {x} {'to' if o['side'] == 'SELL' else 'from'} {t} at {p} P (+{o['gain']:g})"
    body = (f"{o['side']} {x} ({o['rarity']}, {s}) · {t} · offer {oid} at {p} P"
            f"{' · valid until ' + valid_until if valid_until else ''}"
            f"{'' if offer_id else ' [dry run: not posted]'}\nWhy: {why}\n\nES: {es}\n\nEN: {en}\n\n"
            f"Their agent: \"{line}\"")
    return title, body


# ---------------------------------------------------------------------------------------------------- state, output

def book_buys(path=BOOK):
    """Cards the maker book bids for: opps never posts a second bid for one (both could fill: two copies)."""
    try:
        return {e["card"] for e in json.loads(Path(path).read_text()).get("offers") or [] if e.get("side") == "buy"}
    except (OSError, ValueError, AttributeError, KeyError, TypeError):
        return set()


def load_state(path, strict=False):
    """Cooldowns and live offers. A missing file is a fresh start; an unreadable one is refused in live mode (strict),
    because an empty state would silently lift every cap."""
    path = Path(path)
    if not path.exists():
        return {"alerts": [], "live": []}
    try:
        state = json.loads(path.read_text())
        if not isinstance(state, dict):
            raise ValueError("not an object")
        state.setdefault("alerts", [])
        state.setdefault("live", [])
        return state
    except ValueError as e:
        if strict:
            raise RuntimeError(f"{path} unreadable ({e}): fix or delete it before posting") from None
        return {"alerts": [], "live": []}


def save_state(path, state, now):
    state["alerts"] = [a for a in state.get("alerts", []) if now - a["ts"] < 86400]
    state["live"] = [x for x in state.get("live", []) if x.get("status") == "live" or now - x["ts"] < 86400]
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=1))
    os.replace(tmp, path)  # atomic: a crash never leaves half a file


def reconcile(api, state, events, me_id, now, held_refs=(), now_tick=None):
    """Live mode: drop tracked offers that closed (filled or expired), cancel ours unfilled after OFFER_TTL_TICKS (the
    game expires them then too; this is the backstop) and any bid for
    a card we now hold (e.g. the trader bought it). Returns (asset ids in our open offers, so a copy listed by another
    process is never offered twice; cash in ALL our open bids, from every process, for the cash floor)."""
    mine = [o for o in api.my_offers().get("offers", []) if o.get("maker") == me_id
            and o.get("status", "open") in ("open", "queued")]  # a queued offer locks its cash too
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
        elif (stale := now_tick is not None and now_tick - x.get("tick", now_tick) > OFFER_TTL_TICKS) or \
                (x["side"] == "BUY" and x["card"] in held_refs):
            why = f"unfilled {OFFER_TTL_TICKS} ticks" if stale else "we hold the card now"
            try:
                api.cancel(x["offer"])
                x["status"] = f"cancelled: {why}"
            except BazaarError as e:
                print(f"opportunities: cancel {x['offer']} failed: {e.code}", flush=True)
        for a in state.get("alerts", []):
            if a.get("offer") == x["offer"]:
                a["status"] = x["status"]
    cancelled = {x["offer"] for x in state.get("live", []) if x.get("status", "").startswith("cancelled")}
    still = [o for o in mine if o["id"] not in cancelled]
    return ({a["id"] for o in still for a in (o.get("give") or {}).get("assets") or []},
            sum((o.get("give") or {}).get("cash") or 0 for o in still))


def write_md(path, opps, state, ctx, *, dry_run, now, clock, src):
    L = [f"# Opportunities (auto, {time.strftime('%H:%M', time.localtime(now))}, game tick {clock.get('tick')}, "
         f"t {clock.get('t_hours')} h){' · DRY RUN: nothing posted, nobody notified' if dry_run else ''}", "",
         f"Alert rule: gain ≥ {MIN_GAIN} or it completes our page · signal ≤ {int(CONF_H * 60)} game min and "
         f"≤ {WALL_STALE_S // 60} real min old · "
         f"≤ {ALERTS_PER_H} alerts/h · team 45 min · team+card 2 h · never to the top 5 ({', '.join(sorted(ctx['top']))}); "
         f"a sale that closes their page (last or second-to-last known lack) only to teams ≥ {SCORE_GAP} below us "
         f"({ctx['ours']}); page-closers on El Rastro, the rest on {DEFAULT_VENUE}. Data: {src}.", "",
         f"## Ranked now ({len(opps)})", "",
         "| # | side | team | card | price | our value | gain | signal | age (game / real min) | status |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for i, o in enumerate(opps, 1):
        L.append(f"| {i} | {o['side']} | {o['team_name']} (#{o['rank']}, {o['their_score']}) | {o['card']} {o['rarity']}"
                 f"{' · COMPLETES' if o['completes'] else ''} | {o['price'] if o['price'] is not None else '-'} | {o['our_value']:g} | {o['gain']:g} | "
                 f"{o['src']} | {o['age_min']}{' live' if o['live'] else ''}"
                 f"{'' if o.get('wall_age_min') is None else ' / ' + str(o['wall_age_min'])} | {o.get('status', '')} |")
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
             cash_floor=None, notifier=notify, log=print, collectors=None, book_path=BOOK, reserved_path=None):
    now = time.time() if now is None else now
    cash_floor = int(os.environ.get("CASH_FLOOR", 200)) if cash_floor is None else cash_floor
    state = load_state(state_path, strict=not dry_run)
    clock = api.clock()
    events, board, src = load_market(api, now, data_dir)
    lb, cat, me = api.leaderboard(), api.catalog(), api.me()
    gt = GameTime(events, float(clock.get("tick_seconds") or 60))
    now_tick = clock.get("tick") or (events[-1]["tick"] if events else 0)
    wall = WallClock.from_files(data_dir, now, now_tick, float(clock.get("tick_seconds") or 60))
    held_refs = {a["ref"] for a in me.get("assets", []) if a.get("kind") == "card"}
    our_listed, open_bid_cash = reconcile(api, state, events, me["id"], now, held_refs, now_tick) if not dry_run else (set(), 0)
    committed = max(open_bid_cash, sum(x["price"] for x in state.get("live", [])
                                       if x.get("status") == "live" and x["side"] == "BUY"))

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
                                   now_h=clock.get("t_hours"), our_listed=our_listed, wall=wall,
                                   collectors=collectors)
    ctx["values"] = values
    owned = book_buys(book_path)
    if not dry_run:                                   # cards our open offers already want (book bids, swaps)
        try:
            for x in api.my_offers().get("offers") or []:
                if x.get("maker") == me["id"]:
                    w = x.get("want") or {}
                    owned |= set(w.get("cards") or []) | {t[5:] for t in w.get("types") or [] if str(t).startswith("card:")}
        except BazaarError as e:
            log(f"opportunities: my_offers unavailable ({e.code}): book bids only")
    for o in opps:
        if o["side"] == "BUY" and o["card"] in owned:
            o["status"] = "the book bids for it (run/book.json): not posted here"
    import policy  # tools/policy.py: cards no bot gives away (run/reserved.json, Chief 16:45)
    reserved = policy.reserved_refs(reserved_path) if reserved_path else policy.reserved_refs()
    for o in opps:
        if o["side"] == "SELL" and o["card"] in reserved:
            o["status"] = "reserved (run/reserved.json): never sold"
    picked = choose_alerts([o for o in opps if not (o["side"] == "BUY" and o["card"] in owned)
                            and not (o["side"] == "SELL" and o["card"] in reserved)], state, now)
    ttl_ticks = expires_param(OFFER_TTL_TICKS, clock.get("tick_seconds"))
    cash = me.get("cash", 0) - committed
    venues = None
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
        if venues is None:                    # read once, only when something goes out
            try:
                venues = {v.get("venue"): v for v in api.venues().get("venues") or []}
            except Exception as e:            # can't see the venues: El Rastro
                log(f"opportunities: venues unavailable ({e!r}): posting on El Rastro")
                venues = {}
        o["venue"], o["venue_name"] = venue_for(o, venues, ctx["top"])
        try:
            r = api.list_offer(give, want, o["team"], ttl_ticks, o["venue"])
        except BazaarError as e:
            o["status"] = f"post failed: {e.code}"
            log(f"opportunities: post {o['side']} {o['card']} to {o['team']} failed: {e.code} {e.message[:100]}")
            break  # e.g. the team's 12 listings this tick are used up: try next run
        r = r if isinstance(r, dict) else {}
        oid = r.get("id") or (r.get("offer") or {}).get("id")
        if oid is None:  # posted, but we can't point anyone at it: no alert
            o["status"] = "posted without an offer id in the response: check /api/me/offers"
            log(f"opportunities: {o['status']} ({json.dumps(r)[:200]})")
            break
        if o["side"] == "BUY":
            cash -= o["price"]
        rec = {"ts": now, "tick": now_tick, "side": o["side"], "team": o["team"], "card": o["card"], "price": o["price"],
               "offer": oid, "asset": o.get("asset"), "venue": o["venue"], "status": "live"}
        state.setdefault("live", []).append(dict(rec))
        state.setdefault("alerts", []).append(dict(rec))
        save_state(state_path, state, now)  # recorded before anyone is told: a crash can't lose a live offer
        o["status"] = f"ALERTED · offer {oid} live"
        until_ts = now + OFFER_TTL_TICKS * float(clock.get("tick_seconds") or 30)
        title, body = message(o, oid, "~" + time.strftime("%H:%M", time.localtime(until_ts)))
        import alerts                               # the phone policy (Chief 17:40): Dani gets ACT items only
        if o["team"] in alerts.rivals(lb.get("teams") or []):
            log(f"opportunities: posted offer {oid}; no ACT: {o['team']} is a rival (top 6 or within 3)")
        else:
            held_n = sum(1 for a in me.get("assets", []) if a.get("ref") == o["card"])
            alerts.act(f"{o['side']} {o['card']} {'to' if o['side'] == 'SELL' else 'from'} {o['team_name']} at "
                       f"{o['price']} P", oid, until_ts, body, source="opps",
                       asset=o.get("asset") if o["side"] == "SELL" else None,
                       want=o["card"] if o["side"] == "BUY" else None, want_n=held_n, notifier=notifier, now=now,
                       log=log)
        log(f"opportunities: posted offer {oid}: {title}")
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
    a = ap.parse_args(argv)
    api = Api(URL, os.environ.get("BAZAAR_KEY", ""), a.dry_run)
    build = tuple(s.strip().upper() for s in a.build.split(",") if s.strip())
    from collectors import CachedCollectors
    collectors_cache = CachedCollectors()
    while True:
        started = time.time()
        try:
            opps, picked = run_once(api, dry_run=a.dry_run, build=build, collectors=collectors_cache.get())
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
