#!/usr/bin/env bash
# Duel windows (contra-ops #2, directive 07:05): the Operator arms it once at 08:45; it stops trader/swaps/opps/recorder
# at D−5 for every duel wave in /api/schedule and restarts them from run/floors.env after Duels III (never after the
# Final). Keyless; one instance (run/window.lock); state in run/window_state.json. Logic and tests: window.py.
#   nohup tools/sunday/window.sh >> logs/window.log 2>&1 &      # arm
#   tools/sunday/window.sh --status                              # state + next waves
#   tools/sunday/window.sh --dry --once                          # one look, runs nothing
R="$(cd "$(dirname "$0")/../.." && pwd)"
exec python3 -u "$R/tools/sunday/window.py" "$@"
