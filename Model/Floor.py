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
   
    def to_dict(self):
            """Serialize the Floor to a dictionary."""
            return {
                "grid": [[room.to_dict() if isinstance(room, Room) else None for room in row] for row in self.__myGrid],
                "doors": [door.to_dict() for door in self.__myDoorList],
                "start_coords": self.__myStartCord,
            }

    @classmethod
    def from_dict(cls, data):
        """Reconstruct a Floor from a dictionary."""
        from .Room import Room
        from .Door import Door

        grid = [[Room.from_dict(room_data) if room_data else None for room_data in row] for row in data["grid"]]
        doors = [Door.from_dict(door_data) for door_data in data["doors"]]

        floor = cls(grid, doors)
        floor.__myStartCord = tuple(data["start_coords"])  # Ensure tuple format
        return floor