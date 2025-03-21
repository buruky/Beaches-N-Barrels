import os
import sys
import unittest
import pygame
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CustomEvents import CustomEvents
from Model import *
from Controller import *


class TestPlayer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize Pygame (required for some Pygame functionality)."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Quit Pygame after tests are done."""
        pygame.quit()
    def EmptyMethod(self,event):
        print(event)
        
    def setUp(self):
        """Create a Player instance for testing."""
        EventManager.registerEvent(CustomEvents.CHARACTER_STOPPED, self.EmptyMethod(CustomEvents.CHARACTER_STOPPED))
        EventManager.registerEvent(CustomEvents.CHARACTER_MOVED, self.EmptyMethod(CustomEvents.CHARACTER_MOVED))

        EventManager.registerEvent(CustomEvents.CHANGED_ROOM,self.EmptyMethod(CustomEvents.CHANGED_ROOM))
        #self.theController = MController().__InitalizeEvents()
        self.testGameworld = GameWorld.getInstance()
        self.player = Player("P1",2000, 1, 0)
        self.testGameworld.setPlayer(self.player)

    def test_initial_position(self):
        """Test if the player starts at the correct position."""
        self.assertEqual(self.player.getPositionX(), 250)
        self.assertEqual(self.player.getPositionY(), 250)


    def test_movement(self):
        """Test if the player moves correctly."""
        self.player.moveCharacter(["LEFT"])
        self.player.moveCharacter([])
        self.assertTrue(self.player.getPositionX() < 250)  # Moves left by 5 pixels
        
        print("pass")
        self.player.moveCharacter(["RIGHT"])
        self.player.moveCharacter([])
        self.assertTrue(self.player.getPositionX() > 250)  # Moves back to original
        

        self.player.moveCharacter(["UP"])
        self.player.moveCharacter([])
        self.assertTrue(self.player.getPositionY() < 250)  # Moves up by 5 pixels
        

        self.player.moveCharacter(["DOWN"])
        self.player.moveCharacter([])
        self.assertTrue(self.player.getPositionY() > 250)  # Moves back down

    # def test_rect_position_update(self):
    #     """Test if the rect position updates correctly with movement."""
    #     self.player.moveCharacter("RIGHT")
    #     self.assertEqual(self.player.rect.topleft, (105, 100))

if __name__ == "__main__":
    unittest.main()