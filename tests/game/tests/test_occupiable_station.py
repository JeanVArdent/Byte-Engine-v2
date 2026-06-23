import unittest

from game.common.stations.occupiable_station import OccupiableStation
from game.common.stations.station import Station
from game.common.map.wall import Wall
from game.common.avatar import Avatar
from game.common.items.item import Item
from game.common.enums import ObjectType
import game.test_suite.utils


class TestOccupiableStation(unittest.TestCase):
    """
    `Test Item Notes:`

        This class tests the different methods in the OccupiableStation class and ensures the objects that occupy them
        are properly set.
    """

    def setUp(self) -> None:
        self.occupiable_station: OccupiableStation = OccupiableStation()
        self.occupiable_station1: OccupiableStation = OccupiableStation()
        self.wall: Wall = Wall()
        self.station: Station = Station()
        self.avatar: Avatar = Avatar()
        self.item: Item = Item()
        self.utils = game.test_suite.utils

    # test adding item to occupiable_station
    def test_item_occ(self):
        self.occupiable_station.item = self.item
        self.assertEqual(self.occupiable_station.item.object_type, ObjectType.ITEM)
        self.assertEqual(self.occupiable_station.item.durability, self.item.durability)
        self.assertEqual(self.occupiable_station.item.value, self.item.value)

    # test json method
    def test_occ_json(self):
        self.occupiable_station.occupied_by = self.avatar
        data: dict = self.occupiable_station.to_json()
        occupiable_station: OccupiableStation = OccupiableStation().from_json(data)
        self.assertEqual(self.occupiable_station.object_type, occupiable_station.object_type)
