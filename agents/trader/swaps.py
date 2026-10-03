"""Swap engine (Chief, Sat 15:40): our spare copies for cards we lack, card for card, no cash.

A swap scores like a team trade for both sides at private values [V feed: t15 <-> t07, 3 swaps at ticks 607-616]. Every
other tick, for each spare we hold and each card we lack (0 copies):
- a spare: a card with 2+ copies free of open offers (2 copies, one in an ask: no spare), never a card the book asks for
  (run/book.json "sell") nor a reserved one (run/reserved.json {"cards": [...]}, else the "## Reserved" section of
  run/operator-handoff.md); the least valuable free copy goes;
- a holder: a team that holds the card (feed holdings, a lower bound; tools/v10_radar.py) and collects our spare's
  set (tools/collectors.py, never "dumps") or values it at m >= 1 (multipliers);
- the counterparty policy (tools/policy.py, Chief 16:20): the top 5 only if our gain >= 3x theirs; Teams 13 and 17
  never with their gain > ours; a page card (01-10) only to a team >= 6 below us, unless the feed shows it lacks 2+
  other cards of that set (then it isn't a page-closer); unknown scores block;
- our gain = our value of the card (GET /api/me/value, page bonus included) - our value of the copy we give >= +3
  (+PACK_DRAG while we hold an unopened pack); never a card we already want in an open offer or the book bids for;
- their gain, conservative (their low multiplier on what they get, high on what they give; 2nd copy 25%, 3rd 10%) minus
  the venue's per-card fee on both cards, > 0;
and posts the best as an ADDRESSED swap (give our asset, want the card type) on a partner venue (v15 Team 15, v07
Team 10, v20 Team 3) that is open, owned, not the counterparty's own and not owned by a top-5 team. Live swaps are read
from /api/me/offers every run: at most MAX_LIVE, one per team, card and spare; one is cancelled when its card reached
us another way or its counterparty or venue owner entered the top 5. Value reads: only for pairs that pass every other
check, at most VALUE_READS per run, paced. Every post, fill, expiry and cancel goes to logs/swaps.jsonl with our est.
gain (dry-run events are tagged and nothing is posted or saved).

    source .env && uv run python -u agents/trader/swaps.py           # every other tick (tools/daemons.sh start swaps)
    source .env && uv run python agents/trader/swaps.py --dry-run --once
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for p in ("bazaar-kit", "tools", "agents/trader"):
    sys.path.insert(0, str(ROOT / p))
from bazaar_sdk import Bazaar, BazaarError  # noqa: E402
import opportunities as op  # noqa: E402
import v10_radar as vr  # noqa: E402
from book import expires_param  # noqa: E402
from collectors import CachedCollectors  # noqa: E402
import policy  # noqa: E402
import alerts  # noqa: E402  the phone policy (Chief 17:40)
_notify = None             # alerts.act's own transport (tools/notify.py) unless a test passes one
NUDGE_MIN_GAIN, NUDGE_EVERY_S = 10.0, 7200   # Chief 17:40: one push per (team, give, get) per 2 h, gain >= 10

PARTNERS = ("v15",)   # Chief 17:45: never a rival's venue (value created lifts its market); t15 -> El Rastro
HOUSE = "rastro"
MIN_OUR_GAIN = 3.0
PACK_DRAG = 2.5        # an unopened pack drags each trade's score ~-2.4 (GAME.md): raise our bar while we hold one
MAX_LIVE = 4
LIFE_TICKS = 10        # real ticks a swap offer lives
VALUE_TICKS = 20       # our value of a card we lack is re-read this often (and whenever our holdings change)
VALUE_READS, READ_GAP_S = 4, 0.25   # at most this many value reads per run, this far apart (shared 5 req/s)
POSTS_PER_RUN = 2
ME = "t05"
STATE, LOG = ROOT / "run" / "swaps_state.json", ROOT / "logs" / "swaps.jsonl"
BOOK, RESERVED, HANDOFF = ROOT / "run" / "book.json", ROOT / "run" / "reserved.json", ROOT / "run" / "operator-handoff.md"
CARD = re.compile(r"\b[A-Z]{3}-\d{2}\b")


def log(event: dict) -> None:
    event = {"t": time.strftime("%H:%M:%S"), **event}
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps(event) + "\n")
    print(json.dumps(event), flush=True)


def page_card(card: str) -> bool:
    try:
        return 1 <= int(card.split("-")[1]) <= 10
    except (IndexError, ValueError):
        return False


def book_refs(path: Path = BOOK, side: str = "sell") -> set:
    try:
        return {e["card"] for e in json.loads(Path(path).read_text()).get("offers") or [] if e.get("side") == side}
    except (OSError, ValueError, AttributeError, KeyError, TypeError):
        return set()


def reserved_refs(path: Path | None = None, handoff: Path | None = None) -> set:
    return policy.reserved_refs(path, handoff)


def wants_of(offers) -> set:
    """Every card our open offers want (bids and swaps): never a second one through a swap."""
    out = set()
    for o in offers:
        w = o.get("want") or {}
        out |= set(w.get("cards") or []) | {t[5:] for t in w.get("types") or [] if str(t).startswith("card:")}
        out |= {a.get("ref") for a in w.get("assets") or [] if isinstance(a, dict) and a.get("ref")}
    return out


def our_spares(me: dict, locked: set, exclude=frozenset()) -> dict:
    """{ref: the least valuable free copy} for every card with a spare left after the copies already in open offers
    (2 copies, one in an ask: no spare, else both could go and the page loses the card)."""
    copies: dict = {}
    for a in me.get("assets") or []:
        if a.get("kind") == "card" and a.get("your_value") is not None and a.get("ref") not in exclude:
            copies.setdefault(a["ref"], []).append(a)
    out = {}
    for ref, cs in copies.items():
        free = [a for a in cs if a["id"] not in locked]
        if free and len(cs) - 1 - (len(cs) - len(free)) >= 1:
            out[ref] = min(free, key=lambda a: a["your_value"])
    return out


def their_gain(team, gets: str, gives: str, *, mult, held, cards, fee: int = 0) -> tuple[float, float]:
    """(est., conservative) gain for `team` getting card `gets` and giving one copy of `gives`, less its fee."""
    g, v = cards[gets], cards[gives]
    m_g, lo_g, _ = vr._triple((mult.get(team) or {}).get(g["set"], 1.0))
    m_v, _, hi_v = vr._triple((mult.get(team) or {}).get(v["set"], 1.0))
    c_get = vr.copy_weight(len(held.get((team, gets), ())) + 1)
    c_give = vr.copy_weight(len(held.get((team, gives), ())) or 1)
    return (round(g["book"] * m_g * c_get - v["book"] * m_v * c_give - fee, 1),
            round(g["book"] * lo_g * c_get - v["book"] * hi_v * c_give - fee, 1))


def pick_venue(to: str, venues: dict, top: set) -> str | None:
    """A partner venue that is open, owned, not owned by a rival (`top`) nor by the counterparty; El Rastro when the
    counterparty owns the partner venue (it can't trade on its own stall)."""
    for v in PARTNERS:
        x = venues.get(v) or {}
        if x.get("status") == "open" and x.get("owner") and x["owner"] not in top and x["owner"] != to:
            return v
    if any((venues.get(v) or {}).get("owner") == to for v in PARTNERS) and (venues.get(HOUSE) or {}).get("status") \
            in (None, "open"):
        return HOUSE
    return None


def candidates(*, me, locked, our_value, teams, held, mult, cards, last, collectors, venues, skip_want=frozenset(),
               no_spare=frozenset(), busy=(), min_gain=MIN_OUR_GAIN) -> list[dict]:
    """Every swap that clears both bars, best first. `our_value(card)` is called only for pairs that pass every
    other check (a value read costs a request on the shared key) and may return None (not read: skip)."""
    if not teams or ME not in {t["team"] for t in teams}:
        return []                                     # no live ranking: no top 5, no gaps: post nothing
    spares = our_spares(me, locked, no_spare)
    if not spares:
        return []
    top = policy.rivals(teams)
    have = {a["ref"] for a in me.get("assets") or [] if a.get("kind") == "card"}
    busy_teams, busy_cards = {b["to"] for b in busy}, {b["want"] for b in busy}
    busy_assets = {b["asset"] for b in busy}
    holders: dict = {}
    for (team, card), ids in held.items():
        if ids and team != ME and str(team).startswith("t") and card in cards \
                and card not in have and card not in skip_want and card not in busy_cards and team not in busy_teams:
            holders.setdefault(card, []).append(team)
    out = []
    for want, with_it in sorted(holders.items()):
        pairs = []
        for ref, asset in spares.items():
            if asset["id"] in busy_assets or ref not in cards:
                continue
            st = cards[ref]["set"]
            for team in with_it:
                ok, why = collectors.allows(team, st)
                m = vr._triple((mult.get(team) or {}).get(st, 0.0))[0]
                if "dumps" in why or not (ok or m >= 1.0):
                    continue                          # it neither collects our spare's set nor values it
                closer = page_card(ref) and len([k for k, x in last.items() if k[0] == team and k[1] != ref
                                                 and x.get("kind") == "lack"
                                                 and cards.get(k[1], {}).get("set") == st]) < 2
                if closer and not policy.check(team, teams=teams, our_gain=1e9, their_gain=0.0, page_closer=True)[0]:
                    continue                          # the cheap part of the policy first: the page-closer gap
                venue = pick_venue(team, venues, top)
                if venue is None:
                    continue
                fee = 2 * int((venues.get(venue) or {}).get("fee_per_card") or 0)
                est, low = their_gain(team, ref, want, mult=mult, held=held, cards=cards, fee=fee)
                if low <= 0:
                    continue
                pairs.append((ref, asset, team, venue, est, low, closer))
        if not pairs:
            continue
        v_want = our_value(want)                      # only now: every other check passed
        if v_want is None:
            continue
        for ref, asset, team, venue, est, low, closer in pairs:
            gain = round(v_want - asset["your_value"], 1)
            if gain >= min_gain and policy.check(team, teams=teams, our_gain=gain, their_gain=est,
                                                 page_closer=closer)[0]:
                out.append({"asset": asset["id"], "give": ref, "want": want, "to": team, "venue": venue,
                            "our_gain": gain, "their_est": est, "their_low": low, "our_value_want": v_want,
                            "our_value_give": asset["your_value"]})
    out.sort(key=lambda c: (-c["our_gain"], -c["their_low"]))
    return out


def is_swap(o: dict) -> bool:
    give, want = o.get("give") or {}, o.get("want") or {}
    return (o.get("venue") in PARTNERS and len(give.get("assets") or []) == 1 and not give.get("cash")
            and not want.get("cash") and len(wants_of([o])) == 1 and bool(o.get("to")))


class Engine:
    def __init__(self, b, *, dry_run=False, mult_fn=vr.hub_mult, events_fn=vr.load_events, state=STATE, book=BOOK,
                 reserved=None, handoff=None, collectors=None, log=log, sleep=time.sleep, notifier=_notify):
        self.b, self.dry_run, self.mult_fn, self.events_fn, self.state_path = b, dry_run, mult_fn, events_fn, state
        self.book, self.reserved, self.handoff, self.log, self.sleep = book, reserved, handoff, log, sleep
        self.collectors = collectors or CachedCollectors()
        self.notifier = notifier
        self.values: dict = {}
        self.cards: dict = {}
        self._hub: dict = {}
        self._hub_at = 0.0
        self._holdings = None
        self._reads = 0
        try:
            self.state = json.loads(Path(state).read_text())
        except (OSError, ValueError):
            self.state = {"live": []}

    def emit(self, event: dict) -> None:
        self.log({**event, "dry_run": True} if self.dry_run else event)

    def save(self) -> None:
        if self.dry_run:
            return
        path = Path(self.state_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state, indent=1))
        tmp.replace(path)

    def save_gone(self, known, live_ids, mine_ids, have) -> None:
        """Log our swaps gone since the last run (filled or expired) and save at once, so they aren't logged twice."""
        gone = [x for x in known.values() if x["offer"] not in live_ids]
        for x in gone:
            filled = x.get("asset") not in mine_ids and x["want"] in have
            self.emit({"event": "filled" if filled else "expired", **x})
        if gone:
            self.state["live"] = [x for x in self.state.get("live", []) if x.get("offer") in live_ids]
            self.save()

    def our_value(self, card: str, tick: int):
        hit = self.values.get(card)
        if hit is not None and tick - hit[1] < VALUE_TICKS:
            return hit[0]
        if self._reads >= VALUE_READS:
            return None                               # next run
        if self._reads:
            self.sleep(READ_GAP_S)
        self._reads += 1
        try:
            self.values[card] = (float(self.b.value(card)["your_value"]), tick)
        except (BazaarError, KeyError, TypeError, ValueError):
            return None
        return self.values[card][0]

    def run(self, tick: int, tick_seconds: float) -> list[dict]:
        self._reads = 0
        if not self.cards:
            self.cards = vr.card_index(self.b.catalog())
        if time.time() - self._hub_at > 600:
            self._hub, self._hub_at = self.mult_fn() or self._hub, time.time()
        mult = vr.load_mult(self._hub)
        me = self.b.me()
        ids = tuple(sorted(a["id"] for a in me.get("assets") or []))
        if ids != self._holdings:                     # a card in or out: our values moved (page bonuses)
            self.values, self._holdings = {}, ids
        mine = [o for o in self.b.my_offers().get("offers") or []
                if o.get("maker") == me["id"] and o.get("status", "open") in ("open", "queued")]
        locked = {a["id"] if isinstance(a, dict) else a for o in mine for a in (o.get("give") or {}).get("assets") or []}
        have = {a["ref"] for a in me.get("assets") or [] if a.get("kind") == "card"}
        mine_ids = {a["id"] for a in me.get("assets") or []}
        known = {x["offer"]: x for x in self.state.get("live", []) if x.get("offer") is not None}
        live, others = [], []                         # ours (posted by this engine) and hand-made swaps: busy only
        for o in mine:                                # live swaps from the server, not from our file
            if is_swap(o):
                a = (o["give"]["assets"] or [None])[0]
                asset = a.get("id") if isinstance(a, dict) else a
                x = {**known.get(o["id"], {}), "offer": o["id"], "asset": asset, "want": next(iter(wants_of([o]))),
                     "to": o["to"], "venue": o["venue"]}
                (live if o["id"] in known else others).append(x)
        live_ids = {x["offer"] for x in live}
        self.save_gone(known, live_ids, mine_ids, have)
        teams = sorted(self.b.leaderboard().get("teams") or [], key=lambda t: -(t.get("score") or 0))
        top = policy.rivals(teams)
        venues = None
        no_spare = frozenset(book_refs(self.book, "sell") | reserved_refs(self.reserved, self.handoff))
        for x in list(live):                          # cancel what no longer passes
            ok, pwhy = policy.check(x["to"], teams=teams, our_gain=x.get("our_gain"), their_gain=x.get("their_est"))
            ref = x.get("give") or next((a.get("ref") for a in me.get("assets") or [] if a["id"] == x["asset"]), None)
            others_locked = locked - {x["asset"]}
            spare_left = ref is not None and ref in our_spares(me, others_locked, no_spare) and \
                our_spares(me, others_locked, no_spare)[ref]["id"] is not None
            why = ("its card reached us another way" if x["want"] in have else
                   f"{ref} is reserved or asked by the book now" if ref in no_spare else
                   f"{ref} has no other free copy left" if not spare_left else
                   None if ok or not teams else pwhy)
            if why is None and teams:
                venues = venues or {v.get("venue"): v for v in self.b.venues().get("venues") or []}
                if (venues.get(x["venue"]) or {}).get("owner") in top:
                    why = f"venue {x['venue']}'s owner is in the top {policy.TOP_N}"
            if why:
                if not self.dry_run:
                    try:
                        self.b.cancel(x["offer"])
                    except BazaarError as e:
                        self.emit({"event": "cancel_failed", "code": e.code, **x})
                        continue
                self.emit({"event": "cancel", "why": why, **x})
                live.remove(x)
        self.state["live"] = live
        self.save()
        if len(live) >= MAX_LIVE:
            return []
        busy = live + others
        venues = venues or {v.get("venue"): v for v in self.b.venues().get("venues") or []}
        events = self.events_fn()
        last, _ = op.read_signals(events, [], ME, op.GameTime(events), tick, self.cards)
        packs = any(a.get("kind") == "pack" for a in me.get("assets") or [])
        cands = candidates(me=me, locked=locked, our_value=lambda c: self.our_value(c, tick), teams=teams,
                           held=vr.holdings(events), mult=mult, cards=self.cards, last=last,
                           collectors=self.collectors.get(), venues=venues,
                           skip_want=frozenset(wants_of(mine) | book_refs(self.book, "buy")),
                           no_spare=no_spare, busy=busy, min_gain=MIN_OUR_GAIN + (PACK_DRAG if packs else 0))
        posted = []
        for c in cands:
            if len(self.state["live"]) >= MAX_LIVE or len(posted) >= POSTS_PER_RUN:
                break
            if any(c["to"] == x["to"] or c["want"] == x["want"] or c["asset"] == x["asset"]
                   for x in self.state["live"] + others):
                continue
            ev = {"event": "post", "tick": tick, **c}
            if self.dry_run:
                self.emit(ev)
                self.state["live"].append({**c, "offer": None, "tick": tick})   # one per team/card/spare this run
                posted.append(c)
                continue
            try:
                r = self.b.list_offer({"assets": [c["asset"]]}, {"types": [f"card:{c['want']}"]}, venue=c["venue"],
                                      to=c["to"], expires_in_ticks=expires_param(LIFE_TICKS, tick_seconds))
            except BazaarError as e:
                self.emit({**ev, "event": "post_failed", "code": e.code, "message": e.message[:120]})
                break
            r = r if isinstance(r, dict) else {}
            oid = r.get("id") or (r.get("offer") or {}).get("id")
            self.emit({**ev, "offer": oid})
            if oid is None:                           # posted, can't track it: stop; the next run reads it back
                break
            self.state["live"].append({**c, "offer": oid, "tick": tick})
            posted.append(c)
            self.save()
            self.nudge(c, oid, tick_seconds, teams)
        if self.dry_run:
            self.state["live"] = live
        return cands


    def nudge(self, c: dict, oid, tick_seconds: float, teams=()) -> None:
        """An ACT for Dani (a ready DM): only at our gain >= NUDGE_MIN_GAIN, once per (team, give, get) per 2 h (a
        repost's new offer id beat the 10-min dedupe: 3 pushes in 12 min), never to a rival (top 6 or within 3)."""
        if c["our_gain"] < NUDGE_MIN_GAIN or c["to"] in alerts.rivals(teams):
            self.emit({"event": "nudge_skipped", "offer": oid, "to": c["to"], "our_gain": c["our_gain"]})
            return
        until_ts = time.time() + LIFE_TICKS * float(tick_seconds or 30)
        until = "~" + time.strftime("%H:%M", time.localtime(until_ts))
        team = f"Team {int(c['to'][1:])}" if str(c["to"])[1:].isdigit() else c["to"]
        name = lambda r: (self.cards.get(r) or {}).get("name", r)   # noqa: E731
        dm = (f"Hi {team}! Swap offer for you on {c['venue']}: our {name(c['give'])} ({c['give']}) for your "
              f"{name(c['want'])} ({c['want']}), offer {oid}. Thanks!")   # transactional only (Lucas 17:20)
        alerts.act(f"swap {c['give']} for {c['want']} → {team}", oid, until_ts,
                   f"Offer {oid} on {c['venue']}, valid until {until}. Our est. gain +{c['our_gain']:g}.\nDM {team}:\n{dm}",
                   source="swaps", asset=c["asset"], want=c["want"], want_n=0,
                   key=f"swap:{c['to']}:{c['give']}:{c['want']}", key_every_s=NUDGE_EVERY_S, notifier=self.notifier,
                   log=lambda m: self.emit({"event": "alert", "msg": m}))


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], allow_abbrev=False)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="post and save nothing; logged events are tagged dry_run")
    args = ap.parse_args(argv)
    b = Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"],
               wait_on_tick=False, retries=1)
    eng = Engine(b, dry_run=args.dry_run)
    clock, last = None, None
    while True:
        try:
            clock = b.clock() if clock is None else b.wait_tick()
            if clock.get("paused") or clock.get("doors") not in (None, "open"):
                if args.once:
                    return
                time.sleep(max(5.0, float(clock.get("next_tick_in") or 30)))
                continue
            if last is None or clock["tick"] - last >= 2 or args.once:
                last = clock["tick"]
                cands = eng.run(clock["tick"], float(clock.get("tick_seconds") or 30))
                if args.dry_run:
                    for c in cands[:10]:
                        print(json.dumps(c), flush=True)
        except Exception as e:                       # never die, never spin
            log({"event": "error", "error": repr(e)[:200]})
            time.sleep(5)
        if args.once:
            return


if __name__ == "__main__":
    main()
