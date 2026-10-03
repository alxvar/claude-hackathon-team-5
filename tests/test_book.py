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
    g = Game(cash=230)
    st, ev, _ = run(g, [{"card": "RET-07", "side": "buy", "price": 40, "floor": 55}], cash_floor=200)
    assert g.posted == [] and ev[-1]["event"] == "skip" and "cash floor" in ev[-1]["why"]


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
