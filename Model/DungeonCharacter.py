from abc import ABC, abstractmethod

class DungeonCharacter(ABC):
    @abstractmethod
    def __init__ (self, theAttackDamage: int, theHealthPoints: int,
                   thePositionX: int, thePositionY: int, theSpeed: int) -> None:
        self._myAttackDamage = theAttackDamage
        self._myHealthPoints = theHealthPoints
        self._myPositionX = thePositionX
        self._myPositionY = thePositionY
        self._mySpeed = theSpeed
    
    
    @abstractmethod
    def moveCharacter(theNewX: int, theNewY: int) -> None:
        pass

    @abstractmethod
    def Dies():
        pass
    

    @abstractmethod
    def toString() -> str:
        pass