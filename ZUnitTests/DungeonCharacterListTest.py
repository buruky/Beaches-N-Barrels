import unittest
from unittest.mock import MagicMock, patch
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Model.DungeonCharacterList import DungeonCharacterList

class DungeonCharacterListTest(unittest.TestCase):

    def setUp(self):
        self.char_list = DungeonCharacterList()
        self.mock_character1 = MagicMock()
        self.mock_character2 = MagicMock()
        self.mock_character1.to_dict.return_value = {"name": "Pirate", "hp": 50}
        self.mock_character2.to_dict.return_value = {"name": "Crab", "hp": 80}

    def test_add_entity(self):
        self.char_list.add_entity(self.mock_character1)
        self.assertIn(self.mock_character1, self.char_list.get_entities())

    def test_get_entities_returns_correct_list(self):
        self.char_list.add_entity(self.mock_character1)
        self.char_list.add_entity(self.mock_character2)
        result = self.char_list.get_entities()
        self.assertEqual(result, [self.mock_character1, self.mock_character2])

    def test_update_all_calls_update_on_each_character(self):
        self.char_list.add_entity(self.mock_character1)
        self.char_list.add_entity(self.mock_character2)
        self.char_list.update_all()
        self.mock_character1.update.assert_called_once()
        self.mock_character2.update.assert_called_once()

    def test_deleteEnemy_removes_specific_character(self):
        self.char_list.add_entity(self.mock_character1)
        self.char_list.add_entity(self.mock_character2)
        self.char_list.deleteEnemy(self.mock_character1)
        self.assertNotIn(self.mock_character1, self.char_list.get_entities())
        self.assertIn(self.mock_character2, self.char_list.get_entities())
        self.mock_character2.update.assert_called()  # update_all is called

    def test_deleteAllEnemy_clears_all_characters(self):
        self.char_list.add_entity(self.mock_character1)
        self.char_list.add_entity(self.mock_character2)
        self.char_list.deleteAllEnemy()
        self.assertEqual(len(self.char_list.get_entities()), 0)

    def test_to_dict_serializes_characters_correctly(self):
        self.char_list.add_entity(self.mock_character1)
        self.char_list.add_entity(self.mock_character2)
        expected = {
            "characters": [
                {"name": "Pirate", "hp": 50},
                {"name": "Crab", "hp": 80}
            ]
        }
        self.assertEqual(self.char_list.to_dict(), expected)

    @patch('Model.Pirate.Pirate')
    @patch('Model.Crab.Crab')
    @patch('Model.Enemy.Enemy')
    def test_from_dict_reconstructs_characters(self, MockEnemy, MockCrab, MockPirate):
        data = {
            "characters": [
                {"name": "Pirate", "hp": 50},
                {"name": "Crab", "hp": 80},
                {"name": "Unknown", "hp": 10}
            ]
        }

        pirate_mock = MagicMock()
        crab_mock = MagicMock()
        enemy_mock = MagicMock()

        MockPirate.from_dict.return_value = pirate_mock
        MockCrab.from_dict.return_value = crab_mock
        MockEnemy.from_dict.return_value = enemy_mock

        restored_list = DungeonCharacterList.from_dict(data)
        entities = restored_list.get_entities()

        self.assertEqual(entities, [pirate_mock, crab_mock, enemy_mock])

if __name__ == "__main__":
    unittest.main()
