# Duel Lab simulator, copied from the Duel Lab session's scratch lab/sim.py (Sat 15:50) so tools/duel_loop.py is
# reproducible on any machine. Copied unchanged otherwise: fit and worlds as in intel/duel-lab.md §2-3. Price-only
# duels; score = share of the pie x (1 - d)^rounds. Run `python3 tools/duel_sim.py` for the Duels I replay.
"""Duel Lab Monte Carlo: price-only duels, rival-response model fitted on Duels I.

Coordinates: x = our surplus in P at a price (our limit at x=0, the rival's limit at x=pie).
Rival share at x = (pie - x)/pie. Score = (x/pie) * (1-d)^rounds, rounds = min(our msgs, theirs).
"""
import random, math, statistics as st

# ---- empirical inputs (Duels I, docs/duels; pies inferred from duel_points jumps) ----
Q = [0.22, 0.15, 0.19, 0.10, 0.27, 0.32, 0.20, 0.30, 0.57, 0.19, 0.32, 0.17, 0.17, 0.50, 0.72, 0.54, 0.40, 0.26, 0.22, 0.52]  # pie / our limit
U = [0.55, 0.26, 0.55, 0.43, 0.49, 0.40, 0.22, 0.40, 0.38, 0.51, 0.44, 0.67, 0.44, 0.40, 0.64, 0.44, 0.35, 0.36, 0.32, 0.40, 0.43, 0.41]  # our opener x / limit
A0 = [2.51, 2.58, 3.79, 4.0, 1.65, 1.14, 1.39, 1.32, 0.61, 1.32, 2.74, 0.64, 1.08, 0.43, 1.75, 1.42, 1.41, 0.23]  # rival opening demand (rival share)
AF = [0.48, 0.36, 0.9, 0.53, 0.52, 0.79, 0.76, 0.31, 0.61, 0.32, 0.84, 0.82, 0.13, 0.29, 0.46, 1.0]  # rival posted floor (rival share)
LIMS = [44, 57, 60, 64, 71, 72, 73, 74, 75, 80, 86, 87, 87, 92, 94, 95, 97, 100, 101, 101, 103, 108, 122, 124, 125, 129, 146, 160, 170, 172, 175, 192, 196, 219]
ALPHA = None  # filled from steps (our step / gap, Duels I), see below
ALPHA_EMP = [0.03, 0.05, 0.06, 0.08, 0.1, 0.1, 0.12, 0.14, 0.17, 0.17, 0.2, 0.22, 0.25, 0.3, 0.31, 0.35, 0.4, 0.5, 0.6]


class Rival:
    def __init__(s, rng, pie, T, P):
        s.pie = pie
        r = rng.random()
        if r < P['p_dead']:
            s.mode = 'dead'
        elif r < P['p_dead'] + P['p_acc_only']:
            s.mode = 'acc_only'
        elif r < P['p_dead'] + P['p_acc_only'] + P['p_once']:
            s.mode = 'once'
        else:
            s.mode = 'every' if rng.random() < P['p_every'] else 'reply'
        s.a = min(rng.choice(A0) * rng.uniform(0.85, 1.15), 4.0)
        s.af = min(rng.choice(AF) * rng.uniform(0.85, 1.15), 1.0)
        s.af = min(s.af, s.a)
        s.fast = rng.random() < P.get('p_fast', 0.0)
        s.c = rng.uniform(*P['conc_fast']) if s.fast else rng.uniform(*P['conc'])  # fraction of remaining distance per move
        s.rho = P['rho']                          # reaction to our step
        s.tau0 = rng.uniform(*P['tau0'])          # acceptance threshold (rival share) mid-duel
        s.tau_end = rng.uniform(*P['tau_end'])    # near the deadline
        s.start = 0 if rng.random() < 0.6 else (rng.randint(1, 3) if rng.random() < 0.6 else rng.randint(4, 9))
        s.holder = rng.random() < P['p_holder']   # concedes twice then holds
        s.moves = 0
        s.posted = None  # x of standing rival offer
        s.n = 0

    def x_of(s, a):
        return s.pie * (1 - a)

    def wants(s, x_us, ticks_left):
        if s.mode == 'dead' or x_us is None:
            return False
        share = (s.pie - x_us) / s.pie
        if s.posted is not None and x_us <= s.posted:
            return True
        tau = s.tau_end if ticks_left <= 3 else s.tau0
        return share >= tau

    def post(s, rng, t, we_posted_last, our_step):
        """Return x posted this tick or None."""
        if s.mode in ('dead', 'acc_only') or t < s.start:
            return None
        if s.mode == 'once':
            if s.n == 0:
                s.n = 1; s.posted = s.x_of(s.a); return s.posted
            return None
        if s.mode == 'reply' and s.n > 0 and not we_posted_last and rng.random() > 0.3:
            return None
        if s.n > 0:
            stop = s.holder and s.moves >= 2
            if not stop and rng.random() < 0.8:
                stepx = max(1.0, s.c * (s.a - s.af) * s.pie) + s.rho * max(0.0, our_step)
                s.a = max(s.af, s.a - stepx / s.pie); s.moves += 1
        s.n += 1
        s.posted = s.x_of(s.a)
        return s.posted


def default_policy():
    return dict(u_scale=1.0, alpha=None, smin=3.0, wait_first=0, budget=99, end_ticks=3, end_alpha=0.5,
                acc_ratio=None, small_gap=True, deadline_acc=2, silent_walk=True, hold_break=3, move_on='rival_move')


def run(policy, P, rng, T=16, d=0.08, lim=None):
    lim = lim or rng.choice(LIMS)
    pie = rng.choice(Q) * rng.uniform(0.9, 1.1) * lim
    u_draw = rng.choice(U) * rng.uniform(0.9, 1.1)
    rr = random.Random(rng.getrandbits(32)); ru = random.Random(rng.getrandbits(32))
    rv = Rival(rr, pie, T, P)
    x_us = None; n_us = 0; first_us = None
    last_their = None; last_change_t = 0; our_last_step = 0.0
    u0 = u_draw * policy['u_scale'] * lim
    open_x = u0
    floor_walk = policy.get('walk_floor', 0.3) * u0
    budget_left = policy['budget']
    we_posted_last = False
    first_in = None
    for t in range(T):
        tl = T - t
        # 1. rival accepts our standing offer?
        if x_us is not None and rv.wants(x_us, tl) and rr.random() < P['p_check']:
            rounds = min(n_us, rv.n)
            return dict(deal=True, x=x_us, pie=pie, rounds=rounds, score=(x_us / pie) * (1 - d) ** rounds, mode=rv.mode, u0=open_x, closer='rival', first_in=first_in)
        # 2. we accept their standing offer?
        xt = rv.posted
        if xt is not None and xt > 0:
            take = False
            if tl <= policy['deadline_acc']:
                take = True
            if x_us is not None and policy['small_gap'] and (x_us - xt) <= max(2.0, 2 * d / (1 - d) * xt):
                take = True
            if policy['acc_ratio'] is not None and x_us is not None and xt >= policy['acc_ratio'] * x_us:
                take = True
            if policy.get('acc_abs') is not None and xt >= policy['acc_abs'] * open_x:
                take = True
            if take:
                rounds = min(n_us, rv.n)
                return dict(deal=True, x=xt, pie=pie, rounds=rounds, score=(xt / pie) * (1 - d) ** rounds, mode=rv.mode, u0=open_x, closer='us', first_in=first_in)
        # 3. both post
        prev_their = rv.posted
        rv_x = rv.post(rr, t, we_posted_last, our_last_step)
        rival_moved = rv_x is not None and (last_their is None or abs(rv_x - last_their) > 0.5)
        if rival_moved:
            last_change_t = t
        we_posted_last = False
        new = None
        if x_us is None:
            if t >= policy['wait_first'] or rv.posted is not None:
                new = open_x
        else:
            theirs = rv.posted
            if theirs is None:
                # silent rival: code walk from half the duel to a 30% floor at 2 ticks left
                if policy['silent_walk'] and tl <= T // 2 and tl >= 2:
                    k = (T // 2 - tl + 1) / (T // 2 - 1)
                    new = open_x - (open_x - floor_walk) * min(1.0, k)
            else:
                gap = x_us - theirs
                trigger = rival_moved or (t - last_change_t) >= policy['hold_break']
                if tl <= policy['end_ticks']:
                    a = policy['end_alpha']; trigger = True
                else:
                    a = policy['alpha']
                    if budget_left <= 0:
                        trigger = False
                if trigger and gap > 0:
                    if policy.get('mirror') is not None and tl > policy['end_ticks']:
                        their_step = 0.0 if prev_their is None or theirs is None else max(0.0, theirs - prev_their)
                        cand = x_us - min(gap, max(policy['smin'], policy['mirror'] * their_step))
                    elif a is None and tl > policy['end_ticks']:
                        their_step = 0.0 if prev_their is None or theirs is None else max(0.0, theirs - prev_their)
                        stp = (3.1 + 0.21 * their_step + 0.025 * gap) * math.exp(ru.gauss(P.get('step_mu', STEP_MU), P.get('step_sd', STEP_SD))) * policy.get('step_scale', 1.0)
                        cand = x_us - min(stp, gap)
                        STEPLOG.append(min(stp, gap) / gap)
                    else:
                        cand = x_us - a * gap
                    cand = max(cand, 0.0)
                    if policy.get('cap_share') and tl > policy['end_ticks']:
                        cand = max(cand, x_us - policy['cap_share'] * gap)    # never concede more than this share of the gap
                    if policy.get('floor_share') and tl > policy['end_ticks']:
                        cand = min(cand, x_us - policy['floor_share'] * gap)   # enlarge small steps to a share of the gap
                        cand = max(cand, 0.0)
                    if (x_us - cand >= max(policy['smin'], policy.get('smin_share', 0.0) * gap)) or tl <= policy['end_ticks']:
                        new = cand
                        if tl > policy['end_ticks']:
                            budget_left -= 1
                        last_change_t = t
        if new is not None and (x_us is None or abs(new - x_us) >= 0.5):
            our_last_step = 0.0 if x_us is None else x_us - new
            x_us = new; n_us += 1; we_posted_last = True
        if rv_x is not None:
            last_their = rv_x
            if first_in is None and rv_x > 0:
                first_in = (rv_x / pie) * (1 - d) ** min(n_us, rv.n)
    return dict(deal=False, x=None, pie=pie, rounds=min(n_us, rv.n), score=0.0, mode=rv.mode, closer=None, first_in=first_in)


WORLDS = {}
STEP_MU, STEP_SD = 0.0, 0.45
STEPLOG = []
BASE_P = dict(p_dead=0.09, p_acc_only=0.06, p_once=0.12, p_every=0.8, conc=(0.03, 0.12), rho=0.24,
              tau0=(0.2, 0.45), tau_end=(0.0, 0.3), p_holder=0.15, p_check=0.9)


WORLDS['W1 original'] = dict(BASE_P, p_fast=0.0, conc_fast=(0, 0))
WORLDS['W2 fast/slow mix'] = dict(BASE_P, p_fast=0.7, conc_fast=(0.35, 0.65), conc=(0.02, 0.08), tau0=(0.3, 0.55), tau_end=(0.0, 0.3))
WORLDS['W3 tough accept'] = dict(BASE_P, p_fast=0.85, conc_fast=(0.35, 0.65), conc=(0.02, 0.08), tau0=(0.45, 0.75), tau_end=(0.1, 0.4))
WORLDS['W4 lumpy steps'] = dict(BASE_P, step_mu=0.2, step_sd=0.6, p_fast=0.6, conc_fast=(0.35, 0.65), conc=(0.02, 0.08), tau0=(0.45, 0.75), tau_end=(0.0, 0.3))


def evaluate(policy, P=BASE_P, n=20000, seed=1, T=16, d=0.08):
    res = []
    for i in range(n):
        rng = random.Random(seed * 1000003 + i)
        res.append(run(policy, P, rng, T=T, d=d))
    return res


def summary(res):
    deals = [r for r in res if r['deal']]
    sc = [r['score'] for r in res]
    m = st.mean(sc); se = st.pstdev(sc) / math.sqrt(len(sc))
    return dict(score=m, ci=1.96 * se, deal_rate=len(deals) / len(res),
                rounds=st.mean([r['rounds'] for r in deals]) if deals else 0,
                share=st.mean([r['x'] / r['pie'] for r in deals]) if deals else 0,
                r01=sum(1 for r in deals if r['rounds'] <= 1) / max(1, len(deals)),
                r7=sum(1 for r in deals if r['rounds'] >= 7) / max(1, len(deals)))


def paired(a, b):
    """mean and 95% CI of b - a (common random numbers)."""
    dlt = [y['score'] - x['score'] for x, y in zip(a, b)]
    return st.mean(dlt), 1.96 * st.pstdev(dlt) / math.sqrt(len(dlt))


if __name__ == '__main__':
    pol = default_policy()
    s = summary(evaluate(dict(pol, smin=1.0), T=16, d=0.06, n=10000))
    print('Duels I replay (d=.06):', {k: round(v, 3) for k, v in s.items()})
