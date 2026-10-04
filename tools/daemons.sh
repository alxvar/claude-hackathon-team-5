#!/usr/bin/env bash
# Start / stop / list the team's long-running processes, detached from any Claude Code session.
#   tools/daemons.sh start [name...]   tools/daemons.sh stop [name...]   tools/daemons.sh status
# Logs in logs/<name>.log, pids in run/<name>.pid. Names: status collector trader scout judge strategist archiver
R="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$R/logs" "$R/run"
cmd_for() {
  case "$1" in
    status)    echo "python3 -u $R/tools/status.py --every 300 --push" ;;
    collector) echo "python3 -u $R/tools/collector.py" ;;
    trader)    echo "python3 -u $R/agents/trader/loop.py --min-gain 3 --min-gain-sell 6 --cash-floor ${CASH_FLOOR:-100} --max-ratio ${TRADER_MAX_RATIO:-0.8} --exclude '${TRADER_EXCLUDE:-CHA-*,MAL-*}'" ;;  # Market 08:00: a cap per card and no CHA/MAL buys
    scout)     echo "uv run --project $R python -u $R/agents/analyst/analyst.py --role scout --every 900" ;;  # Analyst, Sun: every 15 min
    judge)     echo "uv run --project $R python -u $R/agents/analyst/analyst.py --role judge --every 1800" ;;  # every 30 min
    strategist) echo "uv run --project $R python -u $R/agents/analyst/analyst.py --role strategist --every 2700" ;;  # stopped Sun (Analyst): start only on request
    archiver)  echo "python3 -u $R/tools/archive_round.py --every 60" ;;  # read-only: snapshots at round close
    duelmon)   echo "python3 -u $R/tools/duel_monitor.py --every 15" ;;  # read-only: duel alerts + per-wave review
    recorder)  echo "cd $R && python3 -u -m broker.record_bench --loop" ;;  # read-only: records every Market Test (Market session)
    broker)    echo "cd $R && python3 -u -m broker.broker --strategy ${BROKER_STRATEGY:-auto_clone}" ;;  # needs BROKER_KEY: only after OUR venue is open (Market session)
    book)      echo "uv run --project $R python -u $R/agents/trader/book.py --cash-floor ${CASH_FLOOR:-100} --min-gain-sell ${MIN_GAIN_SELL:-1}" ;;  # the maker book (run/book.json): the Operator starts it
    swaps)     echo "uv run --project $R python -u $R/agents/trader/swaps.py" ;;  # posts addressed card-for-card swaps (Operator starts it; uv: hub model)
    hints)     echo "python3 -u $R/tools/hints.py" ;;  # read-only: dealer hints, eggs, hidden cards -> intel/hints.md + HINT lines
    matchmaker) echo "uv run --project $R python -u $R/tools/matchmaker.py" ;;  # read-only: page finishers + want-lists for v10 -> intel/matches.md
    reactor)   echo "python3 -u $R/tools/reactor.py" ;;  # read-only: public event stream -> BUY / DENY / V10 lines (logs/reactor.log) for the Operator
    radar)     echo "uv run --project $R python -u $R/tools/v10_radar.py" ;;  # read-only: buyers for asks on our v10 stall -> DM drafts to Lucas (uv: hub model)
    news)      echo "python3 -u $R/tools/news.py" ;;  # read-only: Radio Rastro -> intel/news.md, relevant items to Lucas
    bargains)  echo "python3 -u $R/tools/bargains.py" ;;  # read-only: pages Lucas when an ask is worth >= 20 to us after the fee
    opps)      echo "env CASH_FLOOR=${CASH_FLOOR:-100} python3 -u $R/tools/opportunities.py --every 30 --build ${OPPS_BUILD:-RET,CHA}" ;;  # OPPS_BUILD=RET: no CHA bids (Sunday dealer windows)  # posts addressed offers + alerts Dani: start after the 09:00 checks
    *) return 1 ;;
  esac
}
ALL="status collector trader scout judge strategist archiver duelmon opps recorder book bargains news radar swaps hints matchmaker reactor"  # broker: started by the Market session only  # autoflip is DEAD (dealer buys above value subtract): never add it back
alive() { [ -f "$R/run/$1.pid" ] && kill -0 "$(cat "$R/run/$1.pid")" 2>/dev/null; }
action="$1"; shift
case "$action" in start|stop|status) ;;
  restart) [ $# -gt 0 ] || { echo "restart needs explicit names"; exit 1; }
    "$0" stop "$@"; exec "$0" start "$@" ;;   # env (CASH_FLOOR, MIN_GAIN_SELL, ...) passes through to start
  *) echo "usage: $0 start|stop|restart|status [names]"; exit 1 ;;
esac
if [ "$action" = start ] && [ $# -eq 0 ]; then echo "start needs explicit names (safe at once: status collector archiver duelmon recorder bargains news radar hints matchmaker reactor; after the 09:00 checks: trader opps book swaps scout judge strategist)"; exit 1; fi
names="${*:-$ALL}"
for n in $names; do
  case "$action" in
    start)
      if alive "$n"; then echo "$n: already running ($(cat "$R/run/$n.pid"))"; continue; fi
      c="$(cmd_for "$n")" || { echo "$n: unknown"; continue; }
      # supervised: if the process dies (server restart, network), it comes back after 10 s
      (set -a; . "$R/.env"; [ -f "$R/run/daemons.env" ] && . "$R/run/daemons.env"; set +a; nohup bash -c "while true; do $c; echo \"\$(date +%H:%M:%S) exited, restarting\"; sleep 10; done" >> "$R/logs/$n.log" 2>&1 & echo $! > "$R/run/$n.pid")
      echo "$n: started ($(cat "$R/run/$n.pid"))" ;;
    stop)
      if alive "$n"; then pkill -P "$(cat "$R/run/$n.pid")" 2>/dev/null; kill "$(cat "$R/run/$n.pid")" 2>/dev/null; echo "$n: stopped"; else echo "$n: not running"; fi
      rm -f "$R/run/$n.pid" ;;
    status)
      if alive "$n"; then echo "$n: running ($(cat "$R/run/$n.pid")) · last log: $(tail -1 "$R/logs/$n.log" 2>/dev/null | cut -c1-120)"; else echo "$n: DOWN"; fi ;;
  esac
done
