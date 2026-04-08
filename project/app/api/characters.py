from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.models.tortoise import CharacterSchema

from app.models.pydantic import (  # isort: skip
    CharacterPayloadSchema,
    CharacterResponseSchema,
    CharacterUpdatePayloadSchema,
)

router = APIRouter()


@router.post("/", response_model=CharacterResponseSchema, status_code=201)
async def create_character(payload: CharacterPayloadSchema) -> CharacterResponseSchema:
    character_id = await crud.post(payload)

    response_object = {
        "id": character_id,
        "name": payload.name,
        "age": payload.age,
        "race": payload.race,
        "description": payload.description,
        "image": payload.image,
    }
    return response_object


@router.get("/{id}", response_model=CharacterSchema)
async def read_character(id: int = Path(..., gt=0)) -> CharacterSchema:
    character = await crud.get(id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    return character


@router.get("/", response_model=List[CharacterSchema])
async def read_all_characters() -> List[CharacterSchema]:
    return await crud.get_all()


@router.delete("/{id}", response_model=CharacterResponseSchema)
async def delete_character(id: int = Path(..., gt=0)) -> CharacterResponseSchema:
    character = await crud.get(id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    await crud.delete(id)

    return character


@router.put("/{id}", response_model=CharacterSchema)
async def update_character(
    payload: CharacterUpdatePayloadSchema, id: int = Path(..., gt=0)
) -> CharacterSchema:
    character = await crud.put(id, payload)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    return character
