"""Duel Lab live gates for Duels III / the Final (advisory only: it NEVER writes the params file).

Reads the closed duel records of one session from docs/duels/ and the duelist's flat params file
(run/duel_params.json, the duelist-loop format: {"_note": ..., "MIN_STEP_P": 5, ...}), evaluates two gates on the
session so far, and prints a proposed flat diff. Applying it is `tools/duel_loop.py approve` (the Builder's tool, the
only writer of the params file), on Aleks's call.

Gates (the simulator expects, under the Duel Lab params file at 12 ticks / 10%: deal rate ~0.93-0.95 with rivals that
spoke, ~3.0 rounds per deal; night/file_expect.out). Both need >= 8 closed duels with a rival that spoke (two waves),
because one wave of 4 is too noisy (a single no-deal makes 0.75):
  * REVERT  MIN_STEP_P -> 3 when the deal rate (rivals that spoke) is below 0.75 (with 8 duels: 5 deals or fewer)
            (false-alarm chance 3.8% if the true rate is 0.90, 7.4% at 0.87: binomial);
  * STEP UP MIN_STEP_P +1 (max 6) when rounds per deal > 3.5 over >= 6 deals and the deal rate >= 0.85.
Everything else (MAX_STEP_SHARE, LATE_SWITCH_LEFT, MONO_END_SHARE, ...) is left as it is in the file.

Usage: python3 tools/duel_gates.py --session 4 [--params run/duel_params.json]
"""
import argparse, json, glob, os, statistics as st
from pathlib import Path

R = str(Path(__file__).resolve().parents[1] / 'docs' / 'duels') + '/'
TODAY_MIN_STEP_P = 3


def load(session):
    out = []
    for f in glob.glob(R + 'duel-*.json'):
        d = json.load(open(f)); D = d.get('done') or (d['payloads'][-1]['raw'] if d.get('payloads') else None)
        if D and D.get('session') == session and D['status'] in ('deal', 'no_deal'):
            out.append(D)
    return sorted(out, key=lambda D: D['deadline_tick'])


def gates(duels, cur_min_step):
    spoke = [D for D in duels if any(m['from'].startswith('Rival') for m in D['messages'])]
    deals = [D for D in spoke if D['status'] == 'deal']
    ev = {'closed': len(duels), 'rival_spoke': len(spoke), 'deals': len(deals),
          'deal_rate': round(len(deals) / len(spoke), 3) if spoke else None,
          'rounds_per_deal': round(st.mean(D['rounds'] for D in deals), 2) if deals else None,
          'result_per_duel': round(st.mean((D['result'] or 0) for D in duels), 2) if duels else None}
    if len(spoke) < 8:
        return {}, 'fewer than 8 closed duels with a rival that spoke: no gate yet', ev
    if len(deals) < 0.75 * len(spoke) - 1e-9:          # strictly below 0.75: with 8 duels, 5 deals or fewer
        if cur_min_step != TODAY_MIN_STEP_P:
            return {'MIN_STEP_P': TODAY_MIN_STEP_P}, 'REVERT: deal rate %.2f < 0.75: the hold may be costing deals' % ev['deal_rate'], ev
        return {}, "deal rate low, but MIN_STEP_P is already today's value", ev
    if len(deals) >= 6 and ev['rounds_per_deal'] > 3.5 and ev['deal_rate'] >= 0.85 and cur_min_step < 6:
        return {'MIN_STEP_P': cur_min_step + 1}, 'STEP UP: %.1f rounds per deal > 3.5 with deal rate %.2f' % (
            ev['rounds_per_deal'], ev['deal_rate']), ev
    return {}, 'no gate fired: keep the file', ev


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--session', type=int, required=True)
    ap.add_argument('--params', help="the duelist's flat params file (read only)")
    a = ap.parse_args()
    cur = json.load(open(a.params)) if a.params and os.path.exists(a.params) else {}
    cur_min = cur.get('MIN_STEP_P', TODAY_MIN_STEP_P)
    diff, reason, ev = gates(load(a.session), cur_min)
    print(json.dumps({'current_MIN_STEP_P': cur_min, 'proposed_diff': diff, 'reason': reason, 'evidence': ev}, indent=1))
    if diff:
        print('To apply (Aleks): merge this diff into run/duel_params.json with tools/duel_loop.py approve; '
              'every other key in the file stays as it is.')
