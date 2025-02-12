from typing import Final
from .DungeonCharacter import DungeonCharacter
from .EventManager import EventManager
import pygame
class PlayerMock(DungeonCharacter):
    def __init__(self):
        super().__init__(50, 100, 250, 250, 5)#####
        self.__myPositionX = self._myPositionX
        self.__myPositionY = self._myPositionY
        self.__myName = "PlayerMock"
        self.__myDirection = None
        self.__MAX_SIZE:Final = 500 #deprectated
        self.__MIN_SIZE:Final = 10
        self.update()

    def moveCharacter(self, theDirections:list) -> None:
        dx, dy = 0, 0

        if "LEFT" in theDirections:
            dx = -1
        if "RIGHT" in theDirections:
            dx = 1

        if "UP" in theDirections:
            dy = -1
            self.update()

        if "DOWN" in theDirections:
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
        if theDirections:
            self.__myDirection = theDirections[-1]  # Last key pressed is priority
    
    def update(self):
        pygame.event.post(pygame.event.Event(EventManager.PLAYER_MOVED, {self.__class__.__name__: self}))

    def teleportCharacter(self, num1: int, num2: int) -> None:
        self.__myPositionX = num1
        self.__myPositionY = num2
        self.update()

    def Dies(self) -> None:
        print("*dies*")
    

    def getPositionX(self) -> int:
        return self.__myPositionX
    
    def getPositionY(self) -> int:
        return self.__myPositionY
    
    def getSprite(self) -> pygame.Surface:
        return self._mySprite


    def getName(self):
        return self.__myName
    
    def toString() -> str:
        print("*Strings*")