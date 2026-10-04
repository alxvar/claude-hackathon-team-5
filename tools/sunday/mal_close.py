"""MAL close by team trades (Chief 10:40): ONE addressed want-card bid at a time, on El Rastro.
MAL-09 (non-last) from t13 at price + fee <= our value; when MAL-09 lands, MAL-07 LAST from t15 at <= value-when-last - 50.
Never two closer bids live; never t10. A bid that expires unfilled is re-posted (still one live). Stops at 13:55."""
import os, sys, json, time
ROOT = '/Users/lucaswiese/Documents/claude-hackathon-team-5'
sys.path.insert(0, ROOT + '/bazaar-kit')
from bazaar_sdk import Bazaar
b = Bazaar(os.environ['BAZAAR_URL'], os.environ['BAZAAR_KEY'], wait_on_tick=False, timeout=10.0)
PAGE = [f"MAL-{i:02d}" for i in range(1, 11)]
SELLER = {"MAL-09": "t13", "MAL-07": "t15"}
CAP = {"MAL-09": 45, "MAL-07": 999}

def log(**kw):
    print(json.dumps({"t": time.strftime('%H:%M:%S'), **kw}), flush=True)

def retry(f, *a, **kw):
    for i in range(4):
        try: return f(*a, **kw)
        except Exception as e: err = e; time.sleep(3)
    raise err

def live_bids():
    return [o for o in retry(b.my_offers).get('offers', []) if o.get('status') == 'open'
            and any(t.startswith('card:MAL-') for t in ((o.get('want') or {}).get('types') or []))]

while time.strftime('%H%M') < '1355':
    held = {a['ref'] for a in retry(b.me)['assets']}
    miss = [c for c in PAGE if c not in held]
    if not miss: log(event="end", why="MAL PAGE COMPLETE"); break
    if any(c not in SELLER for c in miss): log(event="end", why=f"unexpected missing {miss}"); break
    card = "MAL-09" if "MAL-09" in miss else "MAL-07"
    last = len(miss) == 1
    live = live_bids()
    for o in live:
        if f'card:{card}' not in o['want']['types']:
            retry(b.cancel, o['id']); log(event="closed", offer=o['id'], why="not the current target")
    if not any(f'card:{card}' in o['want']['types'] for o in live):
        v = float(retry(b.value, card)['your_value'])
        price = min(CAP[card], int(v - 50)) if last else min(CAP[card], int((v - 1) / 1.05))
        if price <= 0: log(event="end", why=f"{card} worth {v}, last={last}: no price >= 0 exists"); break
        r = retry(b.list_offer, give={"cash": price}, want={"types": [f"card:{card}"]}, venue="rastro",
                  to=SELLER[card], expires_in_ticks=120)
        log(event="open", card=card, to=SELLER[card], price=price, value=v, last=last, offer=r.get('id'), exp=r.get('expires_tick'))
    time.sleep(20)
else:
    for o in live_bids(): retry(b.cancel, o['id']); log(event="closed", offer=o['id'], why="13:55 cutoff")
