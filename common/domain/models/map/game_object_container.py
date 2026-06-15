from typing import List

from pydantic import BaseModel, field_validator, TypeAdapter

from common.domain.contracts.game_object import GameObject
from common.domain.type_registry import TypeRegistry


class GameObjectContainer(BaseModel):
    GameObjects: List[GameObject]
    class Config:
        frozen = True

    @field_validator('GameObjects', mode="before")
    @classmethod
    def dispatch_game_objects(cls, value):
        out = []
        for obj in value:
            tag = obj.get("object_type")
            if not tag:
                raise ValueError("Missing object_type")
            model = TypeRegistry.get(tag)
            out.append(TypeAdapter(model).validate_python(obj))