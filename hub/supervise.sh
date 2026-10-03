#!/usr/bin/env bash
# Keep one hub process alive (restart after a crash), awake (caffeinate on macOS), logging to logs/hub-<job>.log.
#   hub/supervise.sh collect [--host NAME]     # the keyless collector
#   hub/supervise.sh demand                    # the demand model, every 2 minutes
# Detached:  nohup hub/supervise.sh collect --host lucas >/dev/null 2>&1 &
# Stop:      pkill -f 'hub/supervise.sh collect'; pkill -f 'hub.collect'
set -u
cd "$(dirname "$0")/.." || exit 1
job="${1:?usage: hub/supervise.sh collect|demand [args]}"; shift
mkdir -p logs
log="logs/hub-${job}.log"
UV="$HOME/.local/bin/uv"; [ -x "$UV" ] || UV="$(command -v uv)"   # pyenv shims can shadow a working uv
case "$job" in
  collect) cmd=("$UV" run -q python -u -m hub.collect "$@") ;;
  demand)  cmd=("$UV" run -q python -u -m hub.demand --every 120 "$@") ;;
  *) echo "unknown job: $job" >&2; exit 2 ;;
esac
awake=()
command -v caffeinate >/dev/null && awake=(caffeinate -is)
while true; do
  echo "$(date '+%H:%M:%S') supervise: start ${cmd[*]}" >>"$log"
  ${awake[@]+"${awake[@]}"} "${cmd[@]}" >>"$log" 2>&1
  echo "$(date '+%H:%M:%S') supervise: exited $?, restart in 5 s" >>"$log"
  sleep 5
done
