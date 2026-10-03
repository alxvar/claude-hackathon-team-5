"""Offline tests for tools/opportunities.py on real Friday data (tests/fixtures/opportunities_friday.json: slices of
data/feed.jsonl and data/board.json, plus /api/leaderboard, /api/me, /api/catalog and /api/clock at the frozen tick
159). The game is a fake that records calls; nothing is ever posted and no notification is sent."""
import copy
import json
import math
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "bazaar-kit"))
import opportunities as op  # noqa: E402
from bazaar_sdk import BazaarError  # noqa: E402

FX = json.loads((ROOT / "tests" / "fixtures" / "opportunities_friday.json").read_text())
NOW = 1_800_000_000.0  # wall clock for state and cooldowns
TICK = FX["clock"]["tick"]  # 159, t 2.65 h


def fx():
    return copy.deepcopy(FX)


def cards_of(f):
    return {c["id"]: {"set": s["id"], "rarity": c["rarity"], "book": c["book"], "name": c["name"]}
            for s in f["catalog"]["sets"] for c in s["cards"]}


def lack_event(team, card, tick, eid):
    """A real dealer-thread event (Team 7 asking Abuela for SAL-02), re-pointed at another team and card."""
    e = copy.deepcopy(next(e for e in FX["events"] if e["id"] == 7392))
    e.update(id=eid, tick=tick, t=round(tick / 60, 4))
    e["payload"].update(team=team, topic={"buy": {"card": card}})
    return e


def pull_event(team, card, tick, eid):
    """A real pack.opened event (Team 12 pulling SAL-09), re-pointed at another team and card."""
    e = copy.deepcopy(next(e for e in FX["events"] if e["id"] == 4454))
    e.update(id=eid, tick=tick, t=round(tick / 60, 4))
    e["payload"]["team"] = team
    e["payload"]["best"].update(ref=card, set=card[:3])
    return e


def engine(f=None, values=None, build=("RET", "CHA"), cash_floor=200, collectors=None):
    f = f or fx()
    ev = sorted(f["events"], key=lambda e: (e["tick"], e["id"]))
    return op.find_opportunities(events=ev, board=f["board"], lb=f["leaderboard"], cat=f["catalog"], me=f["me"],
                                 value_of=lambda c: (values or {}).get(c), build=build, cash_floor=cash_floor,
                                 now_tick=TICK, gt=op.GameTime(ev), collectors=collectors)


def signals(f=None):
    f = f or fx()
    ev = sorted(f["events"], key=lambda e: (e["tick"], e["id"]))
    return op.read_signals(ev, f["board"], "t05", op.GameTime(ev), TICK, cards_of(f))


def find(opps, side, team, card):
    return next((o for o in opps if o["side"] == side and o["team"] == team and o["card"] == card), None)


# ------------------------------------------------------------------------------------------------ lack / hold

def test_lack_from_dealer_thread_and_bids():
    last, _ = signals()
    assert last[("t07", "SAL-02")]["kind"] == "lack" and "asked abuela" in last[("t07", "SAL-02")]["src"]
    assert last[("t08", "LAV-03")]["kind"] == "lack" and last[("t08", "LAV-03")]["price"] == 2  # bid at tick 150
    live = last[("t02", "LAT-03")]  # Team 2's bid 2725 is still on the board
    assert live["kind"] == "lack" and live["live"] and "offer 2725" in live["src"]


def test_hold_from_listing_settlement_pack_gift_and_dealer_offer():
    last, _ = signals()
    assert last[("t07", "SAL-04")]["kind"] == "hold"            # listed at tick 159
    assert last[("t12", "SAL-09")]["kind"] == "hold"            # pack.opened best
    assert last[("t10", "LAV-02")]["kind"] == "hold"            # settlement items[].to (backfilled, no `t`)
    assert last[("t06", "LAV-02")]["kind"] == "gone"            # the seller: no longer a known holder
    assert last[("t02", "LAT-04")]["kind"] == "hold" and last[("t02", "LAT-04")]["live"]  # gift, then listed now
    offered = next(e for e in FX["events"] if e["id"] == 10879)["payload"]["offer"]["give"]["assets"][0]["ref"]
    assert last[("t07", offered)]["kind"] == "hold" and "offered it to chato" in last[("t07", offered)]["src"]


def test_settlement_after_a_bid_turns_lack_into_hold():
    last, prof = signals()
    s = last[("t15", "LAT-10")]  # bid 60 at tick 140, bought it from t06 at tick 142
    assert s["kind"] == "hold" and s["tick"] == 142
    assert prof[("t15", "LAT")]["collects"] and max(prof[("t15", "LAT")]["ratios"]) == pytest.approx(60 / 70)


def test_our_own_offers_and_dealers_are_not_signals():
    f = fx()
    f["events"].append(lack_event("t05", "SAL-03", 158, 99001))
    f["events"].append(lack_event("abuela", "SAL-03", 158, 99002))
    last, _ = signals(f)
    assert not any(team in ("t05", "abuela") for team, _ in last)


# ------------------------------------------------------------------------------------------------ our spares

def test_never_sell_the_only_copy_of_a_completed_or_building_page():
    f = fx()
    ret = copy.deepcopy(f["me"]["assets"][0])
    ret.update(id=88001, ref="RET-03", set="RET", your_value=11.0)
    f["me"]["assets"].append(ret)
    f["events"] += [lack_event("t09", "LAV-01", 158, 99001),   # LAV page complete, one copy: never
                    lack_event("t09", "RET-03", 158, 99002),   # RET page we build, one copy: never
                    lack_event("t01", "LAV-02", 158, 99003),   # LAV, second copy: a spare
                    lack_event("t16", "MAL-02", 158, 99004)]   # MAL (not built), one copy: sellable
    opps, _ = engine(f)
    assert find(opps, "SELL", "t09", "LAV-01") is None
    assert find(opps, "SELL", "t09", "RET-03") is None
    lav = find(opps, "SELL", "t01", "LAV-02")
    assert lav and lav["our_value"] == pytest.approx(3.2) and lav["price"] == 40 and lav["gain"] == pytest.approx(36.8)
    assert find(opps, "SELL", "t16", "MAL-02")["our_value"] == 7.0


def test_a_spare_already_listed_by_us_is_not_offered_twice():
    f = fx()
    lav = [a for a in f["me"]["assets"] if a["ref"] == "LAV-02"]
    f["board"].append({"id": 77001, "team": "t05", "give": {"cash": 0, "assets": [lav[0]], "types": []},
                       "want": {"cash": 30, "assets": [], "types": []}})
    f["events"].append(lack_event("t01", "LAV-02", 158, 99003))
    opps, _ = engine(f)
    assert find(opps, "SELL", "t01", "LAV-02") is None  # one copy listed, the other protects the LAV page


# ------------------------------------------------------------------------------------------------ feeding filter

def test_feeding_filter_on_the_real_leaderboard():
    opps, ctx = engine()
    assert ctx["ours"] == 20.03 and ctx["top"] == {"t13", "t12", "t17", "t10", "t05"}   # top 5 (16:20), us included
    t07 = find(opps, "SELL", "t07", "SAL-02")             # Team 7 at 8.98: 11.05 below us
    assert t07["reasons"] == [] and t07["gap"] == pytest.approx(11.05)
    t08 = find(opps, "SELL", "t08", "LAV-03")             # Team 8 at 17.65: close, but it lacks LAV-09/10 too
    assert t08["reasons"] == [] and not t08["closing"]     # plan §4A: not a page-closer, so no 10-point rule
    t12 = find(opps, "SELL", "t12", "MAL-07")             # Team 12: top 4 and above us
    assert "top 5" in t12["reasons"] and any("above us" in r for r in t12["reasons"])


def test_feeding_gap_boundary():
    f = fx()
    for t in f["leaderboard"]["teams"]:
        if t["team"] == "t07":
            t["score"] = 14.03                            # exactly 6 below: allowed (policy 16:20: was 10)
        if t["team"] == "t02":
            t["score"] = 14.04                            # 5.99 below: refused
    opps, _ = engine(f)
    assert find(opps, "SELL", "t07", "SAL-02")["reasons"] == []
    assert any("below us" in r for r in find(opps, "SELL", "t02", "LAT-03")["reasons"])


# ------------------------------------------------------------------------------------------------ prices

def test_sell_price_rules():
    last_common = 10 + 66.25
    assert op.sell_price("common", 3.25, last_common) == 40                     # nothing known about the buyer
    assert op.sell_price("uncommon", 17.5, 25 + 66.25) == 45
    assert op.sell_price("common", 3.25, last_common, m_est=0.5) == 19          # cheap buyer: half of 76 × 0.5
    assert op.sell_price("common", 30.0, last_common, m_est=0.5) == 33          # never below value + 3
    assert op.sell_price("common", 2.0, last_common, m_est=0.5, live_bid=25) == 25  # their live bid is the floor
    assert op.sell_price("epic", 50, 180) is None


def test_sell_prices_on_real_buyers():
    opps, _ = engine()
    assert find(opps, "SELL", "t02", "LAT-03")["price"] == 19   # Team 2 bid 12 for LAT-06: m ≥ 0.48 → 0.5
    assert find(opps, "SELL", "t08", "LAT-03")["price"] == 27   # Team 8 bid 18 for LAT-06/07: m ≥ 0.72
    assert find(opps, "SELL", "t07", "SAL-02")["price"] == 40   # Team 7 never showed a price: base


def test_buy_price_rules():
    assert op.fee(70) == 5 and op.fee(8) == 2
    assert op.max_buy_price(77) == 74                           # they accept our bid: no fee
    assert op.max_buy_price(77, we_accept=True) == 69           # 69 + ceil(3.45) + 1 = 74
    assert op.buy_price(70, 77) == 70                           # book
    assert op.buy_price(70, 72) == 69                           # capped at value − 3
    assert op.buy_price(70, 77, live_ask=60) == 60              # their own ask
    assert op.buy_price(10, 3) is None


def ret_page_fixture(missing=("RET-10",), holder="t09"):
    """Our album with the RET page complete but for `missing`; `holder` pulled each missing card at tick 158."""
    f = fx()
    for s in f["catalog"]["sets"]:
        if s["id"] == "RET":
            s["released"] = True
    base = f["me"]["assets"][0]
    for i in range(1, 11):
        ref = f"RET-{i:02d}"
        if ref not in missing:
            a = copy.deepcopy(base)
            a.update(id=88000 + i, ref=ref, set="RET", your_value=11.0)
            f["me"]["assets"].append(a)
    for j, ref in enumerate(missing):
        f["events"].append(pull_event(holder, ref, 158, 99100 + j))
    return f


def test_buy_that_completes_our_page():
    f = ret_page_fixture()
    opps, _ = engine(f, values={"RET-10": 77 + 72.9}, cash_floor=100)
    o = find(opps, "BUY", "t09", "RET-10")
    assert o["completes"] and o["price"] == 70 and o["gain"] == 50 and o["max_price"] == 146 and o["reasons"] == []
    assert not o["collects"]                                    # Team 9 never bid for RET: ranks first


def test_buy_respects_cash_floor_and_top_4():
    f = ret_page_fixture()
    o = find(engine(f, values={"RET-10": 149.9}, cash_floor=200)[0], "BUY", "t09", "RET-10")
    assert any("cash floor" in r for r in o["reasons"])         # 252 − 70 < 200
    f = ret_page_fixture(holder="t13")
    o = find(engine(f, values={"RET-10": 149.9}, cash_floor=100)[0], "BUY", "t13", "RET-10")
    assert "top 5" in o["reasons"]


# ------------------------------------------------------------------------------------------------ strategic filter

def opp(team, card, gain=30, age=5, completes=False, side="SELL"):
    return {"side": side, "team": team, "card": card, "gain": gain, "age_min": age, "confident": age <= 30,
            "completes": completes, "reasons": []}


def test_thresholds_gain_confidence_and_page_completion():
    opps = [opp("t01", "A-01", gain=19.9), opp("t02", "A-02", age=31), opp("t03", "A-03", gain=5, completes=True)]
    picked = op.choose_alerts(opps, {"alerts": [], "live": []}, NOW)
    assert [o["team"] for o in picked] == ["t03"]
    assert opps[0]["status"].startswith("listed only: gain") and opps[1]["status"].startswith("listed only: signal")


def test_max_three_alerts_per_hour():
    state = {"alerts": [{"ts": NOW - 600, "team": "t09", "card": "X-01"}], "live": []}
    opps = [opp("t01", "A-01"), opp("t02", "A-02"), opp("t03", "A-03")]
    picked = op.choose_alerts(opps, state, NOW)
    assert len(picked) == 2 and opps[2]["status"].startswith("held: 3 alerts")
    state["alerts"] = [{"ts": NOW - 3700, "team": "t09", "card": "X-01"}] * 3   # over an hour ago: free again
    assert len(op.choose_alerts([opp("t01", "A-01")], state, NOW)) == 1


def test_team_cooldown_45_min_and_one_per_team_per_run():
    state = {"alerts": [{"ts": NOW - 30 * 60, "team": "t07", "card": "SAL-05"}], "live": []}
    assert op.choose_alerts([opp("t07", "SAL-02")], state, NOW) == []
    state["alerts"][0]["ts"] = NOW - 50 * 60
    assert len(op.choose_alerts([opp("t07", "SAL-02")], state, NOW)) == 1
    two = [opp("t07", "SAL-02"), opp("t07", "SAL-01")]
    assert len(op.choose_alerts(two, {"alerts": [], "live": []}, NOW)) == 1 and two[1]["status"].startswith("cooldown: team")


def test_same_team_and_card_never_twice_in_2_hours():
    state = {"alerts": [{"ts": NOW - 90 * 60, "team": "t07", "card": "SAL-02"}], "live": []}
    o = opp("t07", "SAL-02")
    assert op.choose_alerts([o], state, NOW) == [] and o["status"].startswith("cooldown: same team + card")
    state["alerts"][0]["ts"] = NOW - 121 * 60
    assert len(op.choose_alerts([opp("t07", "SAL-02")], state, NOW)) == 1


def test_never_more_than_three_live_offers():
    live = [{"team": f"t1{i}", "card": "X", "status": "live"} for i in range(3)]
    o = opp("t01", "A-01")
    assert op.choose_alerts([o], {"alerts": [], "live": live}, NOW) == [] and o["status"].startswith("held: 3 opportunity")


def test_real_friday_team_7_lacks_three_salamanca_cards_so_its_sale_goes_out_addressed():
    # Plan §4A: only a page-closer (their last or second-to-last card) needs the 10-point gap; this one closes no page.
    opps, _ = engine()
    o = find(opps, "SELL", "t07", "SAL-02")
    assert o["reasons"] == [] and o["other_lacks"] == ["SAL-01", "SAL-05"] and not o["closing"]
    picked = op.choose_alerts(opps, {"alerts": [], "live": []}, NOW)
    assert ("t07", "SAL-02") in [(x["team"], x["card"]) for x in picked]


T08_BIDS = (8072, 9820)   # Team 8's bids for LAT-03 and LAV-03, the cards we could sell it


def single_gap_fixture():
    """Real Friday data where Team 7 asked Abuela only for SAL-02 (its other two asks removed), Team 8 not buying."""
    f = fx()
    f["events"] = [e for e in f["events"] if e["id"] not in (6681, 7907, *T08_BIDS)]
    return f


def test_page_closer_sale_is_alerted():
    opps, _ = engine(single_gap_fixture())
    picked = op.choose_alerts(opps, {"alerts": [], "live": []}, NOW)
    assert [(o["team"], o["card"], o["price"]) for o in picked] == [("t07", "SAL-02", 40)]


def test_one_other_lack_is_still_a_second_to_last_card():
    f = fx()
    f["events"] = [e for e in f["events"] if e["id"] not in (6681, *T08_BIDS)]   # Team 7 lacks SAL-02, SAL-01
    opps, _ = engine(f)
    picked = op.choose_alerts(opps, {"alerts": [], "live": []}, NOW)
    assert [(o["team"], o["card"]) for o in picked] == [("t07", "SAL-02")]
    assert find(opps, "SELL", "t07", "SAL-01")["status"].startswith("cooldown: team")


# ------------------------------------------------------------------------------------------------ runs

class FakeApi:
    """The game from the fixture. Records every call; list_offer answers with an id but nothing is sent anywhere."""

    def __init__(self, f=None, open_offers=None, fail_post=None, log=None, venues=None):
        self.f, self.calls, self.open_offers, self.fail_post = f or fx(), [], open_offers or [], fail_post
        self._venues = venues or []
        self.log = log if log is not None else []

    def _c(self, name, *a):
        self.calls.append((name, a))
        self.log.append(name)

    def clock(self):
        self._c("clock")
        return self.f["clock"]

    def feed(self, limit=1000):
        self._c("feed")
        return {"events": self.f["events"]}

    def board(self, venue="rastro"):
        self._c("board")
        return {"offers": [{**{k: v for k, v in o.items() if k != "team"}, "maker": "m0pseudo"} for o in self.f["board"]]}

    def leaderboard(self):
        self._c("leaderboard")
        return self.f["leaderboard"]

    def catalog(self):
        self._c("catalog")
        return self.f["catalog"]

    def me(self):
        self._c("me")
        return self.f["me"]

    def value(self, card):
        self._c("value", card)
        return {"card": card, "your_value": 11.0}

    def my_offers(self):
        self._c("my_offers")
        return {"offers": self.open_offers}

    def venues(self):
        self._c("venues")
        return {"venues": self._venues}

    def list_offer(self, give, want, to, expires_in_ticks, venue="rastro"):
        self._c("list_offer", give, want, to, expires_in_ticks, venue)
        if self.fail_post:
            raise BazaarError(self.fail_post, "refused", 429)
        return {"id": 9001, "maker": "t05", "to": to, "give": give, "want": want}

    def cancel(self, offer_id):
        self._c("cancel", offer_id)
        return {}

    def names(self):
        return [c[0] for c in self.calls]


WRITES = {"list_offer", "cancel", "my_offers"}


def data_dir(tmp_path, f, board_age=5.0):
    d = tmp_path / "data"
    d.mkdir(exist_ok=True)
    (d / "feed.jsonl").write_text("".join(json.dumps(e) + "\n" for e in f["events"]))
    (d / "board.json").write_text(json.dumps({"t": NOW - board_age, "me": "t05", "offers": f["board"]}))
    return d


def run(tmp_path, api, dry_run, **kw):
    return op.run_once(api, dry_run=dry_run, now=kw.pop("now", NOW), state_path=tmp_path / "state.json",
                       out_path=tmp_path / "opportunities.md", data_dir=kw.pop("data", None) or data_dir(tmp_path, api.f),
                       cash_floor=200, log=lambda *a: None, book_path=kw.pop("book_path", tmp_path / "book.json"), **kw)


def test_dry_run_never_calls_a_write_endpoint_or_notifies(tmp_path):
    api, notes = FakeApi(single_gap_fixture()), []
    opps, picked = run(tmp_path, api, True, notifier=lambda *a, **k: notes.append(a))
    assert not WRITES & set(api.names())
    assert notes == []
    assert [(o["team"], o["card"]) for o in picked] == [("t07", "SAL-02")] and picked[0]["status"] == "would alert (dry run)"
    assert not (tmp_path / "state.json").exists()                  # a dry run leaves no cooldowns behind
    md = (tmp_path / "opportunities.md").read_text()
    assert "DRY RUN" in md and "SAL-02" in md
    assert set(api.names()) <= {"clock", "leaderboard", "catalog", "me", "value"}  # collector files were fresh


def test_real_api_refuses_writes_in_dry_run():
    api = op.Api("http://127.0.0.1:9", "not-a-key", dry_run=True, min_gap=0)
    for call in (lambda: api.list_offer({"cash": 1}, {"cards": ["X"]}, "t01", 5), lambda: api.cancel(1), api.my_offers):
        with pytest.raises(RuntimeError, match="dry run"):
            call()


def test_stale_collector_files_are_replaced_by_public_fetches(tmp_path):
    api = FakeApi()
    opps, _ = run(tmp_path, api, True, data=data_dir(tmp_path, api.f, board_age=300))
    assert {"feed", "board"} <= set(api.names())
    t02 = find(opps, "SELL", "t02", "LAT-03")                     # board maker is a pseudonym; the feed names t02
    assert t02 and t02["live"]


def test_live_run_posts_the_offer_then_notifies(tmp_path):
    log, notes = [], []
    api = FakeApi(single_gap_fixture(), log=log)

    def notifier(who, title, body, **k):
        log.append("notify")
        notes.append((who, title, body))

    opps, picked = run(tmp_path, api, False, notifier=notifier)
    post = next(c for c in api.calls if c[0] == "list_offer")
    sal02 = [a["id"] for a in api.f["me"]["assets"] if a["ref"] == "SAL-02"]
    give, want, to, ttl, venue = post[1]
    assert give["assets"][0] in sal02 and want == {"cash": 40} and to == "t07" and ttl == op.OFFER_TTL_TICKS == 20
    assert log.index("list_offer") < log.index("notify")
    assert [n[0] for n in notes] == ["dani", "lucas"]
    body = notes[0][2]
    assert "Accept offer 9001 on El Rastro" in body and "a su nombre" in body and "offer 9001" in body
    state = json.loads((tmp_path / "state.json").read_text())
    assert state["live"][0]["offer"] == 9001 and state["alerts"][0]["team"] == "t07"
    # the next run: same pair and team are in cooldown and the offer is live
    api2 = FakeApi(single_gap_fixture(), open_offers=[{"id": 9001, "maker": "t05", "status": "open"}])
    _, picked2 = run(tmp_path, api2, False, notifier=notifier, now=NOW + 60)
    assert picked2 == [] and "list_offer" not in api2.names()


def test_a_failed_post_sends_no_alert(tmp_path):
    api, notes = FakeApi(single_gap_fixture(), fail_post="rate_limited"), []
    opps, _ = run(tmp_path, api, False, notifier=lambda *a, **k: notes.append(a))
    assert notes == [] and find(opps, "SELL", "t07", "SAL-02")["status"] == "post failed: rate_limited"
    assert json.loads((tmp_path / "state.json").read_text())["alerts"] == []


def test_live_offers_are_cancelled_after_20_ticks(tmp_path):
    state = {"alerts": [], "live": [
        {"ts": NOW - 5 * 60, "tick": TICK - 21, "side": "SELL", "team": "t16", "card": "MAL-02", "price": 30,
         "offer": 1, "asset": 61, "status": "live"},
        {"ts": NOW - 21 * 60, "tick": TICK - 5, "side": "SELL", "team": "t01", "card": "LAV-02", "price": 40, "offer": 2,
         "asset": 300, "status": "live"},
        {"ts": NOW - 10 * 60, "tick": 152, "side": "BUY", "team": "t09", "card": "RET-10", "price": 70, "offer": 3,
         "status": "live"}]}
    (tmp_path / "state.json").write_text(json.dumps(state))
    api = FakeApi(open_offers=[{"id": 1, "maker": "t05", "status": "open"}, {"id": 2, "maker": "t05", "status": "open"}])
    run(tmp_path, api, False, notifier=lambda *a, **k: None)
    assert [c[1] for c in api.calls if c[0] == "cancel"] == [(1,)]
    live = {x["offer"]: x["status"] for x in json.loads((tmp_path / "state.json").read_text())["live"]}
    assert live[1].startswith("cancelled") and live[2] == "live" and live[3].startswith("closed")


def test_message_is_bilingual_and_tells_their_agent_what_to_say():
    o = find(engine()[0], "SELL", "t07", "SAL-02")
    title, body = op.message(o, 1234)
    assert title == "SELL SAL-02 to Team 7 at 40 P (+37.8)"
    assert "ES: ¡Hola, Team 7! Les dejamos la SAL-02" in body and "EN: Hi Team 7! SAL-02" in body and "offer 1234" in body
    dm = body.split("ES: ")[1]                                         # the texts sent to them: no why (17:20)
    assert not any(w in dm for w in ("missing", "falta", "page", "página", "bonus", "collect", "worth"))
    assert 'Their agent: "Accept offer 1234 on El Rastro"' in body
    b = {**o, "side": "BUY", "collects": False, "completes": True, "max_price": 146, "our_value": 149.9, "price": 70,
         "gain": 50, "card": "RET-10", "set_name": "El Retiro"}
    _, body = op.message(b, 77)
    assert "Les compramos la RET-10 a 70 P: oferta 77" in body and "COMPLETES our El Retiro page" in body   # Why: ours
    assert "juntan" not in body and "collect" not in body.split("ES: ")[1]
    assert "Accept offer 77 on El Rastro" in body


def test_hard_limits_recheck_before_posting():
    sell = {"side": "SELL", "price": 7, "our_value": 3.2}
    assert op.within_hard_limits(sell, 0, 200)                           # the floor doesn't apply to sales
    assert not op.within_hard_limits({**sell, "price": 6}, 0, 200)       # 6 < 3.2 + 3
    buy = {"side": "BUY", "price": 70, "our_value": 77}
    assert op.within_hard_limits(buy, 270, 200)
    assert not op.within_hard_limits(buy, 269, 200)                      # 269 − 70 < 200
    assert not op.within_hard_limits({**buy, "price": 75}, 1000, 200)    # above value − 3
    assert not op.within_hard_limits({**buy, "price": None}, 1000, 200)


def test_blocked_by_hard_limits_posts_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(op, "within_hard_limits", lambda o, cash, floor: False)
    api, notes = FakeApi(single_gap_fixture()), []
    opps, _ = run(tmp_path, api, False, notifier=lambda *a, **k: notes.append(a))
    assert "list_offer" not in api.names() and notes == []
    assert find(opps, "SELL", "t07", "SAL-02")["status"] == "blocked by hard limits"


def test_no_offer_id_no_alert(tmp_path, monkeypatch):
    api, notes = FakeApi(single_gap_fixture()), []
    monkeypatch.setattr(api, "list_offer", lambda *a: {"ok": True})
    opps, _ = run(tmp_path, api, False, notifier=lambda *a, **k: notes.append(a))
    assert notes == [] and find(opps, "SELL", "t07", "SAL-02")["status"].startswith("posted without an offer id")


def test_a_mid_table_team_lacking_4_cards_of_a_set_gets_an_addressed_offer():
    # Team 8, 2.38 below us (not 10), bid for LAT-03, -06, -09 and -10: our LAT-03 closes no page of theirs.
    opps, _ = engine()
    o = find(opps, "SELL", "t08", "LAT-03")
    assert o["other_lacks"] == ["LAT-06", "LAT-09", "LAT-10"] and not o["closing"] and o["reasons"] == []
    picked = op.choose_alerts(opps, {"alerts": [], "live": []}, NOW)
    assert ("t08", "LAT-03") in [(x["team"], x["card"]) for x in picked]


def test_a_mid_table_team_lacking_2_cards_of_a_set_does_not():
    f = fx()
    f["events"] = [e for e in f["events"] if e["id"] not in (8065, 8066)]   # no LAT-09/10 bids: LAT-03 + LAT-06 left
    opps, _ = engine(f)
    o = find(opps, "SELL", "t08", "LAT-03")
    assert o["closing"] and any("only 2.38 below us" in r for r in o["reasons"])
    picked = op.choose_alerts(opps, {"alerts": [], "live": []}, NOW)
    assert ("t08", "LAT-03") not in [(x["team"], x["card"]) for x in picked]


def test_one_live_bid_per_card_whoever_holds_it(tmp_path):
    """Two holders of our missing RET-10: one bid only; a second copy would be worth ~25%."""
    f = ret_page_fixture()
    f["events"].append(pull_event("t16", "RET-10", 158, 99200))
    opps, _ = engine(f, values={"RET-10": 149.9}, cash_floor=0)
    picked = op.choose_alerts(opps, {"alerts": [], "live": []}, NOW)
    assert [o["card"] for o in picked if o["side"] == "BUY"] == ["RET-10"]
    other = [o for o in opps if o["side"] == "BUY" and o not in picked]
    assert other and other[0]["status"] == "our bid for this card is already out to another holder"
    live = [{"side": "BUY", "team": "t09", "card": "RET-10", "status": "live"}]
    assert not [o for o in op.choose_alerts(engine(f, values={"RET-10": 149.9}, cash_floor=0)[0],
                                            {"alerts": [], "live": live}, NOW) if o["side"] == "BUY"]


def test_one_copy_is_never_pitched_to_two_teams():
    f = single_gap_fixture()
    f["events"].append(lack_event("t16", "SAL-02", 158, 99300))         # Team 16 lacks SAL-02 too
    opps, _ = engine(f)
    picked = op.choose_alerts(opps, {"alerts": [], "live": []}, NOW)
    assert len([o for o in picked if o["card"] == "SAL-02"]) == 1      # SAL-02 ×2: one spare only


def test_bid_cancelled_once_we_hold_the_card(tmp_path):
    state = {"alerts": [], "live": [{"ts": NOW - 60, "tick": 158, "side": "BUY", "team": "t09", "card": "SAL-08",
                                     "price": 20, "offer": 5, "status": "live"}]}          # we hold SAL-08
    (tmp_path / "state.json").write_text(json.dumps(state))
    api = FakeApi(open_offers=[{"id": 5, "maker": "t05", "status": "open", "give": {"cash": 20}}])
    run(tmp_path, api, False, notifier=lambda *a, **k: None)
    assert ("cancel", (5,)) in api.calls


def test_unreadable_state_blocks_live_posting_but_not_dry_run(tmp_path):
    (tmp_path / "state.json").write_text("{half a fi")
    api, notes = FakeApi(single_gap_fixture()), []
    with pytest.raises(RuntimeError, match="unreadable"):
        run(tmp_path, api, False, notifier=lambda *a, **k: notes.append(a))
    assert "list_offer" not in api.names() and notes == []
    run(tmp_path, FakeApi(single_gap_fixture()), True)                   # dry run still computes


def test_state_is_saved_before_the_notification(tmp_path):
    seen = []
    api = FakeApi(single_gap_fixture())
    run(tmp_path, api, False, notifier=lambda *a, **k: seen.append(json.loads((tmp_path / "state.json").read_text())))
    assert seen and seen[0]["live"][0]["offer"] == 9001


def test_pacing_and_keyless_public_client(monkeypatch):
    api = op.Api("http://127.0.0.1:9", "k", dry_run=True, min_gap=1.0)
    assert "X-Team-Key" not in api.pub._headers and api.pub.retries == 0 and api.team.retries == 0
    t = [100.0]
    slept = []
    monkeypatch.setattr(op.time, "time", lambda: t[0])
    monkeypatch.setattr(op.time, "sleep", lambda s: slept.append(s))
    api._paced(lambda: None)
    t[0] += 0.3
    api._paced(lambda: None)
    assert slept == [pytest.approx(0.7)]


# ------------------------------------------------------------------------------------------------ wall-clock freshness

def test_wall_clock_keeps_fridays_ticks_old_after_the_overnight_pause():
    fri = NOW - 10 * 3600                                     # Friday 22:56, ten real hours ago
    wc = op.WallClock([(150, fri - 300), (155, fri), (155, fri + 30)], now=NOW, now_tick=159, tick_seconds=30)
    assert wc.at(159) == pytest.approx(fri + 4 * 30)          # forward from the last sighting before it
    assert wc.age_s(159) > op.WALL_STALE_S and wc.age_s(140) > op.WALL_STALE_S
    sat = op.WallClock([(155, fri), (160, NOW - 60)], now=NOW, now_tick=162, tick_seconds=30)
    assert sat.age_s(161) == pytest.approx(30) and sat.age_s(159) > op.WALL_STALE_S
    assert op.WallClock([], now=NOW, now_tick=159, tick_seconds=60).age_s(150) == pytest.approx(540)  # no history


def samples_dir(tmp_path, f, rows):
    d = data_dir(tmp_path, f)
    (d / "me.jsonl").write_text("".join(json.dumps({"t": t, "tick": k, "cash": 252}) + "\n" for k, t in rows))
    (d / "leaderboard.jsonl").write_text("{half a line\n")    # unreadable lines are skipped
    return d


def test_signals_seen_hours_ago_in_real_time_are_not_alerted(tmp_path):
    f = single_gap_fixture()
    opps, picked = run(tmp_path, FakeApi(f), True, data=samples_dir(tmp_path, f, [(150, NOW - 10 * 3600)]))
    assert picked == []
    o = find(opps, "SELL", "t07", "SAL-02")
    assert not o["confident"] and o["wall_stale"] and o["status"].startswith("listed only: signal")
    assert "real min old" in o["status"]
    assert all(o["confident"] for o in opps if o["live"])      # a standing board offer is current
    assert " / 6" in (tmp_path / "opportunities.md").read_text()   # real minutes shown next to game minutes


def test_signals_seen_minutes_ago_still_alert(tmp_path):
    f = single_gap_fixture()
    _, picked = run(tmp_path, FakeApi(f), True, data=samples_dir(tmp_path, f, [(155, NOW - 4 * 60)]))
    assert [(o["team"], o["card"]) for o in picked] == [("t07", "SAL-02")]


# ------------------------------------------------------------------------------------------------ crash after a post

def test_a_crash_after_posting_never_reposts(tmp_path):
    api = FakeApi(single_gap_fixture())

    def boom(*a, **k):
        raise RuntimeError("notifier down")
    with pytest.raises(RuntimeError):
        run(tmp_path, api, False, notifier=boom)
    state = json.loads((tmp_path / "state.json").read_text())
    assert state["live"][0]["offer"] == 9001 and state["alerts"][0]["team"] == "t07"
    api2 = FakeApi(single_gap_fixture(), open_offers=[{"id": 9001, "maker": "t05", "status": "open"}])
    _, picked = run(tmp_path, api2, False, notifier=lambda *a, **k: None, now=NOW + 60)
    assert picked == [] and "list_offer" not in api2.names()


# ------------------------------------------------------------------------------------------------ cash floor, every bid

class ValueApi(FakeApi):
    def __init__(self, values, **kw):
        super().__init__(**kw)
        self.values = values

    def value(self, card):
        self._c("value", card)
        return {"card": card, "your_value": self.values.get(card, 11.0)}


def ret_buy_run(tmp_path, open_offers, book=None):
    tmp_path.mkdir(parents=True, exist_ok=True)
    f = ret_page_fixture()
    api = ValueApi({"RET-10": 149.9}, f=f, open_offers=open_offers)
    if book is not None:
        (tmp_path / "book.json").write_text(json.dumps(book))
    opps, _ = op.run_once(api, dry_run=False, now=NOW, state_path=tmp_path / "state.json",
                          out_path=tmp_path / "opportunities.md", data_dir=data_dir(tmp_path, f), cash_floor=100,
                          notifier=lambda *a, **k: None, log=lambda *a: None, book_path=tmp_path / "book.json")
    return api, find(opps, "BUY", "t09", "RET-10")


def test_a_card_the_book_bids_for_gets_no_second_bid_from_opps(tmp_path):
    # Sunday's CHA bids live in run/book.json: an addressed opps bid next to the book's public one could fill too.
    api, o = ret_buy_run(tmp_path, [], book={"offers": [{"card": "RET-10", "side": "buy", "price": 70, "floor": 90}]})
    assert "book bids for it" in o["status"]
    assert not any(c[0] == "list_offer" and c[1][1] == {"cards": ["RET-10"]} for c in api.calls)
    api, o = ret_buy_run(tmp_path / "ask", [], book={"offers": [{"card": "RET-10", "side": "sell", "price": 99,
                                                                  "floor": 90}]})
    assert any(c[0] == "list_offer" and c[1][1] == {"cards": ["RET-10"]} for c in api.calls)   # an ask: no clash


def test_cash_floor_counts_bids_posted_by_other_processes(tmp_path):
    api, o = ret_buy_run(tmp_path / "a", [])
    assert o["reasons"] == [] and any(c[0] == "list_offer" and c[1][1] == {"cards": ["RET-10"]} for c in api.calls)
    other = {"id": 4242, "maker": "t05", "status": "open", "give": {"cash": 100}, "want": {"cards": ["LAV-09"]}}
    for status in ("open", "queued"):                         # 252 − 100 locked − 70 < 100
        api, o = ret_buy_run(tmp_path / status, [{**other, "status": status}])
        assert any("cash floor 100 (cash 152)" in r for r in o["reasons"])
        assert not any(c[0] == "list_offer" and c[1][1] == {"cards": ["RET-10"]} for c in api.calls)   # the bid


def test_offers_live_20_ticks_whatever_the_tick_length():
    # Page-critical bids can't sit 20 wall minutes: that was 41 ticks at Saturday's 30 s and 81 at Sunday's 15 s.
    api = FakeApi(single_gap_fixture())
    api.open_offers = [{"id": 9001, "maker": "t05", "status": "open", "give": {"cash": 30}}]
    state = {"live": [{"offer": 9001, "status": "live", "ts": NOW, "tick": 100, "side": "BUY", "card": "SAL-02",
                       "team": "t07"}]}
    op.reconcile(api, state, [], "t05", NOW, now_tick=120)                 # 20 ticks old: still live
    assert "cancel" not in api.names() and state["live"][0]["status"] == "live"
    op.reconcile(api, state, [], "t05", NOW, now_tick=121)                 # same wall time, 21 ticks: cancelled
    assert "cancel" in api.names() and state["live"][0]["status"] == "cancelled: unfilled 20 ticks"



# ------------------------------------------------------------------ venue: DEFAULT_VENUE, page-closers on El Rastro

V07 = {"venue": "v07", "owner": "t10", "status": "open", "name": "Mercado del 10"}


def test_venue_rules():
    vs, top = {"v07": V07}, {"t13", "t12", "t18", "t02"}
    sale = {"side": "SELL", "other_lacks": ["SAL-03"], "completes": False}
    assert op.venue_for(sale, vs, top) == ("v07", "Mercado del 10")              # an ordinary sale: Team 10's venue
    assert op.venue_for({**sale, "other_lacks": []}, vs, top)[0] == "rastro"     # closes their page (or unknown)
    assert op.venue_for({"side": "BUY", "completes": True}, vs, top)[0] == "rastro"   # closes ours
    assert op.venue_for({"side": "BUY", "completes": False}, vs, top)[0] == "v07"
    assert op.venue_for(sale, {"v07": {**V07, "owner": "t13"}}, top)[0] == "rastro"  # a top-4 team's venue: never
    assert op.venue_for(sale, {"v07": {**V07, "status": "closed"}}, top)[0] == "rastro"
    assert op.venue_for(sale, {}, top)[0] == "rastro"                            # can't see it: El Rastro


def test_a_page_closing_sale_is_posted_on_el_rastro_even_with_v07_open(tmp_path):
    api = FakeApi(single_gap_fixture(), venues=[V07])                           # Team 7 lacks only SAL-02
    run(tmp_path, api, False, notifier=lambda *a, **k: None)
    post = next(c for c in api.calls if c[0] == "list_offer")
    assert post[1][4] == "rastro"
    assert json.loads((tmp_path / "state.json").read_text())["live"][0]["venue"] == "rastro"


def test_the_alert_names_the_venue_the_offer_is_on():
    o = find(engine()[0], "SELL", "t07", "SAL-02")
    title, body = op.message({**o, "venue_name": "Mercado del 10"}, 1234)
    assert 'Their agent: "Accept offer 1234 on Mercado del 10"' in body and "El Rastro" not in body



def test_expires_in_ticks_is_sent_in_fridays_60_s_units():
    # Sat [V]: the server halved what we sent (60 -> 30, 120 -> 60, 200 -> 100 real ticks at 30 s).
    assert op.expires_param(20, 60) == 20
    assert op.expires_param(20, 30) == 40                                  # 20 real ticks on Saturday
    assert op.expires_param(20, 15) == 80                                  # Sunday, if the rule holds: verify



def test_sells_go_only_to_teams_that_collect_the_set():
    # Chief 11:50 [V]: a sale to a non-collector scored -10.2 on our venue. teams.md "dumps" vetoes a sale.
    import collectors as col
    c = col.Collectors({"t07": {"collects": set(), "dumps": {"SAL"}}, "t08": {"collects": {"LAT"}, "dumps": set()}}, {})
    opps, _ = engine(collectors=c)
    assert any("dumps SAL" in r for r in find(opps, "SELL", "t07", "SAL-02")["reasons"])
    assert find(opps, "SELL", "t08", "LAT-03")["reasons"] == []          # collects LAT (teams.md and its bids)
