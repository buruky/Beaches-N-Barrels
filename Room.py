import pygame

class Door:
    def __init__(self, x, y, width, height, direction):
        self.rect = pygame.Rect(x, y, width, height)
        self.direction = direction  # "N", "S", "E", "W"
    
    def draw(self, screen, color=(0, 0, 0)):
        pygame.draw.rect(screen, color, self.rect)
    
    def collides_with(self, player_rect):
        return self.rect.colliderect(player_rect)


class Room:
    all_doors = []
    def __init__(self, room_type, x, y, width, height):
        self.room_type = room_type
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect = pygame.Rect(x, y, width, height)
        self.doors = {}  # Stores Door objects
    
    def add_door(self, direction):
        door_width = 20
        door_height = 7
        
        if direction == "N":
            door_x = self.x + (self.width // 2) - (door_width // 2)
            door_y = self.y - door_height
        elif direction == "S":
            door_x = self.x + (self.width // 2) - (door_width // 2)
            door_y = self.y + self.height
        elif direction == "W":
            door_x = self.x - door_height
            door_y = self.y + (self.height // 2) - (door_width // 2)
            door_width, door_height = door_height, door_width
        elif direction == "E":
            door_x = self.x + self.width
            door_y = self.y + (self.height // 2) - (door_width // 2)
            door_width, door_height = door_height, door_width 
        else:
            return  # Invalid direction
           
        
     # Create Door object
        door = Door(door_x, door_y, door_width, door_height, direction)
        self.doors[direction] = door
        Room.all_doors.append(door)
    
    def draw(self, screen, color=(255, 255, 255)):
        pygame.draw.rect(screen, color, self.rect, 2)  
        if self.room_type == "s":
            pygame.draw.rect(screen, (0,0,0), self.rect, 2) 
        for door in self.doors.values():
            door.draw(screen)
    
    def get_room(self):
        return self
    
    def __str__(self):
        # return f"Room({self.room_type}, Doors: {self.doors})"
        return self.room_type
