"""Offline red team for the duelist: a fake game server, rival bots and experiments around the real DuelRunner code.

Never talks to the game: the team keys are dropped from the environment and the SDK's `Bazaar` raises if anything
builds one. Logs go to the scratch folder (never docs/duels/, which the monitor reads, nor logs/duelist/, which
holds the live duelist's lock). Run from this worktree's root with the main repo's venv:

    ../claude-hackathon-team-5/.venv/bin/python -m redteam.days        # experiment 1 (policy models, $0)
"""
from __future__ import annotations

import os
from pathlib import Path

for _k in ("BAZAAR_KEY", "BROKER_KEY", "BAZAAR_URL"):
    os.environ.pop(_k, None)

import agents.duelist  # noqa: E402,F401  (puts bazaar-kit on sys.path)
import bazaar_sdk  # noqa: E402


class _NoGame:
    def __init__(self, *a, **k):
        raise RuntimeError("redteam: the real game is never called from the simulator")


bazaar_sdk.Bazaar = _NoGame  # type: ignore[misc,assignment]

SCRATCH = Path(os.environ.get("REDTEAM_OUT", "/private/tmp/claude-501/-Users-alex-Workspaces-Personal-claude-hackathon-"
                              "team-5/1ea7dc29-ceb9-4525-ab36-d19bb7298cfe/scratchpad/redteam"))
SCRATCH.mkdir(parents=True, exist_ok=True)
