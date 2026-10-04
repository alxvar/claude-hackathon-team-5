"""tools/eggs.py: rewards grouped by (team, tick, dealer), triggers read from that dealer's echo, Madrid replies."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import eggs  # noqa: E402

_id = [0]


def ev(tick, typ, payload):
    _id[0] += 1
    return {"id": _id[0], "tick": tick, "type": typ, "payload": payload}


def say(tick, dealer, team, text, price=None, thread=1):
    p = {"thread": thread, "kind": "persona", "sender": dealer, "team": team, "text": text}
    if price is not None:
        p["offer"] = {"give": {"assets": [{"ref": "LAT-05"}]}, "want": {"cash": price}}
    return ev(tick, "thread.message", p)


FEED = [
    say(1362, "picaros", "t10", "¡Ay, Monipodio, qué memoria tienes! Mercado de la Cebada, cuatro P."),
    say(1363, "chato", "t10", "Vermut later. Plaza Mayor, con caña — you know Madrid. Here, for your trouble.", 93),
    ev(1363, "egg.found", {"persona": "chato", "team": "t10"}),
    ev(1363, "egg.given", {"team": "t10", "cards": [], "packs": ["sobre_barrio"], "reason": "easter egg"}),
    say(1368, "pilar", "t05", "Sí, un gran señor, muy del barrio."),
    ev(1368, "egg.found", {"persona": "abuela", "team": "t05"}),
    ev(1368, "egg.given", {"team": "t05", "cards": ["MAL-06"], "packs": [], "reason": "easter egg"}),
    say(1368, "abuela", "t05", "¡Ay, cocido madrileño, con sus tres vuelcos! For you, the Puesto, twelve.", 12, 2),
    say(1369, "abuela", "t05", "¡Ay, la verbena de la Paloma! A chotis, cariño — on one tile.", 10, 2),
    ev(1369, "egg.found", {"persona": "abuela", "team": "t05"}),
    ev(1369, "badge.awarded", {"team": "t05", "badge": "Castizo"}),
    ev(1370, "gift.given", {"team": "t05", "cards": ["LAV-04"], "reason": "gift from Abuela Carmen"}),
    say(1400, "abuela", "t09", "Ay, hijo, qué simpático. Toma, una repetida de regalo."),
]


def test_a_reward_is_the_egg_with_what_came_with_it_and_the_dealer_s_own_echo():
    cat = eggs.build(FEED)
    r = {(x["team"], x["tick"]): x for x in cat["rewards"]}
    chato = r[("t10", 1363)]
    assert chato["dealer"] == "chato" and chato["reward"] == "pack sobre_barrio" and "plaza mayor" in chato["words"]
    assert "monipodio" not in chato["words"]                        # the Pícaros' line is someone else's echo
    cocido = r[("t05", 1368)]
    assert cocido["dealer"] == "abuela" and cocido["reward"] == "card MAL-06"
    assert {"cocido", "tres vuelcos"} <= set(cocido["words"])         # not Pilar's same-tick reply
    assert r[("t05", 1369)]["kinds"] == ["badge Castizo"] and "chotis" in r[("t05", 1369)]["words"]
    assert cat["gifts"] == {"t05": 1}


def test_madrid_replies_say_what_followed():
    refs = {(x["team"], x["tick"]): x for x in eggs.build(FEED)["refs"]}
    assert refs[("t05", 1368)]["after"][0] == "card MAL-06"           # then what the next ticks brought
    after = refs[("t05", 1369)]["after"]
    assert "badge Castizo" in after and "card LAV-04" in after and "price 12 → 10" in after
    assert ("t09", 1400) not in refs                                 # "repetida" is no Madrid reference


def test_the_page_marks_what_we_have_and_what_we_lack():
    text = eggs.render(eggs.build(FEED), me="t05")
    assert "| El Chato | pack sobre_barrio | " in text and "| t10 | **no** |" in text
    assert "| Abuela Carmen | badge Castizo |" in text
    chato = text.split("**El Chato**")[1].split("**Los Pícaros**")[0]
    assert "confirmed for t10; **we don't**" in chato
    abuela = text.split("**Abuela Carmen**")[1].split("**El Chato**")[0]
    assert "the Castizo badge" in abuela and "confirmed for t05; we have it" in abuela


def test_madrid_words_are_matched_without_accents_and_not_inside_other_words():
    assert eggs.refs("Plaza Mayor, con caña") == ["con cana", "plaza mayor"]
    assert eggs.refs("una repetida, cariño") == []
    assert "chotis" in eggs.refs("A CHOTIS on one tile") and "moscu" in eggs.refs("el oro de Moscú")
