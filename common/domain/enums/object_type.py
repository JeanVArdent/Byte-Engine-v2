from enum import Enum, auto

class ObjectType(Enum):
    NONE = auto()
    ACTION = auto()
    PLAYER = auto()
    AVATAR = auto()
    GAMEBOARD = auto()
    VECTOR = auto()
    TILE = auto()
    WALL = auto()
    ITEM = auto()
    OCCUPIABLE = auto()
    STATION = auto()
    OCCUPIABLE_STATION = auto()
    STATION_EXAMPLE = auto()
    STATION_RECEIVER_EXAMPLE = auto()
    OCCUPIABLE_STATION_EXAMPLE = auto()
    GAME_OBJECT_CONTAINER = auto()