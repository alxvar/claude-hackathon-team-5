"""Team 5's broker for a `board` venue. Deterministic, no LLM, no state outside the process.

Strategies (--strategy):
  auto_clone  exactly what the free stall does on the Market Test (bazaar-kit/starter_broker.py `bench_plan`): in each
              bench run, the best bid against the best ask while they cross, at the midpoint; with a venue fee the
              midpoint is lowered until the buyer also covers the fee (identical to the stall at fee 0).
  v1          auto_clone + one rule about who is about to leave. Traders whose quote relaxed over the last ticks
              (fastest first: the impatient ones) are served first, each with the tightest counterpart it crosses;
              then the rest best bid / best ask; in the last 2 ticks of a run, every pair that can cross is crossed
              (most pairs). Never a pair whose quotes don't cross, and never fewer pairs in a tick than auto_clone
              (if the rule would match fewer, that tick falls back to auto_clone).
Both cross the venue's real offers card by card as the starter broker does (value created on our venue also scores).

    BROKER_KEY=bk_... python3 -m broker.broker --strategy auto_clone             # live, one heartbeat line per tick
    BROKER_KEY=bk_... python3 -m broker.broker --strategy v1 --dry-run           # print the matches, post nothing
    BROKER_KEY=bk_... python3 -m broker.broker --strategy v1 --record            # also record bench sessions

Supervisor-friendly: after --max-errors consecutive failed API calls (or a rejected key) it exits non-zero, so the
`while true` loop in tools/daemons.sh restarts it. Run it from the repo root (`-m broker.broker`).
"""
from __future__ import annotations

import argparse
import math
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

if __package__ in (None, ""):  # run as a file: make `broker` the package, not this module
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from broker.common import URL, BazaarError, Broker, Public, TickClock  # noqa: E402

STRATEGIES = ("auto_clone", "v1")
RUN_TICKS = 16   # a bench run's length (GET /api/schedule → bench params.ticks)
TAIL = 2         # v1 crosses everything in a run's last TAIL ticks
WINDOW = 3       # ticks of quote history v1 uses to see who is relaxing fastest
TAU = 0.0        # v1: "urgent" = relaxing by at least TAU of its quote per tick (set from the sweep below the README)


# ------------------------------------------------------------------------------------------------ pure planning

def run_of(offer_id) -> str:
    """The bench run of an offer ("b12" in "b12-7"), split exactly as the starter broker does."""
    return str(offer_id).split("-")[0]


def make_fee(fee_bps: int = 0, fee_per_card: int = 0):
    """The venue's fee on a price, rounded up, as starter_broker.public_plan charges it."""
    def fee(price: int) -> int:
        return math.ceil(fee_bps * price / 10000) + fee_per_card
    return fee


NO_FEE = make_fee()


def cross_price(ask: int, bid: int, fee=NO_FEE) -> int | None:
    """The stall's midpoint, lowered until price + fee <= bid; None when no price in [ask, bid] works (no cross)."""
    for p in range((ask + bid) // 2, ask - 1, -1):
        if p + fee(p) <= bid:
            return p
    return None


@dataclass(frozen=True)
class Quote:
    id: str
    side: str   # "sell" (asks want.cash) or "buy" (bids give.cash)
    price: int
    pos: int    # position in the book: the stall's tie-break among equal quotes


def bench_runs(offers: list) -> dict[str, tuple[list[Quote], list[Quote]]]:
    """run -> (asks, bids), in book order. A bench seller asks for cash (want.cash), a bench buyer bids it (give.cash)."""
    runs: dict[str, tuple[list, list]] = {}
    for i, o in enumerate(offers):
        asks, bids = runs.setdefault(run_of(o["id"]), ([], []))
        ask = (o.get("want") or {}).get("cash") or 0
        if ask:
            asks.append(Quote(o["id"], "sell", int(ask), i))
        else:
            bids.append(Quote(o["id"], "buy", int((o.get("give") or {}).get("cash") or 0), i))
    return runs


def stall_pairs(asks: list[Quote], bids: list[Quote], fee=NO_FEE) -> list[tuple[Quote, Quote]]:
    """The free stall: lowest ask against highest bid, then the next two, until a pair doesn't cross.
    sorted() is stable, so equal quotes keep book order, as in the stall."""
    out = []
    for a, b in zip(sorted(asks, key=lambda q: q.price), sorted(bids, key=lambda q: -q.price)):
        if cross_price(a.price, b.price, fee) is None:
            break
        out.append((a, b))
    return out


def most_pairs(asks: list[Quote], bids: list[Quote], fee=NO_FEE) -> list[tuple[Quote, Quote]]:
    """As many crossing pairs as possible (sim.max_pairs): each bid, highest first, takes the dearest ask it covers."""
    free, out = sorted(asks, key=lambda q: q.price), []
    for b in sorted(bids, key=lambda q: -q.price):
        fit = [a for a in free if cross_price(a.price, b.price, fee) is not None]
        if fit:
            free.remove(fit[-1])
            out.append((fit[-1], b))
    return out


def relax_speed(hist: dict[int, int], tick: int, side: str, window: int = WINDOW) -> float:
    """How fast a trader's quote moved toward the other side over the last `window` ticks, as a share of its quote
    per tick (0 = firm or not seen long enough). Impatient traders relax fastest, then leave."""
    past = [t for t in hist if tick - window <= t < tick]
    if tick not in hist or not past:
        return 0.0
    t0 = min(past)
    move = hist[tick] - hist[t0] if side == "buy" else hist[t0] - hist[tick]
    return max(0.0, move / (tick - t0) / max(1, hist[tick]))


def v1_pairs(asks: list[Quote], bids: list[Quote], fee, urgent: dict[str, float]) -> list[tuple[Quote, Quote]]:
    """Urgent traders first (fastest relaxing first), each with an urgent counterpart if one crosses, else the
    tightest one (a bid takes the dearest ask it covers, an ask the cheapest bid covering it: the counterpart other
    traders could least use); then the rest best bid / best ask, as the stall."""
    free_a, free_b, out = list(asks), list(bids), []
    for q in sorted((q for q in asks + bids if q.id in urgent), key=lambda q: (-urgent[q.id], q.pos)):
        if q.side == "buy" and q in free_b:
            fit = [a for a in free_a if cross_price(a.price, q.price, fee) is not None]
            if fit:
                a = min(fit, key=lambda a: (a.id not in urgent, -a.price, a.pos))
                free_a.remove(a)
                free_b.remove(q)
                out.append((a, q))
        elif q.side == "sell" and q in free_a:
            fit = [b for b in free_b if cross_price(q.price, b.price, fee) is not None]
            if fit:
                b = min(fit, key=lambda b: (b.id not in urgent, b.price, b.pos))
                free_a.remove(q)
                free_b.remove(b)
                out.append((q, b))
    return out + stall_pairs(free_a, free_b, fee)


def ids(pairs) -> set[str]:
    return {q.id for pair in pairs for q in pair}


def v1_tick(asks: list[Quote], bids: list[Quote], fee, speed: dict[str, float], tau: float) -> list[tuple[Quote, Quote]]:
    """v1 for one run and one tick, guarded against the stall. Urgent = relaxing at >= tau of its quote per tick.
    The urgent-first pairs replace the stall's only if they match at least as many pairs, every trader they add is
    urgent, and every trader they leave out is relaxing but not urgent (it stays, and its quote keeps improving).
    A firm trader (never relaxes, so never crosses anything new) or a newcomer is never displaced."""
    base = stall_pairs(asks, bids, fee)
    urgent = {q.id: speed[q.id] for q in asks + bids if speed.get(q.id, 0.0) > 0 and speed[q.id] >= tau}
    if not urgent:
        return base
    cand = v1_pairs(asks, bids, fee, urgent)
    added, dropped = ids(cand) - ids(base), ids(base) - ids(cand)
    if (len(cand) >= len(base) and all(i in urgent for i in added)
            and all(i not in urgent and speed.get(i, 0.0) > 0 for i in dropped)):
        return cand
    return base


class Planner:
    """Plans one tick of bench matches for a strategy, remembering each offer's quotes (v1 needs the history).
    Feed it every tick's book in order; offers already matched must not be in the book it gets."""

    def __init__(self, strategy: str = "auto_clone", run_ticks: int = RUN_TICKS, tail: int = TAIL,
                 window: int = WINDOW, bench_fee: bool = True, tau: float = TAU):
        if strategy not in STRATEGIES:
            raise ValueError(f"unknown strategy {strategy!r}; one of {STRATEGIES}")
        self.strategy, self.run_ticks, self.tail, self.window, self.bench_fee = strategy, run_ticks, tail, window, bench_fee
        self.tau = tau
        self.hist: dict[str, dict[int, int]] = {}
        self.run_start: dict[str, int] = {}

    def bench_plan(self, book: dict, tick: int) -> list[tuple[str, str, int]]:
        """[(sell id, buy id, price)] for this tick's bench offers."""
        fee = make_fee(book.get("fee_bps") or 0, book.get("fee_per_card") or 0) if self.bench_fee else NO_FEE
        plan = []
        for run, (asks, bids) in bench_runs(book.get("bench_offers") or []).items():
            start = self.run_start.setdefault(run, tick)
            for q in asks + bids:
                self.hist.setdefault(q.id, {})[tick] = q.price
            base = stall_pairs(asks, bids, fee)
            if self.strategy == "auto_clone":
                pairs = base
            elif tick - start >= self.run_ticks - self.tail:
                pairs = most_pairs(asks, bids, fee)
            else:
                speed = {q.id: relax_speed(self.hist[q.id], tick, q.side, self.window) for q in asks + bids}
                pairs = v1_tick(asks, bids, fee, speed, self.tau)
            if len(pairs) < len(base):
                pairs = base
            plan += [(a.id, b.id, cross_price(a.price, b.price, fee)) for a, b in pairs]
        return plan


def public_plan(book: dict, limit: int = 10) -> list[tuple]:
    """The venue's real offers, card by card, as starter_broker.public_plan: the lowest ask against the highest bid for
    that card, at the midpoint lowered until the buyer can also pay the fee. At most `limit` matches per tick."""
    fee, plan = make_fee(book.get("fee_bps") or 0, book.get("fee_per_card") or 0), []
    offers = book.get("offers") or []
    try:
        bids = sorted((o for o in offers if o["give"].get("cash") and len(o["want"].get("types") or []) == 1),
                      key=lambda o: -o["give"]["cash"])
        sells = sorted((o for o in offers if len(o["give"].get("assets") or []) == 1 and o["want"].get("cash")),
                       key=lambda o: o["want"]["cash"])
        for s in sells:
            ask, card = s["want"]["cash"], "{kind}:{ref}".format(**s["give"]["assets"][0])
            b = next((b for b in bids if b["want"]["types"] == [card] and b.get("maker") != s.get("maker")
                      and cross_price(ask, b["give"]["cash"], fee) is not None), None)
            if b:
                bids.remove(b)
                plan.append((s["id"], b["id"], cross_price(ask, b["give"]["cash"], fee)))
    except (KeyError, TypeError, AttributeError) as e:  # an offer shape we don't know: cross nothing rather than crash
        print(f"public offers: unexpected shape ({e!r}), skipped", flush=True)
    return plan[:limit]


# ------------------------------------------------------------------------------------------------ live loop

class Stats:
    def __init__(self):
        self.reset()

    def reset(self):
        self.bench = self.runs = self.public = self.planned = self.posted = self.refused = self.errors = 0


def run(client, clock: TickClock, planner: Planner, *, dry_run: bool = False, max_errors: int = 20,
        hz: float = 2.0, recorder=None, out=print, sleep=time.sleep, max_loops: int | None = None) -> int:
    """The broker loop. Returns (or exits with) a non-zero code after `max_errors` consecutive API failures."""
    seen, posted, st, beat_tick, failures, loops = None, set(), Stats(), None, 0, 0
    mode = planner.strategy + (" DRY-RUN" if dry_run else "")
    out(f"{time.strftime('%H:%M:%S')} broker up · {mode} · run_ticks {planner.run_ticks} · bench fee "
        f"{'venue fee' if planner.bench_fee else 'none'}", flush=True)
    while max_loops is None or loops < max_loops:
        loops += 1
        try:
            c = clock.read()
            tick = int(c["tick"])
            book = client.book()
            failures = 0
        except BazaarError as e:
            failures += 1
            st.errors += 1
            out(f"{time.strftime('%H:%M:%S')} read failed ({e.code}: {str(e.message)[:100]}) {failures}/{max_errors}",
                flush=True)
            if e.status in (401, 403) or e.code in ("bad_key", "unauthorized"):
                out("broker key rejected: exiting (check BROKER_KEY / the venue)", flush=True)
                return 2
            if failures >= max_errors:
                out("too many consecutive API failures: exiting for the supervisor to restart", flush=True)
                return 1
            sleep(1.0)
            continue
        if beat_tick is not None and tick != beat_tick:  # heartbeat: one line per finished tick
            out(f"{time.strftime('%H:%M:%S')} tick {beat_tick} · {mode} · bench {st.bench} offers/{st.runs} runs · "
                f"public {st.public} · planned {st.planned} · posted {st.posted} · refused {st.refused} · "
                f"errors {st.errors}", flush=True)
            st.reset()
        beat_tick = tick
        if recorder is not None:
            try:
                recorder.observe(book, tick, c.get("t_hours"))
                recorder.poll_results()
            except Exception as e:  # recording never stops the broker
                out(f"recorder: {e!r}"[:200], flush=True)
        bench = [o for o in (book.get("bench_offers") or []) if o.get("id") not in posted]
        public = [o for o in (book.get("offers") or []) if o.get("id") not in posted]
        st.bench, st.public = len(bench), len(public)
        st.runs = len({run_of(o["id"]) for o in bench})
        state = (tick, tuple((o["id"], (o.get("want") or {}).get("cash"), (o.get("give") or {}).get("cash"))
                             for o in bench), tuple(o.get("id") for o in public))
        if state != seen:  # plan once per state of the book, so a refused match is not retried every read
            seen = state
            view = {**book, "bench_offers": bench, "offers": public}
            try:
                plan = planner.bench_plan(view, tick) + public_plan(view)
            except Exception as e:  # an unexpected book shape: log it, count it, keep the loop alive
                plan = []
                failures += 1
                st.errors += 1
                out(f"plan failed: {e!r}"[:200], flush=True)
                if failures >= max_errors:
                    return 1
            st.planned += len(plan)
            for sell, buy, price in plan:
                if dry_run:
                    out(f"  tick {tick} DRY {sell} x {buy} at {price}", flush=True)
                    continue
                try:
                    client.match(sell, buy, price)
                    posted.update((sell, buy))
                    st.posted += 1
                    if recorder is not None:
                        recorder.note_match(tick, sell, buy, price)
                except BazaarError as e:  # taken since the read, a shape the venue cannot cross, a fee we missed
                    st.refused += 1
                    out(f"  tick {tick}: {sell} x {buy} at {price} refused ({e.code}: {str(e.message)[:80]})",
                        flush=True)
                    if e.status == 0 or e.status >= 500:
                        failures += 1
                        if failures >= max_errors:
                            return 1
        sleep(1.0 / hz)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--strategy", choices=STRATEGIES, default="auto_clone")
    ap.add_argument("--dry-run", action="store_true", help="print the matches it would post; post nothing")
    ap.add_argument("--record", action="store_true", help="also record bench sessions to data/bench/ (then don't "
                    "run record_bench.py's book polling on the same key)")
    ap.add_argument("--run-ticks", type=int, default=RUN_TICKS)
    ap.add_argument("--no-bench-fee", action="store_true", help="ignore the venue fee on bench matches (as the "
                    "starter broker does); identical at fee 0")
    ap.add_argument("--max-errors", type=int, default=20)
    ap.add_argument("--hz", type=float, default=2.0, help="book reads per second (the starter reads twice)")
    a = ap.parse_args(argv)
    key = os.environ.get("BROKER_KEY")
    if not key:
        print("BROKER_KEY is not set: the broker needs our venue's key (open_venue returns it once)", flush=True)
        return 2
    client = Broker(URL, key, retries=2)
    recorder = None
    if a.record:
        from broker.common import Bazaar
        from broker.record_bench import BenchRecorder
        team = Bazaar(URL, os.environ["BAZAAR_KEY"], retries=2) if os.environ.get("BAZAAR_KEY") else None
        recorder = BenchRecorder(team=team)
    clock = TickClock(Public().clock)
    planner = Planner(a.strategy, run_ticks=a.run_ticks, bench_fee=not a.no_bench_fee)
    return run(client, clock, planner, dry_run=a.dry_run, max_errors=a.max_errors, hz=a.hz, recorder=recorder)


if __name__ == "__main__":
    sys.exit(main())
