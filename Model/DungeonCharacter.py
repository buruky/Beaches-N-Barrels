from abc import ABC, abstractmethod
import pygame
from ViewUnits import ViewUnits

class DungeonCharacter(ABC):
    """
    Abstract base class representing a character in the dungeon.
    Provides common attributes and requires movement and death behavior to be implemented.
    """
    def __init__ (self, theAttackDamage: int, theHealthPoints: int,
                   thePositionX: int, thePositionY: int, theSpeed: int) -> None:
        """
        Initializes a dungeon character with basic attributes.

        :param theAttackDamage: The character's attack damage.
        :param theHealthPoints: The character's starting health points.
        :param thePositionX: The character's starting X position.
        :param thePositionY: The character's starting Y position.
        :param theSpeed: The movement speed of the character.
        """
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
        """
        Moves the character to a new position.

        :param theNewX: The new X coordinate.
        :param theNewY: The new Y coordinate.
        """
        pass
    
    @abstractmethod
    def Dies():
        """
        Handles character death behavior.
        """
        pass
    
    @abstractmethod
    def toString() -> str:
        """
        Returns a string representation of the character.

        :return: String describing the character.
        """
        pass
    