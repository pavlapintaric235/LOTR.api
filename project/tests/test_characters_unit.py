import json
from datetime import datetime

import pytest

from app.api import crud


def test_create_character(test_app, monkeypatch):
    test_request_payload = {
        "name": "Frodo",
        "age": 50,
        "race": "Hobbit",
        "description": "Ring bearer",
    }
    test_response_payload = {
        "id": 1,
        "name": "Frodo",
        "age": 50,
        "race": "Hobbit",
        "description": "Ring bearer",
    }

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/characters/", data=json.dumps(test_request_payload))

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_character_invalid_json(test_app):
    response = test_app.post("/characters/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {},
                "loc": ["body", "name"],
                "msg": "Field required",
                "type": "missing",
            },
            {
                "input": {},
                "loc": ["body", "age"],
                "msg": "Field required",
                "type": "missing",
            },
            {
                "input": {},
                "loc": ["body", "race"],
                "msg": "Field required",
                "type": "missing",
            },
            {
                "input": {},
                "loc": ["body", "description"],
                "msg": "Field required",
                "type": "missing",
            },
        ]
    }

    response = test_app.post("/characters/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"


def test_read_character(test_app, monkeypatch):
    test_data = {
        "id": 1,
        "name": "Frodo",
        "age": 50,
        "race": "Hobbit",
        "description": "Ring bearer",
        "created_at": datetime.utcnow().isoformat(),
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/characters/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_character_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/characters/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Character not found"}


def test_read_all_characters(test_app, monkeypatch):
    test_data = [
        {
            "id": 1,
            "name": "Frodo",
            "age": 50,
            "race": "Hobbit",
            "description": "Ring bearer",
            "created_at": datetime.utcnow().isoformat(),
        },
        {
            "id": 2,
            "name": "Gandalf",
            "age": 2019,
            "race": "Maia",
            "description": "Wizard",
            "created_at": datetime.utcnow().isoformat(),
        },
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/characters/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_characters(test_app, monkeypatch):
    async def mock_get(id):
        return {
            "id": 1,
            "name": "Frodo",
            "age": 50,
            "race": "Hobbit",
            "description": "Ring bearer",
            "created_at": datetime.utcnow().isoformat(),
        }

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/characters/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Frodo",
        "age": 50,
        "race": "Hobbit",
        "description": "Ring bearer",
    }


def test_remove_characters_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/characters/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Character not found"}


def test_update_characters(test_app, monkeypatch):
    test_request_payload = {
        "name": "Frodo",
        "age": 50,
        "race": "Hobbit",
        "description": "Ring bearer",
    }
    test_response_payload = {
        "id": 1,
        "name": "Frodo",
        "age": 50,
        "race": "Hobbit",
        "description": "Ring bearer",
        "created_at": datetime.utcnow().isoformat(),
    }

    async def mock_put(id, payload):
        return test_response_payload

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/characters/1", data=json.dumps(test_request_payload))
    assert response.status_code == 200
    assert response.json() == test_response_payload


VALID_CHARACTER = {
    "name": "Frodo",
    "age": 50,
    "race": "Hobbit",
    "description": "Ring bearer",
}


@pytest.mark.parametrize(
    "character_id, payload, status_code, detail",
    [
        (
            9999,
            VALID_CHARACTER,
            404,
            "Character not found",
        ),
        (
            0,
            VALID_CHARACTER,
            422,
            [
                {
                    "ctx": {"gt": 0},
                    "input": "0",
                    "loc": ["path", "id"],
                    "msg": "Input should be greater than 0",
                    "type": "greater_than",
                }
            ],
        ),
        (
            1,
            {},
            422,
            [
                {
                    "input": {},
                    "loc": ["body", "name"],
                    "msg": "Field required",
                    "type": "missing",
                },
                {
                    "input": {},
                    "loc": ["body", "age"],
                    "msg": "Field required",
                    "type": "missing",
                },
                {
                    "input": {},
                    "loc": ["body", "race"],
                    "msg": "Field required",
                    "type": "missing",
                },
                {
                    "input": {},
                    "loc": ["body", "description"],
                    "msg": "Field required",
                    "type": "missing",
                },
            ],
        ),
        (
            1,
            {"age": 50, "race": "Hobbit", "description": "Ring bearer"},
            422,
            [
                {
                    "input": {
                        "age": 50,
                        "race": "Hobbit",
                        "description": "Ring bearer",
                    },
                    "loc": ["body", "name"],
                    "msg": "Field required",
                    "type": "missing",
                }
            ],
        ),
        (
            1,
            {"name": "Frodo", "race": "Hobbit", "description": "Ring bearer"},
            422,
            [
                {
                    "input": {
                        "name": "Frodo",
                        "race": "Hobbit",
                        "description": "Ring bearer",
                    },
                    "loc": ["body", "age"],
                    "msg": "Field required",
                    "type": "missing",
                }
            ],
        ),
        (
            1,
            {"name": "Frodo", "age": 50, "description": "Ring bearer"},
            422,
            [
                {
                    "input": {
                        "name": "Frodo",
                        "age": 50,
                        "description": "Ring bearer",
                    },
                    "loc": ["body", "race"],
                    "msg": "Field required",
                    "type": "missing",
                }
            ],
        ),
        (
            1,
            {"name": "Frodo", "age": 50, "race": "Hobbit"},
            422,
            [
                {
                    "input": {
                        "name": "Frodo",
                        "age": 50,
                        "race": "Hobbit",
                    },
                    "loc": ["body", "description"],
                    "msg": "Field required",
                    "type": "missing",
                }
            ],
        ),
    ],
    ids=[
        "nonexistent-id",
        "id-zero",
        "empty-body",
        "missing-name",
        "missing-age",
        "missing-race",
        "missing-description",
    ],
)
def test_update_characters_invalid(
    test_app, monkeypatch, character_id, payload, status_code, detail
):
    async def mock_put(id, payload):
        return None

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(f"/characters/{character_id}", data=json.dumps(payload))
    assert response.status_code == status_code
    assert response.json() == {"detail": detail}
