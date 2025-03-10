import os
import pygame
#from Model.GameWorld import GameWorld
from .SpriteSheet import SpriteSheet
from .SpriteFactory import SpriteFactory
from ViewUnits import ViewUnits
class MView:
    def __init__(self):
        # self.screen = screen
        current_directory = os.path.dirname(__file__)

        # Build the relative path to the player and enemy images
        player_image_path = os.path.join(current_directory, '..', 'Assets', 'TestBackround.png')
        self.myRawPlayerImage = pygame.image.load(player_image_path)
        self.theTest = pygame.transform.scale(self.myRawPlayerImage, (ViewUnits.SCREEN_WIDTH,ViewUnits.SCREEN_HEIGHT))
        player_image_path2 = os.path.join(current_directory, '..', 'Assets', 'Testbackround2.png')
        self.myRawPlayerImage2 = pygame.image.load(player_image_path2)
        self.theTest2 = pygame.transform.scale(self.myRawPlayerImage2, (ViewUnits.SCREEN_WIDTH,ViewUnits.SCREEN_HEIGHT))

        screen_width = ViewUnits.SCREEN_WIDTH
        screen_height = ViewUnits.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.mySpriteFactory = SpriteFactory()
        self.onScreenChar = []
        print(self.onScreenChar)
        self.theRoom = pygame.Rect(0,0,  screen_width, screen_height) 
        # self.theNewRoom = (10,10,10)
    
    def clear(self):
        """Clear the screen before drawing the next frame."""
        self.screen.fill((0, 0, 0))  # Fill screen with black

    def updateRoom(self, event: pygame.event.Event):
        if event.roomtype == "s ":
            self.theNewRoom = self.theTest  # Change background color
        else:
            self.theNewRoom = self.theTest2  # Change background color
        if len(self.onScreenChar) != 0:

            playerSprite = None

            for i in range(len(self.onScreenChar)):
                if self.onScreenChar[i].getName() == ViewUnits.PLAYER_SPRITE_NAME:
                    playerSprite = self.onScreenChar[i]
            
            self.onScreenChar = [playerSprite]

    def addCharacterToScreenList(self, theEvent:pygame.event):
        #print("addid",theEvent.id)
        #print(self.onScreenChar)
        newCharSprite = self.mySpriteFactory.createSpriteSheet(theEvent.id, theEvent.name, theEvent.positionX,theEvent.positionY)
        #print("addchar: ",newCharSprite.getName())
        self.onScreenChar.append(newCharSprite)
        #print("waaa",self.onScreenChar)

    def update_entity(self,theEvent:pygame.event):#need to find way to clear canvas when you draw
        """Adds Chracter to list and to screen with new position  """
    
        isIdInSpriteList = False
        for characterSprite in self.onScreenChar:
            #print(theEvent)
            if characterSprite is not None :
                #print(characterSprite)
                if theEvent.id == characterSprite.getId():
                    isIdInSpriteList = True
                
        if not isIdInSpriteList:
            
            self.addCharacterToScreenList(theEvent)
            
        """Updates position of sprite associated with event passed in"""
        for characterSprite in self.onScreenChar:
            if theEvent.id == characterSprite.getId():
                characterSprite.setPosition(theEvent.positionX, theEvent.positionY)
        
        self.redrawCharacter()



    def display_game_over(self):
        """Display 'Game Over' and stop the game."""
        self.clear()
        
        font = pygame.font.Font(None, 72)  # Default font, size 72
        text_surface = font.render("Game Over", True, (255, 0, 0))  # Red text
        text_rect = text_surface.get_rect(center=(ViewUnits.SCREEN_WIDTH // 2, ViewUnits.SCREEN_HEIGHT // 2))  # Centered dynamically

        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

        pygame.time.delay(3000)  # Pause for some seconds before quitting
    def redrawCharacter(self):
        """ 1. clears screen
            2. draws passed sprite in new position
            3. draws all other sprites that were onscreen 
        """
        self.clear()        

        self.screen.blit(self.theNewRoom, (0, 0))

        for currentSprite in self.onScreenChar:
            self.screen.blit(currentSprite.getCurrentSprite(), currentSprite.getRect().topleft)

        pygame.display.flip()

    

    