"""Offline tests for tools/reactor.py: fake stream, feed, API and clock; nothing sent, nothing written outside tmp."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "bazaar-kit"))
import reactor as rx  # noqa: E402

TEAMS = [{"team": t, "name": f"Team {int(t[1:])}", "score": s} for t, s in
         (("t10", 40), ("t06", 38), ("t03", 36), ("t14", 35), ("t18", 34), ("t12", 33), ("t05", 30), ("t09", 20),
          ("t08", 15), ("t07", 12), ("t13", 10))]
VENUES = [{"venue": "v07", "owner": "t10", "fee_bps": 0, "fee_per_card": 0},
          {"venue": "v15", "owner": "t15", "fee_bps": 0, "fee_per_card": 0},
          {"venue": "v10", "owner": "t05", "fee_bps": 0, "fee_per_card": 0}]


class Clock:
    def __init__(self):
        self.t, self.slept = 1000.0, []

    def now(self):
        return self.t

    def sleep(self, s):
        self.slept.append(round(s, 2))
        self.t += s


class Api:
    def __init__(self, values, cash=500):
        self.values, self.cash, self.calls = values, cash, []

    def value(self, ref):
        self.calls.append(ref)
        return {"your_value": self.values[ref]}

    def me(self):
        return {"id": "t05", "cash": self.cash}


class Pub:
    def _call(self, method, path, *a, **k):
        return {"/api/venues": {"venues": VENUES}, "/api/leaderboard": {"teams": TEAMS}}[path]


_id = [100]


def listed(maker, venue, give, want, to=None, eid=None):
    _id[0] += 1
    oid = _id[0]
    return {"id": eid or oid, "tick": 50, "type": "offer.listed", "actor": maker,
            "payload": {"venue": venue, "offer": {"id": oid, "maker": maker, "to": to, "venue": venue, "give": give,
                                                  "want": want, "expires_tick": 54}}}


def ask(maker, ref, price, venue="rastro", to=None):
    return listed(maker, venue, {"cash": 0, "assets": [{"id": 1, "kind": "card", "ref": ref}]}, {"cash": price}, to)


def bid(maker, ref, cash, venue="rastro"):
    return listed(maker, venue, {"cash": cash, "assets": []}, {"cash": 0, "types": [f"card:{ref}"]})


def make(tmp_path, values=None, cash=500, targets=None):
    clock, sent, logs = Clock(), [], []
    r = rx.Reactor(Api(values or {}, cash), Pub(), notifier=lambda *a, **k: sent.append(a), log=logs.append,
                   now=clock.now, sleep=clock.sleep, v10_out=tmp_path / "v10.jsonl",
                   targets_fn=lambda watch: dict(targets or {}))
    return r, clock, sent, logs


def test_sse_parses_events_and_skips_hello_and_comments():
    lines = [b"event: hello\n", b'data: {"tick": 1}\n', b"\n", b": keep-alive\n", b"\n", b"event: offer.listed\n",
             b'data: {"id": 7, "type": "offer.listed"}\n', b"\n", "data: {\"id\": 8}\n", "\n", b"data: not json\n", b"\n"]
    assert [e["id"] for e in rx.sse(lines)] == [7, 8]


def test_buy_when_an_ask_gains_15_after_the_fee(tmp_path):
    r, clock, sent, logs = make(tmp_path, {"RET-03": 40})
    lines = r.handle(ask("t09", "RET-03", 10))
    assert lines and lines[0].startswith("BUY ") and "gain +28" in lines[0]   # 40 - 10 - (ceil 5% + 1 = 2)
    assert sent and sent[0][0] == "operator"
    r, *_ = make(tmp_path, {"RET-03": 40}, cash=360)
    assert r.handle(ask("t09", "RET-03", 10))[0].startswith("BUY-NOCASH ")   # 360 - 12 < 350


def test_no_buy_from_rivals_dealers_our_venue_or_small_gains(tmp_path):
    r, *_ = make(tmp_path, {"RET-03": 40, "RET-04": 20})
    assert r.handle(ask("t10", "RET-03", 10)) == []                  # a rival seller (top 6)
    assert r.handle(ask("t09", "RET-03", 10, venue="v07")) == []     # on a rival's venue
    assert r.handle(ask("picaros", "RET-03", 10)) == []              # a dealer deal never scores above 0
    assert r.handle(ask("t09", "RET-04", 10)) == []                  # 20 - 10 - 2 = 8 < 15
    assert r.handle(ask("t09", "RET-03", 10, to="t08")) == []        # addressed to someone else
    assert r.handle(bid("t09", "RET-03", 30)) == []                  # a bid, not an ask
    assert r.handle(ask("t09", "RET-03", 10, to="t05"))[0].startswith("BUY ")   # addressed to us: fine


def test_value_lookups_are_cached_paced_and_dropped_after_our_trades(tmp_path):
    r, clock, sent, logs = make(tmp_path, {"RET-03": 40, "RET-04": 40})
    r.handle(ask("t09", "RET-03", 10))
    r.handle(ask("t08", "RET-03", 11))
    assert r.api.calls == ["RET-03"]                                 # cached
    r.handle(ask("t09", "RET-04", 10))
    assert r.api.calls == ["RET-03", "RET-04"] and clock.slept and clock.slept[-1] <= 1.0   # <= 1 lookup/s
    _id[0] += 1
    r.handle({"id": _id[0], "tick": 51, "type": "settlement", "payload": {"parties": ["t09", "t05"], "items": []}})
    r.handle(ask("t07", "RET-03", 10))
    assert r.api.calls[-1] == "RET-03" and len(r.api.calls) == 3      # our holdings moved: re-read


def test_deny_and_hunt_for_a_watched_team_s_last_card(tmp_path):
    r, clock, sent, logs = make(tmp_path, {"RET-02": 12}, targets={"RET-02": [("t10", "RET")]})
    lines = r.handle(ask("t08", "RET-02", 20))
    assert lines[0].startswith("DENY ") and "last RET card t10 needs" in lines[0] and "within the 35 P cap" in lines[0]
    assert any(s[0] == "operator" and "DENY" in s[1] for s in sent)
    assert "OVER the 35 P cap" in r.handle(ask("t08", "RET-02", 40))[0]
    hunt = r.handle(bid("t10", "RET-02", 30))
    assert hunt and hunt[0].startswith("HUNT ")
    assert r.handle(ask("t10", "RET-02", 20)) == []                  # its own ask: nothing to deny (and a rival)


def test_v10_listings_are_logged_for_the_market(tmp_path):
    r, *_ = make(tmp_path)
    lines = r.handle(bid("t09", "LAV-03", 6, venue="v10"))
    assert lines == ["V10 " + lines[0][4:]] and "t09 gives 6 P for LAV-03" in lines[0]
    rec = json.loads((tmp_path / "v10.jsonl").read_text().splitlines()[0])
    assert rec["maker"] == "t09" and rec["want"]["types"] == ["card:LAV-03"]


def test_events_are_handled_once_and_the_first_backfill_only_marks_the_place(tmp_path):
    r, *_ = make(tmp_path, {"RET-03": 40})
    old = ask("t09", "RET-03", 10, venue="rastro")
    old["id"] = 5
    assert r.backfill([old]) == 0 and r.last_id == 5                 # stale listings at start: no page
    new = ask("t08", "RET-03", 10)
    new["id"] = 6
    assert r.backfill([new, old]) == 1
    assert r.handle(new) == []                                       # the stream repeats it: once


def test_a_dropped_stream_falls_back_to_polling(tmp_path):
    r, clock, sent, logs = make(tmp_path, {"RET-03": 40})
    first = ask("t09", "RET-03", 50)
    first["id"] = 10
    later = ask("t09", "RET-03", 10)
    later["id"] = 11
    polls = [[first], [first], [first, later]]

    def poll():
        return polls.pop(0) if polls else []

    def stream():
        raise ConnectionError("503")
        yield  # noqa: unreachable

    r.run(stream, poll, loops=1)
    assert any(x.startswith("reactor: stream down") for x in logs)
    assert any(x.startswith("BUY ") and str(later["payload"]["offer"]["id"]) in x for x in logs)


def test_heartbeat_every_10_ticks_with_counts(tmp_path):
    r, clock, sent, logs = make(tmp_path, {"RET-03": 40})
    r.handle(ask("t09", "RET-03", 10))
    _id[0] += 1
    r.handle({"id": _id[0], "tick": 60, "type": "tick", "payload": {"tick": 60, "tick_seconds": 15.0}})
    beat = [x for x in logs if x.startswith("reactor: tick 60")]
    assert beat and "listings 1" in beat[0] and "BUY 1" in beat[0] and r.tick_seconds == 15.0
