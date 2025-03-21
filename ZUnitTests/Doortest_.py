import unittest
from unittest.mock import MagicMock
import pygame
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Model import Door  # Adjust based on your file structure

class TestDoor(unittest.TestCase):

    def setUp(self):
        pygame.init()

        # Mock ViewUnits constants
        from ViewUnits import ViewUnits
        ViewUnits.NORTH_DOOR_CORD = (100, 0)
        ViewUnits.SOUTH_DOOR_CORD = (100, 500)
        ViewUnits.EAST_DOOR_CORD = (500, 250)
        ViewUnits.WEST_DOOR_CORD = (0, 250)

        # Mock Room objects
        self.mockRoom1 = MagicMock()
        self.mockRoom2 = MagicMock()
        self.mockRoom1.getCords.return_value = [0, 0]
        self.mockRoom2.getCords.return_value = [0, 1]
        self.mockRoom1.getRoomType.return_value = "n "
        self.mockRoom2.getRoomType.return_value = "n "

        self.door = Door("N", "S", self.mockRoom1, self.mockRoom2)

    def test_getConnectedRoom_returns_correct_room(self):
        connectedRoom = self.door.getConnectedRoom(self.mockRoom1)
        self.assertEqual(connectedRoom, self.mockRoom2)

        connectedRoom = self.door.getConnectedRoom(self.mockRoom2)
        self.assertEqual(connectedRoom, self.mockRoom1)

    def test_getConnectedRoom_invalid_room_raises(self):
        fake_room = MagicMock()
        with self.assertRaises(Exception) as context:
            self.door.getConnectedRoom(fake_room)
        self.assertIn("NOT CONNECTED TO THIS DOOR", str(context.exception))

    def test_toggleDoor_opens_and_closes_normally(self):
        self.door.toggleDoor(True)
        self.assertTrue(self.door.getState())
        self.door.toggleDoor(False)
        self.assertFalse(self.door.getState())

    def test_toggleDoor_does_not_close_if_boss(self):
        self.mockRoom1.getRoomType.return_value = "b "
        self.door.toggleDoor(True)
        self.assertTrue(self.door.getState())
        self.door.toggleDoor(False)
        self.assertFalse(self.door.getState())  # Boss room prevents closing

    def test_getBothRect_returns_two_rects(self):
        rects = self.door.getBothRect()
        self.assertIsInstance(rects, tuple)
        self.assertEqual(len(rects), 2)
        self.assertTrue(all(isinstance(r, pygame.Rect) for r in rects))

    def test_getRect_returns_correct_rect(self):
        rect1 = self.door.getRect("N")
        rect2 = self.door.getRect("S")
        self.assertIsInstance(rect1, pygame.Rect)
        self.assertIsInstance(rect2, pygame.Rect)

    def test_getRect_raises_on_invalid_direction(self):
        with self.assertRaises(Exception) as context:
            self.door.getRect("W")
        self.assertIn("THERE IS NO RECT WITH THAT DIRECTION", str(context.exception))

    def test_getConnectedDoorDirection(self):
        self.assertEqual(self.door.getConnectedDoorDirection(self.mockRoom1), "N")
        self.assertEqual(self.door.getConnectedDoorDirection(self.mockRoom2), "S")

    def test_getConnectedDoorDirection_invalid(self):
        other = MagicMock()
        with self.assertRaises(Exception):
            self.door.getConnectedDoorDirection(other)

    def test_getDoorRect_returns_opposite_rect(self):
        rect = self.door.getDoorRect("N")
        self.assertEqual(rect, self.door.getRect("S"))

    def test_getDoorRect_invalid_direction(self):
        with self.assertRaises(Exception):
            self.door.getDoorRect("W")

    def test_getCardinalDirection(self):
        self.assertEqual(self.door.getCardinalDirection(self.mockRoom1), "S")
        self.assertEqual(self.door.getCardinalDirection(self.mockRoom2), "N")

    def test_getCardinalDirection_invalid(self):
        other = MagicMock()
        with self.assertRaises(Exception):
            self.door.getCardinalDirection(other)

    def test_to_dict(self):
        self.door.isOpen = True
        data = self.door.to_dict()
        self.assertEqual(data["direction"], "N")
        self.assertEqual(data["connected_direction"], "S")
        self.assertEqual(data["room_coords"], [0, 0])
        self.assertEqual(data["neighbor_coords"], [0, 1])
        self.assertTrue(data["is_open"])

    def test_from_dict(self):
        data = {
            "direction": "W",
            "connected_direction": "E",
            "room_coords": [1, 2],
            "neighbor_coords": [2, 2],
            "is_open": True
        }
        door = Door.from_dict(data)
        self.assertEqual(door._room_coords, (1, 2))
        self.assertEqual(door._neighbor_coords, (2, 2))
        self.assertTrue(door.getState())

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
