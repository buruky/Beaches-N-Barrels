import os
import pygame
from .UI import UI  # Import the UI class from the UI.py file
from .SpriteSheet import SpriteSheet
from .SpriteFactory import SpriteFactory
from ViewUnits import ViewUnits
from Model.GameWorld import GameWorld 
import random

class MView:
    def __init__(self):
        # self.screen = screen
        current_directory = os.path.dirname(__file__)
        # Build the relative path to the player and enemy images
        player_image_path = os.path.join(current_directory, '..', 'Assets', 'background-normalRoom.png')
        self.myRawPlayerImage = pygame.image.load(player_image_path)
        self.theTest = pygame.transform.scale(self.myRawPlayerImage, (ViewUnits.SCREEN_WIDTH,ViewUnits.SCREEN_HEIGHT))
        normalRoomPath = os.path.join(current_directory, '..', 'Assets', 'background-normalRoom.png')
        self.myRawNormalBackground = pygame.image.load(normalRoomPath)
        self.normalRoomImage = pygame.transform.scale(self.myRawNormalBackground, (ViewUnits.SCREEN_WIDTH,ViewUnits.SCREEN_HEIGHT))
        
        keyRoomImagePath = os.path.join(current_directory, '..', 'Assets', 'background-keyRoom.png')
       
        self.keyRoomBackground = pygame.image.load(keyRoomImagePath)
        self.keyRoomImage = pygame.transform.scale(self.keyRoomBackground, (ViewUnits.SCREEN_WIDTH,ViewUnits.SCREEN_HEIGHT))
        
        # self.bossRoomPath = os.path.join(current_directory, '..', 'Assets', 'background-bossRoom.png')        
        self.BossRoom = self.normalRoomImage
        
        font_path = os.path.join(os.path.dirname(__file__), "..", "Assets", "editundo.ttf")
        self.font_small = pygame.font.Font(font_path, 25)  # Small font for inventory
        self.font_med = pygame.font.Font(font_path, 37)
        self.font_large = pygame.font.Font(font_path, 50)  # Large font for health
        

        door_image_path = os.path.join(current_directory, '..', 'Assets', 'door.png')
        self.mydoor = pygame.image.load(door_image_path)
        
        screen_width = ViewUnits.SCREEN_WIDTH
        screen_height = ViewUnits.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.mySpriteFactory = SpriteFactory()
        self.onScreenChar = []
        self.myDoorList = []
        self.theRoom = pygame.Rect(0,0,  screen_width, screen_height) 
        self.theNewRoom = self.theTest
        self.cords = None
        self.playerHealth = 100
        self.maxHealth = 100
        self.inventory = []
        self.keyInventory = 0
        self.int = 0
        self.showMinimap = False
        self.needs_redraw = False
        self.minimap_rect = pygame.Rect(screen_width - 350 , 0, 350, 350)  
        self.ui = UI(self.screen)  # Create the UI instance
        # self.theNewRoom = (10,10,10)
        self.bossRoom = True
    
    def getScreen(self):
        return self.screen
    
    def clear(self):
        """Clear the screen before drawing the next frame."""
        self.screen.fill((0, 0, 0))  # Fill screen with black

    def updateBossHealthUI(self, event: pygame.event.Event):
        self.BossHealth = event.health
        self.bossMaxHealth = event.maxHealth
        self.bossRoom = event.isdead
        self.needs_redraw = True
    


    def updateHealthUI(self, event: pygame.event.Event):
        self.playerHealth = event.health
        self.maxHealth = event.maxHealth
        self.needs_redraw = True


    def updateInventoryUI(self, event: pygame.event.Event):
        self.inventory = event.inventory
        self.redrawCharacter()

    def updateKeyInventoryUI(self, event: pygame.event.Event):
        self.keyInventory = event.keyInventory
        self.redrawCharacter()   


    def process_updates(self):
        """Process all updates and perform a single redraw if needed."""
        if self.needs_redraw:
            self.redrawCharacter()
            self.needs_redraw = False
    def updateRoom(self, event: pygame.event.Event):
        """Updates the room background and displays room coordinates at the center."""
        if event.roomtype == "s ":
            self.theNewRoom = self.theTest  # Set background for start room
        else:
            self.theNewRoom = self.normalRoomImage  # Set background for other rooms

        self.myDoorList = []
        for dir, isDoor in event.doors.items():
            if isDoor:
                theDoor = None
                if dir == "N":
                    theDoor = self.mySpriteFactory.createSpriteSheet(ord(dir), "Door",ViewUnits.SOUTH_DOOR_CORD[0],ViewUnits.SOUTH_DOOR_CORD[1])
                    theDoor.setCurrentState("UP")
                    self.myDoorList.append(theDoor)
                elif dir == "S":
                    theDoor = self.mySpriteFactory.createSpriteSheet(ord(dir), "Door",ViewUnits.NORTH_DOOR_CORD[0],ViewUnits.NORTH_DOOR_CORD[1])
                    theDoor.setCurrentState("DOWN")
                    self.myDoorList.append(theDoor)
                elif dir == "W":
                    theDoor = self.mySpriteFactory.createSpriteSheet(ord(dir), "Door",ViewUnits.EAST_DOOR_CORD[0],ViewUnits.EAST_DOOR_CORD[1])
                    theDoor.setCurrentState("LEFT")
                    self.myDoorList.append(theDoor)
                else:
                    theDoor = self.mySpriteFactory.createSpriteSheet(ord(dir), "Door",ViewUnits.WEST_DOOR_CORD[0],ViewUnits.WEST_DOOR_CORD[1])
                    theDoor.setCurrentState("RIGHT")
                    self.myDoorList.append(theDoor)
        if event.roomtype == "s ":
            self.theNewRoom = self.theTest  # Set background for start room
        elif event.roomtype == "k ":
            self.theNewRoom = self.keyRoomImage  # Set background for key room
        elif event.roomtype == "n ":
            self.theNewRoom = self.normalRoomImage  # Set background for other rooms
        elif event.roomtype == "b ":
            self.theNewRoom = self.normalRoomImage  # Set background for other rooms
        if len(self.onScreenChar) != 0:
            playerSprite = None
            for i in range(len(self.onScreenChar)):
                if self.onScreenChar[i].getName() in ["Dolphin", "Buddha", "Astronaut"]:
                    playerSprite = self.onScreenChar[i]
            self.onScreenChar = [playerSprite]
        self.cords = event.cords


    def addCharacterToScreenList(self, theEvent:pygame.event):
        
        newCharSprite = self.mySpriteFactory.createSpriteSheet(theEvent.id, theEvent.name, theEvent.positionX,theEvent.positionY)
        self.onScreenChar.append(newCharSprite)
    
    def remove_projectile(self, theEvent:pygame.event):
        """Removes a projectile from the screen."""
        for i in range(len(self.onScreenChar)):
            if theEvent.id == self.onScreenChar[i].getId():
                self.onScreenChar.pop(i)
                break
        self.needs_redraw = True


    def update_entity(self,theEvent:pygame.event):#need to find way to clear canvas when you draw
        """Adds Chracter to list and to screen with new position  """
    
        isIdInSpriteList = False
        for characterSprite in self.onScreenChar:
            if characterSprite is not None :
                if theEvent.id == characterSprite.getId():
                    isIdInSpriteList = True
                
        if not isIdInSpriteList:
            self.addCharacterToScreenList(theEvent)
            
        """Updates position of sprite associated with event passed in"""
        for characterSprite in self.onScreenChar:
            if theEvent.id == characterSprite.getId():
                characterSprite.checkCycle()
                characterSprite.setPosition(theEvent.positionX, theEvent.positionY)
                if characterSprite.getName() in ["Dolphin", "Buddha", "Astronaut"] or characterSprite.getName() =="BeachBall":
                    characterSprite.setCurrentState(theEvent.state)
        
        self.needs_redraw = True

    def display_game_won(self):
        """Display 'You Won!' with animations and effects."""

        # Load assets
        assets_path = os.path.join(os.path.dirname(__file__), "..", "Assets")
        
        fireworks_image = pygame.image.load(os.path.join(assets_path, "Goat2.jpg"))
        fireworks_image = pygame.transform.scale(fireworks_image, (200, 200))  # Resize


        # Colors
        GOLD = (255, 215, 0)
        WHITE = (255, 255, 255)

        # Confetti particle list
        confetti_particles = []

        font_big = pygame.font.Font(None, 100)  # Victory text font
        font_small = pygame.font.Font(None, 40)  # Replay prompt

        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.fill((0, 0, 50))  # Dark blue victory background

            # Draw fireworks at random positions
            for _ in range(3):  # Three fireworks randomly placed
                x = random.randint(100, ViewUnits.SCREEN_WIDTH - 200)
                y = random.randint(50, ViewUnits.SCREEN_HEIGHT // 2)
                self.screen.blit(fireworks_image, (x, y))

            # Victory Text (Glowing Effect)
            text_surface = font_big.render("YOU WON!", True, GOLD)
            glow_surface = font_big.render("YOU WON!", True, WHITE)
            text_rect = text_surface.get_rect(center=(ViewUnits.SCREEN_WIDTH // 2, ViewUnits.SCREEN_HEIGHT // 3))

            self.screen.blit(glow_surface, (text_rect.x - 2, text_rect.y - 2))  # Glow layer
            self.screen.blit(text_surface, text_rect)

            # Instruction to replay
            replay_text = font_small.render("Thanks For Playing!", True, WHITE)
            replay_rect = replay_text.get_rect(center=(ViewUnits.SCREEN_WIDTH // 2, ViewUnits.SCREEN_HEIGHT // 1.5))
            self.screen.blit(replay_text, replay_rect)

            # Confetti Effect
            if random.randint(0, 5) == 0:  # Add confetti randomly
                confetti_particles.append([
                    random.randint(0, ViewUnits.SCREEN_WIDTH),  # X position
                    0,  # Y starts at top
                    random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)])  # Random colors
                ])

            for particle in confetti_particles:
                pygame.draw.circle(self.screen, particle[2], (particle[0], particle[1]), 5)  # Draw confetti
                particle[1] += 3  # Move down
            confetti_particles = [p for p in confetti_particles if p[1] < ViewUnits.SCREEN_HEIGHT]  # Remove off-screen

            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Restart on SPACE
                        pygame.mixer.music.stop()  # Stop victory music
                        return  
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
        """Draws items present in the room using different sprite sheets depending on the item's type."""
        items = room.get_items()
        for item in items:
            # Use the item's stored position.
            pos_x, pos_y = item.position  # Assuming each item has a 'position' attribute.
            # Determine which sprite sheet to use based on the item type.
            if item._name == "KeyItem":
                item_sprite = self.mySpriteFactory.createKeySpriteSheet(id(item), pos_x, pos_y)
            elif item._name == "InvincibilityItem":
                item_sprite = self.mySpriteFactory.createInvincePotionSpriteSheet(id(item), pos_x, pos_y)
            elif item._name == "MockItem":
                item_sprite = self.mySpriteFactory.createHealPotionSpriteSheet(id(item), pos_x, pos_y)
            elif item._name == "SpeedItem":
                item_sprite = self.mySpriteFactory.createSpeedPotionSpriteSheet(id(item), pos_x, pos_y)
            else:
                item_sprite = self.mySpriteFactory.createCrabSpriteSheet(id(item), pos_x, pos_y)

            # Draw the sprite at its designated position.
            self.screen.blit(item_sprite.getCurrentSprite(), item_sprite.getRect().topleft)
    def draw_minimap(self):
        """Draws a minimap of the floor using rounded rectangles to represent rooms with beach-themed colors and a border."""
        gameworld = GameWorld.getInstance()
        floor = gameworld.getFloor()  
        grid = floor.get_dungeon()  
        grid_rows = len(grid)
        grid_cols = len(grid[0]) if grid_rows > 0 else 0
        minimap_area = self.minimap_rect  
        cell_width = minimap_area.width / grid_cols
        cell_height = minimap_area.height / grid_rows

        # Use a border_radius for rounded corners.
        border_radius = 5

        for row in range(grid_rows):
            for col in range(grid_cols):
                room = grid[row][col]
                if room:
                    # Calculate position of each cell in the minimap.
                    rect_x = minimap_area.x + col * cell_width
                    rect_y = minimap_area.y + row * cell_height

                    room_type = room.getRoomType()
                    # Beach-themed colors:
                    if room_type == "s ":
                        color = (0, 255, 0)
                    elif room_type == "n ":
                        color = (128, 128, 128)  # Medium Grey  
                    elif room_type == "k ":
                        color = (255, 255, 0)
                    elif room_type == "b ":
                        color = (255, 0, 0) 
                    else:
                        color = (200, 200, 200)

                    rect = pygame.Rect(rect_x, rect_y, cell_width - 2, cell_height - 2)
                    pygame.draw.rect(self.screen, color, rect, border_radius=border_radius)
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 2, border_radius=border_radius)

    def redrawCharacter(self):
        """Clears the screen, redraws the room, characters, and room coordinates."""
        
        self.screen.blit(self.theNewRoom, (0, 0))
        
        #self.ui.draw_room_coordinates(self.cords)  # Draw room coordinates
        for doorSprite in self.myDoorList:
            self.screen.blit(doorSprite.getCurrentSprite(),doorSprite.getRect().topleft)
        current_room = GameWorld.getInstance().getCurrentRoom()
        if current_room is not None:
            self.draw_room_items(current_room)
        # Draw characters
        for currentSprite in self.onScreenChar:
            self.screen.blit(currentSprite.getCurrentSprite(), currentSprite.getRect().topleft)

        if self.showMinimap:
            self.draw_minimap()  
        else:
            title_surface = self.font_small.render("\"SHIFT\" for", True, (255, 215, 0))  
            title_rect = title_surface.get_rect(center=(ViewUnits.SCREEN_WIDTH-80, 30))
            self.screen.blit(title_surface, title_rect)
            title_surface1 = self.font_small.render("Minimap", True, (255, 215, 0))  
            title_rect1 = title_surface.get_rect(center=(ViewUnits.SCREEN_WIDTH-50, 50))
            self.screen.blit(title_surface, title_rect)
            self.screen.blit(title_surface1, title_rect1)
        if not self.bossRoom:
            self.ui.draw_boss_health(self.BossHealth, self.bossMaxHealth)  # Draw health  

        self.ui.draw_inventory(self.inventory)  # Draw inventory
        self.ui.draw_key_count(self.keyInventory)
        self.ui.draw_health(self.playerHealth, self.maxHealth)  # Draw health  
        pygame.display.flip()


    