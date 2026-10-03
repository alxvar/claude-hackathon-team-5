"""Duel Lab switch rule for Duels III / the Final (advisory: it NEVER writes the params file).

Plan (intel/duel-lab.md, SUNDAY v2): play set C; after every closed wave, evaluate ONE rule on all closed duels of
the session so far; if it fires while C (or C2) is live, the pre-approved complete set A replaces it, once, and
nothing ever switches back. Applying is the params writer's job (tools/duel_loop.py approve with the set's proposal
file, intel/duel-sets/A.json); this script only evaluates and prints SWITCH, HOLD or DONE with the counts.

The rule: at least 12 closed duels whose rival sent at least one message, and a deal rate among them below 0.60
(7 or fewer deals of 12). Why so strict: within a session the sets can't be told apart on points (per-duel points SD
~0.31 in the simulator, so the standard error of a mean is ~0.16 over 4 duels and ~0.11 over 8, against set
differences of 0.02-0.08); only a collapse of the deal rate is visible. Simulated (scratchpad v2/switch_final.out,
LLM moves, no timeouts): fires in ~1% of benign sessions and ~18-21% of sessions against rivals that never soften;
expected value about 0 to +0.02 points per 68-duel session. Insurance against the model being wrong, not an optimiser.

Kept for tools/duel_loop.py (duelist-loop branch), which imports `gates` and `TODAY_MIN_STEP_P`: `gates()` keeps its
signature but proposes NO MIN_STEP_P change any more (the old step-up/revert gate is retired); its reason string
carries the switch rule's verdict.

Usage: python3 tools/duel_gates.py --session 4 [--params run/duel_params.json]
"""
import argparse, json, glob, os
from pathlib import Path

R = str(Path(__file__).resolve().parents[1] / 'docs' / 'duels') + '/'
MIN_N, THR = 12, 0.60
TODAY_MIN_STEP_P = 3                       # kept for tools/duel_loop.py's import
SET_C = {'MIN_STEP_P': 8, 'MAX_STEP_SHARE': 0.12, 'OPEN_WAIT': 0, 'MONO_END_SHARE': 0.25}   # C and C2 share these
SET_A = {'MIN_STEP_P': 5, 'MAX_STEP_SHARE': 0.18, 'LATE_SWITCH_LEFT': 2, 'OPEN_WAIT': 2, 'MONO_END_SHARE': 0.25}


def load(session):
    out = []
    for f in glob.glob(R + 'duel-*.json'):
        d = json.load(open(f)); D = d.get('done') or (d['payloads'][-1]['raw'] if d.get('payloads') else None)
        if D and D.get('session') == session and D['status'] in ('deal', 'no_deal'):
            out.append(D)
    return sorted(out, key=lambda D: D['deadline_tick'])


def live_set(eff):
    """'C' when the effective params are set C (or C2), 'A' when set A, else None (unknown: never switch)."""
    if not eff:
        return None
    if all(eff.get(k) == v for k, v in SET_C.items()):
        return 'C'
    if all(eff.get(k) == v for k, v in SET_A.items()):
        return 'A'
    return None


def rule(duels, eff=None):
    spoke = [D for D in duels if any(m['from'].startswith('Rival') for m in D['messages'])]
    deals = sum(D['status'] == 'deal' for D in spoke)
    ev = {'closed': len(duels), 'rival_spoke': len(spoke), 'deals': deals,
          'deal_rate': round(deals / len(spoke), 3) if spoke else None,
          'rounds_per_deal': round(sum(D['rounds'] for D in spoke if D['status'] == 'deal') / deals, 2) if deals else None,
          'live_set': live_set(eff) if eff is not None else 'unknown (no params given)'}
    if eff is not None and live_set(eff) == 'A':
        return 'DONE', 'set A is live: the one switch has happened (never back)', ev
    if len(spoke) < MIN_N:
        return 'HOLD', 'fewer than %d closed duels with a rival that spoke' % MIN_N, ev
    if deals < THR * len(spoke):
        if eff is not None and live_set(eff) != 'C':
            return 'HOLD', 'rule fired (deal rate %.2f < %.2f) but the live params are not set C: no switch' % (
                deals / len(spoke), THR), ev
        return 'SWITCH', 'deal rate %.2f < %.2f over %d duels: approve intel/duel-sets/A.json (once)' % (
            deals / len(spoke), THR, len(spoke)), ev
    return 'HOLD', 'deal rate %.2f >= %.2f: keep the current set' % (deals / len(spoke), THR), ev


def gates(duels, cur_min_step=TODAY_MIN_STEP_P, eff=None):
    """tools/duel_loop.py's entry point (kept signature): never proposes a param diff; reports the switch rule."""
    verdict, reason, ev = rule(duels, eff)
    return {}, 'Duel Lab switch rule: %s (%s)' % (verdict, reason), ev


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--session', type=int, required=True)
    ap.add_argument('--params', help="the duelist's flat params file (read only), to know which set is live")
    a = ap.parse_args()
    eff = None
    if a.params and os.path.exists(a.params):
        eff = {k: v for k, v in json.load(open(a.params)).items() if not k.startswith('_')}
    verdict, reason, ev = rule(load(a.session), eff)
    print(json.dumps({'verdict': verdict, 'reason': reason, 'evidence': ev, 'rule': {'min_n': MIN_N, 'threshold': THR}}, indent=1))
