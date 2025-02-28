import pygame
from .Room import Room

class Door:
    theCordMap ={
        "N":(350,0),
        "E":(800,250),
        "S":(350,600),
        "W":(0,250)
    }
    def __init__(self, theFirstDirection:str,theEndDirection:str, theFirstRoom:Room = None,  theEndRoom:Room = None):
        
        self.__myFirstDirection = theFirstDirection  # "N", "S", "E", "W"
        self.__myEndDirection = theEndDirection       

        self.__myFirstRoom = theFirstRoom
        self.__myEndRoom = theEndRoom
        
        self.__myFirstDoorRect = self.__getDoorPositionRect(self.__myFirstDirection)
        self.__myEndDoorRect = self.__getDoorPositionRect(self.__myEndDirection)
        
    def __getDoorPositionRect(self, theDirection):
        return pygame.Rect(Door.theCordMap[theDirection], (50,50))
    def getConnectedRoom(self, theOtherRoom:Room) -> Room:
        if theOtherRoom is self.__myFirstRoom:
            return self.__myEndRoom
        elif theOtherRoom is self.__myEndRoom:
            return self.__myFirstRoom
        else:
            raise Exception("Door.getConnectedRoom:",
                        "THE OTHER ROOM IS NOT CONNECTED TO THIS DOOR!!!") 
    def getRect(self):
        return self.rect
    
    def getConnectedDoorDirection(self, theOtherRoom:Room):
        if theOtherRoom is self.__myFirstRoom:
            return self.__myFirstDirection
        elif theOtherRoom is self.__myEndRoom:
            return self.__myEndDirection
        else:
            raise Exception("Door.getConnectedDirection:",
                        "THE OTHER ROOM IS NOT CONNECTED TO THIS DOOR!!!")
    
    def collides_with(self, player_rect):
        return self.rect.colliderect(player_rect)
