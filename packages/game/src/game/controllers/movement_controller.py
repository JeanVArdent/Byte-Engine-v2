from game.common.player import Player
from game.common.map.game_board import GameBoard
from game.common.enums import *
from game.utils.vector import Vector
from game.controllers.controller import Controller


class MovementController(Controller):
    """
    `Movement Controller Notes:`

        The Movement Controller manages the movement actions the player tries to execute. Players can move up, down,
        left, and right. If the player tries to move into a space that's impassable, they don't move.

        For example, if the player attempts to move into an Occupiable Station (something the player can be on) that is
        occupied by a Wall object (something the player can't be on), the player doesn't move; that is, if the player
        tries to move into anything that can't be occupied by something, they won't move.
    """

    def __init__(self):
        super().__init__()

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
        avatar_pos: Vector = Vector(client.avatar.position.x, client.avatar.position.y)

        pos_mod: Vector

        match action:
            case ActionType.MOVE_UP:
                pos_mod = Vector(x=0, y=-1)
            case ActionType.MOVE_DOWN:
                pos_mod = Vector(x=0, y=1)
            case ActionType.MOVE_LEFT:
                pos_mod = Vector(x=-1, y=0)
            case ActionType.MOVE_RIGHT:
                pos_mod = Vector(x=1, y=0)
            case _:  # default case
                return

        temp_vec: Vector = avatar_pos.add_to_vector(pos_mod)

        # if the top of the given coordinates are not occupiable or are invalid, return to do nothing
        if not world.is_occupiable(temp_vec):
            return

        # remove the avatar from its previous location
        world.remove(client.avatar.position, ObjectType.AVATAR)

        # add the avatar to the top of the list of the coordinate
        world.place(temp_vec, client.avatar)

        # reassign the avatar's position
        client.avatar.position = Vector(temp_vec.x, temp_vec.y)
