"""Duels II's real day payloads (Sat 21:20, /api/duels): the game's words name no early/late, only adds/costs."""
from agents.duelist import days

SELL = "each delivery day adds this much cash to your side"
BUY = "each delivery day costs you this much cash"


def test_seller_adds_prefers_late():
    for w in (3.19, 2.0, 7.5):
        v = days.read_days(w, SELL, mode="auto")
        assert v is not None and v.sure
        assert v.best == 10
        assert v.values[10] == 0.0
        assert abs(v.values[0] + 10 * w) < 1e-6


def test_buyer_costs_prefers_early():
    for w in (4.63, 5.01, 1.0):
        v = days.read_days(w, BUY, mode="auto")
        assert v is not None and v.sure
        assert v.best == 0
        assert v.values[0] == 0.0
        assert abs(v.values[10] + 10 * w) < 1e-6


def test_flip_reverses_game_words():
    assert days.read_days(3.19, SELL, mode="flip").best == 0
    assert days.read_days(4.63, BUY, mode="flip").best == 10


def test_old_phrasings_unchanged():
    assert days.direction("each day later costs you 2") == "early"
    assert days.direction("each day earlier costs you 2") == "late"
    assert days.direction("you prefer early delivery, each day costs 2") == "early"
    assert days.direction("0 (soonest) to 10 (latest)") is None
    assert days.direction("the day doesn't matter") is None
