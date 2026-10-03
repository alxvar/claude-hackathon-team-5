"""Offline tests for agents/dealers/narrator.py: the guard, the fallbacks, the flag. No network, no API calls."""
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "agents" / "dealers"))
import narrator  # noqa: E402


def events():
    out = []
    return out, out.append


def test_the_guard_wants_our_exact_price_once_and_no_other_number():
    assert narrator.guard("Hola, Abuela! Could you do 57 P?", 57) is None
    assert narrator.guard("Gracias, Chato. ¿Qué tal 63 P por el Alfonso XII?", 63) is None   # roman numerals are fine
    assert narrator.guard("Could you do 58 P?", 57)                       # wrong price
    assert narrator.guard("What a lovely stall, Abuela!", 57)             # no price
    assert narrator.guard("57 P for the RET-10 card?", 57)                # another number
    assert narrator.guard("57 P? Yes, 57 P.", 57)                         # twice
    assert narrator.guard("57 P, my final offer.", 57)                    # pressure
    assert narrator.guard("57 P o nada, es mi última oferta.", 57)        # pressure, in Spanish
    assert narrator.guard("x" * 400 + " 57 P", 57)                        # too long


def test_a_timeout_falls_back_to_the_template(monkeypatch):
    async def slow(system, user):
        await asyncio.sleep(10)
    monkeypatch.setattr(narrator, "_ask", slow)
    monkeypatch.setattr(narrator, "TIMEOUT_S", 0.05)
    log, put = events()
    text = narrator.say_text("chato", "buy", "a card from the RET set", 63, "You move, I move. 97 P.", 2, log=put)
    assert text == narrator.template("chato", "buy", 63, 2) and "63 P" in text
    assert log[0]["ok"] is False and "Timeout" in log[0]["why"]


def test_no_credentials_or_no_sdk_falls_back_too(monkeypatch):
    async def broken(system, user):
        raise ModuleNotFoundError("No module named 'anthropic'")
    monkeypatch.setattr(narrator, "_ask", broken)
    assert narrator.say_text("abuela", "sell", "a spare card", 24) == narrator.template("abuela", "sell", 24, 0)


def test_a_good_line_goes_out_and_its_cost_is_logged(monkeypatch):
    async def good(system, user):
        assert "Our price in this message: 57 P" in user and "Dealer: Abuela" in user
        return "Hola, Abuela! What a lovely stall. Could you do 57 P?", 0.0006, 2.8
    monkeypatch.setattr(narrator, "_ask", good)
    log, put = events()
    assert narrator.say_text("abuela", "buy", "a card", 57, log=put) == "Hola, Abuela! What a lovely stall. Could you do 57 P?"
    assert log[0]["ok"] is True and log[0]["cost_usd"] == 0.0006


def test_off_means_templates_and_no_model_call(monkeypatch):
    async def never(system, user):
        raise AssertionError("called the model with the narrator off")
    monkeypatch.setattr(narrator, "_ask", never)
    assert narrator.say_text("abuela", "buy", "a card", 57, enabled=False) == narrator.template("abuela", "buy", 57, 0)


def test_every_template_passes_the_guard():
    for side in ("buy", "sell"):
        for turn in range(len(narrator.TEMPLATES[side])):
            for dealer in ("abuela", "chato"):
                assert narrator.guard(narrator.template(dealer, side, 42, turn), 42) is None
