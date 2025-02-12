import pygame
import random

class SpriteMock:
    """will be class that holds relevent data to sprite"""
    def __init__(self, color, width, height):
        self.x = 250
        self.y = 250
        self.color = color  # Store the color
        self.rect = pygame.Rect(250, 250, width, height)  # Use pygame.Rect directly

    def draw(self, screen):
        """Draw the rectangle using pygame.draw.rect."""
        pygame.draw.rect(screen, self.color, self.rect)
    
    def updatePosition(self, theNewX, theNewY):
        self.rect.x = theNewX
        self.rect.y = theNewY

    def changeColor(self):
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
   