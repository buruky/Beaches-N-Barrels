from typing import Final
from .Room import Room 
from .EventManager import EventManager
from CustomEvents import CustomEvents
from .Door import Door
print
class Floor:
    """ a floor that has rooms and doors"""
    _ROOM_SIZE = 100
    _START_POS:Final = (5,5)
    def __init__(self, theGrid:list[list], theDoorList:list[Door]):
        """initializes floor"""
        self.__myGrid = theGrid
        self.__myDoorList = theDoorList
        self.__myStartCord = Floor._START_POS

    def get_dungeon(self) -> list[list]:
        """returns grid"""
        return self.__myGrid  
    
    def getDoorList(self) -> list[Door]:
        """returns the list of doors on the floor"""
        return self.__myDoorList
    
    def getStartRoom(self):
        """returns the start room for the floor"""
        return self.__myGrid[self.__myStartCord[0]][self.__myStartCord[1]]
    
    def print_dungeon(self):
        """prints the grid for testing"""
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
        """returns the room by using coords"""
        return self.__myGrid[theCoords[0]][theCoords[1]]
    
    def to_dict(self):
        """Convert the Floor to a dictionary for serialization."""
        return {
            "grid": [[room.to_dict() if isinstance(room, Room) else None for room in row] for row in self.__myGrid],
            "door_list": [door.to_dict() for door in self.__myDoorList]
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruct the Floor from a dictionary, linking doors to rooms correctly."""
        from .Room import Room
        from .Door import Door

        # Reconstruct rooms
        grid = [
            [Room.from_dict(room) if room else None for room in row]
            for row in data["grid"]
        ]

        # Reconstruct doors (without linking rooms yet)
        door_list = [Door.from_dict(door) for door in data["door_list"]]


        # Create the Floor object
        floor = cls(grid, door_list)

        # Now, link doors to rooms
        for door in door_list:
            room_coords = door._room_coords
            neighbor_coords = door._neighbor_coords

            door._Door__myFirstRoom = grid[room_coords[0]][room_coords[1]]
            door._Door__myEndRoom = grid[neighbor_coords[0]][neighbor_coords[1]]
            
            # Ensure doors are added back into their respective rooms
            door._Door__myFirstRoom.addDoor(door._Door__myFirstDirection, door)
            door._Door__myEndRoom.addDoor(door._Door__myEndDirection, door)

        return floor
