import unittest

from game.common.action import ActionType
from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.common.stations.occupiable_station import OccupiableStation
from game.controllers.movement_controller import MovementController
from game.utils.vector import Vector


class TestMovementControllerIfOccupiableStationIsOccupiable(unittest.TestCase):
    """
    `Test Movement Controller if Occupiable Stations are Occupiable Notes:`

        This class tests the different methods in the Movement Controller class and the Avatar moving onto Occupiable
        Stations so that the Avatar can occupy it.
    """

    def setUp(self) -> None:
        self.movement_controller = MovementController()

        self.avatar = Avatar(None, 1)

        self.locations: dict[Vector, list[GameObject]] = {
            Vector(1, 0): [OccupiableStation(None)],
            Vector(2, 0): [OccupiableStation(None)],
            Vector(0, 1): [OccupiableStation(None)],
            Vector(0, 2): [OccupiableStation(None)],
            Vector(1, 1): [self.avatar],
        }

        self.game_board = GameBoard(0, Vector(3, 3), self.locations, False)
        self.occ_station = OccupiableStation()

        # test movements up, down, left and right by starting with default 3,3 then know if it changes from there
        self.client = Player(None, None, [], self.avatar)
        self.game_board.generate_map()

    def test_move_up(self):
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(1, 0)))

    def test_move_down(self):
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(1, 2)))

    def test_move_left(self):
        self.movement_controller.handle_actions(ActionType.MOVE_LEFT, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(0, 1)))

    def test_move_right(self):
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.game_board)
        self.assertEqual((str(self.client.avatar.position)), str(Vector(2, 1)))
