"""Duel Lab switch rule for Duels III / the Final (advisory: it NEVER writes the params file).

Pre-approved plan (intel/duel-lab.md, SUNDAY v2): play set C (run/duel_params.json); after every closed wave, evaluate
ONE rule on all closed duels of the session so far; if it fires, the pre-approved fallback set replaces C, once, and
nothing ever switches back. Applying is the params writer's job (tools/duel_loop.py, on Aleks's 08:00 approval); this
script only evaluates and prints SWITCH or HOLD with the counts.

The rule: at least 12 closed duels whose rival sent at least one message, and a deal rate among them below 0.60
(i.e. 7 or fewer deals of 12). Why so strict: with 4-8 duels nothing distinguishes the sets (per-duel points SD 0.31,
so the standard error of a mean is 0.16 over 4 duels and 0.11 over 8, against set differences of 0.02-0.06); only a
collapse of the deal rate is visible. In simulation (v2/switch_final.out) this rule fires in ~1% of benign sessions and
~18-21% of sessions against rivals that never soften; its expected value is about +0.0 to +0.02 points per 68 duels.
It is insurance against the model being wrong, not an optimiser.

Usage: python3 tools/duel_gates.py --session 4
"""
import argparse, json, glob
from pathlib import Path

R = str(Path(__file__).resolve().parents[1] / 'docs' / 'duels') + '/'
MIN_N, THR = 12, 0.60


def load(session):
    out = []
    for f in glob.glob(R + 'duel-*.json'):
        d = json.load(open(f)); D = d.get('done') or (d['payloads'][-1]['raw'] if d.get('payloads') else None)
        if D and D.get('session') == session and D['status'] in ('deal', 'no_deal'):
            out.append(D)
    return sorted(out, key=lambda D: D['deadline_tick'])


def rule(duels):
    spoke = [D for D in duels if any(m['from'].startswith('Rival') for m in D['messages'])]
    deals = sum(D['status'] == 'deal' for D in spoke)
    ev = {'closed': len(duels), 'rival_spoke': len(spoke), 'deals': deals,
          'deal_rate': round(deals / len(spoke), 3) if spoke else None,
          'rounds_per_deal': round(sum(D['rounds'] for D in spoke if D['status'] == 'deal') / deals, 2) if deals else None}
    if len(spoke) < MIN_N:
        return 'HOLD', 'fewer than %d closed duels with a rival that spoke' % MIN_N, ev
    if deals < THR * len(spoke):
        return 'SWITCH', 'deal rate %.2f < %.2f over %d duels: apply the pre-approved fallback set (once)' % (
            deals / len(spoke), THR, len(spoke)), ev
    return 'HOLD', 'deal rate %.2f >= %.2f: keep the current set' % (deals / len(spoke), THR), ev


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--session', type=int, required=True)
    a = ap.parse_args()
    verdict, reason, ev = rule(load(a.session))
    print(json.dumps({'verdict': verdict, 'reason': reason, 'evidence': ev, 'rule': {'min_n': MIN_N, 'threshold': THR}}, indent=1))
