import pygame



class Room:
    
    def __init__(self, theRoomType, theX, theY, theEnemyList):
        self.__myRoomType = theRoomType
        self.__myX, self.__myY = theX, theY
        
        self.rect = pygame.Rect(0,0,800,600)
        self.doors = {}  # Stores Door objects
        self.__myEnemyList = theEnemyList


    
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
        #door = Door(door___myX, door_y, door_width, door_height, direction)
        #self.doors[direction] = door
        #Room.all_doors.append(door)
    
    # def draw(self, screen, color=(255, 255, 255)):
    #     pygame.draw.rect(screen, color, self.rect, 2)  
    #     if self.__myRoomType == "s":
    #         pygame.draw.rect(screen, (0,0,0), self.rect, 2) 
    #     for door in self.doors.values():
    #         door.draw(screen)
    def getRoomType(self):
        return self.__myRoomType
    def getEnemyList(self):
        return self.__myEnemyList
    def getRoom(self):
        return self
    
    def __str__(self):
        # return f"Room({self.__myRoomType}, Doors: {self.doors})"
        return self.__myRoomType
    