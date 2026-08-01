from fastapi.testclient import TestClient

from main import app

EMPTY = [[None] * 3 for _ in range(3)]

client = TestClient(app)


def test_create_defaults_to_classic() -> None:
    response = client.post("/games")

    assert response.status_code == 201
    assert response.json()["mode"] == "classic"

    state = client.get(f"/games/{response.json()['id']}").json()
    assert state["board"] == EMPTY
    assert state["meta_board"] is None


def test_create_ultimate_nests_the_board() -> None:
    response = client.post("/games", json={"mode": "ultimate"})

    assert response.status_code == 201
    assert response.json()["mode"] == "ultimate"

    state = client.get(f"/games/{response.json()['id']}").json()
    assert state["mode"] == "ultimate"
    assert state["board"][0][0] == EMPTY
    assert state["meta_board"] == EMPTY
    assert state["drawn_boards"] == []
    assert state["active_board"] is None


def test_unknown_mode_is_rejected() -> None:
    assert client.post("/games", json={"mode": "chess"}).status_code == 422
