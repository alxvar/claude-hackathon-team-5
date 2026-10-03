"""Offline tests for tools/bargains.py: a fake game, no network, no notifications sent."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "bazaar-kit"))
import bargains as bg  # noqa: E402

VALUES = {"RET-12": 495.0, "RET-11": 198.0, "LAT-02": 2.0, "SAL-09": 63.0}
TEAMS = [{"team": t, "score": s} for t, s in (("t18", 30), ("t12", 28), ("t02", 27), ("t05", 24), ("t10", 20))]


def ask(oid, ref, price, rarity="legendary", to=None, maker="m1"):
    return {"id": oid, "maker": maker, "to": to, "status": "open",
            "give": {"cash": 0, "assets": [{"id": oid * 10, "kind": "card", "ref": ref, "rarity": rarity}], "types": []},
            "want": {"cash": price, "assets": [], "types": []}}


class Api:
    def __init__(self, boards, venues=(), mine=(), cash=400):
        self.boards, self._venues, self._mine, self.cash, self.value_calls = boards, list(venues), list(mine), cash, []

    def me(self):
        return {"id": "t05", "cash": self.cash}

    def my_offers(self):
        return {"offers": [{"id": i, "maker": "t05"} for i in self._mine]}

    def venues(self):
        return {"venues": self._venues}

    def leaderboard(self):
        return {"teams": TEAMS}

    def board(self, venue):
        return {"offers": self.boards.get(venue, [])}

    def value(self, ref):
        self.value_calls.append(ref)
        return {"your_value": VALUES[ref]}


def watcher(tmp_path, api, **kw):
    sent, logs = [], []
    w = bg.Watcher(api, notifier=lambda *a, **k: sent.append((a, k)), state_path=tmp_path / "s.json", log=logs.append,
                   **kw)
    w.logs = logs                                    # bargain alerts are logged only since 17:40 (no push to Lucas)
    return w, sent


def test_a_legendary_bargain_on_el_rastro_pages_lucas_once(tmp_path):
    api = Api({"rastro": [ask(1, "RET-12", 300), ask(2, "LAT-02", 11, "common")]})
    w, sent = watcher(tmp_path, api, cash_floor=100)
    found = w.scan()
    assert [b["refs"] for b in found] == [["RET-12"]]
    b = found[0]
    assert b["fee"] == 16 and b["gain"] == 179 and b["score"] == 50 and b["need"] == 316   # 5% of 300 + 1
    assert not b["fits"]                                               # 400 - 316 = 84 < floor 100
    assert sent == []                                                  # Chief 17:40: no push to Lucas
    line = next(x for x in w.logs if "RET-12 at 300 P: +50" in x)
    assert "BELOW the cash floor 100" in line
    assert "accept offer 1 on El Rastro" in line
    w.scan()
    assert sum("RET-12 at 300 P" in x for x in w.logs) == 1            # once per offer


def test_small_gains_our_own_and_others_addressed_offers_are_ignored(tmp_path):
    api = Api({"rastro": [ask(1, "SAL-09", 60, "rare"),                 # 63 - 60 - 4: +(-1)
                          ask(2, "RET-11", 150, "epic", to="t13"),      # addressed to Team 13: not ours to take
                          ask(3, "RET-11", 150, "epic"),                # ours (in /api/me/offers)
                          ask(4, "RET-11", 160, "epic", to="t05")]},    # addressed to us: counts
              mine=[3])
    w, sent = watcher(tmp_path, api)
    found = w.scan()
    assert [b["offer"] for b in found] == [4] and found[0]["to_us"] and found[0]["gain"] == 198 - 160 - 9


def test_venue_fees_auto_stalls_and_top_4_venues(tmp_path):
    venues = [{"venue": "v07", "owner": "t10", "status": "open", "name": "Mercado 10", "fee_bps": 0, "fee_per_card": 0,
               "rules": {"mechanism": "board"}},
              {"venue": "v02", "owner": "t12", "status": "open", "name": "El Duende", "fee_bps": 200, "fee_per_card": 0,
               "pending_fee": {"fee_bps": 300, "fee_per_card": 1}, "rules": {"mechanism": "board"}},
              {"venue": "v09", "owner": "t09", "status": "open", "name": "Puesto 9", "fee_bps": 0, "fee_per_card": 0,
               "rules": {"mechanism": "auto"}}]
    api = Api({"v07": [ask(1, "RET-11", 150, "epic")], "v02": [ask(2, "RET-11", 150, "epic")],
               "v09": [ask(3, "RET-11", 150, "epic")]}, venues=venues)
    w, sent = watcher(tmp_path, api)
    by = {b["venue"]: b for b in w.scan()}
    assert by["v07"]["fee"] == 0 and by["v02"]["fee"] == 6                # pending 3% + 1 beats current 2%
    assert by["v02"]["top4_venue"] and not by["v07"]["top4_venue"]
    assert any("auto stall" in b and "post a bid of 150 P" in b for b in w.logs)
    assert any("top-4 team t12" in b for b in w.logs)


def test_dry_run_sends_and_remembers_nothing(tmp_path):
    api = Api({"rastro": [ask(1, "RET-12", 300)]})
    w, sent = watcher(tmp_path, api)
    assert w.scan(dry=True) and sent == [] and not (tmp_path / "s.json").exists()


# ------------------------------------------------------------------ arbitrage (Chief 15:50)

ARB_TEAMS = TEAMS + [{"team": "t16", "score": 8}, {"team": "t17", "score": 20}, {"team": "t20", "score": 3},
                     {"team": "t03", "score": 4}]   # t10 is in the top 5 here: sellers are t20 / t03


def bid(oid, ref, price, to=None):
    return {"id": oid, "to": to, "status": "open", "give": {"cash": price, "assets": [], "types": []},
            "want": {"cash": 0, "assets": [], "types": [f"card:{ref}"]}}


def legs(ask_venue="v07", bid_venue="rastro", p1=9, p2=20):
    asks = {"LAT-02": [{"offer": 1, "venue": ask_venue, "price": p1, "fee": 0}]}
    bids = {"LAT-02": [{"offer": 2, "venue": bid_venue, "price": p2, "fee": bg.fee(p2, 1)}]}
    return asks, bids


def test_an_ask_below_a_live_bid_on_another_venue_is_an_arbitrage():
    asks, bids = legs()
    x = bg.arbitrage(asks, bids, makers={1: "t20", 2: "t16"}, held={}, teams=ARB_TEAMS, me="t05")
    assert len(x) == 1 and x[0]["net"] == 20 - 9 - 0 - 2 and x[0]["bidder"] == "t16" and x[0]["need"] == 9


def test_the_sell_leg_follows_the_feeding_rule_and_the_bars():
    asks, bids = legs()
    assert bg.arbitrage(asks, bids, makers={1: "t20", 2: "t12"}, held={}, teams=ARB_TEAMS, me="t05") == []   # top 5
    near = {("t17", f"LAT-{i:02d}"): {i} for i in (1, 3, 4, 5, 6, 7, 8, 9)}             # LAT-02 may close its page
    assert bg.arbitrage(asks, bids, makers={1: "t20", 2: "t17"}, held=near, teams=ARB_TEAMS, me="t05") == []
    assert bg.arbitrage(asks, bids, makers={1: "t20", 2: "t16"}, held={**near, **{("t16", k[1]): v for k, v in
                        near.items()}}, teams=ARB_TEAMS, me="t05")                        # t16 is 16 below us: fine
    asks, bids = legs(p1=14)
    assert bg.arbitrage(asks, bids, makers={1: "t20", 2: "t16"}, held={}, teams=ARB_TEAMS, me="t05") == []   # +4
    asks, bids = legs(ask_venue="rastro")
    assert bg.arbitrage(asks, bids, makers={1: "t20", 2: "t16"}, held={}, teams=ARB_TEAMS, me="t05") == []   # same venue


def test_a_scan_alerts_the_operator_once_per_pair(tmp_path):
    api = Api({"v07": [ask(1, "LAT-02", 9, "common")], "rastro": [bid(2, "LAT-02", 20)]},
              venues=[{"venue": "v07", "status": "open", "fee_bps": 0, "fee_per_card": 0, "owner": "t10"}])
    api.leaderboard = lambda: {"teams": ARB_TEAMS}
    w, sent = watcher(tmp_path, api)
    w.arb_out = tmp_path / "arbitrage.md"
    w.feed_path = tmp_path / "feed.jsonl"
    w.feed_path.write_text('{"type": "offer.listed", "payload": {"offer": {"id": 1, "maker": "t20"}}}\n'
                           '{"type": "offer.listed", "payload": {"offer": {"id": 2, "maker": "t16"}}}\n')
    w.scan()
    w.scan()
    ops = [a for a, k in sent if a[0] == "operator"]
    assert len(ops) == 1 and ops[0][1].startswith("ARB LAT-02: buy 9 (v07) → sell 20 (rastro): +9")
    assert "accept offer 1 on v07" in ops[0][2] and "accept offer 2 on rastro" in ops[0][2]
    assert "ARB LAT-02" in w.arb_out.read_text()


def test_our_own_venue_is_never_scanned(tmp_path):
    # Review 16:15 (blocker): RULES forbid trading on our own venue; a v10 bid would strand leg 1.
    api = Api({"v10": [bid(2, "LAT-02", 20)], "v07": [ask(1, "LAT-02", 9, "common")], "rastro": [ask(3, "RET-12", 300)]},
              venues=[{"venue": "v10", "status": "open", "owner": "t05", "fee_bps": 0, "fee_per_card": 0},
                      {"venue": "v07", "status": "open", "owner": "t10", "fee_bps": 0, "fee_per_card": 0}])
    api.leaderboard = lambda: {"teams": ARB_TEAMS}
    w, sent = watcher(tmp_path, api)
    w.feed_path = tmp_path / "none.jsonl"
    w.scan()
    assert not any(a[0] == "operator" for a, k in sent)
    api.boards["v10"] = [ask(4, "RET-12", 100)]
    assert all(b["venue"] != "v10" for b in w.scan())


def test_each_leg_is_scored_at_our_value_capped_at_50():
    asks = {"RET-11": [{"offer": 1, "venue": "v07", "price": 100, "fee": 0}]}
    bids = {"RET-11": [{"offer": 2, "venue": "rastro", "price": 160, "fee": 9}]}
    teams = ARB_TEAMS
    # V 198: buy +98 -> 50, sell -47: 3 < 5, though the spread is +51
    assert bg.arbitrage(asks, bids, makers={1: "t20", 2: "t16"}, held={}, teams=teams, me="t05",
                        value=lambda c: 198.0) == []
    x = bg.arbitrage(asks, bids, makers={1: "t20", 2: "t16"}, held={}, teams=teams, me="t05", value=lambda c: 120.0)
    assert x[0]["buy"] == 20 and x[0]["sell"] == 31 and x[0]["score"] == 51 and x[0]["if_leg2_fails"] == 20
    assert bg.arbitrage(asks, bids, makers={1: "t20", 2: "t16"}, held={}, teams=teams, me="t05", value=lambda c: 120.0,
                        closes_ours=lambda c, v: True) == []                     # it would close our page


def test_the_best_ask_per_bid_and_never_an_unknown_seller():
    asks = {"LAT-02": [{"offer": 1, "venue": "v07", "price": 9, "fee": 0}, {"offer": 3, "venue": "v20", "price": 7,
                                                                             "fee": 0}]}
    _, bids = legs()
    x = bg.arbitrage(asks, bids, makers={1: "t20", 3: "t03", 2: "t16"}, held={}, teams=ARB_TEAMS, me="t05")
    assert [a["ask"]["offer"] for a in x] == [3]
    assert bg.arbitrage(asks, bids, makers={2: "t16"}, held={}, teams=ARB_TEAMS, me="t05") == []


# ------------------------------------------------------------------ underpriced asks (Chief 18:10)

def test_underpriced_asks_ranked_rival_venues_out_and_strong_ones_acted(tmp_path, monkeypatch):
    import alerts
    acts = []
    monkeypatch.setattr(alerts, "act", lambda *a, **k: acts.append((a, k)) or True)
    venues = [{"venue": "v15", "owner": "t16", "status": "open", "fee_bps": 0, "fee_per_card": 0},
              {"venue": "v12", "owner": "t12", "status": "open", "fee_bps": 0, "fee_per_card": 0}]   # t12: a rival
    api = Api({"v15": [ask(1, "SAL-09", 30, "rare"), ask(2, "LAT-02", 1, "common")],
               "v12": [ask(3, "RET-11", 60, "epic")]}, venues=venues, cash=200)
    api.leaderboard = lambda: {"teams": ARB_TEAMS}
    w, sent = watcher(tmp_path, api, min_gain=99)
    w.underpriced_path, w.feed_path = tmp_path / "u.md", tmp_path / "feed.jsonl"
    w.feed_path.write_text('{"type": "offer.listed", "payload": {"offer": {"id": 1, "maker": "t20"}}}\n'
                           '{"type": "offer.listed", "payload": {"offer": {"id": 2, "maker": "t20"}}}\n')
    w.scan()
    md = (tmp_path / "u.md").read_text()
    assert "SAL-09" in md and "LAT-02" in md and "RET-11" not in md       # v12 is a rival's venue
    assert md.index("SAL-09") < md.index("LAT-02")                        # ranked by gain (+33 before +0)
    assert [a[1] for a, k in acts] == [1]                                 # SAL-09: +33 >= 15, 30 <= 200 - 100
    assert acts[0][0][0].startswith("BUY SAL-09 at 30 P on v15") and acts[0][1]["source"] == "underpriced"
