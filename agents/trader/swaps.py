"""Swap engine (Chief, Sat 15:40): our spare copies for cards we lack, card for card, no cash.

A swap scores like a team trade for both sides at private values [V feed: t15 <-> t07, 3 swaps at ticks 607-616]. Every
other tick, for each spare we hold (2nd+ copy: the least valuable copy goes) and each card we lack (0 copies):
- a holder: a team outside the live top 5 that holds the card (feed holdings, a lower bound; tools/v10_radar.py);
- our gain = our value of the card (GET /api/me/value, page bonus included) - our value of the copy we give, >= +3;
- their gain, est. = book x m x copy weight of what they get - the same of what they give (intel/multipliers.json at
  conf V/L, else the hub's model, else 1.0 [L]; 2nd copy 25%, 3rd 10%), > 0;
- never feed a page: no spare of a set where the team holds >= 8 of the 10 page cards (feed) while within 10 points
  of us; never a card the book bids for (run/book.json);
and posts the best as an ADDRESSED swap (give our asset, want the card type) on a partner venue (v15 Team 15, v07
Team 10, v20 Team 3: 0% fee, the partner scores the value created) that is open, not the counterparty's own and not
owned by a top-5 team; El Rastro never (its 1 P per card fee). Short life (LIFE_TICKS), at most MAX_LIVE live, one per
team, one per card wanted, one per spare. Every post, fill and expiry goes to logs/swaps.jsonl with our est. gain.

    source .env && uv run python -u agents/trader/swaps.py           # every other tick (tools/daemons.sh start swaps)
    source .env && uv run python agents/trader/swaps.py --dry-run --once
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for p in ("bazaar-kit", "tools", "agents/trader"):
    sys.path.insert(0, str(ROOT / p))
from bazaar_sdk import Bazaar, BazaarError  # noqa: E402
import v10_radar as vr  # noqa: E402
from book import expires_param  # noqa: E402
from opportunities import book_buys  # noqa: E402

PARTNERS = ("v15", "v07", "v20")
MIN_OUR_GAIN = 3.0
MAX_LIVE = 4
LIFE_TICKS = 10        # real ticks a swap offer lives
TOP_N = 5
SCORE_GAP = 10         # a team this close to us never gets a card that may close its page
VALUE_TICKS = 20       # our value of a card we lack is re-read this often
POSTS_PER_RUN = 2
ME = "t05"
STATE, LOG = ROOT / "run" / "swaps_state.json", ROOT / "logs" / "swaps.jsonl"


def log(event: dict) -> None:
    event = {"t": time.strftime("%H:%M:%S"), **event}
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps(event) + "\n")
    print(json.dumps(event), flush=True)


def page_cards(card: str) -> bool:
    try:
        return 1 <= int(card.split("-")[1]) <= 10
    except (IndexError, ValueError):
        return False


def our_spares(me: dict, locked: set) -> dict:
    """{ref: the least valuable free copy} for every card with a spare left after the copies already in open offers
    (2 copies, one in an ask: no spare, else both could go and the page loses the card)."""
    copies: dict = {}
    for a in me.get("assets") or []:
        if a.get("kind") == "card" and a.get("your_value") is not None:
            copies.setdefault(a["ref"], []).append(a)
    out = {}
    for ref, cs in copies.items():
        free = [a for a in cs if a["id"] not in locked]
        if free and len(cs) - 1 - (len(cs) - len(free)) >= 1:
            out[ref] = min(free, key=lambda a: a["your_value"])
    return out


def their_gain(team, gets: str, gives: str, *, mult, held, cards) -> tuple[float, float]:
    """(est., conservative) gain for `team` getting card `gets` and giving one copy of `gives`."""
    g, v = cards[gets], cards[gives]
    m_g, lo_g, _ = vr._triple((mult.get(team) or {}).get(g["set"], 1.0))
    m_v, _, hi_v = vr._triple((mult.get(team) or {}).get(v["set"], 1.0))
    c_get = vr.copy_weight(len(held.get((team, gets), ())) + 1)
    c_give = vr.copy_weight(len(held.get((team, gives), ())) or 1)
    return (round(g["book"] * m_g * c_get - v["book"] * m_v * c_give, 1),
            round(g["book"] * lo_g * c_get - v["book"] * hi_v * c_give, 1))


def candidates(*, me, locked, our_value, teams, held, mult, cards, skip_want=frozenset(), busy=()) -> list[dict]:
    """Every swap that clears both bars, best first. `our_value(card)` -> our value of a card we lack (or None)."""
    top = {t["team"] for t in teams[:TOP_N]}
    ours = next((t.get("score") for t in teams if t["team"] == ME), None)
    score = {t["team"]: t.get("score") for t in teams}
    have = {a["ref"] for a in me.get("assets") or [] if a.get("kind") == "card"}
    spares = our_spares(me, locked)
    holders: dict = {}
    for (team, card), ids in held.items():
        if ids and team not in top and team != ME and team and team.startswith("t") and card in cards \
                and card not in have and card not in skip_want:
            holders.setdefault(card, []).append(team)
    busy_teams = {b["to"] for b in busy}
    busy_cards = {b["want"] for b in busy}
    busy_assets = {b["asset"] for b in busy}
    out = []
    for want, teams_with in holders.items():
        if want in busy_cards:
            continue
        v_want = our_value(want)
        if v_want is None:
            continue
        for ref, asset in spares.items():
            if asset is None or asset["id"] in busy_assets or ref not in cards:
                continue
            gain = round(v_want - asset["your_value"], 1)
            if gain < MIN_OUR_GAIN:
                continue
            st = cards[ref]["set"]
            for team in teams_with:
                if team in busy_teams:
                    continue
                gap = None if ours is None or score.get(team) is None else ours - score[team]
                theirs_in_set = sum(1 for (t, c), ids in held.items() if t == team and ids and page_cards(c)
                                    and cards.get(c, {}).get("set") == st)
                if page_cards(ref) and theirs_in_set >= 8 and (gap is None or gap < SCORE_GAP):
                    continue                          # may close its page, and it is within 10 points of us
                est, low = their_gain(team, ref, want, mult=mult, held=held, cards=cards)
                if est <= 0:
                    continue
                out.append({"asset": asset["id"], "give": ref, "want": want, "to": team, "our_gain": gain,
                            "their_est": est, "their_low": low, "our_value_want": v_want,
                            "our_value_give": asset["your_value"]})
    out.sort(key=lambda c: (-c["our_gain"], -c["their_est"]))
    return out


def pick_venue(to: str, venues: dict, top: set) -> str | None:
    for v in PARTNERS:
        x = venues.get(v) or {}
        if x.get("status") == "open" and x.get("owner") not in top and x.get("owner") != to:
            return v
    return None


class Engine:
    def __init__(self, b, *, dry_run=False, mult_fn=vr.hub_mult, events_fn=vr.load_events, state=STATE, book=None,
                 log=log):
        self.b, self.dry_run, self.mult_fn, self.events_fn, self.state_path = b, dry_run, mult_fn, events_fn, state
        self.book, self.log = book, log
        self.values: dict = {}
        self.cards: dict = {}
        self._hub: dict = {}
        self._hub_at = 0.0
        try:
            self.state = json.loads(Path(state).read_text())
        except (OSError, ValueError):
            self.state = {"live": []}

    def our_value(self, card: str, tick: int):
        hit = self.values.get(card)
        if hit is None or tick - hit[1] >= VALUE_TICKS:
            try:
                self.values[card] = (float(self.b.value(card)["your_value"]), tick)
            except (BazaarError, KeyError, TypeError, ValueError):
                return None if hit is None else hit[0]
        return self.values[card][0]

    def run(self, tick: int, tick_seconds: float) -> list[dict]:
        if not self.cards:
            self.cards = vr.card_index(self.b.catalog())
        if time.time() - self._hub_at > 600:
            self._hub, self._hub_at = self.mult_fn() or self._hub, time.time()
        mult = vr.load_mult(self._hub)
        me = self.b.me()
        mine = {o["id"]: o for o in self.b.my_offers().get("offers") or []
                if o.get("maker") == me["id"] and o.get("status", "open") in ("open", "queued")}
        locked = {a["id"] if isinstance(a, dict) else a for o in mine.values()
                  for a in (o.get("give") or {}).get("assets") or []}
        have = {a["ref"] for a in me.get("assets") or [] if a.get("kind") == "card"}
        live = []
        for x in self.state.get("live", []):          # reconcile: still open, filled or gone
            if x["offer"] in mine:
                live.append(x)
                continue
            filled = x["want"] in have
            self.log({"event": "filled" if filled else "expired", **x})
        self.state["live"] = live
        teams = sorted(self.b.leaderboard().get("teams") or [], key=lambda t: -(t.get("score") or 0))
        top = {t["team"] for t in teams[:TOP_N]}
        events = self.events_fn()
        cands = candidates(me=me, locked=locked, our_value=lambda c: self.our_value(c, tick), teams=teams,
                           held=vr.holdings(events), mult=mult, cards=self.cards,
                           skip_want=frozenset(book_buys(self.book) if self.book else book_buys()), busy=live)
        venues = None
        posted = []
        for c in cands:
            if len(self.state["live"]) >= MAX_LIVE or len(posted) >= POSTS_PER_RUN:
                break
            if any(c["to"] == x["to"] or c["want"] == x["want"] or c["asset"] == x["asset"]
                   for x in self.state["live"]):
                continue
            if venues is None:
                venues = {v.get("venue"): v for v in self.b.venues().get("venues") or []}
            venue = pick_venue(c["to"], venues, top)
            if venue is None:
                self.log({"event": "skip", "why": "no open partner venue outside the top 5", **c})
                continue
            ev = {"event": "post", "venue": venue, "tick": tick, **c}
            if self.dry_run:
                self.log({**ev, "dry_run": True})
                self.state["live"].append({**c, "offer": None, "venue": venue, "tick": tick})   # one per team/card
                posted.append(c)
                continue
            try:
                r = self.b.list_offer({"assets": [c["asset"]]}, {"types": [f"card:{c['want']}"]}, venue=venue,
                                      to=c["to"], expires_in_ticks=expires_param(LIFE_TICKS, tick_seconds))
            except BazaarError as e:
                self.log({**ev, "event": "post_failed", "code": e.code, "message": e.message[:120]})
                break
            oid = r.get("id") or (r.get("offer") or {}).get("id")
            self.log({**ev, "offer": oid})
            self.state["live"].append({**c, "offer": oid, "venue": venue, "tick": tick})
            posted.append(c)
        if self.dry_run:
            self.state["live"] = live
        else:
            Path(self.state_path).parent.mkdir(parents=True, exist_ok=True)
            Path(self.state_path).write_text(json.dumps(self.state, indent=1))
        return cands


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], allow_abbrev=False)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="log what it would post, write nothing")
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
                time.sleep(30)
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
