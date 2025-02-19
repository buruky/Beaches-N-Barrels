import pygame

class Room:
    def __init__(self, room_type, x, y, width, height):
        self.room_type = room_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.doors = {"N": False, "S": False, "W": False, "E": False}  
        self.rect = pygame.Rect(x, y, width, height)  # Store rectangle for collision

    def add_door(self, direction):
        #called from connect rooms method and marks neighbor and self direction as true
        if direction in self.doors:
            self.doors[direction] = True

    def get_rect(self):
        return self.rect
    
    def get_room(self):
        return self
    
    def __str__(self):
        # return f"Room({self.room_type}, Doors: {self.doors})"
        return self.room_type
