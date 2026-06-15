from typing import List

from pydantic import BaseModel, field_validator, TypeAdapter

from common.domain.contracts.game_object import GameObject
from common.domain.type_registry import TypeRegistry


# If this doesn't work, we should try the solution proposed by tkellogg
# github.com/pydantic/pydantic/discussions/3091

class GameObjectContainer(BaseModel, frozen=True):
    GameObjects: List[GameObject]

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
        return out