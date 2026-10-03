"""Offline tests for tools/v10_radar.py: fake public API and feed, no network, no notifications sent."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "bazaar-kit"))
import v10_radar as vr  # noqa: E402

CATALOG = {"sets": [{"id": "SAL", "cards": [{"id": f"SAL-{i:02d}", "rarity": r, "book": b, "name": f"Card {i}"}
                                            for i, r, b in ((1, "common", 10), (2, "common", 10), (3, "common", 10),
                                                            (6, "uncommon", 25), (7, "uncommon", 25))]}]}
TEAMS = [{"team": "t18", "name": "Team 18", "score": 30}, {"team": "t13", "name": "Team 13", "score": 28},
         {"team": "t12", "name": "Team 12", "score": 27}, {"team": "t02", "name": "Team 2", "score": 26},
         {"team": "t05", "name": "Team 5", "score": 24}, {"team": "t16", "name": "Team 16", "score": 12},
         {"team": "t17", "name": "Team 17", "score": 21}, {"team": "t06", "name": "Team 6", "score": 11},
         {"team": "t10", "name": "Team 10", "score": 10}, {"team": "t03", "name": "Team 3", "score": 13}]
ASK = {"id": 900, "maker": "m1", "to": None, "give": {"cash": 0, "assets": [{"id": 1, "ref": "SAL-07"}]},
       "want": {"cash": 24}}


def ev(eid, tick, typ, actor, payload):
    return {"id": eid, "tick": tick, "t": tick / 120, "type": typ, "actor": actor, "payload": payload}


def bid(eid, team, card, cash):
    return ev(eid, 100, "offer.listed", team, {"offer": {"id": eid, "maker": team, "give": {"cash": cash},
                                                         "want": {"types": [f"card:{card}"]}}})


EVENTS = [ev(1, 90, "offer.listed", "t04", {"offer": {"id": 900, "maker": "t04", "give": {"assets": [{"ref": "SAL-07"}]},
                                                      "want": {"cash": 24}}}),
          bid(2, "t16", "SAL-07", 20), bid(3, "t16", "SAL-01", 8), bid(4, "t16", "SAL-02", 8),   # t16: far below, lacks 3
          bid(5, "t17", "SAL-07", 20),                                                       # t17: 3 below us, lacks only it
          bid(6, "t13", "SAL-07", 22),                                                       # top 4
          ev(7, 100, "settlement", "", {"items": [{"kind": "card", "ref": "SAL-07", "frm": "t09", "to": "t06"}],
                                        "price": 20}),                                       # t06 holds one
          bid(8, "t10", "SAL-07", 20)]                                                       # t10 dumps SAL
MULT = {"t04": {"SAL": 0.7}, "t16": {"SAL": 1.3}, "t17": {"SAL": 1.6}, "t13": {"SAL": 1.6}, "t06": {"SAL": 1.6},
        "t10": {"SAL": 1.5}}


class Pub:
    def __init__(self, board):
        self.board = board

    def _call(self, method, path, *a, **k):
        return {"/api/catalog": CATALOG, "/api/leaderboard": {"teams": [dict(t) for t in TEAMS]},
                "/api/clock": {"tick": 110}}.get(path) or {"offers": self.board}


class Col:
    def get(self):
        return self

    def allows(self, team, set_id):
        if team == "t10":
            return False, "t10 dumps SAL (teams.md)"
        return team in ("t16", "t17", "t13", "t06"), "collects"


def radar(tmp_path, board, **kw):
    sent = []
    r = vr.Radar(Pub(board), events_fn=lambda: list(EVENTS), mult_fn=lambda: MULT, collectors=Col(),
                 notifier=lambda *a, **k: sent.append(a), out=tmp_path / "radar.md", state=tmp_path / "s.json",
                 log=lambda *a: None, **kw)
    return r, sent


def test_the_buyer_that_lacks_the_card_and_values_the_set_gets_the_dm(tmp_path):
    r, sent = radar(tmp_path, [ASK])
    found = r.scan()
    assert [f["team"] for f in found] == ["t16"]                      # not t13 (top 4), t17 (page, 3 below us),
    f = found[0]                                                       # t06 (holds it), t10 (dumps SAL)
    assert f["seller"] == "t04" and f["lacks"] and f["vc"] == 15.0     # 25 × (1.3 − 0.7)
    (channel, title, body), = sent
    assert channel == "lucas" and "Team 16" in title
    assert "Hi Team 16! There's Card 7 (SAL-07) for 24 P on the market v10 (0% fee), in case you need it for your " \
           "Salamanca page." in body
    assert "Team 16" in (tmp_path / "radar.md").read_text()
    r.scan()
    assert len(sent) == 1                                              # once per (ask, buyer)


def test_dry_and_empty_board(tmp_path):
    r, sent = radar(tmp_path, [ASK], dry=True)
    assert r.scan() and sent == [] and not (tmp_path / "radar.md").exists()
    r, sent = radar(tmp_path, [])
    assert r.scan() == [] and sent == []



def test_a_high_multiplier_team_selling_a_duplicate_creates_value():
    # Analyst 12:05 [V]: t15 (LAT ~1.45) sold duplicates to t12 (~0.8): +4.36 and +2.76 on other venues.
    ask = {"id": 77, "give": {"assets": [{"ref": "SAL-06"}]}, "want": {"cash": 24}}
    held = {("t15", "SAL-06"): {501, 502}}                               # the seller holds two copies
    teams = [{"team": "t16", "name": "Team 16", "score": 5, "rank": 9}, {"team": "t05", "score": 24}]
    class Ok:
        def allows(self, team, set_id):
            return True, "collects"
    b = vr.buyers_for(ask, seller="t15", teams=teams, top=set(), ours=24, last={("t16", "SAL-01"): {"kind": "lack"},
                      ("t16", "SAL-02"): {"kind": "lack"}}, prof={}, mult={"t15": {"SAL": 1.45}, "t16": {"SAL": 0.8}},
                      collectors=Ok(), cards=vr.card_index(CATALOG), held=held)
    assert b and b[0]["team"] == "t16" and b[0]["c_seller"] == 0.25
    assert b[0]["vc"] == round(25 * (0.8 * 1.0 - 1.45 * 0.25), 1)        # +10.9; with first copies it would be < 0
