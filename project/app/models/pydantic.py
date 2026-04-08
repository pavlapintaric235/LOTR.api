from pydantic import BaseModel, HttpUrl


class CharacterPayloadSchema(BaseModel):
    name: str
    age: int
    race: str
    description: str
    image_url: HttpUrl


class CharacterResponseSchema(CharacterPayloadSchema):
    id: int


class CharacterUpdatePayloadSchema(CharacterPayloadSchema):
    pass
