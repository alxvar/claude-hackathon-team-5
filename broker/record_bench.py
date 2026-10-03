"""Market Test recorder. Read-only: GET requests only, never a match, an offer or a message.

While a bench session is live it reads GET /api/broker/book twice a second and appends every distinct book state
(stamped with wall time, tick and game hour) to data/bench/<session>.jsonl, where <session> is `bench-h05.0` for the
bench the schedule puts at game hour 5.0. After each session it saves our /api/me bench fields (bench_efficiency,
bench_points, mm_points, bench_venue, market), every team's `market` from the leaderboard and every venue's mechanism,
at +5 s, +3 min and +7 min (the leaderboard refreshes every few minutes), to the session file and to
data/bench/results.jsonl.

Broker key: env BROKER_KEY (our own venue) if set, else the free stall's key from GET /api/me (`starter_broker_key`;
the stall exists from game hour 3.0). Without a key it still records the results after every scheduled bench and
checks /api/me for a key once a minute. Keys are never printed or written.

    source .env && python3 -m broker.record_bench --once     # status: clock, next bench, key, our bench fields
    source .env && python3 -m broker.record_bench --loop     # run all day (tools/daemons.sh)
    ... --loop --no-book     # results only, when broker.py --record already reads the same key's book

File lines (JSON, one per line, `kind` first): meta (session start: schedule entry, venue fees, runs), book (tick,
t_hours, the whole book minus key fields), match (a match our broker posted, from broker.py --record), end, result.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from broker.common import BENCH_DIR, URL, Bazaar, BazaarError, Broker, Public, TickClock, find_broker_key, scrub  # noqa: E402

RESULT_DELAYS = (5, 180, 420)   # seconds after a session ends: the leaderboard snapshot refreshes every few minutes
ME_FIELDS = ("bench_efficiency", "bench_points", "mm_points", "bench_venue", "market", "score", "rank", "venue")


def run_of(offer_id) -> str:
    return str(offer_id).split("-")[0]


def bench_entries(schedule: dict) -> dict[float, dict]:
    return {float(e["at_hours"]): e for e in schedule.get("upcoming") or [] if e.get("action") == "bench"}


class BenchRecorder:
    """Session detection and file writing, network-free except for the results snapshots (team = Bazaar with the team
    key for /api/me, public = keyless reads). broker.py --record feeds it the books it reads anyway."""

    def __init__(self, out_dir: Path = BENCH_DIR, team: Bazaar | None = None, public: Public | None = None,
                 log=print, clock=time.time):
        self.out_dir, self.team, self.public, self.log, self.now = Path(out_dir), team, public or Public(), log, clock
        self.benches: dict[float, dict] = {}   # cached: an entry leaves `upcoming` once it fires
        self.sched_at = -1e9
        self.now_hours: float | None = None
        self.session: str | None = None
        self.last = None                        # (tick, list fields) last written
        self.empty: tuple | None = None         # (tick, wall) since bench_offers went empty mid-session
        self.closed: set[str] = set()           # sessions whose results are scheduled
        self.due: list[tuple[float, str, int]] = []
        self.pause = time.sleep                  # between the three result reads (tests stub it)

    # ---------------------------------------------------------------- schedule
    def note_schedule(self, schedule: dict):
        self.benches.update(bench_entries(schedule))
        if schedule.get("now_hours") is not None:
            self.now_hours = float(schedule["now_hours"])
        self.sched_at = self.now()

    def refresh_schedule(self, every: float = 600):
        if self.now() - self.sched_at > every:
            try:
                self.note_schedule(self.public.schedule())
            except BazaarError as e:
                self.log(f"schedule: {e.code}")
                self.sched_at = self.now()

    def bench_for(self, hours: float | None) -> float | None:
        """The scheduled bench a moment at game hour `hours` belongs to (started ≤ 6 min later, < 1 h earlier)."""
        if hours is None:
            return None
        c = [a for a in self.benches if a - 0.1 <= hours < a + 1.0]
        return max(c) if c else None

    def bench_near(self, hours: float | None, before: float = 0.05, after: float = 0.6) -> bool:
        return hours is not None and any(a - before <= hours <= a + after for a in self.benches)

    def name_for(self, bench_offers: list) -> str:
        at = self.bench_for(self.now_hours)
        if at is not None:
            return f"bench-h{at:04.1f}"
        runs = "+".join(sorted({run_of(o.get("id")) for o in bench_offers})) or "x"
        return f"bench-{runs}-{time.strftime('%Y%m%d-%H%M')}"

    # ---------------------------------------------------------------- files
    def path(self, session: str) -> Path:
        return self.out_dir / f"{session}.jsonl"

    def write(self, session: str, kind: str, **fields):
        self.out_dir.mkdir(parents=True, exist_ok=True)
        line = {"kind": kind, "t": round(self.now(), 3), **scrub(fields)}
        with self.path(session).open("a") as f:
            f.write(json.dumps(line, separators=(",", ":")) + "\n")

    # ---------------------------------------------------------------- the book
    def observe(self, book: dict, tick: int, t_hours: float | None = None) -> str | None:
        """Record one read of the book. Returns the live session's name, or None between sessions."""
        if t_hours is not None:
            self.now_hours = float(t_hours)
        bench = book.get("bench_offers") or []
        if bench and self.session is None:
            self.refresh_schedule(every=60)
            self.session = self.name_for(bench)
            at = self.bench_for(self.now_hours)
            self.write(self.session, "meta", tick=tick, t_hours=self.now_hours, schedule=self.benches.get(at),
                       venue={k: v for k, v in book.items() if not isinstance(v, (list, dict))},
                       runs=sorted({run_of(o.get("id")) for o in bench}))
            self.log(f"{time.strftime('%H:%M:%S')} bench session {self.session} started at tick {tick}: "
                     f"{len(bench)} offers → {self.path(self.session)}")
        if self.session is None:
            return None
        lists = json.dumps({k: v for k, v in book.items() if isinstance(v, (list, dict))}, sort_keys=True)
        if (tick, lists) != self.last:  # every distinct state, and at least one line per tick
            self.last = (tick, lists)
            self.write(self.session, "book", tick=tick, t_hours=self.now_hours, book=book)
        if bench:
            self.empty = None
        else:
            self.empty = self.empty or (tick, self.now())
            if tick >= self.empty[0] + 2 or self.now() - self.empty[1] > 120:
                self.end(tick)
        return self.session

    def note_match(self, tick: int, sell, buy, price: int):
        if self.session:
            self.write(self.session, "match", tick=tick, sell=sell, buy=buy, price=price)

    def end(self, tick: int):
        s, self.session, self.last, self.empty = self.session, None, None, None
        self.write(s, "end", tick=tick, t_hours=self.now_hours)
        self.log(f"{time.strftime('%H:%M:%S')} bench session {s} ended at tick {tick}; results at "
                 f"+{', +'.join(str(d) for d in RESULT_DELAYS)} s")
        self.schedule_results(s)

    def schedule_results(self, session: str):
        if session in self.closed:
            return
        self.closed.add(session)
        self.due += [(self.now() + d, session, i) for i, d in enumerate(RESULT_DELAYS)]

    def schedule_fallback(self, clock: dict):
        """No book (no key, or --no-book): close each scheduled bench by the clock so its results still get saved."""
        h, secs = clock.get("t_hours"), float(clock.get("tick_seconds") or 30)
        if h is None:
            return
        for at, e in self.benches.items():
            name = f"bench-h{at:04.1f}"
            ticks = int((e.get("params") or {}).get("ticks") or 16)
            if name not in self.closed and name != self.session and at <= h and h >= at + (ticks + 2) * secs / 3600:
                if h - at < 1.0:  # only benches that just finished, not ones we slept through
                    self.write(name, "meta", t_hours=h, schedule=e, note="no book recorded (no broker key or --no-book)")
                    self.schedule_results(name)
                else:
                    self.closed.add(name)

    # ---------------------------------------------------------------- results
    def poll_results(self):
        self.refresh_schedule()
        ready = [d for d in self.due if d[0] <= self.now()]
        self.due = [d for d in self.due if d[0] > self.now()]
        for _, session, n in ready:
            try:
                self.snapshot(session, n)
            except BazaarError as e:
                self.log(f"results for {session} failed ({e.code}); retry in 60 s")
                self.due.append((self.now() + 60, session, n))

    def snapshot(self, session: str, n: int):
        me = self.team.me() if self.team is not None else {}
        s = me.get("score") or {}
        mine = {k: s.get(k) for k in ME_FIELDS}
        mine["venue_detail"] = me.get("venue")
        self.pause(0.3)
        lb = self.public.leaderboard()
        teams = [{k: t.get(k) for k in ("team", "name", "market", "venue", "rank", "score")} for t in lb.get("teams") or []]
        self.pause(0.3)
        venues = [{"venue": v.get("venue"), "owner": v.get("owner"), "status": v.get("status"),
                   "mechanism": (v.get("rules") or {}).get("mechanism"), "starter": v.get("starter"),
                   "fee_bps": v.get("fee_bps"), "fee_per_card": v.get("fee_per_card"), "pairs": v.get("pairs"),
                   "trades": v.get("trades"), "volume": v.get("volume")}
                  for v in (self.public.venues().get("venues") or [])]
        line = dict(session=session, n=n, t_hours=self.now_hours, me=mine, snapshot_tick=lb.get("snapshot_tick"),
                    teams=teams, venues=venues)
        self.write(session, "result", **line)
        self.write("results", "result", **line)
        top = sorted((t for t in teams if t.get("market")), key=lambda t: -t["market"])[:5]
        self.log(f"{time.strftime('%H:%M:%S')} {session} result #{n}: ours bench_efficiency "
                 f"{mine['bench_efficiency']} bench_points {mine['bench_points']} market {mine['market']} · top market "
                 + (", ".join(f"{t['team']} {t['market']}" for t in top) or "none yet"))


# -------------------------------------------------------------------------------------------- CLI

def once(team: Bazaar | None, public: Public, out_dir: Path) -> int:
    """One pass at ≤ 1 request per second: status, and one recorded book state if a session is live."""
    c = public.clock()
    print(f"clock: tick {c.get('tick')} · t_hours {c.get('t_hours')} · {c.get('tick_seconds')} s/tick · "
          f"paused {c.get('paused')} · doors {c.get('doors')} · round {c.get('round')} ({c.get('round_name')})")
    time.sleep(1.0)
    rec = BenchRecorder(out_dir, team, public)
    rec.note_schedule(public.schedule())
    rec.now_hours = c.get("t_hours", rec.now_hours)
    nxt = [f"{a:g}{' (' + e['params'].get('name') + ')' if (e.get('params') or {}).get('name') else ''}"
           f" {(e.get('params') or {}).get('traders')} traders/{(e.get('params') or {}).get('ticks')} ticks"
           for a, e in sorted(rec.benches.items())]
    print("benches scheduled at game hour:", "; ".join(nxt) or "none")
    time.sleep(1.0)
    key, where, me = find_broker_key(team)
    print(f"broker key: {'found (' + where + ')' if key else 'NONE: ' + where}")
    if me:
        s = me.get("score") or {}
        v = scrub(me.get("venue"))
        if isinstance(v, dict):
            v = {k: x for k, x in v.items() if k in ("venue", "name", "rules", "fee_bps", "status")}
        print("our bench fields:", {k: s.get(k) for k in ME_FIELDS}, "· venue:", v)
    time.sleep(1.0)
    lb = public.leaderboard()
    mk = sorted(((t.get("market") or 0, t.get("team")) for t in lb.get("teams") or []), reverse=True)[:5]
    print(f"leaderboard snapshot {lb.get('snapshot_tick')}: top market {mk}")
    if key:
        time.sleep(1.0)
        book = Broker(URL, key, retries=1).book()
        bench = book.get("bench_offers") or []
        print(f"book: fields {sorted(book)} · bench_offers {len(bench)} · offers {len(book.get('offers') or [])}")
        if bench:
            print("  sample bench offer:", json.dumps(scrub(bench[0]))[:300])
            name = rec.observe(book, int(c.get("tick") or 0), c.get("t_hours"))
            print(f"  live session → recorded one state to {rec.path(name)}")
    return 0


def loop(team: Bazaar | None, public: Public, out_dir: Path, hz: float, no_book: bool, max_errors: int) -> int:
    rec = BenchRecorder(out_dir, team, public)
    clock = TickClock(public.clock)
    broker, said, next_key, next_book, failures = None, None, 0.0, 0.0, 0
    print(f"{time.strftime('%H:%M:%S')} recorder up · out {out_dir} · {'results only' if no_book else f'book {hz:g}/s in sessions'}",
          flush=True)
    while True:
        now = time.time()
        try:
            c = clock.read()
            rec.now_hours = c.get("t_hours", rec.now_hours)
            rec.refresh_schedule(every=60 if rec.bench_near(rec.now_hours, 0.1, 0.6) else 600)
            if not no_book and broker is None and now >= next_key:
                key, where, _ = find_broker_key(team)
                next_key = now + 60
                if key:
                    broker = Broker(URL, key, retries=1)
                    print(f"{time.strftime('%H:%M:%S')} broker key from {where}", flush=True)
                elif where != said:
                    print(f"{time.strftime('%H:%M:%S')} {where}: recording results only, checking again every 60 s",
                          flush=True)
                said = where
            hot = rec.session is not None or rec.bench_near(rec.now_hours)
            paused = c.get("paused") or c.get("doors") == "closed"
            if broker is not None and (hot or now >= next_book):
                rec.observe(broker.book(), int(c["tick"]), c.get("t_hours"))
                next_book = now + (30 if paused else 5)
            if broker is None or no_book:
                rec.schedule_fallback(c)
            rec.poll_results()
            failures = 0
        except BazaarError as e:
            failures += 1
            print(f"{time.strftime('%H:%M:%S')} {e.code}: {str(e.message)[:120]} ({failures}/{max_errors})", flush=True)
            if e.status in (401, 403) and broker is not None:  # stall replaced by our venue, key rotated: look again
                broker, next_key = None, 0.0
            if failures >= max_errors:
                print("too many consecutive failures: exiting for the supervisor to restart", flush=True)
                return 1
        time.sleep(1.0 / hz if (rec.session is not None or rec.bench_near(rec.now_hours)) else 2.0)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Market Test recorder (read-only)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--once", action="store_true", help="print status, record one state if a session is live")
    g.add_argument("--loop", action="store_true", help="run until stopped")
    ap.add_argument("--out", type=Path, default=BENCH_DIR)
    ap.add_argument("--hz", type=float, default=2.0, help="book reads per second during a session")
    ap.add_argument("--no-book", action="store_true", help="results only (broker.py --record reads the book)")
    ap.add_argument("--max-errors", type=int, default=30)
    a = ap.parse_args(argv)
    team = Bazaar(URL, os.environ["BAZAAR_KEY"], retries=2) if os.environ.get("BAZAAR_KEY") else None
    if team is None:
        print("BAZAAR_KEY not set: no /api/me (no stall key, no bench fields); reading public routes only")
    if a.once:
        return once(team, Public(), a.out)
    return loop(team, Public(), a.out, a.hz, a.no_book, a.max_errors)


if __name__ == "__main__":
    sys.exit(main())
