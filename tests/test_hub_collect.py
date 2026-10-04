"""Offline tests for the hub's collector and importer helpers (no network, no database)."""
from hub import collect as c
from hub import import_files as imp


def test_poll_follows_the_server_clock():
    assert c.poll_seconds({"paused": True, "tick_seconds": 30}) == 60
    assert c.poll_seconds({"doors": "closed", "tick_seconds": 30}) == 60
    assert c.poll_seconds({"doors": "open", "tick_seconds": 30}) == 10
    assert c.poll_seconds({"doors": "open", "tick_seconds": 15}) == 5
    assert c.poll_seconds({"doors": "open", "tick_seconds": 5}) == 4
    assert c.poll_seconds({}) == 60


def test_board_rows_carry_the_tick_twice():
    row = c.board_row({"id": 1, "maker": "m1", "give": {}, "want": {}, "created_tick": 3, "expires_tick": 9}, "rastro", 5)
    assert row[0] == 1 and row[1] == "rastro" and row[-2:] == (5, 5)
    assert c.SQL_OFFER_BOARD.count("%s") == len(row)


def test_event_and_team_rows_match_their_sql():
    e = {"tick": 4, "payload": {"venue": "rastro", "offer": {"id": 9, "maker": "t03", "to": None, "give": {},
                                                             "want": {}, "created_tick": 4, "expires_tick": 20}}}
    assert c.SQL_OFFER_EVENT.count("%s") == len(c.offer_row_from_event(e))
    lb = {"snapshot_tick": 7, "teams": [{"team": "t01", "score": 3.0, "album_filled": 20}, {"name": "no id"}]}
    rows = c.team_rows(lb)
    assert len(rows) == 1 and c.SQL_TEAM.count("%s") == len(rows[0])


def test_cards_skip_nothing_and_keep_flags():
    rows = c.card_rows({"sets": [{"id": "LAV", "cards": [{"id": "LAV-01", "rarity": "common", "book": 10,
                                                          "page": True, "hidden": False}]}]})
    assert rows == [("LAV-01", "LAV", None, "common", 10, None, None, True, False)]


def test_import_classifies_every_shape_we_have():
    assert imp.classify({"id": 5, "type": "settlement", "payload": {}}) == "event"
    assert imp.classify({"t": 1.0, "tick": 7, "teams": []}) == "leaderboard"          # Lucas
    assert imp.classify({"tick": 7, "t": 2.1, "teams": {"t01": {}}}) == "leaderboard"  # Dani
    assert imp.classify({"t": 1.0, "tick": 7, "cash": 252}) == "me"                   # Lucas
    assert imp.classify({"tick": 7, "neg_points": 3.0}) == "me"                       # Dani
    assert imp.classify({"hello": 1}) == "other"
    assert imp.leaderboard_teams({"teams": {"t01": {"score": 1}}}) == [{"team": "t01", "score": 1}]
    assert imp.leaderboard_teams({"teams": [{"team": "t02"}]}) == [{"team": "t02"}]


def test_import_ids_for_backfilled_settlements():
    s = {"id": -1, "type": "settlement", "payload": {"settlement": 42}}
    assert imp.event_id(s, set()) == -42
    assert imp.event_id(s, {42}) is None                     # already stored under its real id
    assert imp.event_id({"id": -1, "type": "offer.listed", "payload": {}}, set()) is None
    assert imp.event_id({"id": 7, "type": "settlement", "payload": {"settlement": 42}}, {42}) == 7
    assert imp.classify({"id": -1, "type": "settlement", "payload": {}}) == "event"


def test_boards_are_swept_every_two_ticks_and_a_429_ends_the_sweep():
    """Chief 11:40: the per-pass board sweep hit the keyless 60/s limit (11:36-11:39)."""
    import urllib.error
    from hub import collect as c

    class Api:
        def __init__(self, tick):
            self.tick, self.paths = tick, []

        def get(self, path, **q):
            self.paths.append(path)
            if path == "/api/clock":
                return {"tick": self.tick, "doors": "open", "paused": False, "tick_seconds": 15}
            if path == "/api/feed":
                return {"events": []}
            if path.endswith("/offers") and "v02" in path:
                raise urllib.error.HTTPError(path, 429, "slow down", {}, None)
            return {"offers": [], "venues": [], "sets": []}

    class Store:
        def __getattr__(self, name):
            return lambda *a, **k: 0

    class Local:
        max_id = 0

        def append(self, events):
            pass

    col = c.Collector(Api(100), Store(), Local())
    col.venues = ["rastro", "v01", "v02", "v03"]
    col.next_state = col.next_catalog = float("inf")
    boards = lambda api: [p for p in api.paths if p.endswith("/offers")]  # noqa: E731
    col.step()
    assert boards(col.api) == ["/api/venues/rastro/offers", "/api/venues/v01/offers", "/api/venues/v02/offers"]
    for tick, swept in ((100, False), (101, False), (102, True)):
        col.api = Api(tick)
        col.step()
        assert bool(boards(col.api)) == swept, tick
