import random
from typing import Final
from .RoomFactory import RoomFactory
from .Door import Door
from .Floor import Floor
from .Room import Room 
from .EventManager import EventManager
from CustomEvents import CustomEvents
import pygame
class FloorFactory:
    _FLOOR_LEVEL = 5
    _instance = None  # Stores the single instance

    def __new__(cls):
        """Ensure only one instance is created."""
        if cls._instance is None:
            cls._instance = super(FloorFactory, cls).__new__(cls)
            cls._instance._init_once()
        return cls._instance
    
    def _init_once(self):
        self.grid_width = 11
        self.grid_height = 11
        self.start_pos = (5, 5)  # Center of the grid
        self.roomFact = RoomFactory.getInstance()
        #self.grid = self.generate_dungeon(level)  # Store the grid in an instance variable
        #self.update()
    @classmethod
    def getInstance(cls):
        """Getter for the singleton instance."""
        if cls._instance is None:  # Ensure an instance exists
            cls._instance = cls()  # This triggers __new__()
        return cls._instance

    def createFloor(self, theWidth:int, theHeight:int) -> Floor:
        grid = self.generateGrid(theWidth, theHeight)
        doors = self.connect_rooms(grid)
        return Floor(grid, doors)
        
    def generateGrid(self, theWidth:int, theHeight:int) -> list[list]:
        startx = Floor._START_POS[0]
        
        starty = Floor._START_POS[1]
        #binding of isaac formula 
        num_rooms = random.randint(2, 3) + 5 + int(FloorFactory._FLOOR_LEVEL * 2.6)
        #fills entire frid with falsh
        grid = [[False for _ in range(theWidth)] for _ in range(theHeight)]
        
        #takes start position and creates a starting room there
        startRoom = "s "
        
        
        grid[startx][starty] = self.roomFact.createRoom(startRoom, startx, starty)
         #Room("s ", startx, starty, EnemyFactory.)
        
       
        queue = [Floor._START_POS]
        rooms = [Floor._START_POS]
        dead_ends = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
        
        #while queue is not empty and list of rooms is still less than set max number of rooms
        while queue and len(rooms) < num_rooms:
            current = queue.pop(0)
            random.shuffle(directions)
            added_room = False
            
            #test adding a room in every direction
            for d in directions:
                #creates new coordinate at a random direction
                neighbor = (current[0] + d[0], current[1] + d[1])
                
                #if new coord is is not within the bounds of the grids skip
                if not (0 <= neighbor[0] < theHeight and 0 <= neighbor[1] < theWidth):
                    continue  
                #if a room at new coord is already there skip
                if grid[neighbor[0]][neighbor[1]]:
                    continue  
                #checks if adding the room creates a loop
                adjacent_filled = sum(1 for dir in directions if 0 <= neighbor[0] + dir[0] < theHeight and 0 <= neighbor[1] + dir[1] < theWidth and grid[neighbor[0] + dir[0]][neighbor[1] + dir[1]])
                if adjacent_filled > 1:
                    continue
                #if adding that room makes list of roomms greater than num_rooms skip
                if len(rooms) >= num_rooms:
                    break
                
                #.3 perccent chance of skiipping 
                if random.random() < 0.3:
                    continue
                
                #add new coord as a room 

                ##### add door
                grid[neighbor[0]][neighbor[1]] = self.roomFact.createRoom("n ", neighbor[0], neighbor[1])  
                rooms.append(neighbor)
                queue.append(neighbor)
                added_room = True
            
            if not added_room:
                dead_ends.append(current)

        return grid  


    
    def get_dungeon(self):
        return self.grid  

    def getStartRoom(self):
        return self.start_pos
    

    
    

    def connect_rooms(self, theGrid):
        doors = []
        directions = {
            "N": (0, -1),
            "S": (0, 1),
            "W": (-1, 0),
            "E": (1, 0)
        }

        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if isinstance(theGrid[row][col], Room):
                    current_room = theGrid[row][col]
                    # Check each direction for an adjacent room
                    for direction, (dr, dc) in directions.items():
                        #row + direction, col + direction
                        neighbor_row, neighbor_col = row + dr, col + dc
                        #inbounds
                        if 0 <= neighbor_row < self.grid_height and 0 <= neighbor_col < self.grid_width:
                            neighbor = theGrid[neighbor_row][neighbor_col]
                            #if neighbor is room
                            if isinstance(neighbor, Room):
                                doorDirection = ""
                                #current_room.addDoor(direction)  # Mark door open
                                # bidirectional connection
                                
                                if direction == "N":
                                    #neighbor.addDoor("S")
                                    doorDirection = "S"
                                elif direction == "S":
                                    #neighbor.addDoor("N")
                                    doorDirection = "N"
                                elif direction == "W":
                                    #neighbor.addDoor("E")
                                    doorDirection = "E"
                                elif direction == "E":
                                    #neighbor.addDoor("W")
                                    doorDirection = "W"
                                doors.append(Door(direction,  doorDirection, current_room, neighbor,))

        return doors