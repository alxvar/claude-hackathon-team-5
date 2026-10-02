#!/usr/bin/env bash
# Start / stop / list the team's long-running processes, detached from any Claude Code session.
#   tools/daemons.sh start [name...]   tools/daemons.sh stop [name...]   tools/daemons.sh status
# Logs in logs/<name>.log, pids in run/<name>.pid. Names: status collector trader scout judge strategist
R="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$R/logs" "$R/run"
cmd_for() {
  case "$1" in
    status)    echo "python3 -u $R/tools/status.py --every 300 --push" ;;
    collector) echo "python3 -u $R/tools/collector.py" ;;
    trader)    echo "python3 -u $R/agents/trader/loop.py --min-gain 3 --min-gain-sell 6 --cash-floor 200" ;;
    scout)     echo "uv run --project $R python -u $R/agents/analyst/analyst.py --role scout --every 300" ;;
    judge)     echo "uv run --project $R python -u $R/agents/analyst/analyst.py --role judge --every 900" ;;
    strategist) echo "uv run --project $R python -u $R/agents/analyst/analyst.py --role strategist --every 2700" ;;
    *) return 1 ;;
  esac
}
ALL="status collector trader scout judge strategist"  # autoflip is DEAD (dealer buys above value subtract): never add it back
alive() { [ -f "$R/run/$1.pid" ] && kill -0 "$(cat "$R/run/$1.pid")" 2>/dev/null; }
action="$1"; shift; names="${*:-$ALL}"
for n in $names; do
  case "$action" in
    start)
      if alive "$n"; then echo "$n: already running ($(cat "$R/run/$n.pid"))"; continue; fi
      c="$(cmd_for "$n")" || { echo "$n: unknown"; continue; }
      # supervised: if the process dies (server restart, network), it comes back after 10 s
      (set -a; . "$R/.env"; set +a; nohup bash -c "while true; do $c; echo \"\$(date +%H:%M:%S) exited, restarting\"; sleep 10; done" >> "$R/logs/$n.log" 2>&1 & echo $! > "$R/run/$n.pid")
      echo "$n: started ($(cat "$R/run/$n.pid"))" ;;
    stop)
      if alive "$n"; then pkill -P "$(cat "$R/run/$n.pid")" 2>/dev/null; kill "$(cat "$R/run/$n.pid")" 2>/dev/null; echo "$n: stopped"; else echo "$n: not running"; fi
      rm -f "$R/run/$n.pid" ;;
    status)
      if alive "$n"; then echo "$n: running ($(cat "$R/run/$n.pid")) · last log: $(tail -1 "$R/logs/$n.log" 2>/dev/null | cut -c1-120)"; else echo "$n: DOWN"; fi ;;
  esac
done
