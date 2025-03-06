from typing import Final

from ViewUnits import ViewUnits
from .DungeonCharacter import DungeonCharacter
from .EventManager import EventManager
from CustomEvents import CustomEvents
from .GameWorld import GameWorld
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
        
        """when player is made should update sprite"""
        self.update(CustomEvents.CHARACTER_STOPPED)
        GameWorld.getInstance().add_player(self)

    def moveCharacter(self, theDirections:list) -> None:
        dx, dy = 0, 0

        if "LEFT" in theDirections:
            dx = -1
        if "RIGHT" in theDirections:
            dx = 1

        if "UP" in theDirections:
            dy = -1
            
        if "DOWN" in theDirections:
            dy = 1
        
        if len(theDirections) == 0:
            """when no direction is passed that means character stopped"""
            self.update(CustomEvents.CHARACTER_STOPPED)

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.707  # 1/sqrt(2)
            dy *= 0.707

        # Compute new position
        new_x = self.__myPositionX + dx * self._mySpeed
        new_y = self.__myPositionY + dy * self._mySpeed
        

        new_x = max(0, min(ViewUnits.SCREEN_WIDTH - ViewUnits.DEFAULT_WIDTH, new_x))
        new_y = max(0, min(ViewUnits.SCREEN_HEIGHT - ViewUnits.DEFAULT_HEIGHT, new_y))

        # Update position
        if not GameWorld.getInstance().check_collision(pygame.Rect(new_x, new_y, 50, 50), ignore=self):
            self.__myPositionX = new_x
            self.__myPositionY = new_y

        collidedDoor = GameWorld.getInstance().collideWithDoor(pygame.Rect(new_x, new_y, 50, 50))
        if collidedDoor is not None:
            self.teleportCharacter(ViewUnits.SCREEN_WIDTH//2, ViewUnits.SCREEN_HEIGHT//2)
            

        if dx != 0 or dy != 0:
            """when character is moving in any direction"""
            self.update(CustomEvents.CHARACTER_MOVED)
         # Update direction if moving
        if theDirections:
            self.__myDirection = theDirections[-1]  # Last key pressed is priority
    
    def update(self, theEventName:str):
        event = pygame.event.Event(
            
            EventManager.event_types[theEventName],
            {"name": self.getName(),
             "positionX": self.getPositionX(),
             "positionY": self.getPositionY(),
             "id": id(self)}        
            )
        pygame.event.post(event)
        pass

    def teleportCharacter(self, num1: int, num2: int) -> None:
        self.__myPositionX = num1
        self.__myPositionY = num2
        """If Character moves their sprite should be updated to location"""
        self.update(CustomEvents.CHARACTER_STOPPED)#might work

    def Dies(self) -> None:
        """Trigger the death event and post a CHARACTER_DIED event."""
        print("*dies*")#Debugging
        death_event = pygame.event.Event(EventManager.event_types[CustomEvents.PLAYER_DIED])
        pygame.event.post(death_event)
    

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