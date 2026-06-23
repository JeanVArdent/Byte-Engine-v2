import unittest

from game.common.action import ActionType
from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.map.wall import Wall
from game.common.player import Player
from game.common.stations.occupiable_station import OccupiableStation
from game.controllers.movement_controller import MovementController
from game.utils.vector import Vector
import game.test_suite.utils

class TestMovementControllerIfOccupiableStations(unittest.TestCase):
    """
    `Test Movement Controller with Occupiable Stations that are Occupied Notes:`

        This class tests the different methods in the Movement Controller and that the Avatar can't move onto an
        Occupiable Station that is occupied by an unoccupiable object (e.g., a Wall or Station object).
    """

    def setUp(self) -> None:
        self.movement_controller = MovementController()

        self.avatar = Avatar(None, 10)

        self.locations: dict[Vector, list[GameObject]] = { 
            Vector(1, 0): [OccupiableStation(None), Wall()],
            Vector(2, 0): [OccupiableStation(None), Wall()],
            Vector(0, 1): [OccupiableStation(None), Wall()],
            Vector(0, 2): [OccupiableStation(None), Wall()],
            Vector(1, 3): [OccupiableStation(None), Wall()],
            Vector(2, 3): [OccupiableStation(None), Wall()],
            Vector(3, 1): [OccupiableStation(None), Wall()],
            Vector(3, 0): [OccupiableStation(None), Wall()],
            Vector(2, 2): [self.avatar]
        }

        self.game_board = GameBoard(0, Vector(4, 4), self.locations, False)
        self.occ_station = OccupiableStation()
        # self.wall = Wall()
        # test movements up, down, left and right by starting with default 4, 4 then know if it changes from there \/

        self.position = Vector(2, 2)
        self.client = Player(None, None, [], self.avatar)
        self.game_board.generate_map()
        self.utils = game.test_suite.utils
    # it is not occupied, so you can move there

    def test_move_up(self):
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.assertEqual(self.client.avatar.position, Vector(2, 1))

    def test_move_up_fail(self):
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.assertEqual(self.client.avatar.position, Vector(2, 1))

    def test_move_down(self):
        self.movement_controller.handle_actions(ActionType.MOVE_UP, self.client, self.game_board)
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.assertEqual(self.client.avatar.position, Vector(2, 2))

    def test_move_down_fail(self):
        self.movement_controller.handle_actions(ActionType.MOVE_DOWN, self.client, self.game_board)
        self.assertEqual(self.client.avatar.position, Vector(2, 2))

    def test_move_left(self):
        self.movement_controller.handle_actions(ActionType.MOVE_LEFT, self.client, self.game_board)
        self.assertEqual(self.client.avatar.position, Vector(1, 2))

    def test_move_left_fail(self):
        self.movement_controller.handle_actions(ActionType.MOVE_LEFT, self.client, self.game_board)
        self.movement_controller.handle_actions(ActionType.MOVE_LEFT, self.client, self.game_board)
        self.assertEqual(self.client.avatar.position, Vector(1, 2))

    def test_move_right(self):
        self.movement_controller.handle_actions(ActionType.MOVE_LEFT, self.client, self.game_board)
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.game_board)
        self.assertEqual(self.client.avatar.position, Vector(2, 2))

    def test_move_right_fail(self):
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.game_board)
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.client, self.game_board)
        self.assertEqual(self.client.avatar.position, Vector(3, 2))
