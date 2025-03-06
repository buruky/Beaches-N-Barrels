from abc import ABC, abstractmethod
import pygame
from ViewUnits import ViewUnits

class DungeonCharacter(ABC):
    
    def __init__ (self, theAttackDamage: int, theHealthPoints: int,
                   thePositionX: int, thePositionY: int, theSpeed: int) -> None:
        self._myAttackDamage = theAttackDamage
        self._myHealthPoints = theHealthPoints
        self._myPositionX = int(thePositionX)
        self._myPositionY = int(thePositionY)

        self._mySpeed = theSpeed
        self._myHasChanged = True
        self._myRect = pygame.Rect(self._myPositionX, self._myPositionY,ViewUnits.DEFAULT_WIDTH, ViewUnits.DEFAULT_HEIGHT)# will be replaced by sprite image with no location data
        self._mySprite = pygame.Surface((self._myRect.width, self._myRect.height), pygame.SRCALPHA)
        self._mySprite.fill((0,30,144))

    @abstractmethod
    def moveCharacter(theNewX: int, theNewY: int) -> None:
        pass

    @abstractmethod
    def Dies():
        pass
    

    @abstractmethod
    def toString() -> str:
        pass