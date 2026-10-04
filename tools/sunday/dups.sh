#!/usr/bin/env bash
# Chief 10:40 (2): spares → dealers above their opening, never below our value, never a page copy.
# Commons: the Pícaros (L4) at >= 5 (their 4 opening never counts), else the Abuela (L1) at >= 6. Chato/Pilar don't buy commons.
R=/Users/lucaswiese/Documents/claude-hackathon-team-5; O=$R/run/sunday; set -a; . $R/.env; set +a
k() { curl -s --max-time 8 -H "X-Team-Key: $BAZAAR_KEY" "$BAZAAR_URL$1"; }
n() { k /api/me | python3 -c "import sys,json;d=json.load(sys.stdin);print(sum(a['ref']=='$1' for a in d['assets']))" 2>/dev/null; }
busy() { k /api/me/threads | python3 -c "import sys,json;d=json.load(sys.stdin);sys.exit(0 if any(t.get('status')=='open' and t.get('with')=='$1' for t in d.get('threads',[])) else 1)" 2>/dev/null; }
sell() { # card dealer ask floor keep
  [ "$(n $1)" -gt "$5" ] || { echo "$(date +%T) $1: only $(n $1) held (keep $5), skip"; return 1; }
  while busy $2; do sleep 10; done
  echo "$(date +%T) $1 → $2 ask $3 floor $4"
  python3 -u $O/dealer_sell.py $1 --dealer $2 --ask $3 --step 1 --floor $4 2>&1 | grep -E '"event": "(open|offer_her_bid|end|walk)"' | tail -3
  sleep 20
}
while kill -0 62592 2>/dev/null; do sleep 10; done   # the LAT-at-Pícaros job ends first
for c in LAV-04 SAL-04; do sell $c picaros 12 5 1; sell $c abuela 10 6 1; done
for c in LAT-01 LAT-03 LAT-04; do sell $c abuela 10 6 0; done
echo "$(date +%T) dups done"
