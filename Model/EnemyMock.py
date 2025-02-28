from .DungeonCharacter import DungeonCharacter
from .EventManager import EventManager
from CustomEvents import CustomEvents
# from .GameWorld import GameWorld
import pygame
import random

class EnemyMock(DungeonCharacter):

    SCREEN_WIDTH = 800  # Example boundary
    SCREEN_HEIGHT = 600  # Example boundary
    def __init__(self, theAttackDamage: int, theHealthPoints: int,
                   thePositionX: int, thePositionY: int, theSpeed: int) -> None:
        #super().__init__(theAttackDamage, theHealthPoints, thePositionX, thePositionY, theSpeed=)
        
        # Fix position initialization (previous bug with _myPositionY)
        self.__myPositionX = thePositionX  # Starting X100
        self.__myPositionY = thePositionY  # Starting Y
    
        # Movement-related variables
        self.__myDirection = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.__move_timer = pygame.time.get_ticks()  # Timer for direction change
        self.__mySpeed = theSpeed # Enemy movement speed (change as needed)2
        
        self.__myName = "EnemyMock"
        # Register enemy in GameWorld
        #print(GameWorld.getInstance())
        #GameWorld.getInstance().add_enemy(self)

    def Dies(self):
        print("*Dies*")
        self.world.remove_enemy(self)

    def getPositionX(self) -> int:
        return int(self.__myPositionX)
    
    def getPositionY(self) -> int:
        return int(self.__myPositionY)
    
    def update(self):
        """ Updates the enemy's position randomly """
        current_time = pygame.time.get_ticks()

        # Change direction every 1 second (1000ms)
        if current_time - self.__move_timer > 1000:
            self.__myDirection = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            self.__move_timer = current_time  # Reset timer

        new_x, new_y = self.__myPositionX, self.__myPositionY

        # Move based on the direction
        if self.__myDirection == "UP":
            new_y -= self.__mySpeed
        elif self.__myDirection == "DOWN":
            new_y += self.__mySpeed
        elif self.__myDirection == "LEFT":
            new_x -= self.__mySpeed
        elif self.__myDirection == "RIGHT":
            new_x += self.__mySpeed

        # Keep enemy inside screen bounds
        new_x = max(0, min(new_x, self.SCREEN_WIDTH - 50))  # Ensure inside width
        new_y = max(0, min(new_y, self.SCREEN_HEIGHT - 50))  # Ensure inside height

        # Check for collision before moving
        from .GameWorld import GameWorld
        if not GameWorld.getInstance().check_collision(pygame.Rect(new_x, new_y, 50, 50), ignore=self):
            self.moveCharacter(new_x, new_y)

            # Post movement event
            event = pygame.event.Event(
                EventManager.event_types[CustomEvents.CHARACTER_MOVED],
                {
                    "name": self.getName(),
                    "id": self.__str__(),
                    "positionX": self.getPositionX(),
                    "positionY": self.getPositionY()
                }
            )
            pygame.event.post(event)

    def moveCharacter(self, theNewX: int, theNewY: int):
        """ Moves the character to a new position """
        self.__myPositionX = theNewX
        self.__myPositionY = theNewY

    def toString(self) -> str:
        return f"{self.__myName} at ({self.__myPositionX}, {self.__myPositionY})"
    
    def getName(self):
        return self.__myName