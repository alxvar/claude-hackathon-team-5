"""Offline tests for tools/matchmaker.py: synthetic catalog, feed and leaderboard; no network, nothing written."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "bazaar-kit"))
import matchmaker as mm  # noqa: E402
from collectors import Collectors, from_feed  # noqa: E402

RARITY = {**{i: ("common", 10) for i in range(1, 6)}, **{i: ("uncommon", 25) for i in (6, 7, 8)},
          9: ("rare", 70), 10: ("rare", 70)}
CATALOG = {"sets": [{"id": "RET", "cards": [{"id": f"RET-{i:02d}", "name": f"Ret {i}", "rarity": r, "book": b,
                                             "page": True} for i, (r, b) in RARITY.items()]
                     + [{"id": "RET-11", "name": "Ret 11", "rarity": "epic", "book": 180, "page": False}]}]}
# us t05 at 30; top 6 = t10..t12; t02 within 3 of us (rival); t16 5.5 below (< 6: no page-closer); t13 a RIVAL
SCORES = {"t10": 40, "t06": 38, "t03": 36, "t14": 35, "t18": 34, "t12": 33, "t05": 30, "t02": 28, "t16": 24.5,
          "t01": 22, "t07": 21, "t09": 20, "t15": 18, "t08": 15, "t13": 10}
TEAMS = [{"team": t, "name": f"Team {int(t[1:])}", "score": s} for t, s in SCORES.items()]
_id = [1000]


def ev(tick, typ, actor, payload):
    _id[0] += 1
    return {"id": _id[0], "tick": tick, "t": tick / 120, "type": typ, "actor": actor, "payload": payload}


def give(team, *refs, frm="abuela", tick=10):
    """One settlement per card: `team` receives a fresh asset of each ref."""
    out = []
    for ref in refs:
        _id[0] += 1
        out.append(ev(tick, "settlement", "", {"parties": [frm, team], "price": 5, "items": [
            {"id": _id[0], "kind": "card", "ref": ref, "frm": frm, "to": team}]}))
    return out


def bid(team, card, cash, tick=50):
    return ev(tick, "offer.listed", team, {"offer": {"id": _id[0] + 1, "maker": team, "give": {"cash": cash},
                                                     "want": {"types": [f"card:{card}"]}}})


def page_but(team, missing):
    return give(team, *[f"RET-{i:02d}" for i in range(1, 11) if f"RET-{i:02d}" not in missing])


def run(events, wants=(), teams_md=None, mult=None):
    coll = Collectors(teams_md or {}, from_feed(events))
    rows, held, prog, names = mm.matches(events=events, catalog=CATALOG, teams=TEAMS, wants=wants, mult=mult or {},
                                         coll=coll)
    return rows, held, prog


def test_page_closer_to_a_far_team_with_a_true_duplicate():
    events = page_but("t09", {"RET-09"}) + give("t08", "RET-09", "RET-09") + [bid("t09", "RET-09", 40)]
    rows, held, prog = run(events)
    assert len(prog[("t09", "RET")]) == 9
    r = rows[0]
    assert (r["buyer"], r["card"], r["seller"]) == ("t09", "RET-09", "t08")
    assert r["closer"] and r["confirmed"] and r["seller_gain"] > 0 and r["buyer_gain"] > 0
    assert r["seller_value"] < r["price"] < r["buyer_value"]
    assert mm.SPARE_LINE in r["dm_seller"]
    for text in (r["dm_seller"], r["dm_buyer"]):
        assert "page" not in text.lower() and "album" not in text.lower()


def test_never_a_page_closer_for_a_rival_or_a_team_close_below_us():
    events = (page_but("t18", {"RET-09"}) + page_but("t16", {"RET-09"}) + give("t08", "RET-09", "RET-09", "RET-09")
              + [bid("t18", "RET-09", 40), bid("t16", "RET-09", 40)])
    rows, held, _ = run(events)
    assert not [r for r in rows if r["card"] == "RET-09" and r["buyer"] in ("t18", "t16")]
    why = {h["buyer"]: h["why"] for h in held}
    assert "rival" in why["t18"] and "below us" in why["t16"]


def test_giver_needs_a_true_duplicate_or_to_dump_the_set():
    events = give("t07", "RET-06") + [bid("t09", "RET-06", 20)]
    low = {"t07": {"RET": (0.5, 0.5, 0.5)}}                         # a team that dumps a set values it low
    assert not run(events, mult=low)[0]                              # one copy, doesn't dump RET: keeps it
    dumps = {"t07": {"collects": set(), "dumps": {"RET"}}}
    rows = run(events, teams_md=dumps, mult=low)[0]
    assert rows and rows[0]["seller"] == "t07" and "dumps" in rows[0]["seller_why"]
    complete = page_but("t07", set()) + [bid("t09", "RET-06", 20)]  # dumps RET but the feed shows its page complete
    assert not run(complete, teams_md=dumps, mult=low)[0]
    assert not run(events, teams_md=dumps)[0]                        # same values on both sides: no gain, no match


def test_receiver_must_show_no_copy_and_collect_the_set():
    dup = give("t08", "RET-06", "RET-06")
    assert not run(dup + give("t01", "RET-06"), wants=[{"team": "t01", "card": "RET-06", "max": None}])[0]
    assert not run(dup + [bid("t01", "RET-06", 20)],                 # teams.md: t01 dumps RET
                   teams_md={"t01": {"collects": set(), "dumps": {"RET"}}})[0]
    rows = run(dup, wants=[{"team": "t01", "card": "RET-06", "max": None}])[0]   # Lucas's want-list counts
    assert rows and rows[0]["buyer"] == "t01" and "want-list" in rows[0]["sources"]


def test_both_sides_must_gain():
    dup = give("t08", "RET-09", "RET-09")
    assert not run(dup, wants=[{"team": "t01", "card": "RET-09", "max": 5}])[0]   # 5 P is below the seller's value
    low_buyer = {"t01": {"RET": (0.1, 0.1, 0.1)}}
    assert not run(dup + [bid("t01", "RET-09", 40)], mult=low_buyer)[0]          # the buyer values it below the seller
    rows = run(dup, wants=[{"team": "t01", "card": "RET-09", "max": 30}])[0]
    assert rows[0]["price"] <= 30 and rows[0]["seller_gain"] > 0


def test_one_spare_goes_to_one_buyer():
    events = give("t08", "RET-07", "RET-07") + [bid("t09", "RET-07", 20), bid("t01", "RET-07", 20)]
    rows = run(events)[0]
    assert [r["seller"] for r in rows] == ["t08"]                    # 2 copies: 1 spare
    events += give("t15", "RET-07", "RET-07")
    rows = run(events)[0]
    assert sorted(r["seller"] for r in rows) == ["t08", "t15"] and len({r["buyer"] for r in rows}) == 2


def test_rival_on_either_side_gains_at_most_ten():
    rows = run(give("t18", "RET-09", "RET-09") + [bid("t09", "RET-09", 40)])[0]
    r = rows[0]
    assert r["rival_seller"] and r["price"] - r["seller_value"] <= mm.RIVAL_GAIN_MAX
    rows = run(give("t08", "RET-09", "RET-09") + [bid("t13", "RET-09", 40)])[0]
    r = rows[0]
    assert r["rival_buyer"] and r["buyer_value"] - r["price"] <= mm.RIVAL_GAIN_MAX
    assert not run(give("t18", "RET-09", "RET-09") + [bid("t13", "RET-09", 40)])[0]   # both rivals: never


def test_page_closers_rank_first():
    events = (page_but("t09", {"RET-03"}) + give("t08", "RET-03", "RET-03")
              + give("t15", "RET-11", "RET-11") + [bid("t01", "RET-11", 150)])
    rows = run(events)[0]
    assert rows[0]["closer"] and rows[0]["card"] == "RET-03"
    assert rows[1]["card"] == "RET-11" and rows[1]["vc"] > rows[0]["vc"] * 0   # the epic first copy follows


def test_parse_wants():
    text = ("# Wants\n- t07 RET-05 40\n- Team 9: SAL-09 up to 75 P\n| Team 12 | MAL-03 | 9 |\n|---|---|---|\n"
            "- t03 LAV-02\nplain line t04 RET-01 20\n")
    got = mm.parse_wants(text)
    assert {"team": "t07", "card": "RET-05", "max": 40.0} in got
    assert {"team": "t09", "card": "SAL-09", "max": 75.0} in got
    assert {"team": "t12", "card": "MAL-03", "max": 9.0} in got
    assert {"team": "t03", "card": "LAV-02", "max": None} in got
    assert not [w for w in got if w["team"] == "t04"]


def test_fair_price_sits_where_no_cap_is_wasted():
    assert mm.fair_price(2.5, 76, 9) == 26             # window [26, 52.5]: clearing 9 moves up to 26
    assert 100 <= mm.fair_price(50.5, 185.4, 70) <= 101   # both cap in [100.5, 135.4]
    assert mm.fair_price(5, 30, 9) == 9                # clearing inside the window
    assert mm.fair_price(100, 300, None) == 200         # no clearing price (epic): the midpoint
    assert mm.fair_price(10, 12, 50) == 11              # strictly between the two values


def test_render_lists_matches_dms_and_held_back():
    events = (page_but("t09", {"RET-09"}) + page_but("t18", {"RET-09"}) + give("t08", "RET-09", "RET-09")
              + [bid("t09", "RET-09", 40)])
    rows, held, prog = run(events)
    names = {t["team"]: t["name"] for t in TEAMS}
    text = mm.render(rows, held, prog, names, mm.pages(CATALOG), tick=1, riv={"t18"})
    assert "| 1 | Team 9 | RET-09" in text and "Ready DMs" in text and mm.SPARE_LINE in text
    assert "Team 18 RET 9/10 · missing RET-09 · rival" in text and "Held back" in text


def test_known_holdings_beat_the_feed(tmp_path):
    f = tmp_path / "known.json"
    f.write_text('{"t09": {"missing": ["RET-09"]}, "t01": {"complete": ["ret"]}, "bad": 1, "t07": {"missing": ["x"]}}')
    known = mm.load_known(f)
    assert known["t09"] == {"complete": set(), "missing": {"RET-09"}} and known["t01"]["complete"] == {"RET"}
    assert "bad" not in known
    events = give("t08", "RET-09", "RET-09") + give("t09", "RET-01") + [bid("t01", "RET-06", 20)] \
        + give("t15", "RET-06", "RET-06")
    coll = Collectors({}, from_feed(events))
    rows, held, prog, _ = mm.matches(events=events, catalog=CATALOG, teams=TEAMS, coll=coll, known=known)
    assert len(prog[("t09", "RET")]) == 9                            # told: only RET-09 missing
    r = [x for x in rows if x["buyer"] == "t09"][0]
    assert r["card"] == "RET-09" and r["closer"] and "known want" in r["sources"] and r["confirmed"]
    assert not [x for x in rows if x["buyer"] == "t01"]              # RET complete: never a RET buyer, bid or not


def test_a_known_team_buys_only_what_it_said_it_misses():
    known = {"t09": {"complete": set(), "missing": {"RET-09"}}}
    events = give("t08", "RET-07", "RET-07", "RET-09", "RET-09") + [bid("t09", "RET-07", 20)]
    coll = Collectors({}, from_feed(events))
    rows = mm.matches(events=events, catalog=CATALOG, teams=TEAMS, coll=coll, known=known)[0]
    assert [r["card"] for r in rows if r["buyer"] == "t09"] == ["RET-09"]


def test_page_open_trusts_the_servers_pages_complete():
    pg = mm.pages(CATALOG)
    prog = {("t09", "RET"): {f"RET-{i:02d}" for i in range(1, 10)}}
    kw = dict(prog=prog, pg=pg, last={})
    assert mm.page_open("t09", "RET", "RET-10", lb=None, **kw)[0]                         # no leaderboard: as before
    assert mm.page_open("t09", "RET", "RET-10", lb={"t09": {"pages_complete": 0}}, **kw)[0]
    ok, why = mm.page_open("t09", "RET", "RET-10", lb={"t09": {"pages_complete": 1}}, **kw)
    assert not ok and "may be complete" in why                                             # 1 complete, feed sees 0
    assert not mm.page_open("t09", "RET", "RET-10", lb={}, **kw)[0]                        # unknown: not open
    recent = {("t09", "RET-10"): {"kind": "lack", "tick": 900}}
    assert mm.page_open("t09", "RET", "RET-10", lb={"t09": {"pages_complete": 1}}, prog=prog, pg=pg, last=recent,
                        tick=950)[0]                                                       # it bid 50 ticks ago
    assert not mm.page_open("t09", "RET", "RET-10", lb={"t09": {"pages_complete": 1}}, prog=prog, pg=pg,
                            last=recent, tick=900 + mm.RECENT_TICKS + 1)[0]
    known = {"t09": {"complete": set(), "missing": {"RET-10"}}}
    assert mm.page_open("t09", "RET", "RET-10", lb={"t09": {"pages_complete": 1}}, known=known, **kw)[0]


def test_a_page_the_server_may_have_closed_gets_no_closer(tmp_path):
    events = page_but("t09", {"RET-09"}) + give("t08", "RET-09", "RET-09")
    coll = Collectors({"t09": {"collects": {"RET"}, "dumps": set()}}, from_feed(events))
    kw = dict(events=events, catalog=CATALOG, teams=TEAMS, coll=coll)
    rows = mm.matches(**kw, lb={"t09": {"pages_complete": 0}}, tick=100)[0]
    assert rows and rows[0]["closer"]
    assert not mm.matches(**kw, lb={"t09": {"pages_complete": 1}}, tick=100)[0]           # may be done: no match
    events += [bid("t09", "RET-09", 40, tick=95)]
    rows = mm.matches(**{**kw, "events": events}, lb={"t09": {"pages_complete": 1}}, tick=100)[0]
    assert rows and rows[0]["closer"]                                                     # a fresh bid: still open


# ---- Market 01:00 (intel/holdings-audit.md): page arithmetic, bid expiry, known-entry vetting, seller safety, DMs

def lbrow(filled, pages):
    return {"album_filled": filled, "pages_complete": pages, "album_slots": 10}


def test_a_friday_bid_proves_nothing():
    sat = ev(159, "day.opened", "", {"day": "sat"})
    events = give("t08", "RET-06", "RET-06") + [bid("t01", "RET-06", 30, tick=100), sat]
    events.sort(key=lambda e: (e["tick"], e["id"]))
    assert mm.bids_since(events) == 159
    assert not run(events)[0]
    events += [bid("t01", "RET-06", 30, tick=200)]                        # a Saturday bid does
    assert [(r["buyer"], r["card"]) for r in run(events)[0]] == [("t01", "RET-06")]


def test_a_bid_expires_when_the_bidder_gets_the_card_another_way():
    events = give("t08", "RET-06", "RET-06") + [bid("t01", "RET-06", 30, tick=50),
                                                ev(60, "egg.given", "banco", {"team": "t01", "cards": ["RET-06"]})]
    assert not run(events)[0]
    crafted = give("t08", "RET-06", "RET-06") + [bid("t01", "RET-06", 30, tick=50),
                                                 ev(60, "taller.crafted", "", {"team": "t01", "from": "common",
                                                                               "to": "uncommon", "card": "Ret 6"})]
    assert not run(crafted)[0]


def test_page_arithmetic_beats_the_feed_on_both_sides():
    # t09 shows 8 RET cards; the server says 10 held, 1 page: RET-09/10 are held, the page is done, no match
    events = page_but("t09", {"RET-09", "RET-10"}) + give("t08", "RET-09", "RET-09") + [bid("t09", "RET-09", 40)]
    coll = Collectors({}, from_feed(events))
    kw = dict(events=events, catalog=CATALOG, teams=TEAMS, coll=coll)
    assert not mm.matches(**kw, lb={"t09": lbrow(10, 1)}, tick=60)[0]
    # the server says 8 held, 0 pages: RET-09 is a proven gap; with one more held it's a page-closer
    info = {}
    rows = mm.matches(**kw, lb={"t09": lbrow(8, 0), "t08": lbrow(1, 0)}, tick=60, info=info)[0]
    r = rows[0]
    assert (r["buyer"], r["card"], r["holding"], r["confirmed"]) == ("t09", "RET-09", "gap", True)
    assert info["albums"]["t09"]["status"] == "exact" and "RET-10" in info["albums"]["t09"]["gap"]


def test_a_known_entry_the_feed_contradicts_is_ignored_and_reported():
    known = {"t15": {"complete": set(), "missing": {"RET-09"}}}
    events = give("t15", "RET-09") + give("t08", "RET-09", "RET-09")
    coll = Collectors({"t15": {"collects": {"RET"}, "dumps": set()}}, from_feed(events))
    info = {}
    rows = mm.matches(events=events, catalog=CATALOG, teams=TEAMS, coll=coll, known=known, info=info)[0]
    assert not [r for r in rows if r["buyer"] == "t15"] and "RET-09" in info["rejected"]["t15"]
    text = mm.render(rows, [], {}, {"t15": "Team 15"}, mm.pages(CATALOG), rejected=info["rejected"])
    assert "entry for Team 15 ignored" in text


def test_a_seller_whose_page_is_complete_and_crafted_since_is_held_back():
    craft = ev(30, "taller.crafted", "", {"team": "t08", "from": "rare", "to": "epic", "card": "Ret 11"})
    events = give("t08", *[f"RET-{i:02d}" for i in range(1, 11)], tick=10) + give("t08", "RET-09", tick=20) \
        + [craft] + page_but("t09", {"RET-09"}) + [bid("t09", "RET-09", 40)]
    rows, held, _ = run(events)
    assert not [r for r in rows if r["seller"] == "t08"]
    assert any("seller safety" in h["why"] and h["card"] == "RET-09" for h in held)
    later = events + [ev(40, "offer.listed", "t08", {"offer": {"id": 1, "maker": "t08", "give": {"assets": [
        {"id": 9001, "ref": "RET-09"}, {"id": 9002, "ref": "RET-09"}]}, "want": {"cash": 90}}})]
    rows = run(later)[0]                                                   # two copies seen after the craft: fine
    assert [(r["seller"], r["card"]) for r in rows if r["buyer"] == "t09"] == [("t08", "RET-09")]


def test_dms_are_addressed_to_the_other_side():
    events = page_but("t09", {"RET-09"}) + give("t08", "RET-09", "RET-09") + [bid("t09", "RET-09", 40)]
    r = run(events)[0][0]
    assert "addressed to Team 9" in r["dm_seller"] and "addressed to Team 9" in r["dm_buyer"]
    assert "Team 8" in r["dm_buyer"] and "open" not in (r["dm_seller"] + r["dm_buyer"]).lower()


# ---- club venue routing (directives 01:10/01:20; Lucas Sun 08:00: half on v10, half on members' markets)

def crow(seller, buyer, card="RET-05", closer=False):
    return {"seller": seller, "buyer": buyer, "card": card, "closer": closer, "seller_name": f"Team {int(seller[1:])}",
            "buyer_name": f"Team {int(buyer[1:])}", "card_name": card, "price": 9}


VENUES = {v: {"owner": o, "status": "open", "name": f"Mercado {o}"} for o, v in mm.CLUB_VENUES.items()}
CLUB_TEAMS = [{"team": t, "market": m} for t, m in
              {"t02": 1.0, "t04": 5.0, "t07": 0.5, "t08": 3.0, "t09": 2.0, "t15": 0.0}.items()]


def test_club_deals_alternate_v10_and_a_member_market():
    rows = [crow("t07", "t09"), crow("t02", "t04", "RET-06"), crow("t08", "t15", "RET-07"), crow("t04", "t02", "RET-01")]
    st = mm.route(rows, teams=CLUB_TEAMS, venues=VENUES, state={}, day="d1")
    assert [r["venue"] for r in rows] == ["v10", "v15", "v10", "v11"]    # t15's v15 (lowest market), then t07's v11
    assert st["v10"] == 2 and st["member"] == 2                          # (v15 already used once)
    assert "on v15 (Team 15's market) as an ask addressed to Team 4" in rows[1]["dm_seller"]
    assert "on v10 as an ask addressed to Team 9" in rows[0]["dm_buyer"]


def test_never_a_party_s_own_market_and_closers_and_outsiders_stay_on_v10():
    rows = [crow("t15", "t07"), crow("t07", "t15", "RET-02"),            # v10, then a market owned by neither
            crow("t09", "t02", "RET-09", closer=True),                   # a page-closer: v10 (a v10 turn)
            crow("t16", "t09", "RET-03"),                                # a non-member: v10, not counted
            crow("t08", "t04", "RET-04")]                                # member turn
    st = mm.route(rows, teams=CLUB_TEAMS, venues=VENUES, state={}, day="d1")
    assert [r["venue"] for r in rows] == ["v10", "v26", "v10", "v10", "v15"]
    assert not rows[3]["club"] and st["v10"] == 2 and st["member"] == 2
    for r in rows:
        assert r["venue"] not in (mm.CLUB_VENUES.get(r["buyer"]), mm.CLUB_VENUES.get(r["seller"]))


def test_a_row_keeps_its_venue_across_runs_and_the_day_resets():
    st = mm.route([crow("t07", "t09"), crow("t02", "t04", "RET-06")], teams=CLUB_TEAMS, venues=VENUES, state={},
                  day="d1")
    again = [crow("t02", "t04", "RET-06"), crow("t08", "t15", "RET-07")]   # the first deal fired and left the list
    mm.route(again, teams=CLUB_TEAMS, venues=VENUES, state=st, day="d1")
    assert again[0]["venue"] == "v15" and again[1]["venue"] == "v10"    # kept; the new one takes the next turn
    fresh = [crow("t02", "t04", "RET-06")]
    mm.route(fresh, teams=CLUB_TEAMS, venues=VENUES, state=st, day="d2")
    assert fresh[0]["venue"] == "v10" and st["day"] == "d2"             # a new day starts on v10


def test_a_closed_or_rival_market_is_never_picked():
    closed = {**VENUES, "v15": {**VENUES["v15"], "status": "closed"}}
    rows = [crow("t07", "t09"), crow("t02", "t04", "RET-06")]
    mm.route(rows, teams=CLUB_TEAMS, venues=closed, state={}, day="d1")
    assert rows[1]["venue"] == "v11"                                     # v15 closed: the next lowest
    rows = [crow("t07", "t09"), crow("t02", "t04", "RET-06")]
    mm.route(rows, teams=CLUB_TEAMS, venues=VENUES, state={}, riv={"t07", "t15", "t09", "t08", "t02", "t04"},
             day="d1")
    assert rows[1]["venue"] == "v10"                                     # every member a rival: v10


def test_a_deal_the_market_doesn_t_fire_doesn_t_take_a_turn():
    """Chief 01:25: no club deal under +3 VC nor with a rival party: v10, not counted."""
    rows = [crow("t07", "t09"), {**crow("t04", "t07", "SAL-01"), "vc": 1.2},
            {**crow("t02", "t08", "RET-03"), "rival_buyer": True}, crow("t02", "t04", "RET-06")]
    st = mm.route(rows, teams=CLUB_TEAMS, venues=VENUES, state={}, day="d1")
    assert [r["venue"] for r in rows] == ["v10", "v10", "v10", "v15"] and [r["club"] for r in rows] == \
        [True, False, False, True] and (st["v10"], st["member"]) == (1, 1)


def test_member_markets_come_from_the_live_venue_list():
    """Market 10:50: t07's v11 closed for board v29; v06 charges 1%: the live list wins, the fee breaks ties."""
    live = {**VENUES, "v11": {**VENUES["v11"], "status": "closed"},
            "v29": {"owner": "t07", "status": "open", "name": "Team 7 board", "opened_tick": 1758},
            "v06": {**VENUES["v06"], "fee_bps": 100}, "rastro": {"owner": "world", "status": "open", "house": True}}
    mk = mm.member_markets(live)
    assert mk["t07"] == "v29" and mk["t08"] == "v06" and "world" not in mk
    two = {**live, "v30": {"owner": "t02", "status": "open", "fee_bps": 50}}       # t02: v26 (0%) beats v30 (0.5%)
    assert mm.member_markets(two)["t02"] == "v26"
    rows = [crow("t07", "t09"), crow("t04", "t02", "RET-06")]
    teams = [{"team": t, "market": 0.0} for t in mm.CLUB]                         # all tied: the fee decides
    mm.route(rows, teams=teams, venues=live, state={}, day="d1")
    assert rows[1]["venue"] != "v06" and "0% fee" not in rows[1]["dm_seller"]
    assert mm.member_markets(None) == mm.CLUB_VENUES
