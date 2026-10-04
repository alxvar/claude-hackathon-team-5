"""MAL close by team trades (Chief 10:40; venue moved 10:43: t13 refuses El Rastro): ONE addressed want-card bid at a time,
on v21 (Team 9's 0% board; non-rival club market; never v10/v24/v15/El Rastro).
MAL-09 (non-last) from t08 (t13 out 10:45) at price <= our value - 1; when MAL-09 lands, MAL-07 LAST from t15 at <= value-when-last - 50.
Never two closer bids live; never t10. A bid that expires unfilled is re-posted (still one live). Stops at 13:55."""
import os, sys, json, time
ROOT = '/Users/lucaswiese/Documents/claude-hackathon-team-5'
sys.path.insert(0, ROOT + '/bazaar-kit')
from bazaar_sdk import Bazaar
b = Bazaar(os.environ['BAZAAR_URL'], os.environ['BAZAAR_KEY'], wait_on_tick=False, timeout=10.0)
PAGE = [f"MAL-{i:02d}" for i in range(1, 11)]
SELLER = {"MAL-09": "t08", "MAL-07": "t15"}  # Chief 12:20: MAL closer GO again (per-trade +50 clip, no round cap)
CAP = {"MAL-09": 48, "MAL-07": 999}
VENUE = {"MAL-09": "rastro", "MAL-07": "rastro"}   # Chief 12:20: El Rastro only (as maker: no fee)

def log(**kw):
    print(json.dumps({"t": time.strftime('%H:%M:%S'), **kw}), flush=True)

def retry(f, *a, **kw):
    for i in range(4):
        try: return f(*a, **kw)
        except Exception as e: err = e; time.sleep(3)
    raise err

def live_bids():
    """Our open MAL bids ADDRESSED to a closer seller (the book's public MAL-07 bid is not ours to manage)."""
    return [o for o in retry(b.my_offers).get('offers', []) if o.get('status') == 'open' and o.get('to') in SELLER.values()
            and any(t.startswith('card:MAL-') for t in ((o.get('want') or {}).get('types') or []))]

def drop_from_book(card):
    """When `card` becomes the LAST missing one, the book's public bid for it goes (the closer replaces it)."""
    B = ROOT + '/run/book.json'
    try:
        bk = json.load(open(B)); n = len(bk['offers'])
        bk['offers'] = [e for e in bk['offers'] if not (e['card'] == card and e['side'] == 'buy')]
        if len(bk['offers']) != n:
            json.dump(bk, open(B + '.tmp', 'w'), indent=1); os.replace(B + '.tmp', B); log(event="closed", why=f"{card} dropped from run/book.json (now last)")
            time.sleep(25)   # book.py cancels its live bid on its next loop
        for o in retry(b.my_offers).get('offers', []):
            if o.get('status') == 'open' and not o.get('to') and f'card:{card}' in ((o.get('want') or {}).get('types') or []):
                retry(b.cancel, o['id']); log(event="closed", offer=o['id'], why=f"public {card} bid cancelled: closer replaces it")
    except Exception as e:
        log(event="error", where="drop_from_book", err=repr(e)[:150])

while time.strftime('%H%M') < '1355':
    held = {a['ref'] for a in retry(b.me)['assets']}
    miss = [c for c in PAGE if c not in held]
    if not miss: log(event="end", why="MAL PAGE COMPLETE"); break
    if any(c not in SELLER for c in miss): log(event="end", why=f"unexpected missing {miss}"); break
    card = "MAL-09" if "MAL-09" in miss else "MAL-07"
    last = len(miss) == 1
    if last: drop_from_book(card)
    live = live_bids()
    for o in live:
        if f'card:{card}' not in o['want']['types'] or o.get('venue') != VENUE[card]:
            retry(b.cancel, o['id']); log(event="closed", offer=o['id'], why="not the current target")
    if not any(f'card:{card}' in o['want']['types'] and o.get('venue') == VENUE[card] for o in live_bids()):
        v = float(retry(b.value, card)['your_value'])
        price = min(CAP[card], int(v - 50)) if last else min(CAP[card], int(v - 1))
        if price <= 0: log(event="end", why=f"{card} worth {v}, last={last}: no price >= 0 exists"); break
        r = retry(b.list_offer, give={"cash": price}, want={"types": [f"card:{card}"]}, venue=VENUE[card],
                  to=SELLER[card], expires_in_ticks=120)
        log(event="open", card=card, to=SELLER[card], price=price, value=v, last=last, offer=r.get('id'), exp=r.get('expires_tick'))
    time.sleep(20)
else:
    for o in live_bids(): retry(b.cancel, o['id']); log(event="closed", offer=o['id'], why="13:55 cutoff")
