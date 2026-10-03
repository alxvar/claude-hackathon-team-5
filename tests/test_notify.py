"""Offline tests for tools/notify.py: the HTTP call is always mocked, nothing reaches ntfy.sh."""
import json
import sys
import urllib.error
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import notify as nt  # noqa: E402


@pytest.fixture
def sent(monkeypatch):
    calls = []

    def fake_post(url, body, timeout=10):
        calls.append((url, body))
        return 200

    monkeypatch.setattr(nt, "_post", fake_post)
    monkeypatch.delenv("NTFY_URL", raising=False)
    return calls


def test_unset_topic_prints_to_stderr_and_returns_false(monkeypatch, tmp_path, sent, capsys):
    monkeypatch.delenv("NTFY_DANI", raising=False)
    assert nt.notify("dani", "SELL LAV-02", "body", state_path=tmp_path / "s.json") is False
    assert sent == []
    assert "NTFY_DANI unset" in capsys.readouterr().err
    assert not (tmp_path / "s.json").exists()


def test_posts_json_to_the_server_root(monkeypatch, tmp_path, sent):
    monkeypatch.setenv("NTFY_LUCAS", "team5-lucas-test")
    ok = nt.notify("lucas", "Título con acentos · ñ", "Che, ¿les falta la LAV-02?", priority=9, tags=["moneybag"],
                   click="https://bazaar.causaprima.ai", state_path=tmp_path / "s.json", now=1000.0)
    assert ok is True
    url, body = sent[0]
    assert url == "https://ntfy.sh/"
    assert body == {"topic": "team5-lucas-test", "title": "Título con acentos · ñ", "message": "Che, ¿les falta la LAV-02?",
                    "priority": 5, "tags": ["moneybag"], "click": "https://bazaar.causaprima.ai"}
    assert json.loads((tmp_path / "s.json").read_text()) == {"lucas|Título con acentos · ñ": 1000.0}


def test_rate_guard_same_channel_and_title_once_per_10_minutes(monkeypatch, tmp_path, sent):
    monkeypatch.setenv("NTFY_DANI", "t-dani")
    monkeypatch.setenv("NTFY_LUCAS", "t-lucas")
    s = tmp_path / "s.json"
    assert nt.notify("dani", "A", "1", state_path=s, now=0) is True
    assert nt.notify("dani", "A", "2", state_path=s, now=599) is False      # same (channel, title) within 10 min
    assert nt.notify("dani", "B", "3", state_path=s, now=599) is True       # another title goes out
    assert nt.notify("lucas", "A", "4", state_path=s, now=599) is True      # another channel goes out
    assert nt.notify("dani", "A", "5", state_path=s, now=601) is True       # 10 minutes later: again
    assert [b["message"] for _, b in sent] == ["1", "3", "4", "5"]


def test_failure_never_raises_and_is_not_recorded(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("NTFY_DANI", "t-dani")

    def boom(url, body, timeout=10):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(nt, "_post", boom)
    s = tmp_path / "s.json"
    assert nt.notify("dani", "A", "x", state_path=s, now=0) is False
    assert "failed" in capsys.readouterr().err
    assert not s.exists()  # a failed send doesn't start the 10-minute guard


def test_cli_returns_nonzero_when_topic_unset(monkeypatch, tmp_path, sent):
    monkeypatch.delenv("NTFY_DANI", raising=False)
    monkeypatch.setattr(nt, "STATE", tmp_path / "s.json")
    assert nt.main(["dani", "title", "message"]) == 1
    assert sent == []
