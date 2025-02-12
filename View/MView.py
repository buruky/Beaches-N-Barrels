import pygame
from View.SpriteMock import SpriteMock
class MView:
    def __init__(self):
        # self.screen = screen
        self.onscreen = dict()
        screen_width = 800
        screen_height = 600
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        color = pygame.Color(255, 0, 0)
        self.myPlayerSprite = SpriteMock(color, 50, 50)
        self.sprites = {
            #"player": pygame.image.load("assets/player.png"),
            "PlayerMock": SpriteMock(color, 50, 50),
            "EnemyMock": SpriteMock(color, 50, 50)
        }
    
    def viewTick(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        self.myPlayerSprite.draw(self.screen)
        pygame.display.flip()  # Update display

    
    
    def updatePlayerSprite(self, theX, theY):
        self.myPlayerSprite.updatePosition(theX,theY)
    
    
    def clear(self):
        """Clear the screen before drawing the next frame."""
        self.screen.fill((0, 0, 0))  # Fill screen with black

    #####
    def addSpriteOnScreen(self, theObjectName, theSprite, theNewX, theNewY):
        self.onscreen[theObjectName] = [theSprite, theNewX, theNewY]

    def update_entity(self, objectName, theSurfaceSprite, theNewX, theNewY):#need to find way to clear canvas when you draw
        """Update only a single entity when it moves."""
        
        self.addSpriteOnScreen(objectName, theSurfaceSprite, theNewX, theNewY)
        
        self.draw_entity( objectName,theSurfaceSprite, theNewX, theNewY)
        pygame.display.flip()
        

    def draw_entity(self,theObjectname, theNewSprite,theNewX, theNewY):
        """Draw an entity based on its class name."""
        self.clear()        
        
        for currentSprite in self.onscreen.keys():
            if currentSprite == theObjectname:
                self.screen.blit(theNewSprite, (theNewX, theNewY))
            else:
                self.screen.blit(self.onscreen[currentSprite][0], (self.onscreen[currentSprite][1], 
                                                                self.onscreen[currentSprite][2]))
                
    

    

    