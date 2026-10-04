"""Chief 12:58: (C) disarmed (no buys from rivals). Keep 26452 (t08, 75). If it lapses unfilled, re-post ONCE to a non-rival
holder on El Rastro at 60, then stop. t01 (asset 1135 per the feed) over t09 (it was bidding 56 for MAL-09: likely needs it)."""
import os, sys, json, time
sys.path.insert(0, '/Users/lucaswiese/Documents/claude-hackathon-team-5/bazaar-kit')
from bazaar_sdk import Bazaar
b = Bazaar(os.environ['BAZAAR_URL'], os.environ['BAZAAR_KEY'], wait_on_tick=False, timeout=10.0)
def log(**kw): print(json.dumps({"t": time.strftime('%H:%M:%S'), **kw}), flush=True)
while time.strftime('%H%M') < '1445':
    try:
        if any(a['ref'] == 'MAL-09' for a in b.me()['assets']): log(event="end", why="MAL-09 ours: MAL PAGE COMPLETE"); break
        live = [o for o in b.my_offers().get('offers', []) if o.get('status') == 'open' and o.get('maker') == 't05'
                and 'card:MAL-09' in ((o.get('want') or {}).get('types') or [])]
        if not live:
            r = b.list_offer(give={"cash": 60}, want={"types": ["card:MAL-09"]}, venue="rastro", to="t01", expires_in_ticks=60)
            log(event="open", card="MAL-09", to="t01", price=60, offer=r.get('id'), exp=r.get('expires_tick'), why="26452 lapsed: one re-post"); break
    except Exception as e:
        log(event="error", err=repr(e)[:150])
    time.sleep(15)
