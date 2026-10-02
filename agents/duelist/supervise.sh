#!/usr/bin/env bash
# Keep the duelist alive: if the process dies (crash, network, server restart), start it again after 5 s.
# The duel records live in docs/duels/ and the game keeps each duel's messages, so a restart picks the duels up.
#   agents/duelist/supervise.sh --negotiator-model claude-sonnet-5-5      (any `run` flags)
# Ctrl-C stops both the run and the loop.
cd "$(dirname "$0")/../.." || exit 1
trap 'echo "supervisor stopped"; exit 0' INT TERM
while true; do
  uv run python -m agents.duelist run "$@"
  code=$?
  echo "$(date +%H:%M:%S) duelist exited ($code); restarting in 5 s (Ctrl-C to stop)"
  sleep 5
done
