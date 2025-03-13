from typing import Final
from ViewUnits import ViewUnits
from .DungeonCharacter import DungeonCharacter
from .EventManager import EventManager
from CustomEvents import CustomEvents
from .GameWorld import GameWorld
from .Abilities import SpeedBoostAbility
import pygame

class Player(DungeonCharacter):
    """Parent class for all player heroes with shared movement and event handling."""
    
    def __init__(self, name: str, speed: int, health: int, damage: int):
        super().__init__(damage, health, 250, 250, speed)  # Default attackDamage = 50
        self._myHealth = health
        self._name = name
        self._direction = None
        self._ability = None  # To be set by subclasses

        #item
        self.__inventory = []
        self._item_Ability = SpeedBoostAbility(self)
        
        """Update sprite when player is made"""
        self.update(CustomEvents.CHARACTER_STOPPED)


    def getAttackDamage(self) -> int:
        return self._myAttackDamage
    
    def moveCharacter(self, theDirections: list) -> None:
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
            """No movement, player stopped"""
            self.update(CustomEvents.CHARACTER_STOPPED)

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.707  # 1/sqrt(2)
            dy *= 0.707

        # Compute new position
        new_x = self._myPositionX + dx * self._mySpeed
        new_y = self._myPositionY + dy * self._mySpeed

        new_x = max(0, min(ViewUnits.SCREEN_WIDTH - ViewUnits.DEFAULT_WIDTH, new_x))
        new_y = max(0, min(ViewUnits.SCREEN_HEIGHT - ViewUnits.DEFAULT_HEIGHT, new_y))

        # Update position if no collision
        if not GameWorld.getInstance().check_collision(pygame.Rect(new_x, new_y, 50, 50), ignore=self):
            self._myPositionX = new_x
            self._myPositionY = new_y

        collidedDoor = GameWorld.getInstance().collideWithDoor(pygame.Rect(new_x, new_y, 50, 50))
        if collidedDoor is not None:
            self.teleportCharacter(ViewUnits.SCREEN_WIDTH//2, ViewUnits.SCREEN_HEIGHT//2)

        collidedItem = GameWorld.getInstance().collideWithItem(pygame.Rect(new_x, new_y, 50, 50))
        if collidedItem is not None:
            self.pickup(collidedItem)

        if dx != 0 or dy != 0:
            """Character is moving"""
            self.update(CustomEvents.CHARACTER_MOVED)
        
        if theDirections:
            self._direction = theDirections[-1]  # Last key pressed is priority
    
    def pickup(self, item) -> None:
        self.__inventory.append(item)
        print(f"Picked up {item}")
        print([str(obj) for obj in self.__inventory])
        event = pygame.event.Event(
            EventManager.event_types["PICKUP_ITEM"],
            {"name": self.getName(),
             "inventory": self.__inventory
            }        
        )
        pygame.event.post(event)

    def getInventory(self) -> list:
        return self.__inventory
    
    def use_item(self) -> None:
        ### use item when t is pressed
        if self.__inventory:
            item = self.__inventory[0]
            if item.name == "MockItem":
                if not self._item_Ability.active:
                    self.__inventory.pop(0)
                    self._item_Ability.use()
                    print([str(obj) for obj in self.__inventory])
            else:
                #other items
                print("other items")
            #event to update the UI
            #self.update("ITEM_USED")
        #else:
            #print("No items available to use!")
     
    def teleportCharacter(self, num1: int, num2: int) -> None:
        self._myPositionX = num1
        self._myPositionY = num2
        """If Character moves their sprite should be updated to location"""
        self.update(CustomEvents.CHARACTER_STOPPED)#might work
    
    def takeDamage(self, damage: int):
        self._myHealth -= damage
        print("player health after damage: ",self._myHealth)
        event = pygame.event.Event(
            EventManager.event_types["TOOK_DAMAGE"],
            {"name": self.getName(),
             "health": self.getHealth()
            }        
        )
        pygame.event.post(event)
        if self._myHealth <= 0:
            self.Dies()


    def activate_ability(self):
        """Triggers the player's special ability when 'E' is pressed."""
        if self._ability:
            self._ability.use()

    def update(self, theEventName: str):
        event = pygame.event.Event(
            EventManager.event_types[theEventName],
            {"name": self.getName(),
             "positionX": self.getPositionX(),
             "positionY": self.getPositionY(),
             "id": id(self)}        
        )
        pygame.event.post(event)

    def update_items(self) -> None:
        """
        Updates each item in the player's inventory so that cooldowns are tracked.
        Call this in your game loop tick.
        """
        for item in self.__inventory:
            item.update(self)

    
    def Dies(self) -> None:
        """Trigger death event"""
        print(f"{self._name} has died!")  # Debugging
        death_event = pygame.event.Event(EventManager.event_types[CustomEvents.PLAYER_DIED])
        pygame.event.post(death_event)

    def getPositionX(self) -> int:
        return self._myPositionX
    def getHealth(self):
        return self._myHealth
    def getPositionY(self) -> int:
        return self._myPositionY
    
    def getName(self):
        return self._name

    def toString(self) -> str:
        return f"{self._name} at ({self._myPositionX}, {self._myPositionY})"
