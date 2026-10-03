"""Packs and other non-card refs never reach a value lookup (Chief 23:30: the trader logged "unknown_card
sobre_bienvenida" five times, 22:41-22:45, when an offer involved a pack)."""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in ("agents/trader", "tools", "bazaar-kit"):
    sys.path.insert(0, str(ROOT / p))
import bargains  # noqa: E402
import book as bk  # noqa: E402
import matchmaker as mm  # noqa: E402
import policy  # noqa: E402
import reactor  # noqa: E402
import swaps as sw  # noqa: E402

_spec = importlib.util.spec_from_file_location("trader_loop_cards", ROOT / "agents" / "trader" / "loop.py")
loop = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(loop)

PACK = "sobre_bienvenida"


class NoValue:
    """A game whose value endpoint must never be asked: any call fails the test."""

    def value(self, ref):
        raise AssertionError(f"value lookup for {ref}")


def test_is_card():
    assert policy.is_card("RET-09") and policy.is_card("CHA-12")
    for ref in (PACK, "sobre_plata", "RET-9", "ret-09", "", None, 7):
        assert not policy.is_card(ref)


def test_the_trader_skips_offers_that_name_a_pack():
    assert loop.wanted_cards({"cards": [PACK]}) is None
    assert loop.wanted_cards({"cards": ["RET-01", PACK]}) is None
    assert loop.wanted_cards({"types": ["card:RET-01"]}) == ["RET-01"]
    try:
        loop.received_value(NoValue(), [{"ref": PACK, "kind": "pack"}], loop.State())
    except ValueError as e:
        assert PACK in str(e)
    else:
        raise AssertionError("a pack reached received_value")


def test_the_book_swaps_bargains_and_reactor_never_look_a_pack_up():
    assert bk.Book(NoValue(), dry_run=True).value(PACK) is None
    assert sw.Engine(NoValue(), dry_run=True).our_value(PACK, 1) is None
    assert bargains.Watcher(NoValue()).value(PACK) is None
    slept = []
    r = reactor.Reactor(NoValue(), None, sleep=slept.append)
    assert r.value(PACK) is None and slept == []                    # no rate-limit pause spent on it either


def test_a_bid_for_a_pack_is_no_card_bid():
    assert bargains.wanted_card({"assets": [{"ref": PACK}]}) is None
    assert bargains.wanted_card({"cards": ["RET-02"]}) == "RET-02"
    assert reactor.bid_card({"give": {"cash": 70}, "want": {"assets": [{"ref": PACK}]}}) is None


def test_the_matchmaker_ignores_a_pack_want():
    catalog = {"sets": [{"id": "RET", "cards": [{"id": "RET-01", "name": "R1", "rarity": "common", "book": 10}]}]}
    cards = mm.vr.card_index(catalog)
    got = mm.candidates(n={}, last={}, prog={}, pg=mm.pages(catalog), cards=cards,
                        wants=[{"team": "t09", "card": PACK, "max": None}, {"team": "t09", "card": "RET-01", "max": 9}])
    assert list(got) == [("t09", "RET-01")]
