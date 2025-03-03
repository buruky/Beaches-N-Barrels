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
        
    def getRoomType(self):
        return self.__myRoomType
    def getEnemyList(self):
        return self.__myEnemyList
    
    def getDoorMap(self):
        return self.__myDoorMap
    def __str__(self):
        # return f"Room({self.__myRoomType}, Doors: {self.doors})"
        return self.__myRoomType