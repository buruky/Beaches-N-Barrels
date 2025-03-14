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
    @abstractmethod
    def to_dict(self):
        """Convert player state to a dictionary for serialization."""
        return {
            "name": self._name,
            "speed": self._mySpeed,
            "health": self._myHealth,
            "direction": self._direction,
            "damage": self._myAttackDamage,
            "positionX": self._myPositionX,
            "positionY": self._myPositionY,
            # "inventory": [item.to_dict() for item in self.__inventory],  # Convert inventory items if needed
            # "ability_active": self._item_Ability.active if self._item_Ability else None
        }
    @abstractmethod
    def from_dict(cls, data):
        """Reconstruct a DungeonCharacter from a dictionary. Assumes subclass implementation."""
        if cls == DungeonCharacter:
            raise NotImplementedError("DungeonCharacter should not be instantiated directly.")
        
        return cls(
            data["damage"],
            data["health"],
            data["positionX"],
            data["positionY"],
            data["speed"]
        )
        

