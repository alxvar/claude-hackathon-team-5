"""Keyless collector: every public thing in The Bazaar → the hub (Neon), plus a local JSONL copy of the feed.

    uv run python -m hub.collect                 # run forever (host name = this machine's)
    uv run python -m hub.collect --host lucas    # name it explicitly
    uv run python -m hub.collect --once          # one pass, then exit (smoke test)

Why more than one: the public feed returns only the newest 500 events (~15 ticks on Friday, a few minutes on
Sunday) and has no paging, so whatever no collector saw in time is gone. Every collector inserts with the server's
event id as the key, so two of them write the same rows once and either alone keeps the record whole.

No team key: only public routes (feed, leaderboard, venues and their boards, clock, schedule, levels, dealers,
catalog), which have their own per-address limit and never touch the team's 5 requests per second.
Pace follows the server's clock: a third of a tick (4-10 s) while open, 60 s while paused or closed.
If the hub is unreachable, events still go to data/hub/feed-<host>.jsonl and are retried; `hub.import_files`
can backfill that file later.
"""
import argparse
import hashlib
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import psycopg
from psycopg.types.json import Jsonb

from hub.db import ROOT, connect, redact

URL = os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai").rstrip("/")
FEED_LIMIT = 500            # the server's cap
STATE_EVERY_S = 60          # schedule, levels, dealers, venues
CATALOG_EVERY_S = 1800
GAP_MIN_EVENTS = FEED_LIMIT  # a full window whose oldest id is newer than ours = we may have missed events
BOARD_EVERY_TICKS = 2       # Chief 11:40: every venue board every pass hit the 60/s keyless limit (11:36-11:39)


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


class Api:
    """Public GETs only. No key is ever sent."""

    def __init__(self, url=URL, timeout=15.0, spacing=0.15):
        self.url, self.timeout, self.spacing, self._last = url, timeout, spacing, 0.0

    def get(self, path, **query):
        wait = self.spacing - (time.time() - self._last)
        if wait > 0:
            time.sleep(wait)
        q = ("?" + "&".join(f"{k}={v}" for k, v in query.items())) if query else ""
        req = urllib.request.Request(self.url + path + q, headers={"User-Agent": "team5-hub-collector"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return json.load(r)
        finally:
            self._last = time.time()


def poll_seconds(clock: dict) -> float:
    if not clock or clock.get("paused") or clock.get("doors") == "closed":
        return 60.0
    return max(4.0, min(10.0, float(clock.get("tick_seconds") or 30) / 3))


def offer_row_from_event(e: dict) -> tuple:
    o = e["payload"]["offer"]
    return (o["id"], o.get("venue") or e["payload"].get("venue"), o.get("maker"), o.get("to"),
            Jsonb(o.get("give")), Jsonb(o.get("want")), o.get("created_tick"), o.get("expires_tick"), e["tick"])


def board_row(o: dict, venue: str, tick: int) -> tuple:
    return (o["id"], venue, o.get("maker"), o.get("to"), Jsonb(o.get("give")), Jsonb(o.get("want")),
            o.get("created_tick"), o.get("expires_tick"), tick, tick)


def team_rows(lb: dict) -> list:
    snap = lb.get("snapshot_tick")
    return [(snap, t.get("team"), t.get("name"), t.get("rank"), t.get("score"), t.get("negotiating"), t.get("market"),
             t.get("level"), t.get("album_filled"), t.get("album_slots"), t.get("pages_complete"), t.get("luck"),
             t.get("deals"), t.get("venue")) for t in lb.get("teams") or [] if t.get("team")]


def card_rows(catalog: dict) -> list:
    rows = []
    for s in catalog.get("sets") or []:
        for c in s.get("cards") or []:
            rows.append((c["id"], s["id"], c.get("name"), c["rarity"], c.get("book"), c.get("print_run"),
                         c.get("minted"), c.get("page"), c.get("hidden")))
    return rows


SQL_EVENT = """insert into hub.events (id, tick, t_hours, type, scope, actor, payload, source)
               values (%s, %s, %s, %s, %s, %s, %s, %s) on conflict (id) do nothing"""
SQL_OFFER_EVENT = """
insert into hub.offers (id, venue, maker, to_team, give, want, created_tick, expires_tick, first_seen_tick, status)
values (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'open')
on conflict (id) do update set maker = excluded.maker, to_team = excluded.to_team,
    venue = coalesce(hub.offers.venue, excluded.venue), give = coalesce(hub.offers.give, excluded.give),
    want = coalesce(hub.offers.want, excluded.want), created_tick = coalesce(hub.offers.created_tick, excluded.created_tick),
    expires_tick = coalesce(hub.offers.expires_tick, excluded.expires_tick),
    first_seen_tick = least(hub.offers.first_seen_tick, excluded.first_seen_tick)"""
SQL_OFFER_CANCEL = """
insert into hub.offers (id, venue, status, closed_tick, first_seen_tick) values (%s, %s, 'cancelled', %s, %s)
on conflict (id) do update set status = 'cancelled', closed_tick = coalesce(hub.offers.closed_tick, excluded.closed_tick)"""
SQL_OFFER_BOARD = """
insert into hub.offers (id, venue, maker_alias, to_team, give, want, created_tick, expires_tick, first_seen_tick,
                        last_seen_tick, last_seen_at, status)
values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), 'open')
on conflict (id) do update set maker_alias = excluded.maker_alias, last_seen_at = now(),
    last_seen_tick = greatest(hub.offers.last_seen_tick, excluded.last_seen_tick),
    give = coalesce(hub.offers.give, excluded.give), want = coalesce(hub.offers.want, excluded.want),
    status = case when hub.offers.status = 'cancelled' then 'cancelled' else 'open' end"""
SQL_OFFER_GONE = """update hub.offers set status = 'gone', closed_tick = coalesce(closed_tick, %s)
                    where venue = %s and status = 'open' and to_team is null and not (id = any(%s))"""
SQL_TEAM = """insert into hub.team_snapshots (snapshot_tick, team, name, rank, score, negotiating, market, level,
              album_filled, album_slots, pages_complete, luck, deals, venue)
              values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              on conflict (snapshot_tick, team) do update set
                  album_filled = coalesce(excluded.album_filled, hub.team_snapshots.album_filled),
                  album_slots = coalesce(excluded.album_slots, hub.team_snapshots.album_slots),
                  pages_complete = coalesce(excluded.pages_complete, hub.team_snapshots.pages_complete),
                  luck = coalesce(excluded.luck, hub.team_snapshots.luck),
                  level = coalesce(excluded.level, hub.team_snapshots.level),
                  rank = coalesce(excluded.rank, hub.team_snapshots.rank),
                  venue = coalesce(excluded.venue, hub.team_snapshots.venue)"""
SQL_LB = """insert into hub.leaderboard (snapshot_tick, tick, t_hours, round, source, data)
            values (%s, %s, %s, %s, %s, %s) on conflict (snapshot_tick) do nothing"""
SQL_CARD = """insert into hub.cards (ref, set, name, rarity, book, print_run, minted, page, hidden)
              values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
              on conflict (ref) do update set name = excluded.name, rarity = excluded.rarity, book = excluded.book,
                  print_run = excluded.print_run, minted = excluded.minted, page = excluded.page,
                  hidden = excluded.hidden, updated_at = now()"""


class Store:
    """The hub over one writer connection; reconnects on failure."""

    def __init__(self, host: str):
        self.host, self.conn = host, None

    def _c(self) -> psycopg.Connection:
        if self.conn is None or self.conn.closed:
            self.conn = connect("writer")
        return self.conn

    def reset(self):
        try:
            if self.conn is not None:
                self.conn.close()
        except Exception:
            pass
        self.conn = None

    def max_event_id(self) -> int:
        with self._c().cursor() as cur:
            cur.execute("select coalesce(max(id), 0) from hub.events")
            return cur.fetchone()[0]

    def put_events(self, events: list) -> int:
        """Insert events and apply their offer side effects in one transaction; return how many were new."""
        if not events:
            return 0
        c = self._c()
        with c.transaction(), c.cursor() as cur:
            cur.execute("select coalesce(count(*), 0) from hub.events where id = any(%s)", ([e["id"] for e in events],))
            before = cur.fetchone()[0]
            cur.executemany(SQL_EVENT, [(e["id"], e["tick"], e.get("t"), e["type"], e.get("scope"), e.get("actor"),
                                         Jsonb(e.get("payload") or {}), self.host) for e in events])
            listed = [offer_row_from_event(e) for e in events
                      if e["type"] == "offer.listed" and (e.get("payload") or {}).get("offer")]
            if listed:
                cur.executemany(SQL_OFFER_EVENT, listed)
            cancelled = [(e["payload"]["offer"], e["payload"].get("venue"), e["tick"], e["tick"]) for e in events
                         if e["type"] == "offer.cancelled" and isinstance((e.get("payload") or {}).get("offer"), int)]
            if cancelled:
                cur.executemany(SQL_OFFER_CANCEL, cancelled)
        return len(events) - before

    def put_gap(self, after_id: int, before_id: int, tick: int):
        with self._c().cursor() as cur:
            cur.execute("insert into hub.gaps (host, after_id, before_id, tick) values (%s, %s, %s, %s)",
                        (self.host, after_id, before_id, tick))

    def put_leaderboard(self, lb: dict) -> bool:
        c = self._c()
        with c.transaction(), c.cursor() as cur:
            cur.execute(SQL_LB, (lb.get("snapshot_tick"), lb.get("tick"), lb.get("t"), lb.get("round"), self.host,
                                 Jsonb(lb)))
            new = cur.rowcount == 1
            rows = team_rows(lb)
            if rows:
                cur.executemany(SQL_TEAM, rows)
        return new

    def put_board(self, venue: str, offers: list, tick: int):
        c = self._c()
        with c.transaction(), c.cursor() as cur:
            if offers:
                cur.executemany(SQL_OFFER_BOARD, [board_row(o, venue, tick) for o in offers])
            if len(offers) < 500:   # a full page might be truncated: never mark offers gone from it
                cur.execute(SQL_OFFER_GONE, (tick, venue, [o["id"] for o in offers]))

    def put_state(self, kind: str, data: dict, tick):
        h = hashlib.sha1(json.dumps(data, sort_keys=True).encode()).hexdigest()
        c = self._c()
        with c.transaction(), c.cursor() as cur:
            cur.execute("""insert into hub.state (kind, tick, hash, data) values (%s, %s, %s, %s)
                           on conflict (kind) do update set tick = excluded.tick, fetched_at = now(),
                               hash = excluded.hash, data = excluded.data""", (kind, tick, h, Jsonb(data)))
            cur.execute("""insert into hub.state_history (kind, tick, hash, data) values (%s, %s, %s, %s)
                           on conflict (kind, hash) do nothing""", (kind, tick, h, Jsonb(data)))

    def put_cards(self, catalog: dict) -> int:
        rows = card_rows(catalog)
        c = self._c()
        with c.transaction(), c.cursor() as cur:
            cur.executemany(SQL_CARD, rows)
        return len(rows)

    def heartbeat(self, tick, max_id, boards, error, started_at):
        with self._c().cursor() as cur:
            cur.execute("select count(*) from hub.events")
            n = cur.fetchone()[0]
            cur.execute("""insert into hub.heartbeats (host, last_at, last_tick, max_event_id, events_stored, boards,
                                                       last_error, started_at)
                           values (%s, now(), %s, %s, %s, %s, %s, to_timestamp(%s))
                           on conflict (host) do update set last_at = now(), last_tick = excluded.last_tick,
                               max_event_id = excluded.max_event_id, events_stored = excluded.events_stored,
                               boards = excluded.boards, last_error = excluded.last_error,
                               started_at = excluded.started_at""",
                        (self.host, tick, max_id, n, boards, error, started_at))
        return n


class LocalLog:
    """Append-only JSONL copy of every event this host saw: the backup when the hub is down."""

    def __init__(self, path: Path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        self.max_id = 0
        if path.exists():
            with path.open() as f:
                for line in f:
                    try:
                        self.max_id = max(self.max_id, json.loads(line)["id"])
                    except (ValueError, KeyError):
                        continue

    def append(self, events: list):
        fresh = [e for e in sorted(events, key=lambda e: e["id"]) if e["id"] > self.max_id]
        if fresh:
            with self.path.open("a") as f:
                for e in fresh:
                    f.write(json.dumps(e) + "\n")
            self.max_id = fresh[-1]["id"]


class Collector:
    def __init__(self, api: Api, store: Store, local: LocalLog):
        self.api, self.store, self.local = api, store, local
        self.pending = {}              # events not yet confirmed in the hub, by id
        self.seen_max = None           # newest event id known to be stored (hub or this run)
        self.last_snap = None
        self.next_state = self.next_catalog = 0.0
        self.venues = ["rastro"]
        self.board_tick = None         # the tick of the last board sweep
        self.clock = {}
        self.started = time.time()
        self.stats = {"new": 0, "boards": 0, "errors": 0}
        self.last_error = None

    def boards_due(self, tick) -> bool:
        """Sweep the boards on this pass? Once every BOARD_EVERY_TICKS ticks; always when the tick is unknown."""
        return tick is None or self.board_tick is None or tick - self.board_tick >= BOARD_EVERY_TICKS \
            or tick < self.board_tick

    def _err(self, where, e):
        self.stats["errors"] += 1
        msg = f"{where}: {type(e).__name__}: {redact(e)[:160]}"
        self.last_error = msg
        log("error", msg)
        if isinstance(e, psycopg.Error):
            self.store.reset()

    def step(self):
        now = time.time()
        try:
            self.clock = self.api.get("/api/clock")
        except Exception as e:
            self._err("clock", e)
        tick = self.clock.get("tick")

        # Feed: the one thing we can never re-read later.
        try:
            events = self.api.get("/api/feed", limit=FEED_LIMIT).get("events") or []
            had = max(self.local.max_id, self.seen_max or 0, max(self.pending, default=0))
            self.local.append(events)
            for e in events:
                self.pending[e["id"]] = e
            if self.seen_max is None:
                self.seen_max = self.store.max_event_id()
                had = max(had, self.seen_max)
            if events and had and len(events) >= GAP_MIN_EVENTS:
                oldest = min(e["id"] for e in events)
                if oldest > had:
                    log(f"possible gap: newest we had {had}, oldest returned {oldest}")
                    self.store.put_gap(had, oldest, tick)
            batch = [self.pending[i] for i in sorted(self.pending)]
            self.stats["new"] += self.store.put_events(batch)
            if batch:
                self.seen_max = max(self.seen_max or 0, batch[-1]["id"])
            self.pending.clear()
        except Exception as e:
            self._err("feed", e)
            if len(self.pending) > 100_000:   # bounded: the local JSONL still has them all
                for i in sorted(self.pending)[:-50_000]:
                    del self.pending[i]

        try:
            lb = self.api.get("/api/leaderboard")
            if lb.get("snapshot_tick") != self.last_snap:
                self.store.put_leaderboard(lb)
                self.last_snap = lb.get("snapshot_tick")
        except Exception as e:
            self._err("leaderboard", e)

        if now >= self.next_state:
            self.next_state = now + STATE_EVERY_S
            for kind, path in (("clock", "/api/clock"), ("schedule", "/api/schedule"), ("levels", "/api/levels"),
                               ("dealers", "/api/dealers"), ("venues", "/api/venues")):
                try:
                    data = self.clock if kind == "clock" and self.clock else self.api.get(path)
                    self.store.put_state(kind, data, tick)
                    if kind == "venues":
                        self.venues = ["rastro"] + [v["venue"] for v in data.get("venues") or []
                                                    if v.get("status") == "open" and v.get("venue") != "rastro"]
                except Exception as e:
                    self._err(kind, e)
        if now >= self.next_catalog:
            self.next_catalog = now + CATALOG_EVERY_S
            try:
                cat = self.api.get("/api/catalog")
                self.store.put_cards(cat)
                self.store.put_state("catalog", cat, tick)
            except Exception as e:
                self._err("catalog", e)

        # Boards: every open venue, once every BOARD_EVERY_TICKS ticks (the feed carries every offer meanwhile); a 429
        # ends the sweep at once, so the address's other readers (window.sh, the monitors) keep their share.
        n = 0
        if self.boards_due(tick):
            self.board_tick = tick
            for v in self.venues:
                try:
                    offers = self.api.get(f"/api/venues/{v}/offers").get("offers") or []
                    self.store.put_board(v, offers, tick)
                    n += 1
                except urllib.error.HTTPError as e:
                    if e.code == 429:
                        self._err(f"board {v}", e)
                        break
                    if e.code != 404:
                        self._err(f"board {v}", e)
                except Exception as e:
                    self._err(f"board {v}", e)
            self.stats["boards"] = n

        try:
            stored = self.store.heartbeat(tick, self.seen_max, n, self.last_error, self.started)
        except Exception as e:
            self._err("heartbeat", e)
            stored = None
        self.last_error = None
        return stored

    def run(self, once=False):
        last_log = 0.0
        while True:
            t0 = time.time()
            stored = self.step()
            if time.time() - last_log >= 60 or once:
                last_log = time.time()
                log(f"tick {self.clock.get('tick')} · {self.clock.get('doors', '?')}"
                    f"{' paused' if self.clock.get('paused') else ''} · +{self.stats['new']} new events "
                    f"(newest {self.seen_max}, hub {stored}) · {self.stats['boards']} boards · "
                    f"{self.stats['errors']} errors · pending {len(self.pending)}")
                self.stats["new"] = self.stats["errors"] = 0
            if once:
                return
            time.sleep(max(0.5, poll_seconds(self.clock) - (time.time() - t0)))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default=socket.gethostname().split(".")[0])
    ap.add_argument("--once", action="store_true")
    a = ap.parse_args(argv)
    local = LocalLog(ROOT / "data" / "hub" / f"feed-{a.host}.jsonl")
    log(f"hub collector · host {a.host} · {URL} · local copy {local.path.relative_to(ROOT)}")
    Collector(Api(), Store(a.host), local).run(once=a.once)


if __name__ == "__main__":
    sys.exit(main())
