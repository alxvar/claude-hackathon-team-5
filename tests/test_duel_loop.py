"""Offline tests for tools/duel_loop.py on small synthetic records (never the live docs/duels, which keep growing).
The simulator is faked where the logic is the point (fast), and real with a few hundred duels end to end."""
import json

import pytest

from agents.duelist import params as pm
from tools import duel_loop as dl

D = 0.08


# ------------------------------------------------------------------ synthetic records

def say(tick, who, price=None, days=None):
    return {"tick": tick, "from": "you" if who == "us" else "Rival Gris", "text": "", "price": price, "days": days}


def duel(n, *, start=100, status="no_deal", role="seller", limit=50, price=None, days=None, result=0.0, msgs=(),
         issues=("price",), weight=None, meaning=None, decisions=()):
    """A record as agents/duelist/records.py writes it; status None: still live (no final payload)."""
    msgs = list(msgs)
    ours = sum(m["from"] == "you" for m in msgs)
    raw = {"duel": n, "session": 3, "status": "live", "role": role, "your_limit": limit, "rival": "Rival Gris",
           "deadline_tick": start + 16, "decay_per_round": D, "issues": list(issues), "your_days_weight": weight,
           "days_meaning": meaning, "messages": msgs, "rounds": min(ours, len(msgs) - ours)}
    rec = {"duel": n, "session": {"session": 3, "name": "Duels II", "duel_ticks": 16, "decay": D}, "first_tick": start,
           "view": {"role": role, "limit": limit, "duel_ticks": 16, "issues": list(issues)},
           "payloads": [{"tick": start, "raw": raw}], "decisions": list(decisions)}
    if status is not None:
        rec["done"] = {**raw, "status": status, "price": price, "days": days, "result": result}
    return rec


def folder(tmp_path, recs, *, feed=(), scores=()):
    f = tmp_path / "duels"
    f.mkdir(exist_ok=True)
    for old in f.glob("duel-*.json"):
        old.unlink()
    for r in recs:
        (f / f"duel-{r['duel']}.json").write_text(json.dumps(r))
    events = [{"id": 1, "tick": 100, "type": "duels.scheduled",
               "payload": {"session": 3, "name": "Duels II", "duel_ticks": 16, "decay": D}}, *feed]
    (f / "feed.jsonl").write_text("".join(json.dumps(e) + "\n" for e in events))
    (f / "scores.jsonl").write_text("".join(json.dumps(s) + "\n" for s in scores))
    return f


def by_id(book):
    return {x.id: x for x in book.duels}


@pytest.fixture
def src(tmp_path):
    """The duelist's constants, as module sources (no policy.py: the code policy hasn't landed)."""
    s = tmp_path / "duelist"
    s.mkdir()
    (s / "agent.py").write_text("MIN_STEP_P = 3\nMIN_STEP_SHARE = 0.05\nMAX_STEP_SHARE = 0.18\nCLOSING_TICKS = 3\n"
                                "SILENT_FROM = 0.5\nSILENT_KEEP = 0.15  # a comment\nNOT_A_PARAM = 7\n"
                                "def f():\n    MAX_STEP_SHARE = 0.9\n")
    (s / "runner.py").write_text("DECIDE_LEFT = 3\nACCEPT_BY = 2\nOPEN_WAIT = 2\nHOLD_TICKS = 3\n")
    return s


# ------------------------------------------------------------------ waves

def three(first_id, start, *, live=(), status="no_deal", same_start=False):
    return [duel(n, start=start if same_start else start + i, status=None if n in live else status)
            for i, n in enumerate(range(first_id, first_id + 3))]


def test_only_closed_waves_are_picked(tmp_path):
    recs = three(1, 100, same_start=True) + three(4, 116, live=(6,)) + [duel(7, start=130), duel(8, start=131)]
    book = dl.load(folder(tmp_path, recs))
    assert [(w.id, [x.id for x in w.duels], w.closed) for w in book.waves] == [
        ("3.1", [1, 2, 3], True), ("3.2", [4, 5, 6], False), ("3.3", [7, 8], False)]
    assert dl.pick(book.waves).id == "3.1"          # 3.2 has a live duel; 3.3 is short and the session runs on
    assert dl.pick(book.waves, "2").id == "3.2" and dl.pick(book.waves, "3.3").id == "3.3"

    recs[5] = duel(6, start=118)                    # duel 6 finishes
    assert dl.pick(dl.load(folder(tmp_path, recs)).waves).id == "3.2"
    over = [{"id": 9, "tick": 160, "type": "duels.finished", "payload": {"session": 3, "name": "Duels II"}}]
    assert dl.pick(dl.load(folder(tmp_path, recs, feed=over)).waves).id == "3.3"   # the session is over


def test_wave_size_is_the_session_max_concurrent_when_known(tmp_path):
    recs = three(1, 100, same_start=True) + three(4, 116)
    f = folder(tmp_path, recs)
    lines = (f / "feed.jsonl").read_text().replace('"decay": 0.08}', '"decay": 0.08, "max_concurrent": 2}', 1)
    (f / "feed.jsonl").write_text(lines)
    assert [len(w.duels) for w in dl.load(f).waves] == [2, 2, 2]


# ------------------------------------------------------------------ the summary

def test_decay_lost_and_in_limit_offers_missed(tmp_path):
    keep2 = (1 - D) ** 2
    recs = [
        # deal at their 70 after two rounds: the best in-limit offer is the one we took, nothing missed
        duel(11, status="deal", price=70, result=round(20 * keep2, 1),
             msgs=[say(100, "us", 90), say(100, "them", 60), say(101, "us", 75), say(101, "them", 70)]),
        # no deal while their 60 sat inside our 50: 10 P x 0.92 (one round) missed
        duel(12, msgs=[say(100, "us", 90), say(100, "them", 60)]),
        # deal at 55 after passing their 62 (11.0 P then) for 4.2 P: 6.8 missed
        duel(13, status="deal", price=55, result=round(5 * keep2, 1),
             msgs=[say(100, "us", 90), say(100, "them", 62), say(101, "us", 80), say(101, "them", 55)]),
        # their 40 was never inside our limit
        duel(14, msgs=[say(100, "us", 90), say(100, "them", 40)]),
    ]
    xs = by_id(dl.load(folder(tmp_path, recs)))
    assert xs[11].surplus == pytest.approx(20, abs=0.1)
    assert xs[11].decay_lost == pytest.approx(20 * (1 - keep2), abs=0.1)
    assert xs[11].missed is None and xs[14].missed is None
    assert xs[12].missed == {"tick": 100, "price": 60, "day": None, "value": 9.2, "lost": 9.2}
    assert xs[13].missed["price"] == 62 and xs[13].missed["lost"] == pytest.approx(6.8, abs=0.05)

    obs = dl.observe(list(xs.values()))
    assert (obs["duels"], obs["deals"], obs["deal_rate"], obs["rounds"]) == (4, 2, 0.5, 2.0)
    assert obs["decay_lost_p"] == pytest.approx((xs[11].surplus + xs[13].surplus) * (1 - keep2), abs=0.01)
    assert {x.id for x in obs["missed"]} == {12, 13}
    assert obs["missed_p"] == pytest.approx(9.2 + 6.8, abs=0.05)
    assert dl.as_json(obs)["missed"] == [12, 13]


def test_days_settled_day_cost_and_day_bonus_in_the_limit(tmp_path):
    recs = [
        # buyer, 2 P a day from day 0: the deal on day 5 cost us 10 P against our best day
        duel(21, role="buyer", limit=100, issues=("price", "days"), weight=2,
             meaning="each delivery day costs you this much cash", status="deal", price=80, days=5,
             result=round(10 * (1 - D), 1), msgs=[say(100, "us", 70, 0), say(100, "them", 80, 5)]),
        # seller, a 3 P bonus a day: their 45 on day 10 is worth -5 + 30 to us, inside our limit; on day 0 it isn't
        duel(22, role="seller", limit=50, issues=("price", "days"), weight=3,
             meaning="each delivery day adds this much cash to your side",
             msgs=[say(100, "us", 90, 10), say(100, "them", 45, 0), say(101, "us", 85, 10), say(101, "them", 45, 10)]),
    ]
    xs = by_id(dl.load(folder(tmp_path, recs)))
    assert (xs[21].best_day, xs[21].day, xs[21].day_cost) == (0, 5, 10.0)
    assert xs[21].surplus == pytest.approx(10, abs=0.1)
    assert xs[22].missed["day"] == 10 and xs[22].missed["value"] == pytest.approx(25 * (1 - D) ** 2, abs=0.05)
    obs = dl.observe(list(xs.values()))
    assert (obs["days_deals"], obs["best_day_deals"], obs["day_cost_p"]) == (1, 0, 10.0)


def test_share_from_a_score_jump_that_holds_one_deal_alone(tmp_path):
    recs = [duel(n, start=90, status="deal", price=60, result=round(10 * (1 - D), 1),
                 msgs=[say(95, "us", 70), say(95, "them", 60)]) for n in (31, 32, 33)]
    closed = [{"id": 10 + n, "tick": t, "type": "duel.closed", "payload": {"duel": n, "status": "deal"}}
              for n, t in ((31, 105), (32, 115), (33, 118))]
    scores = [{"tick": 100, "duel_points": 1.0}, {"tick": None, "duel_points": 1.2},
              {"tick": 110, "duel_points": 1.5}, {"tick": 120, "duel_points": 2.3}]
    xs = by_id(dl.load(folder(tmp_path, recs, feed=closed, scores=scores)))
    assert xs[31].points == pytest.approx(0.5) and xs[31].share == pytest.approx(0.5 / (1 - D), abs=0.001)
    assert xs[32].points is None and xs[33].points is None       # two deals in one interval: no pie
    obs = dl.observe(list(xs.values()))
    assert obs["share_n"] == 1 and obs["score_est"] and obs["score"] == pytest.approx(0.5)


def test_latency_counts_model_code_and_fallback_moves():
    decisions = [
        {"took_s": 5.0, "move": {"meta": {"calls": [{"stage": "strategist", "latency_s": 4.0},
                                                    {"stage": "negotiator", "latency_s": 1.0}]}}},
        {"took_s": 0.01, "hold": True, "move": {"meta": {"rule": "deadline", "calls": []}}},
        {"took_s": 12.0, "move": {"meta": {"fallback": "timeout after 10 s", "calls": []}}},
    ]
    x = dl.read_duel(duel(41, decisions=decisions), {})
    lat = dl.latency([x])
    assert (lat["n"], lat["max"], lat["p90"], lat["model"], lat["code"], lat["fallbacks"], lat["timeouts"],
            lat["holds"]) == (3, 12.0, 12.0, 1, 1, 1, 1, 1)
    assert lat["stages"] == {"strategist": 4.0, "negotiator": 1.0}


# ------------------------------------------------------------------ params -> the simulator's policy

def test_defaults_are_read_from_the_module_sources(src):
    assert dl.module_defaults(src) == {"MIN_STEP_P": 3, "MIN_STEP_SHARE": 0.05, "MAX_STEP_SHARE": 0.18,
                                       "CLOSING_TICKS": 3, "SILENT_FROM": 0.5, "SILENT_KEEP": 0.15,
                                       "DECIDE_LEFT": 3, "ACCEPT_BY": 2, "OPEN_WAIT": 2, "HOLD_TICKS": 3}


def test_this_checkouts_constants_parse():
    found = dl.module_defaults()
    assert {"MIN_STEP_P", "MIN_STEP_SHARE", "MAX_STEP_SHARE", "SILENT_KEEP", "ACCEPT_BY", "HOLD_TICKS"} <= set(found)
    assert all(isinstance(v, (int, float)) for v in found.values())


def test_params_map_onto_the_sim_policy(src, tmp_path):
    p = tmp_path / "duel_params.json"
    p.write_text(json.dumps({"_note": "x", "MAX_STEP_SHARE": 0.25, "OPENER_SHARE": 0.5}))
    _, over, errors = dl.read_params(p)
    eff = dl.effective(dl.module_defaults(src), over)
    assert errors == [] and eff["MAX_STEP_SHARE"] == 0.25 and "OPENER_SHARE" not in eff   # no policy.py: ignored
    pol = dl.sim_policy(eff, days=False, code=False)
    base = dl.sim.default_policy()
    assert {k: pol[k] for k in ("smin", "smin_share", "cap_share", "end_ticks", "walk_floor", "deadline_acc",
                                "hold_break", "wait_first")} == {
        "smin": 3, "smin_share": 0.05, "cap_share": 0.25, "end_ticks": 3, "walk_floor": 0.15, "deadline_acc": 2,
        "hold_break": 3, "wait_first": 0}                          # price only: the opener doesn't wait
    assert (pol["u_scale"], pol["alpha"], pol["end_alpha"]) == (base["u_scale"], base["alpha"], base["end_alpha"])
    assert dl.sim_policy(eff, days=True, code=False)["wait_first"] == 2

    (src / "policy.py").write_text("OPENER_SHARE = 0.43\nCODE_STEP_SHARE = 0.15\nEND_STEP_SHARE = 0.5\n")
    eff = dl.effective(dl.module_defaults(src), over)
    code = dl.sim_policy(eff, days=False, code=True)
    assert code["u_scale"] == pytest.approx(0.5 / dl.mean(dl.sim.U)) and code["alpha"] == 0.15
    assert dl.sim_policy(eff, days=False, code=False)["alpha"] is None     # the models play: the LLM step model


def test_a_bad_params_file_counts_as_no_overrides(tmp_path):
    p = tmp_path / "duel_params.json"
    p.write_text("{broken")
    _, over, errors = dl.read_params(p)
    assert over == {} and len(errors) == 1 and errors[0].startswith("broken JSON")
    p.write_text(json.dumps({"MAX_STEP_SHARE": 0.2, "NOPE": 1}))      # one bad key: the whole file is ignored
    assert dl.read_params(p)[1] == {} and dl.read_params(p)[2] == ["NOPE: unknown parameter"]
    assert dl.read_params(tmp_path / "missing.json") == ({}, {}, [])


def test_the_closest_world_is_picked_and_a_missing_share_drops_out():
    preds = {"A": {"deal_rate": 0.9, "rounds": 3.0, "share": 0.6}, "B": {"deal_rate": 0.8, "rounds": 5.0, "share": 0.3}}
    assert dl.closest({"deal_rate": 0.8, "rounds": 5.0, "share": 0.31}, preds)[0] == "B"
    world, dist = dl.closest({"deal_rate": 0.9, "rounds": 3.5, "share": None}, preds)
    assert world == "A" and dist["A"] == pytest.approx(0.1)


# ------------------------------------------------------------------ the proposal (the simulator faked)

DEF = {"MIN_STEP_P": 3, "MIN_STEP_SHARE": 0.05, "MAX_STEP_SHARE": 0.18, "CLOSING_TICKS": 3, "SILENT_KEEP": 0.15,
       "ACCEPT_BY": 2, "DECIDE_LEFT": 2, "OPEN_WAIT": 2, "HOLD_TICKS": 8}


@pytest.fixture
def fake_sim(monkeypatch):
    """evaluate returns the policy itself; paired looks the change up in `gains`: ((sim key, value), ...) -> (mean,
    ci)."""
    gains = {}

    def evaluate(policy, P=None, n=0, seed=0, T=16, d=D):
        return [dict(policy)]

    def paired(a, b):
        change = tuple(sorted((k, v) for k, v in b[0].items() if a[0].get(k) != v))
        return gains.get(change, (0.0, 0.01))

    monkeypatch.setattr(dl.sim, "evaluate", evaluate)
    monkeypatch.setattr(dl.sim, "paired", paired)
    monkeypatch.setattr(dl.sim, "WORLDS", {"W": {}})
    return gains


def search(defaults=DEF, over=None):
    over = over or {}
    base = dl.sim_policy(dl.effective(defaults, over), days=False, code=False)
    return dl.search(defaults, over, world="W", base_runs=[base], T=16, d=D, days=False, code=False)


def test_only_tweaks_with_ci_above_zero_that_validate_are_proposed(fake_sim):
    fake_sim.update({
        (("cap_share", 0.21),): (0.01, 0.002),       # kept
        (("cap_share", 0.15),): (-0.01, 0.002),      # worse
        (("smin_share", 0.08),): (0.004, 0.006),     # CI spans 0
        (("hold_break", 9),): (0.5, 0.001),          # HOLD_TICKS 9 is past its bound: never run
        (("hold_break", 7),): (0.002, 0.001),        # kept
        (("walk_floor", 0.1),): (0.006, 0.002),      # kept
        (("deadline_acc", 3),): (0.5, 0.001),        # ACCEPT_BY 3 > DECIDE_LEFT 2: never run
        (("cap_share", 0.21), ("hold_break", 7), ("walk_floor", 0.1)): (0.02, 0.003),
    })
    found = search()
    rows = {(r["name"], r["to"]): r for r in found["rows"]}
    assert [k for k, r in rows.items() if r["kept"]] == [("MAX_STEP_SHARE", 0.21), ("HOLD_TICKS", 7),
                                                         ("SILENT_KEEP", 0.1)]
    assert rows[("HOLD_TICKS", 9)]["why"].startswith("invalid") and rows[("HOLD_TICKS", 9)]["mean"] is None
    assert "ACCEPT_BY 3 > DECIDE_LEFT 2" in rows[("ACCEPT_BY", 3)]["why"]
    assert rows[("MIN_STEP_SHARE", 0.08)]["why"] == "no clear effect (CI spans 0)"
    assert rows[("MAX_STEP_SHARE", 0.15)]["why"] == "worse (CI below 0)"
    assert rows[("OPENER_SHARE", None)]["why"].startswith("no default")
    assert found["params"] == {"MAX_STEP_SHARE": 0.21, "HOLD_TICKS": 7, "SILENT_KEEP": 0.1}
    assert found["combined"]["kept"]
    for name, value in found["params"].items():
        assert pm.validate({name: value})[1] == []


def test_a_combination_that_isnt_better_falls_back_to_the_best_single_tweak(fake_sim):
    fake_sim.update({(("cap_share", 0.21),): (0.01, 0.002), (("walk_floor", 0.1),): (0.006, 0.002),
                     (("cap_share", 0.21), ("walk_floor", 0.1)): (0.008, 0.003)})
    found = search()
    assert found["params"] == {"MAX_STEP_SHARE": 0.21} and not found["combined"]["kept"]


def test_no_change_when_nothing_clears_zero(fake_sim):
    found = search()
    assert found["params"] == {} and found["combined"] is None and not any(r["kept"] for r in found["rows"])


def test_tweaks_build_on_the_files_overrides(fake_sim):
    fake_sim.update({(("cap_share", 0.28),): (0.01, 0.002)})
    found = search(over={"MAX_STEP_SHARE": 0.25})
    assert found["params"] == {"MAX_STEP_SHARE": 0.28}


# ------------------------------------------------------------------ approve and revert

def write_proposal(tmp_path, params, base=None):
    p = tmp_path / "proposal.json"
    p.write_text(json.dumps({"wave": "3.6", "made_at": "2026-10-03T22:00:00", "params": params,
                             "evidence": {"base_overrides": base or {}}}))
    return p


def test_approve_merges_validates_and_notes(tmp_path, src, capsys):
    params = tmp_path / "run" / "duel_params.json"
    params.parent.mkdir()
    params.write_text(json.dumps({"_note": "old", "HOLD_TICKS": 4}))
    prop = write_proposal(tmp_path, {"MAX_STEP_SHARE": 0.21, "ACCEPT_BY": 1}, base={"HOLD_TICKS": 4})
    assert dl.approve(proposal_path=prop, params_path=params, by="Aleks", src=src) == 0
    data = json.loads(params.read_text())
    assert {k: v for k, v in data.items() if k != "_note"} == {"HOLD_TICKS": 4, "MAX_STEP_SHARE": 0.21, "ACCEPT_BY": 1}
    assert "wave 3.6" in data["_note"] and "approved by Aleks" in data["_note"]
    assert pm.validate(data)[1] == []
    out = capsys.readouterr().out
    assert "MAX_STEP_SHARE: default 0.18 → 0.21" in out and "ACCEPT_BY: default 2 → 1" in out
    assert "warning" not in out
    assert not list(params.parent.glob("*.tmp"))


def test_approve_only_some_names(tmp_path, src):
    params = tmp_path / "duel_params.json"
    prop = write_proposal(tmp_path, {"MAX_STEP_SHARE": 0.21, "ACCEPT_BY": 1})
    assert dl.approve(proposal_path=prop, params_path=params, only=["ACCEPT_BY"], by="x", src=src) == 0
    assert {k: v for k, v in json.loads(params.read_text()).items() if k != "_note"} == {"ACCEPT_BY": 1}
    assert dl.approve(proposal_path=prop, params_path=params, only=["HOLD_TICKS"], by="x", src=src) == 1


@pytest.mark.parametrize("existing, change, why", [
    ({"HOLD_TICKS": 4}, {"MAX_STEP_SHARE": 0.9}, "outside"),                          # past SPEC's bound
    ({"MAX_STEP_SHARE": 0.1}, {"MIN_STEP_SHARE": 0.2}, "MIN_STEP_SHARE 0.2 > MAX_STEP_SHARE 0.1"),  # CROSS
    ({"HOLD_TICKS": 4}, {"ACCEPT_BY": 2.5}, "whole number"),
])
def test_approve_refuses_and_writes_nothing(tmp_path, src, capsys, existing, change, why):
    params = tmp_path / "duel_params.json"
    params.write_text(json.dumps(existing))
    before = params.read_text()
    assert dl.approve(proposal_path=write_proposal(tmp_path, change), params_path=params, by="x", src=src) == 1
    assert params.read_text() == before
    out = capsys.readouterr().out
    assert "refused" in out and why in out


def test_approve_refuses_a_broken_params_file(tmp_path, src):
    params = tmp_path / "duel_params.json"
    params.write_text("{half")
    assert dl.approve(proposal_path=write_proposal(tmp_path, {"ACCEPT_BY": 1}), params_path=params, src=src) == 1
    assert params.read_text() == "{half"


def test_approve_writes_atomically(tmp_path, src, monkeypatch):
    params = tmp_path / "duel_params.json"
    params.write_text(json.dumps({"HOLD_TICKS": 4}))
    moves = []
    real = dl.os.replace

    def spy(a, b):
        moves.append((str(a), str(b)))
        real(a, b)

    monkeypatch.setattr(dl.os, "replace", spy)
    assert dl.approve(proposal_path=write_proposal(tmp_path, {"ACCEPT_BY": 1}), params_path=params, src=src) == 0
    assert moves == [(str(params) + ".tmp", str(params))]

    def crash(a, b):
        raise OSError("disk full")

    monkeypatch.setattr(dl.os, "replace", crash)
    before = params.read_text()
    with pytest.raises(OSError):
        dl.approve(proposal_path=write_proposal(tmp_path, {"ACCEPT_BY": 3}), params_path=params, src=src)
    assert params.read_text() == before                 # the duelist never sees a half-written file


def test_approve_from_the_markdown_and_with_nothing_proposed(tmp_path, src, capsys):
    md = tmp_path / "duel-loop.md"
    md.write_text('# Duel loop\n\n## wave\n```json\n{"wave": "3.7", "params": {"SILENT_KEEP": 0.1}}\n```\n'
                  '## older\n```json\n{"wave": "3.6", "params": {"ACCEPT_BY": 1}}\n```\n')
    params = tmp_path / "duel_params.json"
    assert dl.approve(proposal_path=md, params_path=params, by="x", src=src) == 0
    assert {k: v for k, v in json.loads(params.read_text()).items() if k != "_note"} == {"SILENT_KEEP": 0.1}
    md.write_text('# Duel loop\n\n## wave 3.8\n**Proposal:** no change proposed.\n'
                  '## wave 3.7\n```json\n{"wave": "3.7", "params": {"ACCEPT_BY": 1}}\n```\n')
    before = params.read_text()
    assert dl.approve(proposal_path=md, params_path=params, by="x", src=src) == 1     # never an older, stale block
    assert params.read_text() == before
    empty = tmp_path / "empty"
    empty.mkdir()
    assert dl.approve(proposal_path=write_proposal(empty, {}), params_path=empty / "p.json", src=src) == 0
    assert not (empty / "p.json").exists() and "nothing to approve" in capsys.readouterr().out


def test_revert_deletes_the_overrides(tmp_path, src, capsys):
    params = tmp_path / "duel_params.json"
    params.write_text(json.dumps({"_note": "wave 3.6", "MAX_STEP_SHARE": 0.21}))
    assert dl.revert(params_path=params, by="Aleks", src=src) == 0
    data = json.loads(params.read_text())
    assert list(data) == ["_note"] and "reverted to defaults by Aleks" in data["_note"]
    assert pm.validate(data) == ({}, [])
    assert "MAX_STEP_SHARE: 0.21 → default 0.18" in capsys.readouterr().out
    assert dl.revert(params_path=tmp_path / "none.json", src=src) == 0 and not (tmp_path / "none.json").exists()


# ------------------------------------------------------------------ run and watch, end to end (the real simulator)

def closed_wave(first_id, start):
    return [duel(n, start=start, status="deal", price=60 + i, result=round((10 + i) * (1 - D) ** 2, 1),
                 msgs=[say(start + 1, "us", 90), say(start + 1, "them", 55), say(start + 2, "us", 70),
                       say(start + 2, "them", 60 + i)]) for i, n in enumerate(range(first_id, first_id + 3))]


def test_run_writes_the_review_and_the_proposal(tmp_path, src):
    f = folder(tmp_path, closed_wave(1, 100) + three(4, 116, live=(6,)))
    out, prop = tmp_path / "intel" / "duel-loop.md", tmp_path / "run" / "proposal.json"
    kw = dict(records=f, params_path=tmp_path / "none.json", n=200, out=out, proposal_path=prop, src=src, quiet=True)
    assert dl.run(dry=True, **kw)["wave"] == "3.1"
    assert not out.exists() and not prop.exists()                   # --dry writes nothing
    p = dl.run(**kw)
    assert p["wave"] == "3.1" and set(p) == {"wave", "label", "made_at", "params", "evidence"}
    assert p["evidence"]["world"] in dl.sim.WORLDS and p["evidence"]["observed"]["deals"] == 3
    assert json.loads(prop.read_text())["wave"] == "3.1"
    for name, value in p["params"].items():
        assert pm.validate({name: value})[1] == []
    dl.run(**kw)                                                     # the same wave again replaces its section
    text = out.read_text()
    assert text.startswith("# Duel loop") and text.count("<!-- wave 3.1 -->") == 1
    assert "| 1 | seller |" in text and "Closest world" in text
    assert dl.run(which="3.2", **kw) is None                         # not closed


def test_watch_handles_each_closed_wave_once(tmp_path, src):
    state = tmp_path / "run" / "state.json"
    kw = dict(params_path=tmp_path / "none.json", n=100, out=tmp_path / "loop.md",
              proposal_path=tmp_path / "proposal.json", src=src)
    recs = closed_wave(1, 100) + three(4, 116, live=(6,))
    line = dl.watch_once(state, records=folder(tmp_path, recs), **kw)
    assert line and "wave 3.1" in line and "closest world" in line
    assert json.loads(state.read_text())["last_wave"] == "3.1"
    assert dl.watch_once(state, records=folder(tmp_path, recs), **kw) is None
    recs = closed_wave(1, 100) + closed_wave(4, 116)
    assert "wave 3.2" in dl.watch_once(state, records=folder(tmp_path, recs), **kw)
