import random
from Room import Room


class Generate:
     def __init__(self):
          # Room type can be "normal", "boss", "shop", etc.

        grid_width = 11
        grid_height = 11
        start_pos = (5, 5)  # Starting room at center (row, col)

        # def create_grid():
        #     return [[False for _ in range(grid_width)] for _ in range(grid_height)]

        def generate_dungeon(level):
            num_rooms = random.randint(2, 3) + 5 + int(level * 2.6)
            
            grid = [[False for _ in range(grid_width)] for _ in range(grid_height)]
            
            grid[start_pos[0]][start_pos[1]] = Room("s ", start_pos[0], start_pos[1], 100, 100)  # Assign a Room object at the start position
            
            queue = [start_pos]
            rooms = [start_pos]
            dead_ends = []
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
            
            while queue and len(rooms) < num_rooms:
                current = queue.pop(0)
                random.shuffle(directions)
                added_room = False
                
                for d in directions:
                    neighbor = (current[0] + d[0], current[1] + d[1])
                    
                    if not (0 <= neighbor[0] < grid_height and 0 <= neighbor[1] < grid_width):
                        continue  # Skip if out of bounds
                    
                    if grid[neighbor[0]][neighbor[1]]:
                        continue  # Skip if already occupied
                    
                    adjacent_filled = sum(1 for dir in directions if 0 <= neighbor[0] + dir[0] < grid_height and 0 <= neighbor[1] + dir[1] < grid_width and grid[neighbor[0] + dir[0]][neighbor[1] + dir[1]])
                    if adjacent_filled > 1:
                        continue
                    
                    if len(rooms) >= num_rooms:
                        break
                    
                    if random.random() < 0.3:
                        continue
                    
                    grid[neighbor[0]][neighbor[1]] = Room("n ", neighbor[0] * 110, neighbor[1] * 110, 100, 100)  # Assign a new Room object
                    rooms.append(neighbor)
                    queue.append(neighbor)
                    added_room = True
                
                if not added_room:
                    dead_ends.append(current)
            
            while len(rooms) < num_rooms:
                queue.append(start_pos)

            
            return grid
        
        def print_dungeon(grid):
            for row in range(grid_height):
                line = ""
                for col in range(grid_width):
                    if (row, col) == start_pos:
                        my_room = grid[row][col]
                        line += str(my_room.get_room())
                    elif isinstance(grid[row][col], Room):
                        my_room = grid[row][col]
                        line += str(my_room.get_room())
                    else:
                        line += ". "
                print(line)
            print()


        dungeon = generate_dungeon(3)
        print_dungeon(dungeon)
        
