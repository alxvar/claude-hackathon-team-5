"""Chief 13:03 (endgame, Chato L2): LAT-06/07/08 public bids at 14 on El Rastro (value 12.5: -1.5 np each, for an L2 ladder
slot each via lat_fodder → Chato >= 14). The book can't bid above value, so these are manual: taken out of run/book.json
first (its live bids cancelled). Unfilled bids are cancelled at 13:55 (dealers close ~14:00): no LAT bought after the ladder."""
import os, sys, json, time
sys.path.insert(0, '/Users/lucaswiese/Documents/claude-hackathon-team-5/bazaar-kit')
from bazaar_sdk import Bazaar
b = Bazaar(os.environ['BAZAAR_URL'], os.environ['BAZAAR_KEY'], wait_on_tick=False, timeout=10.0)
CARDS, PRICE, BOOK = ("LAT-06", "LAT-07", "LAT-08"), 14, '/Users/lucaswiese/Documents/claude-hackathon-team-5/run/book.json'
def log(**kw): print(json.dumps({"t": time.strftime('%H:%M:%S'), **kw}), flush=True)
bk = json.load(open(BOOK)); bk['offers'] = [e for e in bk['offers'] if e['card'] not in CARDS]
json.dump(bk, open(BOOK + '.tmp', 'w'), indent=1); os.replace(BOOK + '.tmp', BOOK); log(event="book", removed=CARDS)
time.sleep(3)
for o in b.my_offers().get('offers', []):
    if o.get('status') == 'open' and o.get('maker') == 't05' and any(f'card:{c}' in ((o.get('want') or {}).get('types') or []) for c in CARDS):
        b.cancel(o['id']); log(event="closed", offer=o['id'], why="book bid replaced by the 14 bid")
held = {a['ref'] for a in b.me()['assets']}
mine = {}
for c in CARDS:
    if c in held: log(event="skip", card=c, why="held"); continue
    r = b.list_offer(give={"cash": PRICE}, want={"types": [f"card:{c}"]}, venue="rastro", expires_in_ticks=200)
    mine[c] = r.get('id'); log(event="open", card=c, price=PRICE, offer=r.get('id'), exp=r.get('expires_tick')); time.sleep(0.5)
while time.strftime('%H%M') < '1355': time.sleep(20)
for o in b.my_offers().get('offers', []):
    if o.get('id') in mine.values() and o.get('status') == 'open':
        b.cancel(o['id']); log(event="closed", offer=o['id'], why="13:55: the ladder closes at 14:00")
log(event="end", held=[c for c in CARDS if c in {a['ref'] for a in b.me()['assets']}])
