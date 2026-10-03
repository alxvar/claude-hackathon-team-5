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
                                              ("t05", 30), ("t02", 18), ("t16", 12), ("t15", 11), ("t07", 10))]
ME = {"id": "t05", "cash": 100, "assets": [
    {"id": 485, "kind": "card", "ref": "SAL-02", "your_value": 2.2},
    {"id": 486, "kind": "card", "ref": "SAL-02", "your_value": 9.0},
    {"id": 700, "kind": "card", "ref": "LAT-01", "your_value": 16.0}]}
HELD = {("t02", "LAT-07"): {1, 2}, ("t13", "LAT-07"): {3}}                 # t13 holds it too, but is top 5
VALUES = {"LAT-07": 12.5}
VENUES = {"v15": {"venue": "v15", "owner": "t15", "status": "open", "fee_per_card": 0},
          "v07": {"venue": "v07", "owner": "t10", "status": "open", "fee_per_card": 0},
          "v20": {"venue": "v20", "owner": "t03", "status": "open", "fee_per_card": 0}}


class Col:
    def __init__(self, ok=True, why="collects"):
        self.ok, self.why = ok, why

    def get(self):
        return self

    def allows(self, team, set_id):
        return self.ok, self.why


def cands(**kw):
    args = dict(me=ME, locked=set(), our_value=VALUES.get, teams=TEAMS, held=HELD, mult={}, cards=CARDS, last={},
                collectors=Col(), venues=VENUES)
    return sw.candidates(**{**args, **kw})


def test_a_spare_for_a_card_we_lack_from_a_team_outside_the_top_5():
    c = cands()
    assert [(x["give"], x["asset"], x["want"], x["to"], x["venue"]) for x in c] == [("SAL-02", 485, "LAT-07", "t02", "v15")]
    assert c[0]["our_gain"] == 10.3                                     # 12.5 - our least valuable copy (2.2)
    assert c[0]["their_low"] == 7.5                                     # 10 x 1.0 x 1st copy - 10 x 1.0 x 2nd copy


def test_both_bars():
    assert cands(our_value={"LAT-07": 5.0}.get) == []                   # our gain 2.8 < 3
    assert cands(our_value={"LAT-07": 6.0}.get, min_gain=3.0 + sw.PACK_DRAG) == []   # +3.8 < 5.5 with a pack held
    assert cands(mult={"t02": {"SAL": (0.9, 0.2, 0.9), "LAT": 1.0}}) == []    # conservative: 10 x 0.2 - 2.5 < 0
    assert cands(held={("t02", "LAT-07"): {1}}) == []                   # their only copy: 10 - 10 = 0, not > 0
    assert cands(venues={**VENUES, "v15": {**VENUES["v15"], "fee_per_card": 4}, "v07": {}, "v20": {}}) == []   # 7.5 - 8


def test_the_feeding_rule_blocks_without_evidence():
    near = [{**t, "score": 25} if t["team"] == "t02" else t for t in TEAMS]   # t02 5 below us, nothing seen of it
    assert cands(teams=near) == []                                      # a page card: blocked, data or not
    lacks = {("t02", "SAL-05"): {"kind": "lack"}, ("t02", "SAL-06"): {"kind": "lack"}}
    assert cands(teams=near, last=lacks)                                # it lacks 2 other SAL cards: not a closer
    unknown = [{**t, "score": None} if t["team"] == "t02" else t for t in TEAMS]
    assert cands(teams=unknown) == []                                   # unknown score: blocked
    assert cands()                                                      # 12 below us: allowed


def test_who_may_get_our_spare():
    assert cands(collectors=Col(False, "no sign")) == []                # neither collects nor values SAL
    assert cands(collectors=Col(False, "no sign"), mult={"t02": {"SAL": 1.3}})   # values SAL at m >= 1
    assert cands(collectors=Col(True, "t02 dumps SAL (teams.md)")) == []
    assert cands(teams=[t for t in TEAMS if t["team"] != "t05"]) == []  # no live ranking for us: nothing
    assert cands(teams=[]) == []


def test_which_copy_may_go():
    assert cands(locked={485}) == []                                    # 2 copies, one in an ask: no spare
    three = {**ME, "assets": ME["assets"] + [{"id": 487, "kind": "card", "ref": "SAL-02", "your_value": 0.9}]}
    c = cands(me=three, locked={485})
    assert c and c[0]["asset"] == 487                                   # 3 copies, one locked: the free cheapest goes
    assert cands(no_spare=frozenset({"SAL-02"})) == []                  # the book asks for it, or it's reserved
    assert cands(skip_want=frozenset({"LAT-07"})) == []                 # an open offer of ours already wants it


def test_value_reads_happen_only_for_pairs_that_pass_everything():
    asked = []
    cands(our_value=lambda c: asked.append(c) or 12.5, collectors=Col(False, "no sign"))
    assert asked == []
    cands(our_value=lambda c: asked.append(c) or 12.5)
    assert asked == ["LAT-07"]


def test_reserved_cards_come_from_the_file_or_the_handoff(tmp_path):
    (tmp_path / "h.md").write_text("# Operator handoff\n\n## Reserved (held OUT of the book)\nMAL-09 rare · SAL-01 "
                                   "(2.2), MAL-05\n\n## Watches\n- LAT-04 here is not reserved\n")
    assert sw.reserved_refs(tmp_path / "none.json", tmp_path / "h.md") == {"MAL-09", "SAL-01", "MAL-05"}
    (tmp_path / "r.json").write_text('{"cards": ["LAT-08"]}')
    assert sw.reserved_refs(tmp_path / "r.json", tmp_path / "h.md") == {"LAT-08"}


class Game:
    def __init__(self, me=ME):
        self.posted, self.offers, self.cancelled, self.next_id, self._me = [], {}, [], 9000, me

    def catalog(self):
        return CATALOG

    def me(self):
        return self._me

    def my_offers(self):
        return {"offers": list(self.offers.values())}

    def leaderboard(self):
        return {"teams": TEAMS}

    def value(self, card):
        return {"your_value": VALUES.get(card, 0.0)}

    def venues(self):
        return {"venues": list(VENUES.values())}

    def cancel(self, oid):
        self.cancelled.append(oid)
        self.offers.pop(oid, None)

    def list_offer(self, give, want, venue=None, to=None, expires_in_ticks=None):
        self.next_id += 1
        o = {"id": self.next_id, "maker": "t05", "status": "open", "venue": venue, "to": to,
             "give": {"cash": 0, "assets": [{"id": i} for i in give["assets"]]}, "want": {"cash": 0, **want},
             "expires_in_ticks": expires_in_ticks}
        self.offers[o["id"]] = o
        self.posted.append(o)
        return o


def engine(tmp_path, game, monkeypatch, dry_run=False, held=HELD):
    monkeypatch.setattr(sw, "LOG", tmp_path / "swaps.jsonl")
    monkeypatch.setattr(sw.vr, "load_mult", lambda hub, path=None: {})
    monkeypatch.setattr(sw.vr, "holdings", lambda events: held)
    monkeypatch.setattr(sw.op, "read_signals", lambda *a, **k: ({}, {}))
    (tmp_path / "book.json").write_text('{"offers": []}')
    return sw.Engine(game, dry_run=dry_run, mult_fn=dict, events_fn=list, state=tmp_path / "state.json",
                     book=tmp_path / "book.json", reserved=tmp_path / "r.json", handoff=tmp_path / "h.md",
                     collectors=Col(), sleep=lambda s: None)


def events(tmp_path):
    return [json.loads(x) for x in (tmp_path / "swaps.jsonl").read_text().splitlines()]


def test_posts_an_addressed_swap_on_a_partner_venue_with_a_short_life(tmp_path, monkeypatch):
    three = {**ME, "assets": ME["assets"] + [{"id": 487, "kind": "card", "ref": "SAL-02", "your_value": 0.9}]}
    g = Game(three)
    e = engine(tmp_path, g, monkeypatch)
    e.run(644, 30.0)
    o = g.posted[0]
    assert o["give"]["assets"] == [{"id": 487}] and o["want"]["types"] == ["card:LAT-07"] and o["to"] == "t02"
    assert o["venue"] == "v15" and o["expires_in_ticks"] == sw.expires_param(sw.LIFE_TICKS, 30.0)
    e.run(646, 30.0)                                                    # a spare remains (485), but t02 and LAT-07 are busy
    assert len(g.posted) == 1
    assert events(tmp_path)[0]["event"] == "post" and events(tmp_path)[0]["our_gain"] == 11.6


def test_at_most_max_live_swaps(tmp_path, monkeypatch):
    many = {**ME, "assets": [{"id": 100 + i, "kind": "card", "ref": "SAL-02", "your_value": 1.0} for i in range(8)]}
    held = {(f"t{20 + i}", f"LAT-0{i + 2}"): {i, 100 + i} for i in range(6)}
    teams = TEAMS + [{"team": f"t{20 + i}", "score": 5} for i in range(6)]
    g = Game(many)
    g.value = lambda card: {"your_value": 12.0}
    g.leaderboard = lambda: {"teams": teams}
    e = engine(tmp_path, g, monkeypatch, held=held)
    for t in range(644, 656, 2):
        e.run(t, 30.0)
    assert len(g.posted) == sw.MAX_LIVE and len({o["to"] for o in g.posted}) == sw.MAX_LIVE


def test_a_dry_run_posts_nothing_saves_nothing_and_tags_its_lines(tmp_path, monkeypatch):
    three = {**ME, "assets": ME["assets"] + [{"id": 487, "kind": "card", "ref": "SAL-02", "your_value": 0.9}]}
    g = Game(three)
    e = engine(tmp_path, g, monkeypatch, dry_run=True)
    e.run(644, 30.0)
    assert g.posted == [] and not (tmp_path / "state.json").exists()
    assert all(x.get("dry_run") for x in events(tmp_path))


def test_live_swaps_are_read_back_from_the_server_and_a_fill_is_logged(tmp_path, monkeypatch):
    three = {**ME, "assets": ME["assets"] + [{"id": 487, "kind": "card", "ref": "SAL-02", "your_value": 0.9}]}
    g = Game(three)
    e = engine(tmp_path, g, monkeypatch)
    e.run(644, 30.0)
    e2 = engine(tmp_path, g, monkeypatch)                               # a restart: state from the file
    g.offers.clear()                                                    # taken: 487 left, LAT-07 arrived
    g._me = {**ME, "assets": ME["assets"] + [{"id": 1, "kind": "card", "ref": "LAT-07", "your_value": 12.5}]}
    e2.run(646, 30.0)
    assert [x["event"] for x in events(tmp_path)][-1] == "filled"


def test_a_live_swap_is_cancelled_once_its_card_arrives_another_way(tmp_path, monkeypatch):
    three = {**ME, "assets": ME["assets"] + [{"id": 487, "kind": "card", "ref": "SAL-02", "your_value": 0.9}]}
    g = Game(three)
    e = engine(tmp_path, g, monkeypatch)
    e.run(644, 30.0)
    oid = g.posted[0]["id"]
    g._me = {**three, "assets": three["assets"] + [{"id": 1, "kind": "card", "ref": "LAT-07", "your_value": 12.5}]}
    e.run(646, 30.0)
    assert g.cancelled == [oid] and any(x["event"] == "cancel" for x in events(tmp_path))


def test_never_on_the_counterpartys_own_venue_nor_a_top_5_or_ownerless_venue():
    assert sw.pick_venue("t15", VENUES, {"t10"}) == "v20"
    assert sw.pick_venue("t03", VENUES, {"t10", "t15"}) is None
    assert sw.pick_venue("t02", {"v15": {"status": "open", "owner": None}}, set()) is None
