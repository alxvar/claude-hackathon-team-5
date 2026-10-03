"""The trader loop (agents/trader/loop.py): offer sources, the three shapes, venue rule, page protection, dry-run.
Mocked SDK, no network."""
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("trader_loop", ROOT / "agents" / "trader" / "loop.py")
loop = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(loop)

ME = "t05"
AFF = {"LAV": 1.3, "MAL": 0.7, "LAT": 0.5, "SAL": 0.9, "RET": 1.1, "CHA": 1.6}


def card(aid, ref, rarity, value):
    return {"id": aid, "kind": "card", "ref": ref, "rarity": rarity, "set": ref.split("-")[0], "your_value": value}


ASSETS = [
    card(63, "LAV-01", "common", 99.1),    # last copy, LAV page complete: carries the page bonus
    card(171, "LAV-02", "common", 3.2), card(486, "LAV-02", "common", 3.2),  # a duplicate: fine to give
    card(119, "MAL-06", "uncommon", 17.5),
    card(61, "MAL-02", "common", 7.0),
    card(69, "SAL-02", "common", 2.2), card(485, "SAL-02", "common", 2.2),
    card(70, "SAL-01", "common", 9.0),
]
ALBUM = {"pages": [{"set": "LAV", "have": 10, "of": 10, "complete": True},
                   {"set": "MAL", "have": 4, "of": 10, "complete": False},
                   {"set": "SAL", "have": 4, "of": 10, "complete": False}]}
VENUES = [
    {"venue": "rastro", "owner": "world", "status": "open", "house": True, "fee_bps": 500, "fee_per_card": 1},
    {"venue": "v01", "owner": "t06", "status": "open", "fee_bps": 50, "fee_per_card": 0},
    {"venue": "v03", "owner": "t13", "status": "open", "fee_bps": 100, "fee_per_card": 0},
    {"venue": "v09", "owner": ME, "status": "open", "fee_bps": 0, "fee_per_card": 0},
]
TEAMS = [{"team": t, "rank": i + 1, "score": 30 - i} for i, t in enumerate(["t13", "t12", "t17", "t10", "t06", ME])]


class FakeBazaar:
    def __init__(self, boards=None, mine=(), values=None, cash=300, assets=ASSETS, album=ALBUM):
        self.boards = {"rastro": [], **(boards or {})}
        self.mine, self.values = list(mine), {"MAL-01": 7.0, "MAL-08": 17.5, "LAV-11": 0, **(values or {})}
        self._me = {"id": ME, "tick": 200, "cash": cash, "assets": list(assets), "affinity": AFF, "album": album,
                    "venue": None}
        self.accepted, self.value_calls, self.board_calls = [], [], []

    def me(self):
        return self._me

    def my_offers(self):
        return {"offers": self.mine}

    def venues(self):
        return {"venues": VENUES}

    def leaderboard(self):
        return {"teams": TEAMS}

    def board(self, venue="rastro"):
        self.board_calls.append(venue)
        return {"offers": [dict(o) for o in self.boards.get(venue, [])]}

    def value(self, ref):
        self.value_calls.append(ref)
        if "-" not in ref:
            raise AssertionError(f"b.value called on a non-card: {ref}")
        return {"card": ref, "your_value": self.values[ref]}

    def accept(self, offer_id, assets=None):
        self.accepted.append((offer_id, assets))
        return {"ok": True}


def bid(oid, cash, ref, venue="rastro", to=None, maker="m1"):
    """They pay cash for a card (we sell)."""
    return {"id": oid, "maker": maker, "to": to, "venue": venue, "status": "open",
            "give": {"cash": cash, "assets": [], "types": []}, "want": {"cash": 0, "assets": [], "types": [f"card:{ref}"]}}


def ask(oid, ref, cash, venue="rastro", aid=900, rarity="common"):
    """They sell a card for cash (we buy)."""
    return {"id": oid, "maker": "m2", "to": None, "venue": venue, "status": "open",
            "give": {"cash": 0, "assets": [{"id": aid, "kind": "card", "ref": ref, "rarity": rarity}], "types": []},
            "want": {"cash": cash, "assets": [], "types": []}}


def swap(oid, give_refs, want_refs, venue="rastro"):
    return {"id": oid, "maker": "m3", "to": None, "venue": venue, "status": "open",
            "give": {"cash": 0, "types": [],
                     "assets": [{"id": 800 + i, "kind": "card", "ref": r, "rarity": "common"} for i, r in enumerate(give_refs)]},
            "want": {"cash": 0, "assets": [], "types": [f"card:{r}" for r in want_refs]}}


@pytest.fixture(autouse=True)
def hermetic(tmp_path, monkeypatch):
    monkeypatch.setattr(loop, "LOG", tmp_path / "trader.jsonl")
    monkeypatch.setattr(loop, "should_hold_accept", lambda b, tick=None: (False, "test: no duel"))


def run(b, *argv):
    return loop.step(b, loop.parse_args(list(argv)), loop.State())


# ------------------------------------------------------------------ fee

def test_fee_matches_el_rastro_and_venue_rules():
    assert loop.fee(22, 1) == 2 + 1          # ceil(1.1) + 1 per card
    assert loop.fee(20, 1) == 1 + 1          # ceil(1.0) exactly
    assert loop.fee(0, 2) == 2               # a swap on El Rastro: per-card part only
    assert loop.fee(100, 1, 50, 0) == 1      # 0.5% of 100 = 0.5 -> 1
    assert loop.fee(0, 3, 50, 0) == 0


# ------------------------------------------------------------------ sources

def test_addressed_to_us_offer_is_accepted_when_it_gains():
    mine = [bid(501, 40, "MAL-06", to=ME, maker="t09"),          # to us: 40 - (2 + 1) - 17.5 = 19.5
            bid(502, 90, "MAL-06", to="t07", maker="t09"),       # to someone else: not ours to take
            {**bid(503, 99, "MAL-06"), "maker": ME}]             # our own offer
    b = FakeBazaar(mine=mine)
    best = run(b)
    assert b.accepted == [(501, [119])]
    assert best["gain"] == pytest.approx(19.5) and best["to_us"]


def test_own_public_offer_is_skipped_by_id_even_under_a_pseudonym():
    b = FakeBazaar(boards={"rastro": [bid(600, 80, "MAL-06", maker="mf00")]},
                   mine=[{**bid(600, 80, "MAL-06"), "maker": ME}])
    run(b)
    assert b.accepted == []


def test_reads_every_open_board_but_our_own_venue():
    b = FakeBazaar()
    run(b)
    assert b.board_calls == ["rastro", "v01", "v03"]


def test_one_accept_per_tick_takes_the_best():
    b = FakeBazaar(boards={"rastro": [bid(1, 30, "MAL-06"), bid(2, 50, "MAL-06")],
                           "v01": [ask(3, "MAL-08", 5, venue="v01")]})
    run(b)
    assert b.accepted == [(2, [119])]  # 50 - 4 - 17.5 = 28.5 beats 30 - 3 - 17.5 and 17.5 - 5 - 1


# ------------------------------------------------------------------ swaps

def test_swap_gain_counts_the_venue_fee():
    st, args = loop.State(), loop.parse_args([])
    b = FakeBazaar()
    me = b.me()
    held = {}
    for a in me["assets"]:
        held.setdefault(a["ref"], []).append(a)
    loop.refresh(b, st, me, me["tick"])
    on_rastro = loop.evaluate(b, swap(10, ["MAL-01"], ["SAL-02"]), me, held, st, args)
    on_v01 = loop.evaluate(b, swap(11, ["MAL-01"], ["SAL-02"], venue="v01"), me, held, st, args)
    # receive MAL-01 (7.0), give our cheaper SAL-02 copy (2.2); El Rastro charges 1 P for each of the 2 cards
    assert on_rastro["kind"] == "swap" and on_rastro["gain"] == pytest.approx(7.0 - 2.2 - 2)
    assert on_rastro["assets"] in ([69], [485])
    assert on_v01["gain"] == pytest.approx(7.0 - 2.2 - 0)


def test_swap_accepted_when_it_clears_the_bar():
    b = FakeBazaar(boards={"v01": [swap(12, ["MAL-08"], ["SAL-02"], venue="v01")]})  # 17.5 - 2.2 - 0
    best = run(b)
    assert b.accepted == [(12, best["assets"])] and best["gain"] == pytest.approx(15.3)


# ------------------------------------------------------------------ venue rule

def test_leader_venue_needs_gain_of_15():
    b = FakeBazaar(boards={"v03": [ask(20, "MAL-08", 5, venue="v03")]})  # 17.5 - 5 - 1 = 11.5 < 15 on t13's venue
    assert run(b) is None and b.accepted == []
    b = FakeBazaar(boards={"v01": [ask(21, "MAL-08", 5, venue="v01")]})  # t06 is rank 5: the normal bar
    assert run(b)["gain"] == pytest.approx(17.5 - 5 - 1) and b.accepted == [(21, None)]
    b = FakeBazaar(boards={"v03": [ask(22, "MAL-08", 1, venue="v03")]})  # 17.5 - 1 - 1 = 15.5 clears it
    best = run(b)
    assert best["gain"] == pytest.approx(15.5) and best["owner"] == "t13" and b.accepted == [(22, None)]


def test_accept_log_names_venue_and_owner(tmp_path):
    b = FakeBazaar(boards={"v01": [ask(23, "MAL-08", 5, venue="v01")]})
    run(b)
    line = loop.LOG.read_text().strip().splitlines()[-1]
    assert '"event": "accept"' in line and '"venue": "v01"' in line and '"owner": "t06"' in line


def test_never_on_our_own_venue():
    b = FakeBazaar(mine=[{**ask(30, "MAL-08", 1, venue="v09"), "to": ME}])  # addressed to us, on our venue
    best = run(b)
    assert best is None and b.accepted == []


# ------------------------------------------------------------------ page protection

def test_page_bonus_card_is_never_sold():
    b = FakeBazaar(boards={"rastro": [bid(40, 300, "LAV-01")]})  # last LAV-01 of a complete page (99.1 > 13)
    assert run(b) is None and b.accepted == []


def test_duplicate_of_a_page_card_can_go():
    b = FakeBazaar(boards={"rastro": [bid(41, 15, "LAV-02")]})  # 15 - (1 + 1) - 3.2 = 9.8
    run(b)
    assert b.accepted == [(41, [171])] or b.accepted == [(41, [486])]


def test_last_copy_in_a_page_we_are_building_is_kept():
    album = {"pages": [{"set": "MAL", "have": 9, "of": 10, "complete": False}]}
    b = FakeBazaar(boards={"rastro": [bid(42, 60, "MAL-02")]}, album=album)  # MAL-02 at base value, page 9/10
    assert run(b) is None and b.accepted == []
    b = FakeBazaar(boards={"rastro": [bid(43, 60, "MAL-02")]})               # page 4/10: free to sell
    run(b)
    assert b.accepted == [(43, [61])]


def test_swap_never_gives_a_page_card():
    b = FakeBazaar(boards={"rastro": [swap(44, ["MAL-08"], ["LAV-01"])]})
    assert run(b) is None and b.accepted == []


# ------------------------------------------------------------------ packs, cash floor, dry-run

def test_packs_are_skipped_without_valuing_them():
    pack_ask = {"id": 50, "maker": "m4", "to": None, "venue": "rastro", "status": "open",
                "give": {"cash": 0, "assets": [{"id": 431, "kind": "pack", "ref": "sobre_bienvenida"}], "types": []},
                "want": {"cash": 5, "assets": [], "types": []}}
    pack_bid = {"id": 51, "maker": "m4", "to": None, "venue": "rastro", "status": "open",
                "give": {"cash": 90, "assets": [], "types": []},
                "want": {"cash": 0, "assets": [], "types": ["pack:sobre_barrio"]}}
    b = FakeBazaar(boards={"rastro": [pack_ask, pack_bid]})
    assert run(b) is None and b.accepted == [] and b.value_calls == []


def test_buy_respects_the_cash_floor():
    b = FakeBazaar(boards={"rastro": [ask(60, "MAL-08", 5)]}, cash=205)  # 205 - (5 + 1 + 1) < 200
    assert run(b) is None and b.accepted == []


def test_dry_run_never_accepts():
    b = FakeBazaar(boards={"rastro": [bid(70, 50, "MAL-06")]}, mine=[bid(71, 45, "MAL-06", to=ME, maker="t09")])
    best = run(b, "--dry-run")
    assert best["offer"] == 70 and b.accepted == []
    text = loop.LOG.read_text()
    assert '"event": "dry_run"' in text and '"would_accept"' in text and '"event": "candidate"' in text
