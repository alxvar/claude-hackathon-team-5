"""Offline tests for agents/trader/book.py: a fake game, no network, no writes anywhere."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "agents" / "trader"))
sys.path.insert(0, str(ROOT / "bazaar-kit"))
import book as bk  # noqa: E402
from bazaar_sdk import BazaarError  # noqa: E402

V07 = {"venue": "v07", "owner": "t10", "status": "open"}
TOP = [{"team": t, "score": s} for t, s in (("t13", 40), ("t12", 38), ("t18", 35), ("t02", 33), ("t05", 20))]
CLOCK = {"tick": 300, "tick_seconds": 30.0, "limits": {"offers_per_team_per_tick": 12, "max_open_offers_per_team": 30}}


class Game:
    """Our team t05: holds SAL-08 (worth 14) and two LAT-04 (8, 9); cash 400. Offers posted here stay open."""

    def __init__(self, venues=(V07,), values=None, cash=400):
        self.assets = [{"id": 179, "kind": "card", "ref": "SAL-08", "your_value": 14},
                       {"id": 277, "kind": "card", "ref": "LAT-04", "your_value": 9},
                       {"id": 484, "kind": "card", "ref": "LAT-04", "your_value": 8}]
        self.offers, self.posted, self.cancelled, self.next_id, self.tick = {}, [], [], 5000, CLOCK["tick"]
        self._venues, self.values, self.cash = list(venues), values or {"RET-07": 60.0}, cash
        self.teams, self.lb_fails = list(TOP), False

    def venues(self):
        return {"venues": self._venues}

    def leaderboard(self):
        if self.lb_fails:
            raise BazaarError("network", "leaderboard down")
        return {"teams": self.teams}

    def me(self):
        return {"id": "t05", "cash": self.cash, "assets": self.assets}

    def my_offers(self):
        return {"offers": list(self.offers.values())}

    def value(self, card):
        return {"your_value": self.values[card]}

    def list_offer(self, give, want, venue=None, to=None, expires_in_ticks=40):
        self.next_id += 1
        o = {"id": self.next_id, "maker": "t05", "status": "open", "give": give, "want": want, "venue": venue, "to": to,
             "expires_tick": self.tick + expires_in_ticks * 30 // 60}   # the server halves it on Saturday
        refs = {a["id"]: a["ref"] for a in self.assets}
        self.offers[o["id"]] = {**o, "give": {**give, "assets": [{"id": i, "ref": refs.get(i)}   # as /api/me/offers
                                                                  for i in give.get("assets") or []]}}
        self.posted.append(o)
        return o

    def cancel(self, oid):
        self.cancelled.append(oid)
        self.offers.pop(oid, None)


class AllowAll:
    """Collectors stub: every named buyer collects every set (the collectors rule has its own tests)."""

    def get(self):
        return self

    def allows(self, team, set_id):
        return (bool(team) or True), "test"


def run(game, entries, st=None, tick=300, **kw):
    events = []
    game.tick = tick
    kw.setdefault("collectors", AllowAll())
    book = bk.Book(game, log=events.append, **kw)
    return book.step(entries, st or {}, {**CLOCK, "tick": tick}), events, book


def test_a_new_entry_is_posted_on_v07_for_40_real_ticks():
    g = Game()
    st, ev, _ = run(g, [{"card": "SAL-08", "side": "sell", "to": "t16", "price": 30, "floor": 20}])
    o = g.posted[0]
    assert o["venue"] == "v07" and o["to"] == "t16" and o["give"] == {"assets": [179]} and o["want"] == {"cash": 30}
    assert o["expires_tick"] == 300 + bk.LIFE_TICKS                     # sent as 80: Friday's 60 s ticks
    assert st["SAL-08:sell"]["price"] == 30 and ev[-1]["event"] == "post"


def test_page_closers_and_top_4_venues_go_to_el_rastro():
    g = Game()
    run(g, [{"card": "SAL-08", "side": "sell", "price": 30, "floor": 20, "page_closer": True}])
    assert g.posted[0]["venue"] == "rastro"
    g = Game(venues=[{**V07, "owner": "t13"}])                           # Team 13 is in the top 4
    run(g, [{"card": "SAL-08", "side": "sell", "price": 30, "floor": 20}])
    assert g.posted[0]["venue"] == "rastro"


def test_an_offer_about_to_expire_is_posted_again_at_the_same_price():
    g = Game()
    e = [{"card": "SAL-08", "side": "sell", "price": 30, "floor": 20}]
    st, _, _ = run(g, e, tick=300)
    st, ev, _ = run(g, e, st, tick=300 + bk.LIFE_TICKS - bk.REFRESH_LEFT)
    assert g.cancelled == [g.posted[0]["id"]] and g.posted[1]["want"] == {"cash": 30}
    assert ev[-1]["event"] == "refresh" and st["SAL-08:sell"]["since"] == 300   # the reprice clock keeps running


def test_after_20_unfilled_ticks_an_ask_steps_down_but_never_below_its_floor():
    g = Game()
    e = [{"card": "SAL-08", "side": "sell", "price": 30, "floor": 21}]  # value 14 + 1 = 15 < 21: floor 21
    st, _, _ = run(g, e, tick=300)
    st, ev, _ = run(g, e, st, tick=319)
    assert len(g.posted) == 1                                           # 19 ticks: not yet
    prices = []
    for t in (320, 340, 360, 380, 400):
        st, ev, _ = run(g, e, st, tick=t)
        prices.append(st["SAL-08:sell"]["price"])
    assert prices == [27, 25, 24, 23, 22]                             # a quarter of the gap, at least 1 P
    assert min(o["want"]["cash"] for o in g.posted) >= 21 and all(p >= 21 for p in prices)


def test_an_ask_never_goes_below_our_value_plus_1():
    # As maker we pay no fee: any price above our copy's value scores (the trader's +6 is a taker's bar). Today +6
    # blocked SAL-08 (worth 22.5: floor 28.5, while uncommons clear ~24.5).
    g = Game()
    run(g, [{"card": "SAL-08", "side": "sell", "price": 10, "floor": 5}])  # the book asks too little
    assert g.posted[0]["want"] == {"cash": 15}                          # 14 + 1


def test_a_bid_steps_up_to_its_cap_value_minus_3():
    g = Game()
    e = [{"card": "RET-07", "side": "buy", "price": 40, "floor": 70}]   # book cap 70, our value 60 -> cap 57
    st, _, _ = run(g, e, tick=300)
    for t in range(320, 600, 20):
        st, _, _ = run(g, e, st, tick=t)
    assert max(o["give"]["cash"] for o in g.posted) == 57 and st["RET-07:buy"]["price"] == 57


def test_a_bid_respects_the_cash_floor():
    g = Game(cash=200)
    st, ev, _ = run(g, [{"card": "RET-07", "side": "buy", "price": 40, "floor": 55}], cash_floor=200)
    assert g.posted == [] and ev[-1]["event"] == "skip" and "cash floor" in ev[-1]["why"]   # no room at all
    g = Game(cash=230)                                                  # 30 of room: a 30 bid, never below the floor
    run(g, [{"card": "RET-07", "side": "buy", "price": 40, "floor": 55}], cash_floor=200)
    assert g.posted[0]["give"] == {"cash": 30}


def test_a_sold_ask_is_done_and_an_expired_one_is_posted_again():
    g = Game()
    e = [{"card": "SAL-08", "side": "sell", "price": 30, "floor": 20},
         {"card": "LAT-04", "side": "sell", "price": 15, "floor": 14}]
    st, _, _ = run(g, e, tick=300)
    sold, lat = g.posted[0]["id"], g.posted[1]["id"]
    g.offers.pop(sold)
    g.assets = [a for a in g.assets if a["id"] != 179]                   # SAL-08 left us: filled
    g.offers.pop(lat)                                                   # LAT-04: expired, copy still ours
    st, ev, _ = run(g, e, st, tick=305)
    kinds = [x["event"] for x in ev]
    assert "filled" in kinds and "expired" in kinds
    assert st["SAL-08:sell"]["done"] and g.posted[-1]["give"] == {"assets": [484]}   # LAT-04 again, cheapest copy
    st, _, _ = run(g, e, st, tick=306)
    assert len(g.posted) == 3                                           # nothing more for the sold card


def test_it_keeps_to_its_share_of_the_new_offers_per_tick():
    g = Game()
    g.assets += [{"id": 900 + i, "kind": "card", "ref": f"X-{i:02d}", "your_value": 5} for i in range(10)]
    e = [{"card": f"X-{i:02d}", "side": "sell", "price": 20, "floor": 12} for i in range(10)]
    st, _, _ = run(g, e)
    assert len(g.posted) == 6                                           # half of the team's 12
    st, _, _ = run(g, e, st, tick=301)
    assert len(g.posted) == 10


def test_a_refused_post_is_logged_and_retried_next_tick():
    g = Game()
    real = g.list_offer

    def refuse(*a, **k):
        raise BazaarError("wait_for_tick", "twelve listings this tick", 429)
    g.list_offer = refuse
    e = [{"card": "SAL-08", "side": "sell", "price": 30, "floor": 20}]
    st, ev, _ = run(g, e)
    assert ev[-1]["event"] == "post_failed" and not st.get("SAL-08:sell", {}).get("offer")
    g.list_offer = real
    st, _, _ = run(g, e, st, tick=301)
    assert len(g.posted) == 1



def test_an_offer_already_out_is_taken_over_not_duplicated():
    g = Game()
    g.tick = 280
    hand = g.list_offer({"assets": [179]}, {"cash": 30}, venue="v07", to="t16", expires_in_ticks=80)   # by hand
    e = [{"card": "SAL-08", "side": "sell", "to": "t16", "price": 30, "floor": 20}]
    st, ev, _ = run(g, e, tick=300)
    assert st["SAL-08:sell"]["offer"] == hand["id"] and ev[0]["event"] == "adopt" and len(g.posted) == 1
    st, ev, _ = run(g, e, st, tick=316)                                   # expires at 320: refreshed
    assert g.cancelled == [hand["id"]] and len(g.posted) == 2 and ev[-1]["event"] == "refresh"



def test_a_bid_follows_our_value_when_the_card_becomes_the_last_of_a_page():
    # CHA-08 reads 40 while other CHA cards are missing, 146 once it is the last one (+106 page bonus).
    g = Game(values={"CHA-08": 40.0})
    e = [{"card": "CHA-08", "side": "buy", "price": 60, "floor": 96}]
    book = bk.Book(g, log=lambda ev: None, collectors=AllowAll())
    st = book.step(e, {}, {**CLOCK, "tick": 300})
    assert g.posted[-1]["give"] == {"cash": 37}                         # capped at value - 3
    g.values["CHA-08"] = 146.0
    for t in range(301, 341):
        g.tick = t
        st = book.step(e, st, {**CLOCK, "tick": t})
    assert max(o["give"]["cash"] for o in g.posted) > 37                 # the new value lifted the cap
    assert all(o["give"]["cash"] <= 96 for o in g.posted)               # never past the book's floor



def test_a_page_closer_bid_goes_to_el_rastro_with_its_own_shorter_life():
    g = Game(values={"CHA-08": 146.0})
    run(g, [{"card": "CHA-08", "side": "buy", "price": 60, "floor": 96, "page_closer": True, "life": 20}])
    o = g.posted[0]
    assert o["venue"] == "rastro" and o["expires_tick"] == 300 + 20     # sent as 40 at 30 s ticks



# ------------------------------------------------------------------ top 4 read per tick; sells only to collectors

def test_a_venue_owner_entering_the_top_4_sends_the_next_post_to_el_rastro():
    # Sat 11:31: MAL-02 was reposted on v07 with t10 already in the top 4 (the top 4 was read every 10 ticks).
    g = Game()
    book = bk.Book(g, log=lambda ev: None, collectors=AllowAll())
    st = book.step([{"card": "SAL-08", "side": "sell", "to": "t16", "price": 30, "floor": 20}], {}, {**CLOCK, "tick": 300})
    assert g.posted[-1]["venue"] == "v07"
    g.teams = [{"team": "t10", "score": 99}] + list(TOP)                # t10, v07's owner, is now #1
    g.tick = 302
    book.step([{"card": "SAL-08", "side": "sell", "to": "t16", "price": 30, "floor": 20},
               {"card": "LAT-04", "side": "sell", "to": "t15", "price": 15, "floor": 14}], st, {**CLOCK, "tick": 302})
    assert g.posted[-1]["give"] == {"assets": [484]} and g.posted[-1]["venue"] == "rastro"


def test_an_unknown_top_4_means_el_rastro():
    g = Game()
    g.lb_fails = True
    run(g, [{"card": "SAL-08", "side": "sell", "to": "t16", "price": 30, "floor": 20}])
    assert g.posted[0]["venue"] == "rastro"


class Rule:
    def __init__(self, allowed):
        self.allowed = allowed

    def get(self):
        return self

    def allows(self, team, set_id):
        return (team, set_id) in self.allowed, f"{team} doesn't collect {set_id}"


def test_asks_go_only_to_teams_that_collect_the_set():
    g = Game()
    e = [{"card": "SAL-08", "side": "sell", "to": "t10", "price": 30, "floor": 20},     # t10 dumps SAL
         {"card": "LAT-04", "side": "sell", "price": 15, "floor": 14},                  # public: buyer unknown
         {"card": "SAL-08", "side": "sell", "to": "t16", "price": 30, "floor": 20}]     # t16 collects SAL
    st, ev, _ = run(g, e[:2], collectors=Rule({("t16", "SAL")}))
    assert g.posted == [] and [x["event"] for x in ev] == ["skip", "skip"]
    st, ev, _ = run(g, e[2:], collectors=Rule({("t16", "SAL")}))
    assert g.posted[0]["to"] == "t16"


def test_a_live_ask_that_stops_qualifying_is_cancelled():
    g = Game()
    e = [{"card": "SAL-08", "side": "sell", "to": "t16", "price": 30, "floor": 20}]
    st, _, _ = run(g, e, collectors=Rule({("t16", "SAL")}))
    oid = g.posted[0]["id"]
    st, ev, _ = run(g, e, st, tick=301, collectors=Rule(set()))           # teams.md now says t16 dumps SAL
    assert g.cancelled == [oid] and ev[-1]["event"] == "cancel_not_collector" and "offer" not in st["SAL-08:sell"]



def test_a_dry_run_never_cancels():
    g = Game()
    e = [{"card": "SAL-08", "side": "sell", "to": "t16", "price": 30, "floor": 20}]
    st, _, _ = run(g, e, collectors=Rule({("t16", "SAL")}))
    st, ev, _ = run(g, e, st, tick=301, collectors=Rule(set()), dry_run=True)
    assert g.cancelled == [] and ev[-1]["event"] == "cancel_not_collector" and ev[-1]["dry_run"]


# ------------------------------------------------------------------ the file is the book: edits and removals act now

BID = {"card": "RET-07", "side": "buy", "price": 40, "floor": 55}


def test_removing_an_entry_cancels_its_live_offer():
    # Sunday's plan removes a CHA bid before buying that card from a dealer: a bid left up could fill too (2 copies).
    g = Game()
    st, _, _ = run(g, [BID, {"card": "SAL-08", "side": "sell", "price": 30, "floor": 20}])
    bid = st["RET-07:buy"]["offer"]
    st, ev, _ = run(g, [{"card": "SAL-08", "side": "sell", "price": 30, "floor": 20}], st, tick=301)
    assert g.cancelled == [bid] and "RET-07:buy" not in st and bid not in g.offers
    assert [e["event"] for e in ev] == ["cancel_removed"] and "SAL-08:sell" in st


def test_a_removed_entry_whose_cancel_fails_is_tried_again_and_a_dry_run_cancels_nothing():
    g = Game()
    st, _, _ = run(g, [BID])

    def refuse(oid):
        raise BazaarError("conflict", "busy")
    g.cancel = refuse
    st2, ev, _ = run(g, [], st, tick=301)
    assert ev[-1]["event"] == "cancel_failed" and st2["RET-07:buy"]["offer"] == st["RET-07:buy"]["offer"]
    g = Game()
    st, _, _ = run(g, [BID])
    _, ev, _ = run(g, [], st, tick=301, dry_run=True)
    assert g.cancelled == [] and ev[-1]["dry_run"] is True


def test_a_missing_or_half_written_book_file_changes_nothing(tmp_path):
    assert bk.desired(tmp_path / "none.json") is None
    (tmp_path / "half.json").write_text('{"offers": [{"card": "CHA-0')
    assert bk.desired(tmp_path / "half.json") is None
    (tmp_path / "empty.json").write_text('{"offers": []}')
    assert bk.desired(tmp_path / "empty.json") == []          # an empty book on purpose: everything comes down


def test_editing_the_price_moves_the_live_offer_within_a_tick():
    g = Game()
    st, _, _ = run(g, [BID])
    st, ev, _ = run(g, [{**BID, "price": 50}], st, tick=301)
    assert g.cancelled == [g.posted[0]["id"]] and g.posted[-1]["give"] == {"cash": 50}
    assert ev[-1]["event"] == "move" and ev[-1]["was"] == 40 and st["RET-07:buy"]["since"] == 301
    st, _, _ = run(g, [{**BID, "price": 50}], st, tick=302)
    assert len(g.posted) == 2                                  # moved once, not every tick
    run(g, [{**BID, "price": 90}], st, tick=303)
    assert g.posted[-1]["give"] == {"cash": 55}                # never past the floor


def test_state_from_before_price_edits_does_not_jump_back_to_the_file_price():
    g = Game()
    st, _, _ = run(g, [BID])
    st["RET-07:buy"].pop("entry")
    st["RET-07:buy"]["price"] = 44                             # repriced up by the old book
    g.offers[st["RET-07:buy"]["offer"]]["give"] = {"cash": 44}
    st, _, _ = run(g, [BID], st, tick=301)
    assert len(g.posted) == 1 and st["RET-07:buy"]["entry"] == 40 and st["RET-07:buy"]["price"] == 44


def test_a_price_edit_reads_our_value_again_so_a_page_closer_moves_to_its_new_floor():
    # CHA-08 filled at 12:05, so CHA-05 is the last card (16 -> 122); the Operator sets its price to 72 at 12:06, inside
    # the 10-tick value cache: the move must not clamp to the old cap of 13.
    g = Game(values={"CHA-05": 16.0})
    e = {"card": "CHA-05", "side": "buy", "price": 9, "floor": 72, "page_closer": True}
    st, _, _ = run(g, [e])
    book = bk.Book(g, log=lambda x: None, collectors=AllowAll())
    st = book.step([e], st, {**CLOCK, "tick": 301})
    g.values["CHA-05"] = 122.0
    st = book.step([{**e, "price": 72}], st, {**CLOCK, "tick": 303})
    assert g.posted[-1]["give"] == {"cash": 72} and st["CHA-05:buy"]["price"] == 72


def test_a_bid_whose_card_arrived_another_way_is_cancelled_and_done():
    # The dealer fallback bought CHA-09 while its team bid was still up: take the bid down before a team fills it too.
    g = Game()
    st, _, _ = run(g, [BID])
    g.assets.append({"id": 900, "kind": "card", "ref": "RET-07", "your_value": 60})
    st, ev, _ = run(g, [BID], st, tick=301)
    assert g.cancelled == [g.posted[0]["id"]] and st["RET-07:buy"]["done"] is True
    assert ev[-1]["event"] == "cancel_held"
    run(g, [BID], st, tick=302)
    assert len(g.posted) == 1                                  # done: never posted again



# ------------------------------------------------------------------ review 13:30: cash and clamped edits

def test_a_bid_cash_cannot_cover_goes_out_at_what_cash_allows_and_moves_up_when_cash_frees():
    g = Game(cash=50)
    st, ev, _ = run(g, [BID], cash_floor=20)                 # 50 - 20 = 30 of room for a 40 bid
    assert g.posted[0]["give"] == {"cash": 30} and st["RET-07:buy"]["clamped"] is True
    assert any(e["event"] == "cash_clamp" for e in ev)
    g.cash = 200
    st, _, _ = run(g, [BID], st, tick=300 + bk.VALUE_TICKS, cash_floor=20)
    assert g.posted[-1]["give"] == {"cash": 40} and st["RET-07:buy"]["clamped"] is False


def test_an_edit_the_value_cap_holds_back_lands_once_the_card_is_the_last_one():
    # Review 13:30 (M2): the closer's price set to 72 while value - 3 is 13 must not be used up at 13.
    g = Game(values={"CHA-05": 16.0})
    e = {"card": "CHA-05", "side": "buy", "price": 9, "floor": 72, "page_closer": True}
    st, _, _ = run(g, [e])
    st, _, _ = run(g, [{**e, "price": 72}], st, tick=301)
    assert g.posted[-1]["give"] == {"cash": 13} and st["CHA-05:buy"]["clamped"] is True
    g.values["CHA-05"] = 122.0                                # the other missing card filled: CHA-05 is the last
    st, _, _ = run(g, [{**e, "price": 72}], st, tick=301 + bk.VALUE_TICKS)
    assert g.posted[-1]["give"] == {"cash": 72} and st["CHA-05:buy"]["clamped"] is False


def test_a_file_without_an_offers_list_changes_nothing(tmp_path):
    for text in ("{}", '{"offers": null}', '{"offer": []}'):
        (tmp_path / "b.json").write_text(text)
        assert bk.desired(tmp_path / "b.json") is None



# ------------------------------------------------------------------ last_card: the page's last card bids value - 50

CHA = {"card": "CHA-05", "side": "buy", "price": 9, "floor": 12, "page_closer": True, "last_card": True}


def test_a_last_card_bid_jumps_to_value_minus_50_once_it_is_the_last_one():
    g = Game(values={"CHA-05": 16.0})
    st, _, _ = run(g, [CHA])
    st, ev, _ = run(g, [CHA], st, tick=300 + bk.VALUE_TICKS)            # not the last card: a recheck posts nothing
    assert len(g.posted) == 1 and st["CHA-05:buy"]["checked"] == 300 + bk.VALUE_TICKS
    g.values["CHA-05"] = 122.0                                            # every other CHA card is in: +106
    st, ev, _ = run(g, [CHA], st, tick=300 + 2 * bk.VALUE_TICKS)
    assert g.posted[-1]["give"] == {"cash": 72} and ev[-1]["event"] == "recheck" and ev[-1]["was"] == 9
    st, _, _ = run(g, [CHA], st, tick=300 + 2 * bk.VALUE_TICKS + bk.REPRICE_AFTER)
    assert g.posted[-1]["give"] == {"cash": 72}                           # stays at 72: never above value - 50


def test_a_last_card_bid_takes_what_cash_allows_and_climbs_when_cash_frees():
    g = Game(values={"CHA-05": 122.0}, cash=60)
    st, ev, _ = run(g, [CHA], cash_floor=0)
    assert g.posted[0]["give"] == {"cash": 60} and st["CHA-05:buy"]["clamped"] is True
    g.cash = 300
    run(g, [CHA], st, tick=300 + bk.VALUE_TICKS, cash_floor=0)
    assert g.posted[-1]["give"] == {"cash": 72}


def test_a_rare_that_turns_last_bids_up_to_its_value_minus_50():
    # Review 13:30 (M1): if CHA-05 and CHA-08 fill first, a rare can be the last card: a team at <= 168 still scores +50.
    g = Game(values={"CHA-09": 218.0})
    run(g, [{"card": "CHA-09", "side": "buy", "price": 70, "floor": 90, "page_closer": True, "last_card": True}])
    assert g.posted[0]["give"] == {"cash": 168}



# ------------------------------------------------------------------ review 3 (13:55)

def test_a_cash_clamped_bid_is_not_reposted_every_tick_once_its_reprice_is_due():
    g = Game(cash=50)
    st, _, _ = run(g, [BID], cash_floor=20)                            # 30 of room: bid 30 (wants 40)
    for t in (300 + bk.REPRICE_AFTER, 301 + bk.REPRICE_AFTER, 302 + bk.REPRICE_AFTER):
        st, _, _ = run(g, [BID], st, tick=t, cash_floor=20)
    assert len(g.posted) == 1 and g.cancelled == []                    # the reprice lands on the live 30: no churn


def test_a_climbed_bid_cut_by_cash_recovers_its_climb_not_its_file_price():
    g = Game(cash=400)
    st, _, _ = run(g, [BID])                                           # 40, floor 55
    st, _, _ = run(g, [BID], st, tick=300 + bk.REPRICE_AFTER)          # climbs to 44
    climbed = g.posted[-1]["give"]["cash"]
    assert climbed > 40
    g.cash = 230                                                       # a dealer buy took cash: room 30
    st, _, _ = run(g, [BID], st, tick=301 + bk.REPRICE_AFTER + bk.REFRESH_LEFT + bk.LIFE_TICKS, cash_floor=200)
    assert g.posted[-1]["give"] == {"cash": 30} and st["RET-07:buy"]["want"] >= climbed
    g.cash = 400
    st, _, _ = run(g, [BID], st, tick=301 + bk.REPRICE_AFTER + bk.REFRESH_LEFT + bk.LIFE_TICKS + bk.VALUE_TICKS,
                   cash_floor=200)
    assert g.posted[-1]["give"]["cash"] >= climbed


def test_a_closing_bid_stays_at_value_minus_50_when_only_its_reprice_is_due():
    g = Game(values={"CHA-05": 122.0})
    st, _, _ = run(g, [CHA])
    assert g.posted[-1]["give"] == {"cash": 72}
    st, _, _ = run(g, [CHA], st, tick=300 + bk.REPRICE_AFTER + 1)      # checked at 300 + 20 + 1 > VALUE_TICKS: recheck
    st, _, _ = run(g, [CHA], st, tick=300 + 2 * bk.REPRICE_AFTER + 2)
    assert {o["give"]["cash"] for o in g.posted} == {72}



def test_an_asset_another_offer_holds_is_never_reused_by_an_ask():
    # Review 16:05: book reused its previous asset after its own ask expired, though a swap had locked it meanwhile.
    g = Game()
    e = [{"card": "SAL-08", "side": "sell", "to": "t16", "price": 30, "floor": 20}]
    st = {"SAL-08:sell": {"offer": None, "price": 30, "since": 300, "asset": 179, "held": 1, "entry": 30}}
    g.offers[777] = {"id": 777, "maker": "t05", "status": "open", "give": {"assets": [{"id": 179, "ref": "SAL-08"}]},
                     "want": {"types": ["card:LAT-07"]}}
    st, ev, _ = run(g, e, st, tick=301)
    assert g.posted == [] and any("no free copy" in (x.get("why") or "") for x in ev)


def test_an_addressed_ask_follows_the_counterparty_policy():
    # Chief 16:20: never the top 5 (their gain unknown here); t02 is 4th in this board, t16 isn't ranked.
    g = Game()
    run(g, [{"card": "SAL-08", "side": "sell", "to": "t02", "price": 30, "floor": 20}])
    assert g.posted == []
    g.teams = TOP + [{"team": "t16", "score": 8}]
    run(g, [{"card": "SAL-08", "side": "sell", "to": "t16", "price": 30, "floor": 20}])
    assert g.posted[0]["to"] == "t16"



def test_a_reserved_card_is_never_asked_and_a_live_ask_for_it_comes_down():
    g = Game()
    e = [{"card": "SAL-08", "side": "sell", "to": "t16", "price": 30, "floor": 20}]
    g.teams = TOP + [{"team": "t16", "score": 8}]
    st, _, book = run(g, e)
    oid = g.posted[0]["id"]
    book.reserved = lambda: {"SAL-08"}
    st = book.step(e, st, {**CLOCK, "tick": 301})
    assert g.cancelled == [oid] and "SAL-08:sell" in st and not st["SAL-08:sell"].get("offer")
