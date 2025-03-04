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
        self.__myFloor = self.__myFloorFactory.createFloor(GameWorld._FLOOR_SIDE_LENGTH, GameWorld._FLOOR_SIDE_LENGTH)
        self.currentRoom = self.__myFloor.getStartRoom()
        event = pygame.event.Event(
                EventManager.event_types[CustomEvents.CHANGED_ROOM],
                {
                    "roomtype": self.currentRoom.getRoomType(),
                    "direction": None
                }
            )
        pygame.event.post(event)
        self.__myFloor.print_dungeon()              
        self.enemies = []  # List of enemies
        self.player = [] # player
        self.item = []

    @classmethod
    def getInstance(cls):
        """Getter for the singleton instance."""
        if cls._instance is None:  # Ensure an instance exists
            cls._instance = cls()  # This triggers __new__()
        return cls._instance

    # def go(self):
    #     doorMap = self.currentRoom.getDoorMap()
    #     for direction in doorMap.keys():
    #         print()
    #         if doorMap[direction] is not None:
    #             print("go:map ",self.currentRoom.getDoorMap())
    #             print("direction: ",direction)
    #             newRoom = doorMap[direction].getConnectedRoom(self.currentRoom)
    #             self.currentRoom = newRoom
    #     event = pygame.event.Event(
    #             EventManager.event_types[CustomEvents.CHANGED_ROOM],
    #             {
    #                 "roomName": self.currentRoom.getRoomType(),
    #                 "direction": self.currentRoom
    #             }
    #         )
    #     pygame.event.post(event)



    def tick(self):
        self.currentRoom.getEnemyList().update_all()


    def get_enemies(self):
        """Return the list of enemies."""
        return self.enemies

    def add_enemy(self, enemy):
        """Add an enemy to the game world."""
        self.enemies.append(enemy)

    def add_player(self, player):
        """Add an enemy to the game world."""
        self.player.append(player)

    def remove_enemy(self, enemy):
        """Remove an enemy from the game world."""
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def getCurrentRoom(self):
        return self.currentRoom
    
    def changeCurrentRoom(self, theDoor:Door):
        print("changeCurrentRoom")
        newRoom = theDoor.getConnectedRoom(self.currentRoom)
        #self.printCheckDirection(theDoor.getCardinalDirection(self.currentRoom))
        #print(self.currentRoom.getCords()," -> ", newRoom.getCords())
        oldRoom = self.currentRoom
        self.currentRoom = newRoom
        event = pygame.event.Event(
                EventManager.event_types[CustomEvents.CHANGED_ROOM],
                {
                    "roomtype": self.currentRoom.getRoomType(),
                    "direction": theDoor.getConnectedDoorDirection(oldRoom)
                }
            )
        pygame.event.post(event)

    def activateRoom(self, theCurrentRoom):
        """Lets know doors and entities in room that should be shown on screen"""

    def check_collision(self, rect, ignore=None):
        """Check if a given rectangle collides with any obstacle or enemy."""
        for enemy in self.currentRoom.getEnemyList().get_entities():
            if enemy != ignore:  # Don't check collision with itself
                enemy_rect = pygame.Rect(enemy.getPositionX(), enemy.getPositionY(), 50, 50)
                if rect.colliderect(enemy_rect):
                    if ignore in self.player:
                        ignore.Dies()
                    #print(f"Collision with another enemy at ({enemy.getPositionX()}, {enemy.getPositionY()})")  # Debugging
                    return True
                
        for player in self.player:
            if player != ignore:  # Don't check collision with itself
                my_rect = pygame.Rect(player.getPositionX(), player.getPositionY(), 50, 50)
                if rect.colliderect(my_rect):
                    if ignore in self.currentRoom.getEnemyList().get_entities():
                        player.Dies()
                    #print(f"Collision with the player at ({player.getPositionX()}, {player.getPositionY()})")  # Debugging
                    return True
            return False  # No collision
        

    def collideWithDoor(self, thePlayerRect) -> str:
        doormap = self.currentRoom.getDoorMap()
        for dir, door in doormap.items():
            if door is not None:
                
                doorRect = door.getDoorRect(dir)
                
                if thePlayerRect.colliderect(doorRect):
                    
                    self.changeCurrentRoom(door)
                    #self.printConnectedDoors(self.currentRoom)
                    return door.getConnectedDoorDirection(self.currentRoom)#maybe return cords
        return None
                    

    def printCheckDirection(self,theDir):
        if theDir == "N":
            print("N (-1,0)")
        elif theDir == "S":
            print("S (1,0)")

        elif theDir == "W":
            print("W (0,-1)")
        elif theDir == "E":
            print("E (0,1)")

    def printConnectedDoors(self,theRoom:Room):
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
