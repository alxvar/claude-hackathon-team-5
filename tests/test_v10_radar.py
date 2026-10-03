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
    kw.setdefault("mult_file", tmp_path / "no-multipliers.json")
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



def test_the_analysts_multipliers_win_where_confident_and_the_conservative_estimate_gates(tmp_path):
    import json
    f = tmp_path / "multipliers.json"
    f.write_text(json.dumps({"_meta": {}, "t15": {"LAT": {"m": 1.45, "lo": 1.3, "hi": 1.6, "conf": "L"}},
                             "t12": {"LAT": {"m": 0.8, "lo": 0.7, "hi": 0.9, "conf": "L"},
                                     "MAL": {"m": 1.6, "lo": 1.6, "hi": 1.6, "conf": "?"}}}))
    m = vr.load_mult({"t12": {"LAT": 1.4, "MAL": 0.9}}, f)
    assert m["t12"]["LAT"] == (0.8, 0.7, 0.9) and m["t12"]["MAL"] == (0.9, 0.9, 0.9)   # "?" keeps the hub's
    cat = {"sets": [{"id": "LAT", "cards": [{"id": "LAT-07", "rarity": "uncommon", "book": 25}]}]}
    ask = {"id": 5, "give": {"assets": [{"ref": "LAT-07"}]}, "want": {"cash": 20}}

    class Ok:
        def allows(self, team, set_id):
            return True, "collects"
    teams = [{"team": "t12", "name": "Team 12", "score": 5, "rank": 12}]
    kw = dict(teams=teams, top=set(), ours=24, last={("t12", "LAT-07"): {"kind": "lack"}}, prof={}, mult=m,
              collectors=Ok(), cards=vr.card_index(cat))
    # t15 sells its 2nd copy (0.25): 25 x (0.8 - 1.45 x 0.25) = +10.9, at least 25 x (0.7 - 1.6 x 0.25) = +7.5
    b = vr.buyers_for(ask, seller="t15", held={("t15", "LAT-07"): {1, 2}}, **kw)
    assert b and b[0]["vc"] == 10.9 and b[0]["vc_low"] == 7.5
    # its only copy: value destroyed, no DM
    assert vr.buyers_for(ask, seller="t15", held={("t15", "LAT-07"): {1}}, **kw) == []


# ------------------------------------------------------------ addressed offers on v10 (hidden from the public board)

def listed(eid, tick, oid, maker, to, give, want, expires=30):
    return ev(eid, tick, "offer.listed", maker, {"offer": {"id": oid, "maker": maker, "to": to, "venue": "v10",
                                                           "give": give, "want": want, "created_tick": tick,
                                                           "expires_tick": tick + expires}})


ASK_TO = ({"cash": 0, "assets": [{"id": 366, "ref": "SAL-03"}]}, {"cash": 13})


def test_open_addressed_drops_cancelled_expired_and_settled_offers():
    events = [listed(1, 10, 7987, "t10", "t03", *ASK_TO), listed(2, 10, 7988, "t10", "t17", *ASK_TO),
              listed(3, 10, 7989, "t10", "t06", *ASK_TO, expires=5), listed(4, 10, 7990, "t10", None, *ASK_TO),
              listed(5, 10, 7991, "t10", "t05", *ASK_TO),
              ev(6, 11, "offer.cancelled", "", {"offer": 7988, "venue": "v10"})]
    assert [o["id"] for o in vr.open_addressed(events, 20)] == [7987]   # 7989 expired, 7990 public, 7991 is to us
    events.append(ev(7, 12, "settlement", "", {"venue": "v10", "parties": ["t10", "t03"],
                                               "items": [{"id": 366, "kind": "card", "ref": "SAL-03"}]}))
    assert vr.open_addressed(events, 20) == []


def test_an_addressed_ask_pages_lucas_with_a_dm_to_the_addressee_only_when_it_creates_value(tmp_path):
    notes, logs = [], []
    r = vr.Radar(None, notifier=lambda *a, **k: notes.append(a), out=tmp_path / "r.md", state=tmp_path / "s.json",
                 log=logs.append, mult_file=tmp_path / "none.json")
    r.cards = vr.card_index(CATALOG)
    teams = [{"team": "t10", "name": "Team 10", "rank": 5}, {"team": "t17", "name": "Team 17", "rank": 9}]
    o = vr.open_addressed([listed(1, 10, 8031, "t10", "t17", *ASK_TO)], 12)[0]
    good = vr.addressed_match(o, teams=teams, mult={"t17": {"SAL": 1.6}, "t10": {"SAL": 0.5}}, cards=r.cards, held={})
    assert good["side"] == "ask" and good["seller"] == "t10" and good["vc"] == 11.0
    r.alert_addressed(good, 12)
    assert len(notes) == 1 and "Team 10 has an offer for you on our v10 stall" in notes[0][2]
    assert "Hi Team 17!" in notes[0][2] and "13 P" in notes[0][2]
    bad = vr.addressed_match(o, teams=teams, mult={"t17": {"SAL": 0.5}, "t10": {"SAL": 1.6}}, cards=r.cards, held={})
    r.alert_addressed(bad, 12)
    assert len(notes) == 1 and "not paged" in logs[-1]                 # est. value created < 0: logged only


def test_an_addressed_bid_reads_the_maker_as_buyer():
    o = vr.open_addressed([listed(1, 10, 9000, "t06", "t10", {"cash": 24}, {"cards": ["SAL-07"]})], 12)[0]
    m = vr.addressed_match(o, teams=[], mult={}, cards=vr.card_index(CATALOG), held={})
    assert m["side"] == "bid" and m["seller"] == "t10" and m["team"] == "t10" and m["price"] == 24


# ------------------------------------------------------------ partner suggestions (Chief 15:45)

class AllCollect:
    def allows(self, team, set_id):
        return True, "collects"


def sugg(held, teams, mult):
    lacks = {(t["team"], f"SAL-0{i}"): {"kind": "lack"} for t in teams for i in (1, 2)}
    return vr.suggestions("t15", teams=teams, held=held, mult=mult, cards=vr.card_index(CATALOG), last=lacks, prof={},
                          collectors=AllCollect(), ours=24)


def test_a_partner_s_2nd_copy_goes_to_the_best_buyer_outside_the_top_5():
    teams = [{"team": t, "name": f"Team {t[1:]}", "score": s} for t, s in
             (("t14", 40), ("t13", 39), ("t18", 38), ("t12", 37), ("t02", 36), ("t05", 24), ("t16", 5), ("t17", 6))]
    held = {("t15", "SAL-06"): {501, 502}, ("t15", "SAL-07"): {503}}       # one 2-copy card; SAL-07 is its only copy
    lines = sugg(held, teams, {"t15": {"SAL": 1.45}, "t16": {"SAL": 0.8}, "t17": {"SAL": 0.6}, "t02": {"SAL": 1.6}})
    assert [(x["card"], x["buyer"], x["price"]) for x in lines] == [("SAL-06", "t16", 24)]   # t02 is 5th: excluded
    assert lines[0]["vc"] > vr.SUGGEST_VC
    text = vr.suggestion_text(lines, vr.card_index(CATALOG))
    assert text.startswith("Suggestions for v10") and "you hold 2" in text and "Team 16 at ~24 P" in text


def test_no_line_below_plus_5_and_at_most_3_lines():
    teams = [{"team": f"t9{i}", "score": 50 - i} for i in range(5)] + [{"team": "t05", "score": 24},
                                                                         {"team": "t16", "name": "Team 16", "score": 5}]
    assert sugg({("t15", "SAL-01"): {1, 2}}, teams, {"t15": {"SAL": 1.6}, "t16": {"SAL": 0.7}}) == []   # 7 - 4 = +3
    held = {("t15", c): {1, 2} for c in ("SAL-01", "SAL-02", "SAL-03", "SAL-06", "SAL-07")}
    lines = sugg(held, teams, {"t15": {"SAL": 0.5}, "t16": {"SAL": 1.6}})
    assert len(lines) == vr.SUGGEST_LINES and lines[0]["vc"] >= lines[-1]["vc"]
