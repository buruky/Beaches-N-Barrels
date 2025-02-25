import random
from Model.Room import Room 

class Floor:
    ROOM_SIZE = 100
    def __init__(self, level=5):
        self.grid_width = 11
        self.grid_height = 11
        self.start_pos = (5, 5)  # Center of the grid
        self.grid = self.generate_dungeon(level)  # Store the grid in an instance variable

    def generate_dungeon(self, level):
        ROOM_SIZE = 100
        #binding of isaac formula 
        num_rooms = random.randint(2, 3) + 5 + int(level * 2.6)
        #fills entire frid with falsh
        grid = [[False for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
        #takes start position and creates a starting room there
        grid[self.start_pos[0]][self.start_pos[1]] = Room("s ", self.start_pos[0] * ROOM_SIZE, self.start_pos[1] * ROOM_SIZE, ROOM_SIZE/2, ROOM_SIZE/2)  
        
       
        queue = [self.start_pos]
        rooms = [self.start_pos]
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
                if not (0 <= neighbor[0] < self.grid_height and 0 <= neighbor[1] < self.grid_width):
                    continue  
                #if a room at new coord is already there skip
                if grid[neighbor[0]][neighbor[1]]:
                    continue  
                #checks if adding the room creates a loop
                adjacent_filled = sum(1 for dir in directions if 0 <= neighbor[0] + dir[0] < self.grid_height and 0 <= neighbor[1] + dir[1] < self.grid_width and grid[neighbor[0] + dir[0]][neighbor[1] + dir[1]])
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
                grid[neighbor[0]][neighbor[1]] = Room("n ", neighbor[0] * ROOM_SIZE, neighbor[1] * ROOM_SIZE, ROOM_SIZE/2, ROOM_SIZE/2)  
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
    
    def print_dungeon(self):
        for row in range(self.grid_height):
            line = ""
            for col in range(self.grid_width):
                if isinstance(self.grid[row][col], Room):
                    line += str(self.grid[row][col].getRoom())
                else:
                    line += ". "
            print(line)
        print()
    

    def connect_rooms(self):
        directions = {
            "N": (0, -1),
            "S": (0, 1),
            "W": (-1, 0),
            "E": (1, 0)
        }

        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if isinstance(self.grid[row][col], Room):
                    current_room = self.grid[row][col]
                    # Check each direction for an adjacent room
                    for direction, (dr, dc) in directions.items():
                        #row + direction, col + direction
                        neighbor_row, neighbor_col = row + dr, col + dc
                        #inbounds
                        if 0 <= neighbor_row < self.grid_height and 0 <= neighbor_col < self.grid_width:
                            neighbor = self.grid[neighbor_row][neighbor_col]
                            #if neighbor is room
                            if isinstance(neighbor, Room):
                                current_room.addDoor(direction)  # Mark door open
                                # bidirectional connection
                                if direction == "N":
                                    neighbor.addDoor("S")
                                elif direction == "S":
                                    neighbor.addDoor("N")
                                elif direction == "W":
                                    neighbor.addDoor("E")
                                elif direction == "E":
                                    neighbor.addDoor("W")
