"""Dealer-hint miner (tools/hints.py): feed events in, hits out; no network."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import hints  # noqa: E402


def msg(eid, tick, sender, team, text):
    return {"id": eid, "tick": tick, "type": "thread.message",
            "payload": {"sender": sender, "team": team, "text": text, "kind": "persona"}}


PILAR = "Let us be civilised: {} P. They say only one golden chulapa was ever printed. Carmen at El Rastro knows the story; ask her about the golden chulapa."


def test_dealer_hints_found_and_folded_flavour_and_team_lines_ignored():
    events = [msg(1, 512, "pilar", "t05", PILAR.format(16)), msg(2, 637, "pilar", "t16", PILAR.format(23)),
              msg(3, 68, "abuela", "t07", "Look, 5 P. My grandchildren would pay more!"),
              msg(4, 132, "abuela", "t02", "Ay, cariño, five P. No secrets at this table!"),
              msg(5, 900, "t05", "t05", "Tell me about the golden chulapa"),
              msg(6, 407, "abuela", "t04", "Ay, la chulapa dorada... solo se imprimió una. Pregúntale por el oro de Moscú, él sabrá."),
              {"id": 7, "tick": 1021, "type": "egg.given", "actor": "banco",
               "payload": {"team": "t02", "cards": ["LAT-13"], "reason": "easter egg"}}]
    hits, seen = hints.scan_events(events)
    assert [(h["kind"], h["dealer"], h["first"]) for h in hits] == [("message", "pilar", 512), ("message", "abuela", 407),
                                                                    ("egg.given", "banco", 1021)]
    assert hits[0]["count"] == 2 and hits[0]["teams"] == ["t05", "t16"] and hits[0]["last"] == 637
    again, _ = hints.scan_events([msg(8, 700, "pilar", "t01", PILAR.format(19))], seen)
    assert again == [] and seen[next(k for k in seen if k.startswith("pilar"))]["count"] == 3


def test_catalog_hidden_cards_and_minted_changes():
    cat0 = {"sets": [{"cards": [{"id": "LAT-12", "rarity": "legendary", "minted": 0}, {"id": "LAT-01", "rarity": "common", "minted": 9}]}]}
    _, snap = hints.scan_catalog(cat0, {})
    cat1 = {"sets": [{"cards": [{"id": "LAT-12", "rarity": "legendary", "minted": 1}, {"id": "LAT-01", "rarity": "common", "minted": 12},
                                {"id": "LAT-13", "rarity": "legendary", "hidden": True, "minted": 1, "print_run": 1}]}]}
    new, _ = hints.scan_catalog(cat1, snap)
    assert sorted(h["kind"] + ":" + h["card"] for h in new) == ["catalog.minted:LAT-12", "catalog.new_card:LAT-13"]


def test_the_feed_is_read_incrementally(tmp_path):
    feed = tmp_path / "feed.jsonl"
    feed.write_text(json.dumps(msg(1, 512, "pilar", "t05", PILAR.format(16))) + "\n")
    m = hints.Miner(None, feed=feed, news=tmp_path / "none.md", out=tmp_path / "h.md", state=tmp_path / "s.json",
                    log=lambda s: None)
    assert len(m.run_once()) == 1
    with feed.open("a") as f:
        f.write(json.dumps(msg(2, 1021, "banco", "t02", "El oro de Moscú. So you know the story — very few do.")) + "\n")
        f.write('{"half": ')                                            # a half-written line: next run
    hits = hints.Miner(None, feed=feed, news=tmp_path / "none.md", out=tmp_path / "h.md", state=tmp_path / "s.json",
                       log=lambda s: None).run_once()
    assert [h["dealer"] for h in hits] == ["banco"]
    assert "banco" in (tmp_path / "h.md").read_text()



def test_the_keepers_answer_to_an_egg_team_is_always_a_hit():
    # Sat 19:20: Don Ernesto's "The gold of Moscow — an old story, and not mine today" matched no pattern.
    events = [{"id": 1, "tick": 1074, "type": "egg.found", "payload": {"persona": "abuela", "team": "t18"}},
              msg(2, 1080, "banco", "t18", "Buenas. Carmen talks, as always. Terms: El Ahuehuete, 761 P."),
              msg(9, 1080, "banco", "t18", "Ciento trece, señor. I said the number twice."),             # haggling: out
              msg(3, 1081, "banco", "t08", "Terms: La Casa Encendida, 113 P."),
              msg(4, 1082, "banco", "t05", "The gold of Moscow — an old story, and not mine today.")]
    hits, seen = hints.scan_events(events)
    assert [(h["kind"], h["dealer"], h["teams"]) for h in hits] == [("egg.found", "abuela", ["t18"]),
                                                                    ("message", "banco", ["t18"]),
                                                                    ("message", "banco", ["t05"])]
    later, _ = hints.scan_events([msg(5, 1090, "banco", "t18", "Carmen sends you? Then the vault opens.")], seen)
    assert later and later[0]["teams"] == ["t18"]                    # the egg teams survive across runs
