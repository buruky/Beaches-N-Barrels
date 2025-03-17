from typing import Final
from ViewUnits import ViewUnits
from .DungeonCharacter import DungeonCharacter
from .EventManager import EventManager
from CustomEvents import CustomEvents
from .GameWorld import GameWorld
from .Abilities import HealAbility
from .Abilities import SpeedBoostAbility
from .FloorFactory import FloorFactory
from .Item import *
import pygame

class Player(DungeonCharacter):
    """Parent class for all player heroes with shared movement and event handling."""
    MAX_INVENTORY_SIZE: Final = 4
    def __init__(self, name: str, speed: int, health: int, damage: int):
        super().__init__(damage, health, 250, 250, speed)  # Default attackDamage = 50
        self._myHealth = health
        self.maxHealth = health
        self._name = name
        self._direction = "LEFT"  # Default direction
        self._ability = None  # To be set by subclasses
        self.__myFloorFactory = FloorFactory.getInstance()
        #item
        self.keyCount = 0
        self.invFull = False
        self.__inventory = [None,None,None,None]
        self._item_Ability = HealAbility(self)
        self._lastDoorTeleportTime = 0 
        
        """Update sprite when player is made"""
        self.update(CustomEvents.CHARACTER_STOPPED)

    def to_dict(self):
        """Convert player state to a dictionary for serialization, ensuring inventory is saved correctly."""
        return {
            "name": self._name,
            "speed": self._mySpeed,
            "health": self._myHealth,
            "direction": self._direction,
            "damage": self._myAttackDamage,
            "positionX": self._myPositionX,
            "positionY": self._myPositionY,
            "inventory": [item.to_dict() if item is not None else None for item in self.__inventory],
            "class": self.__class__.__name__,  # ✅ Save player subclass name
        }


    @classmethod
    def from_dict(cls, data):
        """Reconstruct a Player object, ensuring the correct subclass is restored properly."""
        from .Dolphin import Dolphin
        from .Buddha import Buddha
        from .Astronaut import Astronaut

        class_mapping = {
            "Dolphin": Dolphin,
            "Buddha": Buddha,
            "Astronaut": Astronaut,
            "Player": Player
        }

        player_class = class_mapping.get(data.get("class", "Player"), Player)

        # ✅ If the class is Dolphin/Buddha (no init params), just instantiate
        if player_class in [Dolphin, Buddha, Astronaut]:
            player = player_class()
        else:
            player = player_class(data["name"], data["speed"], data["health"], data["damage"])

        # Restore base attributes
        player._myPositionX = data["positionX"]
        player._myPositionY = data["positionY"]
        player._direction = data["direction"]

        # ✅ Restore inventory correctly on the instance
        if "inventory" in data:
            from .Item import UsableItem  # Ensure item classes are imported
            player.__inventory = []

            for item_data in data["inventory"]:
                if item_data is None:
                    player.__inventory.append(None)  # ✅ Preserve None values
                else:
                    item_class_name = item_data.get("class", "UsableItem")  # Default to UsableItem
                    item_class = globals().get(item_class_name, UsableItem)  # Find the correct item class

                    if hasattr(item_class, 'from_dict'):
                        item_instance = item_class.from_dict(item_data)  # ✅ Create the item instance
                        player.__inventory.append(item_instance)  # ✅ Append to instance inventory
                    else:
                        print(f"Error: {item_class_name} does not have a from_dict method")
        return player


    
    
    
    def restore_abilities(self):
        """Ensure player abilities are restored after loading."""
        for ability in self.abilities:
            ability.restore_state()  # If abilities store cooldowns, restore them
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
        current_time = pygame.time.get_ticks()
        if collidedDoor is not None  and current_time - self._lastDoorTeleportTime > 1000:
            self._lastDoorTeleportTime = current_time
            current_room = GameWorld.getInstance().getCurrentRoom()
            exit_direction = collidedDoor.getConnectedDoorDirection(current_room)
            exit_coords = {
                "N": (ViewUnits.SCREEN_WIDTH // 2, 200),
                "S": (ViewUnits.SCREEN_WIDTH // 2, ViewUnits.SCREEN_HEIGHT - 200), 
                "E": (ViewUnits.SCREEN_WIDTH - 200, ViewUnits.SCREEN_HEIGHT // 2),
                "W": (200, ViewUnits.SCREEN_HEIGHT // 2)
            }
            if exit_direction in exit_coords:
                teleport_x, teleport_y = exit_coords[exit_direction]
                self.teleportCharacter(teleport_x, teleport_y)


        collidedItem = GameWorld.getInstance().collideWithItem(pygame.Rect(new_x, new_y, 50, 50))
        
        if collidedItem is not None:
            self.pickup(collidedItem)

        if dx != 0 or dy != 0:
            """Character is moving"""
            self.update(CustomEvents.CHARACTER_MOVED)
        
        if theDirections:
            self._direction = theDirections[-1]  # Last key pressed is priority
    
    def pickup(self, item) -> None:
        """Add an item to the player's inventory if space is available."""
        if item._name == "KeyItem":
            self.keyCount += 1
        else:
            # Check for the first available slot (None)
            added = False
            for i in range(len(self.__inventory)):
                if self.__inventory[i] is None:  # Find the first empty slot
                    self.__inventory[i] = item  # Add the item to the empty slot
                    added = True
                    self.update("PICKUP_ITEM")  # Notify the game that the player picked up an item
                    break

            # If the inventory was full and no slot was available, display a message
            if not added:
                print("Inventory is full. Cannot pick up more items.")
            
            # Check if the inventory is now full after adding the item
            if None not in self.__inventory:
                self.invFull = True
        if self.__myFloorFactory.getKeyMin() <= self.keyCount:
            GameWorld.getInstance().setFoundKeys(True)

   
    def getInventory(self) -> list:
        return self.__inventory
    
    def use_item(self, idx) -> None:
        """Use the item from inventory at the specified index and replace it with None."""
        if idx < len(self.__inventory):  # Ensure the index is valid
            item = self.__inventory[idx]  # Get the item at the specified index
            
            if item is not None:  # Check if the item exists at the given index
                if str(item) == "MockItem":  # Check for a specific item type (MockItem in this case)
                    if not self._item_Ability.active:
                        self._item_Ability.use()  # Use the ability associated with the item
                        self.__inventory[idx] = None  # Replace the used item with None in the inventory
                        self.invFull = False  # Mark inventory as not full
                else:
                    # Handle other types of items (abilities, consumables, etc.)
                    # Replace the item with None once used
                    self.__inventory[idx] = None  # Replace the used item with None


        #else:
            #print("No items available to use!")
     
    def teleportCharacter(self, num1: int, num2: int) -> None:
        self._myPositionX = num1
        self._myPositionY = num2
        """If Character moves their sprite should be updated to location"""
        self.update(CustomEvents.CHARACTER_STOPPED)#might work

    
    def takeDamage(self, damage: int):
        if damage == 0.1:
            self._myHealth = 1000
            self.maxHealth = 1000
        else:
            self._myHealth -= damage
        # print("player health after damage: ",self._myHealth)
        self.update("HEALTH")
        if self._myHealth <= 0:
            self.Dies()


    def activate_ability(self):
        """Triggers the player's special ability when 'E' is pressed."""
        if self._ability:
            self._ability.use()


    def update(self, theEventName: str):
        if theEventName == CustomEvents.CHARACTER_MOVED:
            state = self._direction
        elif theEventName == CustomEvents.CHARACTER_STOPPED:
            state = ViewUnits.DEFAULT_STATE_NAME
        if theEventName == "CHARACTER_MOVED" or theEventName == "CHARACTER_STOPPED":
            event = pygame.event.Event(
                EventManager.event_types[theEventName],
                {"name": self.getName(),
                "positionX": self.getPositionX(),
                "positionY": self.getPositionY(),
                "state":state,
                "id": id(self)}        
            )
        elif theEventName == "HEALTH":
            event = pygame.event.Event(
                EventManager.event_types[theEventName],
                {"name": self.getName(),
                "health": self.getHealth(),
                "maxHealth": self.getMaxHealth()
                }        
            )
        elif theEventName == "PICKUP_ITEM":
            event = pygame.event.Event(
                EventManager.event_types[theEventName],
                {"name": self.getName(),
                "inventory": self.getInventory()}        
            )
        pygame.event.post(event)

    def getMaxHealth(self):
        return self.maxHealth
    
    def setMaxHealth(self, health):
        self.maxHealth = health
        self.update("HEALTH")

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
