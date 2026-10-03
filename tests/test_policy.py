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


ME_LAV = {"id": "t05", "album": {"pages": [{"set": "LAV", "have": 10, "of": 10, "complete": True},
                                           {"set": "SAL", "have": 4, "of": 10, "complete": False}]},
          "assets": [{"id": 65, "kind": "card", "ref": "LAV-03"}, {"id": 66, "kind": "card", "ref": "LAV-03"},
                     {"id": 70, "kind": "card", "ref": "SAL-02"}]}


def test_never_the_last_copy_of_a_complete_page_counting_open_offers_as_gone():
    # Sat 17:05 (Operator): LAV-03's other copy sits in a book ask while a Workshop conversion could use the free one.
    assert policy.last_copy(ME_LAV, "LAV-03", committed_ids={65}, giving={66})
    assert policy.last_copy(ME_LAV, "LAV-03", committed_ids=set(), giving={66}) == ""    # nothing committed: a spare
    assert policy.last_copy(ME_LAV, "SAL-02", giving={70}) == ""                         # SAL's page isn't complete
    offers = [{"maker": "t05", "status": "open", "give": {"assets": [{"id": 65}]}},
              {"maker": "t09", "status": "open", "give": {"assets": [{"id": 1}]}}]
    assert policy.committed(offers) == {65}
