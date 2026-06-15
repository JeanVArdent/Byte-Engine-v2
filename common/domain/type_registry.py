from typing import ClassVar, Type, Dict

from pydantic import BaseModel


class TypeRegistry:
    registry: ClassVar[Dict[str, Type[BaseModel]]] = {}
    @classmethod
    def register(cls, tag: str, model: Type[BaseModel]):
        cls.registry[tag] = model
    @classmethod
    def get(cls, tag: str) -> Type[BaseModel]:
        return cls.registry[tag]

def register(tag: str):
    def _decorator(model: Type[BaseModel]):
        TypeRegistry.register(tag, model)
        return model
    return _decorator