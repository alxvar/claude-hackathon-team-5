"""Sunday v10 ad (Chief 10:00; text 10:46: deal reward): one fixed transactional line every 15 min until 15:00 via the starter broker. No rebates."""
import os, sys, time
sys.path.insert(0, "/Users/lucaswiese/Documents/claude-hackathon-team-5/bazaar-kit")
from bazaar_sdk import Bazaar, Broker  # noqa: E402
TEXT = ("v10 (Puesto de Team 5) deal reward: complete any trade on v10 (0% fee) and Team 5 buys one of your spare "
        "LAT or MAL cards at a fair price right after. Today only.")  # Chief 10:46
b = Bazaar(os.environ["BAZAAR_URL"], os.environ["BAZAAR_KEY"], wait_on_tick=False, timeout=10.0)
br = Broker(os.environ["BAZAAR_URL"], b.me()["starter_broker_key"])
while time.strftime("%H%M") < "1500":
    try:
        print(time.strftime("%H:%M:%S"), "ANNOUNCE", br.announce(TEXT), flush=True)
    except Exception as e:  # noqa: BLE001
        print(time.strftime("%H:%M:%S"), "ERR", repr(e)[:150], flush=True); time.sleep(60); continue
    time.sleep(900)
