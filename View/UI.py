import os
import pygame
from ViewUnits import ViewUnits  # Assuming this exists
from .SpriteFactory import SpriteFactory
from Model.GameWorld import GameWorld 

class UI:
    def __init__(self, screen):
        """Initializes the UI class with a reference to the screen."""
        self.screen = screen
        font_path = os.path.join(os.path.dirname(__file__), "..", "Assets", "editundo.ttf")
        self.font_small = pygame.font.Font(font_path, 25)  # Small font for inventory
        self.font_med = pygame.font.Font(font_path, 37)
        self.font_large = pygame.font.Font(font_path, 50)  # Large font for health
        self.mySpriteFactory = SpriteFactory()
        self.inventory_start_x = 20  # Starting X position for the inventory
        self.inventory_start_y = ViewUnits.SCREEN_HEIGHT - 100  # Starting Y position (bottom left)
        self.inventory_icon_size = 50
        self.key_ui_x = 10
        self.key_ui_y = 50
    
    def draw_inventory(self, inventory):
        """Draw the player's inventory with a transparent background and transparent item images."""
        # Set the dimensions of the background for the inventory
        inventory_width = self.inventory_icon_size * 4 + 30  # 4 slots with spacing
        inventory_height = self.inventory_icon_size + 40  # Height for the slots + label space
        x_offset = self.inventory_start_x
        y_offset = self.inventory_start_y + 35

        # Create a surface for the inventory background with transparency
        inventory_surface = pygame.Surface((inventory_width + 10, inventory_height - 30), pygame.SRCALPHA)  # Use the SRCALPHA flag for transparency
        inventory_surface.fill((250, 250, 250, 150))  # Black background with alpha (transparency level: 150)
        # Draw the 4 slots inside the inventory with transparent white squares
        spacing = 10  # Space between items in the inventory
        slot_x_offset = 5  # Offset to avoid touching the edges
        slot_y_offset = 5
        for idx in range(4):  # We are always showing 4 slots
            # Check if there is an item in the current slot
            item = inventory[idx] if idx < len(inventory) else None  # If no item, the slot is empty

            # Draw the slot background (empty slot is a square with transparency)
            slot_rect = pygame.Rect(slot_x_offset + idx * (self.inventory_icon_size + spacing), slot_y_offset, self.inventory_icon_size, self.inventory_icon_size)
            pygame.draw.rect(inventory_surface, (255, 255, 255, 100), slot_rect)  # Semi-transparent white square for each slot

            # If the slot is not empty, draw the item image
            if item:
                if str(item) == "MockItem":
                    item_image = self.mySpriteFactory.healPotionImage  # Example: potion image from SpriteFactory
                elif str(item) == "InvincibilityItem":
                    item_image = self.mySpriteFactory.invincePotionImage
                elif str(item) == "SpeedItem":
                    item_image = self.mySpriteFactory.speedPotionImage                
                else:    
                    item_image = None  # Handle other item images if needed

                if item_image:
                    # Resize the item image to fit the inventory slot
                    item_image = pygame.transform.scale(item_image, (self.inventory_icon_size, self.inventory_icon_size))
                    inventory_surface.blit(item_image, (slot_x_offset + idx * (self.inventory_icon_size + spacing), slot_y_offset))

            # No label or "Empty" text for empty slots, just leave them blank

        # Now blit the transparent inventory surface onto the main screen
        self.screen.blit(inventory_surface, (x_offset, y_offset))

    def draw_key_count(self, key_count):
        """Draws the key count on the left side of the screen with a key icon and the count."""
        x = self.key_ui_x
        y = self.key_ui_y
        key_icon = self.mySpriteFactory.keyImage 
        key_icon = pygame.transform.scale(key_icon, (35, 50))
        self.screen.blit(key_icon, (x, y))
        text = f"x{key_count}"
        font = self.font_small
        text_surface = font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x + 28, y + 20))

    def draw_health(self, player_health, max_health):
        """Draw the player's health as a bar with a border and a heart icon on the left,
        positioned in the bottom right of the screen. The bar color changes depending on health.
        """
        bar_width = 400 
        bar_height = 30   
        right_margin = 10
        bottom_margin = 20
        x_offset = ViewUnits.SCREEN_WIDTH - bar_width - right_margin
        y_offset = ViewUnits.SCREEN_HEIGHT - bar_height - bottom_margin

        border_color = (20, 0, 0)  
        pygame.draw.rect(self.screen, border_color, 
                 (x_offset - 2, y_offset - 2, bar_width + 4, bar_height + 4), 
                 4,  # This width parameter draws only the border (4 pixels thick)
                 border_radius=10)

        health_bg_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
        health_bg_surface.fill((200, 0, 0, 0))  # Fully transparent fill (alpha=0)
        self.screen.blit(health_bg_surface, (x_offset, y_offset))
    
        health_percentage = player_health / max_health
        health_bar_width = bar_width * health_percentage

        if health_percentage > 0.7:
            bar_color = (160, 0, 0)  
        elif health_percentage > 0.3:
            bar_color = (120, 0, 0) 
        else:
            bar_color = (80, 0, 0) 

        pygame.draw.rect(self.screen, bar_color, 
                        (x_offset, y_offset, health_bar_width, bar_height), 
                        border_radius=10)

        text_surface = self.font_med.render(f"{player_health}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x_offset + 65, y_offset + bar_height // 2))
        self.screen.blit(text_surface, text_rect)
        
        heart_icon_size = 65
        heart_x = x_offset - heart_icon_size + 30
        heart_y = y_offset + (bar_height - heart_icon_size) // 2 
        heart_sprite = self.mySpriteFactory.heartImage  
        heart_sprite = pygame.transform.scale(heart_sprite, (heart_icon_size, heart_icon_size))
        self.screen.blit(heart_sprite, (heart_x, heart_y))



    def draw_boss_health(self, enemy_health, max_health):
        """Draw the boss's health bar with a thick border, a semi-transparent background,
        and a boss icon on the left side.
        """
        bar_width = 600   # Width of the health bar
        bar_height = 10   # Height of the health bar
        # Position the health bar at the top-center of the screen
        x_offset = (ViewUnits.SCREEN_WIDTH - bar_width) // 2
        y_offset = 30  # Distance from the top

        # Draw a thick dark red border around the boss health bar
        border_color = (200, 0, 0)
        border_thickness = 4
        pygame.draw.rect(self.screen, border_color, 
                        (x_offset - 2, y_offset - 2, bar_width + 4, bar_height + 4), 
                        border_radius=10)

        # Create a semi-transparent background surface with a tint for the boss health bar
        bg_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
        bg_surface.fill((50, 50, 50, 150))  # Dark gray with transparency
        self.screen.blit(bg_surface, (x_offset, y_offset))

        # Calculate the width of the boss health bar based on enemy health
        health_percentage = enemy_health / max_health
        health_bar_width = bar_width * health_percentage

        bar_color = (160, 0, 0)
        pygame.draw.rect(self.screen, bar_color, 
                        (x_offset, y_offset, health_bar_width, bar_height), 
                        border_radius=10)

        # Render the boss health text using the pixelated font
        text_surface = self.font_med.render(f"{enemy_health}/{max_health}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x_offset + bar_width // 2 - 200, y_offset + bar_height // 2))
        self.screen.blit(text_surface, text_rect)

        # Define boss icon parameters
        boss_icon_size = 60
        # Position the boss icon to the left of the health bar, with a gap of 10 pixels
        icon_x = x_offset - boss_icon_size +30
        icon_y = y_offset + (bar_height - boss_icon_size) // 2

        # Retrieve the boss icon from SpriteFactory (use a dedicated boss image if available;
        # otherwise, you can use the crab image as a placeholder)
        boss_icon = self.mySpriteFactory.skullImage  # Replace with a dedicated boss image if available
        boss_icon = pygame.transform.scale(boss_icon, (boss_icon_size, boss_icon_size))
        self.screen.blit(boss_icon, (icon_x, icon_y))


    def draw_room_coordinates(self, cords):
        """Draw the room coordinates at the center of the screen."""
        if cords:
            text_surface = self.font_large.render(f"Room: {cords}", True, (0, 0, 0))  # Black text
            text_rect = text_surface.get_rect(center=(ViewUnits.SCREEN_WIDTH // 2, ViewUnits.SCREEN_HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)
