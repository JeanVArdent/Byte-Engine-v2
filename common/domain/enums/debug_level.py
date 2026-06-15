from enum import Enum, auto

class DebugLevel(Enum):
    NONE = auto()
    CLIENT = auto()
    CONTROLLER = auto()
    ENGINE = auto()