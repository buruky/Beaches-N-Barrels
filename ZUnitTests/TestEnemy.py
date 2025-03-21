import os
import sys
import unittest
import pygame
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CustomEvents import CustomEvents
from Model import *
from Controller import *
from Model.MockEnemy import MockEnemy


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
        self.enemy = MockEnemy()
        # self.testGameworld.add_enemy(self.enemy)
    

    def setUp(self):
        self.enemy = MockEnemy(name="Crab", attackDamage=15, healthPoints=100, speed=2, positionX=50, positionY=50)

    def test_initialization(self):
        self.assertEqual(self.enemy.getName(), "Crab")
        self.assertEqual(self.enemy.getAttackDamage(), 15)
        self.assertEqual(self.enemy.getHealth(), 100)
        self.assertEqual(self.enemy.getPositionX(), 50)
        self.assertEqual(self.enemy.getPositionY(), 50)
        self.assertFalse(self.enemy.isDead())

    def test_take_damage_exact_kill(self):
        self.enemy.takeDamage(100)
        self.assertEqual(self.enemy.getHealth(), 0)
        self.assertTrue(self.enemy.isDead())

    def test_take_damage_overkill(self):
        self.enemy.takeDamage(150)
        self.assertLess(self.enemy.getHealth(), 0)
        self.assertTrue(self.enemy.isDead())

    def test_take_damage_zero(self):
        self.enemy.takeDamage(0)
        self.assertEqual(self.enemy.getHealth(), 100)
        self.assertFalse(self.enemy.isDead())

    def test_multiple_hits(self):
        self.enemy.takeDamage(20)
        self.enemy.takeDamage(30)
        self.assertEqual(self.enemy.getHealth(), 50)
        self.assertFalse(self.enemy.isDead())

    def test_move_left(self):
        self.enemy.setDirection("LEFT")
        start_x = self.enemy.getPositionX()
        self.enemy.moveCharacter()
        self.assertEqual(self.enemy.getPositionX(), start_x - 2)

    def test_move_right(self):
        self.enemy.setDirection("RIGHT")
        start_x = self.enemy.getPositionX()
        self.enemy.moveCharacter()
        self.assertEqual(self.enemy.getPositionX(), start_x + 2)

    def test_move_up(self):
        self.enemy.setDirection("UP")
        start_y = self.enemy.getPositionY()
        self.enemy.moveCharacter()
        self.assertEqual(self.enemy.getPositionY(), start_y - 2)

    def test_move_down(self):
        self.enemy.setDirection("DOWN")
        start_y = self.enemy.getPositionY()
        self.enemy.moveCharacter()
        self.assertEqual(self.enemy.getPositionY(), start_y + 2)

    def test_custom_speed_and_position(self):
        enemy = MockEnemy(speed=5, positionX=10, positionY=20)
        enemy.setDirection("RIGHT")
        enemy.moveCharacter()
        self.assertEqual(enemy.getPositionX(), 15)
        enemy.setDirection("DOWN")
        enemy.moveCharacter()
        self.assertEqual(enemy.getPositionY(), 25)

if __name__ == "__main__":

    unittest.main()