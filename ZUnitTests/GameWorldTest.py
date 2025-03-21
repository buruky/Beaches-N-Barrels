import unittest
from unittest.mock import patch, MagicMock
import pygame
import sys, os

# Patch BEFORE GameWorld is imported
def setUpModule():
    patcher = patch.dict('Model.EventManager.EventManager.event_types', {
        'CHANGED_ROOM': pygame.USEREVENT + 1,
        'SONG_CHANGE': pygame.USEREVENT + 2,
    }, clear=True)
    patcher.start()

# Now safe to import GameWorld
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Model.GameWorld import GameWorld


class TestGameWorld(unittest.TestCase):
    def setUp(self):
        GameWorld.reset_instance()

        # Patch event posting
        self.patcher_event = patch('pygame.event.post')
        self.mock_event_post = self.patcher_event.start()

        # Patch FloorFactory inside GameWorld context
        self.patcher_factory = patch('Model.GameWorld.FloorFactory')
        mock_factory_class = self.patcher_factory.start()
        self.mock_factory_instance = mock_factory_class.getInstance.return_value
        self.mock_room = MagicMock()
        self.mock_factory_instance.createFloor.return_value.getStartRoom.return_value = self.mock_room

        # Room Setup
        self.mock_room.getRoomType.return_value = "n "
        self.mock_room.getDoorPos.return_value = {"N": True}
        self.mock_room.getCords.return_value = (0, 0)
        self.mock_room.get_items.return_value = []
        self.mock_room.getDoorMap.return_value = {}
        self.mock_room.getEnemyList.return_value.get_entities.return_value = []

        # Safe to construct now
        self.world = GameWorld.getInstance()

    def tearDown(self):
        self.patcher_event.stop()
        self.patcher_factory.stop()

    def test_singleton_behavior(self):
        self.assertIs(self.world, GameWorld.getInstance())

    def test_set_and_get_player(self):
        mock_player = MagicMock()
        self.world.setPlayer(mock_player)
        self.assertEqual(self.world.getPlayer(), mock_player)

    def test_add_and_remove_projectile(self):
        mock_projectile = MagicMock()
        self.world.addProjectile(mock_projectile)
        self.assertIn(mock_projectile, self.world.getProjectiles())
        self.world.removeProjectile(mock_projectile)
        self.assertNotIn(mock_projectile, self.world.getProjectiles())

    def test_remove_all_projectiles(self):
        mock_projectile = MagicMock()
        self.world.projectiles = [mock_projectile]
        self.world.removeAllProjectiles()
        self.assertEqual(len(self.world.projectiles), 0)

    def test_collide_with_item_detects_nothing(self):
        mock_rect = pygame.Rect(0, 0, 10, 10)
        self.assertIsNone(self.world.collideWithItem(mock_rect))

    def test_change_current_room_posts_event(self):
        mock_door = MagicMock()
        new_room = MagicMock()
        mock_door.getConnectedRoom.return_value = new_room
        mock_door.getConnectedDoorDirection.return_value = "S"
        new_room.getRoomType.return_value = "n "
        new_room.getCords.return_value = (1, 0)
        new_room.getDoorPos.return_value = {"N": True}
        self.world.changeCurrentRoom(mock_door)
        self.mock_event_post.assert_called()

    def test_check_collision_enemy_hit(self):
        mock_enemy = MagicMock()
        mock_enemy.getRect.return_value = pygame.Rect(0, 0, 10, 10)
        self.mock_room.getEnemyList.return_value.get_entities.return_value = [mock_enemy]
        rect = pygame.Rect(0, 0, 10, 10)
        self.world.setPlayer(MagicMock())
        collided = self.world.check_collision(rect)
        self.assertTrue(collided)

    def test_check_projectile_collision_bounds(self):
        mock_proj = MagicMock()
        mock_proj.getPositionX.return_value = -5
        mock_proj.getPositionY.return_value = 10
        mock_proj.getAttackDamage.return_value = 10
        result = self.world.check_projectile_collision(mock_proj, isEnemy=False)
        self.assertTrue(result)

    def test_check_projectile_collision_with_enemy(self):
        mock_proj = MagicMock()
        mock_proj.getPositionX.return_value = 10
        mock_proj.getPositionY.return_value = 10
        mock_proj.getAttackDamage.return_value = 10

        mock_enemy = MagicMock()
        mock_enemy.getRect.return_value = pygame.Rect(10, 10, 10, 10)
        self.mock_room.getEnemyList.return_value.get_entities.return_value = [mock_enemy]

        result = self.world.check_projectile_collision(mock_proj, isEnemy=False)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
