import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import MagicMock
from Model import Room
import pygame

class TestRoom(unittest.TestCase):

    def setUp(self):
        pygame.init()
        # Mocking DungeonCharacterList
        self.mock_enemy_list = MagicMock()
        self.mock_enemy_list.get_entities.return_value = []
        self.room = Room("n ", 1, 2, self.mock_enemy_list)

    def test_initial_coordinates_and_type(self):
        self.assertEqual(self.room.getCords(), [1, 2])
        self.assertEqual(self.room.getRoomType(), "n ")

    def test_setRoomType(self):
        self.room.setRoomType("b ")
        self.assertEqual(self.room.getRoomType(), "b ")

    def test_add_and_get_item(self):
        item = MagicMock()
        self.room.add_item(item)
        self.assertIn(item, self.room.get_items())

    def test_getDoorPos_empty(self):
        self.assertEqual(self.room.getDoorPos(), {})

    def test_addDoor_and_getDoorPos(self):
        mock_door = MagicMock()
        self.room.addDoor("N", mock_door)
        self.assertIn("N", self.room.getDoorPos())

    def test_killEnemy_calls_deleteEnemy(self):
        enemy = MagicMock()
        self.room.killEnemy(enemy)
        self.mock_enemy_list.deleteEnemy.assert_called_with(enemy)

    def test_randomKillEnemy_no_enemies(self):
        self.mock_enemy_list.get_entities.return_value = []
        self.room.randomKillEnemy()
        self.mock_enemy_list.deleteAllEnemy.assert_not_called()

    def test_randomKillEnemy_with_enemies(self):
        self.mock_enemy_list.get_entities.return_value = ["enemy"]
        self.room.randomKillEnemy()
        self.mock_enemy_list.deleteAllEnemy.assert_called()

    def test_checkState_with_enemies(self):
        self.mock_enemy_list.get_entities.return_value = ["enemy"]
        self.room.checkState()
        self.mock_enemy_list.update_all.assert_called()

    def test_checkState_no_enemies_opens_doors(self):
        self.mock_enemy_list.get_entities.return_value = []
        mock_door = MagicMock()
        self.room.addDoor("E", mock_door)
        self.room.checkState()
        mock_door.toggleDoor.assert_called_with(True)

    def test_to_dict_and_from_dict(self):
        mock_enemy = MagicMock()
        mock_enemy.to_dict.return_value = {"name": "orc"}

        mock_item = MagicMock()
        mock_item.to_dict.return_value = {"type": "potion"}

        mock_door = MagicMock()
        mock_door.to_dict.return_value = {"dir": "N"}

        self.mock_enemy_list.to_dict.return_value = {"enemies": [mock_enemy.to_dict.return_value]}
        self.room.add_item(mock_item)
        self.room.addDoor("N", mock_door)

        room_dict = self.room.to_dict()

        self.assertEqual(room_dict["room_type"], "n ")
        self.assertEqual(room_dict["x"], 1)
        self.assertEqual(room_dict["y"], 2)
        self.assertEqual(room_dict["enemy_list"]["enemies"][0]["name"], "orc")
        self.assertEqual(room_dict["items"][0]["type"], "potion")
        self.assertEqual(room_dict["doors"]["N"]["dir"], "N")

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
