import os
import sys
import unittest
import pygame
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Model import *


class TestPlayer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize Pygame (required for some Pygame functionality)."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Quit Pygame after tests are done."""
        pygame.quit()

    def setUp(self):
        """Create a Player instance for testing."""
        self.player = Player("P1",2000, 1, 0)

    def test_initial_position(self):
        """Test if the player starts at the correct position."""
        self.assertEqual(self.player.getPositionX(), 250)
        self.assertEqual(self.player.getPositionY(), 250)

    def test_movement(self):
        """Test if the player moves correctly."""
        self.player.move("left")
        self.assertEqual(self.player.x, 95)  # Moves left by 5 pixels

        self.player.move("right")
        self.assertEqual(self.player.x, 100)  # Moves back to original

        self.player.move("up")
        self.assertEqual(self.player.y, 95)  # Moves up by 5 pixels

        self.player.move("down")
        self.assertEqual(self.player.y, 100)  # Moves back down

    def test_rect_position_update(self):
        """Test if the rect position updates correctly with movement."""
        self.player.move("right")
        self.assertEqual(self.player.rect.topleft, (105, 100))

if __name__ == "__main__":
    unittest.main()