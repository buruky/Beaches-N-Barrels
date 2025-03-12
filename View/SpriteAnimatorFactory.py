#singleton
from collections import defaultdict
import os

import pygame
from .SpriteSheetFactory import SpriteSheetFactory
from .SpriteAnimator import SpriteAnimator

class SpriteAnimatorFactory:
    def __init__(self):
        self.ssf = SpriteSheetFactory()
        self.__myListOfSpriteSheets = self.ssf.getAllAssets(self)

    def createSpriteAnimator(self, theName:str, theId: str, thePositionCords:list[int]) -> SpriteAnimator:
        self.createDefaultCharacter()
        #might implement different methods
    def createDefaultCharacter(self, theName:str, theId: str, thePositionCords:list[int]) -> SpriteAnimator:

        for currentName, currentSpriteSheet in self.__myListOfSpriteSheets.items():
            if theName == currentName:
                return SpriteAnimator(theName, theId, thePositionCords, currentSpriteSheet)
        raise Exception("SpriteAnimatorFactory.createDefaultCharacter: NO CHARACTER WITH SPRITESHEET WITH THAT NAME\n",
                        "Name Passed: ",theName,"\n"
                        "Names in List: ", self.__myListOfSpriteSheets.keys())
    


    
        