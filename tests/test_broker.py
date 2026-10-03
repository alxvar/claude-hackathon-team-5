"""Offline tests for broker/: no network. Fixtures: synthetic books from broker/sim.py and a hand-made 3-tick book.

    uv run pytest tests/test_broker.py -s      # -s prints v1 vs auto_clone (mean ± sd over 200 seeds)
"""
import importlib
import json
import random
import statistics

import pytest

from broker import broker as B
from broker import replay as R
from broker import sim
from broker.common import BazaarError, find_broker_key, scrub
from broker.record_bench import BenchRecorder

starter_broker = importlib.import_module("starter_broker")  # the organisers' starter: bazaar-kit/, on the path via broker.common

SEEDS = range(200)
MODELS = ("default", "hard-12")


# ------------------------------------------------------------------------------------ helpers

def random_book(rnd: random.Random, runs=("b7", "b8"), fee_bps=0, fee_per_card=0) -> dict:
    """Random bench offers over a few runs, with ties, interleaved as a real book might list them."""
    offers = []
    for run in runs:
        for i in range(rnd.randint(0, 8)):
            q = rnd.randint(20, 40) if rnd.random() < 0.3 else rnd.randint(10, 120)  # a narrow band makes ties
            offers.append(R.bench_offer(f"{run}-{i}", rnd.choice(("buy", "sell")), q))
    rnd.shuffle(offers)
    return {"bench_offers": offers, "offers": [], "fee_bps": fee_bps, "fee_per_card": fee_per_card}


def sim_stall_pairs(traders, m):
    """The pairs sim.py's stall makes, tick by tick (spying on sim.run)."""
    seen = []

    def spy(t, bids, asks, st):
        out = sim.stall(t, bids, asks, st)
        seen.extend((t, b, s) for b, s in out)
        return out

    return sim.run(spy, traders, m), seen


# ------------------------------------------------------------------------------------ auto_clone == the stall

def test_auto_clone_equals_the_starter_brokers_bench_plan():
    rnd = random.Random(1)
    for _ in range(2000):
        book = random_book(rnd, fee_bps=rnd.choice((0, 0, 300)))  # the starter charges no fee on bench matches
        assert B.Planner("auto_clone").bench_plan(book, 0) == starter_broker.bench_plan(book)
        if not book["fee_bps"]:
            assert B.Planner("auto_clone", bench_fee=True).bench_plan(book, 0) == starter_broker.bench_plan(book)


@pytest.mark.parametrize("model", MODELS)
def test_replay_auto_clone_reproduces_sim_stall_exactly(model):
    m = R.MODELS[model]
    for seed in SEEDS:
        sess, traders = R.sim_session(seed, m, model)
        eff, pairs = sim_stall_pairs(traders, m)
        r = R.replay(sess, "auto_clone")
        assert [(t, b.split("-")[1], s.split("-")[1]) for t, s, b, _ in r["matches"]] == pairs, seed
        assert r["eff"] == eff, seed


def test_sim_session_survives_the_file_format(tmp_path):
    for seed in range(20):
        sess, _ = R.sim_session(seed, R.MODELS["hard-12"], "hard")
        R.write_session(sess, tmp_path / f"{sess.name}.jsonl")
        back = R.load(tmp_path / f"{sess.name}.jsonl")
        for s in B.STRATEGIES:
            assert R.replay(back, s)["matches"] == R.replay(sess, s)["matches"]
            assert R.replay(back, s)["eff"] == R.replay(sess, s)["eff"]


# ------------------------------------------------------------------------------------ v1 vs auto_clone

@pytest.mark.parametrize("model", MODELS)
def test_v1_not_below_auto_clone_over_200_seeds(model):
    sessions = [R.sim_session(seed, R.MODELS[model], model)[0] for seed in SEEDS]
    r = R.compare(sessions, ["auto_clone", "v1", "v1_literal"])
    a, v, lit = r["eff"]["auto_clone"], r["eff"]["v1"], r["eff"]["v1_literal"]
    d = [y - x for x, y in zip(a, v)]
    print(f"\n{model}: auto_clone {statistics.mean(a):.4f} ± {statistics.stdev(a):.4f} · v1 {statistics.mean(v):.4f} ± "
          f"{statistics.stdev(v):.4f} · v1 − auto_clone {statistics.mean(d):+.4f} ± {statistics.stdev(d):.4f} "
          f"(better {sum(x > 0 for x in d)}, worse {sum(x < 0 for x in d)}) · v1_literal {statistics.mean(lit):.4f}")
    assert statistics.mean(v) >= statistics.mean(a)
    assert sum(r["violations"].values()) == 0


@pytest.mark.parametrize("model", MODELS)
def test_v1_matches_every_trader_the_stall_would_each_tick(model):
    """Per tick, on the same book and history, v1's matched traders include auto_clone's (it only adds)."""
    m = R.MODELS[model]
    for seed in range(100):
        sess, _ = R.sim_session(seed, m, model)
        stall, v1 = B.Planner("auto_clone", run_ticks=m.ticks), B.Planner("v1", run_ticks=m.ticks)
        for t in sorted(sess.books):
            book = {"bench_offers": sess.books[t]}
            base = {i for s, b, _ in stall.bench_plan(book, t) for i in (s, b)}
            more = {i for s, b, _ in v1.bench_plan(book, t) for i in (s, b)}
            assert base <= more, (seed, t)


@pytest.mark.parametrize("strategy", B.STRATEGIES)
def test_no_crossing_violations_with_fees_and_many_runs(strategy):
    """Every planned match is a sell and a buy of one run, each used once, with ask <= price and price + fee <= bid."""
    rnd = random.Random(7)
    for _ in range(1500):
        fee_bps, per_card = rnd.choice(((0, 0), (500, 1), (1000, 5), (150, 0)))
        start = random_book(rnd, runs=("b1", "b2", "b3"), fee_bps=fee_bps, fee_per_card=per_card)
        fee = B.make_fee(fee_bps, per_card)
        planner = B.Planner(strategy, run_ticks=6, bench_fee=True)
        steps = {o["id"]: rnd.choice((0, 0, 1, 3, 8)) for o in start["bench_offers"]}  # firm, slow and fast relaxers
        for tick in range(6):  # quotes relax tick by tick (v1's urgent path), the last two ticks are its tail
            book = {**start, "bench_offers": [R.bench_offer(o["id"], R.side_of(o), max(1, R.quote_of(o) + (
                1 if R.side_of(o) == "buy" else -1) * steps[o["id"]] * tick)) for o in start["bench_offers"]]}
            used = set()
            by_id = {o["id"]: o for o in book["bench_offers"]}
            for sell, buy, price in planner.bench_plan(book, tick):
                s, b = by_id[sell], by_id[buy]
                assert R.side_of(s) == "sell" and R.side_of(b) == "buy" and B.run_of(sell) == B.run_of(buy)
                assert sell not in used and buy not in used
                assert R.quote_of(s) <= price and price + fee(price) <= R.quote_of(b)
                used.update((sell, buy))


# ------------------------------------------------------------------------------------ hand-made 3-tick book

def hand_book(tmp_path):
    """Run b1 of 4 ticks (so ticks 2-3 are the tail). Truth: B1 values 52, B2 60; S1 costs 40, S2 45.
    tick 0: nothing crosses. tick 1: B1 50 and B2 45 relaxed, S1 44 firm, S2 relaxed to 48: the stall crosses its best
    pair (S1, B1) and strands B2 and S2; v1 re-pairs to (S1, B2) + (S2, B1). tick 2: B2 has left."""
    o = R.bench_offer
    ticks = {0: [o("b1-1", "buy", 40), o("b1-2", "buy", 30), o("b1-3", "sell", 44), o("b1-4", "sell", 60)],
             1: [o("b1-1", "buy", 50), o("b1-2", "buy", 45), o("b1-3", "sell", 44), o("b1-4", "sell", 48)],
             2: [o("b1-1", "buy", 50), o("b1-3", "sell", 44), o("b1-4", "sell", 47)]}
    path = tmp_path / "bench-hand.jsonl"
    lines = [{"kind": "meta", "schedule": {"params": {"ticks": 4}}}]
    lines += [{"kind": "book", "tick": t, "book": {"bench_offers": offers, "fee_bps": 0}} for t, offers in ticks.items()]
    lines.append({"kind": "truth", "limits": {"b1-1": 52, "b1-2": 60, "b1-3": 40, "b1-4": 45}})
    path.write_text("\n".join(json.dumps(x) for x in lines) + "\n")
    return path


def test_hand_made_book(tmp_path):
    sess = R.load(hand_book(tmp_path))
    a, v = R.replay(sess, "auto_clone"), R.replay(sess, "v1")
    assert a["matches"] == [(1, "b1-3", "b1-1", 47)]
    assert v["matches"] == [(1, "b1-3", "b1-2", 44), (1, "b1-4", "b1-1", 49)]
    assert (a["gains"], v["gains"], a["best"]) == (12, 27, 27)
    assert v["eff"] == 1.0 and a["eff"] == pytest.approx(12 / 27)
    assert R.oracle(sess) == 1.0


def test_recorded_session_without_truth_uses_proxy_limits(tmp_path):
    path = hand_book(tmp_path)
    path.write_text("".join(x + "\n" for x in path.read_text().splitlines() if '"truth"' not in x))
    r = R.replay(R.load(path), "v1")
    assert r["basis"] == "proxy" and r["best"] == 50 - 44  # B1 50 vs S1 44; B2 45 never covers S2 47
    assert r["gains"] == (45 - 44) + (50 - 47)  # proxies: B2 45, B1 50, S1 44, S2 47


# ------------------------------------------------------------------------------------ recorder

class FakePublic:
    def __init__(self):
        self.calls = []

    def schedule(self):
        self.calls.append("schedule")
        return {"now_hours": 4.9, "upcoming": [{"at_hours": 5.0, "action": "bench", "params": {"traders": 10, "ticks": 16}},
                                               {"at_hours": 6.5, "action": "duels"}]}

    def leaderboard(self):
        self.calls.append("leaderboard")
        return {"snapshot_tick": 300, "teams": [{"team": "t05", "market": 7.5, "venue": None},
                                                {"team": "t13", "market": 15.0, "venue": "v03"}]}

    def venues(self):
        self.calls.append("venues")
        return {"venues": [{"venue": "v03", "owner": "t13", "rules": {"mechanism": "board"}, "broker_key": "bk_LEAK"}]}


class FakeTeam:
    def me(self):
        return {"id": "t05", "starter_broker_key": "bk_SECRET", "venue": None,
                "score": {"bench_efficiency": 0.93, "bench_points": 7.5, "mm_points": 7.5, "market": 7.5}}


def test_recorder_sessions_results_and_no_keys(tmp_path):
    now = [1000.0]
    rec = BenchRecorder(tmp_path, team=FakeTeam(), public=FakePublic(), log=lambda *a: None, clock=lambda: now[0])
    rec.pause = lambda s: None
    rec.note_schedule(FakePublic().schedule())
    offers = [R.bench_offer("b12-0", "buy", 50), R.bench_offer("b12-1", "sell", 60)]
    book = {"bench_offers": offers, "offers": [], "fee_bps": 0, "broker_key": "bk_SECRET"}
    assert rec.observe({"bench_offers": [], "offers": []}, 299, 4.99) is None
    assert rec.observe(book, 300, 5.0) == "bench-h05.0"
    assert rec.observe(book, 300, 5.0) == "bench-h05.0"          # same state, same tick: no new line
    assert rec.observe(book, 301, 5.01) == "bench-h05.0"         # same offers, new tick: a line
    rec.note_match(301, "b12-1", "b12-0", 55)
    for t in (302, 303):
        assert rec.observe({"bench_offers": [], "offers": []}, t, 5.02) == "bench-h05.0"
    assert rec.observe({"bench_offers": [], "offers": []}, 304, 5.03) is None   # empty for 2 ticks: ended
    now[0] += 1000
    rec.poll_results()
    lines = [json.loads(x) for x in (tmp_path / "bench-h05.0.jsonl").read_text().splitlines()]
    kinds = [x["kind"] for x in lines]
    # ticks 300, 301 (offers), match, 302-304 (empty: one line per tick until the session closes), end, 3 results
    assert kinds == ["meta", "book", "book", "match", "book", "book", "book", "end", "result", "result", "result"]
    assert lines[0]["schedule"]["params"]["ticks"] == 16
    assert lines[-1]["me"]["bench_efficiency"] == 0.93 and lines[-1]["teams"][1]["market"] == 15.0
    assert len((tmp_path / "results.jsonl").read_text().splitlines()) == 3
    for f in tmp_path.iterdir():
        assert "bk_" not in f.read_text()
    sess = R.load(tmp_path / "bench-h05.0.jsonl")
    assert sess.run_ticks == 16 and sess.matched == {"b12-0", "b12-1"} and sess.result["bench_points"] == 7.5


def test_recorder_closes_scheduled_benches_without_a_book(tmp_path):
    now = [0.0]
    rec = BenchRecorder(tmp_path, team=FakeTeam(), public=FakePublic(), log=lambda *a: None, clock=lambda: now[0])
    rec.pause = lambda s: None
    rec.note_schedule(FakePublic().schedule())
    rec.schedule_fallback({"t_hours": 5.1, "tick_seconds": 30})   # 16 ticks of 30 s = 0.13 h: not over yet
    assert rec.due == []
    rec.schedule_fallback({"t_hours": 5.2, "tick_seconds": 30})
    now[0] = 1e4
    rec.poll_results()
    kinds = [json.loads(x)["kind"] for x in (tmp_path / "bench-h05.0.jsonl").read_text().splitlines()]
    assert kinds == ["meta", "result", "result", "result"]


def test_broker_key_lookup(monkeypatch):
    monkeypatch.delenv("BROKER_KEY", raising=False)
    key, where, _ = find_broker_key(FakeTeam())
    assert key == "bk_SECRET" and "starter_broker_key" in where and "bk_" not in where
    key, where, _ = find_broker_key(None, me={"id": "t05", "venue": None})
    assert key is None and "3.0" in where
    monkeypatch.setenv("BROKER_KEY", "bk_ENV")
    assert find_broker_key(FakeTeam())[:2] == ("bk_ENV", "env BROKER_KEY")
    assert scrub({"a": [{"broker_key": 1, "b": 2}], "X-Team-Key": 3}) == {"a": [{"b": 2}]}


# ------------------------------------------------------------------------------------ the live loop, faked

class FakeClock:
    def __init__(self, ticks):
        self.ticks = list(ticks)

    def read(self):
        return {"tick": self.ticks.pop(0) if len(self.ticks) > 1 else self.ticks[0], "t_hours": 5.0}


class FakeBroker:
    def __init__(self, books=None, fail=False):
        self.books, self.fail, self.matches = books or [], fail, []

    def book(self):
        if self.fail:
            raise BazaarError("network", "down", 0)
        return self.books.pop(0) if len(self.books) > 1 else self.books[0]

    def match(self, sell, buy, price):
        self.matches.append((sell, buy, price))
        return {}


def crossing_book():
    o = R.bench_offer
    return {"bench_offers": [o("b3-0", "buy", 70), o("b3-1", "sell", 50), o("b3-2", "buy", 20)], "offers": [], "fee_bps": 0}


def test_broker_exits_nonzero_after_repeated_errors():
    out = []
    code = B.run(FakeBroker(fail=True), FakeClock([1]), B.Planner("v1"), max_errors=3, sleep=lambda s: None,
                 out=lambda *a, **k: out.append(a[0]), max_loops=10)
    assert code == 1 and any("exiting" in x for x in out)


def test_broker_dry_run_posts_nothing_and_live_posts_once():
    out, fake = [], FakeBroker([crossing_book()])
    B.run(fake, FakeClock([1, 1, 2, 2]), B.Planner("auto_clone"), dry_run=True, sleep=lambda s: None,
          out=lambda *a, **k: out.append(a[0]), max_loops=4)
    assert fake.matches == [] and any("DRY b3-1 x b3-0 at 60" in x for x in out)
    out, fake = [], FakeBroker([crossing_book()])
    B.run(fake, FakeClock([1, 1, 2, 3]), B.Planner("auto_clone"), sleep=lambda s: None,
          out=lambda *a, **k: out.append(a[0]), max_loops=4)
    assert fake.matches == [("b3-1", "b3-0", 60)]           # the book still shows them: never posted twice
    assert any(x.split(" ", 1)[1].startswith("tick 1 ·") for x in out)   # a heartbeat per finished tick


class FakeBench:
    """A simulated bench served as the server would: the clock ticks every `k` reads, matched offers leave the book."""

    def __init__(self, sess, k=3):
        self.sess, self.k, self.n, self.tick, self.gone, self.matches = sess, k, 0, 0, set(), []

    def read(self):
        self.n += 1
        self.tick = min((self.n - 1) // self.k, max(self.sess.books))
        return {"tick": self.tick, "t_hours": 5.0}

    def book(self):
        return {"bench_offers": [o for o in self.sess.books[self.tick] if o["id"] not in self.gone], "offers": [],
                "fee_bps": 0, "fee_per_card": 0}

    def match(self, sell, buy, price):
        self.gone.update((sell, buy))
        self.matches.append((self.tick, sell, buy, price))
        return {}


@pytest.mark.parametrize("strategy", B.STRATEGIES)
def test_live_loop_on_a_simulated_bench_equals_the_replay(strategy):
    for seed in range(40):
        sess, _ = R.sim_session(seed, R.MODELS["hard-12"], "hard")
        fake = FakeBench(sess)
        B.run(fake, fake, B.Planner(strategy), sleep=lambda s: None, out=lambda *a, **k: None,
              max_loops=fake.k * len(sess.books))
        assert fake.matches == R.replay(sess, strategy)["matches"], seed


def test_ids_reused_by_a_later_session_start_clean():
    o = R.bench_offer
    planner = B.Planner("v1", run_ticks=16)
    for t in range(4):
        planner.bench_plan({"bench_offers": [o("b1-0", "buy", 40 + t), o("b1-1", "sell", 60)]}, t)
    planner.bench_plan({"bench_offers": []}, 10)                     # the session is over
    assert "b1" not in planner.run_start and "b1-0" not in planner.hist
    planner.bench_plan({"bench_offers": [o("b1-0", "buy", 40), o("b1-1", "sell", 60)]}, 50)
    assert planner.run_start["b1"] == 50                             # the tail rule counts from the new start
    empty = {"bench_offers": [], "offers": [], "fee_bps": 0}
    fake = FakeBroker([crossing_book(), crossing_book(), empty, empty, crossing_book(), crossing_book()])
    B.run(fake, FakeClock([1, 1, 2, 3, 20, 20]), B.Planner("auto_clone"), sleep=lambda s: None,
          out=lambda *a, **k: None, max_loops=6)
    assert fake.matches == [("b3-1", "b3-0", 60)] * 2               # same ids, next session: matched again


def test_broker_survives_odd_shapes_and_exits_on_repeated_match_errors():
    out = []

    class Odd(FakeBroker):
        def match(self, sell, buy, price):
            raise BazaarError("http_502", "bad gateway", 502)

    odd = {"bench_offers": [{"id": "b9-0"}, "junk", {"no": "id"}, *crossing_book()["bench_offers"]], "offers": None}
    code = B.run(Odd([odd]), FakeClock(list(range(1, 50))), B.Planner("v1"), max_errors=3, sleep=lambda s: None,
                 out=lambda *a, **k: out.append(a[0]), max_loops=40)
    assert code == 1 and any("3 consecutive match failures" in x for x in out)
