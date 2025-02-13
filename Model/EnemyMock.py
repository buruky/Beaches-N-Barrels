from .DungeonCharacter import DungeonCharacter
from .EventManager import EventManager
import pygame
class EnemyMock(DungeonCharacter):
    def __init__(self):
        super().__init__(50, 100, 100, 100, 1)#####
        self.__myPositionX = self._myPositionY
        self.__myPositionY = self._myPositionY
        self.__myDirection = None
        self.__myName = "EnemyMock"

        

    


    def Dies(self):
        print("*Dies*")

    def getPositionX(self) -> int:
        return int(self.__myPositionX)
    
    def getPositionY(self) -> int:
        return int(self.__myPositionY)
    

    def update(self):
        self.moveCharacter(self.getPositionX() + 1 * self._mySpeed, self.getPositionY())
        pygame.event.post(pygame.event.Event(EventManager.ENEMY_MOVED, {"EnemyMock": self}))

    def moveCharacter(self, theNewX: int, theNewY: int):
        self.__myPositionX = theNewX #need to add speed!
        self.__myPositionY = theNewY

    def toString(self) -> str:
        print("*Strings*")
    
    def getName(self):
        return self.__myName
    
    def getSprite(self):
        return self._mySprite