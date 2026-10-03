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
