"""Counterparty policy (tools/policy.py, Chief Sat 16:20)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import policy  # noqa: E402

TEAMS = [{"team": t, "score": s} for t, s in (("t14", 30), ("t18", 29.5), ("t12", 29), ("t10", 28.5), ("t05", 28),
                                              ("t13", 27), ("t17", 26), ("t03", 22), ("t16", 10))]


def test_the_top_5_only_at_3x_their_gain():
    assert not policy.check("t14", teams=TEAMS, our_gain=8, their_gain=3)[0]      # 8 < 9
    assert policy.check("t14", teams=TEAMS, our_gain=9, their_gain=3)[0]
    assert not policy.check("t14", teams=TEAMS, our_gain=40)[0]                   # theirs unknown: skip


def test_rivals_never_with_their_gain_above_ours():
    assert not policy.check("t13", teams=TEAMS, our_gain=4, their_gain=5)[0]
    assert policy.check("t13", teams=TEAMS, our_gain=5, their_gain=4)[0]
    assert not policy.check("t17", teams=TEAMS, our_gain=5)[0]


def test_a_page_closer_needs_6_points_below_us():
    assert policy.PAGE_CLOSER_GAP == 6
    assert policy.check("t03", teams=TEAMS, page_closer=True)[0]                 # 6 below
    assert not policy.check("t03", teams=TEAMS[:-2] + [{"team": "t03", "score": 22.5}], page_closer=True)[0]
    assert not policy.check("t99", teams=TEAMS, page_closer=True)[0]             # unknown score
    assert policy.check("t16", teams=TEAMS)[0] and not policy.check("t16", teams=[])[0]
