from .DungeonCharacter import DungeonCharacter
from .EventManager import EventManager
import pygame
class EnemyMock(DungeonCharacter):
    def __init__(self):
        super().__init__(50, 100, 100, 100, 1)#####
        self._myPositionX = self._myPositionY
        self.direction = None
        self.myName = "EnemyMock"

        self.max_size = 500 
        self.min_size = 10

    def changeColor(self):
        self.color = (25,120,0)


    def Dies(self):
        print("*Dies*")

    def getPositionX(self) -> int:
        return int(self._myPositionX)
    
    def getPositionY(self) -> int:
        
        return int(self._myPositionY)
    
    
    def update(self):
        self.moveCharacter(self.getPositionX() + 1 * self._mySpeed, self.getPositionY())
        self.changeColor()
        pygame.event.post(pygame.event.Event(EventManager.ENEMY_MOVED, {"entity": self}))

    def moveCharacter(self, theNewX: int, theNewY: int):
        self._myPositionX = theNewX #no speed rn
        self._myPositionY = theNewY

    def toString(self) -> str:
        print("*Strings*")
    
    def getName(self):
        return self.myName
    
    def getSprite(self):

        return self._mySprite