"""tools/album.py: the page arithmetic, id-less copies, stale dealer offers and the seller-safety counts. Synthetic."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import album as al  # noqa: E402

SETS = ("AAA", "BBB")
PG = {s: {"cards": [f"{s}-{i:02d}" for i in range(1, 11)], "book": 100} for s in SETS}
CATALOG = {"sets": [{"id": s, "released": True,
                     "cards": [{"id": f"{s}-{i:02d}", "name": f"{s} {i}", "rarity": "common" if i < 9 else "rare",
                                "minted": 50} for i in range(1, 11)]} for s in SETS]}
CARDS = {c["id"]: {"set": s["id"], "rarity": c["rarity"], "book": 10, "name": c["name"]}
         for s in CATALOG["sets"] for c in s["cards"]}
_id = [0]


def ev(tick, typ, payload, actor=""):
    _id[0] += 1
    return {"id": _id[0], "tick": tick, "type": typ, "actor": actor, "payload": payload}


def settle(tick, aid, ref, frm, to):
    return ev(tick, "settlement", {"items": [{"id": aid, "kind": "card", "ref": ref, "frm": frm, "to": to}]})


def held(team, cards):
    return {(team, c): 1 for c in cards}


def row(filled, pages, slots=20):
    return {"album_filled": filled, "pages_complete": pages, "album_slots": slots}


def test_solve_forces_held_and_gaps():
    # AAA: 9 known, 1 unknown; BBB: 3 known, 7 unknown; 13 held with 1 full page → AAA's last card is held? No:
    # 13 = 9 + 3 + 1 and one full page: the extra card completes AAA (BBB can't reach 10 with one more).
    sol = al.solve([("AAA", 9, 1, 10), ("BBB", 3, 7, 10)], 13, 1)
    assert sol == {"AAA": [1], "BBB": [0]}
    assert al.solve([("AAA", 9, 1, 10), ("BBB", 3, 7, 10)], 13, 0) == {"AAA": [0], "BBB": [1]}
    assert al.solve([("AAA", 9, 1, 10)], 12, 0) is None


def test_team_album_reads_held_gaps_and_undecided():
    n = held("t09", PG["AAA"]["cards"][:9]) | held("t09", ["BBB-01", "BBB-02", "BBB-03"])
    a = al.team_album("t09", n, PG, list(SETS), row(13, 1), gone=set())
    assert a["status"] == "exact" and "AAA-10" in a["held"] and a["complete"] == {"AAA": True, "BBB": False}
    assert {f"BBB-{i:02d}" for i in range(4, 11)} <= a["gap"]
    b = al.team_album("t09", n, PG, list(SETS), row(14, 1), gone=set())   # one more card, AAA full: BBB +1 of 7
    assert b["status"] == "partial" and "AAA-10" in b["held"] and "BBB-04" in b["undecided"]
    assert al.status({"t09": b}, "t09", "BBB-04") == "undecided" and al.status({"t09": b}, "t09", "AAA-10") == "held"
    assert al.team_album("t09", n, PG, list(SETS), row(13, 1, slots=30), gone=set())["status"] == "unknown"


def test_a_card_with_every_copy_traced_is_a_gap_and_the_leaderboard_rarest_is_held():
    n = held("t09", PG["AAA"]["cards"][:9])
    a = al.team_album("t09", n, PG, list(SETS), row(10, 0), gone={"AAA-10"})   # AAA can't complete: a BBB card
    assert "AAA-10" in a["gap"] and a["complete"]["AAA"] is False
    r = al.team_album("t09", n, PG, list(SETS), {**row(10, 0), "rarest": {"ref": "BBB-09"}}, gone={"AAA-10"})
    assert r["status"] == "exact" and "BBB-09" in r["held"] and "BBB-01" in r["gap"]


def test_an_album_the_feed_overcounts_is_repaired_by_one_card():
    n = held("t14", PG["AAA"]["cards"]) | held("t14", PG["BBB"]["cards"][:9])   # 19 seen, the server says 18, 1 page
    a = al.team_album("t14", n, PG, list(SETS), row(18, 1), gone=set())
    assert a["status"] == "repaired" and set(PG["AAA"]["cards"]) <= a["held"]
    assert "BBB-10" in a["gap"] and "BBB-01" in a["undecided"] and al.status({"t14": a}, "t14", "AAA-01") == "held"
    n2 = held("t14", PG["AAA"]["cards"]) | held("t14", PG["BBB"]["cards"])      # 20 seen, server 15, 0 pages: none
    assert al.team_album("t14", n2, PG, list(SETS), row(15, 0), gone=set())["status"] == "inconsistent"


def test_id_less_copies_count_until_a_new_id_claims_them():
    events = [ev(10, "gift.given", {"team": "t03", "cards": ["AAA-01"]}),
              ev(20, "taller.crafted", {"team": "t03", "from": "common", "to": "rare", "card": "AAA 9"}),
              ev(30, "egg.given", {"team": "t03", "cards": ["BBB-02"]})]
    tr = al.trace(events, CARDS)
    assert al.copies(tr) == {("t03", "AAA-01"): 1, ("t03", "AAA-09"): 1, ("t03", "BBB-02"): 1}
    tr = al.trace(events + [settle(40, 500, "AAA-01", "t03", "t08")], CARDS)      # sold a copy never seen: the gift
    assert ("t03", "AAA-01") not in al.copies(tr) and al.copies(tr)[("t08", "AAA-01")] == 1
    tr = al.trace(events + [settle(40, 501, "BBB-02", "abuela", "t03")], CARDS)   # bought another: both count
    assert al.copies(tr)[("t03", "BBB-02")] == 2
    assert al.receipts(events, CARDS)[1][1:3] == ("t03", "AAA-09")
    assert al.crafts(events) == {"t03": [(20, "common")]}


def test_a_dealer_thread_resending_a_sold_copy_is_stale():
    sold = [settle(10, 7, "AAA-03", "t13", "t15"),
            ev(12, "thread.message", {"kind": "persona", "team": "t13", "sender": "t13",
                                      "offer": {"give": {"assets": [{"id": 7, "ref": "AAA-03"}]}}})]
    assert al.trace(sold)[7][1] == "t15"


def test_copies_after_the_last_craft_and_exhausted_supply():
    events = [settle(5, 1, "AAA-02", "abuela", "t01"), settle(50, 2, "AAA-02", "abuela", "t01"),
              ev(30, "taller.crafted", {"team": "t01", "from": "common", "to": "rare", "card": "AAA 9"})]
    events.sort(key=lambda e: e["tick"])
    tr, cr = al.trace(events, CARDS), al.crafts(events)
    lc = al.last_craft(cr, "t01", "common")
    assert lc == 30 and al.copies_after(tr, "t01", "AAA-02", lc) == 1 and al.copies_after(tr, "t01", "AAA-02") == 2
    assert al.last_craft(cr, "t01", "rare") is None
    cat = {"sets": [{"id": "AAA", "cards": [{"id": "AAA-02", "minted": 2}, {"id": "AAA-03", "minted": 5}]}]}
    assert al.exhausted(tr, cat) == {"AAA-02"}


def test_albums_use_released_sets_only():
    cat = {"sets": [{**CATALOG["sets"][0]}, {**CATALOG["sets"][1], "released": False}]}
    n = held("t09", PG["AAA"]["cards"][:9])
    a = al.albums(n, PG, cat, {"t09": row(10, 1, slots=10), "bank": row(1, 0)}, gone=set())
    assert list(a) == ["t09"] and a["t09"]["status"] == "exact" and "AAA-10" in a["t09"]["held"]
    assert al.albums(n, PG, cat, None, gone=set()) == {}
