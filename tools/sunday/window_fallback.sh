#!/usr/bin/env bash
# Chief 11:50: opps + swaps stay DOWN for the rest of the day (run/floors.env moved to floors.env.off, so window.py's
# restart() restarts nothing). This backup brings back only the RECORDER (for the 12:37 bench): on duels.finished
# "Duels III" (or 12:10) + 180 s, if it's still down.
R=/Users/lucaswiese/Documents/claude-hackathon-team-5; set -a; . "$R/.env"; set +a
python3 -u "$R/run/sunday/wait_duels_end.py" "Duels III" --until 1210; echo "$(date +%T) fallback: duels over or 12:10; waiting 180 s"
sleep 180
cd "$R" || exit 1
if ./tools/daemons.sh status 2>/dev/null | grep -q "^recorder: running"; then echo "$(date +%T) recorder already running"
else ./tools/daemons.sh start recorder; echo "$(date +%T) fallback STARTED recorder"; fi
echo "$(date +%T) fallback done"
