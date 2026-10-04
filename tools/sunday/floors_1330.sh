#!/usr/bin/env bash
# Chief / Analyst endgame: trader + opps floor 150 → 0 at 13:30 (cash doesn't score; trades only at gain >= 0, El Rastro, non-rivals).
R=/Users/lucaswiese/Documents/claude-hackathon-team-5; set -a; . "$R/.env"; set +a
until [ "$(date +%H%M)" -ge 1330 ]; do sleep 20; done
printf 'TRADER_FLOOR=0\nOPPS_FLOOR=0\n' > "$R/run/floors.env.tmp" && mv "$R/run/floors.env.tmp" "$R/run/floors.env"
cd "$R" && CASH_FLOOR=0 ./tools/daemons.sh restart trader && sleep 15 && OPPS_BUILD=RET CASH_FLOOR=0 ./tools/daemons.sh restart opps
echo "$(date +%T) floors → 0 (trader, opps restarted)"
