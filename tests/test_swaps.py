"""Swap engine (agents/trader/swaps.py): a fake game, no network, no writes outside tmp."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in ("agents/trader", "tools", "bazaar-kit"):
    sys.path.insert(0, str(ROOT / p))
import swaps as sw  # noqa: E402

CATALOG = {"sets": [{"id": st, "cards": [{"id": f"{st}-{i:02d}", "rarity": "common", "book": 10, "name": f"{st} {i}"}
                                         for i in range(1, 11)]} for st in ("SAL", "LAT")]}
CARDS = sw.vr.card_index(CATALOG)
TEAMS = [{"team": t, "score": s} for t, s in (("t14", 40), ("t13", 39), ("t18", 38), ("t12", 37), ("t10", 36),
                                              ("t05", 30), ("t02", 25), ("t16", 12), ("t15", 11), ("t07", 10))]
ME = {"id": "t05", "cash": 100, "assets": [
    {"id": 485, "kind": "card", "ref": "SAL-02", "your_value": 2.2},
    {"id": 486, "kind": "card", "ref": "SAL-02", "your_value": 9.0},
    {"id": 700, "kind": "card", "ref": "LAT-01", "your_value": 16.0}]}
HELD = {("t02", "LAT-07"): {1, 2}, ("t13", "LAT-07"): {3}}                 # t13 holds it too, but is top 5
VALUES = {"LAT-07": 12.5, "LAT-08": 4.0}


def cands(**kw):
    args = dict(me=ME, locked=set(), our_value=VALUES.get, teams=TEAMS, held=HELD, mult={}, cards=CARDS)
    return sw.candidates(**{**args, **kw})


def test_a_spare_for_a_card_we_lack_from_a_team_outside_the_top_5():
    c = cands()
    assert [(x["give"], x["asset"], x["want"], x["to"]) for x in c] == [("SAL-02", 485, "LAT-07", "t02")]
    assert c[0]["our_gain"] == 10.3                                     # 12.5 - our least valuable copy (2.2)
    assert c[0]["their_est"] == 7.5                                     # 10 x 1.0 x 1st copy - 10 x 1.0 x 2nd copy


def test_both_bars_and_the_page_rules():
    assert cands(our_value={"LAT-07": 5.0}.get) == []                   # our gain 2.8 < 3
    assert cands(mult={"t02": {"SAL": 0.5, "LAT": 2.5}}) == []         # theirs: 5 - 10 x 2.5 x 2nd copy 0.25 < 0
    assert cands(held={("t02", "LAT-07"): {1}}, mult={"t02": {"SAL": 0.9}}) == []   # their only copy: 9 - 10 < 0
    assert cands(skip_want=frozenset({"LAT-07"})) == []                 # the book bids for it
    near = {**HELD, **{("t02", f"SAL-{i:02d}"): {100 + i} for i in (1, 3, 4, 5, 6, 7, 8, 9)}}
    assert cands(held=near) == []                                       # SAL-02 may close t02's page; t02 is 5 below us
    assert cands(locked={485}) == []                                    # our other SAL-02 copy is the page's


class Game:
    def __init__(self):
        self.posted, self.offers, self.next_id = [], {}, 9000

    def catalog(self):
        return CATALOG

    def me(self):
        return ME

    def my_offers(self):
        return {"offers": list(self.offers.values())}

    def leaderboard(self):
        return {"teams": TEAMS}

    def value(self, card):
        return {"your_value": VALUES.get(card, 0.0)}

    def venues(self):
        return {"venues": [{"venue": "v15", "owner": "t15", "status": "open"},
                           {"venue": "v07", "owner": "t10", "status": "open"},
                           {"venue": "v20", "owner": "t03", "status": "open"}]}

    def list_offer(self, give, want, venue=None, to=None, expires_in_ticks=None):
        self.next_id += 1
        o = {"id": self.next_id, "maker": "t05", "status": "open", "give": give, "want": want, "venue": venue, "to": to,
             "expires_in_ticks": expires_in_ticks}
        self.offers[o["id"]] = o
        self.posted.append(o)
        return o


def engine(tmp_path, game, monkeypatch):
    monkeypatch.setattr(sw, "LOG", tmp_path / "swaps.jsonl")
    monkeypatch.setattr(sw.vr, "load_mult", lambda hub, path=None: {})
    monkeypatch.setattr(sw.vr, "holdings", lambda events: HELD)
    (tmp_path / "book.json").write_text('{"offers": []}')
    return sw.Engine(game, mult_fn=dict, events_fn=list, state=tmp_path / "state.json", book=tmp_path / "book.json")


def test_posts_an_addressed_swap_on_a_partner_venue_with_a_short_life(tmp_path, monkeypatch):
    g = Game()
    e = engine(tmp_path, g, monkeypatch)
    e.run(644, 30.0)
    o = g.posted[0]
    assert o["give"] == {"assets": [485]} and o["want"] == {"types": ["card:LAT-07"]} and o["to"] == "t02"
    assert o["venue"] == "v15" and o["expires_in_ticks"] == sw.expires_param(sw.LIFE_TICKS, 30.0)
    e.run(646, 30.0)
    assert len(g.posted) == 1                                           # one per team, card and spare: no repost
    logged = [json.loads(x) for x in (tmp_path / "swaps.jsonl").read_text().splitlines()]
    assert logged[0]["event"] == "post" and logged[0]["our_gain"] == 10.3


def test_a_filled_swap_is_logged_and_frees_its_slot(tmp_path, monkeypatch):
    g = Game()
    e = engine(tmp_path, g, monkeypatch)
    e.run(644, 30.0)
    g.offers.clear()                                                    # taken: LAT-07 is ours now
    monkeypatch.setattr(sw, "candidates", lambda **kw: [])
    me_after = {**ME, "assets": ME["assets"][1:] + [{"id": 1, "kind": "card", "ref": "LAT-07", "your_value": 12.5}]}
    g.me = lambda: me_after
    e.run(646, 30.0)
    events = [json.loads(x)["event"] for x in (tmp_path / "swaps.jsonl").read_text().splitlines()]
    assert events[-1] == "filled" and e.state["live"] == []


def test_never_on_the_counterpartys_own_venue_nor_a_top_5_venue():
    venues = {"v15": {"owner": "t15", "status": "open"}, "v07": {"owner": "t10", "status": "open"},
              "v20": {"owner": "t03", "status": "open"}}
    assert sw.pick_venue("t15", venues, {"t10"}) == "v20"
    assert sw.pick_venue("t03", venues, {"t10", "t15"}) is None
