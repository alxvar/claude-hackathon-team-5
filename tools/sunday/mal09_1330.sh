#!/usr/bin/env bash
# Chief 12:03: ONE more MAL-09 attempt at the Pícaros at ≈ 13:30 (cap 49, trick guard), only if MAL-09 isn't ours by then
# (bounty 24703 to t13 expires ≈ tick 2208, 12:27). Any live MAL-09 bid of ours is cancelled first (no double fill).
R=/Users/lucaswiese/Documents/claude-hackathon-team-5; set -a; . "$R/.env"; set +a; L="$R/logs/mal_close.log"
k() { curl -s --max-time 8 -H "X-Team-Key: $BAZAAR_KEY" "$BAZAAR_URL$1"; }
until [ "$(date +%H%M)" -ge 1330 ]; do sleep 30; done
if k /api/me | python3 -c "import sys,json;sys.exit(0 if any(a['ref']=='MAL-09' for a in json.load(sys.stdin)['assets']) else 1)"; then
  echo "{\"t\": \"$(date +%T)\", \"event\": \"end\", \"why\": \"13:30 MAL-09 attempt skipped: already ours\"}" >> "$L"; exit 0; fi
python3 - <<'PY' >> "$L"
import os,sys,json,time
sys.path.insert(0,'/Users/lucaswiese/Documents/claude-hackathon-team-5/bazaar-kit')
from bazaar_sdk import Bazaar
b=Bazaar(os.environ['BAZAAR_URL'],os.environ['BAZAAR_KEY'],wait_on_tick=False,timeout=10.0)
for o in b.my_offers().get('offers',[]):
    if o.get('status')=='open' and o.get('maker')=='t05' and 'card:MAL-09' in ((o.get('want') or {}).get('types') or []):
        b.cancel(o['id']); print(json.dumps({"t":time.strftime('%H:%M:%S'),"event":"closed","offer":o['id'],"why":"before the 13:30 Pícaros MAL-09 attempt"}))
PY
while k /api/me/threads | python3 -c "import sys,json;sys.exit(0 if any(t.get('status')=='open' and t.get('with')=='picaros' for t in json.load(sys.stdin).get('threads',[])) else 1)"; do sleep 10; done
echo "{\"t\": \"$(date +%T)\", \"event\": \"open_attempt\", \"why\": \"Chief 12:03: one MAL-09 attempt at the Pícaros, cap 49\"}" >> "$L"
python3 -u "$R/run/sunday/simple_buy.py" MAL-09 --dealer picaros --open 40 --step 2 --cap 49 --floor-cash 50 --offer-only --base-value 49 --deadline 300 >> "$L" 2>&1
echo "{\"t\": \"$(date +%T)\", \"event\": \"end\", \"why\": \"13:30 MAL-09 attempt finished\"}" >> "$L"
