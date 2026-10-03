"""Offline tests for tools/duel_monitor.py on Friday's recorded duels (a frozen copy in tests/fixtures/duels/). No network, no real notifications."""
import copy
import json
from pathlib import Path

from tools import duel_monitor as dm

DUELS = Path(__file__).resolve().parent / "fixtures" / "duels"   # docs/duels as of Sat 08:03 (Friday + practice); docs/duels keeps growing


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
        assert flags[0].tick == 149          # last move at 146, 3 still ticks, 7 left


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
    assert not kinds(dm.live_flags(raw, 141), "in_limit_not_accepted")   # 3 ticks left: not yet
    assert kinds(dm.live_flags(raw, 143), "in_limit_not_accepted")
    assert not kinds(dm.live_flags(raw, 143, accepted=True), "in_limit_not_accepted")


def test_ticks_left_matches_the_duelist_and_arbiter():
    # The duel closes ON its deadline tick: deadline - 1 is the last tick to move on (1 left), as in
    # agents/duelist/adapter.py and tools/arbiter.py. Duel 181's deadline is 144.
    raw, _ = live_181_at(142)
    assert dm.ticks_left(raw, 143) == 1 and dm.ticks_left(raw, 142) == 2
    assert dm.ticks_left({**raw, "ticks_left": 5}, 142) == 5              # the payload's own count wins
    # The critical alert fires with 2 ticks left (142), one tick before the last chance, not on it.
    assert kinds(dm.live_flags(raw, 142), "in_limit_not_accepted")
    first = kinds(dm.replay_record(record(181)), "in_limit_not_accepted")[0]
    assert first.tick == 142


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


def test_a_rival_repeating_its_price_while_we_hold_is_not_silence_but_a_new_move_is():
    # Sat 278: Rival Oro sent 111 every tick; since the rounds fix our duelist holds by sending nothing.
    msgs = [{"tick": 165, "from": "Rival Oro", "price": 111}, {"tick": 165, "from": "you", "price": 80}]
    msgs += [{"tick": t, "from": "Rival Oro", "price": 111} for t in range(166, 172)]
    raw = {"duel": 9, "status": "live", "role": "buyer", "your_limit": 116, "deadline_tick": 185, "rival": "Rival Oro",
           "rival_offer": {"price": 111}, "messages": msgs}
    assert not kinds(dm.live_flags(raw, 171), "we_are_silent")          # 6 ticks of repeats: alive, holding
    raw["messages"] = msgs + [{"tick": 172, "from": "Rival Oro", "price": 109}]   # a real move
    assert not kinds(dm.live_flags(raw, 175), "we_are_silent")
    f = kinds(dm.live_flags(raw, 176), "we_are_silent")
    assert f and f[0].severity == dm.HIGH and "uv run python -m agents.duelist run" in f[0].text
    assert "Only if Aleks confirms" in f[0].text


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
    clk = lambda t: {"tick": t, "t_hours": 6.5 + (t - 390) / 60, "tick_seconds": 60,   # noqa: E731  (60 s ticks)
                     "doors": "open", "paused": False}
    assert m.cycle(clk(380)) == []     # before the session (tick 390)
    assert m.cycle(clk(395)) == []     # first tick without a duel
    new = m.cycle(clk(396))
    assert [f.kind for f in new] == ["no_live_duel"] and new[0].severity == dm.HIGH
    assert sorted(ch for ch, _, _ in notes.sent) == ["dani", "lucas"]


def test_session_start_follows_the_clock_pace(tmp_path):
    # Sat: 30 s ticks, a tick advances 30 s of game time. At tick 176 / hour 2.7917, Duels I at 5.15 starts at tick
    # 459, not 309 (= 5.15 x 60, Friday's 60 s pace): no "no live duel" page at 310-312.
    sched = {"upcoming": [{**DUELS_I["upcoming"][0], "at_hours": 5.15}]}
    notes = Recorder()
    m = monitor(tmp_path, FakeApi([], schedule=sched), notes)
    m.learn_sessions(sched, None)

    def clk(tick):
        return {"tick": tick, "t_hours": 2.7917 + (tick - 176) * 30 / 3600, "tick_seconds": 30, "doors": "open",
                "paused": False}

    for t in (310, 311, 312):
        assert m.cycle(clk(t)) == []
    assert m.tick_at(5.15) == 459
    assert m.cycle(clk(460)) == [] and m.cycle(clk(461)) == []
    assert [f.kind for f in m.cycle(clk(462))] == ["no_live_duel"]


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

    def fake_tests(sha):
        runs.append(sha)
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


def test_test_watch_does_not_page_the_known_data_failure(tmp_path):
    notes = Recorder()
    failed = ["test_review_predicts_each_deals_result_from_our_reading"]
    m = dm.Monitor(FakeApi([]), notify=notes, state_path=tmp_path / "s.json", review_path=tmp_path / "r.md",
                   me="Lucas Wiese", test_watch=True, records=lambda _id: None,
                   run_tests=lambda _sha: (False, list(failed), "1 failed, 44 passed"),
                   foreign_commit=lambda: ("abc1234def", "Aleksandar Varga", "duelist: x"))
    assert m.cycle({"tick": 1, "doors": "closed", "paused": True}) == [] and notes.sent == []
    failed.append("test_deadline_accept")                                 # a real failure alongside it still pages
    m._tests_at, m.state["tests_sha"] = 0, None
    assert [f.kind for f in m.cycle({"tick": 2, "doors": "closed", "paused": True})] == ["duelist_tests_failed"]


def test_duelist_tests_run_on_a_clean_copy_of_the_commit_not_the_working_tree(tmp_path, monkeypatch):
    # Sat 09:44-09:46: three false "duelist tests failed" pages from a half-done edit and a stuck rebase in the
    # shared tree. A repo whose committed test passes and whose working copy is broken must read as a pass.
    # The toy repo is no uv project (`uv run --project` refuses it: "No `project` table found"), and an old `uv`
    # on PATH may not know `--project` (Aleks's Mac): run it with this interpreter, which has pytest.
    import subprocess
    monkeypatch.setattr(dm.shutil, "which", lambda _name: None)
    repo = tmp_path / "repo"
    (repo / "tests").mkdir(parents=True)
    (repo / "tests" / "test_duelist.py").write_text("def test_ok():\n    assert True\n")
    (repo / "pyproject.toml").write_text("[tool.pytest.ini_options]\npythonpath = [\".\"]\n")
    g = lambda *a: subprocess.run(["git", "-C", str(repo), *a], check=True, capture_output=True)   # noqa: E731
    g("init", "-q"); g("add", "-A"); g("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "ok")
    sha = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    (repo / "tests" / "test_duelist.py").write_text("<<<<<<< Updated upstream\n")      # mid-conflict
    ok, failed, tail = dm.run_duelist_tests(sha, root=repo)
    assert ok, tail
    assert not dm.run_duelist_tests(None, root=repo)[0]                              # the working tree is broken
