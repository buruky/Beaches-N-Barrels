from typing import Final
from .Room import Room 
from .EventManager import EventManager
from CustomEvents import CustomEvents
from .Door import Door

class Floor:
    
    _ROOM_SIZE = 100
    _START_POS:Final = (5,5)
    def __init__(self, theGrid:list[list], theDoorList:list[Door]):
        self.__myGrid = theGrid
        self.__myDoorList = theDoorList
        self.__myStartCord = Floor._START_POS


    def get_dungeon(self) -> list[list]:
        return self.__myGrid  
    
    def getDoorList(self) -> list[Door]:
        return self.__myDoorList
    
    def getStartRoom(self):
        return self.__myGrid[self.__myStartCord[0]][self.__myStartCord[1]]
    
    def print_dungeon(self):
        for row in range(len(self.__myGrid)):
            line = ""
            for col in range(len(self.__myGrid[0])):
                if isinstance(self.__myGrid[row][col], Room):
                    line += str(self.__myGrid[row][col])
                else:
                    line += ". "
            print(line)
        print()
    
    def getRoomByCoords(self, theCoords:tuple):
        return self.__myGrid[theCoords[0]][theCoords[1]]
    
    def to_dict(self):
        """Convert the Floor to a dictionary for serialization."""
        return {
            "grid": [[room.to_dict() if isinstance(room, Room) else None for room in row] for row in self.__myGrid],
            "door_list": [door.to_dict() for door in self.__myDoorList]
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruct the Floor from a dictionary."""
        from .Room import Room
        from .Door import Door
        
        grid = [
            [Room.from_dict(room) if room else None for room in row]
            for row in data["grid"]
        ]
        door_list = [Door.from_dict(door) for door in data["door_list"]]
        
        floor = cls(grid, door_list)
        return floor