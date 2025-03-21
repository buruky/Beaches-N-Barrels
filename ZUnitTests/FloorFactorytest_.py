import os
import sys
import unittest
import pygame
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ViewUnits import ViewUnits

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
        EventManager.registerEvent(CustomEvents.CHANGED_ROOM,self.EmptyMethod(CustomEvents.CHANGED_ROOM))

        self.floorFac = FloorFactory()
        self.floor = self.floorFac.createFloor()

    def test_total_grid_array_size(self):
        """"""
        self.assertEqual(ViewUnits.FLOOR_SIDE_LENGTH,len(self.floor.get_dungeon()))

    def test_RoomNumber(self):
        self.floor = self.floorFac.createFloor()
        theArr = self.floor.get_dungeon()
        count = 0
        for i in range(len(theArr)):
            for k in range(len(theArr[0])):
                if theArr[i][k]:
                    count+=1
        self.assertTrue(count == 13 or count == 12)

    def test_startRoom(self):
        self.assertEquals((5,5), self.floorFac.getStartRoom())
        self.assertEqual((5,5),self.floor.getStartRoom())
    
    def test_keyMin(self):
        self.assertEqual(2,self.floorFac.getKeyMin())
if __name__ == "__main__":
    unittest.main()