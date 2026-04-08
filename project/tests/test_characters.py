import json

import pytest


def test_create_character(test_app_with_db):
    response = test_app_with_db.post(
        "/characters/",
        data=json.dumps(
            {
                "name": "Frodo",
                "age": 50,
                "race": "Hobbit",
                "description": "Ring bearer",
                "image_url": "https://example.com/images/frodo.jpg",
            }
        ),
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Frodo"
    assert response.json()["age"] == 50
    assert response.json()["race"] == "Hobbit"
    assert response.json()["description"] == "Ring bearer"
    assert response.json()["image_url"] == "https://example.com/images/frodo.jpg"


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
            {
                "input": {},
                "loc": ["body", "image_url"],
                "msg": "Field required",
                "type": "missing",
            },
        ]
    }


def test_create_character_invalid_age_type(test_app):
    response = test_app.post(
        "/characters/",
        data=json.dumps(
            {
                "name": "Frodo",
                "age": "fifty",
                "race": "Hobbit",
                "description": "Ring bearer",
                "image_url": "https://example.com/images/frodo.jpg",
            },
        ),
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "age"]


def test_read_character(test_app_with_db):
    response = test_app_with_db.post(
        "/characters/",
        data=json.dumps(
            {
                "name": "Frodo",
                "age": 50,
                "race": "Hobbit",
                "description": "Ring bearer",
                "image_url": "https://example.com/images/frodo.jpg",
            }
        ),
    )
    character_id = response.json()["id"]

    response = test_app_with_db.get(f"/characters/{character_id}")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == character_id
    assert response_dict["name"] == "Frodo"
    assert response_dict["age"] == 50
    assert response_dict["race"] == "Hobbit"
    assert response_dict["description"] == "Ring bearer"
    assert response_dict["image_url"] == "https://example.com/images/frodo.jpg"


def test_read_character_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/characters/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Character not found"

    response = test_app_with_db.get("/characters/0")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {"gt": 0},
                "input": "0",
                "loc": ["path", "id"],
                "msg": "Input should be greater than 0",
                "type": "greater_than",
            }
        ]
    }


def test_read_all_characters(test_app_with_db):
    response = test_app_with_db.post(
        "/characters/",
        data=json.dumps(
            {
                "name": "Frodo",
                "age": 50,
                "race": "Hobbit",
                "description": "Ring bearer",
                "image_url": "https://example.com/images/frodo.jpg",
            }
        ),
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.get("/characters/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda x: x["id"] == summary_id, response_list))) == 1


def test_remove_characters(test_app_with_db):
    response = test_app_with_db.post(
        "/characters/",
        data=json.dumps(
            {
                "name": "Frodo",
                "age": 50,
                "race": "Hobbit",
                "description": "Ring bearer",
                "image_url": "https://example.com/images/frodo.jpg",
            }
        ),
    )
    character_id = response.json()["id"]

    response = test_app_with_db.delete(f"/characters/{character_id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": character_id,
        "name": "Frodo",
        "age": 50,
        "race": "Hobbit",
        "description": "Ring bearer",
        "image_url": "https://example.com/images/frodo.jpg",
    }


def test_remove_characters_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/characters/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Character not found"}

    response = test_app_with_db.delete("/characters/0")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {"gt": 0},
                "input": "0",
                "loc": ["path", "id"],
                "msg": "Input should be greater than 0",
                "type": "greater_than",
            }
        ]
    }


def test_update_characters(test_app_with_db):
    response = test_app_with_db.post(
        "/characters/",
        data=json.dumps(
            {
                "name": "Frodo",
                "age": 50,
                "race": "Hobbit",
                "description": "Ring bearer",
                "image_url": "https://example.com/images/frodo.jpg",
            }
        ),
    )
    character_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/characters/{character_id}",
        data=json.dumps(
            {
                "name": "Frodo",
                "age": 50,
                "race": "Hobbit",
                "description": "Ring bearer",
                "image_url": "https://example.com/images/frodo.jpg",
            }
        ),
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == character_id
    assert response_dict["name"] == "Frodo"
    assert response_dict["age"] == 50
    assert response_dict["race"] == "Hobbit"
    assert response_dict["description"] == "Ring bearer"
    assert response_dict["image_url"] == "https://example.com/images/frodo.jpg"
    assert response_dict["created_at"]


VALID_CHARACTER = {
    "name": "Frodo",
    "age": 50,
    "race": "Hobbit",
    "description": "Ring bearer",
    "image_url": "https://example.com/images/frodo.jpg",
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
                {
                    "input": {},
                    "loc": ["body", "image_url"],
                    "msg": "Field required",
                    "type": "missing",
                },
            ],
        ),
        (
            1,
            {
                "age": 50,
                "race": "Hobbit",
                "description": "Ring bearer",
                "image_url": "https://example.com/images/frodo.jpg",
            },
            422,
            [
                {
                    "input": {
                        "age": 50,
                        "race": "Hobbit",
                        "description": "Ring bearer",
                        "image_url": "https://example.com/images/frodo.jpg",
                    },
                    "loc": ["body", "name"],
                    "msg": "Field required",
                    "type": "missing",
                }
            ],
        ),
        (
            1,
            {
                "name": "Frodo",
                "race": "Hobbit",
                "description": "Ring bearer",
                "image_url": "https://example.com/images/frodo.jpg",
            },
            422,
            [
                {
                    "input": {
                        "name": "Frodo",
                        "race": "Hobbit",
                        "description": "Ring bearer",
                        "image_url": "https://example.com/images/frodo.jpg",
                    },
                    "loc": ["body", "age"],
                    "msg": "Field required",
                    "type": "missing",
                }
            ],
        ),
        (
            1,
            {
                "name": "Frodo",
                "age": 50,
                "description": "Ring bearer",
                "image_url": "https://example.com/images/frodo.jpg",
            },
            422,
            [
                {
                    "input": {
                        "name": "Frodo",
                        "age": 50,
                        "description": "Ring bearer",
                        "image_url": "https://example.com/images/frodo.jpg",
                    },
                    "loc": ["body", "race"],
                    "msg": "Field required",
                    "type": "missing",
                }
            ],
        ),
        (
            1,
            {
                "name": "Frodo",
                "age": 50,
                "race": "Hobbit",
                "image_url": "https://example.com/images/frodo.jpg",
            },
            422,
            [
                {
                    "input": {
                        "name": "Frodo",
                        "age": 50,
                        "race": "Hobbit",
                        "image_url": "https://example.com/images/frodo.jpg",
                    },
                    "loc": ["body", "description"],
                    "msg": "Field required",
                    "type": "missing",
                },
            ],
        ),
        (
            1,
            {
                "name": "Frodo",
                "age": 50,
                "race": "Hobbit",
                "description": "Ring bearer",
            },
            422,
            [
                {
                    "input": {
                        "name": "Frodo",
                        "age": 50,
                        "race": "Hobbit",
                        "description": "Ring bearer",
                    },
                    "loc": ["body", "image_url"],
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
        "missing-image_url",
    ],
)
def test_update_characters_invalid(
    test_app_with_db, character_id, payload, status_code, detail
):
    test_app_with_db.post("/characters/", data=json.dumps(VALID_CHARACTER))

    response = test_app_with_db.put(
        f"/characters/{character_id}",
        data=json.dumps(payload),
    )

    assert response.status_code == status_code
    assert response.json()["detail"] == detail
