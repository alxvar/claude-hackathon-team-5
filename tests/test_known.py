"""tools/known.py (run/known_holdings.json, Chief 21:50) and its use in the radar's giver/receiver rules."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bazaar-kit"))
import known  # noqa: E402
import v10_radar as vr  # noqa: E402

K = {"t15": {"complete": {"LAT", "RET", "LAV"}, "missing": {"MAL-09", "MAL-10"}}}


class Dumps:
    def allows(self, team, set_id):
        return False, f"{team} dumps {set_id} (teams.md)"


class Collects:
    def allows(self, team, set_id):
        return True, "collects"


def test_load_ignores_notes_and_bad_entries(tmp_path):
    f = tmp_path / "k.json"
    f.write_text('{"_note": "x", "t15": {"complete": ["lat"], "missing": ["MAL-09", "bad"]}, "t1": {}}')
    assert known.load(f) == {"t15": {"complete": {"LAT"}, "missing": {"MAL-09"}}}
    assert known.load(tmp_path / "absent.json") == {}


def test_holds_and_buys():
    assert known.holds(K, "t15", "RET-03") is True and known.holds(K, "t15", "MAL-04") is True
    assert known.holds(K, "t15", "MAL-09") is False and known.holds(K, "t15", "SAL-01") is None
    assert known.holds(K, "t15", "RET-11") is None and known.holds(K, "t09", "RET-03") is None
    assert known.buys(K, "t15", "MAL-10") is True and known.buys(K, "t15", "RET-03") is False
    assert known.buys(K, "t09", "RET-03") is None


def test_apply_overrides_the_feed():
    pages = {"MAL": [f"MAL-{i:02d}" for i in range(1, 11)], "RET": [f"RET-{i:02d}" for i in range(1, 11)]}
    n = known.apply({("t15", "MAL-09"): 1, ("t15", "RET-02"): 3}, K, pages)
    assert ("t15", "MAL-09") not in n and n[("t15", "RET-02")] == 3 and n[("t15", "RET-05")] == 1
    assert n[("t15", "MAL-01")] == 1 and ("t15", "MAL-10") not in n


def test_radar_receiver_takes_only_known_wants_and_a_complete_page_keeps_its_copy():
    ok = vr.receiver_ok("t15", "RET-03", held={}, last={}, prof={}, collectors=Collects(), known=K)
    assert not ok[0] and "doesn't need" in ok[1]
    assert vr.receiver_ok("t15", "MAL-09", held={("t15", "MAL-09"): {1}}, last={}, prof={}, collectors=Collects(),
                          known=K)[0]                                    # what it told us beats a stale feed copy
    assert not vr.giver_ok("t15", "RET-03", held={("t15", "RET-03"): {7}}, collectors=Dumps(), known=K)[0]
    assert vr.giver_ok("t15", "RET-03", held={("t15", "RET-03"): {7, 8}}, collectors=Dumps(), known=K)[0]
    assert not vr.giver_ok(None, "RET-03", held={}, collectors=Dumps())[0]   # an unknown giver: drop
