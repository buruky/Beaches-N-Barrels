import pygame
from ViewUnits import ViewUnits
from CustomEvents import CustomEvents
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
        self.changedRoom = False
    
        event = pygame.event.Event(
                EventManager.event_types[CustomEvents.CHANGED_ROOM],
                {
                    "roomtype": self.currentRoom.getRoomType(),
                    "doors": self.currentRoom.getDoorPos(),
                    "cords": self.currentRoom.getCords(),
                    "direction": None
                }
            )
        pygame.event.post(event)
  
        # self.__myFloor.print_dungeon()           
        self.player = None # player
        self.item = []
        self.last_damage_time = 0  # Track last damage taken
        self.projectiles = []
        self._foundKeys = False
    @classmethod
    def getInstance(cls):
        """Getter for the singleton instance."""
        if cls._instance is None:  # Ensure an instance exists
            cls._instance = cls()  # This triggers __new__()
        return cls._instance
    @classmethod
    def reset_instance(cls):
        """Resets the singleton instance."""
        cls._instance = None  # This forces a new instance to be created
        
    def setDemo(self):
        """sets the floor or the demo map"""
        self.__myFloor = self.__myFloorFactory.createDemoFloor()
        self.currentRoom = self.__myFloor.getStartRoom()
        event = pygame.event.Event(
            EventManager.event_types[CustomEvents.CHANGED_ROOM],
            {
                "roomtype": self.currentRoom.getRoomType(),
                "doors": self.currentRoom.getDoorPos(),
                "cords": self.currentRoom.getCords(),
                "direction": None
            }
        )
        pygame.event.post(event)
    
    def loadWorld(self):
        """initializes gameworld for load"""
        self.player.update(CustomEvents.CHARACTER_MOVED)
        self.player.update(CustomEvents.HEALTH)
        self.player.update(CustomEvents.PICKUP_ITEM)

    def tick(self):
        "calls all of these thing for each tick"
        self.currentRoom.checkState()
        for entity in self.projectiles:
            if entity.is_active:
                entity.moveCharacter()
        for door in self.currentRoom.getDoorMap().values():
            if door is not None:
                connected_room = door.getConnectedRoom(self.currentRoom)
                if connected_room.getRoomType() == "b ":
                    if self.getFoundKeys():
                        door.toggleDoor(True)

                        break

                    else:
                        door.toggleDoor(False)

    def removeProjectile(self, theProjectile):
        """removes a projectile when it dies"""
        if theProjectile in self.projectiles:
            self.projectiles.remove(theProjectile)
            
            event = pygame.event.Event(
                    EventManager.event_types[CustomEvents.CHANGED_ROOM],
                    {
                        "roomtype": self.currentRoom.getRoomType(),
                        "direction": None,
                        "cords": self.currentRoom.getCords(),
                        "doors": self.currentRoom.getDoorPos()
                    }
                )
            pygame.event.post(event)

    def removeAllProjectiles(self):
        """removes all projectiles when room is changed"""
        self.projectiles.clear()
    
    def add_enemy(self, enemy):
        """Add an enemy to the game world."""
        self.enemies.append(enemy)
 
    def removeEnemy(self, enemy):
        """Remove an enemy from the game world."""
        self.currentRoom.killEnemy(enemy)
        event = pygame.event.Event(
                EventManager.event_types[CustomEvents.CHANGED_ROOM],
                {
                    "roomtype": self.currentRoom.getRoomType(),
                    "direction": None,
                    "cords": self.currentRoom.getCords(),
                    "doors": self.currentRoom.getDoorPos()
                }
            )
        pygame.event.post(event)

    def testRandomKillEnemy(self):
        "kills every enemy in the room for testing"
        self.currentRoom.randomKillEnemy()
        event = pygame.event.Event(
                EventManager.event_types[CustomEvents.CHANGED_ROOM],
                {
                    "roomtype": self.currentRoom.getRoomType(),
                    "direction": None,
                    "cords": self.currentRoom.getCords(),
                    "doors": self.currentRoom.getDoorPos()
                }
            )
        pygame.event.post(event)
    
    def changeCurrentRoom(self, theDoor:Door):
        "updates the current room"
        theDoor.isOpen = False
        newRoom = theDoor.getConnectedRoom(self.currentRoom)
        self.removeAllProjectiles()

        oldRoom = self.currentRoom
        self.currentRoom = newRoom
        self.direction = theDoor.getConnectedDoorDirection(oldRoom)
        event = pygame.event.Event(
                EventManager.event_types[CustomEvents.CHANGED_ROOM],
                {
                    "roomtype": self.currentRoom.getRoomType(),
                    "direction": self.direction,
                    "cords": self.currentRoom.getCords(),
                    "doors": self.currentRoom.getDoorPos()
                }
            )
        pygame.event.post(event)
        if self.currentRoom.getRoomType() == "n " :
            if self.changedRoom:
                event = pygame.event.Event(
                    EventManager.event_types["SONG_CHANGE"],
                    {"song": "MainTheme.mp3"
                    }        
                )
                pygame.event.post(event)
        else:
            self.changedRoom = True

    def collideWithItem(self, thePlayerRect):
        """Checks if the player's rectangle collides with any item in the current room.
        If a collision is detected, remove the item from the room and return it."""
        items = self.currentRoom.get_items() 
        
        for item in items:
            if item is None:
                continue
            if not self.player.invFull or str(item) == "Key":
                if thePlayerRect.colliderect(item.rect):
                    items.remove(item)
                    return item
        return None
    
    def collideWithDoor(self, thePlayerRect) -> str:
        "checks for collision with door only for the player"
        doormap = self.currentRoom.getDoorMap()
        for dir, door in doormap.items():
            if door is not None:
                
                doorRect = door.getDoorRect(dir)
                
                if thePlayerRect.colliderect(doorRect) and door.getState():
                    
                    self.changeCurrentRoom(door)
                    #self.printConnectedDoors(self.currentRoom)
                    #return door.getConnectedDoorDirection(self.currentRoom)#maybe return cords
                    return door
        return None
      
    def check_collision(self, rect, ignore=None):
        """Check if a given rectangle collides with any obstacle or enemy."""
        current_time = pygame.time.get_ticks()  # Get current game time in milliseconds
        DAMAGE_COOLDOWN = 2000  # 2 seconds cooldown

        for enemy in self.currentRoom.getEnemyList().get_entities():
            if enemy != ignore:  # Don't check collision with itself
                enemy_rect = enemy.getRect()
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
    
    def check_projectile_collision(self, projectile,isEnemy):
        """Checks if a projectile collides with an enemy, player, or obstacle."""
        projectile_rect = pygame.Rect(projectile.getPositionX(), projectile.getPositionY(), 10, 10)
        
        room_width = ViewUnits.SCREEN_WIDTH
        room_height = ViewUnits.SCREEN_HEIGHT

        #  Check if the projectile is out of bounds
        if (projectile.getPositionX() < 0 or projectile.getPositionX() > room_width or
            projectile.getPositionY() < 0 or projectile.getPositionY() > room_height):
            # Destroy projectile if it goes outside the room
            return True  # Collision detected (out of bounds)
        
        if isEnemy:
            player_rect = pygame.Rect(self.player.getPositionX(), self.player.getPositionY(), 50, 50)
            if projectile_rect.colliderect(player_rect):
                self.player.takeDamage(projectile.getAttackDamage())  # Player takes damage

                return True
        else:#player loop
            for enemy in self.currentRoom.getEnemyList().get_entities():
                enemy_rect = enemy.getRect()
                if projectile_rect.colliderect(enemy_rect):
                    enemy.takeDamage(projectile.getAttackDamage())  # Apply projectile damage

                    return True  # Collision detected
        return False  # No collision

    def setFoundKeys(self, theFound):
        """updates the found keys"""
        self._foundKeys = theFound
    
    def addProjectile(self, theProjectile):
        """add projectile when shot"""
        self.projectiles.append(theProjectile)

    def setPlayer(self, player):
        """Add an enemy to the game world."""
        self.player = player

    def getPlayer(self):
        """Returns the player object."""
        return self.player
    
    def getFoundKeys(self):
        """when this is true you can enter boss room"""
        return self._foundKeys
    
    def getFloor(self):
        """return the floor"""
        return self.__myFloor

    def get_enemies(self):
        """Return the list of enemies."""
        return self.enemies

    def getProjectiles(self):
        """returns the list of projectiles"""
        return self.projectiles
    
    def getCurrentRoom(self):
        """returns the current room"""
        return self.currentRoom
    
    def to_dict(self):
        """Serialize the entire GameWorld into a dictionary."""
        return {
            "current_room": self.currentRoom.getCords(),
            "floor": self.__myFloor.to_dict(),
            "player": self.player.to_dict() if self.player else None,
        }

    def load_from_dict(self, data):
        """Reconstruct GameWorld from a saved dictionary while ensuring player abilities are restored."""
        from .Floor import Floor
        from .Player import Player  # Ensure Player is imported

        self.__myFloor = Floor.from_dict(data["floor"])
        self.currentRoom = self.__myFloor.getRoomByCoords(tuple(data["current_room"]))

        #  Restore Player properly
        if data.get("player"):
            self.player = Player.from_dict(data["player"])  #  Load player

            # Ensure inventory is restored
            if hasattr(self.player, "restore_inventory"):
                self.player.restore_inventory()

        
        #  Ensure the dungeon is printed correctly
        # self.__myFloor.print_dungeon()
        #  Post event to update room state
        event = pygame.event.Event(
            EventManager.event_types[CustomEvents.CHANGED_ROOM],
            {
                "roomtype": self.currentRoom.getRoomType(),
                "doors": self.currentRoom.getDoorPos(),
                "cords": self.currentRoom.getCords(),
                "direction": None
            }
        )
        pygame.event.post(event)

        # Ensure player updates correctly after loading
        self.loadWorld()


    


 
