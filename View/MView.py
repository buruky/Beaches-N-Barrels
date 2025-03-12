import os
import pygame
#from Model.GameWorld import GameWorld
from .SpriteSheet import SpriteSheet
from .SpriteFactory import SpriteFactory
from ViewUnits import ViewUnits
from Model.GameWorld import GameWorld 

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


        door_image_path = os.path.join(current_directory, '..', 'Assets', 'door.png')
        self.mydoor = pygame.image.load(door_image_path)
        
        screen_width = ViewUnits.SCREEN_WIDTH
        screen_height = ViewUnits.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.mySpriteFactory = SpriteFactory()
        self.onScreenChar = []
        self.theRoom = pygame.Rect(0,0,  screen_width, screen_height) 
        self.theNewRoom = self.theTest
        self.cords = None
        # self.theNewRoom = (10,10,10)
    
    def getScreen(self):
        return self.screen
    
    def clear(self):
        """Clear the screen before drawing the next frame."""
        self.screen.fill((0, 0, 0))  # Fill screen with black

    def updateRoom(self, event: pygame.event.Event):
        """Updates the room background and displays room coordinates at the center."""
        if event.roomtype == "s ":
            self.theNewRoom = self.theTest  # Set background for start room
        else:
            self.theNewRoom = self.theTest2  # Set background for other rooms

        if len(self.onScreenChar) != 0:
            playerSprite = None
            for i in range(len(self.onScreenChar)):
                if self.onScreenChar[i].getName() in ["Dolphin", "Buddha", "Astronaut"]:
                    playerSprite = self.onScreenChar[i]
            self.onScreenChar = [playerSprite]
        self.cords = event.cords


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

    def draw_room_items(self, room):
        """Draws items present in the room using the crab sprite sheet at the item's stored position."""
        items = room.get_items()
        for item in items:
            # Use the item's stored position.
            pos_x, pos_y = item.position  # Assuming each item has a 'position' attribute.
            # Create a crab sprite for this item.
            item_sprite = self.mySpriteFactory.createCrabSpriteSheet(id(item), pos_x, pos_y)
            # Draw the sprite at its designated position.
            self.screen.blit(item_sprite.getCurrentSprite(), item_sprite.getRect().topleft)

    def redrawCharacter(self):
        """Clears the screen, redraws the room, characters, and room coordinates."""
        # self.clear()
        self.screen.blit(self.theNewRoom, (0, 0))

        # Draw characters
        for currentSprite in self.onScreenChar:
            self.screen.blit(currentSprite.getCurrentSprite(), currentSprite.getRect().topleft)

        # Display room coordinates at the center of the screen
        if self.cords:
            font = pygame.font.Font(None, 50)  # Choose an appropriate font and size
            text_surface = font.render(f"Room: {self.cords}", True, (255, 255, 255))  # White text
            text_rect = text_surface.get_rect(center=(ViewUnits.SCREEN_WIDTH // 2, ViewUnits.SCREEN_HEIGHT // 2))
            
            self.screen.blit(text_surface, text_rect)
        
        current_room = GameWorld.getInstance().getCurrentRoom()
        if current_room is not None:
            self.draw_room_items(current_room)
        pygame.display.flip()


    

    