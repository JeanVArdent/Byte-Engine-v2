from common.domain.contracts.game_object import GameObject
from common.domain.type_registry import register


@register("Wall")
class Wall(GameObject):
    pass