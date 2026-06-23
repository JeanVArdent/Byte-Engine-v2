import unittest

from game.common.enums import ObjectType
from game.common.avatar import Avatar
from game.common.items.item import Item
from game.common.stations.station import Station
from game.common.stations.occupiable_station import OccupiableStation
from game.common.map.wall import Wall
from game.utils.vector import Vector
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
import game.test_suite.utils


class TestGameBoard(unittest.TestCase):
    """
    `Test Gameboard Without Generation Notes:`

        This class tests the different methods in the Gameboard class when the map is *not* generated.
    """
    """
    `Test Avatar Notes:`

        This class tests the different methods in the Avatar class.
    """

    def setUp(self) -> None:
        self.item: Item = Item(10, None)
        self.wall: Wall = Wall()
        self.avatar: Avatar = Avatar(Vector(5, 5))
        self.locations: dict[Vector, list[GameObject]] = {
            Vector(1, 1): [Station(None)],
            Vector(1, 2): [OccupiableStation(self.item)],
            Vector(1, 3): [Station(None)],
            Vector(5, 5): [self.avatar],
            Vector(5, 6): [self.wall]
        }
        self.game_board: GameBoard = GameBoard(1, Vector(10, 10), self.locations, False)
        self.utils = game.test_suite.utils

    # test seed
    def test_seed(self):
        self.game_board.seed = 2
        self.assertEqual(self.game_board.seed, 2)

    def test_seed_fail(self):
        value: str = 'False'
        with self.assertRaises(ValueError) as e:
            self.game_board.seed = value
        self.assertTrue(self.utils.spell_check(str(e.exception),
                                               f'GameBoard.seed must be an int. '
                                               f'It is a(n) {value.__class__.__name__} with the value of {value}.',
                                               False))

    # test map_size
    def test_map_size(self):
        self.game_board.map_size = Vector(12, 12)
        self.assertEqual(str(self.game_board.map_size), str(Vector(12, 12)))

    def test_map_size_fail(self):
        value: str = 'wow'
        with self.assertRaises(ValueError) as e:
            self.game_board.map_size = value
        self.assertTrue(self.utils.spell_check(str(e.exception),
                                               f'GameBoard.map_size must be a Vector. '
                                               f'It is a(n) {value.__class__.__name__} with the value of {value}.',
                                               False))

    # test locations
    def test_locations(self):
        self.locations = {
            (Vector(1, 1),): [self.avatar],
            (Vector(1, 2), Vector(1, 3)): [OccupiableStation(self.item), Station(None)],
            (Vector(5, 5),): [Station(None)],
            (Vector(5, 6),): [self.wall]
        }
        self.game_board.locations = self.locations
        self.assertEqual(str(self.game_board.locations), str(self.locations))

    def test_locations_fail_type(self):
        value: str = 'wow'
        with self.assertRaises(ValueError) as e:
            self.game_board.locations = value
        self.assertTrue(self.utils.spell_check(str(e.exception),
                                               f'Locations must be a dict. The key must be a tuple of Vector Objects, '
                                               f'and the value a list of GameObject. '
                                               f'It is a(n) {value.__class__.__name__} with the value of {value}.',
                                               False))

    # test walled
    def test_walled(self):
        self.game_board.walled = True
        self.assertEqual(self.game_board.walled, True)

    def test_walled_fail(self):
        value: str = 'wow'
        with self.assertRaises(ValueError) as e:
            self.game_board.walled = value
        self.assertTrue(self.utils.spell_check(str(e.exception),
                                               f'GameBoard.walled must be a bool. '
                                               f'It is a(n) {value.__class__.__name__} with the value of {value}.',
                                               False))

    # test json method
    def test_game_board_json(self):
        data: dict = self.game_board.to_json()
        temp: GameBoard = GameBoard().from_json(data)

        self.assertEqual(self.game_board.seed, temp.seed)
        self.assertEqual(self.game_board.map_size, temp.map_size)
        self.assertEqual(self.game_board.walled, temp.walled)
        self.assertEqual(self.game_board.event_active, temp.event_active)

        # since the map wasn't generated, it should be the None value
        self.assertTrue(self.game_board.game_map is None)
        self.assertTrue(temp.game_map is None)

    def test_generate_map(self):
        self.game_board.generate_map()

        # access the objects in the GameObjectContainers to see if they are stored properly
        self.assertEqual(self.game_board.get_objects_from(Vector(1, 1))[0].object_type, ObjectType.STATION)
        self.assertEqual(self.game_board.get_objects_from(Vector(1, 2))[0].object_type, ObjectType.OCCUPIABLE_STATION)
        self.assertEqual(self.game_board.get_objects_from(Vector(1, 3))[0].object_type, ObjectType.STATION)
        self.assertEqual(self.game_board.get_objects_from(Vector(5, 5))[0].object_type, ObjectType.AVATAR)
        self.assertEqual(self.game_board.get_objects_from(Vector(5, 6))[0].object_type, ObjectType.WALL)

    # ensure that walls are placed properly when generating the map
    def test_wall_generation(self):
        self.game_board.walled = True
        map_size: Vector = self.game_board.map_size
        self.game_board.generate_map()

        x: int = 0
        y: int = 0

        for iteration in range(map_size.x * map_size.y):
            x = iteration % map_size.x
            coords: Vector = Vector(x, y)

            # check every coordinate that's the border
            if x == 0 or x == map_size.x or y == 0 or y == map_size.y:
                # ensure that the borders only contain Wall objects
                self.assertEqual(self.game_board.get_top(coords).object_type, ObjectType.WALL)
                self.assertTrue(len(self.game_board.get_objects_from(coords)) == 1)

        # access the objects in the GameObject lists to see if they are stored properly
        self.assertEqual(self.game_board.get_objects_from(Vector(1, 1))[0].object_type, ObjectType.STATION)
        self.assertEqual(self.game_board.get_objects_from(Vector(1, 2))[0].object_type, ObjectType.OCCUPIABLE_STATION)
        self.assertEqual(self.game_board.get_objects_from(Vector(1, 3))[0].object_type, ObjectType.STATION)
        self.assertEqual(self.game_board.get_objects_from(Vector(5, 5))[0].object_type, ObjectType.AVATAR)
        self.assertEqual(self.game_board.get_objects_from(Vector(5, 6))[0].object_type, ObjectType.WALL)
