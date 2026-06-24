from typing import ClassVar, Type, Dict

from pydantic import BaseModel


class TypeRegistry:
    registry: ClassVar[Dict[str, Type[BaseModel]]] = {}
    @classmethod
    def register(cls, tag: str, model: Type[BaseModel]):
        cls.registry[tag] = model
    @classmethod
    def get(cls, tag: str) -> Type[BaseModel]:
        if tag not in cls.registry:
            raise ValueError(f"Unknown tag: {tag}")
        return cls.registry[tag]

def register(tag: str):
    def _decorator(model: Type[BaseModel]):
        TypeRegistry.register(tag, model)
        setattr(model, "object_type", tag)
        return model
    return _decorator