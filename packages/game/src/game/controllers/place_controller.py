from game.common.enums import *
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.controller import Controller
from game.common.avatar import *


class PlaceController(Controller):
    def __init__(self) -> None:
        super().__init__()

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
        avatar_pos: Vector = client.avatar.position

        pos_mod: Vector

        match action:
            case ActionType.PLACE_ITEM_UP:
                pos_mod = Vector(x=0, y=-1)
            case ActionType.PLACE_ITEM_DOWN:
                pos_mod = Vector(x=0, y=1)
            case ActionType.PLACE_ITEM_LEFT:
                pos_mod = Vector(x=-1, y=0)
            case ActionType.PLACE_ITEM_RIGHT:
                pos_mod = Vector(x=1, y=0)
            case _:
                return

        updated_coords: Vector = avatar_pos.add_x_y(pos_mod.x, pos_mod.y)

        self.__place_item(client, updated_coords, world)

    def __place_item(self, client: Player, updated_coords: Vector, world: GameBoard) -> None:
        if client.avatar.held_item:
            world.place(updated_coords, client.avatar.drop_held_item())
