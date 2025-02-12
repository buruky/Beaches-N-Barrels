import pygame
import random

from Model import *
class MModel:
    """Class that instantiates DungeonCharacters in game"""
    #probably will need to be refactored to a Instantiator or something
    def __init__(self):
        
        self.myDungeonCharacterList = DungeonCharacterList()
        self.running = True
        self.initalizeAll()

    def initalizeAll(self):
        #Should figure out a way to do tis based on room generation
        #player = PlayerMock()
        enemy1 = EnemyMock()# should have params in here but not set up rn
        #self.myDungeonCharacterList.add_entity(player)
        self.myDungeonCharacterList.add_entity(enemy1)

    def update(self):
        """Update all game entities."""
        self.myDungeonCharacterList.update_all()

    

