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


def test_seller_bonus_counted_from_day_zero():
    # duel 5616: sold at 105 vs limit 69 at day 0 → the game scored the margin alone (33.1 = 36 x 0.92)
    v = days.read_days(3.19, SELL, mode="auto")
    assert abs(v.offset - 31.9) < 1e-6
    assert abs(v(0) + v.offset) < 1e-6              # day 0 adds 0 in the game's terms
    assert abs(v(10) + v.offset - 31.9) < 1e-6      # day 10 adds 10 x w
    assert abs(v(5) + v.offset - 15.95) < 1e-6


def test_buyer_and_overrides_have_no_offset():
    assert days.read_days(4.63, BUY, mode="auto").offset == 0.0
    assert days.read_days(3.19, SELL, mode="flip").offset == 0.0
    assert days.read_days(3.19, SELL, mode="unsure").offset == 0.0
    assert days.read_days(2.0, "each day later costs you 2").offset == 0.0


def test_guard_accepts_seller_day_zero_inside_limit():
    from types import SimpleNamespace
    from agents.duelist import guards
    view = SimpleNamespace(day_values=days.read_days(3.19, SELL, mode="auto"), role="seller", limit=69)
    assert guards.day_value(view, 0) == 0.0
    assert abs(guards.day_value(view, 10) - 31.9) < 1e-6
