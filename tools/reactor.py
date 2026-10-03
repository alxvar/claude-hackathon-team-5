"""Fast reactor (Chief, Sat 21:55): the public event stream instead of 2-minute board sweeps. Read-only: it never
trades; the Operator executes.

It reads /api/events/stream (SSE, keyless: it takes none of the team key's 6 streams) and, on every offer.listed:
1. BUY: an ask (cards for cash, open or addressed to us) by a TEAM (a dealer deal never scores above 0) that we may
   take: not on our venue (RULES) or a rival-owned one (it would credit a rival's market), not from a rival seller
   (policy: their gain unknown), with gain = our value (GET /api/me/value, team key, cached VALUE_TTL_S, at most one
   lookup per second) − price − taker fee (tools/bargains.py) >= MIN_GAIN → a `BUY <offer> ...` line and
   notify("operator"); `BUY-NOCASH` instead when the cost would take cash below the floor (GUARDRAIL 21:02: 350,
   the Sunday CHA reserve).
2. DENY: an ask of the LAST missing page card of a watched rival (DENY_TEAMS: t06, t14, t10 per GUARDRAIL 19:05, plus
   the live top 3; 9/10 from the feed's lower bound + run/known_holdings.json, tools/matchmaker.py, refreshed every
   DENY_EVERY_S) → a `DENY <offer> ...` line (cap 35 P incl. fee flagged) and notify("operator"); a watched team's own
   bid for its last card is a `HUNT` line (log only).
3. V10: every listing on v10 → a `V10 ...` line and data/v10_listings.jsonl for the Market.
When the stream drops it polls /api/feed every POLL_S and reconnects every RECONNECT_S; a reconnect backfills from
/api/feed by event id, so nothing is handled twice or missed. Watch it: `tail -n 0 -F logs/reactor.log | grep
--line-buffered -E '^(BUY|DENY) '`.

    source .env && python3 -u tools/reactor.py        # tools/daemons.sh start reactor
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
sys.path.insert(0, str(ROOT / "tools"))
from bazaar_sdk import Bazaar, BazaarError, _Http  # noqa: E402
import bargains  # noqa: E402
import matchmaker as mm  # noqa: E402
import opportunities as op  # noqa: E402
import policy  # noqa: E402
import v10_radar as vr  # noqa: E402

try:
    from notify import notify as _notify
except Exception:  # noqa: BLE001
    _notify = None

URL = os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai")
ME, HOUSE, V10 = "t05", bargains.HOUSE, "v10"
V10_OUT = ROOT / "data" / "v10_listings.jsonl"
MIN_GAIN = 15
CASH_FLOOR = int(os.environ.get("REACTOR_CASH_FLOOR", 350))
DENY_TEAMS = tuple(t for t in os.environ.get("DENY_TEAMS", "t06,t14,t10").split(",") if t)
DENY_CAP, SCORE_CAP = 35, bargains.SCORE_CAP
VALUE_TTL_S, VALUE_GAP_S, ME_TTL_S, VENUES_TTL_S, TEAMS_TTL_S, DENY_EVERY_S = 300, 1.0, 60, 300, 120, 300
POLL_S, RECONNECT_S, READ_TIMEOUT_S = 10, 60, 120
HEARTBEAT_TICKS = 10      # a `reactor: tick ...` line every 10 ticks: silence means no event, not a dead stream


def sse(lines):
    """Events from SSE lines (bytes or str): a JSON `data:` per event; comments and `hello` without an id skipped."""
    data = []
    for raw in lines:
        line = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else raw
        line = line.rstrip("\r\n")
        if not line:
            if data:
                try:
                    e = json.loads("\n".join(data))
                except ValueError:
                    e = None
                data = []
                if isinstance(e, dict) and e.get("id") is not None:
                    yield e
            continue
        if line.startswith("data:"):
            data.append(line[5:].lstrip())


def open_stream(url: str = URL, timeout: float = READ_TIMEOUT_S):
    req = urllib.request.Request(url.rstrip("/") + "/api/events/stream", headers={"Accept": "text/event-stream"})
    return sse(urllib.request.urlopen(req, timeout=timeout))


def ask_cards(o: dict, me: str = ME) -> list | None:
    """The card refs of an ask we may take (cards for cash only, open or addressed to us), else None."""
    give, want = o.get("give") or {}, o.get("want") or {}
    assets = [a for a in give.get("assets") or [] if isinstance(a, dict)]
    if (not assets or give.get("cash") or not want.get("cash") or want.get("assets") or want.get("types")
            or want.get("cards") or o.get("to") not in (None, me)
            or any(a.get("kind", "card") != "card" or not a.get("ref") for a in assets)):
        return None
    return [a["ref"] for a in assets]


def bid_card(o: dict) -> str | None:
    give, want = o.get("give") or {}, o.get("want") or {}
    return bargains.wanted_card(want) if give.get("cash") and not give.get("assets") else None


class Reactor:
    def __init__(self, api, pub, *, notifier=_notify, log=print, now=time.time, sleep=time.sleep,
                 cash_floor: int = CASH_FLOOR, min_gain: float = MIN_GAIN, deny_teams=DENY_TEAMS,
                 v10_out: Path = V10_OUT, targets_fn=None):
        self.api, self.pub, self.notifier, self.log, self.now, self.sleep = api, pub, notifier, log, now, sleep
        self.cash_floor, self.min_gain, self.deny_teams, self.v10_out = cash_floor, min_gain, set(deny_teams), v10_out
        self.targets_fn = targets_fn or self._targets_from_feed
        self.last_id: int | None = None
        self.tick, self.tick_seconds = None, 30.0
        self.seen: set = set()
        self._values: dict = {}
        self._value_at = 0.0
        self._me, self._me_at = None, 0.0
        self._venues, self._venues_at = {}, 0.0
        self._teams, self._teams_at = [], 0.0
        self._targets, self._targets_at = {}, -1e9
        self.counts = {"listings": 0, "BUY": 0, "BUY-NOCASH": 0, "DENY": 0, "HUNT": 0, "V10": 0}

    # ------------------------------------------------------------------------------------------------ cached reads
    def value(self, ref: str) -> float | None:
        hit = self._values.get(ref)
        if hit and self.now() - hit[1] < VALUE_TTL_S:
            return hit[0]
        wait = VALUE_GAP_S - (self.now() - self._value_at)
        if wait > 0:
            self.sleep(wait)                          # at most one value lookup per second (Chief 21:55)
        self._value_at = self.now()
        try:
            v = float(self.api.value(ref)["your_value"])
        except (BazaarError, KeyError, TypeError, ValueError, OSError):
            return None
        self._values[ref] = (v, self.now())
        return v

    def cash(self) -> float | None:
        if self._me is None or self.now() - self._me_at > ME_TTL_S:
            try:
                self._me, self._me_at = self.api.me(), self.now()
            except (BazaarError, OSError):
                return None if self._me is None else self._me.get("cash")
        return self._me.get("cash")

    def venues(self) -> dict:
        if self.now() - self._venues_at > VENUES_TTL_S:
            try:
                self._venues = {v["venue"]: v for v in self.pub._call("GET", "/api/venues").get("venues") or []}
                self._venues_at = self.now()
            except (BazaarError, OSError):
                pass
        return self._venues

    def teams(self) -> list:
        if self.now() - self._teams_at > TEAMS_TTL_S:
            try:
                self._teams = self.pub._call("GET", "/api/leaderboard").get("teams") or []
                self._teams_at = self.now()
            except (BazaarError, OSError):
                pass
        return self._teams

    def rivals(self) -> set:
        teams = self.teams()
        return (policy.rivals(teams, ME) if teams else set()) | set(policy.RIVALS)

    def targets(self) -> dict:
        """card → [(team, set)]: the last missing page card of each watched team at 9/10."""
        if self.now() - self._targets_at > DENY_EVERY_S:
            top3 = [t["team"] for t in policy.ranked(self.teams()) if t["team"] != ME][:3]
            watch = set(self.deny_teams) | set(top3)
            try:
                self._targets = self.targets_fn(watch)
            except Exception as e:  # noqa: BLE001  the stream keeps running on the last list
                self.log(f"reactor: deny list not refreshed ({e!r})")
            self._targets_at = self.now()
        return self._targets

    def _targets_from_feed(self, watch: set) -> dict:
        """Watched teams one card from a page that can still score (matchmaker.page_open: the server's
        pages_complete beats the feed; Chief 21:45, t10's RET had closed at snapshot 1040)."""
        cat = mm.load_catalog()
        cards, pg = vr.card_index(cat), mm.pages(cat)
        known = mm.load_known()
        n, last, _ = mm.counts(vr.load_events(mm.FEED), cards)
        prog = mm.progress(mm.apply_known(n, known, pg), pg)
        lb = {t["team"]: t for t in self.teams()} or None
        out: dict = {}
        for (team, st), have in prog.items():
            if team in watch and len(have) == len(pg[st]["cards"]) - 1:
                card = next(c for c in pg[st]["cards"] if c not in have)
                ok, why = mm.page_open(team, st, card, prog=prog, pg=pg, lb=lb, last=last, tick=self.tick, known=known)
                if ok:
                    out.setdefault(card, []).append((team, st))
                else:
                    self.log(f"reactor: no DENY watch on {card} for {team} {st}: {why}")
        return out

    def until(self, expires_tick) -> str:
        if expires_tick is None or self.tick is None:
            return "?"
        return time.strftime("%H:%M", time.localtime(self.now() + max(0, expires_tick - self.tick) * self.tick_seconds))

    # ---------------------------------------------------------------------------------------------------- events
    def handle(self, e: dict) -> list[str]:
        """One feed event → the lines it produced (BUY / BUY-NOCASH / DENY / HUNT / V10)."""
        if e.get("id") is not None:
            if self.last_id is not None and e["id"] <= self.last_id:
                return []
            self.last_id = e["id"]
        if isinstance(e.get("tick"), int):
            self.tick = e["tick"]
        p = e.get("payload") if isinstance(e.get("payload"), dict) else {}
        typ = e.get("type")
        if typ == "tick":
            self.tick_seconds = float(p.get("tick_seconds") or self.tick_seconds)
            if self.tick is not None and self.tick % HEARTBEAT_TICKS == 0:
                self.log(f"reactor: tick {self.tick} · last event {self.last_id} · "
                         + " · ".join(f"{k} {v}" for k, v in self.counts.items()))
        elif typ == "settlement" and ME in (p.get("parties") or []):
            self._values.clear()                      # our holdings moved: values and cash change
            self._me_at = 0.0
        elif typ and typ.startswith("venue."):
            self._venues_at = 0.0
        elif typ == "offer.listed":
            o = p.get("offer") or {}
            o = {**o, "venue": o.get("venue") or p.get("venue")}
            return self.on_listing(o, e)
        return []

    def on_listing(self, o: dict, e: dict) -> list[str]:
        out = []
        maker = o.get("maker") or e.get("actor")
        if o.get("id") is None or o["id"] in self.seen or maker == ME:
            return out
        self.seen.add(o["id"])
        self.counts["listings"] += 1
        if o.get("venue") == V10:
            out.append(self.v10_line(o, maker))
        refs = ask_cards(o)
        if refs is None:
            card = bid_card(o)
            for team, st in (self.targets().get(card) or []) if card else []:
                if team == maker:
                    out.append(self.emit(f"HUNT {o['id']} · {maker} bids {o['give'].get('cash')} P for {card}, the last "
                                         f"{st} card it needs, on {o.get('venue')} (until {self.until(o.get('expires_tick'))})"))
            return out
        if not op.is_team(maker):
            return out                                # a dealer's ask: a dealer deal scores at most 0
        venues = self.venues()
        v = venues.get(o.get("venue"))
        bps, per = bargains.venue_fee(v) if o.get("venue") != HOUSE else bargains.HOUSE_FEE
        price = int(o["want"]["cash"])
        f = bargains.fee(price, len(refs), bps, per)
        for card in refs:
            for team, st in self.targets().get(card) or []:
                if team != maker:
                    out.append(self.deny(o, card, team, st, price, f, maker))
        line = self.buy(o, refs, price, f, maker, v)
        if line:
            out.append(line)
        return out

    def buy(self, o, refs, price, f, maker, v) -> str | None:
        owner = (v or {}).get("owner")
        riv = self.rivals()
        if o.get("venue") == V10 or owner == ME:
            return None                               # never on our own venue (RULES)
        if owner in riv or maker in riv:
            return None                               # a rival's market or a rival seller (its gain unknown)
        values = [self.value(r) for r in refs]
        if any(x is None for x in values):
            return None
        value = sum(values)
        gain = round(value - price - f, 1)
        if gain < self.min_gain:
            return None
        cash, need = self.cash(), price + f
        fits = cash is not None and cash - need >= self.cash_floor
        tag = "BUY" if fits else "BUY-NOCASH"
        line = (f"{tag} {o['id']} · {'+'.join(refs)} on {o.get('venue')} at {price} + fee {f} = {need} · our value "
                f"{value:g} → gain +{gain:g} (scores +{min(gain, SCORE_CAP):g}) · seller {maker} · cash {cash} → "
                f"{None if cash is None else cash - need} (floor {self.cash_floor}) · until {self.until(o.get('expires_tick'))}")
        if fits and self.notifier:
            self.notifier("operator", f"BUY {o['id']}: {'+'.join(refs)} at {price} (+{gain:g})", "→ " + line,
                          priority=4, tags=["moneybag"])     # "→ ": notify's stderr echo must not match ^BUY
        return self.emit(line)

    def deny(self, o, card, team, st, price, f, maker) -> str:
        v = self.value(card)
        gain = None if v is None else round(v - price - f, 1)
        within = price + f <= DENY_CAP
        line = (f"DENY {o['id']} · {card} is the last {st} card {team} needs · ask on {o.get('venue')} at {price} + fee "
                f"{f} by {maker} · {'within' if within else 'OVER'} the {DENY_CAP} P cap · our value "
                f"{'?' if v is None else f'{v:g}'} (gain {'?' if gain is None else f'{gain:+g}'}) · until "
                f"{self.until(o.get('expires_tick'))}")
        if self.notifier:
            self.notifier("operator", f"DENY {o['id']}: {card} last for {team}", "→ " + line, priority=4,
                          tags=["no_entry"])
        return self.emit(line)

    def v10_line(self, o: dict, maker) -> str:
        rec = {"t": round(self.now()), "tick": self.tick, "offer": o["id"], "maker": maker, "to": o.get("to"),
               "give": o.get("give"), "want": o.get("want"), "expires_tick": o.get("expires_tick")}
        try:
            self.v10_out.parent.mkdir(parents=True, exist_ok=True)
            with self.v10_out.open("a") as fh:
                fh.write(json.dumps(rec) + "\n")
        except OSError:
            pass
        give, want = o.get("give") or {}, o.get("want") or {}
        what = lambda x: "+".join([a.get("ref", "?") for a in x.get("assets") or [] if isinstance(a, dict)]  # noqa: E731
                                  + [t[5:] for t in x.get("types") or [] if t.startswith("card:")]
                                  + ([f"{x['cash']} P"] if x.get("cash") else [])) or "-"
        return self.emit(f"V10 {o['id']} · {maker}{' → ' + o['to'] if o.get('to') else ''} gives {what(give)} for "
                         f"{what(want)}")

    def emit(self, line: str) -> str:
        tag = line.split(" ", 1)[0]
        if tag in self.counts:
            self.counts[tag] += 1
        self.log(line)
        return line

    # ------------------------------------------------------------------------------------------------------ loop
    def backfill(self, events) -> int:
        """Feed events (any order) after the last one handled; on the first call only marks where we are."""
        evs = sorted((x for x in events or [] if x.get("id") is not None), key=lambda x: x["id"])
        if self.last_id is None:
            if evs:
                self.last_id = evs[-1]["id"]
                self.tick = evs[-1].get("tick", self.tick)
            return 0
        n = 0
        for x in evs:
            if x["id"] > self.last_id:
                self.handle(x)
                n += 1
        return n

    def run(self, stream_fn, poll_fn, *, loops=None) -> None:
        i = 0
        while loops is None or i < loops:
            i += 1
            try:
                self.backfill(poll_fn())
                self.log(f"reactor: stream open (last event {self.last_id})")
                for e in stream_fn():
                    self.handle(e)
                raise ConnectionError("stream ended")
            except Exception as ex:  # noqa: BLE001  any drop: poll until the next reconnect
                self.log(f"reactor: stream down ({ex!r:.120}): polling /api/feed every {POLL_S} s, reconnect in "
                         f"{RECONNECT_S} s")
                end = self.now() + RECONNECT_S
                while self.now() < end:
                    try:
                        self.backfill(poll_fn())
                    except Exception as pe:  # noqa: BLE001
                        self.log(f"reactor: poll failed ({pe!r:.120})")
                    self.sleep(POLL_S)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], allow_abbrev=False)
    ap.add_argument("--cash-floor", type=int, default=CASH_FLOOR)
    ap.add_argument("--min-gain", type=float, default=MIN_GAIN)
    args = ap.parse_args(argv)
    api = Bazaar(URL, os.environ["BAZAAR_KEY"], wait_on_tick=False)
    pub = _Http(URL, {}, 15.0, False, 0)
    r = Reactor(api, pub, cash_floor=args.cash_floor, min_gain=args.min_gain)
    r.log(f"reactor: watching offer.listed (BUY gain >= {args.min_gain:g}, cash floor {args.cash_floor}; DENY for "
          f"{', '.join(sorted(r.deny_teams))} + the live top 3; V10 listings → {V10_OUT.name})")
    r.run(open_stream, lambda: (pub._call("GET", "/api/feed", query={"limit": 150}) or {}).get("events") or [])


if __name__ == "__main__":
    main()
