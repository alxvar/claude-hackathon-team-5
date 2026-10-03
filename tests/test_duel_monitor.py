"""Offline tests for tools/duel_monitor.py on Friday's recorded duels (docs/duels/). No network, no real notifications."""
import copy
import json
from pathlib import Path

from tools import duel_monitor as dm

DUELS = Path(__file__).resolve().parents[1] / "docs" / "duels"


def record(n):
    return json.loads((DUELS / f"duel-{n}.json").read_text())


def kinds(flags, kind):
    return [f for f in flags if f.kind == kind]


# ------------------------------------------------------------------ replay flags

def test_duel_181_in_limit_offer_not_accepted_near_deadline():
    flags = kinds(dm.replay_record(record(181)), "in_limit_not_accepted")
    assert flags, "duel 181: Rival Verde's 73 stood inside our limit 85 and we never accepted"
    assert flags[0].tick in (142, 143)
    assert flags[0].severity == dm.CRITICAL
    assert "73" in flags[0].text and "85" in flags[0].text


def test_duels_103_104_hold_deadlock():
    for n in (103, 104):
        flags = kinds(dm.replay_record(record(n)), "hold_deadlock")
        assert flags, f"duel {n} sat still for 10 ticks"
        assert flags[0].severity == dm.MEDIUM
        assert flags[0].tick == 149          # last move at 146, 3 still ticks, 8 left


def test_friday_replay_raises_no_spurious_critical_or_high():
    flags = [f for r in dm.load_records(DUELS) for f in dm.first_per_kind(dm.replay_record(r))]
    assert not kinds(flags, "deal_outside_limit")
    assert not [f for f in flags if f.severity == dm.HIGH]
    # 181 lost it; 114 closed at 58 on the deadline tick with Luna's in-limit 62 standing (the same gamble, it paid)
    assert {f.duel for f in kinds(flags, "in_limit_not_accepted")} == {181, 114}
    assert {f.duel for f in kinds(flags, "hold_deadlock")} == {103, 104}


# ------------------------------------------------------------------ live flags on synthetic payloads

def live_181_at(tick):
    raw = copy.deepcopy(record(181)["payloads"][-1]["raw"])
    return raw, tick


def test_in_limit_flag_waits_for_the_last_two_ticks_and_respects_an_accept():
    raw, _ = live_181_at(141)
    assert not kinds(dm.live_flags(raw, 141), "in_limit_not_accepted")   # 4 ticks left: not yet
    assert kinds(dm.live_flags(raw, 143), "in_limit_not_accepted")
    assert not kinds(dm.live_flags(raw, 143, accepted=True), "in_limit_not_accepted")


def test_in_limit_flag_ignores_offers_past_or_at_our_limit():
    raw, _ = live_181_at(143)
    raw["rival_offer"]["price"] = 85                                      # at our limit: worth 0
    assert not kinds(dm.live_flags(raw, 143), "in_limit_not_accepted")
    raw["rival_offer"]["price"] = 90
    assert not kinds(dm.live_flags(raw, 143), "in_limit_not_accepted")


def test_we_are_silent_after_a_rival_offer():
    raw = copy.deepcopy(record(181)["payloads"][6]["raw"])               # rival offered 81 at 140, not answered yet
    assert raw["messages"][-1]["from"] != "you"
    raw["deadline_tick"] = 150
    assert not kinds(dm.live_flags(raw, 143), "we_are_silent")
    f = kinds(dm.live_flags(raw, 144), "we_are_silent")
    assert f and f[0].severity == dm.HIGH


def test_never_opened():
    raw = copy.deepcopy(record(181)["payloads"][0]["raw"])               # no messages yet
    assert not kinds(dm.live_flags(raw, 134, first_seen=132), "never_opened")
    assert kinds(dm.live_flags(raw, 135, first_seen=132), "never_opened")


def test_missing_days_refusal_from_records():
    raw = copy.deepcopy(record(181)["payloads"][-1]["raw"])
    errs = [{"tick": 140, "code": "missing_days", "message": "a priced message needs days"}]
    f = kinds(dm.live_flags(raw, 141, errors=errs), "missing_days")
    assert f and f[0].severity == dm.HIGH


def test_deal_outside_limit():
    raw = copy.deepcopy(record(114)["done"])                             # buyer, limit 93, deal at 58
    assert not dm.closed_flags(raw)
    raw["price"] = 95
    f = dm.closed_flags(raw)
    assert f and f[0].kind == "deal_outside_limit" and f[0].severity == dm.CRITICAL


# ------------------------------------------------------------------ review

def test_friday_review_counts():
    text, sm = dm.replay_review(DUELS)
    assert (sm["deals"], sm["finished"]) == (11, 24)
    assert "11 deals / 24 finished" in text
    assert (sm["spoke"], sm["spoke_deals"]) == (12, 9)                   # 9/12 closed when the rival spoke
    assert (sm["engaged"], sm["engaged_deals"]) == (14, 11)
    assert [x.duel for x in sm["missed"]] == [181]
    assert round(sm["missed"][0].missed, 1) == 10.6                      # 12 P x 0.94^2
    assert round(sm["decay_share"], 2) == 0.14                           # ~14% of value lost to decay
    assert {x.duel for x in sm["holds"]} == {103, 104}
    assert "Accept earlier" in text and "Break holds" in text


def test_result_model_matches_the_game():
    for n in (114, 121, 163, 175, 199):
        done = record(n)["done"]
        st = dm.analyse({**done, "result": None})                          # recompute it
        assert abs(st.result - done["result"]) < 0.06, n


def test_prepend_review_keeps_newest_first(tmp_path):
    p = tmp_path / "duel-review.md"
    dm.prepend_review("## one\nbody 1\n", p)
    dm.prepend_review("## two\nbody 2\n", p)
    text = p.read_text()
    assert text.startswith("# Duel review")
    assert text.index("## two") < text.index("## one")


# ------------------------------------------------------------------ the monitor: alerts, dedupe, session, tests

class FakeApi:
    """GETs only; no write method exists, so a write attempt would fail the test."""

    def __init__(self, live, done=(), schedule=None, feed=None, teams=18):
        self.live, self.done = list(live), list(done)
        self._schedule, self._feed, self.teams = schedule or {"upcoming": []}, feed or {"events": []}, teams
        self.calls = []

    def clock(self):
        self.calls.append("clock")
        return {"tick": 143, "doors": "open", "paused": False, "tick_seconds": 30, "next_tick_in": 10}

    def schedule(self):
        self.calls.append("schedule")
        return self._schedule

    def feed(self, limit=200):
        self.calls.append("feed")
        return self._feed

    def leaderboard(self):
        self.calls.append("leaderboard")
        return {"teams": [{}] * self.teams}

    def duels(self, done=False):
        self.calls.append("duels_done" if done else "duels")
        return {"duels": self.done if done else self.live}


class Recorder:
    def __init__(self):
        self.sent = []

    def __call__(self, channel, title, message, priority=3, tags=None, click=None):
        self.sent.append((channel, title, priority))
        return True


def monitor(tmp_path, api, notes, **kw):
    return dm.Monitor(api, notify=notes, state_path=tmp_path / "state.json", review_path=tmp_path / "review.md",
                      me="Lucas Wiese", test_watch=False, records=lambda _id: None, **kw)


def test_critical_goes_to_lucas_and_dani_once(tmp_path):
    raw = copy.deepcopy(record(181)["payloads"][-1]["raw"])
    notes = Recorder()
    m = monitor(tmp_path, FakeApi([raw]), notes)
    new = m.cycle({"tick": 143, "doors": "open", "paused": False})
    assert [f.kind for f in new] == ["in_limit_not_accepted"]
    assert sorted(ch for ch, _, _ in notes.sent) == ["dani", "lucas"]
    assert all(p == 5 for _, _, p in notes.sent)
    m2 = monitor(tmp_path, FakeApi([raw]), notes)                       # restart: dedupe survives in the state file
    assert m2.cycle({"tick": 144, "doors": "open", "paused": False}) == []
    assert len(notes.sent) == 2


def test_medium_is_printed_not_pushed(tmp_path, capsys):
    raw = copy.deepcopy(record(103)["payloads"][-1]["raw"])
    notes = Recorder()
    m = monitor(tmp_path, FakeApi([raw]), notes)
    new = m.cycle({"tick": 149, "doors": "open", "paused": False})
    assert [f.kind for f in new] == ["hold_deadlock"]
    assert notes.sent == []
    assert "hold_deadlock" in capsys.readouterr().out


def test_without_notify_it_prints(tmp_path, capsys):
    raw = copy.deepcopy(record(181)["payloads"][-1]["raw"])
    m = monitor(tmp_path, FakeApi([raw]), None)
    m.notify_fn = None
    m.cycle({"tick": 143, "doors": "open", "paused": False})
    out = capsys.readouterr().out
    assert "notify[lucas]" in out and "notify[dani]" in out


def test_closed_doors_read_nothing(tmp_path):
    api = FakeApi([])
    monitor(tmp_path, api, Recorder()).cycle({"tick": 159, "doors": "closed", "paused": True})
    assert api.calls == []


DUELS_I = {"upcoming": [{"at_hours": 6.5, "action": "duels", "note": "Duels I: price only, one round-robin",
                         "params": {"name": "Duels I", "rounds": 1, "duel_ticks": 16, "decay": 0.06,
                                    "max_concurrent": 3}}]}


def test_no_live_duel_in_a_scored_session(tmp_path):
    notes = Recorder()
    m = monitor(tmp_path, FakeApi([], schedule=DUELS_I), notes)
    m.learn_sessions(DUELS_I, None)
    assert m.cycle({"tick": 380, "doors": "open", "paused": False}) == []     # before the session (tick 390)
    assert m.cycle({"tick": 395, "doors": "open", "paused": False}) == []     # first tick without a duel
    new = m.cycle({"tick": 396, "doors": "open", "paused": False})
    assert [f.kind for f in new] == ["no_live_duel"] and new[0].severity == dm.HIGH
    assert sorted(ch for ch, _, _ in notes.sent) == ["dani", "lucas"]


def test_no_live_duel_is_quiet_in_practice(tmp_path):
    feed = {"events": [{"id": 1, "tick": 120, "type": "duels.scheduled",
                        "payload": {"session": 1, "name": "Practice duels", "duels": 306, "rounds": 1,
                                    "duel_ticks": 12, "decay": 0.06}}]}
    m = monitor(tmp_path, FakeApi([], feed=feed), Recorder())
    m.learn_sessions(None, feed)
    assert m.per_team(m.state["sessions"]["Practice duels"]) == 34       # 18 teams: 306 duels, 34 each
    for t in (125, 126, 127):
        assert m.cycle({"tick": t, "doors": "open", "paused": False}) == []


def test_wave_review_written_after_a_batch(tmp_path):
    friday = [r["done"] for r in dm.load_records(DUELS) if r.get("done")]
    first, rest = friday[:20], friday[20:]
    api = FakeApi([], done=first)
    m = monitor(tmp_path, api, Recorder())
    m.cycle({"tick": 150, "doors": "open", "paused": False})            # first run: old duels are not reviewed
    assert not (tmp_path / "review.md").exists()
    api.done = friday
    m.cycle({"tick": 160, "doors": "open", "paused": False})
    text = (tmp_path / "review.md").read_text()
    assert text.startswith("# Duel review") and f"wave of {len(rest)}" in text
    assert "**This wave:**" in text and "**Session so far:** 11 deals / 24 finished" in text


def test_test_watch_runs_once_per_foreign_commit_and_names_failures(tmp_path):
    runs = []

    def fake_tests():
        runs.append(1)
        return False, ["test_deadline_accept"], "1 failed, 16 passed"

    notes = Recorder()
    commit = ["abc1234def", "Aleksandar Varga", "duelist: deadline trigger"]
    m = dm.Monitor(FakeApi([]), notify=notes, state_path=tmp_path / "s.json", review_path=tmp_path / "r.md",
                   me="Lucas Wiese", test_watch=True, records=lambda _id: None, run_tests=fake_tests,
                   foreign_commit=lambda: tuple(commit))
    new = m.cycle({"tick": 1, "doors": "closed", "paused": True})
    assert [f.kind for f in new] == ["duelist_tests_failed"] and "test_deadline_accept" in new[0].text
    assert sorted(ch for ch, _, _ in notes.sent) == ["dani", "lucas"]
    m._tests_at = 0
    assert m.cycle({"tick": 2, "doors": "closed", "paused": True}) == [] and len(runs) == 1   # same commit
    commit[0] = "fff0000aaa"
    m._tests_at = 0
    m.cycle({"tick": 3, "doors": "closed", "paused": True})
    assert len(runs) == 2


def test_parse_failures():
    out = ("..F.\nFAILED tests/test_duelist.py::test_a - AssertionError\n"
           "ERROR tests/test_duelist.py::test_b - ImportError\n1 failed, 1 error")
    assert dm.parse_failures(out) == ["test_a", "test_b"]


def test_latest_foreign_commit_skips_my_own():
    c = dm.latest_foreign_commit("Lucas Wiese")
    assert c is None or c[1] != "Lucas Wiese"
