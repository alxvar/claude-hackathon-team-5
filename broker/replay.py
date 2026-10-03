"""Replay Market Test sessions through broker strategies, offline, and score them as broker/sim.py does:
realised gains between the traders' limits / the possible gains (the k highest values against the k lowest costs,
per run).

Sessions come from the recorder (data/bench/*.jsonl) or from the simulator (--sim). Sim sessions carry the TRUE
limits. Recorded ones don't: each trader's limit is proxied by its most relaxed quote (a buyer's highest bid, a
seller's lowest ask), so a recorded score is a "proxy" efficiency, comparable between strategies on the same file,
not equal to the server's bench_efficiency (record_bench saves that next to it: compare the two after each bench).

    python3 -m broker.replay data/bench/bench-h05.0.jsonl                         # every strategy on one session
    python3 -m broker.replay data/bench/bench-*.jsonl --compare auto_clone v1     # paired comparison
    python3 -m broker.replay --sim default --seeds 200 --compare auto_clone v1    # 200 simulated sessions
    python3 -m broker.replay --sim all --seeds 200 --compare auto_clone v1        # every trader model
    python3 -m broker.replay --sim hard-12 --seeds 3 --write data/bench/sim       # sim sessions as recorder files
    python3 -m broker.replay FILE --strategy v1 -v                                # the matches, tick by tick

Censoring (--censor): a recorded trader that our broker (or the stall) matched vanishes from the book, so its later
quotes are unknown. `leave` (default) lets a strategy match a trader only on ticks it was really in the book;
`hold` keeps a trader the recording shows as matched (a `match` line or a settlement naming it) in the book, at its
last quote, until the run ends. A file recorded on the free stall (an `auto` venue: the engine crosses first) shows
the book after the stall's matching; use it to calibrate sim.Model more than to rank strategies.
"""
from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from broker import sim
from broker.broker import RUN_TICKS, STRATEGIES, Planner, make_fee, run_of

# Trader models. default = the schedule's bench (10 traders, 16 ticks). hard-12 = the hour-16.0 bench ("firmer and more
# impatient traders", 12 traders, 16 ticks): the firm/impatient shares are OUR guess, to calibrate on the real one.
MODELS = {
    "default": sim.Model(),
    "hard-12": sim.Model(traders=12, impatient=0.7, firm=0.4),
    "light-shading": sim.Model(shade=(0.02, 0.15)),
    "heavy-shading": sim.Model(shade=(0.15, 0.5)),
    "mostly-impatient": sim.Model(impatient=0.7),
    "mostly-patient": sim.Model(impatient=0.1),
    "many-firm": sim.Model(firm=0.5),
    "no-firm": sim.Model(firm=0.0),
    "20-traders": sim.Model(traders=20),
    # bench 3.0 (stall leftovers): ~20 ids, staggered arrivals, asks up to 129, short lives
    "staggered-20": sim.Model(traders=20, arrive=(0, 10), lo_hi=(20, 110), shade=(0.1, 0.4), early_leave=(2, 5), late_leave=(5, 12)),
    "staggered-20-firm": sim.Model(traders=20, arrive=(0, 10), lo_hi=(20, 110), shade=(0.1, 0.4), early_leave=(2, 5), late_leave=(5, 12), firm=0.4, impatient=0.7),
}


@dataclass
class Session:
    name: str
    books: dict[int, list[dict]]            # tick -> bench offers in the book at that tick (last read of the tick)
    limits: dict[str, int] | None = None    # true limits (sim files only)
    fee_bps: int = 0
    fee_per_card: int = 0
    run_ticks: int = RUN_TICKS
    matched: set = field(default_factory=set)   # ids the recording shows as matched (censored afterwards)
    result: dict | None = None              # the server's bench fields, if the file has a result line


# -------------------------------------------------------------------------------------------- sessions

def bench_offer(oid: str, side: str, quote: int) -> dict:
    """A bench offer in the book's shape (starter_broker: a seller's ask is want.cash, a buyer's bid give.cash)."""
    return {"id": oid, "give": {"cash": quote if side == "buy" else 0, "assets": []},
            "want": {"cash": quote if side == "sell" else 0}}


def sim_session(seed: int, model: sim.Model, label: str = "sim") -> tuple[Session, list]:
    """One simulated session (seeded) as the books a broker would read, every tick, before it matches anything."""
    traders = sim.session(random.Random(seed), model)
    run = f"r{seed}"
    books = {t: [bench_offer(f"{run}-{x.id}", x.side, x.quote(t)) for x in traders if x.alive(t)]
             for t in range(model.ticks)}
    limits = {f"{run}-{x.id}": x.limit for x in traders}
    return Session(f"{label}-{seed}", books, limits, run_ticks=model.ticks), traders


def write_session(sess: Session, path: Path):
    """A session in the recorder's file format (meta, book per tick, truth)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        f.write(json.dumps({"kind": "meta", "session": sess.name, "schedule": {"params": {"ticks": sess.run_ticks}},
                            "source": "sim"}) + "\n")
        for t in sorted(sess.books):
            f.write(json.dumps({"kind": "book", "tick": t, "book": {
                "bench_offers": sess.books[t], "fee_bps": sess.fee_bps, "fee_per_card": sess.fee_per_card}}) + "\n")
        if sess.limits:
            f.write(json.dumps({"kind": "truth", "limits": sess.limits}) + "\n")


def load(path: Path) -> Session | None:
    """A recorded (or sim-written) session file; None if it holds no bench offers (results.jsonl, a fallback file)."""
    books, limits, matched, others, run_ticks, fee, result = {}, None, set(), [], RUN_TICKS, (0, 0), None
    for line in Path(path).read_text().splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        kind = d.get("kind")
        if kind == "meta":
            run_ticks = int(((d.get("schedule") or {}).get("params") or {}).get("ticks") or run_ticks)
        elif kind == "book":
            b = d.get("book") or {}
            books[int(d["tick"])] = b.get("bench_offers") or []  # a later read of the same tick replaces it
            fee = (int(b.get("fee_bps") or 0), int(b.get("fee_per_card") or 0))
            others.append(json.dumps({k: v for k, v in b.items() if k not in ("bench_offers", "offers")}))
        elif kind == "truth":
            limits = {k: int(v) for k, v in d["limits"].items()}
        elif kind == "match":
            matched.update((d["sell"], d["buy"]))
        elif kind == "result":
            result = d.get("me")
    ids = {o["id"] for offers in books.values() for o in offers}
    if not ids:
        return None
    blob = "\n".join(others)  # settlements (shape unknown): any bench id quoted in a non-offer field was matched
    matched |= {i for i in ids if f'"{i}"' in blob}
    return Session(Path(path).stem, books, limits, fee[0], fee[1], run_ticks, matched, result)


def side_of(o: dict) -> str:
    return "sell" if (o.get("want") or {}).get("cash") else "buy"


def quote_of(o: dict) -> int:
    return int((o.get("want") or {}).get("cash") or (o.get("give") or {}).get("cash") or 0)


def limits_of(sess: Session) -> tuple[dict[str, int], dict[str, str], str]:
    """(limit per id, side per id, 'true' | 'proxy')."""
    side, best = {}, {}
    for offers in sess.books.values():
        for o in offers:
            s, q = side_of(o), quote_of(o)
            side[o["id"]] = s
            best[o["id"]] = q if o["id"] not in best else (max if s == "buy" else min)(best[o["id"]], q)
    if sess.limits:
        return {i: sess.limits[i] for i in side}, side, "true"
    return best, side, "proxy"


def possible(limits: dict[str, int], side: dict[str, str]) -> int:
    """sim.possible_gains, run by run (a match pairs two offers of one run)."""
    runs: dict[str, list] = {}
    for i, lim in limits.items():
        runs.setdefault(run_of(i), []).append(SimpleNamespace(side=side[i], limit=lim))
    return sum(sim.possible_gains(ts) for ts in runs.values())


def _best_matching(bs: list[str], ss: list[str], gain: dict[tuple[str, str], int]) -> int:
    """Max-weight bipartite matching by DP over a bitmask of `ss` (the smaller side). gain[(b, s)] for allowed pairs."""
    memo: dict[tuple[int, int], int] = {}

    def best(i: int, used: int) -> int:
        if i == len(bs):
            return 0
        if (i, used) not in memo:
            r = best(i + 1, used)
            for j, s in enumerate(ss):
                if not used >> j & 1 and (bs[i], s) in gain:
                    r = max(r, gain[bs[i], s] + best(i + 1, used | 1 << j))
            memo[i, used] = r
        return memo[i, used]

    return best(0, 0)


def oracle(sess: Session) -> float | None:
    """Headroom check: the best ANY quote-respecting broker could have done with hindsight, as a share of the possible
    gains. = a max-weight matching over the pairs that crossed on quotes at some tick while both were in the book (each
    such pair could have been crossed at that tick; the pairs are disjoint). None if a run is too big to solve exactly."""
    limits, side, _ = limits_of(sess)
    crossed: set[tuple[str, str]] = set()  # (buy id, sell id)
    for offers in sess.books.values():
        asks = [(o["id"], quote_of(o)) for o in offers if side_of(o) == "sell"]
        for b in (o for o in offers if side_of(o) == "buy"):
            crossed |= {(b["id"], a) for a, q in asks if run_of(a) == run_of(b["id"]) and q <= quote_of(b)}
    total = 0
    for run in {run_of(i) for i in side}:
        bs = [i for i in side if side[i] == "buy" and run_of(i) == run]
        ss = [i for i in side if side[i] == "sell" and run_of(i) == run]
        if min(len(bs), len(ss)) > 14:
            return None
        gain = {(b, s): limits[b] - limits[s] for b, s in crossed if run_of(b) == run}
        if len(ss) > len(bs):  # the bitmask runs over the smaller side
            bs, ss, gain = ss, bs, {(s, b): g for (b, s), g in gain.items()}
        total += _best_matching(bs, ss, gain)
    best_all = possible(limits, side)
    return total / best_all if best_all else 1.0


# -------------------------------------------------------------------------------------------- replay

def replay(sess: Session, strategy: str, censor: str = "leave", verbose: bool = False, bench_fee: bool = False) -> dict:
    """Feed the session tick by tick to a Planner; matched offers leave the book. Every match is checked against the
    book it was planned on (same run, a sell and a buy, both live and unmatched, ask <= price, price + fee <= bid)."""
    planner = Planner(strategy, run_ticks=sess.run_ticks, bench_fee=bench_fee)
    fee = make_fee(sess.fee_bps, sess.fee_per_card) if bench_fee else make_fee()
    limits, side, basis = limits_of(sess)
    done, matches, violations = set(), [], []
    last: dict[str, tuple[int, dict]] = {}
    ticks = sorted(sess.books)
    current: list[dict] = []
    for t in range(ticks[0], ticks[-1] + 1):
        current = sess.books.get(t, current)  # a tick the recorder missed: the last state seen
        offers = list(current)
        for o in offers:
            last[o["id"]] = (t, o)
        if censor == "hold":
            here = {o["id"] for o in offers}
            live_runs = {run_of(i) for i in here}
            offers += [o for i, (tl, o) in last.items()
                       if i in sess.matched and i not in here and tl < t and run_of(i) in live_runs]
        offers = [o for o in offers if o["id"] not in done]
        by_id = {o["id"]: o for o in offers}
        book = {"bench_offers": offers, "fee_bps": sess.fee_bps, "fee_per_card": sess.fee_per_card}
        for sell, buy, price in planner.bench_plan(book, t):
            s, b = by_id.get(sell), by_id.get(buy)
            bad = (s is None or b is None or sell in done or buy in done or sell == buy or side_of(s) != "sell"
                   or side_of(b) != "buy" or run_of(sell) != run_of(buy) or price is None
                   or not (quote_of(s) <= price and price + fee(price) <= quote_of(b)))
            if bad:
                violations.append((t, sell, buy, price))
                continue
            done.update((sell, buy))
            matches.append((t, sell, buy, price))
            if verbose:
                print(f"  tick {t:>3} {sell} (ask {quote_of(s)}, limit {limits[sell]}) x {buy} (bid {quote_of(b)}, "
                      f"limit {limits[buy]}) at {price} · gain {limits[buy] - limits[sell]}")
    gains = sum(limits[b] - limits[s] for _, s, b, _ in matches)
    best = possible(limits, side)
    unmatched = sorted(i for i in side if i not in done)
    return {"eff": gains / best if best else 1.0, "gains": gains, "best": best, "pairs": len(matches),
            "matches": matches, "violations": violations, "basis": basis, "unmatched": unmatched}


# -------------------------------------------------------------------------------------------- reports

def summary(xs: list[float]) -> str:
    sd = statistics.stdev(xs) if len(xs) > 1 else 0.0
    return f"{statistics.mean(xs):.4f} ± {sd:.4f}"


def compare(sessions: list[Session], strategies: list[str], censor: str = "leave") -> dict:
    """Paired scores: {strategy: [eff per session]} plus violations."""
    out = {s: [] for s in strategies}
    viol = {s: 0 for s in strategies}
    for sess in sessions:
        for s in strategies:
            r = replay(sess, s, censor)
            out[s].append(r["eff"])
            viol[s] += len(r["violations"])
    return {"eff": out, "violations": viol}


def report(label: str, sessions: list[Session], strategies: list[str], censor: str) -> dict:
    r = compare(sessions, strategies, censor)
    basis = "true limits" if all(s.limits for s in sessions) else "PROXY limits (most relaxed quote)"
    print(f"\n{label} · {len(sessions)} sessions · {basis} · censor {censor}")
    print(f"  {'strategy':<12}{'mean ± sd':>20}{'p10':>8}{'min':>8}{'violations':>12}")
    for s in strategies:
        xs = r["eff"][s]
        print(f"  {s:<12}{summary(xs):>20}{sorted(xs)[len(xs) // 10]:>8.3f}{min(xs):>8.3f}{r['violations'][s]:>12}")
    orc = [o for o in (oracle(s) for s in sessions) if o is not None]
    if orc:
        print(f"  {'quote-oracle':<12}{summary(orc):>20}   (hindsight ceiling for any broker that crosses quotes)")
    if len(strategies) == 2:
        a, b = strategies
        d = [y - x for x, y in zip(r["eff"][a], r["eff"][b])]
        better, worse = sum(x > 1e-12 for x in d), sum(x < -1e-12 for x in d)
        print(f"  {b} − {a} (paired): {summary(d)} · better {better} · equal {len(d) - better - worse} · worse {worse}"
              f" · worst {min(d):+.3f}")
    for sess in sessions:
        if sess.result:
            print(f"  server's numbers for {sess.name}: {sess.result}")
    return r


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Replay Market Test sessions through broker strategies")
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--sim", choices=[*MODELS, "all"], help="simulated sessions instead of files")
    ap.add_argument("--seeds", type=int, default=200, help="simulated sessions (seeds 0..N-1)")
    ap.add_argument("--compare", nargs="+", choices=STRATEGIES, metavar="STRATEGY")
    ap.add_argument("--strategy", choices=STRATEGIES, help="one strategy (with -v: its matches)")
    ap.add_argument("--censor", choices=("leave", "hold"), default="leave")
    ap.add_argument("--write", type=Path, help="with --sim: write the sessions as recorder-format files here")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args(argv)
    strategies = a.compare or ([a.strategy] if a.strategy else list(STRATEGIES))
    if a.sim:
        for name in (MODELS if a.sim == "all" else [a.sim]):
            sessions = [sim_session(seed, MODELS[name], name)[0] for seed in range(a.seeds)]
            if a.write:
                for s in sessions:
                    write_session(s, a.write / f"{s.name}.jsonl")
                print(f"wrote {len(sessions)} sessions to {a.write}/")
            report(f"sim {name}", sessions, strategies, a.censor)
        return 0
    sessions = [s for s in (load(p) for p in a.files) if s is not None]
    if not sessions:
        print("no session with bench offers in", [str(p) for p in a.files] or "(no files)")
        return 1
    if a.verbose:
        for sess in sessions:
            for s in strategies:
                print(f"{sess.name} · {s}:")
                r = replay(sess, s, a.censor, verbose=True)
                print(f"  → eff {r['eff']:.4f} ({r['basis']}) · {r['pairs']} pairs · gains {r['gains']}/{r['best']} · "
                      f"unmatched {len(r['unmatched'])} · violations {len(r['violations'])}")
    report("recorded", sessions, strategies, a.censor)
    return 0


if __name__ == "__main__":
    sys.exit(main())
