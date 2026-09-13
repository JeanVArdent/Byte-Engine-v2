import unittest

from game.controllers.place_controller import *
from game.controllers.movement_controller import *


class TestPlaceController(unittest.TestCase):
    def setUp(self) -> None:
        self.place_controller: PlaceController = PlaceController()
        self.movement_controller: MovementController = MovementController()

        self.avatar = Avatar(max_inventory_size=1)
        self.item: Item = Item()
        self.avatar.inventory = [self.item]
        self.client: Player = Player(avatar=self.avatar)
        self.avatar.held_item = self.item

        self.locations: dict[tuple[Vector]: list[GameObject]] = {
            Vector(1, 2): [self.avatar],
        }

        self.game_board = GameBoard(0, Vector(4, 4), self.locations, True)
        self.game_board.generate_map()

    def test_place_up(self) -> None:
        self.place_controller.handle_actions(ActionType.PLACE_ITEM_UP, self.client, self.game_board)

        self.assertTrue(isinstance(self.game_board.get_top(Vector(1, 1)), Item))

    def test_place_down(self) -> None:
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.place_controller.handle_actions(ActionType.PLACE_ITEM_DOWN, self.client, self.game_board)

        self.assertTrue(isinstance(self.game_board.get_top(Vector(1, 2)), Item))

    def test_place_left(self) -> None:
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.game_board)
        self.place_controller.handle_actions(ActionType.PLACE_ITEM_LEFT, self.client, self.game_board)

        self.assertTrue(isinstance(self.game_board.get_top(Vector(1, 2)), Item))

    def test_place_right(self) -> None:
        self.place_controller.handle_actions(ActionType.PLACE_ITEM_RIGHT, self.client, self.game_board)

        self.assertTrue(isinstance(self.game_board.get_top(Vector(2, 2)), Item))
