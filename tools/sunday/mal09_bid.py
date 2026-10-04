"""MAL-09 closer (Chief 12:43; MAL 9/10, MAL-09 last, value-when-last 95.4): ONE addressed want-card bid on El Rastro at 60
(+35), t08 first for 40 ticks, then ONE move to t13 at 60. Never two live. Value must stay >= price."""
import os, sys, json, time
sys.path.insert(0, '/Users/lucaswiese/Documents/claude-hackathon-team-5/bazaar-kit')
from bazaar_sdk import Bazaar
b = Bazaar(os.environ['BAZAAR_URL'], os.environ['BAZAAR_KEY'], wait_on_tick=False, timeout=10.0)
QUEUE, PRICE, LIFE = ["t08", "t13"], 60, 40
def log(**kw): print(json.dumps({"t": time.strftime('%H:%M:%S'), **kw}), flush=True)
while time.strftime('%H%M') < '1450':
    try:
        if any(a['ref'] == 'MAL-09' for a in b.me()['assets']): log(event="end", why="MAL-09 is ours: MAL PAGE COMPLETE"); break
        mine = [o for o in b.my_offers().get('offers', []) if o.get('status') == 'open' and o.get('maker') == 't05'
                and 'card:MAL-09' in ((o.get('want') or {}).get('types') or [])]
        if not mine:
            if not QUEUE: log(event="end", why="t08 and t13 bids expired unfilled"); break
            to = QUEUE.pop(0); v = float(b.value('MAL-09')['your_value'])
            if v < PRICE: log(event="end", why=f"value {v} < {PRICE}"); break
            r = b.list_offer(give={"cash": PRICE}, want={"types": ["card:MAL-09"]}, venue="rastro", to=to, expires_in_ticks=LIFE)
            log(event="open", card="MAL-09", to=to, price=PRICE, value=v, last=True, offer=r.get('id'), exp=r.get('expires_tick'))
    except Exception as e:
        log(event="error", err=repr(e)[:150])
    time.sleep(15)
