import unittest
from unittest.mock import patch, MagicMock
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Model.EnemyFactory import EnemyFactory


class TestEnemyFactory(unittest.TestCase):

    def setUp(self):
        # Reset singleton between tests
        EnemyFactory._instance = None

    @patch('Model.EnemyFactory.initialize_enemy_db')
    def test_singleton_behavior(self, mock_init):
        instance1 = EnemyFactory.getInstance()
        instance2 = EnemyFactory.getInstance()
        self.assertIs(instance1, instance2)
        mock_init.assert_called_once_with("db/enemies.db")

    @patch('Model.EnemyFactory.initialize_enemy_db')
    @patch('Model.EnemyFactory.sqlite3.connect')
    def test_load_enemy_data_returns_expected(self, mock_connect, mock_init):
        cursor = MagicMock()
        cursor.fetchone.return_value = (5, 20, 3)
        mock_connect.return_value.cursor.return_value = cursor

        factory = EnemyFactory.getInstance()
        data = factory.load_enemy_data("Crab")
        self.assertEqual(data, {"attack": 5, "health": 20, "speed": 3})

    @patch('Model.EnemyFactory.initialize_enemy_db')
    @patch('Model.EnemyFactory.sqlite3.connect', side_effect=Exception("DB failed"))
    def test_load_enemy_data_fallback_on_exception(self, mock_connect, mock_init):
        factory = EnemyFactory.getInstance()
        data = factory.load_enemy_data("Unknown")
        self.assertEqual(data, {
            "attack": factory._DEFAULT_ATTACK_DAMAGE,
            "health": factory._DEFAULT_HEALTH,
            "speed": factory._DEFAULT_SPEED
        })

    @patch('ViewUnits.ViewUnits.SCREEN_HEIGHT', 600)
    @patch('ViewUnits.ViewUnits.SCREEN_WIDTH', 800)
    @patch('Model.EnemyFactory.random.randint', return_value=100)
    @patch('Model.EnemyFactory.Crab')
    @patch('Model.EnemyFactory.initialize_enemy_db')
    @patch('Model.EnemyFactory.sqlite3.connect')
    def test_create_enemy_returns_crab(self, mock_connect, mock_init, MockCrab, mock_rand, *_):
        mock_connect.return_value.cursor.return_value.fetchone.return_value = (3, 10, 2)
        factory = EnemyFactory.getInstance()
        factory.create_enemy("Crab")
        MockCrab.assert_called_once_with(3, 10, 100, 100, 2)

    @patch('ViewUnits.ViewUnits.SCREEN_HEIGHT', 600)
    @patch('ViewUnits.ViewUnits.SCREEN_WIDTH', 800)
    @patch('Model.EnemyFactory.random.randint', return_value=123)
    @patch('Model.EnemyFactory.DungeonCharacterList')
    @patch('Model.EnemyFactory.BeachBall')
    @patch('Model.EnemyFactory.Crab')
    @patch('Model.EnemyFactory.initialize_enemy_db')
    @patch('Model.EnemyFactory.sqlite3.connect')
    def test_create_normal_template_returns_expected_enemies(self, mock_connect, mock_init,
                                                              MockCrab, MockBeachBall, MockList,
                                                              mock_rand, *_):
        mock_connect.return_value.cursor.return_value.fetchone.return_value = (1, 1, 1)
        factory = EnemyFactory.getInstance()

        result = factory.createNormalTemplate(1)
        self.assertIs(result, MockList.return_value)
        self.assertTrue(MockList.return_value.add_entity.called)
        MockCrab.assert_called()
        MockBeachBall.assert_called()

    @patch('Model.EnemyFactory.DungeonCharacterList')
    @patch('Model.EnemyFactory.Shark')
    @patch('Model.EnemyFactory.initialize_enemy_db')
    @patch('Model.EnemyFactory.sqlite3.connect')
    def test_create_boss_template_adds_shark(self, mock_connect, mock_init, MockShark, MockList):
        mock_connect.return_value.cursor.return_value.fetchone.return_value = (10, 100, 5)
        factory = EnemyFactory.getInstance()
        result = factory.createBossTemplate()
        MockShark.assert_called_once()
        MockList.return_value.add_entity.assert_called_once()
        self.assertIs(result, MockList.return_value)

    @patch('Model.EnemyFactory.DungeonCharacterList')
    @patch('Model.EnemyFactory.Barrel')
    @patch('Model.EnemyFactory.initialize_enemy_db')
    @patch('Model.EnemyFactory.sqlite3.connect')
    def test_create_key_template_adds_barrel(self, mock_connect, mock_init, MockBarrel, MockList):
        mock_connect.return_value.cursor.return_value.fetchone.return_value = (2, 5, 1)
        factory = EnemyFactory.getInstance()
        result = factory.createKeyTemplate()
        MockBarrel.assert_called_once()
        MockList.return_value.add_entity.assert_called_once()
        self.assertIs(result, MockList.return_value)


if __name__ == "__main__":
    unittest.main()