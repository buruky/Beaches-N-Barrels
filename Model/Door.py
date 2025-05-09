import pygame
from .Room import Room
from ViewUnits import ViewUnits

class Door:
    """coors that reference two connected rooms"""
    theCordMap = {
        "S": (ViewUnits.SOUTH_DOOR_CORD),  # Centered at the top
        "W": (ViewUnits.WEST_DOOR_CORD),  # Right side
        "N": (ViewUnits.NORTH_DOOR_CORD),  # Bottom
        "E": (ViewUnits.EAST_DOOR_CORD)  # Left side
    }

    def __init__(self, theFirstDirection:str,theEndDirection:str, theFirstRoom:Room = None,  theEndRoom:Room = None):
        """initializes the doors"""
        self.__myFirstDirection = theFirstDirection  # "N", "S", "E", "W"
        self.__myEndDirection = theEndDirection       

        self.__myFirstRoom = theFirstRoom
        self.__myEndRoom = theEndRoom
        
        self.__myFirstDoorRect = self.__getDoorPositionRect(self.__myFirstDirection)
        self.__myEndDoorRect = self.__getDoorPositionRect(self.__myEndDirection)
        self.isOpen = False
    
    def __getDoorPositionRect(self, theDirection):
        """returns the position rect"""
        return pygame.Rect(Door.theCordMap[theDirection], (50,50))
    
    def getConnectedRoom(self, theOtherRoom:Room) -> Room:
        """returns the connected rooms"""
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
        """toggles the door"""
        boss_room = False
        if self.__myFirstRoom.getRoomType() == "b ":
            boss_room = True
        elif self.__myEndRoom.getRoomType() == "b ":
            boss_room = True

        if boss_room and not theNewState:
            self.isOpen = False
        else:
            self.isOpen = theNewState

    def getState(self):
        """returns the state of the room"""
        return self.isOpen
        
    def getBothRect(self) ->tuple:
        """returns the rect of both rooms directions"""
        return (self.__myFirstDoorRect, self.__myEndDoorRect)
    
    def getRect(self,theDirection):
        """returns the door rect"""
        if theDirection == self.__myFirstDirection:
            return self.__myFirstDoorRect
        elif theDirection == self.__myEndDirection:
            return self.__myEndDoorRect
        raise Exception("Door.getRECT:",
                        "THERE IS NO RECT WITH THAT DIRECTION IN THIS DOOR")
    
    def getConnectedDoorDirection(self, theOtherRoom:Room):
        """returns the doors direction"""
        if theOtherRoom is self.__myFirstRoom:
            return self.__myFirstDirection
        elif theOtherRoom is self.__myEndRoom:
            return self.__myEndDirection
        else:
            raise Exception("Door.getConnectedDirection:",
                        "THE OTHER ROOM IS NOT CONNECTED TO THIS DOOR!!!")
    
    def getDoorRect(self, theDirection:str) -> pygame.Rect:
        """returns the door rect"""
        if theDirection == self.__myFirstDirection:
            return self.__myEndDoorRect
        elif theDirection == self.__myEndDirection:
            return self.__myFirstDoorRect
        else:
            raise Exception("Door.getDoorRect:",
                        "NO direction associated with this door!!!")
    
    def getCardinalDirection(self, theOtherRoom:Room):
        """gets cardinal direction"""
        if theOtherRoom is self.__myFirstRoom:
            return self.__myEndDirection
        elif theOtherRoom is self.__myEndRoom:
            return self.__myFirstDirection
        else:
            raise Exception("Door.getConnectedDirection:",
                        "THE OTHER ROOM IS NOT CONNECTED TO THIS DOOR!!!")
    
    def collides_with(self, player_rect):
        """checks if palyer is colliding with the door"""
        return self.rect.colliderect(player_rect)
    
    def to_dict(self):
        """Convert Door to a dictionary."""
        return {
            "direction": self.__myFirstDirection,
            "connected_direction": self.__myEndDirection,
            "room_coords": self.__myFirstRoom.getCords() if self.__myFirstRoom else None,
            "neighbor_coords": self.__myEndRoom.getCords() if self.__myEndRoom else None,
            "is_open": self.isOpen,
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruct a Door from a dictionary. Room linking happens in Floor.from_dict()."""
        door = cls(
            data["direction"],
            data["connected_direction"],
            None,  # Placeholder, will be linked later
            None   # Placeholder, will be linked later
        )
        door.isOpen = data["is_open"]
        door._room_coords = tuple(data["room_coords"])  # Temporarily store room coordinates
        door._neighbor_coords = tuple(data["neighbor_coords"])  # Temporarily store neighbor coordinates
        return door

