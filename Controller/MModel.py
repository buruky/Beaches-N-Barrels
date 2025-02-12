import pygame
import random

from Model import *
class MModel:
    """Class that instantiates DungeonCharacters() in game (needs new name!)"""
    #probably will need to be refactored to a Instantiator or something
    def __init__(self):
        self.__myDungeonCharacterList = DungeonCharacterList()
        self.__initalizeAll()
    def __initalizeAll(self):
        #Should figure out a way to do tis based on room generation
        enemy1 = EnemyMock()# should have params in here but not set up rn
        self.__myDungeonCharacterList.add_entity(enemy1)

    def update(self):
        """Update all game entities."""
        self.__myDungeonCharacterList.update_all()

    

