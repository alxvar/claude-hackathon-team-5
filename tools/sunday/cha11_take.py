"""On the Chief's GO only: cancel 25784 (t08, 240) unless it already filled, then accept t10's public CHA-11 ask (default
26209, 162 on El Rastro; we pay the taker fee). Never two CHA-11: abort if we already hold one."""
import os, sys, json, time
sys.path.insert(0, '/Users/lucaswiese/Documents/claude-hackathon-team-5/bazaar-kit')
from bazaar_sdk import Bazaar
b = Bazaar(os.environ['BAZAAR_URL'], os.environ['BAZAAR_KEY'], wait_on_tick=False, timeout=10.0)
ASK = int(sys.argv[1]) if len(sys.argv) > 1 else 26209
def held(): return any(a['ref'] == 'CHA-11' for a in b.me()['assets'])
if held(): sys.exit("CHA-11 already ours: nothing to do")
try: print('cancel 25784', b.cancel(25784))
except Exception as e: print('cancel 25784:', e)
time.sleep(1)
if held(): sys.exit("t08 filled 25784 first: CHA-11 ours, skip the t10 ask")
v = float(b.value('CHA-11')['your_value']); print('value', v)
for i in range(6):
    try: print('ACCEPT', ASK, json.dumps(b.accept(ASK))[:300]); break
    except Exception as e:
        print('accept try', i, e); time.sleep(6)
time.sleep(20); print('held now:', held(), 'cash', b.me()['cash'])
