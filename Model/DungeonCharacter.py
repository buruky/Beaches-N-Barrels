from abc import ABC, abstractmethod

class DungeonCharacter(ABC):
    @abstractmethod
    def __init__ (self, theAttackDamage, theHealthPoints, thePositionX, thePositionY) -> None:
        self.__myAttackDamage = theAttackDamage
        self.__myHealthPoints = theHealthPoints
        self.__myPositionX = thePositionX
        self.__myPositionY = thePositionY
    
    @abstractmethod
    def moveCharacter(theNewX: int, theNewY: int) -> None:
        pass

    @abstractmethod
    def Dies():
        pass
    
    @abstractmethod
    def getPosition() -> list:
        pass

    @abstractmethod
    def toString() -> str:
        pass