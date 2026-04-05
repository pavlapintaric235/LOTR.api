from typing import List, Union

from app.models.pydantic import CharacterPayloadSchema, CharacterUpdatePayloadSchema
from app.models.tortoise import Character


async def post(payload: CharacterPayloadSchema) -> int:
    character = Character(
        name=payload.name,
        age=payload.age,
        race=payload.race,
        description=payload.description,
    )
    await character.save()
    return character.id


async def get(id: int) -> Union[dict, None]:
    character = await Character.filter(id=id).values(
        "id",
        "name",
        "age",
        "race",
        "description",
        "created_at",
    )
    return character[0] if character else None


async def get_all() -> List[dict]:
    characters = await Character.all().values(
        "id",
        "name",
        "age",
        "race",
        "description",
        "created_at",
    )
    return characters


async def delete(id: int) -> int:
    character = await Character.filter(id=id).first()

    if character:
        return await character.delete()

    return 0


async def put(id: int, payload: CharacterUpdatePayloadSchema) -> Union[dict, None]:
    character = await Character.filter(id=id).update(
        name=payload.name,
        age=payload.age,
        race=payload.race,
        description=payload.description,
    )
    if character:
        update_character = await Character.filter(id=id).values(
            "id",
            "name",
            "age",
            "race",
            "description",
            "created_at",
        )
        return update_character[0] if update_character else None
    return None
