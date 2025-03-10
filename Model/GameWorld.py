from typing import Final
import pygame
from CustomEvents import CustomEvents
from .Room import Room
from .EventManager import EventManager
from .FloorFactory import FloorFactory
from .Door import Door
class GameWorld:
    """Singleton class representing the game world with obstacles and enemies."""
    _FLOOR_SIDE_LENGTH:Final = 11
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


    @classmethod
    def getInstance(cls):
        """Getter for the singleton instance."""
        if cls._instance is None:  # Ensure an instance exists
            cls._instance = cls()  # This triggers __new__()
        return cls._instance

    def tick(self):
        self.currentRoom.checkState()


    def get_enemies(self):
        """Return the list of enemies."""
        return self.enemies

    def add_enemy(self, enemy):
        """Add an enemy to the game world."""
        self.enemies.append(enemy)

    def setPlayer(self, player):
        """Add an enemy to the game world."""
        self.player = player

    def getPlayer(self):
        """Returns the player object."""
        return self.player
    
    def removeEnemy(self, enemy):
        """Remove an enemy from the game world."""
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def testRandomKillEnemy(self):
        self.currentRoom.randomKillEnemy()
        
    def getCurrentRoom(self):
        return self.currentRoom
    
    def changeCurrentRoom(self, theDoor:Door):
        
        newRoom = theDoor.getConnectedRoom(self.currentRoom)
        #self.printCheckDirection(theDoor.getCardinalDirection(self.currentRoom))
        #print(self.currentRoom.getCords()," -> ", newRoom.getCords())
        oldRoom = self.currentRoom
        self.currentRoom = newRoom
        event = pygame.event.Event(
                EventManager.event_types[CustomEvents.CHANGED_ROOM],
                {
                    "roomtype": self.currentRoom.getRoomType(),
                    "direction": theDoor.getConnectedDoorDirection(oldRoom),
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
                        self.player.takeDamage(150)  # Only take damage if cooldown has passed
                        self.last_damage_time = current_time  # Reset cooldown timer
                    return True
                
        if self.player != ignore:  # Don't check collision with itself
            player_rect = pygame.Rect(self.player.getPositionX(), self.player.getPositionY(), 50, 50)
            if rect.colliderect(player_rect):
                if ignore in self.currentRoom.getEnemyList().get_entities() and (current_time - self.last_damage_time > DAMAGE_COOLDOWN):
                    self.player.takeDamage(150)  # Apply damage with cooldown
                    self.last_damage_time = current_time  # Reset cooldown timer
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
                    

    # def printCheckDirection(self,theDir):
    #     if theDir == "N":
    #         print("N (-1,0)")
    #     elif theDir == "S":
    #         print("S (1,0)")

    #     elif theDir == "W":
    #         print("W (0,-1)")
    #     elif theDir == "E":
    #         print("E (0,1)")

    # def printConnectedDoors(self,theRoom:Room):
        '''prints rooms adjacent to room passed in using doors'''
        adjacentDoors = [
            [".",       None,       "."],
            [None,theRoom.getCords(),None],
            [".",       None,       "."]
        ]
        
        doormap = theRoom.getDoorMap()
        for dir in doormap.keys():
            if doormap[dir] != None:
                cords = doormap[dir].getConnectedRoom(theRoom).getCords()
                if dir == "N":
                    adjacentDoors[0][1] = cords
                elif dir == "S":
                    adjacentDoors[2][1] = cords
                elif dir == "W":
                    adjacentDoors[1][0] = cords
                elif dir == "E":
                    adjacentDoors[1][2] = cords

        print(adjacentDoors[0])
        print(adjacentDoors[1])
        print(adjacentDoors[2])
