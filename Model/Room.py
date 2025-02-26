import pygame

class Door:
    def __init__(self, theX, theY, width, height, direction):
        self.rect = pygame.Rect(theX, theY, width, height)
        self.direction = direction  # "N", "S", "E", "W"
    
    def draw(self, screen, color=(0, 0, 0)):
        pygame.draw.rect(screen, color, self.rect)
    
    def collides_with(self, player_rect):
        return self.rect.colliderect(player_rect)


class Room:
    all_doors = []
    def __init__(self, __theRoomType, theX, theY, width, height):
        self.__myRoomType = __theRoomType
        self.__myX, self.__myY = theX, theY
        self.width, self.height = width, height
        self.rect = pygame.Rect(theX, theY, width, height)
        self.doors = {}  # Stores Door objects
        self.inRoom = []


    
    def addDoor(self, direction):
        door_width = 20
        door_height = 7
        
        if direction == "N":
            door___myX = self.__myX + (self.width // 2) - (door_width // 2)
            door_y = self.__myY - door_height
        elif direction == "S":
            door___myX = self.__myX + (self.width // 2) - (door_width // 2)
            door_y = self.__myY + self.height
        elif direction == "W":
            door___myX = self.__myX - door_height
            door_y = self.__myY + (self.height // 2) - (door_width // 2)
            door_width, door_height = door_height, door_width
        elif direction == "E":
            door___myX = self.__myX + self.width
            door_y = self.__myY + (self.height // 2) - (door_width // 2)
            door_width, door_height = door_height, door_width 
        else:
            return  # Invalid direction
           
        
     # Create Door object
        door = Door(door___myX, door_y, door_width, door_height, direction)
        self.doors[direction] = door
        Room.all_doors.append(door)
    
    # def draw(self, screen, color=(255, 255, 255)):
    #     pygame.draw.rect(screen, color, self.rect, 2)  
    #     if self.__myRoomType == "s":
    #         pygame.draw.rect(screen, (0,0,0), self.rect, 2) 
    #     for door in self.doors.values():
    #         door.draw(screen)
    
    def getRoom(self):
        return self
    
    def __str__(self):
        # return f"Room({self.__myRoomType}, Doors: {self.doors})"
        return self.__myRoomType
