from .DungeonCharacter import DungeonCharacter
from .EventManager import EventManager
import pygame
class PlayerMock(DungeonCharacter):
    def __init__(self):
        super().__init__(50, 100, 250, 250, 5)#####
        self.__myPositionX = self._myPositionX
        self.__myPositionY = self._myPositionY
        self.__myName = "PlayerMock"
        self.__direction = None
        self.__max_size = 500 
        self.__min_size = 10
        self.update()

    def moveCharacter(self, directions):  # ngl idk what type this is 
        dx, dy = 0, 0

        if "LEFT" in directions:
            dx = -1
        if "RIGHT" in directions:
            dx = 1

        if "UP" in directions:
            dy = -1
            self.update()

        if "DOWN" in directions:
            dy = 1
        

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.707  # 1/sqrt(2)
            dy *= 0.707

        # Update position
        self.__myPositionX += dx * self._mySpeed
        self.__myPositionY += dy * self._mySpeed
        if dx != 0 or dy != 0:
            self.update()
         # Update direction if moving
        if directions:
            self.direction = directions[-1]  # Last key pressed is priority
    
    def update(self):
        pygame.event.post(pygame.event.Event(EventManager.PLAYER_MOVED, {self.__class__.__name__: self}))
        
    def changeColor(self, theColor):
        self.color = theColor

    def teleportCharacter(self, num1, num2):
        self.__myPositionX = num1
        self.__myPositionY = num2
        self.update()

    def Dies():
        print("*dies*")
    

    def getPositionX(self) -> int:
        return self.__myPositionX
    
    def getPositionY(self) -> int:
        return self.__myPositionY
    
    def getSprite(self):
        return self._mySprite


    def getName(self):
        return self.myName
    
    def toString() -> str:
        print("*Strings*")