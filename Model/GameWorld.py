from typing import Final
import pygame
from ViewUnits import ViewUnits
from CustomEvents import CustomEvents
from .Room import Room
from .EventManager import EventManager
from .FloorFactory import FloorFactory
from .Door import Door
class GameWorld:
    """Singleton class representing the game world with obstacles and enemies."""
    _instance = None  # Stores the single instance

    def __new__(cls):
        """Ensure only one instance is created."""
        if cls._instance is None:
            cls._instance = super(GameWorld, cls).__new__(cls)
            cls._instance._init_once()
        return cls._instance

    def _init_once(self):
        """Initialize the game world only once."""
        self.__myFloorFactory = FloorFactory.getInstance()
        self.__myFloor = self.__myFloorFactory.createFloor()
        self.currentRoom = self.__myFloor.getStartRoom()
        event = pygame.event.Event(
                EventManager.event_types[CustomEvents.CHANGED_ROOM],
                {
                    "roomtype": self.currentRoom.getRoomType(),
                    "doors":  self.currentRoom.getDoorMap(),
                    "cords": self.currentRoom.getCords(),
                    "direction": None
                }
            )
        pygame.event.post(event)
        self.__myFloor.print_dungeon()              
        self.enemies = []  # List of enemies
        self.player = None # player
        self.item = []
        self.last_damage_time = 0  # Track last damage taken
        self.projectiles = []


    @classmethod
    def getInstance(cls):
        """Getter for the singleton instance."""
        if cls._instance is None:  # Ensure an instance exists
            cls._instance = cls()  # This triggers __new__()
        return cls._instance

    def tick(self):
        self.currentRoom.checkState()
        for entity in self.projectiles:
            if entity.is_active:
                entity.moveCharacter()



    def addProjectile(self, theProjectile):
        self.projectiles.append(theProjectile)

    def getProjectiles(self):
        return self.projectiles
    
    def removeProjectile(self, theProjectile):
        self.projectiles.remove(theProjectile)
        
        event = pygame.event.Event(
                EventManager.event_types[CustomEvents.CHANGED_ROOM],
                {
                    "roomtype": self.currentRoom.getRoomType(),
                    "direction": None,
                    "cords": self.currentRoom.getCords(),
                    "doors":  self.currentRoom.getDoorMap()
                }
            )
        pygame.event.post(event)
    def get_enemies(self):
        """Return the list of enemies."""
        return self.enemies

    def add_enemy(self, enemy):
        """Add an enemy to the game world."""
        self.enemies.append(enemy)

    def setPlayer(self, player):
        """Add an enemy to the game world."""
        self.player = player

    def collideWithItem(self, thePlayerRect):
        """Checks if the player's rectangle collides with any item in the current room.
        If a collision is detected, remove the item from the room and return it."""
        items = self.currentRoom.get_items()
        for item in items:
            if thePlayerRect.colliderect(item.rect):
                # Remove the item from the room.
                items.remove(item)
                return item
        return None
    
    def getPlayer(self):
        """Returns the player object."""
        return self.player
    
    def removeEnemy(self, enemy):
        """Remove an enemy from the game world."""
        self.currentRoom.killEnemy(enemy)
        event = pygame.event.Event(
                EventManager.event_types[CustomEvents.CHANGED_ROOM],
                {
                    "roomtype": self.currentRoom.getRoomType(),
                    "direction": None,
                    "cords": self.currentRoom.getCords(),
                    "doors":  self.currentRoom.getDoorMap()
                }
            )
        pygame.event.post(event)

    
    def testRandomKillEnemy(self):
        self.currentRoom.randomKillEnemy()
        event = pygame.event.Event(
                EventManager.event_types[CustomEvents.CHANGED_ROOM],
                {
                    "roomtype": self.currentRoom.getRoomType(),
                    "direction": None,
                    "cords": self.currentRoom.getCords(),
                    "doors":  self.currentRoom.getDoorMap()
                }
            )
        pygame.event.post(event)
        
    def getCurrentRoom(self):
        return self.currentRoom
    
    def changeCurrentRoom(self, theDoor:Door):
        
        newRoom = theDoor.getConnectedRoom(self.currentRoom)
        #self.printCheckDirection(theDoor.getCardinalDirection(self.currentRoom))
        #print(self.currentRoom.getCords()," -> ", newRoom.getCords())
        oldRoom = self.currentRoom
        self.currentRoom = newRoom
        self.direction = theDoor.getConnectedDoorDirection(oldRoom)
        event = pygame.event.Event(
                EventManager.event_types[CustomEvents.CHANGED_ROOM],
                {
                    "roomtype": self.currentRoom.getRoomType(),
                    "direction": self.direction,
                    "cords": self.currentRoom.getCords(),
                    "doors":  self.currentRoom.getDoorMap()
                }
            )
        pygame.event.post(event)

    def activateRoom(self, theCurrentRoom):
        """Lets know doors and entities in room that should be shown on screen"""

    def check_collision(self, rect, ignore=None):
        """Check if a given rectangle collides with any obstacle or enemy."""
        current_time = pygame.time.get_ticks()  # Get current game time in milliseconds
        DAMAGE_COOLDOWN = 2000  # 2 seconds cooldown

        for enemy in self.currentRoom.getEnemyList().get_entities():
            if enemy != ignore:  # Don't check collision with itself
                enemy_rect = pygame.Rect(enemy.getPositionX(), enemy.getPositionY(), 50, 50)
                if rect.colliderect(enemy_rect):
                    if ignore is self.player and (current_time - self.last_damage_time > DAMAGE_COOLDOWN):
                        self.player.takeDamage(enemy.getAttackDamage())  # Only take damage if cooldown has passed
                        self.last_damage_time = current_time  # Reset cooldown timer
                    return True
                
        if self.player != ignore:  # Don't check collision with itself
            player_rect = pygame.Rect(self.player.getPositionX(), self.player.getPositionY(), 50, 50)
            if rect.colliderect(player_rect):
                if ignore in self.currentRoom.getEnemyList().get_entities() and (current_time - self.last_damage_time > DAMAGE_COOLDOWN):
                    self.player.takeDamage(ignore.getAttackDamage())  # Apply damage with cooldown
                    self.last_damage_time = current_time  # Reset cooldown timer
                return True

        return False  # No collision
        
    def check_projectile_collision(self, projectile):
        """Checks if a projectile collides with an enemy, player, or obstacle."""
        projectile_rect = pygame.Rect(projectile.getPositionX(), projectile.getPositionY(), 10, 10)
        
        room_width = ViewUnits.SCREEN_WIDTH
        room_height = ViewUnits.SCREEN_HEIGHT

        #  Check if the projectile is out of bounds
        if (projectile.getPositionX() < 0 or projectile.getPositionX() > room_width or
            projectile.getPositionY() < 0 or projectile.getPositionY() > room_height):
            # Destroy projectile if it goes outside the room
            return True  # Collision detected (out of bounds)
        
        # Check collision with enemies
        for enemy in self.currentRoom.getEnemyList().get_entities():
            if enemy.getName() is projectile.shooter:  #  Ignore the shooter
                continue

            enemy_rect = pygame.Rect(enemy.getPositionX(), enemy.getPositionY(), 50, 50)
            if projectile_rect.colliderect(enemy_rect):
                enemy.takeDamage(projectile.getAttackDamage())  # Apply projectile damage
                # projectile.Dies()  # Destroy projectile

                # self.updateWorld()
                return True  # Collision detected

        # Check collision with player (only if projectile was fired by an enemy)
        if projectile.shooter != self.player.getName():
            player_rect = pygame.Rect(self.player.getPositionX(), self.player.getPositionY(), 50, 50)
            if projectile_rect.colliderect(player_rect):
                self.player.takeDamage(projectile.getAttackDamage())  # Player takes damage
                # projectile.Dies()  # Destroy projectile
                # self.updateWorld()
                return True

        return False  # No collision

    def collideWithDoor(self, thePlayerRect) -> str:
        doormap = self.currentRoom.getDoorMap()
        for dir, door in doormap.items():
            if door is not None:
                
                doorRect = door.getDoorRect(dir)
                
                if thePlayerRect.colliderect(doorRect) and door.getState():
                    
                    self.changeCurrentRoom(door)
                    #self.printConnectedDoors(self.currentRoom)
                    return door.getConnectedDoorDirection(self.currentRoom)#maybe return cords
        return None
                