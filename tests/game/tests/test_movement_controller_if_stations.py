import unittest

from game.common.game_object import GameObject
from game.controllers.movement_controller import MovementController
from game.common.map.game_board import GameBoard
from game.common.stations.station import Station
from game.utils.vector import Vector
from game.common.player import Player
from game.common.avatar import Avatar
from game.common.action import ActionType
import game.test_suite.utils

class TestMovementControllerIfStations(unittest.TestCase):
    """
    `Test Movement Controller with Stations Notes:`

        This class tests the different methods in the Movement Controller and that the Avatar can't move onto a Station
        object (an example of an impassable object).
    """

    def setUp(self) -> None:
        self.movement_controller = MovementController()
        self.avatar = Avatar(Vector(2, 2), 1)

        self.locations: dict[Vector: list[GameObject]] = {
            Vector(1, 0): [Station(None)],
            Vector(2, 0): [Station(None)],
            Vector(0, 1): [Station(None)],
            Vector(0, 2): [Station(None)],
            Vector(1, 3): [Station(None)],
            Vector(2, 3): [Station(None)],
            Vector(3, 1): [Station(None)],
            Vector(3, 2): [Station(None)],
            Vector(2, 2): [self.avatar]
        }

        self.game_board = GameBoard(0, Vector(4, 4), self.locations, False)
        # test movements up, down, left and right by starting with default 3,3 then know if it changes from there \/
        self.client = Player(None, None, [], self.avatar)
        self.game_board.generate_map()
        self.utils = game.test_suite.utils

    def test_move_up_fail(self):
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.assertTrue(self.utils.spell_check(str(self.client.avatar.position), str(Vector(2, 1)), False))

    def test_move_down(self):
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(2, 2)))

    def test_move_down_fail(self):
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.assertTrue(self.utils.spell_check(str(self.client.avatar.position), str(Vector(2, 2)), False))

    def test_move_left(self):
        self.movement_controller.handle_actions(ActionType.MOVE_LEFT, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(1, 2)))

    def test_move_left_fail(self):
        self.movement_controller.handle_actions(ActionType.MOVE_LEFT, self.client, self.game_board)
        self.movement_controller.handle_actions(ActionType.MOVE_LEFT, self.client, self.game_board)
        self.assertTrue(self.utils.spell_check(str(self.client.avatar.position), str(Vector(1, 2)), False))

    def test_move_right(self):
        self.movement_controller.handle_actions(ActionType.MOVE_LEFT, self.client, self.game_board)
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(2, 2)))

    def test_move_right_fail(self):
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.game_board)
        self.assertTrue(self.utils.spell_check(str(self.client.avatar.position), str(Vector(2, 2)), False))
