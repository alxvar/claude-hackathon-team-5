"""Operator lock, API preflight and round archiver (tools/): mocked, no network, no real keys."""
import io
import json
import os
import subprocess
import sys
import tarfile
import urllib.error
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "bazaar-kit"))
import archive_round  # noqa: E402
import operator_lock  # noqa: E402
import preflight  # noqa: E402
from bazaar_sdk import BazaarError  # noqa: E402


def dead_pid():
    p = subprocess.Popen(["true"])
    p.wait()
    return p.pid


# ---------------------------------------------------------------- operator lock

@pytest.fixture
def lock(tmp_path, monkeypatch):
    monkeypatch.setattr(operator_lock, "LOCK", tmp_path / "operator.lock")
    return operator_lock


def test_acquire_then_refuse_a_second_live_session(lock):
    me, other = os.getpid(), os.getppid()  # both alive
    assert lock.acquire("operator", pid=me)[0]
    ok, msg = lock.acquire("intruder", pid=other)
    assert not ok and "operator" in msg and "LIVE" in msg
    assert lock.read()["pid"] == me
    assert lock.acquire("operator", pid=me)[0]  # the holder may re-acquire


def test_stale_by_dead_pid(lock):
    assert lock.acquire("old", pid=dead_pid())[0]
    ok, msg = lock.acquire("new", pid=os.getpid())
    assert ok and "stale" in msg
    assert lock.read()["session"] == "new"


def test_stale_by_old_heartbeat(lock):
    assert lock.acquire("old", pid=os.getppid())[0]
    cur = lock.read()
    cur["heartbeat"] -= lock.STALE_AFTER + 1
    lock.LOCK.write_text(json.dumps(cur))
    assert lock.acquire("new", pid=os.getpid())[0]


def test_heartbeat_and_release_only_by_the_holder(lock):
    me, other = os.getpid(), os.getppid()
    lock.acquire("operator", pid=me)
    before = lock.read()["heartbeat"]
    assert lock.heartbeat(pid=me)[0] and lock.read()["heartbeat"] >= before
    assert not lock.heartbeat(pid=other)[0]
    assert not lock.release(pid=other)[0]
    assert lock.release(pid=other, force=True)[0] and lock.read() is None
    lock.acquire("operator", pid=me)
    assert lock.release(pid=me)[0] and not lock.LOCK.exists()


def test_cli(lock, capsys, monkeypatch):
    monkeypatch.setattr(lock, "owner_pid", os.getpid)
    assert lock.main(["status"]) == 0 and "none" in capsys.readouterr().out
    assert lock.main(["acquire", "operator"]) == 0
    monkeypatch.setattr(lock, "owner_pid", os.getppid)
    assert lock.main(["acquire", "other"]) == 1 and "REFUSED" in capsys.readouterr().out
    assert lock.main(["heartbeat"]) == 1
    assert lock.main(["bogus"]) == 2


# ---------------------------------------------------------------- preflight

def test_load_env_and_redact(tmp_path, monkeypatch):
    for k in preflight.KEYS:
        monkeypatch.delenv(k, raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text("# c\nexport BAZAAR_URL=https://x\nexport BAZAAR_KEY=tk-abc      # a comment\nANTHROPIC_API_KEY='sk-ant-xyz'  # x\n"
                        "# export BROKER_KEY=bk\n")
    env = preflight.load_env(env_file)
    assert env["BAZAAR_KEY"] == "tk-abc" and env["ANTHROPIC_API_KEY"] == "sk-ant-xyz" and "BROKER_KEY" not in env
    assert preflight.redact("key tk-abc and sk-ant-xyz", env) == "key <BAZAAR_KEY> and <ANTHROPIC_API_KEY>"


def test_anthropic_usage_limit_is_a_fail(monkeypatch):
    body = json.dumps({"type": "error", "error": {"type": "invalid_request_error",
                       "message": "You have reached your specified API usage limits."}}).encode()

    def boom(req, timeout=0):
        assert json.loads(req.data)["max_tokens"] == 1 and json.loads(req.data)["model"] == preflight.HAIKU
        raise urllib.error.HTTPError(req.full_url, 400, "Bad Request", {}, io.BytesIO(body))
    monkeypatch.setattr(preflight.urllib.request, "urlopen", boom)
    ok, msg = preflight.check_anthropic("sk-ant-xyz")
    assert not ok and "usage limits" in msg and "400" in msg


class FakeResp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def run_preflight(monkeypatch, capsys, anthropic, me_error=None):
    env = {"BAZAAR_URL": "https://x", "BAZAAR_KEY": "tk-secret-1", "ANTHROPIC_API_KEY": "sk-ant-secret-2"}
    monkeypatch.setattr(preflight, "load_env", lambda: env)
    monkeypatch.setattr(preflight.time, "sleep", lambda s: None)

    class FakeBazaar:
        def __init__(self, url, key, retries=3):
            pass

        def me(self):
            if me_error:
                raise BazaarError("unauthorized", f"bad key tk-secret-1 {me_error}", 401)
            return {"id": "t05", "cash": 252, "level": 2, "score": {"score": 20.0, "rank": 5}}
    monkeypatch.setattr(preflight, "Bazaar", FakeBazaar)
    monkeypatch.setattr(preflight, "check_anthropic", lambda key: anthropic)
    clock = json.dumps({"tick": 159, "paused": True, "doors": "closed", "round": 1}).encode()
    monkeypatch.setattr(preflight.urllib.request, "urlopen", lambda url, timeout=0: FakeResp(clock))
    monkeypatch.setattr(preflight.subprocess, "run",
                        lambda *a, **k: subprocess.CompletedProcess(a, 0, "collector: DOWN\n", ""))
    code = preflight.main()
    out = capsys.readouterr().out
    assert "tk-secret-1" not in out and "sk-ant-secret-2" not in out
    return code, out


def test_preflight_all_ok(monkeypatch, capsys):
    code, out = run_preflight(monkeypatch, capsys, (True, "answered"))
    assert code == 0 and "all OK" in out and "cash 252" in out and "tick 159" in out and "collector: DOWN" in out


def test_preflight_fails_on_any_key(monkeypatch, capsys):
    code, out = run_preflight(monkeypatch, capsys, (False, "HTTP 400: You have reached your specified API usage limits"))
    assert code == 1 and "FAIL  ANTHROPIC_API_KEY" in out and "usage limits" in out
    code, out = run_preflight(monkeypatch, capsys, (True, "answered"), me_error="x")
    assert code == 1 and "FAIL  BAZAAR_KEY" in out and "<BAZAAR_KEY>" in out


# ---------------------------------------------------------------- round archiver

CLOCK = {"tick": 159, "round": 1, "round_name": "Friday", "doors": "open", "today": "fri",
         "days": [{"day": "fri", "opens": "2026-10-02T19:00:00+02:00"}, {"day": "sat", "opens": "2026-10-03T09:00:00+02:00"}]}


def test_label_uses_the_game_day():
    assert archive_round.label(CLOCK) == "2026-10-02-round1"
    assert archive_round.label({**CLOCK, "today": "sat", "round": 2}) == "2026-10-03-round2"


def test_triggers():
    closed = {**CLOCK, "doors": "closed"}
    sat = {**CLOCK, "doors": "open", "today": "sat", "round": 2}
    assert archive_round.triggers(None, CLOCK) == []
    assert archive_round.triggers(CLOCK, CLOCK) == []
    [(why, c)] = archive_round.triggers(CLOCK, closed)
    assert why.startswith("day closed") and c is closed
    [(why, c)] = archive_round.triggers(closed, sat)
    assert why == "round 1 -> 2" and c is closed  # filed under the round that ended


class FakeArchiveBazaar:
    def leaderboard(self):
        return {"teams": [{"team": "t05", "score": 20}]}

    def me(self):
        return {"id": "t05", "cash": 252, "level": 2, "tick": 159, "score": {"score": 20.0},
                "assets": [1, 2], "starter_broker_key": "bk-secret"}


def test_snapshot_writes_tar_leaderboard_me_and_skips_files_with_keys(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    (root / "data").mkdir(parents=True)
    (root / "logs").mkdir()
    (root / "data" / "feed.jsonl").write_text('{"id": 1}\n')
    (root / "logs" / "oops.log").write_text("key=tk-secret-1\n")
    monkeypatch.setenv("BAZAAR_KEY", "tk-secret-1")
    monkeypatch.setattr(archive_round.time, "sleep", lambda s: None)
    out = archive_round.snapshot(FakeArchiveBazaar(), {**CLOCK, "doors": "closed"}, "test",
                                 archive=tmp_path / "archive", root=root)
    assert out.name == "2026-10-02-round1"
    [tgz] = out.glob("data-logs-*.tgz")
    with tarfile.open(tgz) as t:
        assert t.getnames() == ["data/feed.jsonl"]
    [me] = out.glob("me-*.json")
    me = json.loads(me.read_text())
    assert me["cash"] == 252 and "starter_broker_key" not in me and "assets" not in me
    assert json.loads(next(out.glob("leaderboard-*.json")).read_text())["teams"][0]["team"] == "t05"
    entry = json.loads((out / "index.jsonl").read_text())
    assert entry["reason"] == "test" and entry["skipped_files"] == ["logs/oops.log"]
