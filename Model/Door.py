import pygame
from .Room import Room
from ViewUnits import ViewUnits

class Door:
    theCordMap = {
        "S": (ViewUnits.SOUTH_DOOR_CORD),  # Centered at the top
        "W": (ViewUnits.WEST_DOOR_CORD),  # Right side
        "N": (ViewUnits.NORTH_DOOR_CORD),  # Bottom
        "E": (ViewUnits.EAST_DOOR_CORD)  # Left side
    }

    def __init__(self, theFirstDirection:str,theEndDirection:str, theFirstRoom:Room = None,  theEndRoom:Room = None):
        
        self.__myFirstDirection = theFirstDirection  # "N", "S", "E", "W"
        self.__myEndDirection = theEndDirection       

        self.__myFirstRoom = theFirstRoom
        self.__myEndRoom = theEndRoom
        
        self.__myFirstDoorRect = self.__getDoorPositionRect(self.__myFirstDirection)
        self.__myEndDoorRect = self.__getDoorPositionRect(self.__myEndDirection)
        self.isOpen = False
    

    
    def __getDoorPositionRect(self, theDirection):
        return pygame.Rect(Door.theCordMap[theDirection], (50,50))
    
    
    def getConnectedRoom(self, theOtherRoom:Room) -> Room:
        str1 = str(theOtherRoom.getCords()) + " "
        if theOtherRoom is self.__myFirstRoom:
            str1 += str(self.__myFirstDirection) + " -> " + str(self.__myEndRoom.getCords()) + " " + str(self.__myEndDirection)
            # print(str1)
            return self.__myEndRoom
        elif theOtherRoom is self.__myEndRoom:
            str1 += str(self.__myEndDirection) + " -> " + str(self.__myFirstRoom.getCords()) + " " + str(self.__myFirstDirection)
            # print(str1)
            return self.__myFirstRoom
        else:
            raise Exception("Door.getConnectedRoom:",
                        "THE ROOM PASSED IS NOT CONNECTED TO THIS DOOR!!!") 
    def toggleDoor(self, theNewState:bool):
        self.isOpen = theNewState

    def getState(self):
        return self.isOpen
        
    def getBothRect(self) ->tuple:
        return (self.__myFirstDoorRect, self.__myEndDoorRect)
    
    def getRect(self,theDirection):
        if theDirection == self.__myFirstDirection:
            return self.__myFirstDoorRect
        elif theDirection == self.__myEndDirection:
            return self.__myEndDoorRect
        raise Exception("Door.getRECT:",
                        "THERE IS NO RECT WITH THAT DIRECTION IN THIS DOOR")
    
    def getConnectedDoorDirection(self, theOtherRoom:Room):
        if theOtherRoom is self.__myFirstRoom:
            return self.__myFirstDirection
        elif theOtherRoom is self.__myEndRoom:
            return self.__myEndDirection
        else:
            raise Exception("Door.getConnectedDirection:",
                        "THE OTHER ROOM IS NOT CONNECTED TO THIS DOOR!!!")
    
    def getDoorRect(self, theDirection:str) -> pygame.Rect:
        if theDirection == self.__myFirstDirection:
            return self.__myEndDoorRect
        elif theDirection == self.__myEndDirection:
            return self.__myFirstDoorRect
        else:
            raise Exception("Door.getDoorRect:",
                        "NO direction associated with this door!!!")
    def getCardinalDirection(self, theOtherRoom:Room):
        if theOtherRoom is self.__myFirstRoom:
            return self.__myEndDirection
        elif theOtherRoom is self.__myEndRoom:
            return self.__myFirstDirection
        else:
            raise Exception("Door.getConnectedDirection:",
                        "THE OTHER ROOM IS NOT CONNECTED TO THIS DOOR!!!")
    
    def collides_with(self, player_rect):
        return self.rect.colliderect(player_rect)
