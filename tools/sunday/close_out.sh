#!/usr/bin/env bash
# 15:00 freeze: stop the trading daemons (scores freeze; offers would stay open, so cancel any of ours) and record the final state.
R=/Users/lucaswiese/Documents/claude-hackathon-team-5; set -a; . "$R/.env"; set +a
until [ "$(date +%H%M%S)" -ge 150020 ]; do sleep 5; done
cd "$R" && ./tools/daemons.sh stop trader opps book swaps 2>&1 | tail -4
python3 - <<'PY'
import os,sys,json,time
sys.path.insert(0,'/Users/lucaswiese/Documents/claude-hackathon-team-5/bazaar-kit')
from bazaar_sdk import Bazaar
b=Bazaar(os.environ['BAZAAR_URL'],os.environ['BAZAAR_KEY'],wait_on_tick=False,timeout=15.0)
for o in b.my_offers().get('offers',[]):
    if o.get('status')=='open' and o.get('maker')=='t05':
        try: print('cancel', o['id'], b.cancel(o['id']))
        except Exception as e: print('cancel err', o['id'], e)
me=b.me(); s=me['score']
print(json.dumps({"t":time.strftime('%H:%M:%S'),"final":{k:s.get(k) for k in ('score','rank','negotiating','market','neg_points','ladder_points','duel_points','mm_points','pages_complete','deals')},"cash":me['cash'],"v10":{k:me['venue'].get(k) for k in ('trades','traders','value_created')}}))
PY
