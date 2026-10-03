"""The maker book: keep our standing offers posted, fresh and repriced, every tick, no LLM (plan §5's repricer).

The Operator writes the desired book in run/book.json and runs this; it re-reads the file every tick:

    {"offers": [{"card": "SAL-08", "side": "sell", "to": "t16", "price": 30, "floor": 20},
                {"card": "RET-07", "side": "buy", "price": 40, "floor": 55, "page_closer": true}]}

`floor` is the worst price we take: the least for an ask, the most for a bid. Optional: `to` (an addressed offer),
`venue`, `page_closer` (a trade that completes a page, ours or theirs: El Rastro), `step` (P per reprice), `life`
(real ticks an offer lives, default LIFE_TICKS; page-critical bids <= 20, directive 09:46), `last_card` (a bid for a
card of a page we build: once it is the page's last missing card, our value jumps by the page bonus and the bid goes
straight to value - LAST_GAIN, cash permitting: any price up to there scores the capped +50; checked every
VALUE_TICKS).

Each tick, per entry (one live offer per card and side):
- not posted, expired or cancelled: post it (an ask whose copy left us, or a bid whose card arrived, is filled: done);
- expiring within REFRESH_LEFT ticks: cancel and post again at the same price;
- unfilled REPRICE_AFTER ticks at one price: cancel and post one step toward the floor (asks down, bids up);
- its `price` edited in the file: cancel and post at the new price within a tick (clamped to the floor). A bid held
  below its file price (by the floor, value - 3 or cash) is re-checked every VALUE_TICKS and moves up once it can;
- a bid that cash can't cover is posted at what cash allows (never dropped: a closer at any price <= value - 50 still
  scores the capped +50), and moves up when cash frees;
- its entry removed from the file: cancel the live offer (an unreadable or missing file changes nothing);
- a bid whose card reached us another way (a dealer, the trader): cancel it, done (a second copy is worth 25%).
An ask goes only to a team that collects the card's set (tools/collectors.py: teams.md "collects" or its bids /
dealer asks; "dumps" or unknown: no; a public ask, with no `to`, never): a live one that stops qualifying is
cancelled. Never past the floor, nor past what scores: an ask at least our copy's value + --min-gain-sell (1: as maker we pay
no fee, so any price above value scores; the trader's +6 is a taker's bar), a bid at most our value - --min-gain. Bids keep cash >= --cash-floor across all our bids.
Venue: the entry's, else DEFAULT_VENUE (v07); El Rastro for a page-closer, and when the venue is closed, unseen or
owned by a top-4 team. Limits: at most NEW_SHARE of the team's new offers per tick and the open-offer limit minus
OPEN_RESERVE (/api/clock limits; the trader and opps post too). expires_in_ticks is sent in Friday's 60 s ticks.
Every post, refresh, reprice, expiry and fill goes to logs/book.jsonl.

    source .env && uv run python -u agents/trader/book.py              # every tick
    source .env && uv run python agents/trader/book.py --dry-run --once
"""
from __future__ import annotations

import argparse
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
from collectors import CachedCollectors, set_of  # noqa: E402
import policy  # noqa: E402

BOOK, STATE, LOG = ROOT / "run" / "book.json", ROOT / "run" / "book_state.json", ROOT / "logs" / "book.jsonl"
HOUSE = "rastro"
DEFAULT_VENUE = os.environ.get("DEFAULT_VENUE", "v07")
LIFE_TICKS = 40         # real ticks an offer lives; refreshed before it ends
REFRESH_LEFT = 5        # re-post when this few ticks are left
REPRICE_AFTER = 20      # ticks unfilled at one price before one step toward the floor
STEP_SHARE = 0.25       # default step: a quarter of the distance to the floor, at least 1 P
NEW_SHARE = 0.5         # of the team's new offers per tick (12): the rest for the trader and opps
OPEN_RESERVE = 5        # open offers left free for the other processes
VALUE_TICKS = 10        # our value of a card is re-read this often
MIN_GAIN_SELL, MIN_GAIN_BUY = 1.0, 3.0     # maker asks: value + 1 (no fee; +6 is the trader's taker bar); bids -3
LAST_GAIN = 50          # a team trade scores at most 50: the page's last card is worth bidding up to value - 50
CASH_FLOOR = int(os.environ.get("CASH_FLOOR", 200))


def log(event: dict) -> None:
    event = {"t": time.strftime("%H:%M:%S"), **event}
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps(event) + "\n")
    print(json.dumps(event), flush=True)


def expires_param(real_ticks: int, tick_seconds: float) -> int:
    """The server counts expires_in_ticks in Friday's 60 s ticks (Sat [V]: 60 -> 30, 120 -> 60, 200 -> 100)."""
    return math.ceil(real_ticks * 60 / float(tick_seconds or 60))


def load(path: Path, default):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return default


def desired(path: Path) -> list | None:
    """The file's offers; None when it is missing or half-written (then nothing changes: never "cancel everything")."""
    d = load(path, None)
    return d["offers"] if isinstance(d, dict) and isinstance(d.get("offers"), list) else None


def save(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=1))
    tmp.replace(path)


def venue_for(e: dict, venues: dict, top: set | None) -> str:
    """El Rastro for a page-closer, an unseen or closed venue, a venue owned by a top-4 team, or when the top 4 is
    unknown (the leaderboard read failed): a team venue only when we know its owner is outside the top 4."""
    if e.get("page_closer") or top is None:
        return HOUSE
    want = e.get("venue") or DEFAULT_VENUE
    v = venues.get(want)
    if want == HOUSE or not v or v.get("status") != "open" or v.get("owner") in top:
        return HOUSE
    return want


def matches(o: dict, e: dict) -> int | None:
    """The price of our open offer `o` when it is entry `e`'s (same card, side and `to`), else None."""
    give, want = o.get("give") or {}, o.get("want") or {}
    if (o.get("to") or None) != (e.get("to") or None):
        return None
    if e["side"] == "sell":
        refs = {a.get("ref") for a in give.get("assets") or [] if isinstance(a, dict)}
        return want.get("cash") if e["card"] in refs and want.get("cash") else None
    cards = set(want.get("cards") or []) | {t.split(":", 1)[1] for t in want.get("types") or [] if t.startswith("card:")}
    return give.get("cash") if e["card"] in cards and give.get("cash") else None


def toward(price: int, floor: int, sell: bool, step: int | None) -> int:
    """One step from `price` toward `floor`, never past it."""
    gap = price - floor if sell else floor - price
    if gap <= 0:
        return price
    d = min(gap, step or max(1, math.ceil(gap * STEP_SHARE)))
    return price - d if sell else price + d


class Book:
    def __init__(self, b, *, dry_run: bool = False, log=log, min_gain_sell=MIN_GAIN_SELL, min_gain_buy=MIN_GAIN_BUY,
                 cash_floor=CASH_FLOOR, collectors=None):
        self.b, self.dry_run, self.log = b, dry_run, log
        self.min_gain_sell, self.min_gain_buy, self.cash_floor = min_gain_sell, min_gain_buy, cash_floor
        self.values: dict[str, tuple[float, int]] = {}   # card -> (our value, tick read): re-read every VALUE_TICKS
        self.tick = 0
        self._ctx_tick: int | None = None
        self._top_tick: int | None = None
        self.collectors = collectors or CachedCollectors()
        self.venues: dict = {}
        self.top: set = set()
        self.teams: list | None = None
        self.reserved = policy.reserved_refs

    def context(self, tick: int) -> None:
        """Venues and the top 4, read every 10 ticks (public reads)."""
        if self._ctx_tick is not None and tick - self._ctx_tick < 10:
            return
        self._ctx_tick = tick
        try:
            self.venues = {v.get("venue"): v for v in self.b.venues().get("venues") or []}
        except BazaarError as e:
            self.log({"event": "error", "where": "venues", "code": e.code})
            self.venues = {}                         # unseen: El Rastro
        self.top4(tick)

    def top4(self, tick: int) -> set | None:
        """The top 4, read at most once a tick; None when the read fails (then nothing goes on a team venue). Sat
        11:31: MAL-02 was reposted on v07 with its owner already in the top 4 (read every 10 ticks before)."""
        if self._top_tick != tick:
            self._top_tick = tick
            try:
                teams = sorted(self.b.leaderboard().get("teams") or [], key=lambda t: -(t.get("score") or 0))
                self.top = {t["team"] for t in teams[:4]}
                self.teams = teams
            except BazaarError as e:
                self.log({"event": "error", "where": "leaderboard", "code": e.code})
                self.top, self.teams = None, None
        return self.top

    def value(self, card: str) -> float | None:
        """Our value, re-read every VALUE_TICKS: it moves with our holdings (the last card of a page jumps by the
        page bonus, CHA +106)."""
        hit = self.values.get(card)
        if hit is None or self.tick - hit[1] >= VALUE_TICKS:
            try:
                self.values[card] = (float(self.b.value(card)["your_value"]), self.tick)
            except (BazaarError, KeyError, TypeError, ValueError):
                return None if hit is None else hit[0]
        return self.values[card][0]

    def step(self, book: list[dict], st: dict, clock: dict) -> dict:
        """One tick. Returns the new state ({key: {offer, price, since, asset, held}})."""
        tick, secs = clock["tick"], float(clock.get("tick_seconds") or 30)
        self.tick = tick
        limits = clock.get("limits") or {}
        self.context(tick)
        me = self.b.me()
        mine = {o["id"]: o for o in self.b.my_offers().get("offers") or []
                if o.get("maker") == me["id"] and o.get("status", "open") in ("open", "queued")}
        copies: dict[str, list] = {}
        for a in me.get("assets") or []:
            if a.get("kind") == "card":
                copies.setdefault(a["ref"], []).append(a)
        locked = {a["id"] if isinstance(a, dict) else a for o in mine.values()
                  for a in (o.get("give") or {}).get("assets") or []}
        bid_cash = sum((o.get("give") or {}).get("cash") or 0 for o in mine.values())
        new_left = max(0, int((limits.get("offers_per_team_per_tick") or 12) * NEW_SHARE))
        open_left = (limits.get("max_open_offers_per_team") or 30) - OPEN_RESERVE - len(mine)
        out: dict = {}
        due = []
        adopted = {x.get("offer") for x in st.values() if x.get("offer")}
        for e in book:
            sell = e["side"] == "sell"
            key = f"{e['card']}:{e['side']}"
            s = dict(st.get(key) or {})
            if s.get("done"):
                out[key] = s
                continue
            held = len(copies.get(e["card"], []))
            if sell:                                  # only to a team that collects the set (Chief 11:50)
                ok, why = self.collectors.get().allows(e.get("to"), set_of(e["card"]))
                if ok and self.teams and e.get("to"):  # and the counterparty policy (16:20); unread board: as before
                    ok, why = policy.check(e.get("to"), teams=self.teams, page_closer=bool(e.get("page_closer")))
                if e["card"] in self.reserved():      # never a reserved card (run/reserved.json, Chief 16:45)
                    ok, why = False, f"{e['card']} is reserved (run/reserved.json)"
                if not ok:
                    if s.get("offer") in mine and self.dry_run:
                        self.log({"event": "cancel_not_collector", "card": e["card"], "offer": s["offer"], "why": why,
                                  "dry_run": True})
                    elif s.get("offer") in mine:
                        try:
                            self.b.cancel(s["offer"])
                            self.log({"event": "cancel_not_collector", "card": e["card"], "offer": s["offer"],
                                      "why": why})
                        except BazaarError as err:
                            self.log({"event": "cancel_failed", "card": e["card"], "offer": s["offer"],
                                      "code": err.code})
                    elif s.get("blocked") != why:
                        self.log({"event": "skip", "card": e["card"], "side": "sell", "why": why})
                    out[key] = {k: v for k, v in s.items() if k != "offer"} | {"blocked": why}
                    continue
                s.pop("blocked", None)
            if not s.get("offer"):                    # one of ours already out (posted by hand): take it over
                for oid, x in mine.items():
                    if oid not in adopted and (p := matches(x, e)) is not None:
                        assets = [a["id"] for a in (x.get("give") or {}).get("assets") or [] if isinstance(a, dict)]
                        s = {"offer": oid, "price": p, "since": tick, "asset": assets[0] if assets else None,
                             "held": held}
                        adopted.add(oid)
                        self.log({"event": "adopt", "card": e["card"], "side": e["side"], "offer": oid, "price": p})
                        break
            if s.get("price") is not None and "entry" not in s:
                s["entry"] = int(e["price"])            # state from before price edits moved offers: no move now
            o = mine.get(s.get("offer"))
            if s.get("offer") and o is None:         # gone since last tick: filled, or expired / cancelled
                filled = (s.get("asset") not in {a["id"] for a in copies.get(e["card"], [])} if sell
                          else held > s.get("held", 0))
                self.log({"event": "filled" if filled else "expired", "card": e["card"], "side": e["side"],
                          "offer": s["offer"], "price": s.get("price")})
                if filled:
                    out[key] = {**s, "done": True, "offer": None}
                    continue
                s["offer"] = None
            if o is not None and not sell and held > s.get("held", held):
                ev = {"event": "cancel_held", "card": e["card"], "offer": s["offer"], "held": held}
                if self.dry_run:
                    self.log({**ev, "dry_run": True})
                    out[key] = s
                    continue
                try:
                    self.b.cancel(s["offer"])
                    self.log(ev)
                    out[key] = {**s, "done": True, "offer": None}
                except BazaarError as err:
                    self.log({**ev, "event": "cancel_failed", "code": err.code})
                    out[key] = s
                continue
            if o is not None:
                left = (o.get("expires_tick") or tick + LIFE_TICKS) - tick
                if left <= REFRESH_LEFT:
                    due.append(((0, left), key, e, s, "refresh"))
                elif int(e["price"]) != s.get("entry"):
                    due.append(((2, -1), key, e, s, "move"))   # the Operator edited the price: now, not in 20 ticks
                elif not sell and (s.get("clamped") or e.get("last_card")) and \
                        tick - s.get("checked", tick) >= VALUE_TICKS:
                    due.append(((2, -1), key, e, s, "recheck"))   # held below what we want, or maybe the last card
                elif tick - s.get("since", tick) >= REPRICE_AFTER:
                    due.append(((2, 0), key, e, s, "reprice"))
                else:
                    out[key] = s
            else:
                due.append(((1, 0), key, e, s, "post"))
        for _, key, e, s, why in sorted(due, key=lambda x: x[0]):   # refreshes first, then posts, then reprices
            if new_left <= 0 or (not s.get("offer") and open_left <= 0):
                out[key] = s                          # next tick
                continue
            r, posted = self.place(e, s, why, tick, secs, copies, locked, me, bid_cash)
            out[key] = s if r is None else r
            if posted:
                new_left -= 1
                open_left -= not s.get("offer")
                if e["side"] == "buy":
                    bid_cash += r["price"] - (s.get("price") or 0 if s.get("offer") else 0)
        keys = {f"{e['card']}:{e['side']}" for e in book}
        for key, s in st.items():                     # removed from the file: take its offer down
            if key in keys or s.get("done") or s.get("offer") not in mine:
                continue
            ev = {"event": "cancel_removed", "key": key, "offer": s["offer"], "price": s.get("price")}
            if self.dry_run:
                self.log({**ev, "dry_run": True})
                continue
            try:
                self.b.cancel(s["offer"])
                self.log(ev)
            except BazaarError as err:
                self.log({**ev, "event": "cancel_failed", "code": err.code})
                out[key] = s                          # try again next tick
        return out

    def place(self, e, s, why, tick, secs, copies, locked, me, bid_cash) -> tuple[dict | None, bool]:
        """Cancel the live one (refresh, reprice) and post at the right price: (new state or None, posted)."""
        sell = e["side"] == "sell"
        card, closing = e["card"], False
        edited = s.get("entry") != int(e["price"])    # a new entry, or its price edited in the file: the file's price
        price = int(e["price"]) if edited or why == "move" else int(s.get("price") or e["price"])
        if sell:
            free = [a for a in copies.get(card, []) if a["id"] not in locked     # ours only while our offer holds it
                    or (a["id"] == s.get("asset") and s.get("offer"))]
            free = [a for a in free if a.get("your_value") is not None]
            if not free:
                self.log({"event": "skip", "card": card, "side": "sell", "why": "no free copy with a value"})
                return None, False
            asset = min(free, key=lambda a: a["your_value"])
            why_last = policy.last_copy(me, card, committed_ids=locked - {asset["id"]}, giving={asset["id"]})
            if why_last:                              # Chief 17:05: never our last copy of a complete page
                self.log({"event": "skip", "card": card, "side": "sell", "why": why_last})
                return None, False
            floor = max(int(e["floor"]), math.ceil(asset["your_value"] + self.min_gain_sell))
        else:
            if why in ("move", "recheck") or (edited and s.get("entry") is not None):
                self.values.pop(card, None)           # an edit often follows a value jump (the page's last card)
            v = self.value(card)
            if v is None:
                self.log({"event": "skip", "card": card, "side": "buy", "why": "our value unavailable"})
                return None, False
            asset = None
            floor = min(int(e["floor"]), math.floor(v - self.min_gain_buy))
            closing = bool(e.get("last_card")) and math.floor(v - LAST_GAIN) > floor
            if closing:                               # the page's last card: value - 50 still scores the capped +50
                floor = math.floor(v - LAST_GAIN)
            if floor < 1:
                self.log({"event": "skip", "card": card, "side": "buy", "why": f"worth {v:g} to us"})
                return None, False
            if why == "recheck" and not closing and not s.get("clamped"):
                return {**s, "checked": tick}, False  # not the last card, nothing held back: as is
            if closing or why == "recheck":
                price = floor if closing else int(s.get("want") or e["price"])   # back to what it wanted, climb kept
        old = int(s.get("price") or price) if why in ("move", "recheck") else price
        if why == "reprice":
            price = toward(price, floor, sell, e.get("step"))
        price = max(price, floor) if sell else min(price, floor)   # never past the floor, whatever the book says
        if why == "reprice" and price == old and s.get("offer"):
            return {**s, "since": tick}, False        # at the floor already: keep it, wait another round
        mine_now = (s.get("price") or 0) if s.get("offer") else 0     # a replaced bid frees its cash
        room = me.get("cash", 0) - (bid_cash - mine_now) - self.cash_floor
        if not sell and price > room:
            if room < 1:
                self.log({"event": "skip", "card": card, "side": "buy", "why": f"cash floor {self.cash_floor}"})
                return None, False
            self.log({"event": "cash_clamp", "card": card, "price": room, "wanted": price})
        wanted = price
        price = price if sell else min(price, max(room, 0))   # what cash allows; moves up when cash frees (clamped)
        target = wanted if sell or closing else max(wanted, int(e["price"]))
        clamped = not sell and price < target
        if why in ("move", "recheck", "reprice") and price == s.get("price") and s.get("offer"):
            # nothing to move. A reprice the cash clamp pulls back to the live price lands here too: without it the
            # bid was cancelled and reposted at the same price every tick (review 3, 13:55)
            return {**s, "entry": int(e["price"]), "clamped": clamped, "want": target, "checked": tick,
                    "since": tick if why == "reprice" else s.get("since", tick)}, False
        venue = venue_for(e, self.venues, self.top4(tick) if (e.get("venue") or DEFAULT_VENUE) != HOUSE else set())
        give, want = ({"assets": [asset["id"]]}, {"cash": price}) if sell else ({"cash": price}, {"cards": [card]})
        ev = {"event": why, "card": card, "side": e["side"], "price": price, "was": old if price != old else None,
              "floor": floor, "venue": venue, "to": e.get("to"), "replaces": s.get("offer")}
        if self.dry_run:
            self.log({**ev, "dry_run": True})
            return None, False
        try:
            if s.get("offer"):
                self.b.cancel(s["offer"])
            r = self.b.list_offer(give, want, venue=venue, to=e.get("to"),
                                  expires_in_ticks=expires_param(int(e.get("life") or LIFE_TICKS), secs))
        except BazaarError as err:
            self.log({**ev, "event": f"{why}_failed", "code": err.code, "message": err.message[:120]})
            return ({**s, "offer": None} if s.get("offer") else None), False
        oid = r.get("id") or (r.get("offer") or {}).get("id")
        self.log({**ev, "offer": oid})
        since = s.get("since", tick) if price == s.get("price") else tick   # the reprice clock runs per price
        return {"offer": oid, "price": price, "since": since, "asset": asset["id"] if asset else None,
                "held": len(copies.get(card, [])), "entry": int(e["price"]), "clamped": clamped, "want": target,
                "checked": tick}, True


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="log what it would do, write nothing")
    ap.add_argument("--cash-floor", type=int, default=CASH_FLOOR)
    ap.add_argument("--min-gain", type=float, default=MIN_GAIN_BUY)
    ap.add_argument("--min-gain-sell", type=float, default=MIN_GAIN_SELL)
    ap.add_argument("--book", type=Path, default=BOOK, help="the desired book (re-read every tick)")
    ap.add_argument("--state", type=Path, default=STATE)
    args = ap.parse_args(argv)
    b = Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"],
               wait_on_tick=False, retries=1)
    book = Book(b, dry_run=args.dry_run, min_gain_sell=args.min_gain_sell, min_gain_buy=args.min_gain,
                cash_floor=args.cash_floor)
    clock = None
    while True:
        try:
            clock = b.clock() if clock is None else b.wait_tick()
            if clock.get("paused") or clock.get("doors") not in (None, "open"):
                if args.once:
                    return
                time.sleep(30)
                continue
            want = desired(args.book)
            if want is None:
                log({"event": "error", "where": "book", "error": f"{args.book} missing or unreadable: nothing changed"})
            st = None if want is None else book.step(want, load(args.state, {}), clock)
            if not args.dry_run and st is not None:
                save(args.state, st)
        except Exception as e:                       # never die, never spin
            log({"event": "error", "where": "loop", "error": repr(e)[:200]})
            time.sleep(5)
        if args.once:
            return


if __name__ == "__main__":
    main()
