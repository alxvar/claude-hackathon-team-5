"""Offline tests for agents/dealers/abuela_bot.py: the dealer hard limits (never a page-completing card, value − 4
with an unopened pack held), closing the conversation on an exception, and request pacing. The game is a fake;
nothing is sent anywhere."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "agents" / "dealers"))
sys.path.insert(0, str(ROOT / "bazaar-kit"))
import abuela_bot as ab  # noqa: E402
import bazaar_sdk  # noqa: E402
from bazaar_sdk import BazaarError  # noqa: E402

AFF = {"RET": 1.1, "LAV": 1.3}
PAGE_LAST = 11 + 72.9   # RET-02 is the last card our RET page misses: book × 1.1 + page bonus 66.25 × 1.1


class FakeGame:
    """The game, read side only, plus a record of every negotiation the bot would start."""

    def __init__(self, values=None, packs=0, cash=400):
        self.values = dict(values or {"RET-01": 11.0, "RET-02": PAGE_LAST, "RET-03": 27.5, "LAV-01": 3.25})
        assets = [{"id": 1, "kind": "card", "ref": "LAV-01", "rarity": "common", "your_value": 13.0},
                  {"id": 2, "kind": "card", "ref": "LAV-01", "rarity": "common", "your_value": 3.25}]
        assets += [{"id": 900 + i, "kind": "pack", "ref": "sobre_barrio"} for i in range(packs)]
        self._me = {"id": "t05", "cash": cash, "affinity": AFF, "assets": assets, "score": {}}
        self.value_calls = []

    def me(self):
        return self._me

    def my_offers(self):
        return {"offers": []}

    def catalog(self):
        return {"sets": [
            {"id": "RET", "released": True, "cards": [
                {"id": "RET-01", "rarity": "common", "book": 10},
                {"id": "RET-02", "rarity": "common", "book": 10},
                {"id": "RET-03", "rarity": "uncommon", "book": 25},
                {"id": "RET-08", "rarity": "rare", "book": 70}]},
            {"id": "LAV", "released": True, "cards": [{"id": "LAV-01", "rarity": "common", "book": 10}]},
            {"id": "CHA", "released": False, "cards": [{"id": "CHA-01", "rarity": "common", "book": 10}]}]}

    def dealer(self, dealer_id):
        return {"menu": {"sells": [{"rarity": "common", "list_price": 8}, {"rarity": "uncommon", "list_price": 25},
                                   {"pack": "sobre_barrio", "list_price": 30}]}}

    def value(self, card):
        self.value_calls.append(card)
        return {"card": card, "your_value": self.values[card]}

    def clock(self):
        return {"tick": 200, "tick_seconds": 30.0}

    def my_threads(self):
        return {"threads": []}


@pytest.fixture
def bot(tmp_path, monkeypatch):
    monkeypatch.setattr(ab, "LOG", tmp_path / "abuela.jsonl")
    monkeypatch.setattr(ab, "should_hold_accept", lambda b, tick=None: (False, "no live duel"))
    monkeypatch.setenv("BAZAAR_KEY", "test-key-not-real")
    return ab


def run_main(bot, monkeypatch, game, *argv, after_deal=None):
    """main() on the fake game; each negotiation is recorded and ends in a deal (no thread is opened)."""
    started = []
    monkeypatch.setattr(bot, "PacedBazaar", lambda url, key, min_gap, **kw: game)

    def fake_negotiate(b, topic, side, cap, tid=None, fast=False):
        started.append((topic, side, cap))
        if after_deal:
            after_deal(topic)
        return {"id": len(started), "status": "deal"}
    monkeypatch.setattr(bot, "negotiate", fake_negotiate)
    bot.main(["--cash-floor", "200", *argv])
    return started


def cards_bought(started):
    return [t["buy"]["card"] for t, side, cap in started if side == "buy"]


# ------------------------------------------------------------------------------------------------ page bonus

def test_page_bonus_rule():
    assert ab.page_bonus(PAGE_LAST, 10, 1.1)
    assert not ab.page_bonus(11.0, 10, 1.1)
    assert not ab.page_bonus(11.5, 10, 1.1)            # within the 0.5 slack: no bonus
    assert ab.page_bonus(11.6, 10, 1.1)


def test_plan_never_lists_a_page_completing_card(bot):
    game = FakeGame()
    me, sells, buys, budget, cards, blocked = bot.plan(game)
    assert "RET-02" not in [c for _, _, c in buys]
    assert blocked == [("RET-02", PAGE_LAST)]
    assert [c for _, _, c in buys] == ["RET-03", "RET-01"]   # 27.5 − 23 = 4.5; 11 − 7.36 = 3.6
    assert "CHA-01" not in game.value_calls and "RET-08" not in game.value_calls  # unreleased; rare not on her menu


def test_buy_run_never_negotiates_a_page_completing_card(bot, monkeypatch):
    started = run_main(bot, monkeypatch, FakeGame(), "--deals", "5")
    assert "RET-02" not in cards_bought(started)
    assert cards_bought(started) == ["RET-03", "RET-01"]


def test_ladder_never_negotiates_a_page_completing_card(bot, monkeypatch):
    started = run_main(bot, monkeypatch, FakeGame(), "--ladder", "--deals", "5")
    assert cards_bought(started) == ["RET-01", "RET-03"]     # cheapest menu rarity first; RET-02 skipped
    log = (bot.LOG).read_text()
    assert '"skip_ladder"' in log and "RET-02" in log


def test_a_card_that_becomes_a_page_closer_mid_run_is_skipped(bot, monkeypatch):
    """Buying RET-03 leaves RET-01 as the page's last card: the fresh lookup before the next buy refuses it."""
    game = FakeGame()

    def after_deal(topic):
        if topic["buy"]["card"] == "RET-03":
            game.values["RET-01"] = 11 + 72.9
    started = run_main(bot, monkeypatch, game, "--deals", "5", after_deal=after_deal)
    assert cards_bought(started) == ["RET-03"]
    assert any(json.loads(x).get("event") == "skip_buy" and x.count("page bonus") for x in bot.LOG.read_text().splitlines())


def test_ladder_rechecks_the_value_before_each_deal(bot, monkeypatch):
    game = FakeGame(values={"RET-01": 11.0, "RET-02": 10.5, "RET-03": 27.5, "LAV-01": 3.25})

    def after_deal(topic):
        if topic["buy"]["card"] == "RET-01":
            game.values["RET-02"] = PAGE_LAST
    started = run_main(bot, monkeypatch, game, "--ladder", "--deals", "5", after_deal=after_deal)
    assert "RET-02" not in cards_bought(started)


def test_resume_refuses_a_page_completing_card(bot, monkeypatch):
    game = FakeGame()
    closed = []
    game.my_threads = lambda: {"threads": [{"id": 77, "with": "abuela", "status": "open",
                                            "topic": {"buy": {"card": "RET-02"}}}]}
    game.close_thread = lambda tid: closed.append(tid)
    started = run_main(bot, monkeypatch, game, "--resume-cap", "60", "--no-buy")
    assert started == [] and closed == [77]


# ------------------------------------------------------------------------------------------------ packs: value − 4

def test_hard_cap():
    assert ab.hard_cap(27.5, 0) == 27 and ab.hard_cap(27.5, 1) == 23 and ab.hard_cap(27.5, 3) == 23
    assert ab.packs_held(FakeGame(packs=2).me()) == 2 and ab.packs_held(FakeGame().me()) == 0


def test_buy_caps_without_and_with_an_unopened_pack(bot, monkeypatch):
    no_pack = run_main(bot, monkeypatch, FakeGame(), "--deals", "5")
    assert [(t["buy"]["card"], cap) for t, _, cap in no_pack] == [("RET-03", 24), ("RET-01", 8)]   # value − 3 margin
    with_pack = run_main(bot, monkeypatch, FakeGame(packs=1), "--deals", "5")
    assert [(t["buy"]["card"], cap) for t, _, cap in with_pack] == [("RET-03", 23), ("RET-01", 7)]  # value − 4


def test_ladder_cap_with_an_unopened_pack(bot, monkeypatch):
    game = FakeGame(values={"RET-01": 11.0, "RET-02": 9.0, "RET-03": 27.5, "LAV-01": 3.25}, packs=1)
    game.dealer = lambda d: {"menu": {"sells": [{"rarity": "uncommon", "list_price": 40}]}}
    started = run_main(bot, monkeypatch, game, "--ladder", "--deals", "1")
    assert [(t["buy"]["card"], cap) for t, _, cap in started] == [("RET-03", 23)]   # not 26 (value − 1) nor 36 (90% list)


def test_dry_run_starts_nothing(bot, monkeypatch, capsys):
    started = run_main(bot, monkeypatch, FakeGame(packs=1), "--dry-run")
    out = capsys.readouterr().out
    assert started == [] and "never buy (page bonus" in out and "RET-02" in out and "value − 4" in out


# ------------------------------------------------------------------------------------------------ errors close the thread

class FakeThread:
    """A dealer conversation. `fail` raises inside the haggling loop."""

    def __init__(self, fail=None, accept_then_fail=None):
        self.fail, self.accept_then_fail = fail, accept_then_fail
        self.closed, self.accepted, self.opened = [], [], []

    def open_thread(self, with_, topic=None):
        self.opened.append(topic)
        return {"id": 42}

    def thread(self, tid):
        if self.fail:
            raise self.fail
        return {"status": "open", "messages": [], "standing_offers": [
            {"id": 5, "maker": "abuela", "status": "open", "final": True, "want": {"cash": 9}}]}

    def accept(self, oid):
        self.accepted.append(oid)

    def wait_tick(self):
        if self.accept_then_fail:
            raise self.accept_then_fail
        return {}

    def close_thread(self, tid):
        self.closed.append(tid)


def events(bot):
    return [json.loads(x)["event"] for x in bot.LOG.read_text().splitlines()]


def test_an_exception_closes_the_thread_and_returns_error(bot):
    b = FakeThread(fail=BazaarError("network", "GET /api/threads/42: timed out"))
    t = bot.negotiate(b, {"buy": {"card": "RET-01"}}, "buy", 10)
    assert t["status"] == "error" and t["id"] == 42 and b.closed == [42]
    assert events(bot)[-2:] == ["error", "closed_after_error"]


def test_ctrl_c_closes_the_thread_then_propagates(bot):
    b = FakeThread(fail=KeyboardInterrupt())
    with pytest.raises(KeyboardInterrupt):
        bot.negotiate(b, {"buy": {"card": "RET-01"}}, "buy", 10)
    assert b.closed == [42]


def test_a_failed_close_is_logged_not_raised(bot):
    b = FakeThread(fail=ValueError("bad json"))

    def refuse(tid):
        raise BazaarError("not_found", "no thread")
    b.close_thread = refuse
    assert bot.negotiate(b, {"buy": {"card": "RET-01"}}, "buy", 10)["status"] == "error"
    assert "close_failed" in events(bot)


def test_after_an_accept_the_thread_is_left_to_settle(bot):
    b = FakeThread(accept_then_fail=BazaarError("network", "clock"))
    t = bot.negotiate(b, {"buy": {"card": "RET-01"}}, "buy", 10)
    assert t["status"] == "error" and b.accepted == [5] and b.closed == []
    assert "left_open_after_accept" in events(bot)


def test_an_error_stops_the_run(bot, monkeypatch):
    game = FakeGame()
    monkeypatch.setattr(bot, "PacedBazaar", lambda url, key, min_gap, **kw: game)
    started = []

    def failing(b, topic, side, cap, tid=None, fast=False):
        started.append(topic)
        return {"id": 1, "status": "error", "error": "boom"}
    monkeypatch.setattr(bot, "negotiate", failing)
    bot.main(["--deals", "5", "--sell-spares"])
    assert len(started) == 1 and "halt" in events(bot)


# ------------------------------------------------------------------------------------------------ pacing

def test_requests_are_paced(monkeypatch):
    t, slept, calls = [100.0], [], []
    monkeypatch.setattr(ab.time, "monotonic", lambda: t[0])
    monkeypatch.setattr(ab.time, "sleep", lambda s: slept.append(s))
    monkeypatch.setattr(bazaar_sdk._Http, "_call", lambda self, *a, **k: calls.append(a) or {"your_value": 1})
    b = ab.PacedBazaar("http://127.0.0.1:9", "k", min_gap=0.25)
    b.value("RET-01")
    t[0] += 0.1
    b.value("RET-02")
    t[0] += 1.0
    b.value("RET-03")
    assert len(calls) == 3 and slept == [pytest.approx(0.15)]


# ------------------------------------------------------------------------------------------------ 429: wait a tick

class BusyTick(FakeThread):
    """The team's one acceptance is taken this tick: the first accept is refused with wait_for_tick (a 429)."""

    def __init__(self):
        super().__init__()
        self.refused = False

    def accept(self, oid):
        if not self.refused:
            self.refused = True
            raise BazaarError("wait_for_tick", "one acceptance per team per tick")
        self.accepted.append(oid)

    def thread(self, tid):
        if self.accepted:
            return {"status": "deal", "closed_reason": "deal", "messages": [], "standing_offers": []}
        return super().thread(tid)


def test_a_refused_accept_waits_a_tick_and_asks_the_duel_arbiter_again(bot, monkeypatch):
    asked = []
    monkeypatch.setattr(bot, "should_hold_accept", lambda b, tick=None: asked.append(1) or (False, "no live duel"))
    b = BusyTick()
    t = bot.negotiate(b, {"buy": {"card": "RET-01"}}, "buy", 10)
    assert t["status"] == "deal" and b.accepted == [5] and b.closed == []   # not closed as an error
    assert len(asked) == 2 and "accept_waits" in events(bot)              # the retry went through the arbiter
