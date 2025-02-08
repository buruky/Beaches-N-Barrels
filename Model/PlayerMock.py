import pygame
class PlayerMock:
    def __init__(self):
        self.player_x = 250
        self.player_y = 250
        self.speed = 5

        self.direction = None
        self.max_size = 500 
        self.min_size = 10

    def movePlayer(self, directions):  # Initial color (Green)
        
        dx, dy = 0, 0

        if "LEFT" in directions:
            dx = -1
        if "RIGHT" in directions:
            dx = 1
        if "UP" in directions:
            dy = -1
        if "DOWN" in directions:
            dy = 1

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.707  # 1/sqrt(2)
            dy *= 0.707

        # Update position
        self.player_x += dx * self.speed
        self.player_y += dy * self.speed

         # Update direction if moving
        if directions:
            self.direction = directions[-1]  # Last key pressed is priority

    def changeColor(self, theColor):
        self.color = theColor

    def moveTo(self, num1, num2):
        self.player_x = num1
        self.player_y = num2