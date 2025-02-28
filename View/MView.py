import os
import pygame
#from Model.GameWorld import GameWorld
from .SpriteSheet import SpriteSheet
from .SpriteFactory import SpriteFactory
class MView:
    def __init__(self):
        # self.screen = screen
        
        screen_width = 800
        screen_height = 600
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.mySpriteFactory = SpriteFactory()
        self.mySpriteFactory.Initalize()
        self.allSprites = self.mySpriteFactory.listOfSpriteSheets
        self.onScreenChar = []
        self.theRoom = pygame.Rect(0,0,  screen_width, screen_height) 
        self.theNewRoom = (0,0,0)
        
    def clear(self):
        """Clear the screen before drawing the next frame."""
        self.screen.fill((0, 0, 0))  # Fill screen with black

    def updateRoom(self, event: pygame.event.Event):
            print("gamer is gaming")  # Console output
            if event.name == "startRoom":
                self.theNewRoom = self.background_color = (150, 150, 10)  # Change background color
            else:
                self.theNewRoom = self.background_color = (150, 40, 400)  # Change background color


    def update_entity(self,theEvent:pygame.event):#need to find way to clear canvas when you draw
        """Adds Chracter to list and to screen with new position  """
        if not theEvent.id in self.onScreenChar:
            self.onScreenChar.append(theEvent.id)
        character = self.allSprites[theEvent.name]
        
        character.setPosition(theEvent.positionX, theEvent.positionY)
        


        self.redrawCharacter()

    def display_game_over(self):
        """Display 'Game Over' and stop the game."""
        self.clear()
        
        font = pygame.font.Font(None, 72)  # Default font, size 72
        text_surface = font.render("Game Over", True, (255, 0, 0))  # Red text
        text_rect = text_surface.get_rect(center=(400, 300))  # Centered

        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

        pygame.time.delay(9000)  # Pause for 9 seconds before quitting
    def redrawCharacter(self):
        """ 1. clears screen
            2. draws passed sprite in new position
            3. draws all other sprites that were onscreen 
        """
        self.clear()        

        # Draw obstacles in RED for visibility
        # for obstacle in GameWorld.getInstance().get_obstacles():
        #     pygame.draw.rect(self.screen, (255, 0, 0), obstacle)  # RED rectangles
        pygame.draw.rect(self.screen, self.theNewRoom, self.theRoom, 50) 
        for currentSprite in self.allSprites.values():
            self.screen.blit(currentSprite.getCurrentSprite(), currentSprite.getRect().topleft)
            
        pygame.display.flip()

    

    