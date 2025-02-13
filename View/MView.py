import pygame
from View.SpriteMock import SpriteMock
class MView:
    def __init__(self):
        # self.screen = screen
        self.onscreen = dict()
        screen_width = 800
        screen_height = 600
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        
    def clear(self):
        """Clear the screen before drawing the next frame."""
        self.screen.fill((0, 0, 0))  # Fill screen with black

    def addSpriteScreenList(self, theObjectName, theSprite, theNewX, theNewY):
        self.onscreen[theObjectName] = [theSprite, theNewX, theNewY]

    def update_entity(self, objectName, theSurfaceSprite, theNewX, theNewY):#need to find way to clear canvas when you draw
        """Adds Chracter to list and to screen with new position  """
        
        self.addSpriteScreenList(objectName, theSurfaceSprite, theNewX, theNewY)
        
        self.drawCharacter( objectName,theSurfaceSprite, theNewX, theNewY)

        pygame.display.flip()
        

    def drawCharacter(self,theObjectname, theNewSprite,theNewX, theNewY):
        """ 1. clears screen
            2. draws passed sprite in new position
            3. draws all other sprites that were onscreen 
        """
        self.clear()        
        
        for currentSprite in self.onscreen.keys():
            if currentSprite == theObjectname:
                self.screen.blit(theNewSprite, (theNewX, theNewY))
            else:
                self.screen.blit(self.onscreen[currentSprite][0], (self.onscreen[currentSprite][1], 
                                                                self.onscreen[currentSprite][2]))
                
    

    

    