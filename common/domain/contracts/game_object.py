import uuid
from pydantic import BaseModel, Field


# If you need to create a new instance with modified values
# (since the original instance is immutable), you can use the copy
# method provided by Pydantic.
# This allows you to create a new instance based on the existing
# one with some changes.
# new_user = user.copy(update={"username": "jane_doe"})


class GameObject(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid7()))
    object_type: str
    state: str = "idle"
    class Config:
        frozen = True