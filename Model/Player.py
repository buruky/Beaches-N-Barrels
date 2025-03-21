from typing import Final
from ViewUnits import ViewUnits
from .DungeonCharacter import DungeonCharacter
from .EventManager import EventManager
from CustomEvents import CustomEvents
from .GameWorld import GameWorld
from .Abilities import HealAbility
from .Abilities import SpeedBoostAbility,Invincibility
from .FloorFactory import FloorFactory
from .Item import *
import pygame
from .Abilities import InvincibilityAbility
import os

class Player(DungeonCharacter):
    """Parent class for all player heroes with shared movement and event handling."""
    MAX_INVENTORY_SIZE: Final = 4
    
    def __init__(self, name: str, speed: int, health: int, damage: int):

        super().__init__(damage, health, ViewUnits.PLAYER_START_X, ViewUnits.PLAYER_START_Y, speed)  # Default attackDamage = 50
        self._myHealth = health
        self.maxHealth = health
        self._name = name
        self._direction = "LEFT"  # Default direction
        self._ability = None  # To be set by subclasses
        self.__myFloorFactory = FloorFactory.getInstance()
        self.keyCount = 0
        self.invFull = False
        self.__inventory = [None,None,None,None]
        self._item_Ability = HealAbility(self)
        self._item_Invincibility = InvincibilityAbility(self)
        self._item_Speed = SpeedBoostAbility(self)
        self._invincibility = Invincibility(self)
        self._canDie = True
        self._lastDoorTeleportTime = 0
        assets_path = os.path.join(os.path.dirname(__file__), "..", "Assets/sounds")
 
        self.pickup_sound = pygame.mixer.Sound(os.path.join(assets_path, "item.mp3"))  # A sound effect

        # Set individual sound volumes
        self.pickup_sound.set_volume(0.4)
        
        """Update sprite when player is made"""
        self.update(CustomEvents.CHARACTER_STOPPED)

    def restore_abilities(self):
        """Ensure player abilities are restored after loading."""
        for ability in self.abilities:
            ability.restore_state()  # If abilities store cooldowns, restore them
    
    def moveCharacter(self, theDirections: list) -> None:
        """
        Moves the player character based on the input direction.

        :param theDirections: A list of movement directions (UP, DOWN, LEFT, RIGHT).
        """
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

        new_x = max(25, min(ViewUnits.SCREEN_WIDTH - ViewUnits.DEFAULT_WIDTH - 25, new_x))
        new_y = max(0, min(ViewUnits.SCREEN_HEIGHT - ViewUnits.DEFAULT_HEIGHT - 35, new_y))

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
                self._invincibility.use()


        collidedItem = GameWorld.getInstance().collideWithItem(pygame.Rect(new_x, new_y, 50, 50))
        
        if collidedItem is not None:
            self.pickup(collidedItem)

        if dx != 0 or dy != 0:
            """Character is moving"""
            self.update(CustomEvents.CHARACTER_MOVED)
        
        if theDirections:
            self._direction = theDirections[-1]  # Last key pressed is priority
    
    def teleportCharacter(self, num1: int, num2: int) -> None:
        """
        Instantly moves the player to a new position.

        :param num1: X coordinate.
        :param num2: Y coordinate.
        """
        self._myPositionX = num1
        self._myPositionY = num2
        """If Character moves their sprite should be updated to location"""
        self.update(CustomEvents.CHARACTER_STOPPED)#might work
   
    def pickup(self, item) -> None:
        """Add an item to the player's inventory if space is available."""
        if item._name == "KeyItem":
            self.keyCount += 1
            self.pickup_sound.play()
            self.update("PICKUP_KEY")
        else:
            # Check for the first available slot (None)
            added = False
            for i in range(len(self.__inventory)):
                if self.__inventory[i] is None:  # Find the first empty slot
                    self.__inventory[i] = item  # Add the item to the empty slot
                    added = True
                    self.pickup_sound.play()
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
    
    def use_item(self, idx) -> None:
        """
        Uses an item from the player's inventory at the given index.

        :param idx: Index of the item in the inventory.
        """
        if idx < len(self.__inventory):
            item = self.__inventory[idx]
            if item is not None:
                if item._name == "MockItem" and not self._item_Ability.active:
                    self._item_Ability.use()
                    self.__inventory[idx] = None
                    self.invFull = False
                elif item._name == "InvincibilityItem" and not self._item_Invincibility.active:
                    self._item_Invincibility.use()
                    self.__inventory[idx] = None
                    self.invFull = False
                elif item._name == "SpeedItem" and not self._item_Speed.active:
                    self._item_Speed.use()
                    self.__inventory[idx] = None
                    self.invFull = False
                #else:
                    # Handle other types of items (abilities, consumables, etc.)
                    # Replace the item with None once used
                    # print("No usable item at this slot or ability on cooldown.")
                    # self.__inventory[idx] = None  # Replace the used item with None
    
    def activate_ability(self):
        """Triggers the player's special ability when 'E' is pressed."""
        if self._ability:
            self._ability.use()
    
    def takeDamage(self, damage: int):
        """
        Reduces the player's health by the given damage amount.

        :param damage: The amount of damage taken.
        """
        if damage == 0.1:
            self._myHealth = 1000
            self.maxHealth = 1000
        else:
            if self._canDie == True:
                self._myHealth -= damage
        # print("player health after damage: ",self._myHealth)
        self.update("HEALTH")
        if self._myHealth <= 0 :
            self.Dies()
    
    def Dies(self) -> None:
        """Trigger death event"""
        death_event = pygame.event.Event(EventManager.event_types[CustomEvents.PLAYER_DIED])
        pygame.event.post(death_event)
    
    def setCanDie(self,canDie):
        """
        Toggles whether the player can die.

        :param canDie: Boolean value indicating if the player can die.
        """
        self._canDie = canDie
    
    def getInventory(self) -> list:
        """
        Returns the player's inventory.

        :return: List of items in the inventory.
        """
        return self.__inventory
    
    def setMaxKeys(self):
        """
        Sets the maximum number of keys as found.
        """
        GameWorld.getInstance().setFoundKeys(True)
    
    def getKey(self):
        """
        Returns the number of keys the player has.

        :return: Number of keys.
        """
        return  self.keyCount
    
    def update(self, theEventName: str):
        """
        Updates the player's state and dispatches relevant events.

        :param theEventName: Name of the event to update.
        """
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
        elif theEventName == "PICKUP_KEY":
            event = pygame.event.Event(
                EventManager.event_types[theEventName],
                {"name": self.getName(),
                "keyInventory": self.getKey()}        
            )
        pygame.event.post(event)
    
    def update_items(self) -> None:
        """
        Updates each item in the player's inventory so that cooldowns are tracked.
        Call this in your game loop tick.
        """
        for item in self.__inventory:
            item.update(self)
    
    def getMaxHealth(self):
        """
        Returns the player's maximum health.

        :return: Maximum health value.
        """
        return self.maxHealth
    
    def setMaxHealth(self, health):
        """
        Sets the player's maximum health.

        :param health: New maximum health value.
        """
        self.maxHealth = health
        self.update("HEALTH")
    
    def getPositionX(self) -> int:
        """
        Returns the player's current X-coordinate.

        :return: X position of the player.
        """
        return self._myPositionX
    
    def getHealth(self):
        """
        Returns the player's current health.

        :return: Health value.
        """
        return self._myHealth
    
    def getPositionY(self) -> int:
        """
        Returns the player's current Y-coordinate.

        :return: Y position of the player.
        """
        return self._myPositionY
    
    def getName(self):
        """
        Returns the player's name.

        :return: Name of the player.
        """
        return self._name
    
    def setDamage(self, damage):
        """
        Sets the player's attack damage.

        :param damage: New attack damage value.
        """
        self._myAttackDamage = damage
    
    def getAttackDamage(self) -> int:
        """
        Returns the player's current attack damage.

        :return: Attack damage value.
        """
        return self._myAttackDamage 
    
    def toString(self) -> str:
        """
        Returns a string representation of the player's state.

        :return: String describing the player's name and position.
        """
        return f"{self._name} at ({self._myPositionX}, {self._myPositionY})"

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
            "class": self.__class__.__name__,  
            "keys": self.keyCount
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

        #  If the class is Dolphin/Buddha (no init params), just instantiate
        if player_class in [Dolphin, Buddha, Astronaut]:
            player = player_class()
        else:
            player = player_class(data["name"], data["speed"], data["health"], data["damage"])

        # Restore base attributes
        player._myPositionX = data["positionX"]
        player._myPositionY = data["positionY"]
        player._direction = data["direction"]
        player.keyCount = data["keys"]
        player.update("PICKUP_KEY")

        #  Restore inventory correctly on the instance
        if "inventory" in data:
            from .Item import UsableItem  # Ensure item classes are imported
            player.__inventory = []
            
            for item_data in data["inventory"]:
                if item_data is None:
                    player.__inventory.append(None)  #  Preserve None values
                else:
                    item_class_name = item_data.get("class", "UsableItem")  # Default to UsableItem
                    item_class = globals().get(item_class_name, UsableItem)  # Find the correct item class

                    if hasattr(item_class, 'from_dict'):
                        item_instance = item_class.from_dict(item_data)  #  Create the item instance
                        player.__inventory.append(item_instance)  #  Append to instance inventory
                    else:
                        print(f"Error: {item_class_name} does not have a from_dict method")
        return player

