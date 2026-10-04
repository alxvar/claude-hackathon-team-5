"""Chief 12:49 (Lucas offers t10 185, cap 190): when the feed shows t10 listing a CHA-11 ask on El Rastro at <= 190, to us
(or public), cancel our t08 CHA-11 bid first, then accept it. Above 190: ignore. Stops once CHA-11 is ours, or 14:30."""
import os, sys, json, time
sys.path.insert(0, '/Users/lucaswiese/Documents/claude-hackathon-team-5/bazaar-kit')
from bazaar_sdk import Bazaar
b = Bazaar(os.environ['BAZAAR_URL'], os.environ['BAZAAR_KEY'], wait_on_tick=False, timeout=10.0)
F = '/Users/lucaswiese/Documents/claude-hackathon-team-5/data/feed.jsonl'
def log(**kw): print(json.dumps({"t": time.strftime('%H:%M:%S'), **kw}), flush=True)
def held(): return any(a['ref'] == 'CHA-11' for a in b.me()['assets'])
pos = os.path.getsize(F); log(event="start", watching="t10 CHA-11 ask <= 190 on El Rastro")
last_held_check = 0
while time.strftime('%H%M') < '1430':
    with open(F) as f: f.seek(pos); chunk = f.read(); pos = f.tell()
    for line in chunk.splitlines():
        try: e = json.loads(line)
        except Exception: continue
        p = e.get('payload') or {}; o = p.get('offer') or {}
        if e['type'] != 'offer.listed' or e.get('actor') != 't10' or o.get('venue') != 'rastro': continue
        if not any(a.get('ref') == 'CHA-11' for a in (o.get('give') or {}).get('assets') or []): continue
        price = (o.get('want') or {}).get('cash', 0); log(event="seen", offer=o.get('id'), price=price, to=o.get('to'))
        if price > 190 or o.get('to') not in (None, 't05'): log(event="ignore", offer=o.get('id'), why="> 190 or addressed elsewhere"); continue
        if held(): log(event="end", why="CHA-11 already ours"); sys.exit(0)
        for x in b.my_offers().get('offers', []):
            if x.get('status') == 'open' and x.get('maker') == 't05' and 'card:CHA-11' in ((x.get('want') or {}).get('types') or []):
                b.cancel(x['id']); log(event="closed", offer=x['id'], why="t10's ask <= 190 replaces it")
        time.sleep(1)
        if held(): log(event="end", why="t08 filled first"); sys.exit(0)
        for i in range(6):
            try: log(event="accept", offer=o.get('id'), result=json.dumps(b.accept(o['id']))[:200]); break
            except Exception as ex: log(event="accept_retry", i=i, err=repr(ex)[:120]); time.sleep(6)
        time.sleep(20); log(event="end", held=held(), cash=b.me()['cash'], neg=b.me()['score'].get('neg_points')); sys.exit(0)
    if time.time() - last_held_check > 60:
        last_held_check = time.time()
        if held(): log(event="end", why="CHA-11 ours (t08 filled?)"); break
    time.sleep(5)
