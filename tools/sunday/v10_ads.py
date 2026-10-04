"""Starter-broker ads for v10 (Chief 21:30, GUARDRAIL public rebate). One pair ad every 12 min until 22:50 from
intel/matches.md (Builder) or intel/v10-suggestions.md: both teams non-rival, giver holds 2+ (true spare), never our cards.
Single instance (lock file). `--once-rebate` posts the rebate line once."""
import json, os, re, sys, time, urllib.request
ROOT = "/Users/lucaswiese/Documents/claude-hackathon-team-5"
sys.path.insert(0, ROOT + "/bazaar-kit"); sys.path.insert(0, ROOT + "/tools")
from bazaar_sdk import Bazaar, Broker  # noqa: E402
import policy  # noqa: E402

REBATE = ("v10 tonight: 0% fee, crossed every tick — cash back 5 P per common, 10 P per uncommon or rare you sell here "
          "(max 2 per team, spares only).")
FIXED = ["Selling to Team 6 or Team 8? List on v10 instead: 0% fee, cash back 5-10 P, crossed every tick.",
         "Bidding for an epic? Post your bid on v10: sellers' bots cross there every tick."]
NEVER = {"t10", "t06", "t14", "t03", "t18", "t01", "t16", "t13", "t17", "t05"}
PAIR = re.compile(r"Team (\d+) → Team (\d+): ([A-Z]{3}-\d\d) \(holds (\d+)\) at ~(\d+) P(.*)$")
LOOSE = re.compile(r"Team (\d+)\D.*?\b([A-Z]{3}-\d\d)\b.*?\(holds (\d+)\).*?Team (\d+)\D.*?~?(\d+) P")
LOCK = ROOT + "/run/v10_ads.lock"
BUYER_ONLY = {"t15": {"MAL-09", "MAL-10"}}  # Chief 21:15: t15 has LAT/RET/LAV complete, lacks only MAL-09/10
RANK = {"rare": 0, "uncommon": 1, "common": 2}


def candidates():
    out = []
    for f in ("intel/matches.md", "intel/v10-suggestions.md"):
        path = os.path.join(ROOT, f)
        if not os.path.exists(path):
            continue
        for line in open(path):
            line = line.strip()
            cols = [x.strip() for x in line.strip("|").split("|")] if line.startswith("|") else []
            if len(cols) >= 9 and cols[0].isdigit():  # matchmaker table: # | Buyer | Card | Seller | Price | VC | Closer | Rival | Why
                yb, cs, sb, pr, rival, why = cols[1], cols[2], cols[3], cols[4], cols[7], cols[8]
                mb, ms, mc, mp = re.search(r"Team (\d+)", yb), re.search(r"Team (\d+)", sb), re.match(r"([A-Z]{3}-\d\d)", cs), re.search(r"(\d+)", pr)
                if not (mb and ms and mc and mp) or rival:
                    continue
                spare = 2 if ("holds 2" in why or "holds 3" in why or "dumps" in why) else 1
                out.append((f"t{int(ms[1]):02d}", f"t{int(mb[1]):02d}", mc[1], spare, int(mp[1])))
                continue
            m = PAIR.search(line)
            if m:
                s, y, card, n, p, rest = m[1], m[2], m[3], int(m[4]), int(m[5]), m[6]
            else:
                m = LOOSE.search(line)
                if not m:
                    continue
                s, card, n, y, p, rest = m[1], m[2], int(m[3]), m[4], int(m[5]), ""
            if "closer" in rest or "rival" in rest:
                continue
            out.append((f"t{int(s):02d}", f"t{int(y):02d}", card, n, p))
        if out:
            return out
    return out


def main():
    url, key = os.environ["BAZAAR_URL"], os.environ["BAZAAR_KEY"]
    b = Bazaar(url, key, wait_on_tick=False, timeout=8.0)
    br = Broker(url, b.me()["starter_broker_key"])
    if "--once-rebate" in sys.argv:
        print(time.strftime("%H:%M:%S"), "ANNOUNCE", br.announce(REBATE), REBATE, flush=True); return
    try:
        pid = int(open(LOCK).read())
        os.kill(pid, 0); sys.exit(f"v10_ads already running (pid {pid})")
    except (OSError, ValueError):
        open(LOCK, "w").write(str(os.getpid()))
    cat = urllib.request.urlopen(urllib.request.Request(url + "/api/catalog", headers={"X-Team-Key": key}), timeout=8).read().decode()
    rar = dict(re.findall(r'\{"id":"([A-Z]{3}-\d\d)","name":"[^"]+","rarity":"(\w+)"', cat))
    used = {("t08", "t09", "RET-09")}
    fixed = list(FIXED)
    while int(time.strftime("%H%M")) < 2250:
        try:
            lb = b._call("GET", "/api/leaderboard"); teams = lb.get("teams") if isinstance(lb, dict) else lb
            bad = NEVER | policy.rivals(teams) | policy.RIVALS
            ok = [(RANK.get(rar.get(c, "common"), 3), s, y, c, p) for s, y, c, n, p in candidates()
                  if s not in bad and y not in bad and n >= 2 and (s, y, c) not in used
                  and (y not in BUYER_ONLY or c in BUYER_ONLY[y])]
            ok.sort()
            if fixed:
                text = fixed.pop(0)
            elif ok:
                _, s, y, c, p = ok[0]; used.add((s, y, c))
                text = (f"v10 match: Team {int(s[1:])} has a spare {c}, Team {int(y[1:])} collects it. Post it as an open "
                        f"ask on v10 at ~{p} P (cash back tonight: 5 P common, 10 P uncommon/rare).")
            else:
                text = REBATE
            print(time.strftime("%H:%M:%S"), "ANNOUNCE", br.announce(text), text, flush=True)
        except Exception as e:  # noqa: BLE001
            print(time.strftime("%H:%M:%S"), "ERR", repr(e)[:150], flush=True)
        time.sleep(615)
    os.remove(LOCK)


if __name__ == "__main__":
    main()
