# Duel Lab simulator v2 (Sun 00:20), self-contained copy of the Duel Lab's night/sim2.py for tools/duel_loop.py.
# Price + delivery day, role-aware (limits, openers, money pies and day weights drawn by role), rivals fitted on the
# Duels II transcripts, calibrated per role on the 62 post-fix Duels II duels (intel/duel-lab.md, checkpoint 2 + FINAL).
# Worlds: RW (role-aware, use these); WORLDS/ROBUST are the earlier role-blind ones, kept for comparison.
# Policy keys differ from the v1 copy (lab/sim.py): see POLICY_KEYS below for the mapping to params.py SPEC names.
POLICY_KEYS = {"MIN_STEP_P": "smin", "MIN_STEP_SHARE": "smin_share", "MAX_STEP_SHARE": "cap", "CLOSING_TICKS": "end_ticks",
               "SILENT_KEEP": "silent_keep", "LATE_SWITCH_LEFT": "late_switch", "MONO_END_SHARE": "mono_end",
               "ACCEPT_BY": "accept_by", "OPEN_WAIT": "open_wait", "HOLD_TICKS": "hold_break", "GIVE_COST_P": "give_C",
               "GUARDS": "guard_worse"}
# The live duelist's behaviour, as modelled: dict(default_policy(), switch_any=True, end_emp=True, guard_worse=True,
# mono_end=<MONO_END_SHARE>) with the constants above; evaluate(policy, RW[world], n, T=12, d=0.10, H='H1').
"""Duel Lab night sim: price + delivery day, code-first policies, rivals fitted on Duels I + II.

Game economics (Duels II payloads, verified: pred = result on every closed deal):
  seller worth = price - cost + w_s * day      (each day adds w_s)
  buyer  worth = value - price - w_b * day     (each day costs w_b)
  pie(day) = M + (w_s - w_b) * day, M = value - cost; best pie = M + max(0, 10 (w_s - w_b)).
Score per duel = our worth / PIE * (1 - d)^rounds, rounds = min(our msgs, theirs); PIE = best pie (H1) or pie at
the agreed day (H2). No deal = 0.
"""
import json, math, random, statistics as st

F = {"W": [2.1, 2.2, 2.16, 3.79, 6.46, 5.03, 1.34, 1.16, 2.76, 0.94, 5.52, 3.19, 2.1, 5.11, 2.59, 4.63, 2.53, 3.98, 1.32, 4.51, 6.26, 1.43, 5.01, 1.08, 1.42, 2.6, 2.33, 0.95, 3.66, 5.45, 3.29, 3.34, 1.86, 2.33, 3.62, 2.12, 0.79, 2.37, 6.7, 2.56, 2.75], "LIM": [93, 65, 109, 72, 97, 98, 141, 114, 98, 87, 86, 69, 78, 34, 68, 88, 72, 77, 76, 130, 61, 125, 50, 72, 83, 122, 124, 77, 119, 79, 123, 70, 72, 114, 97, 130, 111, 78, 195, 73, 63], "U": [0.5591397849462365, 1.1538461538461537, 0.36146788990825685, 1.0138888888888888, 0.36082474226804123, 0.46938775510204084, 0.6907801418439716, 0.4614035087719298, 0.6597701149425287, 0.4186046511627907, 1.086231884057971, 0.6538461538461539, 2.2088235294117644, 0.4117647058823529, 0.3392045454545455, 1.1792207792207792, 0.7526315789473684, 0.4, 0.5081967213114754, 0.2616, 0.25900000000000006, 0.2777777777777778, 0.7120481927710843, 0.3442622950819672, 0.5991935483870967, 0.6168831168831169, 0.2579831932773109, 1.1803797468354431, 0.6134146341463415, 1.262857142857143, 0.6388888888888888, 0.31315789473684214, 0.4329896907216495, 0.4307692307692308, 0.5126126126126126, 0.4358974358974359, 0.4358974358974359, 1.0630136986301368, 1.1031746031746033]}   # Duels II fits (night/fit2.json, Sat 22:00)
W_EMP = F['W']                    # Duels II day weights (ours; rivals assumed alike)
LIM_EMP = F['LIM']                # Duels II our limits
U_EMP = [u for u in F['U'] if u > 0]   # our opener worth / limit (Duels II, LLM)
BR = {"LIM": {"seller": [69, 123, 83, 63, 79, 77, 111, 93, 77, 130, 73, 72, 72, 72, 114, 65, 76, 124, 87, 78, 73, 68, 141, 87, 83, 136, 34, 56, 80, 70, 92, 71, 60, 83], "buyer": [88, 50, 119, 114, 72, 122, 78, 98, 86, 195, 97, 110, 61, 109, 130, 97, 98, 94, 115, 68, 48, 125, 145, 99, 148, 126, 46, 122, 147, 74, 76, 82, 54, 143]}, "U": {"seller": [1.086, 0.613, 0.712, 1.103, 1.18, 0.617, 0.513, 0.559, 1.179, 0.431, 1.063, 0.949, 0.639, 1.014, 0.461, 1.154, 0.753, 0.599, 0.66, 0.654, 1.186, 0.691, 0.691, 0.667, 0.663, 0.544, 2.209, 0.814, 0.979, 1.263, 0.685, 0.948, 1.402, 0.904], "buyer": [0.339, 0.259, 0.258, 0.313, 0.278, 0.344, 0.436, 0.469, 0.419, 0.436, 0.433, 0.364, 0.508, 0.361, 0.4, 0.361, 0.367, 0.415, 0.391, 0.412, 0.375, 0.262, 0.345, 0.545, 0.275, 0.381, 0.565, 0.303, 0.354, 0.568, 0.408, 0.329, 0.37, 0.336]}, "W": {"seller": [3.19, 3.29, 1.42, 2.75, 5.45, 0.95, 0.79, 2.1, 3.98, 2.12, 2.56, 2.53, 1.86, 3.79, 1.16, 2.2, 1.32, 2.33, 0.94, 2.1, 4.46, 0.84, 1.34, 1.12, 1.07, 1.28, 5.11, 1.76, 2.33, 3.34, 2.45, 3.33, 3.21, 1.15], "buyer": [4.63, 5.01, 3.66, 2.33, 1.08, 2.6, 2.37, 5.03, 5.52, 6.7, 3.62, 3.68, 6.26, 2.16, 4.51, 6.46, 2.76, 7.74, 2.78, 2.59, 2.07, 1.43, 5.99, 4.03, 2.53, 3.78, 2.67, 3.54, 3.36, 7.75, 7.06, 4.03, 3.68, 5.0]}, "Q": {"seller": [0.22, 0.189, 0.275, 0.3, 0.317, 0.501, 0.722, 0.404, 0.891, 0.638, 0.484, 1.969, 0.919, 0.908, 0.121], "buyer": [0.148, 0.103, 0.319, 0.202, 0.572, 0.186, 0.169, 0.173, 0.537, 0.26, 0.224, 0.523, 0.243, 0.689, 0.394, 0.475, 0.322, 0.332, 0.416, 0.359, 0.572, 0.402, 0.528, 0.339, 0.201]}, "Q1": {"seller": [0.22, 0.189, 0.275, 0.3, 0.317, 0.501, 0.722, 0.404], "buyer": [0.148, 0.103, 0.319, 0.202, 0.572, 0.186, 0.169, 0.173, 0.537, 0.26, 0.224, 0.523]}}   # by role (night/byrole.json, Sat 23:00)
LIM_R, U_R, Q_R = BR['LIM'], {r: [u for u in v if u > 0] for r, v in BR['U'].items()}, BR['Q1']   # by role (night/byrole.out)
Q = [0.22, 0.15, 0.19, 0.10, 0.27, 0.32, 0.20, 0.30, 0.57, 0.19, 0.32, 0.17, 0.17, 0.50, 0.72, 0.54, 0.40, 0.26, 0.22, 0.52]
A0 = [2.51, 2.58, 3.79, 4.0, 1.65, 1.14, 1.39, 1.32, 0.61, 1.32, 2.74, 0.64, 1.08, 0.43, 1.75, 1.42, 1.41, 0.23]
AF = [0.48, 0.36, 0.9, 0.53, 0.52, 0.79, 0.76, 0.31, 0.61, 0.32, 0.84, 0.82, 0.13, 0.29, 0.46, 1.0]

# Duels II rival mix (rivals2.out, 41 duels): price behaviour x day behaviour
PRICE_MIX = [('reply', 0.55), ('clock', 0.20), ('acc_only', 0.08), ('silent', 0.07), ('holder', 0.10)]
DAY_MIX = [('own', 0.50), ('zero', 0.08), ('middle', 0.12), ('copy', 0.20), ('erratic', 0.10)]


def pick(rng, mix):
    r = rng.random(); c = 0.0
    for k, p in mix:
        c += p
        if r < c:
            return k
    return mix[-1][0]


class Duel:
    def __init__(s, rng, T, d, P):
        s.T, s.d = T, d
        s.role = 'seller' if rng.random() < 0.5 else 'buyer'
        byr = P.get('by_role', True)
        s.L = rng.choice(LIM_R[s.role] if byr else LIM_EMP)
        other = 'buyer' if s.role == 'seller' else 'seller'
        s.w_us = rng.choice(BR['W'][s.role] if byr else W_EMP)
        s.w_r = rng.choice(BR['W'][other] if byr else W_EMP)
        if P.get('fix'):
            s.role, s.L, s.w_us = P['fix']
        s.M = rng.choice(Q_R[s.role] if byr else Q) * rng.uniform(0.9, 1.1) * s.L * (P.get('M_scale_seller', P.get('M_scale', 1.0)) if s.role == 'seller' else P.get('M_scale', 1.0))
        if s.role == 'seller':
            s.cost, s.value, s.w_s, s.w_b = s.L, s.L + s.M, s.w_us, s.w_r
        else:
            s.value, s.cost, s.w_b, s.w_s = s.L, s.L - s.M, s.w_us, s.w_r
        s.best_pie = s.M + max(0.0, 10 * (s.w_s - s.w_b))
        s.our_best = 10 if s.role == 'seller' else 0
        s.their_best = 10 - s.our_best

    def pie(s, day):
        return s.M + (s.w_s - s.w_b) * day

    def w_us_at(s, p, day):
        return (p - s.cost + s.w_s * day) if s.role == 'seller' else (s.value - p - s.w_b * day)

    def w_r_at(s, p, day, blind=False):
        if s.role == 'seller':      # rival is buyer
            return s.value - p - (0 if blind else s.w_b * day)
        return p - s.cost + (0 if blind else s.w_s * day)

    def price_for_us(s, worth, day):
        return (worth + s.cost - s.w_s * day) if s.role == 'seller' else (s.value - s.w_b * day - worth)

    def price_for_r(s, worth_r, day, blind=False):
        if s.role == 'seller':
            return s.value - (0 if blind else s.w_b * day) - worth_r
        return worth_r + s.cost - (0 if blind else s.w_s * day)


class Rival:
    def __init__(s, rng, du, P):
        s.rng = rng
        s.kind = pick(rng, P.get('price_mix', PRICE_MIX))
        s.dayb = pick(rng, P.get('day_mix', DAY_MIX))
        s.blind = s.dayb in ('zero', 'middle', 'copy', 'erratic')
        base = max(du.pie(du.their_best), du.M, 1.0)
        s.base = base
        s.demand = min(rng.choice(A0) * rng.uniform(0.85, 1.15), 4.0) * base      # its worth target (to itself)
        s.floor = min(rng.choice(AF) * rng.uniform(0.85, 1.15), 1.0) * base * P.get('floor_scale', 1.0)
        s.floor = min(s.floor, s.demand)
        s.c = rng.uniform(*P.get('conc', (0.08, 0.2)))
        s.tau0 = rng.uniform(*P.get('tau0', (0.2, 0.45)))
        s.tau_end = rng.uniform(*P.get('tau_end', (0.0, 0.3)))
        s.start = 0 if rng.random() < 0.6 else rng.randint(1, 3)
        s.day = {'own': du.their_best, 'zero': 0, 'middle': 5, 'copy': du.their_best, 'erratic': rng.randint(0, 10)}[s.dayb]
        s.n = 0; s.posted = None; s.moves = 0
        s.beta = P.get('react', 0.0)          # reciprocity: extra concession per P of our last step

    def wants(s, du, ours, tl):
        if s.kind == 'silent' or ours is None:
            return False
        p, day = ours
        wr = du.w_r_at(p, day, blind=s.blind)
        if s.posted is not None:
            wr_theirs = du.w_r_at(s.posted[0], s.posted[1], blind=s.blind)
            if wr >= wr_theirs - 0.5:
                return True
        tau = s.tau_end if tl <= 3 else s.tau0
        if s.kind == 'holder':
            return wr >= s.floor
        return wr >= tau * s.base

    def post(s, du, t, we_posted_last, our_day, our_step=0.0):
        if s.kind in ('silent', 'acc_only') or t < s.start:
            return None
        if s.kind == 'holder':
            if s.n == 0:
                s.n = 1; s.posted = (round(du.price_for_r(s.floor + 0.3 * s.base, s.day, s.blind)), s.day); return s.posted
            return None
        if s.kind == 'reply' and s.n > 0 and not we_posted_last:
            return None
        if s.n > 0:
            s.demand = max(s.floor, s.demand - max(1.0, s.c * (s.demand - s.floor)) - s.beta * max(0.0, our_step))
            s.moves += 1
        if s.dayb == 'copy' and our_day is not None:
            s.day = our_day
        elif s.dayb == 'erratic':
            s.day = s.rng.randint(0, 10)
        s.n += 1
        s.posted = (round(du.price_for_r(s.demand, s.day, s.blind)), s.day)
        return s.posted


END_EMP = [0.035, 0.055, 0.065, 0.066, 0.072, 0.076, 0.078, 0.094, 0.101, 0.109, 0.111, 0.113, 0.119, 0.125, 0.131, 0.143, 0.146, 0.154, 0.157, 0.165, 0.167, 0.167, 0.169, 0.174, 0.176, 0.182, 0.195, 0.198, 0.207, 0.208, 0.215, 0.229, 0.235, 0.293, 0.321, 0.375, 0.4, 0.408, 0.412, 0.444, 0.444, 0.462, 0.481, 0.483, 0.5, 0.5, 0.5, 0.5, 0.524, 0.533, 0.556, 0.556, 0.567, 0.571, 0.643, 0.667, 0.667, 0.703, 0.703, 0.704, 0.714, 0.714, 0.724, 0.808, 0.817, 1.0, 1.594, 1.667, 3.158]   # our real last-3-ticks concessions / gap (Duels I + II, endsteps.out)
MIX_B = [('reply', 0.62), ('clock', 0.22), ('acc_only', 0.10), ('silent', 0.03), ('holder', 0.03)]
WORLDS = {
    'V1': dict(M_scale=2.0, price_mix=MIX_B, tau0=(0.4, 0.65), conc=(0.12, 0.3)),
    'V2': dict(M_scale=1.6, price_mix=MIX_B, tau0=(0.3, 0.55), conc=(0.12, 0.3)),
    'V3': dict(M_scale=1.6, price_mix=MIX_B, tau0=(0.2, 0.45), conc=(0.08, 0.2)),
}
MIX_DATA = [('reply', 0.66), ('clock', 0.17), ('acc_only', 0.14), ('silent', 0.03)]
DAY_DATA = [('own', 0.35), ('zero', 0.17), ('middle', 0.14), ('copy', 0.22), ('erratic', 0.12)]
ROBUST = {
    'V4 data mix': dict(M_scale=1.8, price_mix=MIX_DATA, day_mix=DAY_DATA, tau0=(0.3, 0.6), conc=(0.12, 0.3)),
    'V5 day-aware': dict(M_scale=1.8, price_mix=MIX_B, day_mix=[('own', 0.8), ('copy', 0.2)], tau0=(0.3, 0.6), conc=(0.12, 0.3)),
}


RW = {   # role-aware worlds (calib4.out): limits, openers, money pies and day weights drawn by role
    'R1 best fit': dict(M_scale=1.4, M_scale_seller=2.0, tau0=(0.4, 0.65), conc=(0.08, 0.2), price_mix=MIX_DATA, day_mix=DAY_DATA),
    'R2': dict(M_scale=1.2, M_scale_seller=2.0, tau0=(0.4, 0.65), conc=(0.12, 0.3), price_mix=MIX_DATA, day_mix=DAY_DATA),
    'R3': dict(M_scale=1.2, M_scale_seller=2.0, tau0=(0.3, 0.55), conc=(0.08, 0.2), price_mix=MIX_DATA, day_mix=DAY_DATA),
    'R4 day-aware': dict(M_scale=1.4, M_scale_seller=2.0, tau0=(0.4, 0.65), conc=(0.08, 0.2), price_mix=MIX_DATA, day_mix=[('own', 0.8), ('copy', 0.2)]),
    'R5 more silent/holders': dict(M_scale=1.4, M_scale_seller=2.0, tau0=(0.4, 0.65), conc=(0.08, 0.2),
                                   price_mix=[('reply', 0.5), ('clock', 0.15), ('acc_only', 0.2), ('silent', 0.1), ('holder', 0.05)], day_mix=DAY_DATA),
}


def default_policy():
    """BASE = the live duelist (4699673 + 69ef465 + 89a6dd6 + b7d91f3/6a2d2f9), approximated in code."""
    return dict(open_wait=2, u=None, u_scale=1.0, step='llm', alpha=0.15, cap=0.25, smin=3.0, smin_share=0.05,
                give_C=15.0, premium=1.0, late_switch=4, accept_by=2, small_gap=True, acc_f=None,
                silent_keep=0.15, hold_break=3, end_ticks=3, end_alpha=0.5, msg_budget=99)


def run(pol, P, rng, T=16, d=0.08, H='H1'):
    du = Duel(rng, T, d, P)
    rr = random.Random(rng.getrandbits(32)); ru = random.Random(rng.getrandbits(32))
    rv = Rival(rr, du, P)
    u_pool = U_R[du.role] if P.get('by_role', True) else U_EMP
    u_draw = rng.choice(u_pool)
    if pol.get('u_role') and du.role in pol['u_role']:
        u_draw = pol['u_role'][du.role]                       # fixed opener for this role
    elif pol['u'] is not None:
        u_draw = pol['u']
    u_draw *= pol['u_scale'] * (pol.get('u_scale_role') or {}).get(du.role, 1.0)
    ours = None; n_us = 0; our_day = du.our_best; switched = False; budget = pol['msg_budget']
    last_change = 0; we_posted_last = False; prev_their = None; last_step = 0.0
    open_worth = u_draw * du.L

    def score(p, day):
        w = du.w_us_at(p, day); rounds = min(n_us, rv.n)
        pie = du.best_pie if H == 'H1' else max(du.pie(day), w, 1e-9)   # H2: pie at the agreed day (a blind rival can accept below its limit: cap share at 1)
        return dict(deal=True, role=du.role, worth=w, wl=w / du.L, share=w / pie, rounds=rounds, score=(w / pie) * (1 - d) ** rounds, day=day, kind=rv.kind, dayb=rv.dayb)

    for t in range(T):
        tl = T - t
        if ours is not None and rv.wants(du, ours, tl) and rr.random() < 0.9:
            return score(*ours)
        th = rv.posted
        if th is not None:
            tw = du.w_us_at(*th)
            if tw > 0:
                take = tl <= pol['accept_by']
                if ours is not None:
                    ow = du.w_us_at(*ours)
                    if pol['small_gap'] and ow - tw <= max(2.0, 2 * d / (1 - d) * tw):
                        take = True
                    if pol['acc_f'] is not None:
                        nxt = ow - max(pol['smin'], pol['alpha'] * (ow - tw))
                        if tw >= pol['acc_f'] * nxt:
                            take = True
                if take:
                    return score(*th)
        prev_their = rv.posted
        rv_x = rv.post(du, t, we_posted_last, our_day if ours is not None else None, last_step)
        moved = rv_x is not None and (prev_their is None or rv_x != prev_their)
        if moved:
            last_change = t
        we_posted_last = False
        new = None
        th = rv.posted
        if ours is None:
            if t >= pol['open_wait'] or th is not None:
                if th is not None and th[1] is not None:        # day rule on their first day
                    C = abs(du.w_us_at(0, du.our_best) - du.w_us_at(0, th[1]))
                    if th[1] == du.our_best or C <= 2:
                        our_day = th[1]
                    elif rv.dayb in ('middle', 'erratic') and 0 < th[1] < 10:
                        our_day = du.our_best                    # a middle day is no signal: our corner
                    elif C <= pol['give_C']:
                        our_day = th[1]; open_worth = open_worth + 0 * C   # worth target unchanged: price moves by C
                    else:
                        our_day = du.our_best
                new = (round(du.price_for_us(open_worth, our_day)), our_day)
        else:
            ow = du.w_us_at(*ours)
            if th is None:
                start = max(round(T * 0.5), 2)
                if tl <= start and tl >= 2:
                    floor_w = pol['silent_keep'] * open_worth
                    k = min(1.0, (start - tl + 1) / (start - 2 + 1))
                    new = (round(du.price_for_us(open_worth + (floor_w - open_worth) * k, our_day)), our_day)
            else:
                tw = du.w_us_at(*th)
                gap = ow - tw
                # late switch: their day at a worth-neutral price
                if (not switched and pol['late_switch'] and tl <= pol['late_switch'] and th[1] is not None
                        and th[1] != our_day and (tw <= 0 or pol.get('switch_any'))):
                    switched = True; our_day = th[1]
                    new = (round(du.price_for_us(ow, our_day)), our_day)
                elif gap > 0:
                    trigger = moved or (t - last_change) >= pol['hold_break'] or tl <= pol['end_ticks']
                    if budget <= 0 and tl > pol['end_ticks']:
                        trigger = False
                    if trigger:
                        if tl <= pol['end_ticks']:
                            step = (ru.choice(END_EMP) if pol.get('end_emp') else pol['end_alpha']) * gap
                            if pol.get('mono_end') is not None:      # MONO_END_SHARE guard (a1d679e)
                                step = min(step, max(pol['mono_end'] * gap, min(pol['smin'], gap)))
                            if pol.get('guard_worse') and step >= gap and tw > 0:   # theirs is inside our limit and no worse: accept it
                                return score(*th)
                        elif pol['step'] == 'llm':
                            their_step = 0.0
                            step = (3.1 + 0.025 * gap) * math.exp(ru.gauss(0.2, 0.6))
                            step = min(step, pol['cap'] * gap) if pol['cap'] else step
                        else:
                            step = pol['alpha'] * gap
                        step = min(step, gap)
                        if pol.get('floor_wins') and tl > pol['end_ticks'] and step < pol['smin'] <= gap:
                            step = pol['smin']             # send the minimum step instead of holding
                        if step >= max(pol['smin'], pol['smin_share'] * gap) or tl <= pol['end_ticks']:
                            nw = max(ow - step, 0.0)
                            new = (round(du.price_for_us(nw, our_day)), our_day)
                            if tl > pol['end_ticks']:
                                budget -= 1
                            last_change = t
        if new is not None and new != ours:
            if du.w_us_at(*new) < 0:
                new = None
            else:
                last_step = 0.0 if ours is None else max(0.0, du.w_us_at(*ours) - du.w_us_at(*new))
                ours = new; n_us += 1; we_posted_last = True
    return dict(deal=False, role=du.role, worth=0.0, wl=0.0, share=0.0, rounds=min(n_us, rv.n), score=0.0, day=None, kind=rv.kind, dayb=rv.dayb)


def evaluate(pol, P=None, n=20000, seed=1, T=16, d=0.08, H='H1'):
    P = P or {}
    return [run(pol, P, random.Random(seed * 1000003 + i), T=T, d=d, H=H) for i in range(n)]


def summary(res):
    deals = [r for r in res if r['deal']]
    sc = [r['score'] for r in res]
    return dict(score=st.mean(sc), ci=1.96 * st.pstdev(sc) / math.sqrt(len(sc)), deal_rate=len(deals) / len(res),
                rounds=st.mean([r['rounds'] for r in deals]) if deals else 0,
                worth=st.mean([r['worth'] for r in deals]) if deals else 0,
                share=st.mean([r['share'] for r in deals]) if deals else 0)


def paired(a, b):
    dl = [y['score'] - x['score'] for x, y in zip(a, b)]
    return st.mean(dl), 1.96 * st.pstdev(dl) / math.sqrt(len(dl))
