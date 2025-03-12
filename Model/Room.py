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
    def getEnemyList(self):
        return self.__myEnemyList
    def getCords(self):
        return [self.__myX,self.__myY]
    
    def getDoorMap(self):
        return self.__myDoorMap
    def __str__(self):
        # return f"Room({self.__myRoomType}, Doors: {self.doors})"
        return self.__myRoomType