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
    sent = []
    w = bg.Watcher(api, notifier=lambda *a, **k: sent.append((a, k)), state_path=tmp_path / "s.json", log=lambda *a: None,
                   **kw)
    return w, sent


def test_a_legendary_bargain_on_el_rastro_pages_lucas_once(tmp_path):
    api = Api({"rastro": [ask(1, "RET-12", 300), ask(2, "LAT-02", 11, "common")]})
    w, sent = watcher(tmp_path, api, cash_floor=100)
    found = w.scan()
    assert [b["refs"] for b in found] == [["RET-12"]]
    b = found[0]
    assert b["fee"] == 16 and b["gain"] == 179 and b["score"] == 50 and b["need"] == 316   # 5% of 300 + 1
    assert not b["fits"]                                               # 400 - 316 = 84 < floor 100
    (channel, title, body), k = sent[0]
    assert channel == "lucas" and "RET-12 at 300 P: +50" in title and "BELOW the cash floor 100" in body
    assert "accept offer 1 on El Rastro" in body and k["priority"] == 5
    w.scan()
    assert len(sent) == 1                                              # once per offer


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
    bodies = {a[1]: a[2] for a, _ in sent}
    assert any("auto stall" in b and "post a bid of 150 P" in b for b in bodies.values())
    assert any("top-4 team t12" in b for b in bodies.values())


def test_dry_run_sends_and_remembers_nothing(tmp_path):
    api = Api({"rastro": [ask(1, "RET-12", 300)]})
    w, sent = watcher(tmp_path, api)
    assert w.scan(dry=True) and sent == [] and not (tmp_path / "s.json").exists()
