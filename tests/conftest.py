"""Shared test setup: no test reads the live run/reserved.json or run/operator-handoff.md (review 17:15: 16 tests
failed in the shared tree once the Operator reserved SAL-08)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import policy  # noqa: E402


@pytest.fixture(autouse=True)
def _no_live_reserved_list(tmp_path, monkeypatch):
    monkeypatch.setattr(policy, "RESERVED", tmp_path / "no-reserved.json")
    monkeypatch.setattr(policy, "HANDOFF", tmp_path / "no-handoff.md")
