"""CHA-11 (Chief 12:26): ONE addressed want-card bid at a time on El Rastro at min(220, value - 50); t08 first (25638),
then ONE move to t16 when it expires unfilled. Never two live (a 2nd copy is a dup worth ~25%). Cash after the bid >= 100."""
import os, sys, json, time
sys.path.insert(0, '/Users/lucaswiese/Documents/claude-hackathon-team-5/bazaar-kit')
from bazaar_sdk import Bazaar
b = Bazaar(os.environ['BAZAAR_URL'], os.environ['BAZAAR_KEY'], wait_on_tick=False, timeout=10.0)
QUEUE = ["t16"]
def log(**kw): print(json.dumps({"t": time.strftime('%H:%M:%S'), **kw}), flush=True)
while time.strftime('%H%M') < '1445':
    try:
        me = b.me()
        if any(a['ref'] == 'CHA-11' for a in me['assets']): log(event="end", why="CHA-11 is ours"); break
        mine = [o for o in b.my_offers().get('offers', []) if o.get('status') == 'open' and o.get('maker') == 't05']
        if not any('card:CHA-11' in ((o.get('want') or {}).get('types') or []) for o in mine):
            if not QUEUE: log(event="end", why="t08 and t16 bids expired unfilled"); break
            to = QUEUE.pop(0); v = float(b.value('CHA-11')['your_value']); price = int(min(220, v - 50))
            committed = sum((o['give'] or {}).get('cash', 0) for o in mine)
            if v < 260 or me['cash'] - committed - price < 100: log(event="end", why=f"value {v} or cash guard"); break
            r = b.list_offer(give={"cash": price}, want={"types": ["card:CHA-11"]}, venue="rastro", to=to, expires_in_ticks=60)
            log(event="open", card="CHA-11", to=to, price=price, value=v, offer=r.get('id'), exp=r.get('expires_tick'))
    except Exception as e:
        log(event="error", err=repr(e)[:150])
    time.sleep(20)
