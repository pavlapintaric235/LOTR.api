from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Character(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    age = fields.IntField()
    race = fields.CharField(max_length=255)
    description = fields.TextField()
    image = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.name


CharacterSchema = pydantic_model_creator(Character)
