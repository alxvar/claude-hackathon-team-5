"""Accept arbiter (tools/arbiter.py) and its use in the dealer bot: mocked SDK, no network."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "bazaar-kit"))
import arbiter  # noqa: E402
from bazaar_sdk import BazaarError  # noqa: E402


class FakeBazaar:
    def __init__(self, duels, tick=100, feed=(), fail=False):
        self._duels, self.tick, self._feed, self.fail = duels, tick, list(feed), fail
        self.calls = {"duels": 0, "clock": 0, "feed": 0}

    def duels(self):
        self.calls["duels"] += 1
        if self.fail:
            raise BazaarError("network", "down")
        return {"duels": self._duels}

    def clock(self):
        self.calls["clock"] += 1
        return {"tick": self.tick}

    def feed(self, limit=150):
        self.calls["feed"] += 1
        return {"events": self._feed}


def duel(session=2, role="buyer", limit=100, rival=None, deadline=120, issues=("price",), status="live"):
    return {"duel": 7, "session": session, "status": status, "role": role, "your_limit": limit,
            "rival_offer": None if rival is None else {"id": 1, "price": rival, "tick": 99, "days": 0},
            "deadline_tick": deadline, "issues": list(issues)}


def scheduled(session, name):
    return {"type": "duels.scheduled", "payload": {"session": session, "name": name}}


@pytest.fixture(autouse=True)
def clean(tmp_path, monkeypatch):
    monkeypatch.setattr(arbiter, "FEED", tmp_path / "feed.jsonl")  # hermetic: no real feed
    monkeypatch.setattr(arbiter, "LOG", tmp_path / "arbiter.jsonl")
    monkeypatch.setenv("ARBITER_HOLDS", "1")                         # the decision rules below; off mode at the end
    arbiter.reset()
    yield
    arbiter.reset()


def test_no_live_duel_does_not_hold():
    assert arbiter.should_hold_accept(FakeBazaar([]), 100) == (False, "no live duel")


def test_practice_session_never_holds_even_in_limit_and_at_deadline():
    b = FakeBazaar([duel(session=1, rival=80, deadline=101)])  # session 1 = the practice (RULES.md)
    hold, why = arbiter.should_hold_accept(b, 100)
    assert not hold and "none in a scored session" in why


def test_practice_named_in_feed_does_not_hold(tmp_path):
    arbiter.FEED.write_text(json.dumps(scheduled(4, "Practice duels")) + "\n")
    hold, _ = arbiter.should_hold_accept(FakeBazaar([duel(session=4, rival=80)]), 100)
    assert not hold


def test_feed_overrides_the_session_1_fallback():
    b = FakeBazaar([duel(session=1, rival=80)], feed=[scheduled(1, "Duels I")])
    assert arbiter.should_hold_accept(b, 100)[0]
    assert b.calls["feed"] == 1


def test_explicit_scored_flag_wins():
    d = duel(session=1, rival=80)
    d["scored"] = True
    assert arbiter.should_hold_accept(FakeBazaar([d]), 100)[0]


def test_scored_buyer_with_rival_offer_inside_limit_holds():
    hold, why = arbiter.should_hold_accept(FakeBazaar([duel(rival=80, limit=100)]), 100)
    assert hold and "inside our limit" in why


def test_scored_buyer_with_rival_offer_outside_limit_and_time_left_does_not_hold():
    hold, why = arbiter.should_hold_accept(FakeBazaar([duel(rival=120, limit=100, deadline=110)]), 100)
    assert not hold and "none needs the accept" in why


def test_scored_seller_limit_direction():
    assert arbiter.should_hold_accept(FakeBazaar([duel(role="seller", limit=60, rival=65)]), 100)[0]
    arbiter.reset()
    assert not arbiter.should_hold_accept(FakeBazaar([duel(role="seller", limit=60, rival=55)]), 100)[0]


@pytest.mark.parametrize("deadline,expect", [(103, True), (101, True), (104, False)])
def test_ticks_left(deadline, expect):
    hold, why = arbiter.should_hold_accept(FakeBazaar([duel(rival=None, deadline=deadline)]), 100)
    assert hold is expect
    if expect:
        assert "tick(s) left" in why


def test_a_days_duel_whose_weight_we_cannot_read_holds_on_any_offer():
    d = duel(rival=150, limit=100, issues=("price", "days"))                 # no weight in the payload
    assert arbiter.should_hold_accept(FakeBazaar([d]), 100)[0]


def days_duel(price, day, weight=2, meaning="each day later costs you 2 P"):
    """Duels II as RULES.md describes it: we buy at value 100; each day after day 0 costs us 2 P."""
    d = duel(limit=100, issues=("price", "days"))
    d.update(your_days_weight=weight, days_meaning=meaning,
             rival_offer={"id": 1, "price": price, "tick": 99, **({} if day is None else {"days": day})})
    return d


def test_a_days_duel_holds_only_when_the_whole_package_is_inside_our_limit():
    # Aleks's review (10:20): counting every standing offer would freeze our bots through most of Duels II.
    assert not arbiter.should_hold_accept(FakeBazaar([days_duel(95, 5)]), 100)[0]   # +5 on price, -10 for day 5
    hold, why = arbiter.should_hold_accept(FakeBazaar([days_duel(85, 2)]), 101)       # +15, -4: worth 11
    assert hold and "inside our limit" in why
    assert not arbiter.should_hold_accept(FakeBazaar([days_duel(85, None)]), 102)[0]  # no day: our worst, -20
    assert arbiter.should_hold_accept(FakeBazaar([days_duel(95, 5, weight={"x": 1})]), 103)[0]   # unreadable


def test_finished_duels_are_ignored():
    assert not arbiter.should_hold_accept(FakeBazaar([duel(rival=80, status="deal")]), 100)[0]


def test_duels_read_once_per_tick():
    b = FakeBazaar([duel(rival=120, deadline=130)])
    for _ in range(3):
        arbiter.should_hold_accept(b, 100)
    assert b.calls["duels"] == 1
    arbiter.should_hold_accept(b, 101)
    assert b.calls["duels"] == 2


def test_without_tick_reads_the_clock():
    b = FakeBazaar([duel(rival=None, deadline=102)], tick=100)
    assert arbiter.should_hold_accept(b)[0]
    assert b.calls["clock"] == 1


def test_read_failure_keeps_the_last_state():
    assert arbiter.should_hold_accept(FakeBazaar([duel(rival=80)]), 100)[0]
    hold, why = arbiter.should_hold_accept(FakeBazaar([], fail=True), 101)
    assert hold and "read failed" in why
    arbiter.reset()
    assert not arbiter.should_hold_accept(FakeBazaar([], fail=True), 101)[0]


# ---- the dealer bot holds her final offer while a scored duel needs the accept

class FakeDealerBazaar:
    """A dealer thread whose standing offer is final and inside our cap."""

    def __init__(self):
        self.accepted, self.status = [], "open"

    def thread(self, tid):
        offer = {"id": 55, "maker": "abuela", "status": "open", "final": True, "want": {"cash": 10},
                 "give": {"types": ["card:LAV-01"]}}
        return {"status": self.status, "messages": [],
                "standing_offers": [offer] if self.status == "open" else []}

    def accept(self, oid):
        self.accepted.append(oid)
        self.status = "deal"

    def wait_tick(self):
        return {}


def test_abuela_holds_a_final_offer_until_the_duel_no_longer_needs_the_accept(tmp_path, monkeypatch):
    sys.path.insert(0, str(ROOT / "agents" / "dealers"))
    import abuela_bot
    monkeypatch.setattr(abuela_bot, "LOG", tmp_path / "abuela.jsonl")
    answers = iter([(True, "duel 7: 2 tick(s) left"), (False, "no live duel")])
    monkeypatch.setattr(abuela_bot, "should_hold_accept", lambda b: next(answers))
    b = FakeDealerBazaar()
    t = abuela_bot.negotiate(b, {"buy": {"card": "LAV-01"}}, "buy", cap=12, tid=9)
    assert t["status"] == "deal" and b.accepted == [55]
    events = [json.loads(x)["event"] for x in (tmp_path / "abuela.jsonl").read_text().splitlines()]
    assert events.index("hold_accept_duel") < events.index("accept")


# ------------------------------------------------------------------ ARBITER_HOLDS off (the default since 13:00)

def test_off_by_default_never_holds_but_logs_what_it_would_have_held(monkeypatch, tmp_path):
    monkeypatch.delenv("ARBITER_HOLDS")
    b = FakeBazaar([duel(rival=80, limit=100)])
    hold, why = arbiter.should_hold_accept(b, 100)
    assert hold is False and why.startswith("would have held: duel 7: rival offer 80 inside our limit")
    arbiter.should_hold_accept(b, 100)                               # same tick, same reason: one line
    arbiter.should_hold_accept(b, 101)
    lines = [json.loads(x) for x in (tmp_path / "arbiter.jsonl").read_text().splitlines()]
    assert [(x["tick"], x["event"]) for x in lines] == [(100, "would_have_held"), (101, "would_have_held")]
    assert arbiter.should_hold_accept(FakeBazaar([]), 102) == (False, "no live duel")   # nothing to hold: no line
    assert len((tmp_path / "arbiter.jsonl").read_text().splitlines()) == 2


def test_on_holds_and_logs_nothing(monkeypatch, tmp_path):
    for v in ("1", "on", "true"):
        monkeypatch.setenv("ARBITER_HOLDS", v)
        arbiter.reset()
        assert arbiter.should_hold_accept(FakeBazaar([duel(rival=80, limit=100)]), 100)[0] is True
    assert not (tmp_path / "arbiter.jsonl").exists()
    monkeypatch.setenv("ARBITER_HOLDS", "0")
    assert arbiter.should_hold_accept(FakeBazaar([duel(rival=80, limit=100)]), 101)[0] is False
