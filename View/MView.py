import pygame
from View.SpriteMock import SpriteMock
class MView:
    def __init__(self):
        # self.screen = screen
        screen_width = 800
        screen_height = 600
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        color = pygame.Color(255, 0, 0)
        self.myPlayerSprite = SpriteMock(color, 50, 50)
        
    
    def viewTick(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        self.myPlayerSprite.draw(self.screen)
        pygame.display.flip()  # Update display

    def updatePlayerSprite(self, theX, theY):
        self.myPlayerSprite.updatePosition(theX,theY)
        