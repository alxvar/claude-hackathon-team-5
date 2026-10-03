"""Hot-reloaded tuning (agents/duelist/params.py): defaults are today's constants, a good file applies on the next
reload, a bad one changes nothing, and every change is logged."""
import json
import os
from pathlib import Path

import pytest

from agents.duelist import agent as A, policy as P, runner as R
from agents.duelist.model import DuelView, Offer, Role
from agents.duelist.params import CROSS, SPEC, Params, modules, validate
from agents.duelist.runner import DuelRunner, Log

SELLER = DuelView(duel_id=1, role=Role.SELLER, limit=40, item="a card", decay=0.06, duel_ticks=12)


@pytest.fixture
def params(tmp_path):
    p = Params(modules(), tmp_path / "duel_params.json")
    yield p
    for k, v in p.defaults.items():               # never leak a tuned constant into another test
        setattr(p.modules[SPEC[k].module], k, v)


def put(p: Params, data) -> None:
    p.path.write_text(data if isinstance(data, str) else json.dumps(data))
    st = p.path.stat()
    os.utime(p.path, ns=(st.st_atime_ns, st.st_mtime_ns + 1_000_000))   # a new stamp even within one clock tick


def test_every_spec_names_a_real_constant_and_its_default_is_inside_its_bounds(params):
    assert set(params.defaults) == set(SPEC)
    for k, s in SPEC.items():
        assert s.lo <= params.defaults[k] <= s.hi, k
        assert isinstance(params.defaults[k], (int, float))
    for a, b in CROSS:
        assert params.defaults[a] <= params.defaults[b]
    assert params.defaults["MAX_STEP_SHARE"] == 0.18 and params.defaults["HOLD_TICKS"] == 3


def test_a_good_file_applies_and_a_removed_key_or_file_reverts(params):
    put(params, {"_note": "wave 2", "MAX_STEP_SHARE": 0.12, "HOLD_TICKS": 5, "OPENER_SHARE": 0.5})
    r = params.reload()
    assert r["changed"] == {"MAX_STEP_SHARE": [0.18, 0.12], "HOLD_TICKS": [3, 5], "OPENER_SHARE": [0.42, 0.5]}
    assert A.MAX_STEP_SHARE == 0.12 and R.HOLD_TICKS == 5 and P.OPENER_SHARE == 0.5
    assert params.reload() == {}                                         # unchanged file: not even re-read
    put(params, {"MAX_STEP_SHARE": 0.12})
    assert params.reload()["changed"] == {"HOLD_TICKS": [5, 3], "OPENER_SHARE": [0.5, 0.42]}
    params.path.unlink()
    assert params.reload()["changed"] == {"MAX_STEP_SHARE": [0.12, 0.18]}
    assert params.overrides() == {}


@pytest.mark.parametrize("data,why", [
    ({"MAX_STEP_SHARE": 0.9}, "outside"),
    ({"NOT_A_PARAM": 1}, "unknown"),
    ({"HOLD_TICKS": 2.5}, "whole number"),
    ({"MIN_STEP_P": "3"}, "not a number"),
    ({"MIN_STEP_P": True}, "not a number"),
    ("{broken", "broken JSON"),
    ([1, 2], "JSON object"),
    ({"MIN_STEP_SHARE": 0.25, "MAX_STEP_SHARE": 0.2}, "MIN_STEP_SHARE 0.25 > MAX_STEP_SHARE 0.2"),
])
def test_a_bad_file_changes_nothing(params, data, why):
    put(params, {"HOLD_TICKS": 4})
    params.reload()
    put(params, {"OPEN_WAIT": 3, **data} if isinstance(data, dict) else data)   # a good key beside the bad one
    r = params.reload()
    assert r["changed"] == {} and any(why in e for e in r["errors"])
    assert R.HOLD_TICKS == 4 and R.OPEN_WAIT == 2                          # the last good set stays, whole


def test_a_tuned_constant_reaches_the_code_on_the_next_call(params):
    ours, theirs = Offer(price=70), Offer(price=50)
    assert A.min_step(SELLER, ours, theirs) == 3.0
    put(params, {"MIN_STEP_P": 8})
    params.reload()
    assert A.min_step(SELLER, ours, theirs) == 8.0


def test_validate_reports_each_bad_key():
    over, errors = validate({"MAX_STEP_SHARE": 0.2, "X": 1, "ACCEPT_BY": 9})
    assert over == {"MAX_STEP_SHARE": 0.2} and len(errors) == 2


def test_the_runner_reloads_and_logs_every_change(params, tmp_path):
    r = DuelRunner(None, None, None, dry_run=True, log=Log(tmp_path / "logs"), decay=None, duel_ticks=None,
                   poll_s=0.1, params=params)
    put(params, {"ACCEPT_BY": 3})
    r.tick = 900
    assert r.reload_params()["changed"] == {"ACCEPT_BY": [2, 3]}
    put(params, {"ACCEPT_BY": 9})
    assert r.reload_params()["errors"]
    events = [json.loads(x) for x in r.log.path.read_text().splitlines()]
    logged = [e for e in events if e["event"] == "params"]
    assert logged[0]["changed"] == {"ACCEPT_BY": [2, 3]} and logged[0]["overrides"] == {"ACCEPT_BY": 3}
    assert logged[1]["errors"] and R.ACCEPT_BY == 3
    assert DuelRunner(None, None, None, dry_run=True, log=Log(tmp_path / "l2"), decay=None, duel_ticks=None,
                      poll_s=0.1).reload_params() == {}                    # --no-params: nothing to read
