"""tools/sunday/window.py: stop at D−5, restart after Duels III from floors.env, never after the Final. Synthetic."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "sunday"))
import window as w  # noqa: E402

D3, F = 18.65, 21.65


def sched(*names_at):
    return {"now_hours": 16.7, "upcoming": [{"at_hours": at, "action": "duels", "params": {"name": n}}
                                            for n, at in names_at] + [{"at_hours": 19.0, "action": "bench"}]}


def clock(t, doors="open", paused=False):
    return {"t_hours": t, "doors": doors, "paused": paused}


def no_feed(name):
    return {"scheduled": None, "finished": None}


def setup(tmp_path, monkeypatch, floors="TRADER_FLOOR=464\nOPPS_FLOOR=300\n", trader_ok=True):
    if floors is not None:
        (tmp_path / "floors.env").write_text(floors)
    if trader_ok:
        (tmp_path / "trader_ok").write_text("")
    monkeypatch.setattr(w, "FLOORS", tmp_path / "floors.env")
    monkeypatch.setattr(w, "TRADER_OK", tmp_path / "trader_ok")
    ops = w.Ops(dry=True, sleep=lambda s: None)
    return ops


def test_waits_then_stops_at_d_minus_5_only_on_a_running_clock(tmp_path, monkeypatch):
    ops, st = setup(tmp_path, monkeypatch), {}
    s = sched(("Duels III", D3), ("Final duels", F))
    assert w.step(st, clock(16.7), s, ops, feed=no_feed) == w.EVERY_S and ops.ran == []
    assert w.step(st, clock(18.5), s, ops, feed=no_feed) == w.NEAR_S and ops.ran == []   # 9 min before: watch closely
    assert w.step(st, clock(18.6, paused=True), s, ops, feed=no_feed) and ops.ran == []  # paused: no game time passes
    w.step(st, clock(18.57), s, ops, feed=no_feed)                                        # 18.65 − 5 min = 18.567
    assert ops.ran == [("stop", w.STOP, {})] and st["Duels III"]["stopped_t"] == 18.57 and not st["Duels III"]["done"]


def test_the_default_stop_list_leaves_the_trader_running():
    """Directive 07:25 (contra-duels): the trader's duel-side cost is ~0, so it keeps running."""
    assert w.STOP == ("swaps", "opps", "recorder") and "trader" not in w.STOP


def test_restart_after_duels_finished_in_order_from_floors(tmp_path, monkeypatch):
    monkeypatch.setattr(w, "STOP", ("trader", "swaps", "opps", "recorder"))       # WINDOW_STOP with the trader
    ops, st = setup(tmp_path, monkeypatch), {}
    s = sched(("Duels III", D3), ("Final duels", F))
    w.step(st, clock(18.6), s, ops, feed=no_feed)
    ops.ran.clear()
    w.step(st, clock(18.9), sched(("Final duels", F)), ops, feed=no_feed)                # under way: nothing
    assert ops.ran == []
    done = lambda n: {"scheduled": D3, "finished": 19.1 if n == "Duels III" else None}  # noqa: E731
    w.step(st, clock(19.12), sched(("Final duels", F)), ops, feed=done)
    assert [(a, n) for a, n, _ in ops.ran] == [("restart", ("trader",)), ("start", ("opps",)), ("start", ("swaps",)),
                                               ("start", ("recorder",))]
    assert ops.ran[0][2] == {"CASH_FLOOR": "464"} and ops.ran[1][2] == {"OPPS_BUILD": "RET", "CASH_FLOOR": "300"}
    assert st["Duels III"]["done"] == "restarted"
    ops.ran.clear()
    w.step(st, clock(19.5), sched(("Final duels", F)), ops, feed=done)                   # a re-look: no second restart
    assert ops.ran == []


def test_restart_falls_back_at_d_plus_65_and_never_after_the_final(tmp_path, monkeypatch):
    monkeypatch.setattr(w, "STOP", ("trader", "swaps", "opps", "recorder"))
    ops, st = setup(tmp_path, monkeypatch), {}
    w.step(st, clock(18.6), sched(("Duels III", D3), ("Final duels", F)), ops, feed=no_feed)
    w.step(st, clock(D3 + 64 / 60), sched(("Final duels", F)), ops, feed=no_feed)
    assert len(ops.ran) == 1                                                              # still waiting
    w.step(st, clock(D3 + 65 / 60), sched(("Final duels", F)), ops, feed=no_feed)
    assert st["Duels III"]["done"] == "restarted" and len(ops.ran) == 5
    ops.ran.clear()
    w.step(st, clock(F - 4 / 60), sched(("Final duels", F)), ops, feed=no_feed)
    assert ops.ran == [("stop", w.STOP, {})] and "no restart" in st["Final duels"]["done"]
    ops.ran.clear()
    w.step(st, clock(23.0), sched(), ops, feed=lambda n: {"scheduled": F, "finished": 22.4})
    assert ops.ran == []


def test_no_floors_no_restart_and_no_trader_ok_holds_the_trader(tmp_path, monkeypatch):
    monkeypatch.setattr(w, "STOP", ("trader", "swaps", "opps", "recorder"))
    ops, st = setup(tmp_path, monkeypatch, floors=None), {}
    w.step(st, clock(18.6), sched(("Duels III", D3)), ops, feed=no_feed)
    w.step(st, clock(20.0), sched(), ops, feed=lambda n: {"scheduled": D3, "finished": 19.5})
    assert ops.ran == [("stop", w.STOP, {})] and st["Duels III"]["done"] == "no floors.env"
    (tmp_path / "x").mkdir()
    ops2, st2 = setup(tmp_path / "x", monkeypatch, trader_ok=False), {}
    w.step(st2, clock(18.6), sched(("Duels III", D3)), ops2, feed=no_feed)
    w.step(st2, clock(20.0), sched(), ops2, feed=lambda n: {"scheduled": D3, "finished": 19.5})
    assert [n for _, n, _ in ops2.ran] == [w.STOP, ("opps",), ("swaps",), ("recorder",)]   # no trader


def test_armed_late_stops_at_once_or_leaves_a_finished_wave_alone(tmp_path, monkeypatch):
    ops, st = setup(tmp_path, monkeypatch), {}
    under_way = lambda n: {"scheduled": 18.65, "finished": None} if n == "Duels III" else no_feed(n)  # noqa: E731
    w.step(st, clock(18.8), sched(("Final duels", F)), ops, feed=under_way)
    assert ops.ran == [("stop", w.STOP, {})] and st["Duels III"]["at"] == 18.65
    ops, st = setup(tmp_path, monkeypatch), {}
    over = lambda n: {"scheduled": 18.65, "finished": 19.2} if n == "Duels III" else no_feed(n)  # noqa: E731
    w.step(st, clock(19.5), sched(("Final duels", F)), ops, feed=over)
    assert ops.ran == [] and "finished before" in st["Duels III"]["done"]


def test_a_bot_back_inside_the_wave_is_stopped_again(tmp_path, monkeypatch):
    ops, st = setup(tmp_path, monkeypatch), {}
    w.step(st, clock(18.6), sched(("Duels III", D3)), ops, feed=no_feed)
    ops.left = lambda: ["123 python3 agents/trader/loop.py"]
    w.step(st, clock(18.8), sched(), ops, feed=lambda n: {"scheduled": D3, "finished": None})
    assert [a for a, _, _ in ops.ran] == ["stop", "stop"]


def test_the_schedule_moves_the_wave_and_names_come_from_it(tmp_path, monkeypatch):
    ops, st = setup(tmp_path, monkeypatch), {}
    w.step(st, clock(18.6), sched(("Duels III", 19.0), ("Duels IV", 20.0), ("Final duels", F)), ops, feed=no_feed)
    assert ops.ran == [] and st["Duels III"]["at"] == 19.0                                # moved: not yet
    assert [n for n, _ in w.waves(st, None)] == ["Duels III", "Duels IV", "Final duels"]
    assert dict(w.waves(st, None)) == {"Duels III": True, "Duels IV": True, "Final duels": False}


def test_feed_and_floors_parsers(tmp_path):
    f = tmp_path / "feed.jsonl"
    f.write_text("\n".join(json.dumps(e) for e in [
        {"type": "duels.scheduled", "t": 18.65, "payload": {"name": "Duels III"}},
        {"type": "duels.finished", "t": 13.25, "payload": {"name": "Duels II"}},
        {"type": "duels.finished", "t": 19.3, "payload": {"name": "Duels III"}}]) + "\n")
    assert w.feed_events("Duels III", f) == {"scheduled": 18.65, "finished": 19.3}
    assert w.feed_events("Final duels", f) == {"scheduled": None, "finished": None}
    (tmp_path / "fl").write_text("TRADER_FLOOR=464\nOPPS_FLOOR=464\n")
    assert w.floors(tmp_path / "fl") == {"TRADER_FLOOR": 464, "OPPS_FLOOR": 464}
    (tmp_path / "fl").write_text("TRADER_FLOOR=464\n")
    assert w.floors(tmp_path / "fl") is None and w.floors(tmp_path / "none") is None


def test_one_instance_only(tmp_path, monkeypatch):
    monkeypatch.setattr(w, "LOCK", tmp_path / "window.lock")
    held = open(tmp_path / "window.lock", "a+")
    w.fcntl.flock(held, w.fcntl.LOCK_EX | w.fcntl.LOCK_NB)
    assert w.main([]) == 1                                  # a second armed instance refuses
    r = subprocess.run(["bash", "-n", str(ROOT / "tools" / "sunday" / "window.sh")])
    assert r.returncode == 0


def test_only_what_was_stopped_comes_back(tmp_path, monkeypatch):
    ops, st = setup(tmp_path, monkeypatch), {}                                           # the default list
    w.step(st, clock(18.6), sched(("Duels III", D3)), ops, feed=no_feed)
    w.step(st, clock(20.0), sched(), ops, feed=lambda n: {"scheduled": D3, "finished": 19.5})
    assert [(a, n) for a, n, _ in ops.ran] == [("stop", ("swaps", "opps", "recorder")), ("start", ("opps",)),
                                               ("start", ("swaps",)), ("start", ("recorder",))]
    monkeypatch.setattr(w, "STOP", ("swaps", "recorder"))                                 # no floors needed for these
    (tmp_path / "y").mkdir()
    ops, st = setup(tmp_path / "y", monkeypatch, floors=None), {}
    w.step(st, clock(18.6), sched(("Duels III", D3)), ops, feed=no_feed)
    w.step(st, clock(20.0), sched(), ops, feed=lambda n: {"scheduled": D3, "finished": 19.5})
    assert [n for _, n, _ in ops.ran] == [("swaps", "recorder"), ("swaps",), ("recorder",)]


def test_a_typo_in_window_stop_refuses_to_arm(monkeypatch):
    monkeypatch.setattr(w, "STOP", ("swaps", "opp"))
    assert w.main([]) == 2
