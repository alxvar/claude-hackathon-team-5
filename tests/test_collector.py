"""Collector rows in data/me.jsonl: the score parts and our venue's numbers the Analyst fits the market hurdle on."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "bazaar-kit"))
import collector  # noqa: E402

ME = {"tick": 470, "cash": 109, "level": 2,
      "score": {"score": 23.61, "rank": 7, "negotiating": 16.11, "market": 7.5, "neg_points": 35.2,
                "mm_points": -5.2, "duel_points": 0.78, "ladder_points": 0.055, "bench_efficiency": 0.933,
                "bench_points": 0.5, "deals": 35},
      "venue": {"venue": "v10", "value_created": 9.0, "trades": 2, "traders": 3, "volume": 40}}


def test_a_row_carries_mm_points_bench_points_and_value_created():
    row = collector.me_row(ME, t=1.0)
    assert row["mm_points"] == -5.2 and row["bench_points"] == 0.5
    assert row["venue_value_created"] == 9.0 and row["venue_trades"] == 2 and row["venue_traders"] == 3
    assert row["neg_points"] == 35.2 and row["cash"] == 109 and row["t"] == 1.0


def test_no_venue_logs_none_not_a_crash():
    row = collector.me_row({**ME, "venue": None}, t=1.0)
    assert row["venue_value_created"] is None and row["mm_points"] == -5.2


def test_a_value_created_change_alone_logs_a_row_a_tick_alone_does_not():
    last = collector.me_row(ME, t=1.0)
    assert not collector.changed(collector.me_row({**ME, "tick": 471}, t=2.0), last)
    moved = {**ME, "venue": {**ME["venue"], "value_created": 14.2}}
    assert collector.changed(collector.me_row(moved, t=2.0), last)
    assert collector.changed(last, None)
