"""PLAN #24: the --days-read override (auto | flip | unsure) for the duelist's day reading."""
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agents.duelist import days  # noqa: E402

WEIGHTS = [(2, "each day later costs you 2"), (-2, None), (3, None), ([0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0], None),
           ({"per_day": 1.5, "best_day": 3}, None), ({"days": 2, "prefer": "late"}, None), ("2 per day, prefer early", None),
           ({"weird": 1}, None), (None, None)]


@pytest.fixture(autouse=True)
def _mode(monkeypatch):
    monkeypatch.setattr(days, "MODE", "auto")


def test_auto_is_todays_reading_exactly():
    for w, m in WEIGHTS:
        assert days.read_days(w, m) == days._read_days(w, m)


def test_flip_reads_a_backwards_weight_right():
    # Red team "direction backwards": a signed weight whose sign convention is the opposite of ours. We read -2 as
    # "early days are worth more"; the truth is late. Flipped, our day values equal the right reading's exactly, so
    # every decision (and the score) is the "read right" one.
    backwards = days.read_days(-2)
    right = days._per_day(2, "late", "right")
    assert backwards.values != right.values and backwards.best == 0
    flipped = days.read_days(-2, mode="flip")
    assert flipped.values == right.values and flipped.sure and flipped.best == 10
    days.set_mode("flip")                                              # the process mode, as the CLI sets it
    assert days.read_days(-2).values == right.values


def test_unsure_is_the_safe_direction_unknown_mode():
    for w, m in WEIGHTS:
        v = days.read_days(w, m, mode="unsure")
        assert v is None or v.sure is False
    assert days.read_days(3, mode="unsure").values == days._per_day(3, None, "x").values   # = "direction unknown"
    assert days.read_days(None, mode="unsure") is None


def test_the_mode_comes_from_the_cli_or_the_environment():
    with pytest.raises(ValueError):
        days.set_mode("sideways")
    env = {**os.environ, "DAYS_READ": "unsure", "PYTHONPATH": str(ROOT)}
    out = subprocess.run([sys.executable, "-c", "from agents.duelist import days; print(days.MODE)"], env=env,
                         capture_output=True, text=True, cwd=ROOT)
    assert out.stdout.strip() == "unsure"
    env["DAYS_READ"] = "nonsense"
    out = subprocess.run([sys.executable, "-c", "from agents.duelist import days; print(days.MODE)"], env=env,
                         capture_output=True, text=True, cwd=ROOT)
    assert out.stdout.strip() == "auto"
