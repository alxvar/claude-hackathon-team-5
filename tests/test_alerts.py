"""Phone alert policy (tools/alerts.py, Chief Sat 17:40). The state file is a tmp one (tests/conftest.py)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import alerts  # noqa: E402

NOW = 1_800_000_000.0


def sink():
    sent = []
    return sent, (lambda *a, **k: sent.append((a, k)))


def test_an_act_goes_to_dani_with_the_offer_and_its_real_expiry():
    sent, n = sink()
    assert alerts.act("SELL SAL-02 to Team 9 at 40 P", 1234, NOW + 600, "body", source="opps", notifier=n, now=NOW)
    (ch, title, body), k = sent[0]
    assert ch == "dani" and title == f"ACT · SELL SAL-02 to Team 9 at 40 P · offer 1234 · until {alerts.hhmm(NOW + 600)}"
    assert not alerts.act("x", 1, NOW - 1, "b", source="opps", notifier=n, now=NOW)   # already expired: never


def test_at_most_4_acts_an_hour_across_senders():
    sent, n = sink()
    for i in range(6):
        alerts.act(f"what {i}", i, NOW + 600, "b", source="opps" if i % 2 else "swaps", notifier=n, now=NOW + i)
    assert len(sent) == alerts.ACT_PER_HOUR
    assert alerts.act("later", 9, NOW + 7200, "b", source="opps", notifier=n, now=NOW + 3601)   # an hour on: again


def test_a_swap_key_sends_once_per_window():
    # 17:40: "LAV-02 for LAT-05 → t07" went out 3x in 12 min: each repost's new offer id beat the 10-min dedupe.
    sent, n = sink()
    for i, oid in enumerate((11, 12, 13)):
        alerts.act("swap LAV-02 for LAT-05 → Team 7", oid, NOW + 900, "b", source="swaps", key="swap:t07:LAV-02:LAT-05",
                   key_every_s=7200, notifier=n, now=NOW + 240 * i)
    assert len(sent) == 1


def test_done_and_void_close_the_loop_once():
    sent, n = sink()
    alerts.act("SELL SAL-02 to Team 9 at 40 P", 1, NOW + 600, "b", source="opps", asset=485, notifier=n, now=NOW)
    alerts.act("BUY LAT-07 from Team 9 at 12 P", 2, NOW + 600, "b", source="opps", want="LAT-07", want_n=0, notifier=n,
               now=NOW)
    alerts.act("SELL MAL-02 to Team 9 at 9 P", 3, NOW + 600, "b", source="opps", asset=61, notifier=n, now=NOW)
    closed = alerts.sweep(open_offer_ids={3}, asset_ids={61}, counts={"LAT-07": 1}, notifier=n, now=NOW + 60)
    assert closed == 2
    titles = [a[1] for a, k in sent[3:]]
    assert titles == ["✓ DONE · SELL SAL-02 to Team 9 at 40 P", "✓ DONE · BUY LAT-07 from Team 9 at 12 P"]
    assert all(k["priority"] == 2 for _, k in sent[3:])
    alerts.sweep(open_offer_ids={3}, asset_ids={61}, counts={}, notifier=n, now=NOW + 120)
    assert len(sent) == 5                                              # once each
    alerts.sweep(open_offer_ids={3}, asset_ids={61}, counts={}, notifier=n, now=NOW + 700)   # 3 still open, expired
    assert sent[-1][0][1] == "✗ VOID · SELL MAL-02 to Team 9 at 9 P"


def test_rivals_are_the_top_6_and_anyone_within_3():
    teams = [{"team": f"t9{i}", "score": 40 - i} for i in range(6)] + [{"team": "t05", "score": 28},
                                                                         {"team": "t03", "score": 27.9},
                                                                         {"team": "t16", "score": 10}]
    assert alerts.rivals(teams) == {f"t9{i}" for i in range(6)} | {"t03"}


def test_critical_goes_to_lucas_only():
    sent, n = sink()
    alerts.critical("CRITICAL duelist tests failed", "red", notifier=n)
    assert [a[0] for a, k in sent] == ["lucas"] and sent[0][1]["priority"] == 5
