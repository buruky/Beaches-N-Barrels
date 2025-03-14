import pygame
from .DungeonCharacterList import DungeonCharacterList
import copy
from ViewUnits import ViewUnits

class Room:
    DoorMap ={
        "N":None,
        "E":None,
        "S":None,
        "W":None
    }

    def __init__(self, theRoomType, theX, theY, theEnemyList: DungeonCharacterList):
        self.__myDoorMap = copy.copy(Room.DoorMap)
        self.__myRoomType = theRoomType
        self.__myX, self.__myY = theX, theY
        
        self.rect = pygame.Rect(0,0,ViewUnits.SCREEN_WIDTH, ViewUnits.SCREEN_HEIGHT)
        self.__myEnemyList = theEnemyList
        self.__items = []

    
    def to_dict(self):
        """Convert Room to a dictionary for serialization."""
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
        return room  



    def addDoor(self, theDirection, theDoor):
        self.__myDoorMap[theDirection] = theDoor
        
    def checkState(self):
        if len(self.__myEnemyList.get_entities()) > 0:
            self.__myEnemyList.update_all()
        else:
            self.openRooms()

    def openRooms(self):
        for door in self.__myDoorMap.values():
            if door is not None:
                door.toggleDoor(True)

    def addDoor(self, theDirection, theDoor):
        self.__myDoorMap[theDirection] = theDoor

    def randomKillEnemy(self):
        if len(self.__myEnemyList.get_entities()) > 0:
            self.__myEnemyList.deleteAllEnemy()
        else:
            print("They are dead!")
    
    def killEnemy(self, theEnemy):
        self.__myEnemyList.deleteEnemy(theEnemy)
        
    def getRoomType(self):
        return self.__myRoomType
    def setRoomType(self, new_type: str) -> None:
        self.__myRoomType = new_type
    def getEnemyList(self):
        return self.__myEnemyList
    def getCords(self):
        return [self.__myX,self.__myY]
    def add_item(self, item):
        self.__items.append(item)
    def get_items(self):
        return self.__items
    def getDoorMap(self):
        return self.__myDoorMap
    def __str__(self):
        # return f"Room({self.__myRoomType}, Doors: {self.doors})"
        return self.__myRoomType