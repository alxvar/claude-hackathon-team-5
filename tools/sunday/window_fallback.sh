#!/usr/bin/env bash
# Backup for window.sh (its keyless clock/schedule reads are 429ing at the tick boundary; with no clock it does nothing):
# on duels.finished "Duels III" (or 12:10), wait 3 min; start whatever of opps/swaps/recorder is still down, from
# run/floors.env (opps: OPPS_BUILD=RET). tools/daemons.sh sources run/daemons.env (El Rastro routing).
R=/Users/lucaswiese/Documents/claude-hackathon-team-5; set -a; . "$R/.env"; set +a
python3 -u "$R/run/sunday/wait_duels_end.py" "Duels III" --until 1210; echo "$(date +%T) fallback: duels over or 12:10; waiting 180 s for window.sh"
sleep 180
set -a; . "$R/run/floors.env"; set +a
cd "$R" || exit 1
for n in opps swaps recorder; do
  if ./tools/daemons.sh status 2>/dev/null | grep -q "^$n: running"; then echo "$(date +%T) $n already running (window.sh did it)"; continue; fi
  case $n in
    opps) OPPS_BUILD=RET CASH_FLOOR=$OPPS_FLOOR ./tools/daemons.sh start opps ;;
    *) ./tools/daemons.sh start $n ;;
  esac
  echo "$(date +%T) fallback STARTED $n"; sleep 15
done
echo "$(date +%T) fallback done"
