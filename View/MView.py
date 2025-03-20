import os
import pygame
from .UI import UI
from .SpriteFactory import SpriteFactory
from ViewUnits import ViewUnits
from Model.GameWorld import GameWorld 
import random

class MView:
    """
    Handles rendering, UI management, and game state updates for the view.
    """
    def __init__(self):
        """
        Initializes the game view, loads assets, and sets up the UI.
        """
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
    
    def clear(self):
        """Clear the screen before drawing the next frame."""
        self.screen.fill((0, 0, 0))  # Fill screen with black

    def process_updates(self):
        """Process all updates and perform a single redraw if needed."""
        if self.needs_redraw:
            self.redrawCharacter()
            self.needs_redraw = False
    
    def updateBossHealthUI(self, event: pygame.event.Event):
        """
        Updates the boss health UI.

        :param event: Event containing boss health information.
        """
        self.BossHealth = event.health
        self.bossMaxHealth = event.maxHealth
        self.bossRoom = event.isdead
        self.needs_redraw = True
    
    def updateHealthUI(self, event: pygame.event.Event):
        """
        Updates player health UI.

        :param event: Event containing updated health information.
        """
        self.playerHealth = event.health
        self.maxHealth = event.maxHealth
        self.needs_redraw = True
    
    def updateInventoryUI(self, event: pygame.event.Event):
        """
        Updates player inventory UI.

        :param event: Event containing inventory updates.
        """
        self.inventory = event.inventory
        self.redrawCharacter()
    
    def updateKeyInventoryUI(self, event: pygame.event.Event):
        """
        Updates the key inventory UI.

        :param event: Event containing key count.
        """
        self.keyInventory = event.keyInventory
        self.redrawCharacter()   
    
    def updateRoom(self, event: pygame.event.Event):
        """Updates the room background and creates door sprites.
        The door that connects to a boss room uses a boss door sprite.
        """
        # Set background based on room type.
        if event.roomtype == "s ":
            self.theNewRoom = self.theTest
        elif event.roomtype == "k ":
            self.theNewRoom = self.keyRoomImage
        elif event.roomtype == "n ":
            self.theNewRoom = self.normalRoomImage
        elif event.roomtype == "b ":
            self.theNewRoom = self.normalRoomImage

        # Clear the current door list.
        self.myDoorList = []
        # Get the current room from GameWorld.
        current_room = GameWorld.getInstance().getCurrentRoom()
        door_map = current_room.getDoorMap()  # Should return a dictionary: direction -> Door object
        for direction, door in door_map.items():
            if door is None:
                continue
            connected_room = door.getConnectedRoom(current_room)
            if connected_room and connected_room.getRoomType().strip() == "b":
                # This door connects to a boss room – use the boss door sprite.
                door_sprite = self.mySpriteFactory.createSpriteSheet(
                    ord(direction), "BossDoor", 
                    self._getDoorX(direction), 
                    self._getDoorY(direction))
                if direction == "N":
                    door_sprite.setCurrentState("UP")
                elif direction == "S":
                    door_sprite.setCurrentState("DOWN")
                elif direction == "W":
                    door_sprite.setCurrentState("LEFT")
                elif direction == "E":
                    door_sprite.setCurrentState("RIGHT")
            else:
                # Use the normal door sprite.
                door_sprite = self.mySpriteFactory.createSpriteSheet(
                    ord(direction), "Door", 
                    self._getDoorX(direction), 
                    self._getDoorY(direction))
                # Set the door state based on direction.
                if direction == "N":
                    door_sprite.setCurrentState("UP")
                elif direction == "S":
                    door_sprite.setCurrentState("DOWN")
                elif direction == "W":
                    door_sprite.setCurrentState("LEFT")
                elif direction == "E":
                    door_sprite.setCurrentState("RIGHT")
            self.myDoorList.append(door_sprite)

        if self.onScreenChar:
            playerSprite = None
            for sprite in self.onScreenChar:
                if sprite.getName() in ["Dolphin", "Buddha", "Astronaut"]:
                    playerSprite = sprite
            self.onScreenChar = [playerSprite]
        self.cords = event.cords
    
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
    
    def update_game_won_screen(self):
        """Continuously updates the game won animations each frame."""
        
        # Redraw background
        self.screen.fill((0, 0, 50))  

        # Draw fireworks at random positions
        for _ in range(3):  
            x = random.randint(100, ViewUnits.SCREEN_WIDTH - 200)
            y = random.randint(50, ViewUnits.SCREEN_HEIGHT // 2)
            self.screen.blit(self.fireworks_image, (x, y))

        # Victory Text
        text_surface = self.font_big.render("YOU WON!", True, self.GOLD)
        glow_surface = self.font_big.render("YOU WON!", True, self.WHITE)
        text_rect = text_surface.get_rect(center=(ViewUnits.SCREEN_WIDTH // 2, ViewUnits.SCREEN_HEIGHT // 3))

        self.screen.blit(glow_surface, (text_rect.x - 2, text_rect.y - 2))  
        self.screen.blit(text_surface, text_rect)

        # Instruction text
        replay_text = self.font_small.render("Press ENTER to Restart, ESC to Quit", True, self.WHITE)
        replay_rect = replay_text.get_rect(center=(ViewUnits.SCREEN_WIDTH // 2, ViewUnits.SCREEN_HEIGHT // 1.5))
        self.screen.blit(replay_text, replay_rect)

        # Add new confetti particles randomly
        if random.randint(0, 5) == 0:  
            self.confetti_particles.append([
                random.randint(0, ViewUnits.SCREEN_WIDTH),  # X position
                0,  # Y starts at top
                random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)])  # Random colors
            ])

        # Move and draw confetti
        for particle in self.confetti_particles:
            pygame.draw.circle(self.screen, particle[2], (particle[0], particle[1]), 5)
            particle[1] += 3  # Move confetti down

        # Remove off-screen particles
        self.confetti_particles = [p for p in self.confetti_particles if p[1] < ViewUnits.SCREEN_HEIGHT]

        pygame.display.flip()  # Refresh screen
    
    def addCharacterToScreenList(self, theEvent:pygame.event):
        """
        adds characters to screen  
        """
        newCharSprite = self.mySpriteFactory.createSpriteSheet(theEvent.id, theEvent.name, theEvent.positionX,theEvent.positionY)
        self.onScreenChar.append(newCharSprite)

    def remove_projectile(self, theEvent:pygame.event):
        """Removes a projectile from the screen."""
        for i in range(len(self.onScreenChar)):
            if theEvent.id == self.onScreenChar[i].getId():
                self.onScreenChar.pop(i)
                break
        self.needs_redraw = True

    def display_game_won(self):
        """Displays 'You Won!' screen with animations that update every frame."""
        
        # Load assets
        assets_path = os.path.join(os.path.dirname(__file__), "..", "Assets")
        fireworks_image = pygame.image.load(os.path.join(assets_path, "Goat2.jpg"))
        fireworks_image = pygame.transform.scale(fireworks_image, (200, 200))  # Resize

        # Colors
        self.GOLD = (255, 215, 0)
        self.WHITE = (255, 255, 255)

        # Fonts
        self.font_big = pygame.font.Font(None, 100)
        self.font_small = pygame.font.Font(None, 40)

        # Set background color
        self.screen.fill((0, 0, 50))  

        # Create confetti storage
        self.confetti_particles = []  

        # Store fireworks image for repeated drawing
        self.fireworks_image = fireworks_image

        pygame.display.flip()  # Update screen

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

    def reset_view(self):
        """Clears the screen and resets the view state."""
        self.inventory.clear()
        
        self.screen.fill((0, 0, 0))  # Fill screen with black
        self.bossRoom = True
        self.onScreenChar.clear()
        self.showMinimap = False  # Hide minimap if needed
        pygame.display.update()  # Force screen update

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
            title_surface = self.font_small.render("\"LSHIFT\" for", True, (255, 215, 0))  
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
    
    def getScreen(self):
        """
        Returns the Pygame screen object.

        :return: The Pygame display screen.
        """
        return self.screen
    
    def _getDoorX(self, direction):
        """Helper function to get X position for doors based on direction."""
        if direction == "N":
            return ViewUnits.SOUTH_DOOR_CORD[0]
        elif direction == "S":
            return ViewUnits.NORTH_DOOR_CORD[0]
        elif direction == "W":
            return ViewUnits.EAST_DOOR_CORD[0]
        elif direction == "E":
            return ViewUnits.WEST_DOOR_CORD[0]
        return 0
    
    def _getDoorY(self, direction):
        """Helper function to get Y position for doors based on direction."""
        if direction == "N":
            return ViewUnits.SOUTH_DOOR_CORD[1]
        elif direction == "S":
            return ViewUnits.NORTH_DOOR_CORD[1]
        elif direction == "W":
            return ViewUnits.EAST_DOOR_CORD[1]
        elif direction == "E":
            return ViewUnits.WEST_DOOR_CORD[1]
        return 0

    