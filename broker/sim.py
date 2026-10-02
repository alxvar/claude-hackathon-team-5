"""Offline Market Test: broker strategies against the free stall, on simulated bench sessions. Free, no key.

What we know (starter_broker.py, RULES.md): every bench session gives every venue the same book of buyers and
sellers. Each trader keeps a hidden limit and quotes away from it ("shades"); most relax their quote as their
patience runs out and leave when it does; the firm ones never relax. A match needs the quotes to cross
(ask <= price, price + fee <= bid). The score is the share of the possible gains, between the TRUE limits, that
the venue realises. The free stall crosses the best bid with the best ask each tick, at the midpoint.

What we guess (calibrate on the first real session with broker/record_bench.py): limit ranges, shade sizes, how
patience and relaxation work, the mix of trader types. Every guess is a parameter of `Model`, and `--sweep`
runs the strategies across a range of them: we pick the strategy that wins everywhere, not under one guess.

    python3 broker/sim.py              # default model, 2,000 sessions
    python3 broker/sim.py --sweep      # robustness across trader models
"""
import argparse
import random
import statistics
from dataclasses import dataclass


@dataclass
class Model:
    traders: int = 10        # per session, split between buyers and sellers
    ticks: int = 16
    shade: tuple = (0.05, 0.35)    # initial distance of the quote from the limit, as a share of the limit
    impatient: float = 0.4   # share that leaves early
    firm: float = 0.2        # share that never relaxes
    early_leave: tuple = (3, 7)    # patience of the impatient ones, in ticks
    late_leave: tuple = (10, 17)   # patience of the others
    lo_hi: tuple = (20, 100)       # limits drawn from this range


class Trader:
    def __init__(self, rnd: random.Random, side: str, m: Model, i: int):
        self.id, self.side = f"{side[0]}{i}", side
        self.limit = rnd.randint(*m.lo_hi)
        self.shade = rnd.uniform(*m.shade)
        self.firm = rnd.random() < m.firm
        self.patience = rnd.randint(*(m.early_leave if rnd.random() < m.impatient else m.late_leave))

    def quote(self, t: int) -> int:
        s = self.shade if self.firm else self.shade * max(0.0, 1 - t / self.patience)
        return round(self.limit * (1 - s)) if self.side == "buy" else round(self.limit * (1 + s))

    def alive(self, t: int) -> bool:
        return t < self.patience


def session(rnd: random.Random, m: Model) -> list:
    nb = m.traders // 2
    return [Trader(rnd, "buy", m, i) for i in range(nb)] + [Trader(rnd, "sell", m, i) for i in range(m.traders - nb)]


def possible_gains(traders: list) -> float:
    """The most any matching can realise: the k highest values against the k lowest costs."""
    v = sorted((t.limit for t in traders if t.side == "buy"), reverse=True)
    c = sorted(t.limit for t in traders if t.side == "sell")
    return sum(max(0, a - b) for a, b in zip(v, c))


# ---------------------------------------------------------------- strategies: (t, live quotes, state) -> pairs

def stall(t, bids, asks, st):
    """What the free stall and the starter broker do: best bid against best ask, while they cross."""
    out = []
    for (b, bq), (s, sq) in zip(sorted(bids, key=lambda x: -x[1]), sorted(asks, key=lambda x: x[1])):
        if bq < sq:
            break
        out.append((b, s))
    return out


def max_pairs(bids, asks):
    """As many crossing pairs as possible: each bid, highest first, takes the highest ask it still covers.
    Best-vs-best spends the cheapest asks on the richest bids and can leave a cheaper bid with nothing it covers."""
    free, out = sorted(asks, key=lambda x: x[1]), []
    for b, bq in sorted(bids, key=lambda x: -x[1]):
        fit = [a for a in free if a[1] <= bq]
        if fit:
            a = fit[-1]
            free.remove(a)
            out.append((b, a[0]))
    return out


def most_pairs(t, bids, asks, st):
    return max_pairs(bids, asks)


def patient(t, bids, asks, st):
    """Most pairs, but only cross a pair now if one side is about to leave or the session is ending; otherwise
    wait a tick so relaxing quotes open more pairs. A trader 'about to leave' = its quote moved fast last tick
    (impatient traders relax fastest) or it has been in the book a long time."""
    last = st.setdefault("last", {})
    urgent = set()
    for i, q in bids + asks:
        prev = last.get(i)
        if prev is not None and abs(q - prev) >= max(2, 0.04 * q):
            urgent.add(i)
    last.update(dict(bids + asks))
    pairs = max_pairs(bids, asks)
    if t >= st["ticks"] - 2:
        return pairs
    return [(b, s) for b, s in pairs if b in urgent or s in urgent]


STRATEGIES = {"stall": stall, "most_pairs": most_pairs, "patient": patient}


def run(strategy, traders: list, m: Model) -> float:
    by_id = {x.id: x for x in traders}
    done, gains, st = set(), 0.0, {"ticks": m.ticks}
    for t in range(m.ticks):
        live = [x for x in traders if x.alive(t) and x.id not in done]
        bids = [(x.id, x.quote(t)) for x in live if x.side == "buy"]
        asks = [(x.id, x.quote(t)) for x in live if x.side == "sell"]
        for b, s in strategy(t, bids, asks, st):
            done.update((b, s))
            gains += by_id[b].limit - by_id[s].limit
    best = possible_gains(traders)
    return gains / best if best else 1.0


def compare(m: Model, n: int, seed: int = 7) -> dict:
    rnd = random.Random(seed)
    sessions = [session(rnd, m) for _ in range(n)]  # the same sessions for every strategy (paired)
    out = {}
    for name, f in STRATEGIES.items():
        eff = [run(f, s, m) for s in sessions]
        out[name] = (statistics.mean(eff), sorted(eff)[n // 10])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--sweep", action="store_true")
    args = ap.parse_args()
    models = [("default", Model())]
    if args.sweep:
        models += [
            ("light shading", Model(shade=(0.02, 0.15))),
            ("heavy shading", Model(shade=(0.15, 0.5))),
            ("mostly impatient", Model(impatient=0.7)),
            ("mostly patient", Model(impatient=0.1)),
            ("many firm", Model(firm=0.5)),
            ("no firm", Model(firm=0.0)),
            ("20 traders", Model(traders=20)),
        ]
    print(f"{'model':<18}" + "".join(f"{k:>22}" for k in STRATEGIES))
    for label, m in models:
        r = compare(m, args.n)
        print(f"{label:<18}" + "".join(f"{f'{mean:.3f} (p10 {p10:.2f})':>22}" for mean, p10 in r.values()))


if __name__ == "__main__":
    main()
