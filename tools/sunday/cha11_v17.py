"""Chief 12:55 (Lucas: "negociá y cerralo"): CHA-11 from t10, one path live at a time.
1) cancel 26414 (El Rastro 190); 2) counter on v17 (t17's stall, 0%): bid to t10, 190, want CHA-11; 3) after 8 ticks unfilled:
cancel the counter (confirm), then accept t10's 26439 (v17, 200) if still open; 4) if gone: re-post 190 to t10 on El Rastro."""
import os, sys, json, time
sys.path.insert(0, '/Users/lucaswiese/Documents/claude-hackathon-team-5/bazaar-kit')
from bazaar_sdk import Bazaar
b = Bazaar(os.environ['BAZAAR_URL'], os.environ['BAZAAR_KEY'], wait_on_tick=False, timeout=10.0)
def log(**kw): print(json.dumps({"t": time.strftime('%H:%M:%S'), **kw}), flush=True)
def held(): return any(a['ref'] == 'CHA-11' for a in b.me()['assets'])
def neg(): return b.me()['score'].get('neg_points')
n0 = neg(); log(event="start", neg=n0)
if held(): log(event="end", why="CHA-11 already ours"); sys.exit()
try: log(event="closed", offer=26414, result=str(b.cancel(26414)))
except Exception as e: log(event="cancel_err", offer=26414, err=str(e))
time.sleep(1)
if held(): log(event="end", why="t10 filled 26414 first", neg=neg()); sys.exit()
fee_ok = True
for v in b.venues().get('venues', []):
    if v.get('venue') == 'v17': fee = 200 * v.get('fee_bps', 0) / 10000 + v.get('fee_per_card', 0); fee_ok = 200 + fee <= 238; log(event="fee", fee=fee, ok=fee_ok)
c = b.list_offer(give={"cash": 190}, want={"types": ["card:CHA-11"]}, venue="v17", to="t10", expires_in_ticks=12)
log(event="open", offer=c.get('id'), venue="v17", to="t10", price=190, exp=c.get('expires_tick'))
t0 = b.clock()['tick']
while b.clock()['tick'] < t0 + 8:
    if held(): log(event="end", why="t10 accepted our 190 counter", neg=neg(), delta=round((neg() or 0) - (n0 or 0), 2)); sys.exit()
    time.sleep(5)
try: r = b.cancel(c['id']); log(event="closed", offer=c['id'], result=str(r))
except Exception as e: log(event="cancel_err", offer=c['id'], err=str(e))
time.sleep(1)
if held(): log(event="end", why="t10 accepted our counter at the last moment", neg=neg(), delta=round((neg() or 0) - (n0 or 0), 2)); sys.exit()
if not fee_ok: log(event="end", why="v17 fee + 200 > 238: stop, ask the Chief"); sys.exit()
for i in range(6):
    try: r = b.accept(26439); log(event="accept", offer=26439, result=json.dumps(r)[:200]); break
    except Exception as e:
        log(event="accept_err", i=i, err=str(e)[:150])
        if 'not_open' in str(e) or 'cancelled' in str(e) or 'settled' in str(e):
            r2 = b.list_offer(give={"cash": 190}, want={"types": ["card:CHA-11"]}, venue="rastro", to="t10", expires_in_ticks=60)
            log(event="open", offer=r2.get('id'), venue="rastro", to="t10", price=190, why="26439 gone: re-posted 190 on El Rastro"); sys.exit()
        time.sleep(6)
for i in range(8):
    time.sleep(8)
    if held(): break
log(event="end", held=held(), neg=neg(), delta=round((neg() or 0) - (n0 or 0), 2), cash=b.me()['cash'])
