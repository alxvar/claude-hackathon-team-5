#!/usr/bin/env bash
# Keep the duelist alive: if the process dies (crash, network, server restart), start it again after 5 s.
# The duel records live in docs/duels/ and the game keeps each duel's messages, so a restart picks the duels up.
#   agents/duelist/supervise.sh --negotiator-model claude-sonnet-5-5      (any `run` flags)
# Ctrl-C stops both the run and the loop. The laptop stays awake while it runs (caffeinate on macOS).
cd "$(dirname "$0")/../.." || exit 1
UV="$HOME/.local/bin/uv"; [ -x "$UV" ] || UV="$(command -v uv)"   # pyenv shims can shadow a working uv
"$UV" --version >/dev/null 2>&1 || { echo "no working uv (tried $UV)"; exit 1; }
awake=()
command -v caffeinate >/dev/null && awake=(caffeinate -is)
trap 'echo "supervisor stopped"; exit 0' INT TERM
while true; do
  ${awake[@]+"${awake[@]}"} "$UV" run python -m agents.duelist run "$@"
  code=$?
  if [ "$code" -eq 3 ]; then
    echo "$(date +%H:%M:%S) another duelist holds the lock on this machine; not restarting"
    exit 3
  fi
  echo "$(date +%H:%M:%S) duelist exited ($code); restarting in 5 s (Ctrl-C to stop)"
  sleep 5
done
