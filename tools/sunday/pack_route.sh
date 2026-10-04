#!/usr/bin/env bash
# Chief 11:58: route the castizo pack (Chato egg, 11:59): LAV-08 spare → Pilar > 16 (3rd L3 slot) else Chato > 13 (empty L2);
# RET-03 spare + LAT-05 → the Pícaros > 4 else the Abuela >= 6. Never below our value; keep 1 copy of page cards.
R=/Users/lucaswiese/Documents/claude-hackathon-team-5; O=$R/run/sunday; set -a; . $R/.env; set +a
k() { curl -s --max-time 8 -H "X-Team-Key: $BAZAAR_KEY" "$BAZAAR_URL$1"; }
n() { k /api/me | python3 -c "import sys,json;d=json.load(sys.stdin);print(sum(a['ref']=='$1' for a in d['assets']))" 2>/dev/null; }
busy() { k /api/me/threads | python3 -c "import sys,json;d=json.load(sys.stdin);sys.exit(0 if any(t.get('status')=='open' and t.get('with')=='$1' for t in d.get('threads',[])) else 1)" 2>/dev/null; }
sell() { # card dealer ask floor keep → 0 on deal
  [ "$(n $1)" -gt "$5" ] || { echo "$(date +%T) $1: only $(n $1) held (keep $5), skip"; return 0; }
  while busy $2; do sleep 10; done
  echo "$(date +%T) $1 → $2 ask $3 floor $4"
  out=$(python3 -u $O/dealer_sell.py $1 --dealer $2 --ask $3 --step 1 --floor $4 2>&1); echo "$out" | grep -E '"event": "(open|offer_her_bid|end|walk)"' | tail -3
  sleep 15; echo "$out" | grep -q '"status": "deal"'
}
( sell LAV-08 pilar 24 17 1 || sell LAV-08 chato 20 14 1 ) &
( sell RET-03 picaros 12 5 1 || sell RET-03 abuela 10 6 1; sleep 10; sell LAT-05 picaros 12 5 0 || sell LAT-05 abuela 10 6 0 ) &
wait; echo "$(date +%T) pack_route done"
