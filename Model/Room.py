import pygame
from .DungeonCharacterList import DungeonCharacterList
import copy
from ViewUnits import ViewUnits

class Room:
    """
    Represents a single room in the dungeon or map grid.

    Each room can have:
    - Doors connecting to neighboring rooms in cardinal directions.
    - A list of enemies currently in the room.
    - A collection of items that can be picked up.
    - A room type (e.g., start room, boss room, key room).

    This class manages door access, enemy state, and serialization of room contents.
    """
    DoorMap ={
        "N":None,
        "E":None,
        "S":None,
        "W":None
    }

    def __init__(self, theRoomType, theX, theY, theEnemyList: DungeonCharacterList):
        """initializes the room"""
        self.__myDoorMap = copy.copy(Room.DoorMap)
        self.__myRoomType = theRoomType
        self.__myX, self.__myY = theX, theY
        
        self.rect = pygame.Rect(0,0,ViewUnits.SCREEN_WIDTH, ViewUnits.SCREEN_HEIGHT)
        self.__myEnemyList = theEnemyList
        self.__items = []

    def getDoorPos(self):
        """
        Returns a dictionary of directions (e.g., 'N', 'S', 'E', 'W') where doors exist.

        :return: Dictionary with direction keys mapped to True if a door exists.
        """
        dirToBool = dict()
        for dir in self.__myDoorMap.keys():
            if self.__myDoorMap[dir] is not None:
                dirToBool[dir] = True
        return dirToBool

    def addDoor(self, theDirection, theDoor):
        """
        Adds a door to the room in the specified direction.

        :param theDirection: The cardinal direction (e.g., 'N', 'S', 'E', 'W').
        :param theDoor: The Door object to be added.
        """
        self.__myDoorMap[theDirection] = theDoor

    def checkState(self):
        """
        Checks whether there are enemies in the room.
        If not, opens all connected doors.
        """
        if len(self.__myEnemyList.get_entities()) > 0:
            self.__myEnemyList.update_all()
        else:
            self.openRooms()

    def openRooms(self):
        """
        Opens all doors in the room by toggling their state to open.
        """
        for door in self.__myDoorMap.values():
            if door is not None:
                door.toggleDoor(True)

    def randomKillEnemy(self):
        """
        Removes all enemies from the room if any exist. Otherwise, prints a message.
        """
        if len(self.__myEnemyList.get_entities()) > 0:
            self.__myEnemyList.deleteAllEnemy()
        
    def killEnemy(self, theEnemy):
        """
        Removes a specific enemy from the room.

        :param theEnemy: The enemy object to be removed.
        """
        self.__myEnemyList.deleteEnemy(theEnemy)

    def getRoomType(self):
        """
        Returns the type of the room (e.g., 's ', 'b ', 'n ', etc.).

        :return: A string representing the room type.
        """
        return self.__myRoomType

    def setRoomType(self, new_type: str) -> None:
        """
        Sets the room's type to a new value.

        :param new_type: A string representing the new room type.
        """
        self.__myRoomType = new_type

    def getEnemyList(self):
        """
        Returns the enemy list object associated with this room.

        :return: Enemy list object.
        """
        return self.__myEnemyList

    def getCords(self):
        """
        Returns the room's (x, y) grid coordinates.

        :return: A list [x, y] of the room's position.
        """
        return [self.__myX, self.__myY]

    def add_item(self, item):
        """
        Adds an item to the room's item list.

        :param item: The item to add.
        """
        self.__items.append(item)

    def get_items(self):
        """
        Returns the list of items currently in the room.

        :return: List of items.
        """
        return self.__items

    def getDoorMap(self):
        """
        Returns the dictionary mapping directions to connected Door objects.

        :return: Dictionary of {direction: Door}.
        """
        return self.__myDoorMap

    def __str__(self):
        """
        Returns a string representation of the room, showing its type.

        :return: String describing the room type.
        """
        return self.__myRoomType

    def to_dict(self):
        """Convert Room to a dictionary for serialization."""
        # print({direction: door.to_dict() for direction, door in self.__myDoorMap.items() if door})
        return {
            "room_type": self.__myRoomType,
            "x": self.__myX,
            "y": self.__myY,
            "enemy_list": self.__myEnemyList.to_dict(),  # Serialize enemies
            "items": [item.to_dict() for item in self.__items],  # Serialize items
            "doors": {direction: door.to_dict() for direction, door in self.__myDoorMap.items() if door},
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruct a Room from a dictionary."""
        from .DungeonCharacterList import DungeonCharacterList
        from .Door import Door

        enemy_list = DungeonCharacterList.from_dict(data["enemy_list"])  # Restore enemies
        
        room = cls(data["room_type"], data["x"], data["y"], enemy_list)
        from .Item import UsableItem
        # room.__items = [UsableItem.from_dict(item_data) for item_data in data["items"]]  # Restore items
        room.__myDoorMap = {direction: Door.from_dict(door) for direction, door in data["doors"].items()}
        # print("GGGGGGGGGG")
        return room  