"""Offline tests for tools/news.py: fake news API, no network, no notifications sent."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "bazaar-kit"))
import news  # noqa: E402

SETS = {"SAL": "Salamanca", "RET": "El Retiro", "CHA": "Chamberí", "LAV": "Lavapiés"}
VENUES = {"v07": "Mercado del 10", "v10": "Puesto de Team 5", "rastro": "El Rastro"}   # the house is listed too
NOISE = [{"id": 1, "tick": 283, "at_hours": 3.68, "source": "boletin", "source_name": "Boletín del Bazar",
          "headline": "Radio Rastro is on the air",
          "body": "News, rumours and what you hear between the stalls. Believe what you like."},
         {"id": 2, "tick": 331, "at_hours": 4.08, "source": "radio", "source_name": "Radio Rastro",
          "headline": "Atleti win 2-1 and Madrid goes out to celebrate", "body": "Car horns on Gran Vía until late."}]


class Pub:
    def __init__(self, items):
        self.items = items

    def _call(self, method, path, *a, **k):
        if path == "/api/news":
            return {"news": list(reversed(self.items))}               # newest first, as the server sends it
        if path == "/api/catalog":
            return {"sets": [{"id": k, "name": v} for k, v in SETS.items()]}
        if path == "/api/venues":
            return {"venues": [{"venue": k, "name": v} for k, v in VENUES.items()]}
        raise AssertionError(path)


def test_the_first_two_items_are_noise():
    for n in NOISE:
        assert news.names(f"{n['headline']} {n['body']}", SETS, VENUES) == []


def test_items_that_name_what_we_trade():
    got = news.names("Doña Pilar se queda sin RET-11: el precio de los sobres sube a 40 P en El Rastro", SETS, VENUES)
    assert {"dealer dona pilar", "dealer pilar", "card RET-11", "price", "venue rastro", "event precio"} <= set(got)
    assert "set CHA" in news.names("Rumour: Chamberí cards arrive tonight", SETS, VENUES)
    assert "venue v07" in news.names("Mercado del 10 drops its fee", SETS, VENUES)


def test_poll_writes_every_item_once_and_pages_only_the_relevant(tmp_path):
    items = list(NOISE)
    sent, logged = [], []
    w = news.Watcher(Pub(items), out=tmp_path / "news.md", state=tmp_path / "s.json",
                     notifier=lambda *a, **k: sent.append(a), log=logged.append)
    assert [n["id"] for n in w.poll()] == [1, 2] and sent == []
    items.append({"id": 3, "tick": 340, "at_hours": 4.2, "source": "tablon", "source_name": "Tablón",
                  "headline": "El Chato sells SAL-09 at half price next hour", "body": "Or so they say."})
    assert [n["id"] for n in w.poll()] == [3] and w.poll() == []
    text = (tmp_path / "news.md").read_text()
    assert text.startswith("# Radio Rastro") and text.count("\n- ") == 3 and "Names: none" in text
    assert sent == [] and any("SAL-09" in x for x in logged)          # Chief 17:40: no push, logged and relayed
    assert any(line.startswith("NEWS #3 [tablon]") for line in logged)


def test_dry_writes_nothing(tmp_path):
    w = news.Watcher(Pub(NOISE), out=tmp_path / "news.md", state=tmp_path / "s.json", notifier=None,
                     log=lambda *a: None, dry=True)
    assert len(w.poll()) == 2 and not (tmp_path / "news.md").exists() and not (tmp_path / "s.json").exists()
