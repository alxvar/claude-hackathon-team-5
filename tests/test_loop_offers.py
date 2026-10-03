"""The trader loop (agents/trader/loop.py): offer sources, the three shapes, venue rule, page protection, dry-run,
and the safety rules (our open offers, --build, feeding, paused clock, retries, value lookups). Mocked SDK, no network."""
import importlib.util
import json
import time
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
TEAMS = [{"team": t, "rank": i + 1, "score": 30 - i} for i, t in enumerate(["t13", "t12", "t17", "t10", "t06", ME])] + [
    {"team": "t04", "rank": 7, "score": 20},   # 5 points below us: near
    {"team": "t09", "rank": 8, "score": 5}]    # 20 points below us: far, safe to sell to


class FakeBazaar:
    """`listed`: offer id -> team, what GET /api/feed's offer.listed events say. By default every offer on a board
    or addressed to us was listed by t09 (20 points below us), so a sale to it is allowed."""

    def __init__(self, boards=None, mine=(), values=None, cash=300, assets=ASSETS, album=ALBUM, listed=None):
        self.boards = {"rastro": [], **(boards or {})}
        self.mine, self.values = list(mine), {"MAL-01": 7.0, "MAL-08": 17.5, "LAV-11": 0, **(values or {})}
        self._me = {"id": ME, "tick": 200, "cash": cash, "assets": list(assets), "affinity": AFF, "album": album,
                    "venue": None}
        self.listed = listed if listed is not None else {
            o["id"]: "t09" for o in [*self.mine, *(o for v in self.boards.values() for o in v)] if o.get("maker") != ME}
        self.accepted, self.value_calls, self.board_calls, self.feed_calls = [], [], [], 0
        self.offers_error = self.refuse = None
        self.me_calls = 0

    def me(self):
        self.me_calls += 1
        return self._me

    def my_offers(self):
        if self.offers_error:
            raise loop.BazaarError(self.offers_error)
        return {"offers": self.mine}

    def feed(self, limit=150):
        self.feed_calls += 1
        return {"events": [{"type": "offer.listed", "actor": t, "payload": {"offer": {"id": i}}}
                           for i, t in self.listed.items()]}

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
        if self.refuse:
            raise loop.BazaarError(self.refuse)
        return {"ok": True}


def bid(oid, cash, ref, venue="rastro", to=None, maker="m1"):
    """They pay cash for a card (we sell)."""
    return {"id": oid, "maker": maker, "to": to, "venue": venue, "status": "open",
            "give": {"cash": cash, "assets": [], "types": []}, "want": {"cash": 0, "assets": [], "types": [f"card:{ref}"]}}


RARITY = {"MAL-08": "uncommon", "MAL-06": "uncommon"}  # every other test card is a common


def ask(oid, ref, cash, venue="rastro", aid=900, rarity=None):
    """They sell a card for cash (we buy)."""
    return {"id": oid, "maker": "m2", "to": None, "venue": venue, "status": "open",
            "give": {"cash": 0, "assets": [{"id": aid, "kind": "card", "ref": ref, "rarity": rarity or RARITY.get(ref, "common")}],
                     "types": []},
            "want": {"cash": cash, "assets": [], "types": []}}


def swap(oid, give_refs, want_refs, venue="rastro"):
    return {"id": oid, "maker": "m3", "to": None, "venue": venue, "status": "open",
            "give": {"cash": 0, "types": [],
                     "assets": [{"id": 800 + i, "kind": "card", "ref": r, "rarity": RARITY.get(r, "common")}
                                for i, r in enumerate(give_refs)]},
            "want": {"cash": 0, "assets": [], "types": [f"card:{r}" for r in want_refs]}}


@pytest.fixture(autouse=True)
def hermetic(tmp_path, monkeypatch):
    monkeypatch.setattr(loop, "LOG", tmp_path / "trader.jsonl")
    monkeypatch.setattr(loop, "BOARD", tmp_path / "board.json")   # absent unless a test writes it
    monkeypatch.setattr(loop, "FEED", tmp_path / "feed.jsonl")
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


# ------------------------------------------------------------------ 1. copies in our own open offers

def our_ask(oid, *asset_ids, status="open"):
    return {"id": oid, "maker": ME, "to": None, "venue": "rastro", "status": status,
            "give": {"cash": 0, "assets": [{"id": a, "kind": "card"} for a in asset_ids], "types": []},
            "want": {"cash": 50, "assets": [], "types": []}}


def test_copy_in_our_open_offer_is_never_given():
    b = FakeBazaar(boards={"rastro": [bid(80, 20, "SAL-02")]}, mine=[our_ask(700, 69)])
    run(b)
    assert b.accepted == [(80, [485])]          # 69 is promised in our ask 700: the other copy goes
    b = FakeBazaar(boards={"rastro": [bid(81, 60, "MAL-02")]}, mine=[our_ask(701, 61)])
    assert run(b) is None and b.accepted == []  # our only MAL-02 is in our ask


def test_our_offer_makes_the_free_copy_the_last_one():
    album = {"pages": [{"set": "SAL", "have": 9, "of": 10, "complete": False}]}
    b = FakeBazaar(boards={"rastro": [bid(82, 20, "SAL-02")]}, mine=[our_ask(702, 69)], album=album)
    assert run(b) is None and b.accepted == []  # 485 is now our last free SAL-02 of a 9/10 page


def test_unreadable_my_offers_skips_the_tick():
    b = FakeBazaar(boards={"rastro": [bid(83, 60, "MAL-02"), ask(84, "MAL-08", 1), swap(85, ["MAL-08"], ["SAL-02"])]})
    b.offers_error = "network"
    assert run(b) is None and b.accepted == [] and b.value_calls == []
    assert '"skip_tick"' in loop.LOG.read_text()


# ------------------------------------------------------------------ 2. --build and LAV

RET_CHA = [*ASSETS, card(901, "RET-03", "common", 11.0), card(902, "CHA-02", "common", 16.0),
           card(903, "CHA-02", "common", 4.0)]


def test_build_sets_keep_their_last_copy():
    b = FakeBazaar(boards={"rastro": [bid(90, 100, "RET-03")]}, assets=RET_CHA)
    assert run(b) is None and b.accepted == []           # last RET-03, RET is being built
    b = FakeBazaar(boards={"rastro": [bid(91, 30, "CHA-02")]}, assets=RET_CHA)
    run(b)
    assert b.accepted == [(91, [903])]                   # the spare CHA-02 can go
    b = FakeBazaar(boards={"rastro": [bid(92, 100, "RET-03")]}, assets=RET_CHA)
    run(b, "--build", "CHA")
    assert b.accepted == [(92, [901])]                   # RET no longer built: free to sell


def test_lav_last_copy_kept_even_on_an_open_page():
    album = {"pages": [{"set": "LAV", "have": 5, "of": 10, "complete": False}]}
    assets = [card(904, "LAV-05", "common", 13.0)]       # book x 1.3: no page bonus, page far from complete
    b = FakeBazaar(boards={"rastro": [bid(93, 40, "LAV-05")]}, assets=assets, album=album)
    assert run(b, "--build", "") is None and b.accepted == []


def test_build_sets_are_kept_in_swaps_too():
    b = FakeBazaar(boards={"rastro": [swap(94, ["MAL-08"], ["RET-03"])]}, assets=RET_CHA)
    assert run(b) is None and b.accepted == []


# ------------------------------------------------------------------ 3. feeding rule

def write_board(tmp_path, teams, age=0):
    (tmp_path / "board.json").write_text(json.dumps(
        {"t": time.time() - age, "me": ME, "offers": [{"id": i, "team": t} for i, t in teams.items()]}))


def test_no_sale_to_a_top4_bidder_named_by_board_json(tmp_path):
    write_board(tmp_path, {100: "t13"})
    b = FakeBazaar(boards={"rastro": [bid(100, 30, "MAL-06")]})   # 30 - 3 - 17.5 = 9.5 clears the bar
    assert run(b) is None and b.accepted == [] and b.feed_calls == 0
    run(FakeBazaar(boards={"rastro": [bid(100, 30, "MAL-06")]}), "--dry-run")
    cand = [e for e in events() if e["event"] == "candidate"][0]
    assert cand["bidder"] == "t13" and "top 6" in cand["skip"] and not cand["ok"]


def test_stale_board_json_falls_back_to_the_feed(tmp_path):
    write_board(tmp_path, {101: "t09"}, age=300)                   # says a safe team, but 5 min old
    b = FakeBazaar(boards={"rastro": [bid(101, 30, "MAL-06")]}, listed={101: "t12"})
    assert run(b) is None and b.accepted == [] and b.feed_calls == 1


def test_local_feed_file_names_the_bidder_without_a_request(tmp_path):
    (tmp_path / "feed.jsonl").write_text(json.dumps(
        {"id": 1, "type": "offer.listed", "actor": "t17", "payload": {"offer": {"id": 102}}}) + "\n")
    b = FakeBazaar(boards={"rastro": [bid(102, 30, "MAL-06")]}, listed={})
    assert run(b) is None and b.accepted == [] and b.feed_calls == 0


def test_unknown_or_near_bidder_gets_no_page_closer_price():
    # MAL-06 is an uncommon (book 25): 1.5 x book = 37.5
    b = FakeBazaar(boards={"rastro": [bid(103, 40, "MAL-06")]}, listed={})          # unknown bidder, 40 >= 37.5
    assert run(b) is None and b.accepted == []
    b = FakeBazaar(boards={"rastro": [bid(104, 36, "MAL-06")]}, listed={})          # unknown, 36 < 37.5:
    run(b)
    assert b.accepted == []                                  # policy 16:20: an unknown counterparty is skipped
    b = FakeBazaar(boards={"rastro": [bid(104, 36, "MAL-06")]}, listed={104: "t09"})  # known, far below us: fine
    run(b)
    assert b.accepted == [(104, [119])]
    b = FakeBazaar(boards={"rastro": [bid(105, 40, "MAL-06")]}, listed={105: "t04"})  # 5 points below us
    assert run(b) is None and b.accepted == []
    b = FakeBazaar(boards={"rastro": [bid(106, 40, "MAL-06")]}, listed={106: "t09"})  # 20 below: fine
    run(b)
    assert b.accepted == [(106, [119])]


def test_live_feed_read_at_most_once_per_tick():
    b = FakeBazaar(boards={"rastro": [bid(107, 30, "MAL-06"), bid(108, 31, "MAL-06"), bid(109, 20, "SAL-02")]},
                   listed={})
    run(b)
    assert b.feed_calls == 1


def test_swap_into_a_top4_team_is_skipped():
    b = FakeBazaar(boards={"v01": [swap(110, ["MAL-08"], ["SAL-02"], venue="v01")]}, listed={110: "t10"})
    assert run(b) is None and b.accepted == []


# ------------------------------------------------------------------ 5. retries

def test_rate_refusal_is_retried_next_tick_a_gone_one_is_not():
    st, args = loop.State(), loop.parse_args([])
    b = FakeBazaar(boards={"rastro": [ask(120, "MAL-08", 5)]})
    b.refuse = "wait_for_tick"
    loop.step(b, args, st)
    assert 120 not in st.tried
    b.refuse = "gone"
    loop.step(b, args, st)
    assert 120 in st.tried and len(b.accepted) == 2
    loop.step(b, args, st)
    assert len(b.accepted) == 2                               # not tried again


def test_accepted_offer_is_not_taken_twice():
    st, args = loop.State(), loop.parse_args([])
    b = FakeBazaar(boards={"rastro": [ask(121, "MAL-08", 5)]})
    loop.step(b, args, st)
    loop.step(b, args, st)
    assert b.accepted == [(121, None)]


def test_server_errors_on_one_offer_stop_after_three_tries():
    st, args = loop.State(), loop.parse_args([])
    b = FakeBazaar(boards={"rastro": [ask(122, "MAL-08", 5)]})
    b.refuse = "http_502"
    for _ in range(4):
        loop.step(b, args, st)
    assert len(b.accepted) == 3 and 122 in st.tried          # it no longer blocks every other accept


def test_addressed_offer_from_a_top4_team_is_refused_by_its_maker_id():
    b = FakeBazaar(mine=[bid(111, 30, "MAL-06", to=ME, maker="t12")], listed={})
    assert run(b) is None and b.accepted == [] and b.feed_calls == 0


def test_no_sales_while_the_leaderboard_is_unknown():
    b = FakeBazaar(boards={"rastro": [bid(112, 30, "MAL-06"), ask(113, "MAL-08", 5)]})
    b.leaderboard = lambda: (_ for _ in ()).throw(loop.BazaarError("network"))
    run(b)
    assert b.accepted == []                                  # policy 16:20: no top 5 known, no counterparty at all


def test_odd_feed_lines_do_not_break_the_tick(tmp_path):
    (tmp_path / "feed.jsonl").write_text('[1, 2]\n{"type": "offer.listed", "payload": 5}\nnot json "offer.listed"\n')
    b = FakeBazaar(boards={"rastro": [bid(114, 30, "MAL-06")]})
    run(b)
    assert b.accepted == [(114, [119])]


# ------------------------------------------------------------------ 6. value lookups

def test_no_value_lookup_for_a_buy_that_cannot_clear_the_bar():
    b = FakeBazaar(boards={"rastro": [ask(130, "MAL-08", 20),            # worth at most 17.5 to us
                                      ask(131, "MAL-06", 3, aid=901)]})  # our 2nd copy: at most 25% of 17.5
    assert run(b) is None and b.value_calls == []


def test_last_missing_card_of_a_page_is_always_looked_up():
    album = {"pages": [{"set": "MAL", "have": 9, "of": 10, "complete": False}]}
    b = FakeBazaar(boards={"rastro": [ask(132, "MAL-08", 100)]}, album=album, cash=500, values={"MAL-08": 120.0})
    run(b)
    assert b.value_calls == ["MAL-08"] and b.accepted == [(132, None)]   # 120 - 100 - 6 = 14


def test_value_cache_resets_after_a_one_for_one_swap():
    st, args = loop.State(), loop.parse_args([])
    b = FakeBazaar(boards={"rastro": [ask(133, "MAL-01", 1)]}, values={"MAL-01": 7.0})
    b.refuse = "wait_for_tick"
    loop.step(b, args, st)
    assert st.values["MAL-01"] == 7.0
    b._me["assets"] = [*ASSETS[:-1], card(999, "MAL-01", "common", 7.0)]  # SAL-01 out, MAL-01 in: same count, same cash
    b.values["MAL-01"] = 1.75
    b.refuse = None
    loop.step(b, args, st)
    assert st.values.get("MAL-01") != 7.0      # the stale 7.0 is gone: now a 2nd copy, worth at most 25%
    assert len(b.accepted) == 1                 # so the buy (1 + 2 fee for 1.75 of value) is not taken


# ------------------------------------------------------------------ 4. the main loop: clock, errors, SDK settings

class Stop(BaseException):
    """Ends main()'s endless loop from inside a test (not an Exception, so main doesn't catch it)."""


class ClockBazaar(FakeBazaar):
    def __init__(self, clocks, **kw):
        super().__init__(**kw)
        self.clocks, self.me_error = list(clocks), None

    def clock(self):
        return {"tick": 200, "paused": False, "doors": "open"}

    def wait_tick(self):
        x = self.clocks.pop(0)
        if isinstance(x, Exception):
            raise x
        return x

    def me(self):
        if self.me_error:
            e, self.me_error = self.me_error, None
            raise e
        return super().me()


OPEN = {"tick": 201, "paused": False, "doors": "open"}
CLOSED = {"tick": 201, "paused": True, "doors": "closed"}


def run_main(monkeypatch, fake, argv=(), stop_after=3, clock=None):
    built, sleeps = {}, []

    def make(url, key, **kw):
        built.update(kw)
        return fake

    def sleep(s):
        sleeps.append(s)
        if len(sleeps) >= stop_after:
            raise Stop

    monkeypatch.setenv("BAZAAR_KEY", "tk-test")
    monkeypatch.setattr(loop, "Bazaar", make)
    monkeypatch.setattr(loop, "pace", lambda b, gap: b)
    monkeypatch.setattr(loop.time, "sleep", sleep)
    if clock:
        monkeypatch.setattr(fake, "clock", lambda: clock)
    try:
        loop.main(list(argv))
    except Stop:
        pass
    return built, sleeps


def events(path=None):
    return [json.loads(x) for x in (path or loop.LOG).read_text().splitlines()]


def test_paused_clock_sleeps_and_scans_nothing(monkeypatch):
    fake = ClockBazaar([CLOSED, CLOSED, CLOSED], boards={"rastro": [ask(140, "MAL-08", 5)]})
    built, sleeps = run_main(monkeypatch, fake, clock=CLOSED)
    assert sleeps == [30, 30, 30] and fake.me_calls == 0 and fake.accepted == []
    assert [e["event"] for e in events()] == ["closed"]                # logged once, not every 30 s
    assert built["wait_on_tick"] is False                              # no silent SDK retry past the arbiter


def test_loop_survives_errors_and_waits_for_the_next_tick(monkeypatch):
    fake = ClockBazaar([loop.BazaarError("network", "GET /api/clock"), OPEN, CLOSED],
                       boards={"rastro": [ask(141, "MAL-08", 5)]})
    fake.me_error = KeyError("assets")                                 # the first step crashes
    _, sleeps = run_main(monkeypatch, fake, stop_after=3)
    kinds = [(e["event"], e.get("code")) for e in events()]
    assert ("error", "KeyError") in kinds and ("error", "network") in kinds
    assert sleeps == [5, 5, 30]                                        # short pause after each error, no spin
    assert fake.accepted == [(141, None)]                              # the open tick still traded


def test_dry_run_once_still_evaluates_while_closed(monkeypatch, tmp_path):
    monkeypatch.setattr(loop, "ROOT", tmp_path)
    fake = ClockBazaar([], boards={"rastro": [ask(142, "MAL-08", 5)]})
    _, sleeps = run_main(monkeypatch, fake, argv=["--dry-run", "--once"], clock=CLOSED)
    log = events(tmp_path / "logs" / "trader-dry.jsonl")
    assert sleeps == [] and fake.accepted == [] and fake.me_calls == 1
    assert log[0]["event"] == "clock" and log[1]["would_accept"]["offer"] == 142


def test_live_once_while_closed_does_nothing(monkeypatch):
    fake = ClockBazaar([])
    _, sleeps = run_main(monkeypatch, fake, argv=["--once"], clock=CLOSED)
    assert sleeps == [] and fake.me_calls == 0



def test_cash_in_our_open_bids_counts_against_the_floor():
    # Review 13:30 (M5): the book's CHA bids hold cash the trader must not spend.
    ours = {"id": 90, "maker": ME, "to": None, "venue": "rastro", "status": "open",
            "give": {"cash": 100, "assets": [], "types": []}, "want": {"cash": 0, "cards": ["CHA-09"], "types": []}}
    b = FakeBazaar(boards={"rastro": [ask(60, "MAL-08", 5)]}, cash=300, mine=[ours])   # 300 - 100 - 7 < 200
    assert run(b) is None and b.accepted == []
    b = FakeBazaar(boards={"rastro": [ask(60, "MAL-08", 5)]}, cash=300)
    run(b)
    assert [a[0] for a in b.accepted] == [60]



# ------------------------------------------------------------------ counterparty policy and our own asks (Chief 16:20/16:30)

def test_a_rival_or_top_5_seller_is_skipped_on_a_buy_and_a_far_one_is_not():
    b = FakeBazaar(boards={"rastro": [ask(120, "MAL-08", 5)]}, listed={120: "t17"})   # Team 17: rival and top 5 here
    run(b)
    assert b.accepted == []
    b = FakeBazaar(boards={"rastro": [ask(121, "MAL-08", 5)]}, listed={121: "t09"})
    run(b)
    assert [a[0] for a in b.accepted] == [121]


def test_our_own_live_ask_for_the_card_beats_a_worse_accept():
    # Sat 16:28: t08's swap took a RET-04 copy for +6.2 while our ask at 40 (+37) had been DM'd to Team 15.
    ours = {"id": 9343, "maker": ME, "to": "t15", "venue": "rastro", "status": "open", "expires_tick": 99999,
            "give": {"cash": 0, "assets": [{"id": 69, "kind": "card", "ref": "SAL-02"}], "types": []},
            "want": {"cash": 30, "assets": [], "types": []}}
    b = FakeBazaar(boards={"rastro": [bid(122, 15, "SAL-02")]}, listed={122: "t09"}, mine=[ours])
    run(b)
    assert b.accepted == []                                  # 30 - 2.2 beats 15 - 2 - 2.2: our ask stands
    b = FakeBazaar(boards={"rastro": [bid(122, 15, "SAL-02")]}, listed={122: "t09"})
    run(b)
    assert [a[0] for a in b.accepted] == [122]               # no ask of ours: the same bid is taken



def test_a_reserved_card_is_never_given(tmp_path, monkeypatch):
    # Sat 16:06: Team 10's swap would have taken MAL-09; the reserved list (run/reserved.json) blocks any such give.
    monkeypatch.setattr(loop.policy, "reserved_refs", lambda *a, **k: {"MAL-06"})
    b = FakeBazaar(boards={"rastro": [bid(130, 36, "MAL-06")]}, listed={130: "t09"})
    run(b)
    assert b.accepted == []


def test_never_the_last_copy_of_a_complete_page_when_the_other_is_committed():
    # Sat 17:05: LAV-02's other copy (171) sits in our ask; the free one (486) is now the last: no sale.
    ours = {"id": 9400, "maker": ME, "to": "t16", "venue": "v15", "status": "open", "expires_tick": 99999,
            "give": {"cash": 0, "assets": [{"id": 171, "kind": "card", "ref": "LAV-02"}], "types": []},
            "want": {"cash": 50, "assets": [], "types": []}}
    b = FakeBazaar(boards={"rastro": [bid(140, 30, "LAV-02")]}, listed={140: "t09"}, mine=[ours])
    run(b)
    assert b.accepted == []


def test_a_page_card_to_a_team_within_6_is_a_possible_page_closer_at_any_price():
    # Review 17:15: only prices >= 1.5x book counted as page-closers; t04 is 5 below us.
    b = FakeBazaar(boards={"rastro": [bid(150, 12, "SAL-02")]}, listed={150: "t04"})
    run(b)
    assert b.accepted == []
    b = FakeBazaar(boards={"rastro": [bid(151, 12, "SAL-02")]}, listed={151: "t09"})   # 20 below: fine
    run(b)
    assert [a[0] for a in b.accepted] == [151]
