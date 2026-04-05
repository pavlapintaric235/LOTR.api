from pydantic import BaseModel


class CharacterPayloadSchema(BaseModel):
    name: str
    age: int
    race: str
    description: str


class CharacterResponseSchema(CharacterPayloadSchema):
    id: int


class CharacterUpdatePayloadSchema(CharacterPayloadSchema):
    pass
